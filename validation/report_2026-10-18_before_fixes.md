# Data validation report — 2026-10-18

Seasons 2023–2026. Reference data downloaded to `validation/downloads/2026-10-18`. Qualified hitters: 543 player-seasons (502+ PA).

**Summary:** 34 OK · 9 CHECK · 1 ISSUE.

Status rule: OK = 95%+ of players within tolerance; CHECK = 80–95%; ISSUE = under 80% (or any internal check failing). Bias is ours minus theirs: positive means our number runs higher.

## 1. Counting stats vs. MLB Stats API (every hitter)

| Season | Our hitters | API hitters (1+ PA) | In both | Only ours | Only API |
|---|---|---|---|---|---|
| 2023 | 656 | 656 | 656 | 0 | 0 |
| 2024 | 651 | 651 | 651 | 0 | 0 |
| 2025 | 673 | 673 | 673 | 0 | 0 |
| 2026 | 662 | 662 | 662 | 0 | 0 |

| Stat | Player-seasons | Exact match | Our total | Official total | Total diff |
|---|---|---|---|---|---|
| PA | 2642 | 94.10% | 733,356 | 733,328 | +0.004% |
| AB | 2642 | 95.31% | 655,180 | 655,098 | +0.013% |
| H | 2642 | 97.96% | 160,652 | 160,649 | +0.002% |
| 2B | 2642 | 99.89% | 31,236 | 31,237 | -0.003% |
| 3B | 2642 | 99.96% | 2,707 | 2,708 | -0.037% |
| HR | 2642 | 99.96% | 22,547 | 22,546 | +0.004% |
| RBI | 2642 | 99.43% | 83,443.0 | 83,436 | +0.008% |
| BB | 2642 | 98.22% | 62,416 | 62,464 | -0.077% |
| IBB | 2642 | 98.22% | 2,036 | 2,084 | -2.303% |
| HBP | 2642 | 100.00% | 8,178 | 8,178 | +0.000% |
| SO | 2642 | 98.68% | 164,380 | 164,385 | -0.003% |
| SF | 2642 | 100.00% | 5,096 | 5,096 | +0.000% |
| SH | 2642 | 99.85% | 2,121 | 2,123 | -0.094% |
| GIDP | 2642 | 98.71% | 12,927 | 12,960 | -0.255% |
| Pitches | 2642 | 94.10% | 2,852,021 | 2,852,024 | -0.000% |

Largest mismatches:

| Stat | Season | Player | Ours | Official |
|---|---|---|---|---|
| Pitches | 2023 | Jesús Sánchez | 1664 | 1658 |
| Pitches | 2023 | Tucupita Marcano | 737 | 731 |
| Pitches | 2025 | Shea Langeliers | 1918 | 1924 |
| Pitches | 2025 | Logan Davidson | 211 | 205 |
| Pitches | 2023 | Eduardo Escobar | 1242 | 1237 |
| Pitches | 2023 | Danny Jansen | 1190 | 1185 |
| Pitches | 2023 | Anthony Rendon | 756 | 761 |
| Pitches | 2023 | Tyler Heineman | 176 | 181 |
| Pitches | 2026 | James Wood | 2610 | 2605 |
| Pitches | 2026 | Jazz Chisholm Jr. | 2163 | 2168 |
| Pitches | 2026 | Ronald Acuña Jr. | 1860 | 1865 |
| Pitches | 2026 | Francisco Alvarez | 1740 | 1745 |
| Pitches | 2026 | Luis Torrens | 1109 | 1104 |
| Pitches | 2026 | Anthony Volpe | 984 | 979 |
| Pitches | 2026 | Brice Matthews | 964 | 959 |
| Pitches | 2026 | Drew Millas | 580 | 585 |
| Pitches | 2026 | Brewer Hicklen | 179 | 174 |
| Pitches | 2023 | Teoscar Hernández | 2669 | 2673 |
| Pitches | 2023 | Jack Suwinski | 2277 | 2281 |
| Pitches | 2023 | Jonah Heim | 1991 | 1995 |
| Pitches | 2023 | Royce Lewis | 902 | 906 |
| Pitches | 2023 | Riley Adams | 562 | 566 |
| Pitches | 2023 | Cade Marlowe | 435 | 431 |
| Pitches | 2023 | Michael Chavis | 380 | 376 |
| Pitches | 2023 | Sam Huff | 164 | 160 |

