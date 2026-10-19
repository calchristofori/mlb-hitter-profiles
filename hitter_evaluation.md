# Hitter Evaluation Method

## Core tenet
Evaluate the hitter systematically, using expected stats and batted-ball primitives across seasons, platoon splits and pitch types, to build a foundational understanding of the player. Outcome stats (AVG, HR, wOBA, RBI) are noisy, so expected stats and process metrics carry the evaluation. Lead with underlying skills; use outcome stats only as context, or to flag gaps worth investigating.

## The question every report answers
Who is this hitter stylistically, what are his strengths and weaknesses, and how does he drive value?

## Foundational metrics
Four metrics give a first, rounded view of the hitter. Each covers one dimension of the profile:

1. **xwOBA (house model)** — *performance.* Overall quality of performance with outcome noise stripped out. xBA and xSLG (also house model) split it into its contact and power components.
2. **EV90** (90th-percentile exit velocity) — *power and output.* His damage ceiling: the capacity to impact the baseball, and a strong signal of hitter type.
3. **Pulled Air%** — *batted-ball tendency.* How often he hits the ball in the air (fly balls, line drives and popups) to the pull side, where most damage happens.
4. **IZ Swing% minus Chase%** — *plate discipline.* His ability to swing at favorable pitches and lay off unfavorable ones. Higher is better.

Read these four together before anything else. The sections below explain *why* the four look the way they do.

## Batted-ball profile
Reason across all of these dimensions together to categorize the batted-ball profile. The goal is to distinguish hitters who hit the ball in the air from those who hit it on the ground, pull-side hitters from those who use the middle and opposite field, and the exit velocities at which each happens.

- **Exit velocity** — higher is better. The capacity to impact the baseball is central to understanding the hitter. *(Exit velocity by batted-ball type: when available.)*
- **Contact quality** — Hard-hit% (95+ mph), Barrel% and Sweet spot% (launch angle 8–32°) show how often contact turns into damage, not just how hard his best contact is. A hitter can have a strong EV90 and still convert few batted balls into damage.
- **Launch angle median and SD** — the median shows where he generally lives in ball flight, on the spectrum from ground-ball hitter to fly-ball hitter. The SD shows how consistent his launch is: hitters with a wider spread hit more balls at both extremes, more grounders and more high fly balls or popups.
- **Ball-flight mix (GB%, LD%, FB%, PU%)** — does he live in the air or on the ground? A high PU% is the usual cost of an air-ball approach: lift without enough force or a good enough angle.
- **Spray direction** — how does he use the field, and where does his damage come from? Is he pull-happy, or does he use the opposite field? What is the distribution of his batted balls across the diamond? Pulled Air% is the precise measure; Pull% and Oppo% are approximate and best read as trends. *(Center% and exit velocity / launch angle by field direction: when available.)*
- **Speed** — sprint speed shows whether his legs add value, through infield hits and extra bases, or whether his value depends entirely on the bat.

## Plate discipline
- **IZ Swing%** — how aggressive he is on pitches in the zone. Does he attack strikes, or is he passive?
- **Chase%** — how often he offers at pitches outside the zone. A high rate signals a less disciplined, more aggressive hitter; pitches outside the zone are harder to make contact with and to barrel.
- **Whiff%** — how often he swings and misses. A key piece of the profile: it decides how much of his swing turns into contact at all.
- **K% and BB%** — how the swing decisions and contact skills above show up in results. Does he strike out a lot? Does he draw walks?

Read these together. A low chase rate with a low in-zone swing rate is passivity, not discipline; a high whiff rate with a low chase rate means he is missing hittable pitches, not expanding the zone.

## Performance by platoon split
Apply the foundational metrics, batted-ball profile and plate discipline to his performance against right-handed and left-handed pitchers. Call out any differences in style or ability against either side of the platoon, and whether he is a platoon candidate or an everyday bat. For switch hitters, each split is a different side of the plate.
- Apply the sample-size rules below to each split; vs-LHP samples are often small.
- *(Batted-ball profile and plate discipline by split, beyond EV90, Whiff%, K% and BB%: when available.)*

## Performance by pitch type
The question: where does he do damage, and is there a pitch group pitchers can use against him?
- Compare xwOBA and Whiff% for each group with the qualified average for that group.
- A weakness is a group where his xwOBA or Whiff% ranks in the bottom quarter of qualified hitters for that group. Check Chase% on that group too.
- Against which pitch types does he have the most success? Can he handle all three groups, or is his performance weighted toward certain ones?
- Can he hit velocity, or does he struggle against fastballs? *(Performance by pitch velocity: when available.)*
- Pitch share shows how pitchers attack him. A rising share for one group across seasons means pitchers have noticed something.
- Across pitch types and locations, are there areas with a valid sample where he struggles, or where he excels? *(Pitch type × location over his last 600 PA: when available.)*
- Sample: fewer than 50 PA ending on a group is no read.

## Compare with the league
Judge every metric against the qualified-hitter average and his rank or percentile in that season, not against fixed cutoffs. "Well above average" means near the top of the league in rank, not past a set number. When a hitter is not qualified, compare him with the qualified average only.

## Aging and decline signals
Read the trend through batted-ball inputs, not results. Possible signs of a slowing bat:
- EV90 trending down
- Whiff% trending up
- Pulled Air% trending down

When two or more move together, flag it, with more weight for older hitters.

## Sample size
| PA in a season or split | How to treat it |
|---|---|
| < 100 | No read. Say so explicitly. |
| 100–200 | Early read. Flag as tentative. |
| 200+ | Reliable read. |

Always state PA for every season shown.

## Priorities
Profile, Skill breakdown and Performance by pitch type are the most important sections: they carry most of the report, roughly two-thirds of the words. Every other section is brief:
- Bottom line: two or three sentences.
- Three-year trend table: the table, plus one sentence on direction.
- Underlying vs. results: one or two sentences.
- Platoon splits: two or three sentences, unless the split defines the hitter.
- Strengths and concerns: three short bullets each, with no new analysis; point back to the findings above.
- Outlook: two or three sentences.
- Sample and sources: a few short lines.

## Report format
1. Header — name, position, team, age, bats/throws
2. Bottom line — the hitter in two or three sentences: how he drives value, his defining strength and his biggest vulnerability. Write last.
3. Profile — hitter type and style (from the foundational metrics, batted-ball profile and approach)
4. Three-year trend table — PA, xwOBA, EV90, Pulled Air%, IZ Swing% − Chase%, Whiff%, LA median, LA SD, with a direction column
5. Underlying vs. results — wOBA vs. xwOBA
6. Skill breakdown — contact quality, batted-ball profile, plate discipline
7. Platoon splits — style and performance vs. RHP and LHP
8. Performance by pitch type — damage and weaknesses by fastball / breaking / offspeed, and how pitchers attack him
9. Strengths and concerns — three bullets each, every one backed by a number
10. Outlook — trend direction and any aging/decline signals; the one thing to watch
11. Sample and sources — PA by season and split, data dates, small-sample flags

## Rules
- Every number must come from the data, never from memory.
- Separate what the data shows from your interpretation.
- No 20–80 grades.
- If data needed for a section is missing, say so instead of filling the gap.
- Items marked *(when available)* depend on data that may not be collected yet. When it is missing, skip them without comment.
