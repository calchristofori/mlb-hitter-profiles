"""Compare the mlb database against public sources and write a validation report.

    bash validation/fetch_sources.sh 2023 2026        # download reference data first
    .venv/bin/python -I validation/validate.py 2023 2026

Checks:
  1. Counting stats, every hitter     vs MLB Stats API (official)
  2. Rates and Statcast metrics       vs Baseball Savant + FanGraphs (qualified hitters)
  3. Pitch-group table                vs Savant pitch-arsenal leaderboard (rolled up into our groups)
  4. Internal consistency             math, totals, and data.py's league averages / ranks

Writes validation/report_<date>.md and prints a summary.
"""

import csv
import json
import statistics
import sys
from datetime import date
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import data  # noqa: E402  (the data packet module under test)

CONNINFO = data.CONNINFO

# Metric spec: (label, our column, source key, source column, scale to ours, unit, tolerance in display units, note)
# unit: "rate" (.383, shown in points of .001), "pct" (shown in percentage points), "mph", "fts", "count"
SAVANT = [
    ("PA", "pa", "custom", "pa", 1, "count", 0, "automatic IBBs missing from pbp (known)"),
    ("AVG", "avg", "custom", "batting_avg", 1, "rate", 2, ""),
    ("OBP", "obp", "custom", "on_base_percent", 1, "rate", 2, ""),
    ("SLG", "slg", "custom", "slg_percent", 1, "rate", 2, ""),
    ("wOBA", "woba", "custom", "woba", 1, "rate", 10, "house weights vs Savant weights"),
    ("xwOBA", "xwoba", "custom", "xwoba", 1, "rate", 10, "house model; guide says typical gap 3–7 pts"),
    ("xBA", "xba", "custom", "xba", 1, "rate", 10, "house model"),
    ("xSLG", "xslg", "custom", "xslg", 1, "rate", 20, "house model"),
    ("K%", "k_pct", "custom", "k_percent", 0.01, "pct", 0.3, ""),
    ("BB%", "bb_pct", "custom", "bb_percent", 0.01, "pct", 0.3, ""),
    ("Avg EV", "avg_ev", "custom", "exit_velocity_avg", 1, "mph", 0.3, ""),
    ("Hard-hit%", "hard_hit_pct", "custom", "hard_hit_percent", 0.01, "pct", 1.0, ""),
    ("Barrel%", "barrel_pct", "custom", "barrel_batted_rate", 0.01, "pct", 1.0, "guide says ~0.5 pts below Savant"),
    ("Sweet spot%", "sweet_spot_pct", "custom", "sweet_spot_percent", 0.01, "pct", 2.0, "8° and 32° count as half (integer launch angles)"),
    ("IZ Swing%", "z_swing_pct", "custom", "z_swing_percent", 0.01, "pct", 1.0, ""),
    ("Chase%", "chase_pct", "custom", "oz_swing_percent", 0.01, "pct", 1.0, "zone = ball touches zone, as Savant"),
    ("Whiff%", "whiff_pct", "custom", "whiff_percent", 0.01, "pct", 1.0, ""),
    ("GB%", "gb_pct", "custom", "groundballs_percent", 0.01, "pct", 1.0, ""),
    ("FB%", "fb_pct", "custom", "flyballs_percent", 0.01, "pct", 1.0, ""),
    ("LD%", "ld_pct", "custom", "linedrives_percent", 0.01, "pct", 1.0, ""),
    ("PU%", "pu_pct", "custom", "popups_percent", 0.01, "pct", 1.0, ""),
    ("Pulled Air% (Savant Pull AIR%)", "pulled_fb_pct", "battedball", "pull_air_rate", 1, "pct", 1.0, "spray from hit coordinates; avg within ~0.5"),
    ("Pull%", "pull_pct", "custom", "pull_percent", 0.01, "pct", 6.0, "known approximate (~4 pts high)"),
    ("Oppo%", "oppo_pct", "custom", "opposite_percent", 0.01, "pct", 6.0, "known approximate"),
    ("Sprint speed", "sprint_speed", "custom", "sprint_speed", 1, "fts", 0.05, "copied from Savant"),
    ("Pitches seen", "pitches", "custom", "pitch_count", 1, "count", 5, ""),
    ("EV90", "ev90", "fangraphs", "EV90", 1, "mph", 0.5, "FanGraphs EV90"),
    ("wOBA (FanGraphs)", "woba", "fangraphs", "wOBA", 1, "rate", 10, "guide says ~.005 above FG for power hitters"),
]

