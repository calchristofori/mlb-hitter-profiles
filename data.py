"""Step 1 of the hitter report workflow: build the data packet.

    python data.py "Pete Crow-Armstrong"

Everything here is deterministic: no AI. Given a player name, it pulls every number
the hitter report needs from the `mlb` database and returns it as one block of text
(the "data packet") that later goes to the model.

Design rules (agreed 2026-10-18):
- Code computes, the model judges. Code does all arithmetic (gaps, IZ Swing - Chase,
  league averages, ranks). Code does NOT apply the evaluation method
  (sample-size labels, "gap >= .030", thresholds) — that is the model's job, and
  what the evals will test.
- Numbers are formatted baseball-style here (.383, 26.3%), so the model can copy
  them exactly and the grader can check every number against the packet.
"""

import os
import re
import sys
import unicodedata

import psycopg
from psycopg.rows import dict_row

CONNINFO = os.environ.get("MLB_ANALYST_CONN", "host=localhost port=5432 dbname=mlb user=mlb_analyst")

# Qualified hitter = 3.1 PA per team game (502 PA in a 162-game season; 2020 had 60 games).
QUALIFIED_PA = {2020: 186}
DEFAULT_QUALIFIED_PA = 502

# Metrics shown in the league-context table: (label, column, which direction is better).
# "higher"/"lower" get a rank; None means there is no better direction (e.g. GB% is a
# style, not a skill), so only the league average is shown.
CONTEXT_METRICS = [
    ("xwOBA (house)", "xwoba", "higher"),
    ("wOBA", "woba", "higher"),
    ("xSLG", "xslg", "higher"),
    ("xBA", "xba", "higher"),
    ("EV90", "ev90", "higher"),
    ("Avg EV", "avg_ev", "higher"),
    ("Hard-hit%", "hard_hit_pct", "higher"),
    ("Barrel%", "barrel_pct", "higher"),
    ("Sweet spot% (8-32°)", "sweet_spot_pct", "higher"),
    ("Pulled Air%", "pulled_fb_pct", "higher"),
    ("IZ Swing - Chase", "swing_score", "higher"),
    ("IZ Swing%", "z_swing_pct", None),
    ("Chase%", "chase_pct", "lower"),
    ("Whiff%", "whiff_pct", "lower"),
    ("K%", "k_pct", "lower"),
    ("BB%", "bb_pct", "higher"),
    ("LA median", "median_la", None),
    ("LA SD", "sd_la", "lower"),
    ("GB%", "gb_pct", None),
    ("FB%", "fb_pct", None),
    ("Pull%", "pull_pct", None),
    ("Sprint speed", "sprint_speed", "higher"),
]

# Same idea for the by-pitch-group league context.
PITCH_GROUP_METRICS = [
    ("Pitch share", "pitch_share", None),
    ("xwOBA (house)", "xwoba", "higher"),
    ("wOBA", "woba", "higher"),
    ("IZ Swing%", "z_swing_pct", None),
    ("Chase%", "chase_pct", "lower"),
    ("IZ Swing - Chase", "swing_score", "higher"),
    ("Whiff%", "whiff_pct", "lower"),
    ("K%", "k_pct", "lower"),
    ("EV90", "ev90", "higher"),
    ("Hard-hit%", "hard_hit_pct", "higher"),
    ("Barrel%", "barrel_pct", "higher"),
]
PITCH_GROUPS = ["fastball", "breaking", "offspeed"]

# Season-over-season changes, computed here so the model never has to subtract.
CHANGE_METRICS = [
    ("xwOBA (house)", "xwoba"), ("wOBA", "woba"), ("BABIP", "babip"), ("EV90", "ev90"),
    ("Hard-hit%", "hard_hit_pct"), ("Barrel%", "barrel_pct"), ("Sweet spot%", "sweet_spot_pct"),
    ("Pulled Air%", "pulled_fb_pct"), ("Pull%", "pull_pct"), ("LA median", "median_la"), ("LA SD", "sd_la"),
    ("IZ Swing - Chase", "swing_score"), ("IZ Swing%", "z_swing_pct"), ("Chase%", "chase_pct"),
    ("Whiff%", "whiff_pct"), ("K%", "k_pct"), ("BB%", "bb_pct"), ("Sprint speed", "sprint_speed"),
]


