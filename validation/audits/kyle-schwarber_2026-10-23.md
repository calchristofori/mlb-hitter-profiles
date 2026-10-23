# Packet audit: Kyle Schwarber

Run 2026-10-23 on the data packet `data.py` builds today (860 numbers in its tables and notes). Seasons in the packet: 2024, 2025, 2026.

Three checks, each done without `data.py`'s own code:

1. **Packet math.** Every table cell rebuilt from the database rows: the computed numbers (xISO, IZ Swing − Chase, gaps), season-over-season changes, trend wording, league averages, ranks and percentiles (ranked in SQL), platoon usage and the pitch-group tables. Must match exactly.
2. **Rows rebuilt from pitches.** His season, split and pitch-group rows recomputed from the raw pitch-by-pitch table, so the nightly pipeline is checked too. Must match to the digit shown. The house expected stats (xwOBA, xBA, xSLG) come from a model and can't be rebuilt this way.
3. **Public sources.** His rows against Baseball Savant and FanGraphs (downloaded 2026-10-18), within the tolerances of the league-wide validation.

## Summary

| Check | Numbers checked | Match | Differ | Not checked |
|---|---|---|---|---|
| 1. Packet math | 857 | 856 | 1 | 3 |
| 2. Rows rebuilt from pitches | 450 | 450 | 0 | — |
| 3. Savant / FanGraphs | 147 | 136 | 11 | 0 |

## Everything that differs

**Packet math**

| Table | Row | Column | Packet | Recomputed | Why |
|---|---|---|---|---|---|
| League context by season | Sprint speed | 2024 pctl | 12 | 13 | Exactly halfway (12.5): the packet rounds halves to the even number, this audit rounds them up. Not an error. |

**Outside tolerance vs Savant / FanGraphs**

| Season | Metric | Ours | Theirs | Diff | Tolerance | Note |
|---|---|---|---|---|---|---|
| 2024 | Pull% (Savant) | 54.7% | 48.4% | +6.3 pts | ±6.0 pts | known approximate (~4 pts high) |
| 2024 | fastball Pitches (Savant arsenal) | 1548 | 1538 | +10 | ±5 |  |
| 2024 | offspeed K% (Savant arsenal) | 39.8% | 40.9% | -1.1 pts | ±1.0 pts | PA-weighted roll-up |
| 2025 | xwOBA (Savant) | .416 | .401 | +15.0 pts | ±10 pts | house model; guide says typical gap 3–7 pts |
| 2025 | fastball Pitches (Savant arsenal) | 1498 | 1489 | +9 | ±5 |  |
| 2025 | fastball PA ending (Savant arsenal) | 366 | 362 | +4 | ±2 |  |
| 2025 | offspeed xwOBA (Savant arsenal) | .407 | .382 | +25.5 pts | ±20 pts | house model; PA-weighted roll-up |
| 2026 | xwOBA (Savant) | .375 | .364 | +11.0 pts | ±10 pts | house model; guide says typical gap 3–7 pts |
| 2026 | Barrel% (Savant) | 14.5% | 15.6% | -1.1 pts | ±1.0 pts | guide says ~0.5 pts below Savant |
| 2026 | Chase% (Savant) | 24.6% | 26.1% | -1.5 pts | ±1.0 pts | zone = ball touches zone, as Savant |
| 2026 | offspeed xwOBA (Savant arsenal) | .333 | .311 | +22.3 pts | ±20 pts | house model; PA-weighted roll-up |

## 1. Packet math

Each table in the packet, cell by cell. A table with nothing listed under it matched in full.

- **Seasons (full season, last three seasons) › Core (foundational metrics)**: 27 of 30 match; not checked: Team
- **Seasons (full season, last three seasons) › Results vs. expected**: 33 of 33 match
- **Seasons (full season, last three seasons) › Contact quality and batted-ball shape**: 45 of 45 match
- **Seasons (full season, last three seasons) › Plate discipline**: 24 of 24 match
- **Season-over-season changes**: 57 of 57 match
- **2026 league context**: 96 of 96 match
- **League context by season**: 215 of 216 match; 1 differ
- **2026 platoon splits › Expected stats and batted-ball profile**: 32 of 32 match
- **2026 platoon splits › Plate discipline**: 16 of 16 match
- **2026 platoon splits › Platoon usage (last three seasons)**: 24 of 24 match
- **By pitch group › Seasons**: 135 of 135 match
- **By pitch group › Trends by group (last three seasons)**: 15 of 15 match
- **By pitch group › 2026 vs. fastball — league context (135 qualified hitters, 502+ season PA)**: 44 of 44 match
- **By pitch group › 2026 vs. breaking — league context (135 qualified hitters, 502+ season PA)**: 44 of 44 match
- **By pitch group › 2026 vs. offspeed — league context (135 qualified hitters, 502+ season PA)**: 44 of 44 match

