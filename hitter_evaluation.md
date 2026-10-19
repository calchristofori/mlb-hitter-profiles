# Hitter Evaluation Method

## Core tenet
Evaluate the hitter systematically, using expected stats and batted-ball primitives across seasons, platoon splits and pitch types, to build a foundational understanding of the player. Outcome stats (AVG, HR, wOBA, RBI) are noisy, so expected stats and process metrics carry the evaluation. Lead with underlying skills; use outcome stats only as context, or to flag gaps worth investigating.

## The question every report answers
Who is this hitter stylistically, what are his strengths and weaknesses, and how does he drive value?

Build the answer in layers: expected stats, batted-ball profile, plate discipline, platoon profile and performance by pitch type. Then synthesize across all of them: what kind of hitter he is, how he wins, where he is vulnerable, and what is changing.

## Foundational metrics
Four metrics give a first, rounded view of the hitter. Each covers one dimension of the profile:

1. **xwOBA (house model)** — *performance.* Overall quality of performance with outcome noise stripped out. xBA and xSLG split it into its contact and power components.
2. **EV90** — *power and output.* His damage ceiling: the capacity to impact the baseball, and a strong signal of hitter type.
3. **Pulled Air%** — *batted-ball tendency.* How often he hits the ball in the air to the pull side, where most damage happens.
4. **IZ Swing% minus Chase%** — *plate discipline.* How well he attacks pitches in the zone and lays off pitches outside it; generally, higher is better. Read it with IZ Swing% and Chase% to see whether it reflects attacking strikes, taking them, or chasing.

Read these four together before anything else. The steps below explain *why* they look the way they do.

## Expected stats
**xwOBA** (house model) is the best overall view of a hitter's underlying performance: what his quality of contact, strikeouts and walks should have produced, with outcome noise stripped out.

**xBA** and **xSLG** show *how* he gets to his xwOBA:
- **xBA** reflects how often he puts the ball in play, and how often that contact comes at favorable exit velocity and launch angle combinations. Strikeouts pull it down, because they count as at-bats with no chance of a hit.
- **xSLG** gauges his damage profile: how much extra-base damage his contact should produce.

**xISO** (xSLG − xBA), expected isolated power, is the extra bases a hitter should produce per at-bat. It separates his damage profile from his batting average, which makes it one of the clearest markers of style. Two hitters with the same xBA can be a slugger and a singles hitter.

xISO should confirm what the batted-ball metrics show. A high EV90 and Pulled Air% should produce a high xISO. A high EV90 with a low xISO means power that isn't playing, usually because the ball is on the ground or going the other way.

Read xBA and xISO together:
- High xBA, high xISO: a complete hitter who hits for average and power.
- Low xBA, high xISO: damage over contact.
- High xBA, low xISO: a contact or singles hitter whose value depends on batting average.
- Low xBA, low xISO: little offensive value from contact.

Lean on xISO over actual ISO, since actual ISO carries outcome noise.

## 1. What kind of hitter is he?
Read his batted-ball profile and his plate discipline, then name the type.

### Batted-ball profile
A batted-ball profile has three core components: **exit velocity, launch angle and spray angle**. Every hitter has a different distribution of each, and together they define his batted-ball style.

- **EV90**: how hard he can impact the baseball. Harder-hit balls are more likely to go for hits and do damage.
- **LA median**: his launch profile, the trajectory at which he tends to hit the ball, from ground-ball hitter to fly-ball hitter.
- **LA SD**: the context for the median. His typical deviation in launch angle, and a marker of launch consistency. A tight spread means he repeats his launch; a wide spread means more balls at both extremes, grounders and popups.
- **Pull%**: a proxy for spray angle. How often he pulls the ball rather than using center and the opposite field. Pull% is approximate in this data, so read it as direction and against the league average, and use Pulled Air% for how often he pulls the ball in the air.

