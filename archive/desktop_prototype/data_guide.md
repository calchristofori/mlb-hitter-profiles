# MLB database guide

Postgres database `mlb`, schema `main`. Always schema-qualify tables (`main.batter_season`).
Data comes from the public MLB Stats API and refreshes every morning at 6 AM ET.

## Freshness

| Data | Coverage |
|---|---|
| Sprint speed (`sprint_speed`, from Baseball Savant) | 2015 – today |
| MLB games, pitch-by-pitch, win probability, linescores | 2015 – yesterday (regular season, postseason, spring training) |
| 40-man rosters (daily snapshots) | 2002 – today |
| Transactions | 2000 – yesterday |
| `batter_season` (hitting stats) | MLB regular season 2015 – yesterday |
| Minor league games (`minors_games`) | 2015 – **May 19, 2026 (stale)** |
| Minor league pitch-by-pitch (`minors_pbp`) | 2015 – **Jul 25, 2026 (stale)** |

If a question needs minor league data after those dates, say the data isn't current.

## Start here: which table answers what

| Question about… | Use |
|---|---|
| A hitter's season stats, leaderboards, platoon splits, contact quality, plate discipline | `batter_season` |
| A hitter vs. fastballs / breaking balls / offspeed, by season | `batter_pitch_group_season` |
| Who is on a 40-man roster / injured list on a given date | `rosters_40man_daily` |
| Call-ups, options, DFAs, trades, signings, IL placements over time | `transactions` |
| Player bio, handedness, position, debut, current team | `players` |
| Games, scores, schedules | `mlb_games` (MLB), `minors_games` (minors) |
| Team names, abbreviations, leagues, affiliates | `mlbteams` |
| Anything not in `batter_season` (pitcher stats, game-level or date-range hitting, counts, pitch types, situational splits) | `pbp` (pitch-by-pitch) — read its section first |
| Win probability / leverage by plate appearance | `mlb_game_wp` |

There is **no park factor data** — for park questions, only the home venue is known (`mlb_games.venue_name`).

There is **no pitcher stats table**. Pitcher questions must be computed from `pbp`; say that you are doing so.

## `batter_season` — hitting stats (validated against official MLB and Baseball Savant)

One row per **season × batter_id × split**. MLB **regular season only**.
- `split` = `'all'` (full season), `'vs_lhp'`, `'vs_rhp'`. **Always filter `split`** — otherwise each hitter appears three times.
- Traded players have one combined row; `teams` lists every team in the order he played for them, joined with `' / '`.
- `name` is the player's name; `batter_id` joins to `players.player_id`.
- Bio on every row: `age` (as of June 30 of that season), `pos`, `bats`, `throws`.
- Before 2022 (no universal DH) pitchers appear as hitters.