## 2. Rates and Statcast metrics vs. Savant / FanGraphs (qualified hitters)

| Metric | n | Corr | Bias (ours − theirs) | Mean abs diff | 95th pct abs diff | Largest diff | Within tolerance | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| PA | 543 | 1.000 | -0.00 | 0.11 | 1.00 | -2 (Shea Langeliers 2024) | 89% (±0 count) | CHECK |  |
| AVG | 543 | 1.000 | -0.0 | 0.10 | 1.00 | +3.0 (Jazz Chisholm Jr. 2026) | 100% (±2 pts (.001)) | OK |  |
| OBP | 543 | 1.000 | -0.1 | 0.13 | 1.00 | -2.0 (Paul Goldschmidt 2024) | 100% (±2 pts (.001)) | OK |  |
| SLG | 543 | 1.000 | -0.0 | 0.13 | 1.00 | +8.0 (TJ Rumfield 2026) | 100% (±2 pts (.001)) | OK |  |
| wOBA | 543 | 0.999 | +2.3 | 2.47 | 5.00 | +8.0 (Shohei Ohtani 2023) | 100% (±10 pts (.001)) | OK | house weights vs Savant weights |
| xwOBA | 543 | 0.990 | +3.7 | 5.12 | 12.00 | +19.0 (JJ Wetherholt 2026) | 89% (±10 pts (.001)) | CHECK | house model; guide says typical gap 3–7 pts |
| xBA | 543 | 0.987 | +3.0 | 3.86 | 9.00 | +15.0 (Brent Rooker 2025) | 97% (±10 pts (.001)) | OK | house model |
| xSLG | 543 | 0.994 | +1.2 | 5.89 | 14.00 | +29.0 (JJ Wetherholt 2026) | 99% (±20 pts (.001)) | OK | house model |
| K% | 543 | 1.000 | -0.0 | 0.00 | 0.00 | -0.2 (Nolan Schanuel 2025) | 100% (±0.3 pct pts) | OK |  |
| BB% | 543 | 1.000 | -0.0 | 0.01 | 0.10 | -0.4 (Shea Langeliers 2024) | 100% (±0.3 pct pts) | OK |  |
| Avg EV | 543 | 1.000 | -0.0 | 0.00 | 0.00 | +0.1 (Alex Bregman 2024) | 100% (±0.3 mph) | OK |  |
| Hard-hit% | 543 | 1.000 | +0.1 | 0.13 | 0.40 | +1.2 (Elly De La Cruz 2026) | 100% (±1.0 pct pts) | OK |  |
| Barrel% | 543 | 0.996 | -0.5 | 0.50 | 1.10 | -2.1 (Jake Bauers 2026) | 92% (±1.0 pct pts) | CHECK | guide says ~0.5 pts below Savant |
| Sweet spot% | 543 | 0.985 | +1.4 | 1.42 | 2.40 | +3.7 (Willson Contreras 2026) | 87% (±2.0 pct pts) | CHECK | guide says ~1.5 pts below Savant |
| IZ Swing% | 543 | 0.998 | +0.1 | 0.22 | 0.90 | +1.5 (Tyler Stephenson 2024) | 97% (±1.0 pct pts) | OK |  |
| Chase% | 543 | 0.994 | +0.5 | 0.53 | 1.80 | +2.6 (Ian Happ 2024) | 76% (±1.0 pct pts) | ISSUE |  |
| Whiff% | 543 | 1.000 | +0.0 | 0.00 | 0.00 | +0.2 (Jo Adell 2025) | 100% (±1.0 pct pts) | OK |  |
| GB% | 543 | 1.000 | -0.0 | 0.00 | 0.00 | +0.1 (Gleyber Torres 2023) | 100% (±1.0 pct pts) | OK |  |
| FB% | 543 | 1.000 | -0.0 | 0.00 | 0.00 | -0.1 (Aaron Judge 2024) | 100% (±1.0 pct pts) | OK |  |
| LD% | 543 | 1.000 | -0.0 | 0.00 | 0.00 | -0.1 (Aaron Judge 2024) | 100% (±1.0 pct pts) | OK |  |
| PU% | 543 | 1.000 | -0.0 | 0.00 | 0.00 | -0.1 (Cedric Mullins 2026) | 100% (±1.0 pct pts) | OK |  |
| Pulled FB% (Pull AIR%) | 543 | 0.994 | +0.1 | 0.46 | 1.19 | -2.4 (Mookie Betts 2026) | 90% (±1.0 pct pts) | CHECK | guide says within 0.5 pts |
| Pull% | 543 | 0.930 | +3.9 | 3.96 | 7.80 | +11.4 (Luis García Jr. 2024) | 82% (±6.0 pct pts) | CHECK | known approximate (~4 pts high) |
| Oppo% | 543 | 0.939 | +1.9 | 2.03 | 4.90 | +7.8 (Jacob Wilson 2025) | 99% (±6.0 pct pts) | OK | known approximate |
| Sprint speed | 543 | 1.000 | +0.00 | 0.00 | 0.00 | +0.00 (Marcus Semien 2023) | 100% (±0.05 ft/s) | OK | copied from Savant |
| Pitches seen | 543 | 1.000 | -0.07 | 0.17 | 1.00 | -6 (Shea Langeliers 2025) | 100% (±5 count) | OK |  |
| EV90 | 543 | 1.000 | -0.0 | 0.03 | 0.20 | +0.4 (Jacob Young 2024) | 100% (±0.5 mph) | OK | FanGraphs EV90 |
| wOBA (FanGraphs) | 543 | 0.999 | +2.3 | 2.48 | 5.20 | +8.5 (Shohei Ohtani 2024) | 100% (±10 pts (.001)) | OK | guide says ~.005 above FG for power hitters |

