# Hitter Evaluation Method

## Core tenet
Evaluate the hitter systematically, using expected stats and batted-ball primitives across seasons, platoon splits and pitch types, to build a foundational understanding of the player. Outcome stats (AVG, HR, wOBA, RBI) are noisy, so expected stats and process metrics carry the evaluation. Lead with underlying skills; use outcome stats only as context, or to flag gaps worth investigating.

## The question every report answers
Who is this hitter stylistically, what are his strengths and weaknesses, and how does he drive value?

Answer it in four steps: what kind of hitter he is, how he wins, how pitchers beat him, and what is changing.

## Foundational metrics
Four metrics give a first, rounded view of the hitter. Each covers one dimension of the profile:

1. **xwOBA (house model)** — *performance.* Overall quality of performance with outcome noise stripped out. xBA and xSLG split it into its contact and power components.
2. **EV90** — *power and output.* His damage ceiling: the capacity to impact the baseball, and a strong signal of hitter type.
3. **Pulled Air%** — *batted-ball tendency.* How often he hits the ball in the air to the pull side, where most damage happens.
4. **IZ Swing% minus Chase%** — *plate discipline.* How well he attacks pitches in the zone and lays off pitches outside it; generally, higher is better. Read it with IZ Swing% and Chase% to see whether it reflects attacking strikes, taking them, or chasing.

Read these four together before anything else. The steps below explain *why* they look the way they do.

## 1. What kind of hitter is he?
Place him on three axes, then name the type.

- **Impact:** how hard he can hit the ball (EV90, Avg EV) and how often contact turns into damage (Hard-hit%, Barrel%, Sweet spot%). A hitter can have a strong EV90 and still convert few batted balls into damage.
- **Shape:** where the ball goes. LA median shows where he lives, from ground-ball hitter to fly-ball hitter; LA SD shows how consistent his launch is, and a wider spread means more balls at both extremes, grounders and popups. The ball-flight mix (GB%, LD%, FB%, PU%) confirms it. Spray shows how he uses the field: Pulled Air% is the precise measure; Pull% and Oppo% are approximate and best read as direction.
- **Approach:** how aggressive he is on strikes (IZ Swing%), how often he expands (Chase%), how often he misses (Whiff%), and how that shows up in K% and BB%.

Speed matters only when it changes the profile: when his legs add infield hits and extra bases, or when his value depends entirely on the bat.

> **[Your call — Q1]** Which hitter types do you use, and what metric signature defines each? (For example: pull-side slugger = high EV90 + high Pulled Air%, accepts whiffs.)

## 2. How does he win?
Find the one or two skills that carry his value. Most of the insight is in how metrics combine:

- **High EV90, low LA median:** real power spent on the ground. The damage is capped until he lifts the ball.
- **Modest EV90, high Barrel% and Sweet spot%:** damage through efficient launch, not raw force.
- **High Pulled Air%, high PU%:** the lift is there, but he gets under the ball too often. A high PU% is the usual cost of an air-ball approach without enough force or a good enough angle.
- **Low Chase% with low IZ Swing%:** passivity, not discipline.
- **High Whiff% with low Chase%:** he is missing hittable pitches, not expanding the zone.
- **High xSLG, average xBA:** a damage hitter, not a contact hitter. The reverse is a contact hitter whose value depends on batting average.

> **[Your call — Q2]** What other combinations do you read when you evaluate a hitter?

A strength is real when several metrics point the same way and the pattern holds across seasons. One standout number, or one season, is a lead, not a strength.

> **[Your call — Q3]** Is that the right bar for a strength? Is there a number you've seen fool people?

## 3. How do pitchers beat him?
The question: where is he vulnerable, and are pitchers already using it?

**By pitch group (fastball, breaking, offspeed).**
- Compare xwOBA and Whiff% for each group with the qualified average for that group. A weakness is a group where either ranks in the bottom quarter of qualified hitters. Check Chase% on that group too.
- Can he handle all three groups, or is his performance weighted toward one? Can he hit fastballs?
- Swing data (IZ Swing%, Chase%, Whiff%) counts every pitch, so its samples are large. Results data (xwOBA, Hard-hit%) counts only PA ending on that group, so its samples are small. A weakness is most convincing when both agree.
- Pitch share shows how pitchers attack him. A share above average, or rising across seasons, means pitchers have noticed something.

**By platoon side.**
- Apply the same reading to his performance against right-handed and left-handed pitchers. Is he a different hitter against one side, or the same hitter with fewer PA? Is he a platoon candidate or an everyday bat?
- For switch hitters, each split is a different side of the plate.

> **[Your call — Q4]** How do you decide a hole is real and not noise? What would convince you?

## 4. What is changing?
Read the trend through batted-ball inputs, not results. Possible signs of a slowing bat:
- EV90 trending down
- Whiff% trending up
- Pulled Air% trending down

When two or more move together, flag it, with more weight for older hitters. Separate decline from a change in approach: falling Pulled Air% with rising Sweet spot% and Oppo% can be a deliberate all-fields adjustment.

Results vs. expected: when wOBA and xwOBA diverge, the expected stat is the better guide to his skill.

## Compare with the league
Judge every metric against the qualified-hitter average and his rank or percentile in that season, not against fixed cutoffs. "Well above average" means near the top of the league in rank, not past a set number. When a hitter is not qualified, compare him with the qualified average only.

## Sample size
| PA in a season or split | How to treat it |
|---|---|
| < 100 | No read. Say so explicitly. |
| 100–200 | Early read. Flag as tentative. |
| 200+ | Reliable read. |

For pitch groups, fewer than 50 PA ending on a group is no read for its results data.
