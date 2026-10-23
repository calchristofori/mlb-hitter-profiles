"""Audit one hitter's data packet: is every number in it right?

    .venv/bin/python -I validation/audit_packet.py "Kyle Schwarber"

Free (no AI). Writes validation/audits/<player>_<date>.md, a sheet a person can read.
Three independent checks, each done without data.py's own code:

  1. Packet math. Every cell of every table in the packet, recomputed here from the
     database rows: derived numbers (xISO, IZ Swing - Chase, gaps), season-over-season
     changes, trend wording, league averages, ranks and percentiles (in SQL), platoon
     usage, and the by-pitch-group tables.
  2. Rows rebuilt from pitches. His season, split and pitch-group rows rebuilt from
     the pitch-by-pitch table (pbp), so the nightly pipeline's numbers are checked too.
     The house expected stats (xwOBA, xBA, xSLG) come from a model and are not rebuilt.
  3. Public sources. His season rows against Baseball Savant and FanGraphs, and his
     pitch-group rows against Savant's pitch-arsenal leaderboard, using the downloads
     from fetch_sources.sh and the tolerances in validate.py.
"""

import math
import re
import statistics
import sys
from collections import defaultdict
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import data      # noqa: E402  only for the packet under test, the connection and the name lookup
import validate  # noqa: E402  Savant / FanGraphs loaders and tolerances

OUT = HERE / "audits"
QUALIFIED = {2020: 186}   # 3.1 PA per team game
QUALIFIED_DEFAULT = 502
USAGE_MIN = 300           # platoon usage comparison group, as the packet states

# ---------------------------------------------------------------- display

def f_rate(x):
    if x is None:
        return "—"
    s = f"{x:.3f}"
    return s[1:] if s.startswith("0") else s.replace("-0.", "-.")


def f_srate(x):
    return "—" if x is None else ("+" if x >= 0 else "-") + f_rate(abs(x))


def f_pct(x):
    return "—" if x is None else f"{x * 100:.1f}%"


def f_one(x):
    return "—" if x is None else f"{x:.1f}"


KIND_FMT = {"rate": f_rate, "srate": f_srate, "pct": f_pct, "one": f_one,
            "int": lambda x: "—" if x is None else str(int(x)), "str": lambda x: "—" if x is None else str(x)}

# Packet column header -> (row field, display kind). Built from the glossary, not from data.py.
HEADERS = {
    "PA": ("pa", "int"), "BBE": ("bbe", "int"), "Pitches": ("pitches", "int"), "HR": ("hr", "int"),
    "PA ending": ("pa", "int"), "Team": ("teams", "str"), "Bats": ("bats", "str"), "Age": ("age", "int"),
    "xwOBA (house)": ("xwoba", "rate"), "wOBA": ("woba", "rate"), "xSLG": ("xslg", "rate"), "xBA": ("xba", "rate"),
    "xISO": ("xiso", "rate"), "ISO": ("iso", "rate"), "BABIP": ("babip", "rate"), "AVG": ("avg", "rate"),
    "OBP": ("obp", "rate"), "SLG": ("slg", "rate"), "wOBA - xwOBA": ("gap", "srate"),
    "IZ Swing - Chase": ("swing_score", "rate"),
    "EV90": ("ev90", "one"), "Avg EV": ("avg_ev", "one"), "LA median": ("median_la", "one"),
    "LA SD": ("sd_la", "one"), "Sprint speed (ft/s)": ("sprint_speed", "one"), "Sprint speed": ("sprint_speed", "one"),
    "Pulled Air%": ("pulled_fb_pct", "pct"), "Whiff%": ("whiff_pct", "pct"), "Hard-hit%": ("hard_hit_pct", "pct"),
    "Barrel%": ("barrel_pct", "pct"), "Sweet spot%": ("sweet_spot_pct", "pct"),
    "Sweet spot% (8-32°)": ("sweet_spot_pct", "pct"), "GB%": ("gb_pct", "pct"), "LD%": ("ld_pct", "pct"),
    "FB%": ("fb_pct", "pct"), "PU%": ("pu_pct", "pct"), "Pull%": ("pull_pct", "pct"), "Oppo%": ("oppo_pct", "pct"),
    "IZ Swing%": ("z_swing_pct", "pct"), "Chase%": ("chase_pct", "pct"), "K%": ("k_pct", "pct"),
    "BB%": ("bb_pct", "pct"), "Share": ("pitch_share", "pct"),
    "Pitch share (rank 1 = saw it most)": ("pitch_share", "pct"),
}
# Which way is better, for ranks (from the glossary's metric definitions). None = no rank.
BETTER = {
    "xwoba": "higher", "woba": "higher", "xslg": "higher", "xba": "higher", "xiso": "higher", "iso": "higher",
    "ev90": "higher", "avg_ev": "higher", "hard_hit_pct": "higher", "barrel_pct": "higher",
    "sweet_spot_pct": "higher", "pulled_fb_pct": "higher", "swing_score": "higher", "bb_pct": "higher",
    "sprint_speed": "higher", "chase_pct": "lower", "whiff_pct": "lower", "k_pct": "lower", "sd_la": "lower",
    "z_swing_pct": None, "median_la": None, "gb_pct": None, "fb_pct": None, "pull_pct": None,
    "pitch_share": "higher",  # rank 1 = saw the group most often
}
# Computed columns, as SQL over the stored ones.
SQL_EXPR = {"xiso": "xslg - xba", "swing_score": "z_swing_pct - chase_pct"}


