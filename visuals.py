"""Charts and tables for the hitter report, drawn by code from the database.

    .venv/bin/python visuals.py "Wilyer Abreu"                      # draw the images
    .venv/bin/python visuals.py "Wilyer Abreu" reports/<report>.md  # draw + insert into a report

Same rule as data.py: code computes, the model judges. Every number in a visual comes
straight from the same rows the data packet is built from. Images, not markdown tables,
because Substack does not render markdown tables.

Shading: a cell is colored by the hitter's percentile among qualified hitters that
season (red = better, blue = worse). Metrics with no better direction are not shaded.
"""

import re
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import psycopg
from psycopg.rows import dict_row

import data
from data import fmt, pct

HERE = Path(__file__).resolve().parent

# Savant-style scale: blue (0th percentile) -> grey (50th) -> red (100th).
SCALE = LinearSegmentedColormap.from_list("pctile", ["#3661ad", "#d8d8d8", "#d22d49"])
TEXT, MUTED, RULE = "#1d1d1f", "#6e6e73", "#d2d2d7"

# Percentile chart, grouped like the report. (label, column, better direction)
CHART_GROUPS = [
    ("Expected stats", [("xwOBA", "xwoba", "higher"), ("xBA", "xba", "higher"), ("xISO", "xiso", "higher")]),
    ("Batted-ball profile", [("EV90", "ev90", "higher"), ("Hard-hit%", "hard_hit_pct", "higher"),
                             ("Barrel%", "barrel_pct", "higher"), ("Pulled Air%", "pulled_fb_pct", "higher")]),
    ("Plate discipline", [("IZ Swing − Chase", "swing_score", "higher"), ("Chase%", "chase_pct", "lower"),
                          ("Whiff%", "whiff_pct", "lower"), ("K%", "k_pct", "lower"), ("BB%", "bb_pct", "higher")]),
    ("Speed", [("Sprint speed", "sprint_speed", "higher")]),
]

# Season tables: (header, column, better direction or None)
EXPECTED_COLS = [("xwOBA", "xwoba", "higher"), ("xBA", "xba", "higher"), ("xISO", "xiso", "higher"),
                 ("wOBA", "woba", "higher")]
BATTED_COLS = [("EV90", "ev90", "higher"), ("Hard-hit%", "hard_hit_pct", "higher"),
               ("Barrel%", "barrel_pct", "higher"), ("LA median", "median_la", None),
               ("LA SD", "sd_la", "lower"), ("Pulled Air%", "pulled_fb_pct", "higher"), ("GB%", "gb_pct", None)]
DISCIPLINE_COLS = [("IZ Swing%", "z_swing_pct", None), ("Chase%", "chase_pct", "lower"),
                   ("IZ Swing − Chase", "swing_score", "higher"), ("Whiff%", "whiff_pct", "lower"),
                   ("K%", "k_pct", "lower"), ("BB%", "bb_pct", "higher")]
PLATOON_COLS = [("xwOBA", "xwoba"), ("xBA", "xba"), ("xISO", "xiso"), ("EV90", "ev90"), ("Barrel%", "barrel_pct"),
                ("GB%", "gb_pct"), ("Chase%", "chase_pct"), ("Whiff%", "whiff_pct"), ("K%", "k_pct"),
                ("BB%", "bb_pct")]
PITCH_COLS = [("Share", "pitch_share", None), ("Chase%", "chase_pct", "lower"), ("Whiff%", "whiff_pct", "lower"),
              ("xwOBA", "xwoba", "higher"), ("EV90", "ev90", "higher"), ("Barrel%", "barrel_pct", "higher")]

MIN_PA_SHOWN = 100  # seasons below this are left out of the tables (no read, per the method)


# ---------------------------------------------------------------- numbers

def percentile(value, league, col, better):
    """Same definition as the packet: share of qualified hitters he ranks ahead of (100 = best)."""
    values = [r[col] for r in league if r[col] is not None]
    if value is None or better is None or len(values) < 2:
        return None
    rank = 1 + sum(v > value if better == "higher" else v < value for v in values)
    return round(100 * (len(values) - rank) / (len(values) - 1))


def average(league, col):
    values = [r[col] for r in league if r[col] is not None]
    return sum(values) / len(values) if values else None