| Number in the text | Packet | Recomputed |
|---|---|---|
| League size in the note | 135 | 135 ✓ |
| League size in “2026 vs. fastball” | 135 | 135 ✓ |
| League size in “2026 vs. breaking” | 135 | 135 ✓ |
| League size in “2026 vs. offspeed” | 135 | 135 ✓ |
| Data-through date | 2026-09-27 | 2026-09-27 ✓ |

Not checked means the column is copied as is from the database row (team name) or this audit has no rule for it yet.

## 2. Rows rebuilt from pitches

The database value, then ✓ if rebuilding it from the raw pitches gives the same number to the digit shown. A ✗ shows both values.

### Full season

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| PA | 692 ✓ | 724 ✓ | 701 ✓ |
| AB | 573 ✓ | 604 ✓ | 581 ✓ |
| H | 142 ✓ | 145 ✓ | 135 ✓ |
| 2B | 22 ✓ | 23 ✓ | 20 ✓ |
| 3B | 0 ✓ | 2 ✓ | 1 ✓ |
| HR | 38 ✓ | 56 ✓ | 45 ✓ |
| BB | 106 ✓ | 108 ✓ | 105 ✓ |
| IBB | 4 ✓ | 6 ✓ | 6 ✓ |
| HBP | 5 ✓ | 11 ✓ | 8 ✓ |
| SO | 197 ✓ | 197 ✓ | 220 ✓ |
| SF | 8 ✓ | 1 ✓ | 6 ✓ |
| AVG | .248 ✓ | .240 ✓ | .232 ✓ |
| OBP | .366 ✓ | .365 ✓ | .354 ✓ |
| SLG | .485 ✓ | .563 ✓ | .503 ✓ |
| ISO | .237 ✓ | .323 ✓ | .270 ✓ |
| BABIP | .301 ✓ | .253 ✓ | .280 ✓ |
| wOBA | .371 ✓ | .398 ✓ | .373 ✓ |
| K% | 28.5% ✓ | 27.2% ✓ | 31.4% ✓ |
| BB% | 15.3% ✓ | 14.9% ✓ | 15.0% ✓ |
| BBE | 384 ✓ | 408 ✓ | 366 ✓ |
| Avg EV | 93.6 ✓ | 94.3 ✓ | 92.3 ✓ |
| EV90 | 109.2 ✓ | 109.8 ✓ | 108.6 ✓ |
| LA median | 15.0 ✓ | 20.0 ✓ | 19.0 ✓ |
| LA SD | 29.5 ✓ | 27.8 ✓ | 28.9 ✓ |
| Hard-hit% | 55.5% ✓ | 59.6% ✓ | 49.5% ✓ |
| Barrel% | 15.1% ✓ | 20.8% ✓ | 14.5% ✓ |
| Sweet spot% | 32.0% ✓ | 34.9% ✓ | 37.4% ✓ |
| GB% | 40.9% ✓ | 34.3% ✓ | 31.3% ✓ |
| LD% | 22.7% ✓ | 22.5% ✓ | 26.4% ✓ |
| FB% | 28.6% ✓ | 34.3% ✓ | 31.9% ✓ |
| PU% | 7.8% ✓ | 8.8% ✓ | 10.4% ✓ |
| Pull% | 54.7% ✓ | 58.1% ✓ | 59.6% ✓ |
| Oppo% | 16.9% ✓ | 17.2% ✓ | 16.9% ✓ |
| Pulled Air% | 26.6% ✓ | 31.1% ✓ | 32.2% ✓ |
| Pitches | 2852 ✓ | 3059 ✓ | 2998 ✓ |
| IZ Swing% | 60.7% ✓ | 64.1% ✓ | 66.1% ✓ |
| Chase% | 20.9% ✓ | 21.5% ✓ | 24.6% ✓ |
| Whiff% | 32.0% ✓ | 33.1% ✓ | 33.1% ✓ |

