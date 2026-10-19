# MLB analyst (week-1 prototype)

An MCP server that lets Claude answer plain-English baseball questions from the `mlb`
Postgres database (kept current by `~/mlb_data_scripts/run_daily.sh`).

- `server.py` — tools: `get_data_guide`, `run_sql`, `find_player`, `describe_table`
- `data_guide.md` — what the AI knows about the data: tables, definitions, gotchas,
  sample-size rules. **Most accuracy fixes go here.** Restart Claude Desktop after editing.
- `hitter_evaluation.md` — the hitter evaluation method; served as the `hitter_report`
  prompt (+ menu in Claude Desktop → mlb → hitter_report, then type a player).
  `sample_reports/` has an example.
- Connects as the read-only Postgres role `mlb_analyst` (password in `~/.pgpass`,
  30-second query limit, cannot write).
- Registered in Claude Desktop as the `mlb` server
  (`~/Library/Application Support/Claude/claude_desktop_config.json`).

## Questions to try (and the start of the test set)

1. Who led MLB in wOBA in 2026 among qualified hitters?
2. Which qualified hitters chased least in 2026, and how hard do they hit the ball?
3. Show Pete Crow-Armstrong's year-by-year line.
4. Which left-handed hitters crushed lefties in 2026 (min 100 PA vs LHP)?
5. Who had the biggest drop in EV90 from 2025 to 2026?
6. Which Brewers were on the injured list on September 1, 2026?
7. List every player the Yankees optioned in August 2026.
8. Which hitters had the largest gap between wOBA vs LHP and vs RHP?
9. What's Aaron Judge's whiff rate by pitch type in 2026? (needs pbp)
10. Who threw the most sweepers in 2026? (no pitcher table — computed from pbp)

When an answer is wrong, write down the question and the correct answer — that list
becomes the test set for the real product.