# ---------------------------------------------------------------- formatting

def rate(x):          # .383  (wOBA, xwOBA, AVG, BABIP...)
    if x is None:
        return "—"
    s = f"{x:.3f}"
    return s[1:] if s.startswith("0") else s.replace("-0.", "-.")


def signed_rate(x):   # +.023 / -.007  (gaps)
    return "—" if x is None else ("+" if x >= 0 else "-") + rate(abs(x))


def pct(x):           # 26.3%
    return "—" if x is None else f"{x * 100:.1f}%"


def one(x):           # 106.6  (mph, degrees, ft/s)
    return "—" if x is None else f"{x:.1f}"


# How each column is displayed.
FORMAT = {
    "xwoba": rate, "woba": rate, "xslg": rate, "xba": rate, "avg": rate, "obp": rate,
    "slg": rate, "babip": rate, "iso": rate, "swing_score": rate,
    "ev90": one, "avg_ev": one, "median_la": one, "sd_la": one, "sprint_speed": one,
}


def fmt(col, x):
    return FORMAT.get(col, pct)(x)


def change(col, new, old):
    """Difference between two seasons, in the column's display units (+.048, +4.4 pts, +1.4)."""
    if new is None or old is None:
        return "—"
    d = new - old
    if FORMAT.get(col) is rate:
        return signed_rate(d)
    if FORMAT.get(col) is one:
        return f"{d:+.1f}"
    return f"{d * 100:+.1f} pts"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]
    return "\n".join(out)


# ---------------------------------------------------------------- database

def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", "", s).strip()


def resolve_player(cur, name):
    """Turn a name into one player_id. Only players with MLB hitting seasons count.
    A workflow must not guess: if the name is ambiguous, stop and list the options."""
    cur.execute("""
        SELECT p.player_id, p.full_name, coalesce(p.use_name, p.first_name) AS use_name,
               p.last_name, max(b.season) AS last_season
        FROM main.players p JOIN main.batter_season b ON b.batter_id = p.player_id
        GROUP BY 1, 2, 3, 4""")
    q = _norm(name)
    hits = []
    for r in cur.fetchall():
        names = {_norm(r["full_name"]), _norm(f"{r['use_name']} {r['last_name']}")}
        if q in names:
            hits.append((0, r))                       # exact match
        elif all(any(t in n for n in names) for t in q.split()):
            hits.append((1, r))                       # partial match
    if not hits:
        raise ValueError(f"No MLB hitter matches '{name}'.")
    best = min(h[0] for h in hits)
    hits = [r for rank, r in hits if rank == best]
    if len(hits) > 1:
        opts = "; ".join(f"{r['full_name']} (id {r['player_id']}, last season {r['last_season']})" for r in hits)
        raise ValueError(f"'{name}' matches more than one hitter: {opts}. Be more specific.")
    return hits[0]


def add_derived(rows):
    """The two computed numbers: IZ Swing - Chase and the wOBA - xwOBA gap."""
    for r in rows:
        r["swing_score"] = None if r["z_swing_pct"] is None or r["chase_pct"] is None else r["z_swing_pct"] - r["chase_pct"]
        r["gap"] = None if r["woba"] is None or r["xwoba"] is None else r["woba"] - r["xwoba"]
    return rows


def fetch_seasons(cur, player_id):
    cur.execute("SELECT * FROM main.batter_season WHERE batter_id = %s ORDER BY season, split", (player_id,))
    return add_derived(cur.fetchall())


def fetch_pitch_groups(cur, player_id, first_season):
    cur.execute("""SELECT * FROM main.batter_pitch_group_season
                   WHERE batter_id = %s AND season >= %s ORDER BY season""", (player_id, first_season))
    return add_derived(cur.fetchall())


def fetch_league_pitch_groups(cur, season, min_pa):
    """Pitch-group rows for every qualified hitter (qualified on full-season PA)."""
    cur.execute("""
        SELECT g.* FROM main.batter_pitch_group_season g
        JOIN main.batter_season b ON b.season = g.season AND b.batter_id = g.batter_id AND b.split = 'all'
        WHERE g.season = %s AND b.pa >= %s""", (season, min_pa))
    return add_derived(cur.fetchall())