## 3. Pitch groups vs. Savant pitch-arsenal leaderboard (qualified hitters)

Savant reports each pitch type separately; they are rolled up into our three groups. Savant gives no swing or batted-ball counts per pitch type, so whiff% and hard-hit% roll-ups are weighted approximations.

| Metric | n | Corr | Bias (ours − theirs) | Mean abs diff | 95th pct abs diff | Largest diff | Within tolerance | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| Pitches | 1629 | 1.000 | +1 | 3.22 | 11.00 | +20 (Ozzie Albies 2023 fastball) | 80% (±5 count) | CHECK |  |
| PA ending | 1629 | 1.000 | +0.53 | 1.11 | 3.00 | +10 (Ezequiel Tovar 2026 fastball) | 86% (±2 count) | CHECK |  |
| wOBA | 1629 | 0.988 | -6.8 | 8.51 | 22.30 | -58.9 (Marcus Semien 2026 offspeed) | 85% (±15 pts (.001)) | CHECK | Savant rolled up PA-weighted (approximate) |
| xwOBA | 1629 | 0.992 | +2.5 | 6.31 | 15.98 | +26.2 (Aaron Judge 2025 fastball) | 98% (±20 pts (.001)) | OK | house model; PA-weighted roll-up |
| K% | 1629 | 0.999 | -0.0 | 0.17 | 0.57 | +1.8 (Jordan Beck 2025 offspeed) | 99% (±1.0 pct pts) | OK | PA-weighted roll-up |
| Whiff% | 1629 | 0.999 | +0.1 | 0.25 | 0.73 | -3.3 (Andrew McCutchen 2024 offspeed) | 100% (±2.0 pct pts) | OK | pitch-weighted roll-up (Savant gives no swing counts) |
| Hard-hit% | 1629 | 0.997 | +0.0 | 0.53 | 1.60 | +6.0 (Brent Rooker 2023 offspeed) | 99% (±3.0 pct pts) | OK | PA-weighted roll-up (Savant gives no BBE counts) |

## 4. Internal consistency

| Check | Passing | Status | Detail |
|---|---|---|---|
| H = 1B + 2B + 3B + HR | 2,642 / 2,642 | OK |  |
| AVG = H / AB (rounded) | 2,642 / 2,642 | OK |  |
| SLG = TB / AB (rounded) | 2,642 / 2,642 | OK |  |
| PA ≥ AB + BB + HBP + SF + SH | 2,642 / 2,642 | OK |  |
| Rates between 0 and 1 | 2,642 / 2,642 | OK |  |
| GB + LD + FB + PU ≈ 100% (50+ BBE) | 1,961 / 1,961 | OK |  |
| Pitch groups never exceed season pitches / PA | 2,638 / 2,638 | OK |  |
| Pitch-group shares sum to 100% (±0.2) | 2,638 / 2,638 | OK |  |
| data.py league averages and ranks match SQL (2026, 22 metrics) | 2,970 / 2,970 | OK |  |