def fetch(name):
    """Everything the visuals need, from the same queries as the data packet."""
    with psycopg.connect(data.CONNINFO, autocommit=True, row_factory=dict_row) as conn, conn.cursor() as cur:
        player = data.resolve_player(cur, name)
        rows = data.fetch_seasons(cur, player["player_id"])
        full = [r for r in rows if r["split"] == "all"]
        latest = full[-1]
        recent = [r for r in full[-3:] if r["pa"] >= MIN_PA_SHOWN]
        leagues = {r["season"]: data.fetch_league(cur, r["season"])[0] for r in recent}
        min_pa = data.QUALIFIED_PA.get(latest["season"], data.DEFAULT_QUALIFIED_PA)
        groups = [g for g in data.fetch_pitch_groups(cur, player["player_id"], latest["season"])
                  if g["season"] == latest["season"]]
        league_groups = data.fetch_league_pitch_groups(cur, latest["season"], min_pa)
    splits = {r["split"]: r for r in rows if r["season"] == latest["season"] and r["split"] != "all"}
    return dict(player=player, latest=latest, recent=recent, leagues=leagues, splits=splits,
                groups=groups, league_groups=league_groups)


# ---------------------------------------------------------------- drawing

def style_axes(ax):
    ax.set_axis_off()
    ax.set_xlim(0, 1)


def percentile_chart(d, path):
    latest, league = d["latest"], d["leagues"][d["latest"]["season"]]
    lines = []  # ("group", title) or ("bar", label, value text, percentile)
    for title, metrics in CHART_GROUPS:
        bars = [(label, fmt(col, latest[col]), percentile(latest[col], league, col, better))
                for label, col, better in metrics]
        bars = [b for b in bars if b[2] is not None]
        if bars:
            lines.append(("group", title))
            lines += [("bar",) + b for b in bars]

    row_h = 0.42
    fig, ax = plt.subplots(figsize=(8, 0.95 + row_h * len(lines)), dpi=200)
    style_axes(ax)
    ax.set_ylim(len(lines) + 0.4, -1.6)
    name = d["player"]["full_name"]
    ax.text(0, -1.2, f"{name} · {latest['season']} percentile rankings", fontsize=14, weight="bold", color=TEXT)
    ax.text(0, -0.55, f"vs. {len(league)} qualified hitters · 100 = best · red = better, blue = worse",
            fontsize=9, color=MUTED)
    x0, x1 = 0.36, 0.90
    for i, line in enumerate(lines):
        if line[0] == "group":
            ax.text(0, i + 0.15, line[1].upper(), fontsize=8.5, weight="bold", color=MUTED)
            continue
        _, label, value, p = line
        ax.text(0.02, i, label, fontsize=10.5, color=TEXT, va="center")
        ax.text(x0 - 0.02, i, value, fontsize=10.5, color=MUTED, va="center", ha="right")
        ax.plot([x0, x1], [i, i], color="#ececec", lw=7, solid_capstyle="round", zorder=1)
        end = x0 + (x1 - x0) * p / 100
        ax.plot([x0, end], [i, i], color=SCALE(p / 100), lw=7, solid_capstyle="round", zorder=2)
        ax.scatter([end], [i], s=260, color=SCALE(p / 100), edgecolor="white", linewidth=1.5, zorder=3)
        ax.text(end, i, str(p), fontsize=7.5, color="white" if abs(p - 50) > 20 else TEXT, weight="bold", ha="center", va="center", zorder=4)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def table_image(title, subtitle, headers, rows, shades, path, avg_row=None):
    """rows: lists of display strings; shades: same shape, a percentile or None per cell."""
    all_rows = rows + ([avg_row] if avg_row else [])
    n_cols = len(headers)
    first_w = 0.17
    col_w = (1 - first_w) / (n_cols - 1)
    xs = [first_w / 2] + [first_w + col_w * (j + 0.5) for j in range(n_cols - 1)]
    row_h = 0.5
    fig, ax = plt.subplots(figsize=(max(7.5, 1.0 + 0.95 * n_cols), 1.25 + row_h * (len(all_rows) + 1)), dpi=200)
    style_axes(ax)
    ax.set_ylim(len(all_rows) + 0.6, -2.2)
    ax.text(0, -1.75, title, fontsize=13, weight="bold", color=TEXT)
    ax.text(0, -1.15, "\n".join(textwrap.wrap(subtitle, 110)), fontsize=8.5, color=MUTED, va="center")
    for j, h in enumerate(headers):
        ax.text(xs[j], 0, h.replace(" − ", "\n− "), fontsize=9, weight="bold", color=MUTED, ha="center", va="center")
    ax.plot([0, 1], [0.5, 0.5], color=RULE, lw=1)
    for i, row in enumerate(all_rows, start=1):
        is_avg = avg_row is not None and i == len(all_rows)
        if is_avg:
            ax.plot([0, 1], [i - 0.5, i - 0.5], color=RULE, lw=1)
        for j, cell in enumerate(row):
            p = None if is_avg or j == 0 else shades[i - 1][j]
            if p is not None:
                ax.add_patch(plt.Rectangle((xs[j] - col_w * 0.44, i - 0.36), col_w * 0.88, 0.72,
                                           color=SCALE(p / 100), alpha=0.75, lw=0))
            ax.text(xs[j], i, cell, fontsize=10, ha="center", va="center",
                    color=MUTED if is_avg else TEXT, weight="bold" if j == 0 and not is_avg else "normal",
                    style="italic" if is_avg else "normal")
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def season_table(d, title, cols, path, extra_first=("PA", "pa")):
    recent, leagues = d["recent"], d["leagues"]
    season = d["latest"]["season"]
    headers = ["Season", extra_first[0]] + [h for h, _, _ in cols]
    rows, shades = [], []
    for r in recent:
        lg = leagues[r["season"]]
        rows.append([str(r["season"]), str(r[extra_first[1]])] + [fmt(c, r[c]) for _, c, _ in cols])
        shades.append([None, None] + [percentile(r[c], lg, c, b) for _, c, b in cols])
    lg = leagues[season]
    avg = [f"{season} avg", "—"] + [fmt(c, average(lg, c)) for _, c, _ in cols]
    table_image(title, f"Seasons with {MIN_PA_SHOWN}+ PA · shading = percentile vs. qualified hitters that season "
                       "(red = better, blue = worse)", headers, rows, shades, path, avg)


