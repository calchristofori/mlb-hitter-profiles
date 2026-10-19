"""MLB analyst MCP server: read-only access to the `mlb` Postgres database.

Tools: get_data_guide, run_sql, find_player, describe_table.
Connects as the read-only `mlb_analyst` role (password from ~/.pgpass); the role
itself enforces read-only transactions and a 30s statement timeout.
"""

import os
import re
import unicodedata
from pathlib import Path

import psycopg
from mcp.server.mcpserver import MCPServer

CONNINFO = os.environ.get("MLB_ANALYST_CONN", "host=localhost port=5432 dbname=mlb user=mlb_analyst")
GUIDE = (Path(__file__).parent / "data_guide.md").read_text()
HITTER_METHOD = (Path(__file__).parent / "hitter_evaluation.md").read_text()
MAX_ROWS_CAP = 500
CELL_MAX = 200

mcp = MCPServer(
    name="mlb",
    instructions=(
        "Read-only MLB database (Postgres, schema `main`). Before writing your first query, "
        "read the data guide below; it explains which table answers what and the column-name gotchas.\n\n"
        + GUIDE
    ),
)


def _connect():
    return psycopg.connect(CONNINFO, autocommit=True)


def _fmt(v):
    if v is None:
        return ""
    if isinstance(v, float):
        v = round(v, 4)
    s = str(v).replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= CELL_MAX else s[:CELL_MAX] + "…"


def _table(cols, rows):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(_fmt(v) for v in r) + " |" for r in rows]
    return "\n".join(out)


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", "", s)


@mcp.tool()
def get_data_guide() -> str:
    """Return the guide to the MLB database: tables, column meanings, stat definitions,
    sample-size rules and SQL gotchas. Read it before writing queries."""
    return GUIDE


@mcp.tool()
def run_sql(sql: str, max_rows: int = 100) -> str:
    """Run one read-only SQL query (SELECT or WITH) against the MLB Postgres database
    and return the results as a table. Schema-qualify tables (main.batter_season).
    Results are capped at max_rows (up to 500); add ORDER BY / LIMIT for leaderboards.
    Queries time out after 30 seconds."""
    stmt = sql.strip().rstrip(";").strip()
    if ";" in stmt:
        return "Error: send one statement at a time."
    if not re.match(r"(?is)^\s*(select|with|explain)\b", stmt):
        return "Error: only SELECT / WITH / EXPLAIN queries are allowed (the database is read-only)."
    max_rows = max(1, min(int(max_rows), MAX_ROWS_CAP))
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(stmt)
            if cur.description is None:
                return "Query returned no result set."
            cols = [d.name for d in cur.description]
            rows = cur.fetchmany(max_rows + 1)
    except psycopg.Error as e:
        return f"SQL error: {e}".strip()
    truncated = len(rows) > max_rows
    rows = rows[:max_rows]
    note = f"{len(rows)} row(s)" + (f" — truncated at {max_rows}; refine the query or raise max_rows" if truncated else "")
    return note + "\n\n" + (_table(cols, rows) if rows else "(no rows)")


_PLAYERS = None


