# MLB hitter profiles (Claude API workflow)

Type a hitter's name; get a scouting-style profile written by Claude: how he drives
value, his strengths and weaknesses, and his style. Code gathers and computes every
number; the model only interprets them. One API call per report, streamed. Each report
also becomes an interactive page: charts and tables drawn by code, with Claude's text.

```
name → data.py (data packet) ─┐
                              ├→ report.py → Claude (claude-opus-5-5) → reports/<player>_<time>.md + .json
prompts/system_vN.md ─────────┤                        └→ html_report.py → docs/<player>.html
  + hitter_evaluation.md      │
  + metrics.md ───────────────┘
```

If a saved report was made from the same instructions, data and settings, `report.py`
reuses it instead of calling Claude again ($0). New games or an edit to the prompt,
method or glossary produce a new report. `--fresh` always writes a new one.

## Run it

```bash
cd ~/mlb_analyst
.venv/bin/python data.py "Pete Crow-Armstrong"          # the data packet only (free, no AI)
.venv/bin/python report.py "Pete Crow-Armstrong"        # report + page (~$0.17, or $0 if reused)
.venv/bin/python report.py "Pete Crow-Armstrong" --fresh   # force a new report
.venv/bin/python report.py "Nick Sogard" --prompt v1 --effort medium   # other prompt / effort
.venv/bin/python visuals.py "Wilyer Abreu"               # static PNG charts (for Substack)
```

Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

The API key is read from `.env` (`ANTHROPIC_API_KEY=...`). Never commit or share that file.

## Files

| File | What it is |
|---|---|
| `data.py` | Builds the data packet from the `mlb` Postgres database. No AI: same name in, same numbers out. All math (averages, ranks, percentiles, changes) happens here. |
| `report.py` | Assembles the system prompt, sends it with the packet to Claude, streams the report, and saves it with a `.json` record (prompt, model, tokens, cost, packet). Reuses a matching saved report instead of paying for a new one. Then builds the page. |
| `html_report.py` + `templates/report.html` | The interactive page: percentile chart with a season switch, shaded season tables, platoon and pitch-type charts, hover definitions. Every number comes from the database, not from the model. |
| `docs/` | The website, published by GitHub Pages at https://calchristofori.github.io/mlb-hitter-profiles/: one page per player plus a home page listing them. Rebuilt on every report run. |
| `visuals.py` | The same charts and tables as static images, for places that can't show the page (Substack). |
| `prompts/system_vN.md` | The system prompt, versioned. `{{METHOD}}` and `{{GLOSSARY}}` are filled in at run time. v8 is current: the report is about the latest season (the packet holds only the last three), cites about 20 numbers, and describes ranks in words. Chosen with the eval (see `evals/`). |
| `hitter_evaluation.md` | The evaluation method: the baseball judgment behind every report. |
| `metrics.md` | The metric glossary: what each number means, how it's computed, and how it compares with Savant and FanGraphs. The single source of truth for definitions. |
| `reports/` | Every report written. `.json` records stay local (not committed). `reports/visuals/` holds the static images. |
| `evals/` | The eval: are the reports good? `eval_plan.md` holds the test hitters, the answer key and the checklist; `run_eval.py` writes reports for each hitter (never published), scores them with code checks and an AI grader, and saves a scorecard to `evals/runs/<time>/`. Full run ~$5: `.venv/bin/python evals/run_eval.py`. |
| `validation/` | Checks the database against MLB, Savant and FanGraphs: `bash validation/fetch_sources.sh 2023 2026`, then `.venv/bin/python -I validation/validate.py 2023 2026`. |
| `learn/data_annotated.py` | A heavily commented copy of `data.py`, with a Python primer, for reading. Doesn't update itself. |
| `archive/desktop_prototype/` | The earlier Claude Desktop (MCP) version. Not maintained. |

## Where the data comes from

The `mlb` database is built nightly by `~/mlb_data_scripts/run_daily.sh` from the public MLB Stats API
and Baseball Savant. `data.py` reads it through the read-only `mlb_analyst` login.
