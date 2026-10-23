# Packet audit: Steven Kwan

Run 2026-10-23 on the data packet `data.py` builds today (860 numbers in its tables and notes). Seasons in the packet: 2024, 2025, 2026.

Three checks, each done without `data.py`'s own code:

1. **Packet math.** Every table cell rebuilt from the database rows: the computed numbers (xISO, IZ Swing − Chase, gaps), season-over-season changes, trend wording, league averages, ranks and percentiles (ranked in SQL), platoon usage and the pitch-group tables. Must match exactly.
2. **Rows rebuilt from pitches.** His season, split and pitch-group rows recomputed from the raw pitch-by-pitch table, so the nightly pipeline is checked too. Must match to the digit shown. The house expected stats (xwOBA, xBA, xSLG) come from a model and can't be rebuilt this way.
3. **Public sources.** His rows against Baseball Savant and FanGraphs (downloaded 2026-10-18), within the tolerances of the league-wide validation.

## Summary

| Check | Numbers checked | Match | Differ | Not checked |
|---|---|---|---|---|
| 1. Packet math | 857 | 857 | 0 | 3 |
| 2. Rows rebuilt from pitches | 450 | 450 | 0 | — |
| 3. Savant / FanGraphs | 147 | 141 | 6 | 0 |

## Everything that differs

**Outside tolerance vs Savant / FanGraphs**

| Season | Metric | Ours | Theirs | Diff | Tolerance | Note |
|---|---|---|---|---|---|---|
| 2024 | offspeed wOBA (Savant arsenal) | .207 | .235 | -27.7 pts | ±15 pts | Savant rolled up PA-weighted (approximate) |
| 2025 | Pulled Air% (Savant Pull AIR%) (Savant) | 16.5% | 15.0% | +1.5 pts | ±1.0 pts | spray from hit coordinates; avg within ~0.5 |
| 2025 | Pull% (Savant) | 36.2% | 29.7% | +6.5 pts | ±6.0 pts | known approximate (~4 pts high) |
| 2025 | fastball Pitches (Savant arsenal) | 1703 | 1695 | +8 | ±5 |  |
| 2025 | offspeed Pitches (Savant arsenal) | 387 | 394 | -7 | ±5 |  |
| 2026 | fastball wOBA (Savant arsenal) | .367 | .385 | -18.2 pts | ±15 pts | Savant rolled up PA-weighted (approximate) |

## 1. Packet math

Each table in the packet, cell by cell. A table with nothing listed under it matched in full.