def derive(r):
    r = dict(r)
    r["xiso"] = None if r.get("xslg") is None or r.get("xba") is None else r["xslg"] - r["xba"]
    r["swing_score"] = None if r.get("z_swing_pct") is None or r.get("chase_pct") is None \
        else r["z_swing_pct"] - r["chase_pct"]
    r["gap"] = None if r.get("woba") is None or r.get("xwoba") is None else r["woba"] - r["xwoba"]
    return r


def show(col, kind, row):
    return KIND_FMT[kind](row.get(col))


def change_text(kind, new, old):
    if new is None or old is None:
        return "—"
    d = new - old
    if kind in ("rate", "srate"):
        return f_srate(d)
    if kind == "one":
        return f"{d:+.1f}"
    return f"{d * 100:+.1f} pts"


def trend_text(kind, seq):
    """seq: [(season, value)] in order. The packet's trend wording, rebuilt."""
    vals = [(s, v) for s, v in seq if v is not None]
    if len(vals) < 2:
        return "—"
    dirs = []
    for (_, a), (_, b) in zip(vals, vals[1:]):
        shown = change_text(kind, b, a)
        digits = re.sub(r"[^0-9]", "", shown)
        dirs.append("flat" if set(digits) <= {"0"} else ("up" if shown.startswith("+") else "down"))
    last = dirs[-1]
    run = 1
    for d in reversed(dirs[:-1]):
        if d != last:
            break
        run += 1
    start, end = vals[-1 - run][0], vals[-1][0]
    verb = {"up": "rose", "down": "fell", "flat": "flat"}[last]
    if run == 1:
        head = f"flat in {end}" if last == "flat" else f"{verb} in {end} only"
    else:
        head = f"flat {run} seasons in a row" if last == "flat" else f"{verb} {run} seasons in a row"
    return (f"{head} ({start} → {end}); up in {dirs.count('up')} of {len(dirs)} changes, "
            f"down in {dirs.count('down')}, since {vals[0][0]}")


HALFWAY = set()  # percentiles that land exactly on .5, so rounding conventions can differ


def pctile(rank, n):
    if n < 2:
        return "—"
    exact = Decimal(100) * (n - rank) / (n - 1)
    shown = str(int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP)))
    if exact % 1 == Decimal("0.5"):
        HALFWAY.add((shown, f"{exact:.1f}"))
    return shown


# ---------------------------------------------------------------- the packet's tables

def parse_packet(text):
    """{(h2, h3): (headers, rows)} for every markdown table, plus the full text."""
    tables, h2, h3, buf = {}, "", "", []

    def flush():
        if buf:
            headers = [c.strip() for c in buf[0].strip("|").split("|")]
            rows = [[c.strip() for c in line.strip("|").split("|")] for line in buf[2:]]
            tables[(h2, h3)] = (headers, rows)
            buf.clear()

    for line in text.splitlines():
        if line.startswith("|"):
            buf.append(line)
            continue
        flush()
        if line.startswith("## "):
            h2, h3 = line[3:].strip(), ""
        elif line.startswith("### "):
            h3 = line[4:].strip()
    flush()
    return tables


# ---------------------------------------------------------------- check 1: packet math

