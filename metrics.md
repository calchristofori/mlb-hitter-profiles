# Metric glossary

What every metric in the data packet means, how it is computed, and how it compares with Baseball Savant and FanGraphs. Definitions follow the pipeline code (`~/mlb_data_scripts/build_batter_season.sql`); comparisons come from the 2023–2026 validation (`validation/report_2026-10-18.md`, qualified hitters).

Units: rates like .383 are shown to three decimals; percentages to one decimal. "Batted balls" (BBE) are balls in play with tracking data, bunts included unless noted. All stats are MLB regular season only.

## Samples and context

- **PA** — plate appearances. Matches MLB official totals to within 0.01% league-wide. Known gap: automatic intentional walks (no pitch thrown) are missing, about 12 per season league-wide, so a hitter's PA, BB and IBB can be 1–2 short.
- **BBE** — batted balls with exit velocity and launch angle tracked. The denominator for most contact and batted-ball metrics.
- **Pitches** — pitches seen.
- **Qualified** — 502+ PA in a season (3.1 per team game; 186 in 2020). League context uses qualified hitters only.
- **Qualified avg** — the simple average of qualified hitters' values (each hitter counts once, not weighted by PA).
- **Rank** — the player's place among qualified hitters, 1 = best. Ties share a rank. Shown only for metrics with a clear better direction, and only when the player is qualified.
- **Percentile** — the share of qualified hitters he ranks ahead of: 100 = best, 0 = worst. Rank 104 of 135 is the 23rd percentile; the bottom quarter is below 25.
- **Age** — as of June 30 of the season.
- **Platoon splits** — vs LHP / vs RHP, by the pitcher's throwing hand.
- **Season-over-season change** — later season minus earlier. Rates in points of .001 (+.048); percentages in percentage points (+4.4 pts).

## Results

- **AVG, OBP, SLG** — standard definitions. Match Savant to within .001 on average; all qualified hitters within .002 except a rare outlier (largest .008, from late official-scoring changes).
- **BABIP** — (H − HR) ÷ (AB − SO − HR + SF).
- **wOBA** — weighted on-base average with **house weights**: each event's run value comes from this database's run-expectancy tables for that season, scaled so league wOBA equals league OBP (the FanGraphs method). Formula: (uBB, HBP, 1B, 2B, 3B, HR, each × its weight) ÷ (AB + BB − IBB + SF + HBP). Runs about .002 above Savant and FanGraphs on average, up to ~.008 for big power hitters.
- **K%** — strikeouts ÷ PA. **BB%** — walks (including intentional) ÷ PA. Both match Savant.
- **HR** — home runs.

## Expected stats (house model)

Built from this database, not copied from Savant. Always label them "(house model)".

- **xwOBA** — expected wOBA. Each tracked batted ball gets single/double/triple/HR probabilities from what balls with the same exit velocity and launch angle (1 mph × 1° cells, smoothed toward wider cells, season-specific) did that season. Ground balls (launch angle under 10°) and bunts are adjusted by the batter's sprint-speed tier. Walks, HBP and strikeouts count at actual value. Same denominator as wOBA. Runs about .004 above Savant's xwOBA on average; 89% of qualified hitters are within .010; correlation 0.99.
- **xBA** — expected hits ÷ AB, same model. About .003 above Savant.
- **xSLG** — expected total bases ÷ AB, same model. About .001 above Savant.
- **wOBA − xwOBA (gap)** — results minus expected. Positive means results ran ahead of contact quality.

## Contact quality

- **EV90** — 90th-percentile exit velocity of his batted balls, bunts excluded. A measure of top-end damage. Matches FanGraphs' EV90 to within 0.1 mph on average.
- **Avg EV** — average exit velocity, bunts excluded. Matches Savant.
- **Hard-hit%** — batted balls at 95+ mph ÷ BBE. Matches Savant to within ~0.1 pts.
- **Barrel%** — barrels ÷ BBE. A barrel here is 98+ mph with launch angle ≤ 50°, 1.5 × EV − LA ≥ 117 and EV + LA ≥ 124, an approximation of Statcast's barrel zone. Runs about 0.5 pts below Savant.
- **Sweet spot%** — batted balls with launch angle 8–32° ÷ BBE. Launch angles come rounded to whole degrees, so balls at exactly 8° or 32° count as half. Within ~0.3 pts of Savant.