- **Seasons (full season, last three seasons) › Core (foundational metrics)**: 27 of 30 match; not checked: Team
- **Seasons (full season, last three seasons) › Results vs. expected**: 33 of 33 match
- **Seasons (full season, last three seasons) › Contact quality and batted-ball shape**: 45 of 45 match
- **Seasons (full season, last three seasons) › Plate discipline**: 24 of 24 match
- **Season-over-season changes**: 57 of 57 match
- **2026 league context**: 96 of 96 match
- **League context by season**: 216 of 216 match
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
| PA | 540 ✓ | 693 ✓ | 637 ✓ |
| AB | 480 ✓ | 625 ✓ | 539 ✓ |
| H | 140 ✓ | 170 ✓ | 151 ✓ |
| 2B | 16 ✓ | 29 ✓ | 21 ✓ |
| 3B | 3 ✓ | 1 ✓ | 3 ✓ |
| HR | 14 ✓ | 11 ✓ | 3 ✓ |
| BB | 53 ✓ | 55 ✓ | 85 ✓ |
| IBB | 0 ✓ | 2 ✓ | 1 ✓ |
| HBP | 5 ✓ | 3 ✓ | 4 ✓ |
| SO | 51 ✓ | 60 ✓ | 62 ✓ |
| SF | 0 ✓ | 7 ✓ | 3 ✓ |
| AVG | .292 ✓ | .272 ✓ | .280 ✓ |
| OBP | .368 ✓ | .330 ✓ | .380 ✓ |
| SLG | .425 ✓ | .374 ✓ | .347 ✓ |
| ISO | .133 ✓ | .102 ✓ | .067 ✓ |
| BABIP | .304 ✓ | .283 ✓ | .310 ✓ |
| wOBA | .350 ✓ | .310 ✓ | .331 ✓ |
| K% | 9.4% ✓ | 8.7% ✓ | 9.7% ✓ |
| BB% | 9.8% ✓ | 7.9% ✓ | 13.3% ✓ |
| BBE | 431 ✓ | 575 ✓ | 482 ✓ |
| Avg EV | 86.3 ✓ | 86.2 ✓ | 83.8 ✓ |
| EV90 | 99.1 ✓ | 98.2 ✓ | 95.3 ✓ |
| LA median | 16.0 ✓ | 16.0 ✓ | 14.0 ✓ |
| LA SD | 26.9 ✓ | 24.7 ✓ | 24.3 ✓ |
| Hard-hit% | 23.7% ✓ | 19.3% ✓ | 10.4% ✓ |
| Barrel% | 2.6% ✓ | 1.9% ✓ | 0.4% ✓ |
| Sweet spot% | 39.0% ✓ | 39.7% ✓ | 41.4% ✓ |
| GB% | 37.4% ✓ | 39.1% ✓ | 41.9% ✓ |
| LD% | 27.8% ✓ | 29.0% ✓ | 30.9% ✓ |
| FB% | 28.3% ✓ | 26.1% ✓ | 22.3% ✓ |
| PU% | 6.5% ✓ | 5.7% ✓ | 4.9% ✓ |
| Pull% | 36.4% ✓ | 36.2% ✓ | 32.6% ✓ |
| Oppo% | 33.2% ✓ | 31.8% ✓ | 34.9% ✓ |
| Pulled Air% | 17.2% ✓ | 16.5% ✓ | 12.9% ✓ |
| Pitches | 2165 ✓ | 2786 ✓ | 2618 ✓ |
| IZ Swing% | 57.7% ✓ | 58.8% ✓ | 51.5% ✓ |
| Chase% | 19.2% ✓ | 22.7% ✓ | 18.9% ✓ |
| Whiff% | 8.2% ✓ | 8.7% ✓ | 8.2% ✓ |

### vs LHP

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| PA | 159 ✓ | 224 ✓ | 205 ✓ |
| AB | 141 ✓ | 203 ✓ | 170 ✓ |
| H | 45 ✓ | 50 ✓ | 39 ✓ |
| 2B | 3 ✓ | 7 ✓ | 5 ✓ |
| 3B | 0 ✓ | 0 ✓ | 0 ✓ |
| HR | 5 ✓ | 0 ✓ | 0 ✓ |
| BB | 16 ✓ | 15 ✓ | 30 ✓ |
| IBB | 0 ✓ | 1 ✓ | 1 ✓ |
| HBP | 1 ✓ | 2 ✓ | 2 ✓ |
| SO | 19 ✓ | 20 ✓ | 26 ✓ |
| SF | 0 ✓ | 3 ✓ | 1 ✓ |
| AVG | .319 ✓ | .246 ✓ | .229 ✓ |
| OBP | .392 ✓ | .300 ✓ | .350 ✓ |
| SLG | .447 ✓ | .281 ✓ | .259 ✓ |
| ISO | .128 ✓ | .034 ✓ | .029 ✓ |
| BABIP | .342 ✓ | .269 ✓ | .269 ✓ |
| wOBA | .369 ✓ | .259 ✓ | .286 ✓ |
| K% | 11.9% ✓ | 8.9% ✓ | 12.7% ✓ |
| BB% | 10.1% ✓ | 6.7% ✓ | 14.6% ✓ |
| BBE | 123 ✓ | 187 ✓ | 146 ✓ |
| Avg EV | 86.4 ✓ | 84.2 ✓ | 83.5 ✓ |
| EV90 | 99.8 ✓ | 97.2 ✓ | 94.8 ✓ |
| LA median | 16.5 ✓ | 14.0 ✓ | 14.5 ✓ |
| LA SD | 23.6 ✓ | 26.6 ✓ | 24.7 ✓ |
| Hard-hit% | 25.2% ✓ | 15.0% ✓ | 9.6% ✓ |
| Barrel% | 3.3% ✓ | 0.0% ✓ | 0.0% ✓ |
| Sweet spot% | 41.9% ✓ | 34.2% ✓ | 38.0% ✓ |
| GB% | 39.0% ✓ | 43.9% ✓ | 43.5% ✓ |
| LD% | 29.3% ✓ | 27.8% ✓ | 27.9% ✓ |
| FB% | 22.8% ✓ | 21.4% ✓ | 21.1% ✓ |
| PU% | 8.9% ✓ | 7.0% ✓ | 7.5% ✓ |
| Pull% | 35.8% ✓ | 35.3% ✓ | 32.2% ✓ |
| Oppo% | 33.3% ✓ | 34.2% ✓ | 26.7% ✓ |
| Pulled Air% | 14.6% ✓ | 13.4% ✓ | 11.0% ✓ |
| Pitches | 635 ✓ | 845 ✓ | 845 ✓ |
| IZ Swing% | 56.8% ✓ | 59.9% ✓ | 52.1% ✓ |
| Chase% | 17.9% ✓ | 22.1% ✓ | 18.7% ✓ |
| Whiff% | 11.1% ✓ | 8.0% ✓ | 11.3% ✓ |