class Check1:
    """Rebuild every packet table from the database rows and compare cell by cell."""

    def __init__(self, cur, pid):
        self.cur, self.pid = cur, pid
        cur.execute("SELECT * FROM main.batter_season WHERE batter_id = %s", (pid,))
        rows = [derive(r) for r in cur.fetchall()]
        self.full = sorted((r for r in rows if r["split"] == "all"), key=lambda r: r["season"])[-3:]
        self.latest = self.full[-1]["season"]
        self.splits = {r["split"]: r for r in rows if r["season"] == self.latest and r["split"] != "all"}
        self.lhp_pa = {r["season"]: r["pa"] for r in rows if r["split"] == "vs_lhp"}
        cur.execute("""SELECT * FROM main.batter_pitch_group_season
                       WHERE batter_id = %s AND season BETWEEN %s AND %s""", (pid, self.latest - 2, self.latest))
        self.groups = {(r["season"], r["pitch_group"]): derive(r) for r in cur.fetchall()}
        cur.execute("SELECT birth_date FROM main.players WHERE player_id = %s", (pid,))
        born = cur.fetchone()["birth_date"]
        for r in self.full:  # age on June 30 of the season
            r["age"] = r["season"] - born.year - (1 if born.month > 6 else 0)

    # league ranks, in SQL
    def league(self, season, cols, group=None):
        """{col: (avg, n, rank of the player or None)} among qualified hitters that season."""
        min_pa = QUALIFIED.get(season, QUALIFIED_DEFAULT)
        exprs = {c: SQL_EXPR.get(c, c) for c in cols}
        if group:
            base = f"""SELECT g.batter_id, {", ".join(f"g_{c} AS {c}" for c in cols)} FROM (
                         SELECT batter_id, {", ".join(f"({e}) AS g_{c}" for c, e in exprs.items())}
                         FROM main.batter_pitch_group_season WHERE season = %(s)s AND pitch_group = %(g)s) g
                       JOIN main.batter_season b ON b.batter_id = g.batter_id AND b.season = %(s)s
                        AND b.split = 'all' AND b.pa >= %(min)s"""
        else:
            base = f"""SELECT batter_id, {", ".join(f"({e}) AS {c}" for c, e in exprs.items())}
                       FROM main.batter_season WHERE season = %(s)s AND split = 'all' AND pa >= %(min)s"""
        win = []
        for c in cols:
            order = "ASC" if BETTER.get(c) == "lower" else "DESC"
            win += [f"avg({c}) OVER () AS avg_{c}", f"count({c}) OVER () AS n_{c}",
                    f"rank() OVER (ORDER BY {c} {order} NULLS LAST) AS rank_{c}", f"{c} AS v_{c}"]
        self.cur.execute(f"SELECT * FROM (SELECT batter_id, {', '.join(win)} FROM ({base}) q) z",
                         {"s": season, "g": group, "min": min_pa})
        rows = self.cur.fetchall()
        mine = next((r for r in rows if r["batter_id"] == self.pid), None)
        any_row = rows[0] if rows else {}
        out = {}
        for c in cols:
            rank = mine[f"rank_{c}"] if mine and mine[f"v_{c}"] is not None else None
            out[c] = (any_row.get(f"avg_{c}"), any_row.get(f"n_{c}", 0), rank)
        return out, len(rows)

    def expected(self, packet):
        """{(h2, h3): {row key: {header: value}}} for every table this check knows how to rebuild."""
        exp, L = {}, self.latest
        seasons_h2 = next(k[0] for k in packet if k[0].startswith("Seasons"))
        by_season = {str(r["season"]): r for r in self.full}
        for h3 in ("Core (foundational metrics)", "Results vs. expected",
                   "Contact quality and batted-ball shape", "Plate discipline"):
            exp[(seasons_h2, h3)] = ("rows", {(s,): r for s, r in by_season.items()})

        # changes and trends
        rows = {}
        for label in packet.get(("Season-over-season changes", ""), ([], []))[1]:
            col, kind = HEADERS[label[0]]
            cells = {}
            for a, b in zip(self.full, self.full[1:]):
                cells[f"{a['season']} → {b['season']}"] = change_text(kind, b[col], a[col])
            cells["Trend (last three seasons)"] = trend_text(kind, [(r["season"], r[col]) for r in self.full])
            rows[(label[0],)] = cells
        exp[("Season-over-season changes", "")] = ("cells", rows)

        # league context, latest season
        self.league_sizes = {}
        key = (f"{L} league context", "")
        if key in packet:
            exp[key] = ("cells", self.context_rows(packet[key][1], self.full[-1], L))
        # league context by season
        key = ("League context by season", "")
        if key in packet:
            rows = {}
            for label in packet[key][1]:
                col, kind = HEADERS[label[0]]
                cells = {}
                for r in self.full:
                    lg, n_q = self.league(r["season"], [col])
                    avg, n, rank = lg[col]
                    qualified = r["pa"] >= QUALIFIED.get(r["season"], QUALIFIED_DEFAULT)
                    cells[f"{r['season']} player"] = show(col, kind, r)
                    cells[f"{r['season']} avg"] = KIND_FMT[kind](avg)
                    cells[f"{r['season']} pctl"] = pctile(rank, n) if BETTER.get(col) and qualified and rank else "—"
                rows[(label[0],)] = cells
            exp[key] = ("cells", rows)

        # platoon splits
        split_h2 = f"{L} platoon splits"
        names = {"vs LHP": "vs_lhp", "vs RHP": "vs_rhp"}
        for h3 in ("Expected stats and batted-ball profile", "Plate discipline"):
            exp[(split_h2, h3)] = ("rows", {(k,): self.splits[v] for k, v in names.items() if v in self.splits})
        exp[(split_h2, "Platoon usage (last three seasons)")] = ("cells", self.usage())

        # pitch groups
        exp[("By pitch group", "Seasons")] = ("rows", {(str(s), g): r for (s, g), r in self.groups.items()})
        rows = {}
        for g in ("fastball", "breaking", "offspeed"):
            for label in ("Share", "Whiff%", "Chase%", "xwOBA (house)", "EV90"):
                col, kind = HEADERS[label]
                seq = [(s, self.groups[(s, g)][col]) for s in range(L - 2, L + 1) if (s, g) in self.groups]
                rows[(g, label)] = {"Trend": trend_text(kind, seq)}
        exp[("By pitch group", "Trends by group (last three seasons)")] = ("cells", rows)
        for (h2, h3), (_, prow) in packet.items():
            m = re.match(rf"{L} vs\. (\w+) — league context", h3)
            if h2 == "By pitch group" and m and (L, m.group(1)) in self.groups:
                exp[(h2, h3)] = ("cells", self.context_rows(prow, self.groups[(L, m.group(1))], L,
                                                            group=m.group(1), h3=h3))
        return exp

    def context_rows(self, packet_rows, row, season, group=None, h3=None):
        cols = [HEADERS[r[0]][0] for r in packet_rows]
        lg, n_q = self.league(season, cols, group)
        self.league_sizes[h3 or season] = n_q
        qualified = self.full[-1]["pa"] >= QUALIFIED.get(season, QUALIFIED_DEFAULT)
        out = {}
        for r in packet_rows:
            col, kind = HEADERS[r[0]]
            avg, n, rank = lg[col]
            ranked = BETTER.get(col) and qualified and rank
            out[(r[0],)] = {"Player": show(col, kind, row), "Qualified avg": KIND_FMT[kind](avg),
                            "Player rank": f"{rank} of {n}" if ranked else "—",
                            "Percentile": pctile(rank, n) if ranked else "—"}
        return out

    def usage(self):
        out = {}
        for r in self.full:
            lhp = self.lhp_pa.get(r["season"])
            if lhp is None:
                continue
            self.cur.execute("""
                SELECT coalesce(l.pa, 0)::float / a.pa AS share
                FROM main.batter_season a
                LEFT JOIN main.batter_season l ON l.batter_id = a.batter_id AND l.season = a.season AND l.split = 'vs_lhp'
                WHERE a.season = %s AND a.split = 'all' AND a.bats = %s AND a.pa >= %s""",
                             (r["season"], r["bats"], USAGE_MIN))
            shares = [x["share"] for x in self.cur.fetchall()]
            share = lhp / r["pa"]
            below = sum(v < share for v in shares)
            out[(str(r["season"]),)] = {
                "Season": str(r["season"]), "Bats": r["bats"], "PA": str(r["pa"]), "PA vs LHP": str(lhp),
                "PA vs RHP": str(r["pa"] - lhp), "Share vs LHP": f_pct(share),
                f"Avg share, same-handed hitters ({USAGE_MIN}+ PA)": f_pct(statistics.fmean(shares)) if shares else "—",
                "Hitters compared": str(len(shares)),
                "Share percentile": str(min(100, int((Decimal(100) * below / (len(shares) - 1))
                                                     .quantize(Decimal(1), rounding=ROUND_HALF_UP))))
                if len(shares) > 1 else "—"}
        return out

    def run(self, packet_text):
        """[(table, row key, header, packet value, expected value or None)]"""
        packet = parse_packet(packet_text)
        exp = self.expected(packet)
        cells = []
        for key, (headers, prow) in packet.items():
            table = " › ".join(x for x in key if x)
            mode, want = exp.get(key, (None, {}))
            nkey = 2 if key == ("By pitch group", "Seasons") or key[1].startswith("Trends by group") else 1
            for r in prow:
                rk = tuple(r[:nkey])
                e = want.get(rk)
                for h, v in zip(headers[nkey:], r[nkey:]):
                    if e is None or h in ("Team",):
                        expect = None  # no rule, or copied as is from the row
                    elif mode == "rows":
                        expect = show(*HEADERS[h], e) if h in HEADERS else None
                    else:
                        expect = e.get(h)
                    cells.append((table, rk, h, v, expect))
        # numbers in the text: league sizes and the data-through date
        text_checks = []
        m = re.search(r"League = the (\d+) qualified hitters in (\d{4})", packet_text)
        if m:
            text_checks.append(("League size in the note", m.group(1), str(self.league_sizes.get(int(m.group(2))))))
        for h3, n in self.league_sizes.items():
            if isinstance(h3, str):
                got = re.search(r"\((\d+) qualified hitters", h3)
                text_checks.append((f"League size in “{h3.split(' — ')[0]}”", got.group(1) if got else "?", str(n)))
        self.cur.execute("SELECT max(game_date) AS d FROM main.mlb_games WHERE game_type = 'R' AND season = %s",
                         (self.latest,))
        d = str(self.cur.fetchone()["d"])
        got = re.search(r"data through (\d{4}-\d\d-\d\d)", packet_text)
        text_checks.append(("Data-through date", got.group(1) if got else "?", d))
        return cells, text_checks


