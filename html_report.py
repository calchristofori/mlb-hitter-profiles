"""Interactive HTML version of a hitter report.

    .venv/bin/python html_report.py "Wilyer Abreu" reports/<report>.md

Same rule as data.py: code computes, the model judges. The numbers, percentiles and
league averages come from the database (the same queries as the data packet); the
writing comes from the report Claude wrote. Output: reports/html/<player>.html
"""

import html
import json
import re
import sys
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

import data
from data import fmt

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "templates" / "report.html"
MIN_PA_SHOWN = 100  # seasons below this are left out (no read, per the method)

# (column, label, better direction, short definition for the hover card)
METRICS = {
    "xwoba": ("xwOBA", "higher", "Expected wOBA from the quality of his contact (exit velocity and launch angle), "
                                 "plus his actual strikeouts and walks. House model."),
    "xba": ("xBA", "higher", "Expected batting average from his contact quality. Strikeouts pull it down. House model."),
    "xiso": ("xISO", "higher", "Expected isolated power: xSLG minus xBA. The extra bases his contact should produce per at-bat."),
    "woba": ("wOBA", "higher", "Weighted on-base average: every way of reaching base, weighted by its run value."),
    "ev90": ("EV90", "higher", "His 90th-percentile exit velocity (mph). How hard he hits the ball at the top end."),
    "hard_hit_pct": ("Hard-hit%", "higher", "Share of batted balls hit 95 mph or harder."),
    "barrel_pct": ("Barrel%", "higher", "Share of batted balls hit at the exit velocity and launch angle that most often "
                                        "become extra-base hits."),
    "sweet_spot_pct": ("Sweet spot%", "higher", "Share of batted balls with a launch angle of 8 to 32 degrees."),
    "median_la": ("LA median", None, "His median launch angle in degrees. Higher means more balls in the air."),
    "sd_la": ("LA SD", "lower", "How spread out his launch angles are. Lower means a more consistent swing path."),
    "pulled_fb_pct": ("Pulled Air%", "higher", "Fly balls, line drives and popups hit to his pull side, as a share of "
                                               "batted balls. Not the same as FB%."),
    "gb_pct": ("GB%", None, "Share of batted balls hit on the ground."),
    "z_swing_pct": ("IZ Swing%", None, "How often he swings at pitches in the strike zone."),
    "chase_pct": ("Chase%", "lower", "How often he swings at pitches outside the strike zone."),
    "swing_score": ("IZ Swing − Chase", "higher", "In-zone swing rate minus chase rate. Generally higher is better: he "
                                                  "attacks strikes and lays off balls. Not a swing-decision score."),
    "whiff_pct": ("Whiff%", "lower", "Share of his swings that miss."),
    "k_pct": ("K%", "lower", "Strikeouts per plate appearance."),
    "bb_pct": ("BB%", "higher", "Walks per plate appearance."),
    "sprint_speed": ("Sprint speed", "higher", "Feet per second on competitive runs. About 27 is average, 30+ elite."),
    "pitch_share": ("Share", None, "Share of the pitches he saw that came from this group. How pitchers attack him."),
}

PERCENTILE_GROUPS = [
    ("Expected stats", ["xwoba", "xba", "xiso"]),
    ("Batted-ball profile", ["ev90", "hard_hit_pct", "barrel_pct", "pulled_fb_pct"]),
    ("Plate discipline", ["swing_score", "chase_pct", "whiff_pct", "k_pct", "bb_pct"]),
    ("Speed", ["sprint_speed"]),
]
TABLES = {
    "expected": ["xwoba", "xba", "xiso", "woba"],
    "batted": ["ev90", "hard_hit_pct", "barrel_pct", "median_la", "sd_la", "pulled_fb_pct", "gb_pct"],
    "discipline": ["z_swing_pct", "chase_pct", "swing_score", "whiff_pct", "k_pct", "bb_pct"],
}
PLATOON = ["xwoba", "xba", "xiso", "ev90", "barrel_pct", "gb_pct", "chase_pct", "whiff_pct", "k_pct", "bb_pct"]
PITCH = ["pitch_share", "chase_pct", "whiff_pct", "swing_score", "xwoba", "ev90", "barrel_pct"]
SECTIONS = {"Top line": "top", "Expected stats": "expected", "Batted-ball profile": "batted",
            "Plate discipline": "discipline", "Platoon profile": "platoon", "Vs. pitch type": "pitch",
            "Synthesis": "synthesis", "Sample notes": "notes"}


# ---------------------------------------------------------------- numbers

def stat(row, col, league):
    """One metric for one row: display value, raw value, and where it stands in the league."""
    value = row.get(col)
    label, better, _ = METRICS[col]
    values = [r[col] for r in league if r.get(col) is not None]
    out = {"v": fmt(col, value), "raw": value,
           "avg": fmt(col, sum(values) / len(values)) if values else "—"}
    if better and value is not None and len(values) > 1:
        rank = 1 + sum(v > value if better == "higher" else v < value for v in values)
        out.update(rank=rank, of=len(values), p=round(100 * (len(values) - rank) / (len(values) - 1)))
    if values:  # range of the middle 90% of qualified hitters, to scale the platoon chart
        s = sorted(values)
        out["lo"], out["hi"] = s[int(0.05 * (len(s) - 1))], s[int(0.95 * (len(s) - 1))]
        out["avgRaw"] = sum(values) / len(values)
    return out