def fetch_current_team(cur, player_id):
    """Latest 40-man roster row (players.current_team_name is often stale)."""
    cur.execute("""
        SELECT r.date, r."STATUS" AS status, t.team_full_name, t.venue_name
        FROM main.rosters_40man_daily r
        LEFT JOIN main.mlbteams t ON t.team_id = r."ORG" AND t.season = extract(year FROM r.date)::int
        WHERE r."MLBAMID" = %s ORDER BY r.date DESC LIMIT 1""", (player_id,))
    return cur.fetchone()


def fetch_league(cur, season):
    """Every qualified hitter's full-season row, for league averages and ranks."""
    min_pa = QUALIFIED_PA.get(season, DEFAULT_QUALIFIED_PA)
    cur.execute("SELECT * FROM main.batter_season WHERE season = %s AND split = 'all' AND pa >= %s",
                (season, min_pa))
    return add_derived(cur.fetchall()), min_pa


def fetch_data_through(cur, season):
    cur.execute("SELECT max(game_date) AS d FROM main.mlb_games WHERE game_type = 'R' AND season = %s", (season,))
    return cur.fetchone()["d"]


# ---------------------------------------------------------------- packet sections

def section_seasons(full):
    core = table(
        ["Season", "Team", "Age", "PA", "xwOBA (house)", "EV90", "Pulled Air%", "IZ Swing - Chase",
         "Whiff%", "LA median", "LA SD"],
        [[r["season"], r["teams"], r["age"], r["pa"], fmt("xwoba", r["xwoba"]), fmt("ev90", r["ev90"]),
          fmt("pulled_fb_pct", r["pulled_fb_pct"]), fmt("swing_score", r["swing_score"]),
          fmt("whiff_pct", r["whiff_pct"]), fmt("median_la", r["median_la"]), fmt("sd_la", r["sd_la"])]
         for r in full])
    results = table(
        ["Season", "PA", "wOBA", "xwOBA (house)", "wOBA - xwOBA", "BABIP", "AVG", "OBP", "SLG", "HR", "Sprint speed (ft/s)"],
        [[r["season"], r["pa"], fmt("woba", r["woba"]), fmt("xwoba", r["xwoba"]), signed_rate(r["gap"]),
          fmt("babip", r["babip"]), fmt("avg", r["avg"]), fmt("obp", r["obp"]), fmt("slg", r["slg"]),
          r["hr"], fmt("sprint_speed", r["sprint_speed"])] for r in full])
    contact = table(
        ["Season", "PA", "BBE", "xBA", "xSLG", "Avg EV", "Hard-hit%", "Barrel%", "Sweet spot%",
         "GB%", "LD%", "FB%", "PU%", "Pull%", "Oppo%"],
        [[r["season"], r["pa"], r["bbe"], fmt("xba", r["xba"]), fmt("xslg", r["xslg"]), fmt("avg_ev", r["avg_ev"]),
          pct(r["hard_hit_pct"]), pct(r["barrel_pct"]), pct(r["sweet_spot_pct"]), pct(r["gb_pct"]),
          pct(r["ld_pct"]), pct(r["fb_pct"]), pct(r["pu_pct"]), pct(r["pull_pct"]), pct(r["oppo_pct"])]
         for r in full])
    swing = table(
        ["Season", "PA", "Pitches", "IZ Swing%", "Chase%", "IZ Swing - Chase", "Whiff%", "K%", "BB%"],
        [[r["season"], r["pa"], r["pitches"], pct(r["z_swing_pct"]), pct(r["chase_pct"]),
          fmt("swing_score", r["swing_score"]), pct(r["whiff_pct"]), pct(r["k_pct"]), pct(r["bb_pct"])]
         for r in full])
    return ("## Seasons (full season, every MLB season on record)\n\n### Core (foundational metrics)\n\n" + core
            + "\n\n### Results vs. expected\n\n" + results
            + "\n\n### Contact quality and batted-ball shape\n\n" + contact
            + "\n\n### Plate discipline\n\n" + swing)