# Counting stats vs MLB Stats API: (label, our column, API field)
OFFICIAL = [
    ("PA", "pa", "plateAppearances"), ("AB", "ab", "atBats"), ("H", "h", "hits"),
    ("2B", "doubles", "doubles"), ("3B", "triples", "triples"), ("HR", "hr", "homeRuns"),
    ("RBI", "rbi", "rbi"), ("BB", "bb", "baseOnBalls"), ("IBB", "ibb", "intentionalWalks"),
    ("HBP", "hbp", "hitByPitch"), ("SO", "so", "strikeOuts"), ("SF", "sf", "sacFlies"),
    ("SH", "sh", "sacBunts"), ("GIDP", "gidp", "groundIntoDoublePlay"), ("Pitches", "pitches", "numberOfPitches"),
]

# Savant pitch-arsenal codes -> our groups (Savant folds knuckle curves into CU).
SAVANT_GROUP = {"FF": "fastball", "SI": "fastball", "FC": "fastball",
                "SL": "breaking", "ST": "breaking", "CU": "breaking", "SV": "breaking",
                "CH": "offspeed", "FS": "offspeed", "FO": "offspeed"}

# Pitch-group metrics vs Savant arsenal: (label, our column, how Savant is rolled up, unit, tolerance, note)
ARSENAL = [
    ("Pitches", "pitches", "sum:pitches", "count", 5, ""),
    ("PA ending", "pa", "sum:pa", "count", 2, ""),
    ("wOBA", "woba", "wavg:woba:pa", "rate", 15, "Savant rolled up PA-weighted (approximate)"),
    ("xwOBA", "xwoba", "wavg:est_woba:pa", "rate", 20, "house model; PA-weighted roll-up"),
    ("K%", "k_pct", "wavg:k_percent:pa", "pct", 1.0, "PA-weighted roll-up"),
    ("Whiff%", "whiff_pct", "wavg:whiff_percent:pitches", "pct", 2.0, "pitch-weighted roll-up (Savant gives no swing counts)"),
    ("Hard-hit%", "hard_hit_pct", "wavg:hard_hit_percent:pa", "pct", 3.0, "PA-weighted roll-up (Savant gives no BBE counts)"),
]


# ---------------------------------------------------------------- helpers

def num(x):
    if x is None:
        return None
    s = str(x).strip().replace('"', "")
    if s in ("", "-", ".---", "null", "NA"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def display_scale(unit):
    return {"rate": 1000, "pct": 100}.get(unit, 1)


def unit_label(unit):
    return {"rate": "pts (.001)", "pct": "pct pts", "mph": "mph", "fts": "ft/s", "count": "count"}[unit]


def compare(pairs, unit, tol):
    """pairs: list of (ours, theirs, who). Differences are ours - theirs, in display units."""
    pairs = [(a, b, w) for a, b, w in pairs if a is not None and b is not None]
    if len(pairs) < 3:
        return None
    k = display_scale(unit)
    diffs = [(a - b) * k for a, b, _ in pairs]
    absd = sorted(abs(d) for d in diffs)
    worst = max(zip(diffs, pairs), key=lambda t: abs(t[0]))
    xs, ys = [a for a, _, _ in pairs], [b for _, b, _ in pairs]
    try:
        corr = statistics.correlation(xs, ys)
    except statistics.StatisticsError:
        corr = None
    within = sum(abs(d) <= tol + 1e-9 for d in diffs) / len(diffs)
    return {
        "n": len(pairs), "corr": corr, "bias": statistics.fmean(diffs), "mae": statistics.fmean(absd),
        "p95": absd[min(len(absd) - 1, int(0.95 * len(absd)))], "max": worst[0], "who": worst[1][2],
        "within": within, "status": "OK" if within >= 0.95 else ("CHECK" if within >= 0.80 else "ISSUE"),
    }


def fmt_num(x, unit):
    if x is None:
        return "—"
    if unit == "count":
        return f"{x:+.0f}" if abs(x) >= 1 or x == 0 else f"{x:+.2f}"
    return f"{x:+.1f}" if unit in ("rate", "pct", "mph") else f"{x:+.2f}"


def result_row(label, res, unit, tol, note):
    if res is None:
        return [label, "—", "—", "—", "—", "—", "—", "—", "no data", note]
    corr = "—" if res["corr"] is None else f"{res['corr']:.3f}"
    return [label, res["n"], corr, fmt_num(res["bias"], unit), f"{res['mae']:.2f}", f"{res['p95']:.2f}",
            f"{fmt_num(res['max'], unit)} ({res['who']})", f"{res['within'] * 100:.0f}% (±{tol} {unit_label(unit)})",
            res["status"], note]


RESULT_HEADERS = ["Metric", "n", "Corr", "Bias (ours − theirs)", "Mean abs diff", "95th pct abs diff",
                  "Largest diff", "Within tolerance", "Status", "Note"]


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]
    return "\n".join(out)