# ---------------------------------------------------------------- check 2: rows rebuilt from pitches

PA_CLASS = {"single": "1B", "double": "2B", "triple": "3B", "home_run": "HR", "walk": "uBB",
            "intent_walk": "IBB", "hit_by_pitch": "HBP", "sac_fly": "SF", "sac_fly_double_play": "SF",
            "sac_bunt": "SH", "sac_bunt_double_play": "SH", "catcher_interf": "CI",
            "field_error": "ROE_FC", "fielders_choice": "ROE_FC"}
OUTS = {"strikeout", "strikeout_double_play", "field_out", "force_out", "grounded_into_double_play",
        "double_play", "triple_play", "fielders_choice_out"}
SWING = set("SWMQFTOLXDE")
WHIFF = set("SWMQTO")
GROUP = {**{c: "fastball" for c in ("FF", "SI", "FC", "FT", "FA")},
         **{c: "breaking" for c in ("SL", "ST", "CU", "KC", "SV", "CS")},
         **{c: "offspeed" for c in ("CH", "FS", "FO", "SC")}}
HALF_PLATE = 17 / 24 + 1.45 / 12   # feet, ball radius included
BALL = 1.45 / 12


def quantile(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    pos = q * (len(xs) - 1)
    lo = math.floor(pos)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


class Check2:
    def __init__(self, cur, pid, seasons):
        self.notes = []
        cur.execute("""
            SELECT g.season, p.game_pk, p."atBatIndex"::int AS ab, p."index" AS idx, p."startTime" AS t, p."playId" AS play,
                   p."isPitch" AS is_pitch, p."details.call.code" AS call, p."details.type.code" AS ptype,
                   p."pitchData.coordinates.pX" AS px, p."pitchData.coordinates.pZ" AS pz,
                   p."pitchData.strikeZoneTop" AS top, p."pitchData.strikeZoneBottom" AS bot, p."pitchData.zone" AS zone,
                   p."details.isInPlay" AS in_play, p."hitData.launchSpeed" AS ev, p."hitData.launchAngle" AS la,
                   p."hitData.trajectory" AS traj, p."hitData.coordinates.coordX" AS hx, p."hitData.coordinates.coordY" AS hy,
                   p."result.eventType" AS event, p."matchup.pitchHand.code" AS hand, p."matchup.batSide.code" AS side
            FROM main.pbp p JOIN main.mlb_games g USING (game_pk)
            WHERE p."matchup.batter.id" = %s AND g.game_type = 'R' AND g.season = ANY(%s)""", (pid, list(seasons)))
        events = cur.fetchall()
        cur.execute("SELECT * FROM main.woba_weights WHERE season = ANY(%s)", (list(seasons),))
        self.w = {r["season"]: r for r in cur.fetchall()}
        events.sort(key=lambda e: (e["game_pk"], e["ab"], e["idx"] if e["idx"] is not None else -1,
                                   e["t"] or "", e["play"] or ""))
        by_pa = defaultdict(list)
        for e in events:
            by_pa[(e["season"], e["game_pk"], e["ab"])].append(e)

        self.pas, self.pitches = [], []
        no_play_id = null_traj = 0
        for (season, _, _), evs in by_pa.items():
            event = next((e["event"] for e in reversed(evs) if e["event"]), None)
            cls = PA_CLASS.get(event) or ("OUT" if event in OUTS else None)
            hit = next((e for e in reversed(evs) if e["in_play"]), None)
            seen, pitches = set(), []
            for e in evs:
                if not e["is_pitch"]:
                    continue
                if e["play"] is not None:
                    if e["play"] in seen:
                        continue
                    seen.add(e["play"])
                else:
                    no_play_id += 1
                pitches.append(e)
            for e in pitches:
                if e["px"] is not None and e["pz"] is not None and e["top"] is not None and e["bot"] is not None:
                    in_zone = abs(e["px"]) <= HALF_PLATE and e["bot"] - BALL <= e["pz"] <= e["top"] + BALL
                elif e["zone"] is not None:
                    in_zone = 1 <= e["zone"] <= 9
                else:
                    in_zone = None
                self.pitches.append({"season": season, "hand": e["hand"], "group": GROUP.get(e["ptype"]),
                                     "in_zone": in_zone, "swing": (e["call"] or "") in SWING and e["call"] is not None,
                                     "whiff": (e["call"] or "") in WHIFF and e["call"] is not None})
            if cls is None:
                continue
            ev = hit["ev"] if hit else None
            la = hit["la"] if hit else None
            traj = (hit["traj"] or None) if hit else None
            if ev is not None and traj is None:
                null_traj += 1
            spray = None
            if hit and hit["hx"] is not None and hit["hy"] is not None:
                spray = math.degrees(math.atan2(hit["hx"] - 125.42, 198.27 - hit["hy"]))
            last_type = next((e["ptype"] for e in reversed(pitches)), None)
            self.pas.append({"season": season, "hand": evs[0]["hand"], "side": evs[0]["side"], "event": event,
                             "cls": cls, "ev": ev, "la": la, "traj": traj, "spray": spray,
                             "group": GROUP.get(last_type) if pitches else None})
        if no_play_id:
            self.notes.append(f"{no_play_id} pitches have no play ID, so they can't be checked for duplicates; "
                              "they are all counted here.")
        if null_traj:
            self.notes.append(f"{null_traj} tracked batted balls have no trajectory. Here they count as non-bunts in "
                              "Avg EV, EV90 and launch angle.")

    def season_line(self, pas, pitches, season):
        c = defaultdict(int)
        for p in pas:
            c[p["cls"]] += 1
        so = sum(p["event"] in ("strikeout", "strikeout_double_play") for p in pas)
        ab = c["1B"] + c["2B"] + c["3B"] + c["HR"] + c["ROE_FC"] + c["OUT"]
        h = c["1B"] + c["2B"] + c["3B"] + c["HR"]
        bb = c["uBB"] + c["IBB"]
        pa = len(pas)
        w = self.w[season]
        div = lambda a, b: a / b if b else None
        bat = [p for p in pas if p["ev"] is not None]
        nonbunt = [p for p in bat if not (p["traj"] or "").startswith("bunt")]
        evs = [p["ev"] for p in nonbunt]
        las = [p["la"] for p in nonbunt if p["la"] is not None]
        traj = [p for p in pas if p["traj"]]
        dirn = [p for p in bat if p["spray"] is not None]

        def pulled(p):
            return (p["side"] == "R" and p["spray"] < -16) or (p["side"] == "L" and p["spray"] > 16)

        def oppo(p):
            return (p["side"] == "R" and p["spray"] > 16) or (p["side"] == "L" and p["spray"] < -16)

        zp = [x for x in pitches if x["in_zone"] is True]
        op = [x for x in pitches if x["in_zone"] is False]
        sw = [x for x in pitches if x["swing"]]
        woba_num = (float(w["w_ubb"]) * c["uBB"] + float(w["w_hbp"]) * c["HBP"] + float(w["w_1b"]) * c["1B"]
                    + float(w["w_2b"]) * c["2B"] + float(w["w_3b"]) * c["3B"] + float(w["w_hr"]) * c["HR"])
        return {
            "pa": pa, "ab": ab, "h": h, "doubles": c["2B"], "triples": c["3B"], "hr": c["HR"], "bb": bb,
            "ibb": c["IBB"], "hbp": c["HBP"], "so": so, "sf": c["SF"],
            "avg": div(h, ab), "obp": div(h + bb + c["HBP"], ab + bb + c["HBP"] + c["SF"]),
            "slg": div(c["1B"] + 2 * c["2B"] + 3 * c["3B"] + 4 * c["HR"], ab),
            "iso": div(c["2B"] + 2 * c["3B"] + 3 * c["HR"], ab),
            "babip": div(h - c["HR"], ab - so - c["HR"] + c["SF"]),
            "k_pct": div(so, pa), "bb_pct": div(bb, pa),
            "woba": div(woba_num, ab + c["uBB"] + c["SF"] + c["HBP"]),
            "bbe": len(bat), "avg_ev": statistics.fmean(evs) if evs else None, "ev90": quantile(evs, 0.9),
            "median_la": statistics.median(las) if las else None,
            "sd_la": statistics.stdev(las) if len(las) > 1 else None,
            "hard_hit_pct": div(sum(p["ev"] >= 95 for p in bat), len(bat)),
            "barrel_pct": div(sum(p["ev"] >= 98 and p["la"] is not None and p["la"] <= 50
                                  and 1.5 * p["ev"] - p["la"] >= 117 and p["ev"] + p["la"] >= 124 for p in bat), len(bat)),
            "sweet_spot_pct": div(sum(1 if p["la"] is not None and 8 < p["la"] < 32 else
                                      0.5 if p["la"] in (8, 32) else 0 for p in bat), len(bat)),
            "gb_pct": div(sum(p["traj"] in ("ground_ball", "bunt_grounder") for p in traj), len(traj)),
            "ld_pct": div(sum(p["traj"] in ("line_drive", "bunt_line_drive") for p in traj), len(traj)),
            "fb_pct": div(sum(p["traj"] == "fly_ball" for p in traj), len(traj)),
            "pu_pct": div(sum(p["traj"] in ("popup", "bunt_popup") for p in traj), len(traj)),
            "pull_pct": div(sum(pulled(p) for p in dirn), len(dirn)),
            "oppo_pct": div(sum(oppo(p) for p in dirn), len(dirn)),
            "pulled_fb_pct": div(sum(pulled(p) and p["traj"] is not None
                                     and p["traj"] not in ("ground_ball", "bunt_grounder") for p in dirn), len(dirn)),
            "pitches": len(pitches), "z_swing_pct": div(sum(x["swing"] for x in zp), len(zp)),
            "chase_pct": div(sum(x["swing"] for x in op), len(op)),
            "whiff_pct": div(sum(x["whiff"] for x in sw), len(sw)),
        }

    def rebuild(self, seasons):
        """{(season, split or group): rebuilt row}"""
        out = {}
        for s in seasons:
            pas = [p for p in self.pas if p["season"] == s]
            pit = [x for x in self.pitches if x["season"] == s]
            out[(s, "all")] = self.season_line(pas, pit, s)
            for split, hand in (("vs_lhp", "L"), ("vs_rhp", "R")):
                out[(s, split)] = self.season_line([p for p in pas if p["hand"] == hand],
                                                   [x for x in pit if x["hand"] == hand], s)
            grouped = sum(1 for x in pit if x["group"])
            for g in ("fastball", "breaking", "offspeed"):
                line = self.season_line([p for p in pas if p["group"] == g], [x for x in pit if x["group"] == g], s)
                line["pitch_share"] = line["pitches"] / grouped if grouped else None
                out[(s, g)] = line
        return out


# Columns compared in check 2: (label, column, display kind)
SEASON_COLS = [
    ("PA", "pa", "int"), ("AB", "ab", "int"), ("H", "h", "int"), ("2B", "doubles", "int"), ("3B", "triples", "int"),
    ("HR", "hr", "int"), ("BB", "bb", "int"), ("IBB", "ibb", "int"), ("HBP", "hbp", "int"), ("SO", "so", "int"),
    ("SF", "sf", "int"), ("AVG", "avg", "rate"), ("OBP", "obp", "rate"), ("SLG", "slg", "rate"),
    ("ISO", "iso", "rate"), ("BABIP", "babip", "rate"), ("wOBA", "woba", "rate"), ("K%", "k_pct", "pct"),
    ("BB%", "bb_pct", "pct"), ("BBE", "bbe", "int"), ("Avg EV", "avg_ev", "one"), ("EV90", "ev90", "one"),
    ("LA median", "median_la", "one"), ("LA SD", "sd_la", "one"), ("Hard-hit%", "hard_hit_pct", "pct"),
    ("Barrel%", "barrel_pct", "pct"), ("Sweet spot%", "sweet_spot_pct", "pct"), ("GB%", "gb_pct", "pct"),
    ("LD%", "ld_pct", "pct"), ("FB%", "fb_pct", "pct"), ("PU%", "pu_pct", "pct"), ("Pull%", "pull_pct", "pct"),
    ("Oppo%", "oppo_pct", "pct"), ("Pulled Air%", "pulled_fb_pct", "pct"), ("Pitches", "pitches", "int"),
    ("IZ Swing%", "z_swing_pct", "pct"), ("Chase%", "chase_pct", "pct"), ("Whiff%", "whiff_pct", "pct"),
]
GROUP_COLS = [
    ("Pitches", "pitches", "int"), ("Share", "pitch_share", "pct"), ("IZ Swing%", "z_swing_pct", "pct"),
    ("Chase%", "chase_pct", "pct"), ("Whiff%", "whiff_pct", "pct"), ("PA ending", "pa", "int"),
    ("wOBA", "woba", "rate"), ("K%", "k_pct", "pct"), ("BBE", "bbe", "int"), ("EV90", "ev90", "one"),
    ("Hard-hit%", "hard_hit_pct", "pct"), ("Barrel%", "barrel_pct", "pct"),
]
# Half a display unit: the database rounds half away from zero and Python half to even, so a
# value exactly on a rounding boundary may show one unit apart without being wrong.
HALF = {"rate": 0.0005, "pct": 0.0005, "one": 0.05, "int": 0}


def same(kind, a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= HALF[kind] + 1e-9


# ---------------------------------------------------------------- check 3: public sources

def check3(rows, groups, pid, seasons, folder):
    """[(season, label, ours, theirs, diff text, tolerance text, ok, note)]"""
    out = []
    for s in seasons:
        try:
            src = validate.load_sources(folder, s)
        except FileNotFoundError:
            continue
        r = rows.get((s, "all"))
        if r is None:
            continue
        for label, col, key, scol, scale, unit, tol, note in validate.SAVANT:
            them = src[key].get(pid)
            theirs = validate.num(them.get(scol)) if them else None
            theirs = None if theirs is None else theirs * scale
            out.append(compare3(s, f"{label} ({'FanGraphs' if key == 'fangraphs' else 'Savant'})",
                                r.get(col), theirs, unit, tol, note))
        for g in ("fastball", "breaking", "offspeed"):
            ours = groups.get((s, g))
            arsenal = src["arsenal"].get((pid, g))
            if not ours or not arsenal:
                continue
            for label, col, how, unit, tol, note in validate.ARSENAL:
                theirs = validate.rollup(arsenal, how)
                if theirs is not None and unit == "pct":
                    theirs *= 0.01
                out.append(compare3(s, f"{g} {label} (Savant arsenal)", ours.get(col), theirs, unit, tol, note))
    return out


def compare3(season, label, ours, theirs, unit, tol, note):
    fmt = {"rate": f_rate, "pct": f_pct, "mph": f_one, "fts": lambda x: "—" if x is None else f"{x:.2f}",
           "count": lambda x: "—" if x is None else f"{x:.0f}"}[unit]
    if ours is None or theirs is None:
        return (season, label, fmt(ours), fmt(theirs), "—", "—", None, note or "not available")
    k = validate.display_scale(unit)
    d = (ours - theirs) * k
    unit_s = {"rate": "pts", "pct": "pts", "mph": "mph", "fts": "ft/s", "count": ""}[unit]
    return (season, label, fmt(ours), fmt(theirs), f"{d:+.1f} {unit_s}".strip() if unit != "count" else f"{d:+.0f}",
            f"±{tol} {unit_s}".strip(), abs(d) <= tol + 1e-9, note)


# ---------------------------------------------------------------- the sheet

def md(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python -I validation/audit_packet.py "Player Name"')
    packet_text = data.get_hitter_data(sys.argv[1])
    folders = sorted(p for p in (HERE / "downloads").iterdir() if p.is_dir() and re.match(r"\d{4}-\d\d-\d\d", p.name))
    with psycopg.connect(data.CONNINFO, autocommit=True, row_factory=dict_row) as conn, conn.cursor() as cur:
        player = data.resolve_player(cur, sys.argv[1])
        pid, name = player["player_id"], player["full_name"]
        c1 = Check1(cur, pid)
        cells, text_checks = c1.run(packet_text)
        seasons = [r["season"] for r in c1.full]
        cur.execute("SELECT * FROM main.batter_season WHERE batter_id = %s AND season = ANY(%s)", (pid, seasons))
        db_rows = {(r["season"], r["split"]): r for r in cur.fetchall()}
        cur.execute("SELECT * FROM main.batter_pitch_group_season WHERE batter_id = %s AND season = ANY(%s)",
                    (pid, seasons))
        db_groups = {(r["season"], r["pitch_group"]): r for r in cur.fetchall()}
        c2 = Check2(cur, pid, seasons)
        rebuilt = c2.rebuild(seasons)
    checks3 = check3(db_rows, db_groups, pid, seasons, folders[-1]) if folders else []

    # ---- check 1 results
    checked = [c for c in cells if c[4] is not None]
    unchecked = [c for c in cells if c[4] is None]
    diff1 = [c for c in checked if c[3] != c[4]]
    diff_text = [t for t in text_checks if t[1] != t[2]]

    # ---- check 2 results
    rows2, diff2, tables2 = [], [], defaultdict(list)
    for source, cols, keys in ((db_rows, SEASON_COLS, ("all", "vs_lhp", "vs_rhp")),
                               (db_groups, GROUP_COLS, ("fastball", "breaking", "offspeed"))):
        for k in keys:
            for label, col, kind in cols:
                line = [label]
                for s in seasons:
                    db_v, mine = (source.get((s, k)) or {}).get(col), rebuilt[(s, k)].get(col)
                    ok = same(kind, db_v, mine)
                    shown = KIND_FMT[kind](db_v)
                    line.append(f"{shown} ✓" if ok else f"**{shown} vs {KIND_FMT[kind](mine)}** ✗")
                    rows2.append(ok)
                    if not ok:
                        diff2.append((k, s, label, shown, KIND_FMT[kind](mine)))
                tables2[k].append(line)

    # ---- check 3 results
    diff3 = [c for c in checks3 if c[6] is False]
    n3 = [c for c in checks3 if c[6] is not None]

    # ---- write the sheet
    today = date.today().isoformat()
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{slug}_{today}.md"
    L = []
    L += [f"# Packet audit: {name}", "",
          f"Run {today} on the data packet `data.py` builds today ({len(cells) + len(text_checks)} numbers in its "
          f"tables and notes). Seasons in the packet: {', '.join(map(str, seasons))}.", "",
          "Three checks, each done without `data.py`'s own code:", "",
          "1. **Packet math.** Every table cell rebuilt from the database rows: the computed numbers (xISO, "
          "IZ Swing − Chase, gaps), season-over-season changes, trend wording, league averages, ranks and "
          "percentiles (ranked in SQL), platoon usage and the pitch-group tables. Must match exactly.",
          "2. **Rows rebuilt from pitches.** His season, split and pitch-group rows recomputed from the raw "
          "pitch-by-pitch table, so the nightly pipeline is checked too. Must match to the digit shown. "
          "The house expected stats (xwOBA, xBA, xSLG) come from a model and can't be rebuilt this way.",
          f"3. **Public sources.** His rows against Baseball Savant and FanGraphs (downloaded "
          f"{folders[-1].name if folders else 'never'}), within the tolerances of the league-wide validation.", ""]
    L += ["## Summary", "",
          md(["Check", "Numbers checked", "Match", "Differ", "Not checked"],
             [["1. Packet math", len(checked) + len(text_checks), len(checked) - len(diff1) + len(text_checks) - len(diff_text),
               len(diff1) + len(diff_text), len(unchecked)],
              ["2. Rows rebuilt from pitches", len(rows2), sum(rows2), len(rows2) - sum(rows2), "—"],
              ["3. Savant / FanGraphs", len(n3), len(n3) - len(diff3), len(diff3), len(checks3) - len(n3)]]), ""]

    L += ["## Everything that differs", ""]
    if not (diff1 or diff_text or diff2 or diff3):
        L.append("Nothing. Every number checked matches.")
    if diff1 or diff_text:
        halfway = dict(HALFWAY)
        why = lambda e: (f"Exactly halfway ({halfway[e]}): the packet rounds halves to the even number, this "
                         "audit rounds them up. Not an error." if e in halfway else "")
        L += ["**Packet math**", "", md(["Table", "Row", "Column", "Packet", "Recomputed", "Why"],
                                         [[t, " / ".join(rk), h, v, e, why(e)] for t, rk, h, v, e in diff1]
                                         + [["Text", n, "", a, b, ""] for n, a, b in diff_text]), ""]
    if diff2:
        L += ["**Rows rebuilt from pitches**", "",
              md(["Split / group", "Season", "Metric", "Database", "Rebuilt"], [list(map(str, d)) for d in diff2]), ""]
    if diff3:
        L += ["**Outside tolerance vs Savant / FanGraphs**", "",
              md(["Season", "Metric", "Ours", "Theirs", "Diff", "Tolerance", "Note"],
                 [[s, lbl, a, b, d, t, n] for s, lbl, a, b, d, t, _, n in diff3]), ""]

    L += ["## 1. Packet math", "",
          "Each table in the packet, cell by cell. A table with nothing listed under it matched in full.", ""]
    by_table = defaultdict(list)
    for c in cells:
        by_table[c[0]].append(c)
    for t, cs in by_table.items():
        ok = sum(1 for c in cs if c[4] is not None and c[3] == c[4])
        bad = [c for c in cs if c[4] is not None and c[3] != c[4]]
        skip = sorted({c[2] for c in cs if c[4] is None})
        L.append(f"- **{t}**: {ok} of {len(cs)} match"
                 + (f"; {len(bad)} differ" if bad else "")
                 + (f"; not checked: {', '.join(skip)}" if skip else ""))
    L += ["", md(["Number in the text", "Packet", "Recomputed"], [[n, a, b + (" ✓" if a == b else " ✗")]
                                                                  for n, a, b in text_checks]), ""]
    if unchecked:
        L += ["Not checked means the column is copied as is from the database row (team name) or this "
              "audit has no rule for it yet.", ""]

    L += ["## 2. Rows rebuilt from pitches", "",
          "The database value, then ✓ if rebuilding it from the raw pitches gives the same number to the digit "
          "shown. A ✗ shows both values.", ""]
    for note in c2.notes:
        L.append(f"- {note}")
    if c2.notes:
        L.append("")
    titles = {"all": "Full season", "vs_lhp": "vs LHP", "vs_rhp": "vs RHP", "fastball": "Fastball (pitch group)",
              "breaking": "Breaking (pitch group)", "offspeed": "Offspeed (pitch group)"}
    for k, lines in tables2.items():
        L += [f"### {titles[k]}", "", md(["Metric"] + [str(s) for s in seasons], lines), ""]

    L += ["## 3. Compared with Baseball Savant and FanGraphs", "",
          "His database rows against the public numbers. Tolerances are the league-wide validation's "
          "(`validation/validate.py`). The house-model stats (xwOBA, xBA, xSLG) differ by design. "
          "Pitch groups compare against Savant's pitch types rolled up into our three groups, which is approximate.", ""]
    for s in seasons:
        rs = [c for c in checks3 if c[0] == s]
        if rs:
            L += [f"### {s}", "", md(["Metric", "Ours", "Theirs", "Diff", "Tolerance", "", "Note"],
                                     [[lbl, a, b, d, t, "—" if ok is None else ("✓" if ok else "✗"), n]
                                      for _, lbl, a, b, d, t, ok, n in rs]), ""]
    path.write_text("\n".join(L) + "\n")

    print(f"Wrote {path.relative_to(HERE.parent)}")
    print(f"  1. packet math: {len(checked) + len(text_checks)} checked, {len(diff1) + len(diff_text)} differ, "
          f"{len(unchecked)} not checked")
    print(f"  2. rebuilt from pitches: {len(rows2)} checked, {len(rows2) - sum(rows2)} differ")
    print(f"  3. Savant / FanGraphs: {len(n3)} checked, {len(diff3)} outside tolerance")


if __name__ == "__main__":
    main()