### vs LHP

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| PA | 248 ✓ | 276 ✓ | 258 ✓ |
| AB | 210 ✓ | 234 ✓ | 215 ✓ |
| H | 63 ✓ | 59 ✓ | 56 ✓ |
| 2B | 4 ✓ | 8 ✓ | 8 ✓ |
| 3B | 0 ✓ | 2 ✓ | 1 ✓ |
| HR | 12 ✓ | 23 ✓ | 15 ✓ |
| BB | 36 ✓ | 36 ✓ | 36 ✓ |
| IBB | 0 ✓ | 0 ✓ | 0 ✓ |
| HBP | 2 ✓ | 6 ✓ | 6 ✓ |
| SO | 67 ✓ | 77 ✓ | 70 ✓ |
| SF | 0 ✓ | 0 ✓ | 1 ✓ |
| AVG | .300 ✓ | .252 ✓ | .260 ✓ |
| OBP | .407 ✓ | .366 ✓ | .380 ✓ |
| SLG | .490 ✓ | .598 ✓ | .516 ✓ |
| ISO | .190 ✓ | .346 ✓ | .256 ✓ |
| BABIP | .389 ✓ | .269 ✓ | .313 ✓ |
| wOBA | .395 ✓ | .413 ✓ | .394 ✓ |
| K% | 27.0% ✓ | 27.9% ✓ | 27.1% ✓ |
| BB% | 14.5% ✓ | 13.0% ✓ | 14.0% ✓ |
| BBE | 143 ✓ | 157 ✓ | 145 ✓ |
| Avg EV | 93.9 ✓ | 91.6 ✓ | 91.0 ✓ |
| EV90 | 109.7 ✓ | 109.2 ✓ | 108.0 ✓ |
| LA median | 8.0 ✓ | 22.0 ✓ | 16.0 ✓ |
| LA SD | 28.8 ✓ | 28.3 ✓ | 28.2 ✓ |
| Hard-hit% | 55.2% ✓ | 54.1% ✓ | 44.8% ✓ |
| Barrel% | 10.5% ✓ | 20.4% ✓ | 12.4% ✓ |
| Sweet spot% | 29.7% ✓ | 40.4% ✓ | 39.0% ✓ |
| GB% | 50.3% ✓ | 29.9% ✓ | 33.6% ✓ |
| LD% | 19.6% ✓ | 26.1% ✓ | 30.1% ✓ |
| FB% | 21.7% ✓ | 32.5% ✓ | 28.8% ✓ |
| PU% | 8.4% ✓ | 11.5% ✓ | 7.5% ✓ |
| Pull% | 54.5% ✓ | 56.7% ✓ | 58.6% ✓ |
| Oppo% | 14.0% ✓ | 17.8% ✓ | 16.6% ✓ |
| Pulled Air% | 21.0% ✓ | 33.8% ✓ | 29.0% ✓ |
| Pitches | 1017 ✓ | 1183 ✓ | 1113 ✓ |
| IZ Swing% | 57.1% ✓ | 63.6% ✓ | 65.7% ✓ |
| Chase% | 18.8% ✓ | 21.2% ✓ | 21.2% ✓ |
| Whiff% | 29.7% ✓ | 33.5% ✓ | 29.9% ✓ |

### vs RHP

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| PA | 444 ✓ | 448 ✓ | 443 ✓ |
| AB | 363 ✓ | 370 ✓ | 366 ✓ |
| H | 79 ✓ | 86 ✓ | 79 ✓ |
| 2B | 18 ✓ | 15 ✓ | 12 ✓ |
| 3B | 0 ✓ | 0 ✓ | 0 ✓ |
| HR | 26 ✓ | 33 ✓ | 30 ✓ |
| BB | 70 ✓ | 72 ✓ | 69 ✓ |
| IBB | 4 ✓ | 6 ✓ | 6 ✓ |
| HBP | 3 ✓ | 5 ✓ | 2 ✓ |
| SO | 130 ✓ | 120 ✓ | 150 ✓ |
| SF | 8 ✓ | 1 ✓ | 5 ✓ |
| AVG | .218 ✓ | .232 ✓ | .216 ✓ |
| OBP | .342 ✓ | .364 ✓ | .339 ✓ |
| SLG | .482 ✓ | .541 ✓ | .495 ✓ |
| ISO | .264 ✓ | .308 ✓ | .279 ✓ |
| BABIP | .247 ✓ | .243 ✓ | .257 ✓ |
| wOBA | .357 ✓ | .388 ✓ | .361 ✓ |
| K% | 29.3% ✓ | 26.8% ✓ | 33.9% ✓ |
| BB% | 15.8% ✓ | 16.1% ✓ | 15.6% ✓ |
| BBE | 241 ✓ | 251 ✓ | 221 ✓ |
| Avg EV | 93.4 ✓ | 96.0 ✓ | 93.2 ✓ |
| EV90 | 108.5 ✓ | 110.9 ✓ | 108.6 ✓ |
| LA median | 18.0 ✓ | 18.0 ✓ | 20.0 ✓ |
| LA SD | 29.9 ✓ | 27.5 ✓ | 29.1 ✓ |
| Hard-hit% | 55.6% ✓ | 62.9% ✓ | 52.5% ✓ |
| Barrel% | 17.8% ✓ | 21.1% ✓ | 15.8% ✓ |
| Sweet spot% | 33.4% ✓ | 31.5% ✓ | 36.4% ✓ |
| GB% | 35.3% ✓ | 37.1% ✓ | 29.9% ✓ |
| LD% | 24.5% ✓ | 20.3% ✓ | 24.0% ✓ |
| FB% | 32.8% ✓ | 35.5% ✓ | 33.9% ✓ |
| PU% | 7.5% ✓ | 7.2% ✓ | 12.2% ✓ |
| Pull% | 54.8% ✓ | 59.0% ✓ | 60.2% ✓ |
| Oppo% | 18.7% ✓ | 16.7% ✓ | 17.2% ✓ |
| Pulled Air% | 29.9% ✓ | 29.5% ✓ | 34.4% ✓ |
| Pitches | 1835 ✓ | 1876 ✓ | 1885 ✓ |
| IZ Swing% | 62.8% ✓ | 64.4% ✓ | 66.4% ✓ |
| Chase% | 22.0% ✓ | 21.7% ✓ | 26.5% ✓ |
| Whiff% | 33.2% ✓ | 32.8% ✓ | 34.8% ✓ |