### vs RHP

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| PA | 381 ✓ | 469 ✓ | 432 ✓ |
| AB | 339 ✓ | 422 ✓ | 369 ✓ |
| H | 95 ✓ | 120 ✓ | 112 ✓ |
| 2B | 13 ✓ | 22 ✓ | 16 ✓ |
| 3B | 3 ✓ | 1 ✓ | 3 ✓ |
| HR | 9 ✓ | 11 ✓ | 3 ✓ |
| BB | 37 ✓ | 40 ✓ | 55 ✓ |
| IBB | 0 ✓ | 1 ✓ | 0 ✓ |
| HBP | 4 ✓ | 1 ✓ | 2 ✓ |
| SO | 32 ✓ | 40 ✓ | 36 ✓ |
| SF | 0 ✓ | 4 ✓ | 2 ✓ |
| AVG | .280 ✓ | .284 ✓ | .304 ✓ |
| OBP | .358 ✓ | .345 ✓ | .395 ✓ |
| SLG | .416 ✓ | .419 ✓ | .388 ✓ |
| ISO | .136 ✓ | .135 ✓ | .084 ✓ |
| BABIP | .289 ✓ | .291 ✓ | .328 ✓ |
| wOBA | .342 ✓ | .334 ✓ | .352 ✓ |
| K% | 8.4% ✓ | 8.5% ✓ | 8.3% ✓ |
| BB% | 9.7% ✓ | 8.5% ✓ | 12.7% ✓ |
| BBE | 308 ✓ | 388 ✓ | 336 ✓ |
| Avg EV | 86.2 ✓ | 87.1 ✓ | 84.0 ✓ |
| EV90 | 98.8 ✓ | 98.6 ✓ | 95.7 ✓ |
| LA median | 16.0 ✓ | 18.0 ✓ | 14.0 ✓ |
| LA SD | 28.1 ✓ | 23.8 ✓ | 24.1 ✓ |
| Hard-hit% | 23.1% ✓ | 21.4% ✓ | 10.7% ✓ |
| Barrel% | 2.3% ✓ | 2.8% ✓ | 0.6% ✓ |
| Sweet spot% | 37.8% ✓ | 42.4% ✓ | 42.9% ✓ |
| GB% | 36.7% ✓ | 36.9% ✓ | 41.1% ✓ |
| LD% | 27.3% ✓ | 29.6% ✓ | 32.2% ✓ |
| FB% | 30.5% ✓ | 28.4% ✓ | 22.8% ✓ |
| PU% | 5.5% ✓ | 5.2% ✓ | 3.8% ✓ |
| Pull% | 36.7% ✓ | 36.6% ✓ | 32.7% ✓ |
| Oppo% | 33.1% ✓ | 30.7% ✓ | 38.4% ✓ |
| Pulled Air% | 18.2% ✓ | 18.0% ✓ | 13.7% ✓ |
| Pitches | 1530 ✓ | 1941 ✓ | 1773 ✓ |
| IZ Swing% | 58.1% ✓ | 58.3% ✓ | 51.2% ✓ |
| Chase% | 19.7% ✓ | 23.0% ✓ | 19.0% ✓ |
| Whiff% | 7.0% ✓ | 9.1% ✓ | 6.8% ✓ |