# ---------------------------------------------------------------- loading

def load_ours(cur, first, last):
    cur.execute("SELECT * FROM main.batter_season WHERE split = 'all' AND season BETWEEN %s AND %s", (first, last))
    bs = {(r["season"], r["batter_id"]): r for r in cur.fetchall()}
    cur.execute("SELECT * FROM main.batter_pitch_group_season WHERE season BETWEEN %s AND %s", (first, last))
    pg = {(r["season"], r["batter_id"], r["pitch_group"]): r for r in cur.fetchall()}
    return bs, pg


def load_sources(folder, season):
    src = {}
    src["custom"] = {int(r["player_id"]): r for r in read_csv(folder / f"savant_custom_{season}.csv")}
    src["battedball"] = {int(r["id"]): r for r in read_csv(folder / f"savant_battedball_{season}.csv")}
    src["fangraphs"] = {int(float(r["xMLBAMID"])): r for r in read_csv(folder / f"fangraphs_{season}.csv")
                        if num(r.get("xMLBAMID"))}
    api = json.loads((folder / f"statsapi_hitting_{season}.json").read_text())
    src["official"] = {s["player"]["id"]: s["stat"] for s in api["stats"][0]["splits"]}
    arsenal = {}
    for r in read_csv(folder / f"savant_arsenal_{season}.csv"):
        g = SAVANT_GROUP.get(r["pitch_type"])
        if g:
            arsenal.setdefault((int(r["player_id"]), g), []).append(r)
    src["arsenal"] = arsenal
    return src


# ---------------------------------------------------------------- checks

def check_official(bs, sources, seasons):
    """Every hitter, every season: exact-match rate for each counting stat."""
    rows, mismatches = [], []
    for label, col, field in OFFICIAL:
        n = exact = 0
        tot_ours = tot_api = 0
        for s in seasons:
            off = sources[s]["official"]
            for (season, pid), r in bs.items():
                if season != s or pid not in off:
                    continue
                a, b = r[col], off[pid].get(field)
                if a is None or b is None:
                    continue
                n += 1
                tot_ours += a
                tot_api += b
                if a == b:
                    exact += 1
                else:
                    mismatches.append((label, s, r["name"], a, b))
        rows.append([label, n, f"{exact / n * 100:.2f}%" if n else "—", f"{tot_ours:,}", f"{tot_api:,}",
                     f"{(tot_ours - tot_api) / tot_api * 100:+.3f}%" if tot_api else "—"])
    coverage = []
    for s in seasons:
        ours = {pid for (season, pid) in bs if season == s}
        api = {pid for pid, st in sources[s]["official"].items() if (st.get("plateAppearances") or 0) > 0}
        coverage.append([s, len(ours), len(api), len(ours & api), len(ours - api), len(api - ours)])
    return rows, mismatches, coverage


def check_metrics(bs, sources, seasons, qualified_ids):
    out = []
    for label, col, key, scol, scale, unit, tol, note in SAVANT:
        pairs = []
        for s in seasons:
            src = sources[s][key]
            for pid in qualified_ids[s]:
                if pid in src:
                    theirs = num(src[pid].get(scol))
                    pairs.append((bs[(s, pid)][col], None if theirs is None else theirs * scale,
                                  f"{bs[(s, pid)]['name']} {s}"))
        out.append(result_row(label, compare(pairs, unit, tol), unit, tol, note))
    return out


