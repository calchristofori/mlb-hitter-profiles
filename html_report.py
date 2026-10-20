"""Interactive HTML version of a hitter report.

    .venv/bin/python html_report.py "Wilyer Abreu" reports/<report>.md

Same rule as data.py: code computes, the model judges. The numbers, percentiles and
league averages come from the database (the same queries as the data packet); the
writing comes from the report Claude wrote.

Output goes to docs/, which GitHub Pages publishes as the website:
    docs/<player>.html   the player's page
    docs/index.html      home page listing every player (rebuilt from docs/players.json)
    docs/img/            percentile chart image, used as the link preview (Substack, social)
"""

import html
import json
import re
import sys
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

import data
import visuals
from data import fmt

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "templates" / "report.html"
SITE = HERE / "docs"
SITE_URL = "https://calchristofori.github.io/mlb-hitter-profiles/"
REPO_URL = "https://github.com/calchristofori/mlb-hitter-profiles"

# The page template is written for the claude.ai preview, which supplies the document
# shell. For the website, each page gets its own shell and the same base reset.
SHELL_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{meta}
<style>
:root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; font: 14px/1.5 system-ui, -apple-system, sans-serif; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
"""
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
        usage_raw = data.usage_rows(rows, full)
        usage_league = {u["season"]: data.fetch_usage_league(cur, u["season"], u["bats"]) for u in usage_raw}

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

    usage = []
    for u in usage_raw:
        lg = usage_league.get(u["season"], [])
        if u["lhp"] is None or not lg:
            continue
        share, avg = u["lhp"] / u["pa"], sum(lg) / len(lg)
        usage.append({"season": u["season"], "pa": u["pa"], "lhp": u["lhp"], "share": share, "shareV": fmt("pitch_share", share),
                      "avg": avg, "avgV": fmt("pitch_share", avg), "n": len(lg), "bats": u["bats"],
                      "p": min(100, round(100 * sum(v < share for v in lg) / (len(lg) - 1))) if len(lg) > 1 else None})

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
        "seasons": seasons, "platoon": platoon, "usage": usage, "usageMinPa": data.USAGE_MIN_PA, "pitch": pitch,
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


def shell(head, body, title, description, image=None, url=None):
    """A complete web page: document shell, link-preview tags, then the page itself."""
    tags = [f'<meta name="description" content="{html.escape(description)}">',
            f'<meta property="og:title" content="{html.escape(title)}">',
            f'<meta property="og:description" content="{html.escape(description)}">',
            '<meta property="og:type" content="article">']
    if url:
        tags.append(f'<meta property="og:url" content="{url}">')
    if image:
        tags += [f'<meta property="og:image" content="{image}">', '<meta name="twitter:card" content="summary_large_image">']
    return SHELL_HEAD.format(meta="\n".join(tags)) + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"


def plain(html_text):
    return re.sub(r"<[^>]+>", "", html_text).strip()


def write(name, report_path):
    bundle = build(name, report_path)
    p = bundle["player"]
    slug = re.sub(r"[^a-z0-9]+", "-", p["name"].lower()).strip("-")
    page = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(bundle).replace("</", "<\\/"))
    page = page.replace("__TITLE__", html.escape(p["name"])).replace("__REPO__", REPO_URL)
    head, body = page.split('<div class="wrap">', 1)
    body = '<div class="wrap">' + body

    # Percentile chart image for the link preview.
    (SITE / "img").mkdir(parents=True, exist_ok=True)
    visuals.percentile_chart(visuals.fetch(name), SITE / "img" / f"{slug}-percentiles.png")

    top = plain(bundle["report"]["sections"].get("top", ""))
    out = SITE / f"{slug}.html"
    out.write_text(shell(head, body, f"{p['name']} Hitter Profile", top,
                         image=f"{SITE_URL}img/{slug}-percentiles.png", url=f"{SITE_URL}{slug}.html"))
    update_index(slug, p, top, Path(report_path).name)
    return out


# ---------------------------------------------------------------- home page

def update_index(slug, p, top, source):
    manifest_path = SITE / "players.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest[slug] = {"name": p["name"], "pos": p["pos"], "team": p["team"], "age": p["age"], "bats": p["bats"],
                      "season": p["season"], "pa": p["pa"], "dataThrough": p["dataThrough"], "top": top,
                      "source": source}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    (SITE / ".nojekyll").touch()  # serve files as they are, no GitHub build step

    cards = "".join(f"""
    <a class="player" href="{s}.html">
      <span class="pname">{html.escape(m['name'])}</span>
      <span class="pmeta">{html.escape(m['pos'])} · {html.escape(m['team'])} · Age {m['age']} · Bats {m['bats']} · {m['pa']} PA</span>
      <span class="ptop">{html.escape(m['top'])}</span>
    </a>""" for s, m in sorted(manifest.items(), key=lambda kv: kv[1]["name"].split()[-1]))
    head = INDEX_HEAD
    body = f"""<div class="wrap">
  <header>
    <div class="eyebrow">Hitter profiles · built with the Claude API</div>
    <h1>MLB Hitter Profiles</h1>
    <p class="intro">Scouting-style profiles of MLB hitters. Every number and chart is computed by code from a
    pitch-by-pitch database; the writing is by Claude, working only from those numbers and a written evaluation
    method. <a href="{REPO_URL}">See how it's built</a>.</p>
  </header>
  <div class="list">{cards}
  </div>
</div>"""
    description = "Scouting-style MLB hitter profiles: charts computed from pitch-by-pitch data, written by Claude."
    (SITE / "index.html").write_text(shell(head, body, "MLB Hitter Profiles", description, url=SITE_URL))


INDEX_HEAD = """<title>MLB Hitter Profiles</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400&display=swap">
<style>
:root { --bg: #f4f5f7; --paper: #ffffff; --ink: #15181e; --muted: #5b6270; --rule: #e0e3e9; --accent: #1d3557;
  --display: "Barlow Condensed", "Arial Narrow", Arial, sans-serif; --ui: "Barlow", "Helvetica Neue", Arial, sans-serif;
  --prose: "Source Serif 4", Georgia, serif; }
@media (prefers-color-scheme: dark) { :root { --bg: #0e1014; --paper: #161920; --ink: #e8eaef; --muted: #9ba2ae;
  --rule: #2a2f39; --accent: #a9c1e3; color-scheme: dark; } }
body { background: var(--bg); color: var(--ink); font-family: var(--ui); }
.wrap { max-width: 860px; margin: 0 auto; padding-block: 40px 64px; display: grid; gap: 28px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.eyebrow { font: 600 12px/1 var(--ui); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
h1 { font: 700 clamp(42px, 8vw, 68px)/.95 var(--display); text-transform: uppercase; margin: 10px 0 14px; }
.intro { font: 400 18px/1.55 var(--prose); max-width: 40em; margin: 0; }
a { color: var(--accent); }
.list { display: grid; gap: 12px; }
.player { display: grid; gap: 6px; background: var(--paper); border: 1px solid var(--rule); border-radius: 10px;
  padding: 18px 22px; text-decoration: none; color: var(--ink); }
.player:hover, .player:focus-visible { border-color: var(--accent); }
.player:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.pname { font: 600 28px/1 var(--display); text-transform: uppercase; }
.pmeta { color: var(--muted); font-size: 13px; }
.ptop { font: 400 16px/1.5 var(--prose); }
</style>"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('usage: python html_report.py "Player Name" reports/<report>.md')
    try:
        print(write(sys.argv[1], sys.argv[2]).relative_to(HERE))
    except ValueError as e:
        sys.exit(str(e))