**Columns**
- Counting: `g` (games with a PA — not official games played), `pa`, `ab`, `h`, `singles`, `doubles`, `triples`, `hr`, `rbi`, `bb` (includes `ibb`), `ibb`, `hbp`, `so`, `sf`, `sh`, `gidp`, `bbe` (batted balls with tracking data), `pitches` (pitches seen).
- Rates (all stored as **decimals**: 0.285 = .285, 0.231 = 23.1%): `avg`, `obp`, `slg`, `ops`, `iso`, `babip`, `k_pct`, `bb_pct`, `woba`.
- Contact quality: `avg_ev` (mph), `ev90` (90th-percentile exit velocity), `median_la`, `sd_la` (std. dev. of launch angle, degrees) — these four **exclude bunts** (Statcast convention). `hard_hit_pct` (EV ≥ 95), `barrel_pct`, `sweet_spot_pct` (LA 8–32°), `gb_pct`, `ld_pct`, `fb_pct`, `pu_pct` — share of batted balls. FB% uses the Statcast definition: popups are counted separately (PU%), so it runs well below FanGraphs' FB%.
- Plate discipline: `z_swing_pct` (swing rate on pitches in the zone), `chase_pct` (swing rate on pitches outside the zone; "in the zone" = any part of the ball touches it, as on Savant — matches Savant within ~0.25 pts on average), `whiff_pct` (misses ÷ swings; foul tips count as misses, matching Savant). Swing-decision score = `z_swing_pct - chase_pct` (higher is better).
- Direction (share of batted balls): `pulled_fb_pct` — shown as **Pulled Air%** (balls in the air — fly balls, line drives, popups — hit to the pull side; Savant's "Pull AIR%"; within ~0.5 pts of Savant on average, occasionally 2+ pts apart), `pull_pct`, `oppo_pct` (approximate: run ~4 pts above Savant because ground-ball direction is inferred from where the ball was fielded — use for trends, not cross-source comparisons).
- **Expected stats (house model)**: `xba`, `xslg`, `xwoba`. Built from this database, not copied from Savant: every tracked batted ball gets single/double/triple/HR probabilities from what balls with the same exit velocity and launch angle did that season (bunts modeled separately; ground balls and bunts adjusted for the batter's sprint speed). Walks, HBP and strikeouts count at actual value. Validated against Savant 2019/2023/2026 (qualified hitters): correlation 0.99+ for xwOBA and xSLG, 0.98–0.99 for xBA; typical difference 3–7 points of xwOBA. Call them "xwOBA (house model)" in reports. The model tables (`xstat_model`, `xstat_speed_adj`) live only in the pipeline's DuckDB file, not in this Postgres database.
- `sprint_speed`: feet per second on competitive runs (Statcast, from Baseball Savant). ~27 is average, 30+ elite, under 25 slow. Null for players without enough runs.

**Accuracy notes**
- Counting stats match official MLB totals to within 0.02%; a few players differ by 1 because of late official-scoring changes.
- `woba` uses weights computed from this database (see `woba_weights`); it runs ~.005 above FanGraphs for big power hitters. Say "wOBA (house weights)" if precision matters.
- `barrel_pct` runs ~0.5 pts below Savant; `sweet_spot_pct` matches within ~0.3 pts (launch angles come rounded to whole degrees, so balls at exactly 8° or 32° count as half). Rankings are reliable.
- Known gap: automatic intentional walks (no pitch thrown) are missing from `pbp`, so `pa`, `bb` and `ibb` are short by about 12 per season league-wide (at most 1–2 for any one hitter).
- 2015–2019: ~10% of batted balls lack Statcast tracking, so contact metrics are based on fewer balls.
- `g` counts games with a plate appearance, not official games played.

**Sample-size rules (apply them, and state them in your answer)**
- Rate-stat leaderboards: qualified = `pa >= 502` for a full season (3.1 PA per team game; 2020 = 186). For in-progress seasons, scale by team games played, or use a stated minimum.
- Platoon splits: use a minimum (e.g. `pa >= 100`) and mention it.
- Contact / discipline leaderboards: use `bbe >= 150` or `pitches >= 1000` minimums.

`woba_weights`: one row per season — `w_ubb, w_hbp, w_1b, w_2b, w_3b, w_hr, woba_scale, lg_woba, run_value_out`.

## `batter_pitch_group_season` — hitting by pitch group
One row per **season × batter_id × pitch_group**, MLB regular season. Built with the same definitions as `batter_season`.
- `pitch_group`: `'fastball'` (four-seam, sinker, cutter, two-seam), `'breaking'` (slider, sweeper, curveball, knuckle curve, slurve, slow curve), `'offspeed'` (changeup, splitter, forkball, screwball). Eephus, knuckleballs and unknown pitch types are left out.
- **Two ways of counting** (as on Savant's pitch-type leaderboards):
  - Every pitch of the group he saw: `pitches`, `pitch_share` (share of his pitches in a known group), `z_swing_pct`, `chase_pct`, `whiff_pct`.
  - Only PAs that **ended** on a pitch of the group: `pa`, `woba`, `xwoba` (house model), `k_pct`, `bbe`, `ev90`, `hard_hit_pct`, `barrel_pct`. These `pa` are much smaller than the season total; the three groups add up to it, minus PAs with no pitch (automatic intentional walks).
- Rates are decimals, as in `batter_season`. Use minimums (e.g. `pa >= 50` per group) — samples get small fast.

## `players`
`player_id` (= MLBAM ID used everywhere), `full_name`, `first_name`, `last_name`, `use_name`, `birth_date`, `birth_country`, `height`, `weight`, `bat_side_code` (L/R/S), `pitch_hand_code`, `primary_position_abbreviation`, `mlb_debut_date`, `last_played_date`, `draft_year`, `active`, `current_team_id`, `current_team_name`.
Use the `find_player` tool to resolve names to IDs instead of guessing spellings.
`current_team_name` and `last_played_date` are often blank or out of date for active players — for a player's current team, use their latest row in `rosters_40man_daily` (or their most recent `pbp` games).

## `rosters_40man_daily` — **column names are UPPERCASE and must be double-quoted**
One row per player per day on a 40-man roster. Columns: `date`, `"ORG"` (team id), `"MLBAMID"` (player id), `"NAME"`, `"POS"`, `"STATUS"`, `team_id`, `note`, `roster_type` (always `'40Man'`).
`"STATUS"` values: `Active` (on the active MLB roster), `Forty Man` (on the 40-man, not active — usually optioned to the minors), `Injured 7-Day` / `10-Day` / `15-Day` / `60-Day`, `Reassigned to Minors`, `Paternity List`, `Bereavement List`, `Family Medical Emergency`, `Suspended # days`, `Not Yet Reported`.
Example: `SELECT "NAME", "POS", "STATUS" FROM main.rosters_40man_daily WHERE date = '2026-10-14' AND "ORG" = 158`.

## `transactions`
One row per player per transaction (multi-player moves share `transaction_id`). Columns: `transaction_id`, `date`, `effective_date`, `resolution_date`, `code`, `type`, `description` (full text), `"MLBAMID"` (quoted, uppercase), `name`, `to_team_id`, `from_team_id`.
Common `type` values: `Optioned`, `Recalled`, `Status Change` (IL placements/activations — read `description`), `Designated for Assignment`, `Outrighted`, `Released`, `Claimed Off Waivers`, `Trade`, `Signed`, `Signed as Free Agent`, `Selected`, `Contract Purchased`, `Assigned`, `Declared Free Agency`, `Rule 5 Selection`, `Suspension`, `Retired`.
Includes minor league moves. Filter on `type` and search `description` with `ILIKE` for detail.

## `mlb_games` / `minors_games`
One row per game: `game_pk`, `game_date`, `season`, `game_type`, `away_team_id`, `away_team_name`, `away_score`, `home_team_id`, `home_team_name`, `home_score`, `venue_name`, `detailed_state`. `minors_games` adds `level` (AAA, AA, A+, A, ROK).
`game_type`: `R` regular season, `S` spring training, `F` wild card, `D` division series, `L` league championship, `W` World Series, `E` exhibition, `A` All-Star.

## `mlbteams`
One row per team per season, all levels. `team_id`, `team_full_name`, `team_abbreviation`, `season`, `level` (MLB, AAA, AA, A+, A, ROK…), `league_name`, `division_name`, `parent_org_id` / `parent_org_name` (MLB parent club for affiliates), `venue_name`. MLB clubs: `sport_id = 1`.

## `player_seasons`
`player_id`, `season`, `level` — which levels a player appeared at each season.

## `pbp` — MLB pitch-by-pitch (9M+ rows; use only when `batter_season` can't answer)
One row per pitch **or** in-play event (pickoffs, substitutions, etc.). Key rules:
- **Column names contain dots and mixed case — always double-quote them**: `"matchup.batter.id"`, `"result.eventType"`.
- **Season**: `pbp.season` is unreliable (blank for most of 2026). Join `main.mlb_games` on `game_pk` and use `mlb_games.season`; filter `game_type = 'R'` for regular season.
- **`"atBatIndex"` is TEXT** — cast with `"atBatIndex"::int` before sorting or comparing.
- Pitches: filter `"isPitch" = true`. Plate appearance results: one result per `(game_pk, "atBatIndex")`; take `"result.eventType"` (it repeats on every row of the PA), e.g. `SELECT DISTINCT game_pk, "atBatIndex", "result.eventType"`.
- `"game_date"` is TEXT (`'2026-07-04'`).

Useful columns: `game_pk`, `game_date`, `"atBatIndex"`, `"index"` (event order within the PA), `"isPitch"`, `type`, `"about.inning"`, `"about.isTopInning"`, `"matchup.batter.id"`, `"matchup.batter.fullName"`, `"matchup.batSide.code"`, `"matchup.pitcher.id"`, `"matchup.pitcher.fullName"`, `"matchup.pitchHand.code"`, `"result.eventType"`, `"result.description"`, `"result.rbi"`, `"details.call.code"`, `"details.call.description"`, `"details.isInPlay"`, `"details.type.code"` / `"details.type.description"` (pitch type: FF four-seam, SI sinker, SL slider, ST sweeper, CU curve, CH changeup, FS splitter, FC cutter, KC knuckle-curve), `"pitchData.startSpeed"`, `"pitchData.breaks.spinRate"`, `"pitchData.breaks.breakHorizontal"`, `"pitchData.breaks.breakVerticalInduced"`, `"pitchData.extension"`, `"pitchData.zone"` (1–9 in zone, 11–14 outside), `"pitchData.coordinates.pX"` / `"pZ"`, `"hitData.launchSpeed"`, `"hitData.launchAngle"`, `"hitData.totalDistance"`, `"hitData.trajectory"`, `"count.balls.start"`, `"count.strikes.start"`, `"count.outs.start"`, `batting_team`, `fielding_team`, `home_team`, `away_team`.
Swing call codes: S, W, M, Q (misses), T, O (foul tips), F, L (fouls), X, D, E (in play). Whiffs: S, W, M, Q, T, O.
`"result.eventType"` values include single, double, triple, home_run, walk, intent_walk, hit_by_pitch, strikeout, field_out, force_out, grounded_into_double_play, sac_fly, sac_bunt, field_error, fielders_choice, catcher_interf; caught_stealing_*, pickoff_*, stolen_base_* are not plate appearances.

`minors_pbp` has the same layout (no `season` column; join `minors_games`).

## How to answer
1. Resolve player names with `find_player`, then query by ID.
2. Prefer `batter_season` over `pbp`. Keep queries focused and add `LIMIT`.
3. Show the SQL you ran and state filters and minimums ("qualified: 502+ PA").
4. Format rates baseball-style (.285, 23.1%).
5. If the data can't answer the question (stale minors data, no pitcher table, no contracts or projections), say so plainly instead of guessing.