### Fastball (pitch group)

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Pitches | 1548 ✓ | 1498 ✓ | 1424 ✓ |
| Share | 54.5% ✓ | 49.3% ✓ | 47.6% ✓ |
| IZ Swing% | 60.6% ✓ | 63.9% ✓ | 64.9% ✓ |
| Chase% | 18.8% ✓ | 21.0% ✓ | 24.7% ✓ |
| Whiff% | 25.2% ✓ | 24.7% ✓ | 24.6% ✓ |
| PA ending | 393 ✓ | 366 ✓ | 359 ✓ |
| wOBA | .396 ✓ | .477 ✓ | .428 ✓ |
| K% | 20.9% ✓ | 20.8% ✓ | 23.7% ✓ |
| BBE | 238 ✓ | 228 ✓ | 210 ✓ |
| EV90 | 109.2 ✓ | 110.9 ✓ | 108.8 ✓ |
| Hard-hit% | 57.1% ✓ | 64.5% ✓ | 56.2% ✓ |
| Barrel% | 14.7% ✓ | 25.4% ✓ | 14.3% ✓ |

### Breaking (pitch group)

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Pitches | 899 ✓ | 1123 ✓ | 1134 ✓ |
| Share | 31.6% ✓ | 37.0% ✓ | 37.9% ✓ |
| IZ Swing% | 59.7% ✓ | 60.4% ✓ | 65.5% ✓ |
| Chase% | 21.6% ✓ | 21.2% ✓ | 24.7% ✓ |
| Whiff% | 39.7% ✓ | 44.4% ✓ | 41.0% ✓ |
| PA ending | 206 ✓ | 238 ✓ | 240 ✓ |
| wOBA | .365 ✓ | .304 ✓ | .296 ✓ |
| K% | 38.3% ✓ | 37.8% ✓ | 38.8% ✓ |
| BBE | 100 ✓ | 117 ✓ | 116 ✓ |
| EV90 | 108.8 ✓ | 106.7 ✓ | 107.9 ✓ |
| Hard-hit% | 56.0% ✓ | 53.8% ✓ | 38.8% ✓ |
| Barrel% | 18.0% ✓ | 13.7% ✓ | 12.1% ✓ |

### Offspeed (pitch group)

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Pitches | 394 ✓ | 415 ✓ | 436 ✓ |
| Share | 13.9% ✓ | 13.7% ✓ | 14.6% ✓ |
| IZ Swing% | 65.1% ✓ | 74.5% ✓ | 74.0% ✓ |
| Chase% | 25.0% ✓ | 24.4% ✓ | 24.1% ✓ |
| Whiff% | 43.0% ✓ | 36.8% ✓ | 41.8% ✓ |
| PA ending | 88 ✓ | 109 ✓ | 96 ✓ |
| wOBA | .282 ✓ | .342 ✓ | .362 ✓ |
| K% | 39.8% ✓ | 26.6% ✓ | 43.8% ✓ |
| BBE | 44 ✓ | 62 ✓ | 40 ✓ |
| EV90 | 108.8 ✓ | 108.8 ✓ | 107.6 ✓ |
| Hard-hit% | 47.7% ✓ | 53.2% ✓ | 45.0% ✓ |
| Barrel% | 11.4% ✓ | 17.7% ✓ | 22.5% ✓ |