## Batted-ball shape

- **LA median** — median launch angle in degrees, bunts excluded. Note: Savant shows the *average* launch angle, which differs.
- **LA SD** — standard deviation of launch angle, bunts excluded. Lower means a more consistent swing path.
- **GB%, LD%, FB%, PU%** — ground balls, line drives, fly balls and popups, each ÷ batted balls with a recorded type; the four add to 100%. Statcast classification, matching Savant exactly. **FB% excludes popups** (they are PU%), so it runs well below FanGraphs' FB%, which includes popups and uses a different batted-ball classifier. Bunts count in GB%, LD% or PU% by their trajectory.

## Direction

Direction comes from where the ball landed or was fielded (spray angle). "Pull side" means more than 16° toward his pull field (left field for a right-handed hitter); "opposite field" means more than 16° the other way.

- **Pulled Air%** — balls in the air (fly balls, line drives and popups) hit to the pull side ÷ batted balls with a direction. Savant's name is "Pull AIR%". Within ~0.5 pts of Savant on average, occasionally 2+ apart. **Not the same as FB%**: it includes line drives and popups, and it counts only pulled balls. Database column: `pulled_fb_pct`.
- **Pull%** — all pulled batted balls (including ground balls) ÷ batted balls with a direction. Approximate: runs about 4 pts above Savant because ground-ball direction is inferred from where the ball was fielded. Use for trends, not cross-source comparisons.
- **Oppo%** — same, to the opposite field. Approximate: about 2 pts above Savant.

## Plate discipline

"In the zone" means any part of the ball touches the strike zone: the 17-inch plate width and the batter's own zone top and bottom, widened by the ball's radius (1.45 in) on every side. This is Savant's definition. Swings include swinging strikes, fouls, foul tips, balls in play and bunt attempts.

- **IZ Swing%** — swings ÷ pitches in the zone. Within ~0.2 pts of Savant on average.
- **Chase%** — swings ÷ pitches outside the zone (Savant: O-Swing%). Within ~0.25 pts of Savant on average; 92% of qualified hitters within 1 pt.
- **IZ Swing − Chase** — IZ Swing% minus Chase%, shown as a decimal (.360 = 36.0 points). Generally, higher is better: a hitter who attacks pitches in the zone and lays off pitches outside it. It is not a swing-decision score: it does not account for count, pitch quality or location within the zone, so it shows how a hitter's swings split between strikes and balls, not how good each decision was. Read it with IZ Swing% and Chase% to see what drives it. Not a public stat.
- **Whiff%** — misses ÷ swings. Foul tips count as misses, as on Savant. Matches Savant.

## Speed

- **Sprint speed** — feet per second on competitive runs, copied from Baseball Savant. About 27 is average, 30+ elite, under 25 slow.

## By pitch group

- **Pitch groups** — **Fastball**: four-seam, sinker, cutter, two-seam. **Breaking**: slider, sweeper, curveball, knuckle curve, slurve, slow curve. **Offspeed**: changeup, splitter, forkball, screwball. Eephus, knuckleballs and unknown types are left out (about 0.2% of pitches). Pitch types are MLB's labels; Savant sometimes relabels pitches after the game, so group pitch counts can differ from Savant by a few.
- **Two ways of counting.** Pitches, Share, IZ Swing%, Chase% and Whiff% count **every pitch** of the group he saw. **PA ending** and everything after it (wOBA, xwOBA, K%, BBE, EV90, Hard-hit%, Barrel%) count only plate appearances whose **last pitch** was in the group, as on Savant's pitch-type leaderboards.
- **Share** — pitches of the group ÷ his pitches in all three groups. How pitchers attack him.
- **PA ending** — plate appearances that ended on a pitch of the group. Much smaller than his season PA.
- Every other pitch-group metric has the same definition as its full-season version above, limited to that group.