No single one of these defines the profile; how they come together does. Synthesize EV90, LA median, LA SD and Pull% into one description of his batted-ball profile, for example:
- **High EV90, high LA median, tight LA SD, pull-heavy:** the power profile. Hard contact, lifted consistently to the pull side.
- **High EV90, low LA median:** real power spent on the ground.
- **Modest EV90, productive LA median, tight LA SD:** damage through efficient launch, not high exit velocity.
- **Wide LA SD:** good contact that's inconsistent. Some balls driven, many topped or popped up.
- **Low EV90, low LA median, all fields:** a contact and speed profile.

Supporting evidence: Hard-hit%, Barrel% and Sweet spot% show how often contact turns into damage (a hitter can have a strong EV90 and still convert few batted balls into damage), and the ball-flight mix (GB%, LD%, FB%, PU%) confirms the launch profile.

### Plate discipline
The batted-ball profile describes what happens once the hitter makes contact. Plate discipline describes how he navigates the plate appearance: **how often he swings, what he swings at, and whether he makes contact when he does.**

- **IZ Swing% and Chase%: how often he swings, and at what.** Read them separately first. Is he aggressive in the zone, off the plate, or both? Then read **IZ Swing − Chase**: a single number for his aggressiveness in the zone net of his aggressiveness outside it.
- **Whiff%: what happens when he swings.** Read it with the swing rates:
  - **High Whiff%, high IZ Swing%:** he attacks strikes but struggles to make contact. Often a power-only profile.
  - **High Whiff%, high Chase%:** he expands out of the zone and gets beat. There are gains to be had from chasing less, staying in the zone and putting balls in play.
  - **High Whiff%, low Chase%:** he is missing hittable pitches, not expanding the zone.
  - **Low Chase%, low IZ Swing%:** passivity, not discipline.
- **K% and BB%** show how all of this turns into results.

Synthesize these into one description of his discipline profile: how often he swings, what he swings at, and whether he makes contact.

Speed matters only when it changes the profile: when his legs add infield hits and extra bases, or when his value depends entirely on the bat.

## 2. Platoon profile and pitch types: where is he vulnerable?
The question: where is he vulnerable, and are pitchers already using it?

**By platoon side.**
Platoon performance is critical to understanding the full profile of the hitter. Is he far better against one side? Does he have a distinct batted-ball profile against each hand? Or can he handle left- and right-handed pitching with similar ability? His batted-ball profile sometimes changes by handedness, and hitters often have distinct performance profiles against each side. These are important features to understand.
- Apply the same reading to each split: expected stats, batted-ball profile and plate discipline. Is he a different hitter against one side, or the same hitter with fewer PA? Is he a platoon candidate or an everyday bat?
- For switch hitters, each split is a different side of the plate.

**By pitch group (fastball, breaking, offspeed).**
- Compare xwOBA and Whiff% for each group with the qualified average for that group. A weakness is a group where either ranks in the bottom quarter of qualified hitters. Check Chase% on that group too.
- Can he handle all three groups, or is his performance weighted toward one? Can he hit fastballs?
- Swing data (IZ Swing%, Chase%, Whiff%) counts every pitch, so its samples are large. Results data (xwOBA, Hard-hit%) counts only PA ending on that group, so its samples are small. A weakness is most convincing when both agree.
- Pitch share shows how pitchers attack him. A share above average, or rising across seasons, means pitchers have noticed something.

## 3. How does he win?
How he drives value is the synthesis of every layer above. How often does he swing, what does he swing at, how often does he make contact, what does that contact look like, and how does that combination produce his xBA, xSLG, xISO and xwOBA? Find the one or two skills that carry his value.

- **High Pulled Air%, high PU%:** the lift is there, but he gets under the ball too often. A high PU% is the usual cost of an air-ball approach without enough exit velocity or a good enough angle.

A strength is real when several metrics point the same way and the pattern holds across seasons. One standout number, or one season, is a lead, not a strength.

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