def build(name, report_path):
    with psycopg.connect(data.CONNINFO, autocommit=True, row_factory=dict_row) as conn, conn.cursor() as cur:
        player = data.resolve_player(cur, name)
        rows = data.fetch_seasons(cur, player["player_id"])
        full = [r for r in rows if r["split"] == "all"]
        latest = full[-1]
        recent = [r for r in full[-3:] if r["pa"] >= MIN_PA_SHOWN]
        leagues = {r["season"]: data.fetch_league(cur, r["season"])[0] for r in recent}
        min_pa = data.QUALIFIED_PA.get(latest["season"], data.DEFAULT_QUALIFIED_PA)
        groups = data.fetch_pitch_groups(cur, player["player_id"], latest["season"] - 2)
        league_groups = data.fetch_league_pitch_groups(cur, latest["season"], min_pa)
        team = data.fetch_current_team(cur, player["player_id"])
        data_through = data.fetch_data_through(cur, latest["season"])

    season = latest["season"]
    lg = leagues[season]
    splits = {r["split"]: r for r in rows if r["season"] == season and r["split"] != "all"}

    seasons = [{"season": r["season"], "pa": r["pa"], "bbe": r["bbe"], "qualified": r["pa"] >= min_pa,
                "league": len(leagues[r["season"]]),
                "stats": {c: stat(r, c, leagues[r["season"]]) for c in METRICS if c != "pitch_share"}}
               for r in recent]

    platoon = [{"key": k, "label": lab, "pa": r["pa"], "stats": {c: stat(r, c, lg) for c in PLATOON}}
               for k, lab, r in [("lhp", "vs LHP", splits.get("vs_lhp")), ("rhp", "vs RHP", splits.get("vs_rhp")),
                                 ("all", "Overall", latest)] if r]

    pitch = []
    for g in data.PITCH_GROUPS:
        lg_g = [x for x in league_groups if x["pitch_group"] == g]
        mine = [x for x in groups if x["pitch_group"] == g]
        cur_row = next((x for x in mine if x["season"] == season), None)
        if cur_row is None:
            continue
        pitch.append({
            "group": g, "pa": cur_row["pa"], "pitches": cur_row["pitches"],
            "leagueShare": fmt("pitch_share", sum(x["pitch_share"] for x in lg_g) / len(lg_g)),
            "leagueShareRaw": sum(x["pitch_share"] for x in lg_g) / len(lg_g),
            "stats": {c: stat(cur_row, c, lg_g) for c in PITCH},
            "history": [{"season": x["season"], "share": fmt("pitch_share", x["pitch_share"]),
                         "shareRaw": x["pitch_share"], "whiff": fmt("whiff_pct", x["whiff_pct"]),
                         "chase": fmt("chase_pct", x["chase_pct"])} for x in mine],
        })

    title, sections = parse_report(Path(report_path).read_text())
    return {
        "player": {"name": player["full_name"], "pos": latest["pos"], "bats": latest["bats"],
                   "throws": latest["throws"], "age": latest["age"], "season": season, "pa": latest["pa"],
                   "team": team["team_full_name"] if team else latest["teams"], "dataThrough": str(data_through)},
        "metrics": {c: {"label": m[0], "better": m[1], "def": m[2]} for c, m in METRICS.items()},
        "percentileGroups": PERCENTILE_GROUPS, "tables": TABLES, "platoonCols": PLATOON, "pitchCols": PITCH,
        "seasons": seasons, "platoon": platoon, "pitch": pitch,
        "report": {"title": title, "sections": sections, "source": Path(report_path).name},
    }


# ---------------------------------------------------------------- report text

def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)


def parse_report(md):
    """Split the report into its sections, each as HTML paragraphs."""
    title, sections, key, buf = "", {}, None, []

    def flush():
        if key:
            paras = [p.strip().replace("\n", " ") for p in "\n".join(buf).split("\n\n") if p.strip()]
            sections[key] = "".join(f"<p>{inline(p)}</p>" for p in paras)

    for line in md.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            key, buf = SECTIONS.get(line[3:].strip(), line[3:].strip()), []
        else:
            buf.append(line)
    flush()
    return title, sections


def write(name, report_path):
    bundle = build(name, report_path)
    page = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(bundle).replace("</", "<\\/"))
    page = page.replace("__TITLE__", html.escape(bundle["player"]["name"]))
    slug = re.sub(r"[^a-z0-9]+", "-", bundle["player"]["name"].lower()).strip("-")
    out = HERE / "reports" / "html" / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('usage: python html_report.py "Player Name" reports/<report>.md')
    try:
        print(write(sys.argv[1], sys.argv[2]).relative_to(HERE))
    except ValueError as e:
        sys.exit(str(e))