def rollup(rows, how):
    kind, *args = how.split(":")
    if kind == "sum":
        vals = [num(r[args[0]]) for r in rows]
        return sum(v for v in vals if v is not None)
    col, wcol = args
    pts = [(num(r[col]), num(r[wcol])) for r in rows]
    pts = [(v, w) for v, w in pts if v is not None and w]
    wsum = sum(w for _, w in pts)
    return sum(v * w for v, w in pts) / wsum if wsum else None


def check_pitch_groups(pg, sources, seasons, qualified_ids):
    out = []
    for label, col, how, unit, tol, note in ARSENAL:
        pct_scale = 0.01 if unit == "pct" else 1
        pairs = []
        for s in seasons:
            for pid in qualified_ids[s]:
                for g in data.PITCH_GROUPS:
                    mine, theirs = pg.get((s, pid, g)), sources[s]["arsenal"].get((pid, g))
                    if not mine or not theirs:
                        continue
                    v = rollup(theirs, how)
                    pairs.append((mine[col], None if v is None else v * pct_scale, f"{mine['name']} {s} {g}"))
        out.append(result_row(label, compare(pairs, unit, tol), unit, tol, note))
    return out


def check_internal(cur, bs, pg, latest):
    """Math and totals inside our own tables, plus data.py's league context."""
    rows = []

    def add(name, bad, total, detail=""):
        rows.append([name, f"{total - bad:,} / {total:,}", "OK" if bad == 0 else "ISSUE", detail])

    recs = list(bs.values())
    add("H = 1B + 2B + 3B + HR", sum(r["h"] != r["singles"] + r["doubles"] + r["triples"] + r["hr"] for r in recs), len(recs))
    add("AVG = H / AB (rounded)", sum(r["ab"] and abs(r["avg"] - r["h"] / r["ab"]) > 0.0006 for r in recs), len(recs))
    add("SLG = TB / AB (rounded)", sum(r["ab"] and abs(r["slg"] - (r["singles"] + 2 * r["doubles"] + 3 * r["triples"] + 4 * r["hr"]) / r["ab"]) > 0.0006 for r in recs), len(recs))
    add("PA ≥ AB + BB + HBP + SF + SH", sum(r["pa"] < r["ab"] + r["bb"] + r["hbp"] + r["sf"] + r["sh"] for r in recs), len(recs))
    rate_cols = ["avg", "obp", "k_pct", "bb_pct", "hard_hit_pct", "barrel_pct", "sweet_spot_pct", "gb_pct", "fb_pct",
                 "z_swing_pct", "chase_pct", "whiff_pct", "pulled_fb_pct", "xba"]
    add("Rates between 0 and 1", sum(any(r[c] is not None and not 0 <= r[c] <= 1 for c in rate_cols) for r in recs), len(recs))
    gb = [r for r in recs if r["gb_pct"] is not None and r["bbe"] >= 50]
    add("GB + LD + FB + PU ≈ 100% (50+ BBE)", sum(abs(r["gb_pct"] + r["ld_pct"] + r["fb_pct"] + r["pu_pct"] - 1) > 0.003 for r in gb), len(gb))

    # pitch groups reconcile with batter_season
    by_player = {}
    for (s, pid, g), r in pg.items():
        t = by_player.setdefault((s, pid), [0, 0])
        t[0] += r["pitches"]
        t[1] += r["pa"]
    over = sum((k in bs) and (v[0] > bs[k]["pitches"] or v[1] > bs[k]["pa"]) for k, v in by_player.items())
    add("Pitch groups never exceed season pitches / PA", over, len(by_player))
    shares = {}
    for (s, pid, g), r in pg.items():
        shares[(s, pid)] = shares.get((s, pid), 0) + (r["pitch_share"] or 0)
    add("Pitch-group shares sum to 100% (±0.2)", sum(abs(v - 1) > 0.002 for v in shares.values()), len(shares))

    # data.py league context: recompute averages and ranks independently in SQL
    min_pa = data.QUALIFIED_PA.get(latest, data.DEFAULT_QUALIFIED_PA)
    league, _ = data.fetch_league(cur, latest)
    bad = total = 0
    examples = []
    for label, col, better in data.CONTEXT_METRICS:
        expr = "z_swing_pct - chase_pct" if col == "swing_score" else col
        order = "DESC" if better == "higher" else "ASC"
        cur.execute(f"""
            SELECT batter_id, {expr} AS v, avg({expr}) OVER () AS lg,
                   rank() OVER (ORDER BY {expr} {order}) AS rk
            FROM main.batter_season WHERE season = %s AND split = 'all' AND pa >= %s AND {expr} IS NOT NULL""",
                    (latest, min_pa))
        sql = {r["batter_id"]: r for r in cur.fetchall()}
        for row in league:
            if row["batter_id"] not in sql:
                continue
            table = data.context_table(row, league, [(label, col, better)], True).splitlines()[2]
            cells = [c.strip() for c in table.strip("|").split("|")]
            want_avg = data.fmt(col, sql[row["batter_id"]]["lg"])
            want_rank = f"{sql[row['batter_id']]['rk']} of {len(sql)}" if better else "—"
            total += 1
            if cells[2] != want_avg or cells[3] != want_rank:
                bad += 1
                if len(examples) < 3:
                    examples.append(f"{label} {row['name']}: packet {cells[2]}/{cells[3]}, SQL {want_avg}/{want_rank}")
    add(f"data.py league averages and ranks match SQL ({latest}, {len(data.CONTEXT_METRICS)} metrics)",
        bad, total, "; ".join(examples))
    return rows