def context_table(player_row, league, metrics, qualified):
    """Player value, league average and rank for each metric."""
    rows = []
    for label, col, better in metrics:
        values = [r[col] for r in league if r[col] is not None]
        avg = sum(values) / len(values) if values else None
        mine = player_row[col]
        if better and qualified and mine is not None:
            rank = 1 + sum(v > mine if better == "higher" else v < mine for v in values)
            rank_s = f"{rank} of {len(values)}"
            # share of qualified hitters he ranks ahead of: 100 = best, 0 = worst
            pctile_s = str(round(100 * (len(values) - rank) / (len(values) - 1))) if len(values) > 1 else "—"
        else:
            rank_s = pctile_s = "—"
        rows.append([label, fmt(col, mine), fmt(col, avg), rank_s, pctile_s])
    return table(["Metric", "Player", "Qualified avg", "Player rank", "Percentile"], rows)


def section_changes(full):
    """Change between consecutive seasons, for the last three seasons."""
    recent = full[-3:]
    if len(recent) < 2:
        return "## Season-over-season changes\n\nOnly one MLB season on record."
    pairs = list(zip(recent, recent[1:]))
    headers = ["Metric"] + [f"{a['season']} → {b['season']}" for a, b in pairs]
    rows = [[label] + [change(col, b[col], a[col]) for a, b in pairs] for label, col in CHANGE_METRICS]
    note = ("Computed from the season rows above (later season minus earlier). "
            "Rates in points of .001 (+.048); percentages in percentage points (+4.4 pts); EV90, LA and sprint speed in mph / degrees / ft/s. "
            "PA by season: " + ", ".join(f"{r['season']} {r['pa']}" for r in recent) + ".")
    return f"## Season-over-season changes\n\n{note}\n\n" + table(headers, rows)


def section_league(player_row, league, min_pa):
    season = player_row["season"]
    qualified = player_row["pa"] >= min_pa
    note = (f"League = the {len(league)} qualified hitters in {season} ({min_pa}+ PA); league average is the simple "
            "mean of their values. Rank 1 = best; shown only for metrics with a clear better direction"
            + ("." if qualified else f", and not shown here because this player had {player_row['pa']} PA (not qualified)."))
    return f"## {season} league context\n\n{note}\n\n" + context_table(player_row, league, CONTEXT_METRICS, qualified)


def section_pitch_groups(groups, league, latest, min_pa):
    """Last three seasons by pitch group, then league context per group for the latest season."""
    if not groups:
        return "## By pitch group\n\nNo pitch-group rows in the database."
    groups = sorted(groups, key=lambda r: (r["season"], PITCH_GROUPS.index(r["pitch_group"])))
    seasons = table(
        ["Season", "Group", "Pitches", "Share", "IZ Swing%", "Chase%", "IZ Swing - Chase", "Whiff%",
         "PA ending", "wOBA", "xwOBA (house)", "wOBA - xwOBA", "K%", "BBE", "EV90", "Hard-hit%", "Barrel%"],
        [[r["season"], r["pitch_group"], r["pitches"], pct(r["pitch_share"]), pct(r["z_swing_pct"]),
          pct(r["chase_pct"]), fmt("swing_score", r["swing_score"]), pct(r["whiff_pct"]), r["pa"],
          fmt("woba", r["woba"]), fmt("xwoba", r["xwoba"]), signed_rate(r["gap"]), pct(r["k_pct"]), r["bbe"],
          fmt("ev90", r["ev90"]), pct(r["hard_hit_pct"]), pct(r["barrel_pct"])] for r in groups])
    season = latest["season"]
    qualified = latest["pa"] >= min_pa
    parts = [
        "## By pitch group",
        "Fastball = four-seam, sinker, cutter, two-seam. Breaking = slider, sweeper, curveball, knuckle curve, "
        "slurve, slow curve. Offspeed = changeup, splitter, forkball.\n\n"
        "Two ways of counting: Pitches, Share, IZ Swing%, Chase% and Whiff% count every pitch of the group he saw. "
        "\"PA ending\" and everything after it count only plate appearances whose last pitch was in the group.",
        "### Seasons\n\n" + seasons,
    ]
    for g in PITCH_GROUPS:
        mine = next((r for r in groups if r["season"] == season and r["pitch_group"] == g), None)
        if mine is None:
            continue
        lg = [r for r in league if r["pitch_group"] == g]
        parts.append(f"### {season} vs. {g} — league context ({len(lg)} qualified hitters, {min_pa}+ season PA)\n\n"
                     + context_table(mine, lg, PITCH_GROUP_METRICS, qualified))
    return "\n\n".join(parts)


