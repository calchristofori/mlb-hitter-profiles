# Hitter Evaluation Method

## Core belief
Judge the process, not the outcomes. Outcome stats (AVG, HR, wOBA, RBI) are noisy. Expected stats and batted-ball primitives are signal. Lead with underlying skills; use outcome stats only as context or to flag gaps worth investigating.

## The question every report answers
How does this hitter create value, and what kind of hitter is he? Trends and aging inform the answer but do not replace it.

## First look (in this order)
1. xwOBA — overall quality of performance, with outcome noise stripped out. This comes from a house model.
2. EV90 (90th percentile exit velocity) — damage ceiling and hitter type.
3. Pulled Air% — how often he hits the ball in the air (fly balls, line drives and popups) to the pull side, where most damage happens.
4. IZ Swing% minus Chase% — swing decisions. Higher is better.

## Trusted inputs
- Contact quality: xwOBA, xSLG, xBA, EV90 - these are expected stats that explain a hitter's impact, as well as EV90 which indicates the capacity of the player to impact the baseball.
- Batted-ball shape: FB%, GB%, launch angle median, launch angle standard deviation. 
- Swing decisions: IZ Swing%, Chase%, Whiff%

## Batted-ball profile
Reason across all of these dimensions together to understand the profile holistically.

- **Exit velocity** — generally higher is better. His capacity to impact the baseball is critical to understanding the hitter. Distinguish hitters who can hit the ball in the air at high exit velocity from those whose hard contact stays lower, in line drives and ground balls. *(Exit velocity by batted-ball type: when available.)*
- **Spray angle** — understand how the hitter uses the field and where his damage comes from. Is he pull-happy? Does he use the opposite field? What is the distribution of his batted balls across the diamond? The exit velocity / launch angle combination within pull, center and oppo, and how often each direction is used, gives the strongest understanding. *(Center%, and exit velocity / launch angle by field direction: when available.)*
- **Launch angle median and SD** — the median signals where he generally lives in ball flight: where on the spectrum from ground-ball hitter to fly-ball hitter he sits. The SD signals consistency of launch. Hitters with greater deviation tend to hit more fly balls and more ground balls, at both extremes.

## Plate discipline and approach
- **Count** — Is he aggressive early in the count? How does he perform when ahead or in hitter's counts — does he do damage? How does he fare with two strikes? How often does he get himself behind in the count or into two-strike counts? Does he tend to play ahead or behind? *(when available)*
- **Zone** — Is he aggressive in the middle of the zone (heart-swing%)? Where in the strike zone does he do the most damage? Are there hot zones based on pitcher handedness? Are there cold zones where he has a really hard time? *(when available)*

## Compare with the league
Judge every metric against the qualified-hitter average and his rank or percentile in that season, not against fixed cutoffs. "Well above average" means near the top of the league in rank, not past a set number.

## Green flags
Hits the ball hard (EV90 well above average), a high Sweet spot% (lives in the 8–32° launch angle window), swings at strikes, and whiffs less than average.

## Red flags
Whiffs well above average, struggles to make contact.

## Aging and decline signals
Read the trend through batted-ball inputs, not results. Possible signs of a slowing bat:
- EV90 trending down
- Whiff% trending up
- Pull% or Pulled Air% trending down

When two or more move together, flag it — with more weight for older hitters.

## Sample size
| PA in a season | How to treat it |
|---|---|
| < 100 | No read. Say so explicitly. |
| 100–200 | Early read. Flag as tentative. |
| 200+ | Reliable read. |

Always state PA for every season shown.

## Performance by pitch type
The question: where does he do damage, and is there a pitch group pitchers can use against him?
- Compare xwOBA and Whiff% for each group with the qualified average for that group.
- A weakness is a group where his xwOBA or Whiff% ranks in the bottom quarter of qualified hitters for that group. Check Chase% on that group too.
- Pitch share shows how pitchers attack him. A rising share for one group across seasons means pitchers have noticed something.
- Sample: fewer than 50 PA ending on a group is no read.
- Against which pitch types does he have the most success? Can he hit velocity, or does he struggle against fastballs? Can he handle all of them, or is his performance weighted toward certain pitch types? *(Performance by pitch velocity: when available.)*
- Across pitch types and locations, are there areas with a valid sample where he struggles, or where he really excels? *(Pitch type × location over his last 600 PA: when available.)*

## Priorities
Profile, Skill breakdown and Performance by pitch type are the most important sections: they carry most of the report, roughly two-thirds of the words. Every other section is brief:
- Bottom line: two or three sentences.
- Three-year trend table: the table, plus one sentence on direction.
- Underlying vs. results: one or two sentences.
- Strengths and concerns: three short bullets each, with no new analysis; point back to the findings above.
- Outlook: two or three sentences.
- Sample and sources: a few short lines.

## Report format
1. Header — name, position, team, age, bats/throws
2. Bottom line — the hitter in two or three sentences: how he drives value, his defining strength and his biggest vulnerability. Write last.
3. Profile — hitter type and style (from EV90, batted-ball shape, approach)
4. Three-year trend table — PA, xwOBA, EV90, Pulled Air%, IZ Swing% − Chase%, Whiff%, LA median, LA SD, with a direction column
5. Underlying vs. results — wOBA vs. xwOBA
6. Skill breakdown — contact quality, batted-ball shape, swing decisions
7. Performance by pitch type — damage and weaknesses by fastball / breaking / offspeed, and how pitchers attack him
8. Strengths and concerns — three bullets each, every one backed by a number
9. Outlook — trend direction and any aging/decline signals; the one thing to watch
10. Sample and sources — PA by season, data dates, small-sample flags

## Rules
- Every number must come from the data, never from memory.
- Separate what the data shows from your interpretation.
- No 20–80 grades.
- If data needed for a section is missing, say so instead of filling the gap.
- Items marked *(when available)* depend on data that may not be collected yet. When it is missing, skip them without comment.