def _players():
    global _PLAYERS
    if _PLAYERS is None:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT p.player_id, p.full_name, coalesce(p.use_name, p.first_name), p.last_name,
                       p.primary_position_abbreviation, p.bat_side_code, p.pitch_hand_code,
                       p.current_team_name, p.mlb_debut_date, p.last_played_date, p.active,
                       b.last_season
                FROM main.players p
                LEFT JOIN (SELECT batter_id, max(season) AS last_season
                           FROM main.batter_season GROUP BY 1) b ON b.batter_id = p.player_id
            """)
            _PLAYERS = cur.fetchall()
    return _PLAYERS


@mcp.tool()
def find_player(name: str, limit: int = 10) -> str:
    """Look up players by name (accent- and case-insensitive; partial names and last
    names work) and return their player_id plus position, handedness, team and career
    dates. Use the player_id in queries; IDs match batter_id, MLBAMID, etc."""
    q = _norm(name).split()
    if not q:
        return "Error: give a name."
    hits = []
    for r in _players():
        full = _norm(r[1])
        alt = _norm(f"{r[2]} {r[3]}")
        if all(t in full or t in alt for t in q):
            exact = full == " ".join(q) or alt == " ".join(q)
            # exact name first, then players with MLB hitting stats (most recent first), then active
            hits.append((not exact, r[11] is None, -(r[11] or 0), not r[10], r))
    hits.sort(key=lambda h: h[:4])
    rows = [h[4] for h in hits[: max(1, min(int(limit), 50))]]
    if not rows:
        return f"No players match '{name}'. Try a last name or a different spelling."
    cols = ["player_id", "full_name", "use_name", "last_name", "pos", "bats", "throws",
            "current_team", "mlb_debut", "last_played", "active", "last_batter_season"]
    return f"{len(hits)} match(es); showing {len(rows)}\n\n" + _table(cols, rows)


@mcp.tool()
def describe_table(table: str, column_filter: str = "") -> str:
    """List a table's columns and types plus 3 sample rows. Use column_filter to search
    wide tables (e.g. table='pbp', column_filter='pitchData')."""
    t = table.split(".")[-1].strip()
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT column_name, data_type FROM information_schema.columns
                WHERE table_schema = 'main' AND table_name = %s AND column_name ILIKE %s
                ORDER BY ordinal_position""", (t, f"%{column_filter}%"))
            cols = cur.fetchall()
            if not cols:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY 1")
                return f"No columns found for '{table}'" + (f" matching '{column_filter}'" if column_filter else "") + \
                       ". Tables: " + ", ".join(r[0] for r in cur.fetchall())
            names = ", ".join('"' + c[0].replace('"', '""') + '"' for c in cols[:40])
            cur.execute(f'SELECT {names} FROM main."{t}" LIMIT 3')
            sample = cur.fetchall()
    except psycopg.Error as e:
        return f"SQL error: {e}".strip()
    out = f"main.{t}: {len(cols)} column(s)\n\n" + _table(["column", "type"], cols)
    out += "\n\nSample rows" + (" (first 40 columns)" if len(cols) > 40 else "") + ":\n\n"
    out += _table([c[0] for c in cols[:40]], sample)
    return out


HITTER_DATA_MAP = """
## Where each number comes from (main.batter_season, split = 'all' unless noted)
| Method term | Column / source |
|---|---|
| xwOBA, xSLG, xBA | `xwoba`, `xslg`, `xba` — house expected-stats model; label them "(house model)" |
| EV90 | `ev90` |
| Pulled Air% | `pulled_fb_pct` (balls in the air — fly balls, line drives, popups — to the pull side ÷ batted balls) |
| Pull% | `pull_pct` (approximate — fine for trends) |
| IZ Swing% − Chase% | `z_swing_pct - chase_pct` |
| Whiff% | `whiff_pct` |
| FB%, GB% | `fb_pct`, `gb_pct` (also `ld_pct`, `pu_pct`) |
| LA median / LA SD | `median_la`, `sd_la` |
| 8–32° sweet spot | `sweet_spot_pct` |
| wOBA, BABIP history | `woba`, `babip` by season |
| Sprint speed | `sprint_speed` (ft/s; ~27 average, 30+ elite) |
| Park | Not available — no park factors in the database. Say so in the gap check; you may name the home venue from `main.mlb_games`. |
| Header | `age`, `pos`, `bats`, `throws` from the latest season row; current team from the player's latest `main.rosters_40man_daily` row (fall back to `teams`) |
| Data dates | `SELECT max(game_date) FROM main.mlb_games WHERE game_type = 'R' AND season = <season>` |

Steps: 1) `find_player` to get the id. 2) One query for every season of the player's `split = 'all'` rows (last three seasons for the trend table; all seasons for BABIP history). 3) Optional: `vs_lhp` / `vs_rhp` rows for platoon context. 4) Write the report in the format above. Show numbers baseball-style (.383, 26.3%, 106.6 mph).
"""


@mcp.prompt()
def hitter_report(player: str) -> str:
    """Write a hitter analyst report using the house evaluation method and the MLB database."""
    return (f"Write a hitter analyst report on {player}. Use the mlb tools for every number.\n\n"
            + HITTER_METHOD + "\n" + HITTER_DATA_MAP)


if __name__ == "__main__":
    mcp.run()