def platoon_table(d, path):
    s, latest = d["splits"], d["latest"]
    order = [("vs LHP", s.get("vs_lhp")), ("vs RHP", s.get("vs_rhp")), ("Overall", latest)]
    headers = ["Split", "PA"] + [h for h, _ in PLATOON_COLS]
    rows = [[label, str(r["pa"])] + [fmt(c, r[c]) for _, c in PLATOON_COLS] for label, r in order if r]
    shades = [[None] * len(headers) for _ in rows]
    table_image(f"{latest['season']} platoon profile", "Bottom row is the full season, for reference",
                headers, rows[:-1], shades[:-1], path, avg_row=rows[-1])


def pitch_table(d, path):
    groups, lg_all = d["groups"], d["league_groups"]
    season = d["latest"]["season"]
    headers = ["Pitch group", "PA ending"] + [h for h, _, _ in PITCH_COLS]
    rows, shades = [], []
    for g in data.PITCH_GROUPS:
        r = next((x for x in groups if x["pitch_group"] == g), None)
        if r is None:
            continue
        lg = [x for x in lg_all if x["pitch_group"] == g]
        rows.append([g.capitalize(), str(r["pa"])] + [fmt(c, r[c]) for _, c, _ in PITCH_COLS])
        shades.append([None, None] + [percentile(r[c], lg, c, b) for _, c, b in PITCH_COLS])
    table_image(f"{season} vs. pitch type",
                "Share, Chase% and Whiff% count every pitch seen; xwOBA, EV90 and Barrel% count PA ending on the "
                "group · shading vs. qualified hitters on that group", headers, rows, shades, path)


def draw_all(name):
    d = fetch(name)
    slug = re.sub(r"[^a-z0-9]+", "-", d["player"]["full_name"].lower()).strip("-")
    out = HERE / "reports" / "visuals" / slug
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "top": out / "percentiles.png",
        "expected": out / "expected_stats.png",
        "batted": out / "batted_ball.png",
        "discipline": out / "plate_discipline.png",
        "platoon": out / "platoon.png",
        "pitch": out / "pitch_type.png",
    }
    percentile_chart(d, files["top"])
    season_table(d, "Expected stats (house model)", EXPECTED_COLS, files["expected"])
    season_table(d, "Batted-ball profile", BATTED_COLS, files["batted"], extra_first=("BBE", "bbe"))
    season_table(d, "Plate discipline", DISCIPLINE_COLS, files["discipline"])
    platoon_table(d, files["platoon"])
    pitch_table(d, files["pitch"])
    return files


# Which image goes under which report heading.
PLACEMENT = {"## Top line": "top", "## Expected stats": "expected", "## Batted-ball profile": "batted",
             "## Plate discipline": "discipline", "## Platoon profile": "platoon", "## Vs. pitch type": "pitch"}


def insert_into_report(report_path, files):
    """Write <report>_visual.md with each image placed right under its section heading."""
    report_path = Path(report_path).resolve()
    out_lines = []
    for line in report_path.read_text().splitlines():
        out_lines.append(line)
        key = PLACEMENT.get(line.strip())
        if key:
            rel = Path("visuals") / files[key].parent.name / files[key].name
            out_lines += ["", f"![{line.strip('# ')}]({rel.as_posix()})"]
    out = report_path.with_name(report_path.stem + "_visual.md")
    out.write_text("\n".join(out_lines) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit('usage: python visuals.py "Player Name" [reports/<report>.md]')
    try:
        files = draw_all(sys.argv[1])
    except ValueError as e:
        sys.exit(str(e))
    for f in files.values():
        print(f.relative_to(HERE))
    if len(sys.argv) == 3:
        print(insert_into_report(sys.argv[2], files).relative_to(HERE))