### Fastball (pitch group)

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Pitches | 1323 ✓ | 1703 ✓ | 1772 ✓ |
| Share | 61.3% ✓ | 61.1% ✓ | 67.9% ✓ |
| IZ Swing% | 57.1% ✓ | 57.9% ✓ | 47.8% ✓ |
| Chase% | 15.9% ✓ | 21.3% ✓ | 17.1% ✓ |
| Whiff% | 4.6% ✓ | 5.5% ✓ | 5.5% ✓ |
| PA ending | 327 ✓ | 442 ✓ | 407 ✓ |
| wOBA | .405 ✓ | .325 ✓ | .367 ✓ |
| K% | 6.4% ✓ | 5.7% ✓ | 6.9% ✓ |
| BBE | 263 ✓ | 369 ✓ | 305 ✓ |
| EV90 | 99.6 ✓ | 97.3 ✓ | 94.9 ✓ |
| Hard-hit% | 26.6% ✓ | 15.7% ✓ | 9.5% ✓ |
| Barrel% | 1.9% ✓ | 1.1% ✓ | 0.3% ✓ |

### Breaking (pitch group)

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Pitches | 531 ✓ | 696 ✓ | 572 ✓ |
| Share | 24.6% ✓ | 25.0% ✓ | 21.9% ✓ |
| IZ Swing% | 54.5% ✓ | 55.8% ✓ | 56.9% ✓ |
| Chase% | 21.3% ✓ | 22.4% ✓ | 20.2% ✓ |
| Whiff% | 16.3% ✓ | 13.5% ✓ | 14.2% ✓ |
| PA ending | 123 ✓ | 154 ✓ | 148 ✓ |
| wOBA | .310 ✓ | .300 ✓ | .287 ✓ |
| K% | 16.3% ✓ | 14.9% ✓ | 18.2% ✓ |
| BBE | 92 ✓ | 126 ✓ | 109 ✓ |
| EV90 | 99.3 ✓ | 99.1 ✓ | 96.1 ✓ |
| Hard-hit% | 21.7% ✓ | 28.6% ✓ | 13.8% ✓ |
| Barrel% | 5.4% ✓ | 3.2% ✓ | 0.9% ✓ |

### Offspeed (pitch group)

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Pitches | 304 ✓ | 387 ✓ | 267 ✓ |
| Share | 14.1% ✓ | 13.9% ✓ | 10.2% ✓ |
| IZ Swing% | 68.3% ✓ | 71.7% ✓ | 71.2% ✓ |
| Chase% | 25.3% ✓ | 27.2% ✓ | 25.6% ✓ |
| Whiff% | 9.9% ✓ | 14.5% ✓ | 11.8% ✓ |
| PA ending | 88 ✓ | 95 ✓ | 78 ✓ |
| wOBA | .207 ✓ | .253 ✓ | .231 ✓ |
| K% | 10.2% ✓ | 12.6% ✓ | 9.0% ✓ |
| BBE | 75 ✓ | 80 ✓ | 67 ✓ |
| EV90 | 96.4 ✓ | 98.2 ✓ | 92.8 ✓ |
| Hard-hit% | 16.0% ✓ | 21.3% ✓ | 7.5% ✓ |
| Barrel% | 1.3% ✓ | 3.8% ✓ | 0.0% ✓ |

## 3. Compared with Baseball Savant and FanGraphs

His database rows against the public numbers. Tolerances are the league-wide validation's (`validation/validate.py`). The house-model stats (xwOBA, xBA, xSLG) differ by design. Pitch groups compare against Savant's pitch types rolled up into our three groups, which is approximate.

### 2024