def section_splits(splits, season):
    label = {"vs_lhp": "vs LHP", "vs_rhp": "vs RHP"}
    rows = [[label[r["split"]], r["pa"], fmt("woba", r["woba"]), fmt("xwoba", r["xwoba"]), signed_rate(r["gap"]),
             fmt("ev90", r["ev90"]), pct(r["whiff_pct"]), pct(r["k_pct"]), pct(r["bb_pct"])]
            for r in splits]
    if not rows:
        return f"## {season} platoon splits\n\nNo split rows in the database."
    return (f"## {season} platoon splits\n\n"
            + table(["Split", "PA", "wOBA", "xwOBA (house)", "wOBA - xwOBA", "EV90", "Whiff%", "K%", "BB%"], rows))


# ---------------------------------------------------------------- the packet

def get_hitter_data(name):
    """Return the data packet (markdown text) for one hitter."""
    with psycopg.connect(CONNINFO, autocommit=True, row_factory=dict_row) as conn, conn.cursor() as cur:
        player = resolve_player(cur, name)
        rows = fetch_seasons(cur, player["player_id"])
        full = [r for r in rows if r["split"] == "all"]
        latest = full[-1]
        splits = [r for r in rows if r["season"] == latest["season"] and r["split"] != "all"]
        team = fetch_current_team(cur, player["player_id"])
        league, min_pa = fetch_league(cur, latest["season"])
        groups = fetch_pitch_groups(cur, player["player_id"], latest["season"] - 2)
        league_groups = fetch_league_pitch_groups(cur, latest["season"], min_pa)
        data_through = fetch_data_through(cur, latest["season"])

    team_s = (f"{team['team_full_name']} (40-man roster as of {team['date']}, status: {team['status']})"
              if team else f"{latest['teams']} (from {latest['season']} stats; not on a current 40-man roster)")
    header = "\n".join([
        f"# Data packet: {player['full_name']}",
        "",
        f"- Player ID: {player['player_id']}",
        f"- Position: {latest['pos']} · Bats {latest['bats']} / Throws {latest['throws']}",
        f"- Age: {latest['age']} in {latest['season']} (age as of June 30 of that season)",
        f"- Current team: {team_s}",
        f"- Home venue: {team['venue_name'] if team and team['venue_name'] else '—'}",
        f"- Latest season: {latest['season']} · data through {data_through} (MLB regular season only)",
    ])
    notes = "\n".join([
        "## Notes on the data",
        "",
        "- Rates are per plate appearance or per batted ball; \"—\" means the value is not available.",
        "- xwOBA, xSLG, xBA come from a house expected-stats model (validated against Statcast; typical "
        "difference 3–7 points of xwOBA). Call them \"(house model)\".",
        "- IZ Swing - Chase is in-zone swing rate minus chase rate (generally higher is better). It is not a "
        "swing-decision score.",
        "- Pull% and Oppo% are approximate (about 4 points above Statcast); fine for trends.",
        "- FB% uses the Statcast definition: popups are counted separately (PU%), so it runs well below FanGraphs' FB%.",
        "- Sprint speed: about 27 ft/s is average, 30+ elite.",
        "- Park factors are NOT in the database, so park effects cannot be checked.",
    ])
    return "\n\n".join([header, section_seasons(full), section_changes(full), section_league(latest, league, min_pa),
                        section_splits(splits, latest["season"]),
                        section_pitch_groups(groups, league_groups, latest, min_pa), notes]) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('usage: python data.py "Player Name"')
    try:
        print(get_hitter_data(sys.argv[1]))
    except ValueError as e:
        sys.exit(str(e))