# ---------------------------------------------------------------- main

def main():
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (2023, 2026)
    seasons = list(range(first, last + 1))
    folders = sorted((HERE / "downloads").iterdir())
    if not folders:
        sys.exit("No downloads. Run validation/fetch_sources.sh first.")
    folder = folders[-1]
    sources = {s: load_sources(folder, s) for s in seasons}

    with psycopg.connect(CONNINFO, autocommit=True, row_factory=dict_row) as conn, conn.cursor() as cur:
        bs, pg = load_ours(cur, first, last)
        qualified_ids = {s: [pid for (season, pid), r in bs.items() if season == s
                             and r["pa"] >= data.QUALIFIED_PA.get(s, data.DEFAULT_QUALIFIED_PA)] for s in seasons}
        official_rows, mismatches, coverage = check_official(bs, sources, seasons)
        metric_rows = check_metrics(bs, sources, seasons, qualified_ids)
        group_rows = check_pitch_groups(pg, sources, seasons, qualified_ids)
        internal_rows = check_internal(cur, bs, pg, last)

    n_q = sum(len(v) for v in qualified_ids.values())
    statuses = [r[8] for r in metric_rows + group_rows] + [r[2] for r in internal_rows]
    summary = {k: statuses.count(k) for k in ("OK", "CHECK", "ISSUE")}

    mm_rows = sorted(mismatches, key=lambda m: -abs(m[3] - m[4]))[:25]
    report = "\n\n".join([
        f"# Data validation report — {date.today()}",
        f"Seasons {first}–{last}. Reference data downloaded to `{folder.relative_to(HERE.parent)}`. "
        f"Qualified hitters: {n_q} player-seasons (502+ PA).\n\n"
        f"**Summary:** {summary['OK']} OK · {summary['CHECK']} CHECK · {summary['ISSUE']} ISSUE.\n\n"
        "Status rule: OK = 95%+ of players within tolerance; CHECK = 80–95%; ISSUE = under 80% (or any internal check failing). "
        "Bias is ours minus theirs: positive means our number runs higher.",
        "## 1. Counting stats vs. MLB Stats API (every hitter)",
        md_table(["Season", "Our hitters", "API hitters (1+ PA)", "In both", "Only ours", "Only API"], coverage),
        md_table(["Stat", "Player-seasons", "Exact match", "Our total", "Official total", "Total diff"], official_rows),
        "Largest mismatches:\n\n" + (md_table(["Stat", "Season", "Player", "Ours", "Official"], mm_rows) if mm_rows else "None."),
        "## 2. Rates and Statcast metrics vs. Savant / FanGraphs (qualified hitters)",
        md_table(RESULT_HEADERS, metric_rows),
        "## 3. Pitch groups vs. Savant pitch-arsenal leaderboard (qualified hitters)",
        "Savant reports each pitch type separately; they are rolled up into our three groups. Savant gives no swing or "
        "batted-ball counts per pitch type, so whiff% and hard-hit% roll-ups are weighted approximations.",
        md_table(RESULT_HEADERS, group_rows),
        "## 4. Internal consistency",
        md_table(["Check", "Passing", "Status", "Detail"], internal_rows),
    ]) + "\n"
    out = HERE / f"report_{date.today()}.md"
    out.write_text(report)
    print(report)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