| Metric | Ours | Theirs | Diff | Tolerance |  | Note |
|---|---|---|---|---|---|---|
| PA (Savant) | 540 | 540 | +0 | ±0 | ✓ | automatic IBBs missing from pbp (known) |
| AVG (Savant) | .292 | .292 | +0.0 pts | ±2 pts | ✓ |  |
| OBP (Savant) | .368 | .368 | +0.0 pts | ±2 pts | ✓ |  |
| SLG (Savant) | .425 | .425 | +0.0 pts | ±2 pts | ✓ |  |
| wOBA (Savant) | .350 | .349 | +1.0 pts | ±10 pts | ✓ | house weights vs Savant weights |
| xwOBA (Savant) | .328 | .337 | -9.0 pts | ±10 pts | ✓ | house model; guide says typical gap 3–7 pts |
| xBA (Savant) | .278 | .283 | -5.0 pts | ±10 pts | ✓ | house model |
| xSLG (Savant) | .384 | .392 | -8.0 pts | ±20 pts | ✓ | house model |
| K% (Savant) | 9.4% | 9.4% | +0.0 pts | ±0.3 pts | ✓ |  |
| BB% (Savant) | 9.8% | 9.8% | +0.0 pts | ±0.3 pts | ✓ |  |
| Avg EV (Savant) | 86.3 | 86.3 | +0.0 mph | ±0.3 mph | ✓ |  |
| Hard-hit% (Savant) | 23.7% | 23.7% | +0.0 pts | ±1.0 pts | ✓ |  |
| Barrel% (Savant) | 2.6% | 2.6% | -0.0 pts | ±1.0 pts | ✓ | guide says ~0.5 pts below Savant |
| Sweet spot% (Savant) | 39.0% | 38.5% | +0.5 pts | ±2.0 pts | ✓ | 8° and 32° count as half (integer launch angles) |
| IZ Swing% (Savant) | 57.7% | 57.8% | -0.1 pts | ±1.0 pts | ✓ |  |
| Chase% (Savant) | 19.2% | 19.1% | +0.1 pts | ±1.0 pts | ✓ | zone = ball touches zone, as Savant |
| Whiff% (Savant) | 8.2% | 8.2% | +0.0 pts | ±1.0 pts | ✓ |  |
| GB% (Savant) | 37.4% | 37.4% | +0.0 pts | ±1.0 pts | ✓ |  |
| FB% (Savant) | 28.3% | 28.3% | -0.0 pts | ±1.0 pts | ✓ |  |
| LD% (Savant) | 27.8% | 27.8% | +0.0 pts | ±1.0 pts | ✓ |  |
| PU% (Savant) | 6.5% | 6.5% | +0.0 pts | ±1.0 pts | ✓ |  |
| Pulled Air% (Savant Pull AIR%) (Savant) | 17.2% | 16.7% | +0.5 pts | ±1.0 pts | ✓ | spray from hit coordinates; avg within ~0.5 |
| Pull% (Savant) | 36.4% | 30.4% | +6.0 pts | ±6.0 pts | ✓ | known approximate (~4 pts high) |
| Oppo% (Savant) | 33.2% | 32.0% | +1.2 pts | ±6.0 pts | ✓ | known approximate |
| Sprint speed (Savant) | 27.10 | 27.10 | +0.0 ft/s | ±0.05 ft/s | ✓ | copied from Savant |
| Pitches seen (Savant) | 2165 | 2165 | +0 | ±5 | ✓ |  |
| EV90 (FanGraphs) | 99.1 | 99.0 | +0.1 mph | ±0.5 mph | ✓ | FanGraphs EV90 |
| wOBA (FanGraphs) (FanGraphs) | .350 | .349 | +0.6 pts | ±10 pts | ✓ | guide says ~.005 above FG for power hitters |
| fastball Pitches (Savant arsenal) | 1323 | 1322 | +1 | ±5 | ✓ |  |
| fastball PA ending (Savant arsenal) | 327 | 327 | +0 | ±2 | ✓ |  |
| fastball wOBA (Savant arsenal) | .405 | .409 | -3.6 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| fastball xwOBA (Savant arsenal) | .357 | .366 | -9.0 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| fastball K% (Savant arsenal) | 6.4% | 6.4% | -0.0 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| fastball Whiff% (Savant arsenal) | 4.6% | 4.6% | -0.0 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| fastball Hard-hit% (Savant arsenal) | 26.6% | 26.7% | -0.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| breaking Pitches (Savant arsenal) | 531 | 532 | -1 | ±5 | ✓ |  |
| breaking PA ending (Savant arsenal) | 123 | 123 | +0 | ±2 | ✓ |  |
| breaking wOBA (Savant arsenal) | .310 | .311 | -1.1 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| breaking xwOBA (Savant arsenal) | .315 | .320 | -5.3 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| breaking K% (Savant arsenal) | 16.3% | 16.3% | +0.0 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| breaking Whiff% (Savant arsenal) | 16.3% | 16.4% | -0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| breaking Hard-hit% (Savant arsenal) | 21.7% | 20.7% | +1.0 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| offspeed Pitches (Savant arsenal) | 304 | 303 | +1 | ±5 | ✓ |  |
| offspeed PA ending (Savant arsenal) | 88 | 87 | +1 | ±2 | ✓ |  |
| offspeed wOBA (Savant arsenal) | .207 | .235 | -27.7 pts | ±15 pts | ✗ | Savant rolled up PA-weighted (approximate) |
| offspeed xwOBA (Savant arsenal) | .248 | .261 | -12.9 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| offspeed K% (Savant arsenal) | 10.2% | 10.3% | -0.1 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| offspeed Whiff% (Savant arsenal) | 9.9% | 10.2% | -0.3 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| offspeed Hard-hit% (Savant arsenal) | 16.0% | 14.9% | +1.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |

### 2025

| Metric | Ours | Theirs | Diff | Tolerance |  | Note |
|---|---|---|---|---|---|---|
| PA (Savant) | 693 | 693 | +0 | ±0 | ✓ | automatic IBBs missing from pbp (known) |
| AVG (Savant) | .272 | .272 | +0.0 pts | ±2 pts | ✓ |  |
| OBP (Savant) | .330 | .330 | +0.0 pts | ±2 pts | ✓ |  |
| SLG (Savant) | .374 | .374 | +0.0 pts | ±2 pts | ✓ |  |
| wOBA (Savant) | .310 | .310 | +0.0 pts | ±10 pts | ✓ | house weights vs Savant weights |
| xwOBA (Savant) | .305 | .310 | -5.0 pts | ±10 pts | ✓ | house model; guide says typical gap 3–7 pts |
| xBA (Savant) | .269 | .273 | -4.0 pts | ±10 pts | ✓ | house model |
| xSLG (Savant) | .361 | .366 | -5.0 pts | ±20 pts | ✓ | house model |
| K% (Savant) | 8.7% | 8.7% | +0.0 pts | ±0.3 pts | ✓ |  |
| BB% (Savant) | 7.9% | 7.9% | +0.0 pts | ±0.3 pts | ✓ |  |
| Avg EV (Savant) | 86.2 | 86.2 | +0.0 mph | ±0.3 mph | ✓ |  |
| Hard-hit% (Savant) | 19.3% | 19.3% | +0.0 pts | ±1.0 pts | ✓ |  |
| Barrel% (Savant) | 1.9% | 1.9% | +0.0 pts | ±1.0 pts | ✓ | guide says ~0.5 pts below Savant |
| Sweet spot% (Savant) | 39.7% | 39.7% | +0.0 pts | ±2.0 pts | ✓ | 8° and 32° count as half (integer launch angles) |
| IZ Swing% (Savant) | 58.8% | 58.8% | +0.0 pts | ±1.0 pts | ✓ |  |
| Chase% (Savant) | 22.7% | 22.7% | +0.0 pts | ±1.0 pts | ✓ | zone = ball touches zone, as Savant |
| Whiff% (Savant) | 8.7% | 8.7% | +0.0 pts | ±1.0 pts | ✓ |  |
| GB% (Savant) | 39.1% | 39.1% | +0.0 pts | ±1.0 pts | ✓ |  |
| FB% (Savant) | 26.1% | 26.1% | +0.0 pts | ±1.0 pts | ✓ |  |
| LD% (Savant) | 29.0% | 29.0% | +0.0 pts | ±1.0 pts | ✓ |  |
| PU% (Savant) | 5.7% | 5.7% | +0.0 pts | ±1.0 pts | ✓ |  |
| Pulled Air% (Savant Pull AIR%) (Savant) | 16.5% | 15.0% | +1.5 pts | ±1.0 pts | ✗ | spray from hit coordinates; avg within ~0.5 |
| Pull% (Savant) | 36.2% | 29.7% | +6.5 pts | ±6.0 pts | ✗ | known approximate (~4 pts high) |
| Oppo% (Savant) | 31.8% | 31.5% | +0.3 pts | ±6.0 pts | ✓ | known approximate |
| Sprint speed (Savant) | 27.30 | 27.30 | +0.0 ft/s | ±0.05 ft/s | ✓ | copied from Savant |
| Pitches seen (Savant) | 2786 | 2786 | +0 | ±5 | ✓ |  |
| EV90 (FanGraphs) | 98.2 | 98.1 | +0.1 mph | ±0.5 mph | ✓ | FanGraphs EV90 |
| wOBA (FanGraphs) (FanGraphs) | .310 | .309 | +0.5 pts | ±10 pts | ✓ | guide says ~.005 above FG for power hitters |
| fastball Pitches (Savant arsenal) | 1703 | 1695 | +8 | ±5 | ✗ |  |
| fastball PA ending (Savant arsenal) | 442 | 442 | +0 | ±2 | ✓ |  |
| fastball wOBA (Savant arsenal) | .325 | .330 | -4.9 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| fastball xwOBA (Savant arsenal) | .312 | .314 | -2.3 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| fastball K% (Savant arsenal) | 5.7% | 5.6% | +0.1 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| fastball Whiff% (Savant arsenal) | 5.5% | 5.5% | -0.0 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| fastball Hard-hit% (Savant arsenal) | 15.7% | 15.8% | -0.1 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| breaking Pitches (Savant arsenal) | 696 | 697 | -1 | ±5 | ✓ |  |
| breaking PA ending (Savant arsenal) | 154 | 154 | +0 | ±2 | ✓ |  |
| breaking wOBA (Savant arsenal) | .300 | .310 | -10.1 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| breaking xwOBA (Savant arsenal) | .296 | .312 | -15.7 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| breaking K% (Savant arsenal) | 14.9% | 14.9% | -0.0 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| breaking Whiff% (Savant arsenal) | 13.5% | 13.1% | +0.4 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| breaking Hard-hit% (Savant arsenal) | 28.6% | 28.2% | +0.4 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| offspeed Pitches (Savant arsenal) | 387 | 394 | -7 | ±5 | ✗ |  |
| offspeed PA ending (Savant arsenal) | 95 | 95 | +0 | ±2 | ✓ |  |
| offspeed wOBA (Savant arsenal) | .253 | .255 | -2.3 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| offspeed xwOBA (Savant arsenal) | .288 | .291 | -2.6 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| offspeed K% (Savant arsenal) | 12.6% | 12.6% | -0.0 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| offspeed Whiff% (Savant arsenal) | 14.5% | 14.5% | +0.0 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| offspeed Hard-hit% (Savant arsenal) | 21.3% | 21.3% | +0.0 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |

### 2026

| Metric | Ours | Theirs | Diff | Tolerance |  | Note |
|---|---|---|---|---|---|---|
| PA (Savant) | 637 | 637 | +0 | ±0 | ✓ | automatic IBBs missing from pbp (known) |
| AVG (Savant) | .280 | .282 | -2.0 pts | ±2 pts | ✓ |  |
| OBP (Savant) | .380 | .382 | -2.0 pts | ±2 pts | ✓ |  |
| SLG (Savant) | .347 | .349 | -2.0 pts | ±2 pts | ✓ |  |
| wOBA (Savant) | .331 | .334 | -3.0 pts | ±10 pts | ✓ | house weights vs Savant weights |
| xwOBA (Savant) | .332 | .328 | +4.0 pts | ±10 pts | ✓ | house model; guide says typical gap 3–7 pts |
| xBA (Savant) | .280 | .277 | +3.0 pts | ±10 pts | ✓ | house model |
| xSLG (Savant) | .347 | .343 | +4.0 pts | ±20 pts | ✓ | house model |
| K% (Savant) | 9.7% | 9.7% | +0.0 pts | ±0.3 pts | ✓ |  |
| BB% (Savant) | 13.3% | 13.3% | +0.0 pts | ±0.3 pts | ✓ |  |
| Avg EV (Savant) | 83.8 | 83.9 | -0.1 mph | ±0.3 mph | ✓ |  |
| Hard-hit% (Savant) | 10.4% | 10.5% | -0.1 pts | ±1.0 pts | ✓ |  |
| Barrel% (Savant) | 0.4% | 0.4% | +0.0 pts | ±1.0 pts | ✓ | guide says ~0.5 pts below Savant |
| Sweet spot% (Savant) | 41.4% | 40.6% | +0.8 pts | ±2.0 pts | ✓ | 8° and 32° count as half (integer launch angles) |
| IZ Swing% (Savant) | 51.5% | 51.2% | +0.3 pts | ±1.0 pts | ✓ |  |
| Chase% (Savant) | 18.9% | 19.8% | -0.9 pts | ±1.0 pts | ✓ | zone = ball touches zone, as Savant |
| Whiff% (Savant) | 8.2% | 8.2% | +0.0 pts | ±1.0 pts | ✓ |  |
| GB% (Savant) | 41.9% | 41.9% | +0.0 pts | ±1.0 pts | ✓ |  |
| FB% (Savant) | 22.3% | 22.3% | +0.0 pts | ±1.0 pts | ✓ |  |
| LD% (Savant) | 30.9% | 30.9% | +0.0 pts | ±1.0 pts | ✓ |  |
| PU% (Savant) | 4.9% | 4.9% | +0.0 pts | ±1.0 pts | ✓ |  |
| Pulled Air% (Savant Pull AIR%) (Savant) | 12.9% | 12.2% | +0.7 pts | ±1.0 pts | ✓ | spray from hit coordinates; avg within ~0.5 |
| Pull% (Savant) | 32.6% | 27.0% | +5.6 pts | ±6.0 pts | ✓ | known approximate (~4 pts high) |
| Oppo% (Savant) | 34.9% | 33.2% | +1.7 pts | ±6.0 pts | ✓ | known approximate |
| Sprint speed (Savant) | 27.60 | 27.60 | +0.0 ft/s | ±0.05 ft/s | ✓ | copied from Savant |
| Pitches seen (Savant) | 2618 | 2618 | +0 | ±5 | ✓ |  |
| EV90 (FanGraphs) | 95.3 | 95.2 | +0.1 mph | ±0.5 mph | ✓ | FanGraphs EV90 |
| wOBA (FanGraphs) (FanGraphs) | .331 | .334 | -2.7 pts | ±10 pts | ✓ | guide says ~.005 above FG for power hitters |
| fastball Pitches (Savant arsenal) | 1772 | 1773 | -1 | ±5 | ✓ |  |
| fastball PA ending (Savant arsenal) | 407 | 409 | -2 | ±2 | ✓ |  |
| fastball wOBA (Savant arsenal) | .367 | .385 | -18.2 pts | ±15 pts | ✗ | Savant rolled up PA-weighted (approximate) |
| fastball xwOBA (Savant arsenal) | .362 | .359 | +2.8 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| fastball K% (Savant arsenal) | 6.9% | 6.9% | +0.0 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| fastball Whiff% (Savant arsenal) | 5.5% | 5.3% | +0.2 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| fastball Hard-hit% (Savant arsenal) | 9.5% | 9.3% | +0.2 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| breaking Pitches (Savant arsenal) | 572 | 572 | +0 | ±5 | ✓ |  |
| breaking PA ending (Savant arsenal) | 148 | 147 | +1 | ±2 | ✓ |  |
| breaking wOBA (Savant arsenal) | .287 | .300 | -12.6 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| breaking xwOBA (Savant arsenal) | .283 | .277 | +6.4 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| breaking K% (Savant arsenal) | 18.2% | 18.3% | -0.1 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| breaking Whiff% (Savant arsenal) | 14.2% | 14.3% | -0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| breaking Hard-hit% (Savant arsenal) | 13.8% | 14.0% | -0.2 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |
| offspeed Pitches (Savant arsenal) | 267 | 265 | +2 | ±5 | ✓ |  |
| offspeed PA ending (Savant arsenal) | 78 | 77 | +1 | ±2 | ✓ |  |
| offspeed wOBA (Savant arsenal) | .231 | .237 | -6.1 pts | ±15 pts | ✓ | Savant rolled up PA-weighted (approximate) |
| offspeed xwOBA (Savant arsenal) | .265 | .269 | -4.3 pts | ±20 pts | ✓ | house model; PA-weighted roll-up |
| offspeed K% (Savant arsenal) | 9.0% | 9.1% | -0.1 pts | ±1.0 pts | ✓ | PA-weighted roll-up |
| offspeed Whiff% (Savant arsenal) | 11.8% | 11.9% | -0.1 pts | ±2.0 pts | ✓ | pitch-weighted roll-up (Savant gives no swing counts) |
| offspeed Hard-hit% (Savant arsenal) | 7.5% | 7.5% | -0.0 pts | ±3.0 pts | ✓ | PA-weighted roll-up (Savant gives no BBE counts) |