## 3. Compared with Baseball Savant and FanGraphs

His database rows against the public numbers. Tolerances are the league-wide validation's (`validation/validate.py`). The house-model stats (xwOBA, xBA, xSLG) differ by design. Pitch groups compare against Savant's pitch types rolled up into our three groups, which is approximate.

### 2024

| Metric | Ours | Theirs | Diff | Tolerance |  | Note |
|---|---|---|---|---|---|---|
| PA (Savant) | 692 | 692 | +0 | ±0 | ✓ | automatic IBBs missing from pbp (known) |
| AVG (Savant) | .248 | .248 | +0.0 pts | ±2 pts | ✓ |  |
| OBP (Savant) | .366 | .366 | +0.0 pts | ±2 pts | ✓ |  |
| SLG (Savant) | .485 | .485 | +0.0 pts | ±2 pts | ✓ |  |
| wOBA (Savant) | .371 | .366 | +5.0 pts | ±10 pts | ✓ | house weights vs Savant weights |
| xwOBA (Savant) | .387 | .380 | +7.0 pts | ±10 pts | ✓ | house model; guide says typical gap 3–7 pts |
| xBA (Savant) | .256 | .249 | +7.0 pts | ±10 pts | ✓ | house model |
| xSLG (Savant) | .519 | .519 | +0.0 pts | ±20 pts | ✓ | house model |
| K% (Savant) | 28.5% | 28.5% | -0.0 pts | ±0.3 pts | ✓ |  |
| BB% (Savant) | 15.3% | 15.3% | +0.0 pts | ±0.3 pts | ✓ |  |
| Avg EV (Savant) | 93.6 | 93.6 | +0.0 mph | ±0.3 mph | ✓ |  |
| Hard-hit% (Savant) | 55.5% | 55.5% | +0.0 pts | ±1.0 pts | ✓ |  |
| Barrel% (Savant) | 15.1% | 15.6% | -0.5 pts | ±1.0 pts | ✓ | guide says ~0.5 pts below Savant |
| Sweet spot% (Savant) | 32.0% | 31.8% | +0.2 pts | ±2.0 pts | ✓ | 8° and 32° count as half (integer launch angles) |
| IZ Swing% (Savant) | 60.7% | 60.7% | -0.0 pts | ±1.0 pts | ✓ |  |
| Chase% (Savant) | 20.9% | 21.0% | -0.1 pts | ±1.0 pts | ✓ | zone = ball touches zone, as Savant |
| Whiff% (Savant) | 32.0% | 32.0% | +0.0 pts | ±1.0 pts | ✓ |  |
| GB% (Savant) | 40.9% | 40.9% | +0.0 pts | ±1.0 pts | ✓ |  |
| FB% (Savant) | 28.6% | 28.6% | -0.0 pts | ±1.0 pts | ✓ |  |
| LD% (Savant) | 22.7% | 22.7% | +0.0 pts | ±1.0 pts | ✓ |  |
| PU% (Savant) | 7.8% | 7.8% | +0.0 pts | ±1.0 pts | ✓ |  |
| Pulled Air% (Savant Pull AIR%) (Savant) | 26.6% | 25.8% | +0.8 pts | ±1.0 pts | ✓ | spray from hit coordinates; avg within ~0.5 |
| Pull% (Savant) | 54.7% | 48.4% | +6.3 pts | ±6.0 pts | ✗ | known approximate (~4 pts high) |
| Oppo% (Savant) | 16.9% | 16.4% | +0.5 pts | ±6.0 pts | ✓ | known approximate |
| Sprint speed (Savant) | 25.80 | 25.80 | +0.0 ft/s | ±0.05 ft/s | ✓ | copied from Savant |
| Pitches seen (Savant) | 2852 | 2852 | +0 | ±5 | ✓ |  |
| EV90 (FanGraphs) | 109.2 | 109.2 | +0.0 mph | ±0.5 mph | ✓ | FanGraphs EV90 |
| wOBA (FanGraphs) (FanGraphs) | .371 | .366 | +5.2 pts | ±10 pts | ✓ | guide says ~.005 above FG for power hitters |
| fastball Pitches (Savant arsenal) | 1548 | 1538 | +10 | ±5 | ✗ |  |
| fastball PA ending (Savant arsenal) | 393 | 391 | +2 | ±2 | ✓ |  |
| fastball wOBA (Savant arsenal) | .396 | .398 | -1.6 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| fastball xwOBA (Savant arsenal) | .429 | .424 | +5.2 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| fastball K% (Savant arsenal) | 20.9% | 20.7% | +0.2 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| fastball Whiff% (Savant arsenal) | 25.2% | 25.1% | +0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| fastball Hard-hit% (Savant arsenal) | 57.1% | 57.8% | -0.7 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| breaking Pitches (Savant arsenal) | 899 | 899 | +0 | ±5 | ✓ |  |
| breaking PA ending (Savant arsenal) | 206 | 205 | +1 | ±2 | ✓ |  |
| breaking wOBA (Savant arsenal) | .365 | .372 | -7.5 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| breaking xwOBA (Savant arsenal) | .349 | .343 | +6.0 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| breaking K% (Savant arsenal) | 38.3% | 38.5% | -0.2 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| breaking Whiff% (Savant arsenal) | 39.7% | 39.7% | +0.0 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| breaking Hard-hit% (Savant arsenal) | 56.0% | 55.7% | +0.3 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| offspeed Pitches (Savant arsenal) | 394 | 392 | +2 | ±5 | ✓ |  |
| offspeed PA ending (Savant arsenal) | 88 | 88 | +0 | ±2 | ✓ |  |
| offspeed wOBA (Savant arsenal) | .282 | .273 | +8.7 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| offspeed xwOBA (Savant arsenal) | .298 | .297 | +1.4 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| offspeed K% (Savant arsenal) | 39.8% | 40.9% | -1.1 pts | ±1.0 pts | ✗ | PA-weighted roll-up |
| offspeed Whiff% (Savant arsenal) | 43.0% | 44.0% | -1.0 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| offspeed Hard-hit% (Savant arsenal) | 47.7% | 47.6% | +0.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |

### 2025

| Metric | Ours | Theirs | Diff | Tolerance |  | Note |
|---|---|---|---|---|---|---|
| PA (Savant) | 724 | 724 | +0 | ±0 | ✓ | automatic IBBs missing from pbp (known) |
| AVG (Savant) | .240 | .240 | +0.0 pts | ±2 pts | ✓ |  |
| OBP (Savant) | .365 | .365 | +0.0 pts | ±2 pts | ✓ |  |
| SLG (Savant) | .563 | .563 | +0.0 pts | ±2 pts | ✓ |  |
| wOBA (Savant) | .398 | .391 | +7.0 pts | ±10 pts | ✓ | house weights vs Savant weights |
| xwOBA (Savant) | .416 | .401 | +15.0 pts | ±10 pts | ✗ | house model; guide says typical gap 3–7 pts |
| xBA (Savant) | .257 | .249 | +8.0 pts | ±10 pts | ✓ | house model |
| xSLG (Savant) | .592 | .581 | +11.0 pts | ±20 pts | ✓ | house model |
| K% (Savant) | 27.2% | 27.2% | +0.0 pts | ±0.3 pts | ✓ |  |
| BB% (Savant) | 14.9% | 14.9% | +0.0 pts | ±0.3 pts | ✓ |  |
| Avg EV (Savant) | 94.3 | 94.3 | +0.0 mph | ±0.3 mph | ✓ |  |
| Hard-hit% (Savant) | 59.6% | 59.6% | +0.0 pts | ±1.0 pts | ✓ |  |
| Barrel% (Savant) | 20.8% | 20.8% | -0.0 pts | ±1.0 pts | ✓ | guide says ~0.5 pts below Savant |
| Sweet spot% (Savant) | 34.9% | 35.3% | -0.4 pts | ±2.0 pts | ✓ | 8° and 32° count as half (integer launch angles) |
| IZ Swing% (Savant) | 64.1% | 64.1% | +0.0 pts | ±1.0 pts | ✓ |  |
| Chase% (Savant) | 21.5% | 21.5% | +0.0 pts | ±1.0 pts | ✓ | zone = ball touches zone, as Savant |
| Whiff% (Savant) | 33.1% | 33.1% | +0.0 pts | ±1.0 pts | ✓ |  |
| GB% (Savant) | 34.3% | 34.3% | +0.0 pts | ±1.0 pts | ✓ |  |
| FB% (Savant) | 34.3% | 34.3% | +0.0 pts | ±1.0 pts | ✓ |  |
| LD% (Savant) | 22.5% | 22.5% | +0.0 pts | ±1.0 pts | ✓ |  |
| PU% (Savant) | 8.8% | 8.8% | -0.0 pts | ±1.0 pts | ✓ |  |
| Pulled Air% (Savant Pull AIR%) (Savant) | 31.1% | 31.1% | -0.0 pts | ±1.0 pts | ✓ | spray from hit coordinates; avg within ~0.5 |
| Pull% (Savant) | 58.1% | 54.7% | +3.4 pts | ±6.0 pts | ✓ | known approximate (~4 pts high) |
| Oppo% (Savant) | 17.2% | 17.2% | +0.0 pts | ±6.0 pts | ✓ | known approximate |
| Sprint speed (Savant) | 25.90 | 25.90 | +0.0 ft/s | ±0.05 ft/s | ✓ | copied from Savant |
| Pitches seen (Savant) | 3059 | 3059 | +0 | ±5 | ✓ |  |
| EV90 (FanGraphs) | 109.8 | 109.8 | +0.0 mph | ±0.5 mph | ✓ | FanGraphs EV90 |
| wOBA (FanGraphs) (FanGraphs) | .398 | .391 | +6.6 pts | ±10 pts | ✓ | guide says ~.005 above FG for power hitters |
| fastball Pitches (Savant arsenal) | 1498 | 1489 | +9 | ±5 | ✗ |  |
| fastball PA ending (Savant arsenal) | 366 | 362 | +4 | ±2 | ✗ |  |
| fastball wOBA (Savant arsenal) | .477 | .471 | +5.6 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| fastball xwOBA (Savant arsenal) | .489 | .475 | +13.5 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| fastball K% (Savant arsenal) | 20.8% | 20.5% | +0.3 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| fastball Whiff% (Savant arsenal) | 24.7% | 24.6% | +0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| fastball Hard-hit% (Savant arsenal) | 64.5% | 64.7% | -0.2 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| breaking Pitches (Savant arsenal) | 1123 | 1125 | -2 | ±5 | ✓ |  |
| breaking PA ending (Savant arsenal) | 238 | 240 | -2 | ±2 | ✓ |  |
| breaking wOBA (Savant arsenal) | .304 | .303 | +0.9 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| breaking xwOBA (Savant arsenal) | .309 | .304 | +4.5 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| breaking K% (Savant arsenal) | 37.8% | 37.9% | -0.1 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| breaking Whiff% (Savant arsenal) | 44.4% | 44.4% | -0.0 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| breaking Hard-hit% (Savant arsenal) | 53.8% | 53.9% | -0.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| offspeed Pitches (Savant arsenal) | 415 | 415 | +0 | ±5 | ✓ |  |
| offspeed PA ending (Savant arsenal) | 109 | 108 | +1 | ±2 | ✓ |  |
| offspeed wOBA (Savant arsenal) | .342 | .334 | +7.6 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| offspeed xwOBA (Savant arsenal) | .407 | .382 | +25.5 pts | ±20 pts | ✗ | house model; PA-weighted roll-up |
| offspeed K% (Savant arsenal) | 26.6% | 26.9% | -0.3 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| offspeed Whiff% (Savant arsenal) | 36.8% | 36.7% | +0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| offspeed Hard-hit% (Savant arsenal) | 53.2% | 53.3% | -0.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |

### 2026

| Metric | Ours | Theirs | Diff | Tolerance |  | Note |
|---|---|---|---|---|---|---|
| PA (Savant) | 701 | 701 | +0 | ±0 | ✓ | automatic IBBs missing from pbp (known) |
| AVG (Savant) | .232 | .232 | +0.0 pts | ±2 pts | ✓ |  |
| OBP (Savant) | .354 | .354 | +0.0 pts | ±2 pts | ✓ |  |
| SLG (Savant) | .503 | .503 | +0.0 pts | ±2 pts | ✓ |  |
| wOBA (Savant) | .373 | .368 | +5.0 pts | ±10 pts | ✓ | house weights vs Savant weights |
| xwOBA (Savant) | .375 | .364 | +11.0 pts | ±10 pts | ✗ | house model; guide says typical gap 3–7 pts |
| xBA (Savant) | .238 | .236 | +2.0 pts | ±10 pts | ✓ | house model |
| xSLG (Savant) | .499 | .487 | +12.0 pts | ±20 pts | ✓ | house model |
| K% (Savant) | 31.4% | 31.4% | +0.0 pts | ±0.3 pts | ✓ |  |
| BB% (Savant) | 15.0% | 15.0% | +0.0 pts | ±0.3 pts | ✓ |  |
| Avg EV (Savant) | 92.3 | 92.3 | +0.0 mph | ±0.3 mph | ✓ |  |
| Hard-hit% (Savant) | 49.5% | 49.3% | +0.2 pts | ±1.0 pts | ✓ |  |
| Barrel% (Savant) | 14.5% | 15.6% | -1.1 pts | ±1.0 pts | ✗ | guide says ~0.5 pts below Savant |
| Sweet spot% (Savant) | 37.4% | 37.3% | +0.1 pts | ±2.0 pts | ✓ | 8° and 32° count as half (integer launch angles) |
| IZ Swing% (Savant) | 66.1% | 66.4% | -0.3 pts | ±1.0 pts | ✓ |  |
| Chase% (Savant) | 24.6% | 26.1% | -1.5 pts | ±1.0 pts | ✗ | zone = ball touches zone, as Savant |
| Whiff% (Savant) | 33.1% | 33.1% | +0.0 pts | ±1.0 pts | ✓ |  |
| GB% (Savant) | 31.3% | 31.3% | +0.0 pts | ±1.0 pts | ✓ |  |
| FB% (Savant) | 31.9% | 31.9% | +0.0 pts | ±1.0 pts | ✓ |  |
| LD% (Savant) | 26.4% | 26.4% | +0.0 pts | ±1.0 pts | ✓ |  |
| PU% (Savant) | 10.4% | 10.4% | -0.0 pts | ±1.0 pts | ✓ |  |
| Pulled Air% (Savant Pull AIR%) (Savant) | 32.2% | 32.2% | +0.0 pts | ±1.0 pts | ✓ | spray from hit coordinates; avg within ~0.5 |
| Pull% (Savant) | 59.6% | 54.2% | +5.4 pts | ±6.0 pts | ✓ | known approximate (~4 pts high) |
| Oppo% (Savant) | 16.9% | 16.9% | +0.0 pts | ±6.0 pts | ✓ | known approximate |
| Sprint speed (Savant) | 25.60 | 25.60 | +0.0 ft/s | ±0.05 ft/s | ✓ | copied from Savant |
| Pitches seen (Savant) | 2998 | 2998 | +0 | ±5 | ✓ |  |
| EV90 (FanGraphs) | 108.6 | 108.6 | +0.0 mph | ±0.5 mph | ✓ | FanGraphs EV90 |
| wOBA (FanGraphs) (FanGraphs) | .373 | .368 | +5.0 pts | ±10 pts | ✓ | guide says ~.005 above FG for power hitters |
| fastball Pitches (Savant arsenal) | 1424 | 1421 | +3 | ±5 | ✓ |  |
| fastball PA ending (Savant arsenal) | 359 | 359 | +0 | ±2 | ✓ |  |
| fastball wOBA (Savant arsenal) | .428 | .424 | +4.4 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| fastball xwOBA (Savant arsenal) | .424 | .417 | +6.9 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| fastball K% (Savant arsenal) | 23.7% | 23.7% | +0.0 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| fastball Whiff% (Savant arsenal) | 24.6% | 24.4% | +0.2 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| fastball Hard-hit% (Savant arsenal) | 56.2% | 55.7% | +0.5 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| breaking Pitches (Savant arsenal) | 1134 | 1136 | -2 | ±5 | ✓ |  |
| breaking PA ending (Savant arsenal) | 240 | 238 | +2 | ±2 | ✓ |  |
| breaking wOBA (Savant arsenal) | .296 | .293 | +2.5 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| breaking xwOBA (Savant arsenal) | .321 | .311 | +9.8 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| breaking K% (Savant arsenal) | 38.8% | 39.1% | -0.3 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| breaking Whiff% (Savant arsenal) | 41.0% | 40.9% | +0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| breaking Hard-hit% (Savant arsenal) | 38.8% | 38.7% | +0.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| offspeed Pitches (Savant arsenal) | 436 | 437 | -1 | ±5 | ✓ |  |
| offspeed PA ending (Savant arsenal) | 96 | 97 | -1 | ±2 | ✓ |  |
| offspeed wOBA (Savant arsenal) | .362 | .348 | +14.2 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| offspeed xwOBA (Savant arsenal) | .333 | .311 | +22.3 pts | ±20 pts | ✗ | house model; PA-weighted roll-up |
| offspeed K% (Savant arsenal) | 43.8% | 43.3% | +0.5 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| offspeed Whiff% (Savant arsenal) | 41.8% | 41.7% | +0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| offspeed Hard-hit% (Savant arsenal) | 45.0% | 46.9% | -1.9 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |

