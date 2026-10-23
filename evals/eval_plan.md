# Hitter report eval: plan (DRAFT, to be rewritten in my words)

The question this eval answers: **are the reports good, and did a change make them better or worse?**
Judging by eye can't answer that (the same prompt gave 0 of a habit one run and 5 the next).
So: the same test hitters, each run several times, scored the same way every time.

## 1. Test hitters

Eight hitters, each picked to test a different part of the method. 2026 is the latest season.

| # | Hitter | Type it tests | What makes him a test |
|---|---|---|---|
| 1 | Kyle Schwarber | Power over contact | Elite xISO, bottom-quarter xBA, high Whiff%. |
| 2 | Luis Arraez | Contact / singles | Elite xBA and Whiff%, almost no xISO. |
| 3 | Yordan Alvarez | Complete hitter | Near the top in everything; only 199 PA in 2025 (tests sample-size handling across seasons). |
| 4 | Salvador Perez | Chaser, aging | One of the highest Chase% in the league, age 36, EV90 down from 2024. |
| 5 | Christian Yelich | Decline signals | Age 34; EV90 down (108.0 → 104.4) and Whiff% up (.231 → .296) together. |
| 6 | Spencer Torkelson | Trap: low chase isn't automatically good | Rarely chases, but misses a lot in the zone and bottom-tier xBA. |
| 7 | Max Clark | Small sample | Rookie, 206 PA: an early read, must be flagged as tentative. |
| 8 | Wilyer Abreu | Platoon role change | Shielded from lefties in 2024–25, near-average share in 2026. |

## 2. Answer key: what a good report must get right

My read of each hitter, written before looking at any report. The grader checks the report against this.
(First drafts below; rewrite each in my own words.)

1. **Schwarber**: damage over contact. Value comes from xISO and walks; the swing-and-miss is the cost, not a flaw to fix.
2. **Arraez**: contact and bat-to-ball skills carry everything; very little damage. Value depends on batting average.
3. **Alvarez**: complete hitter, average and power. 2025 is a smaller sample and should be treated with care.
4. **Perez**: chases a lot but still does damage when he connects; watch for exit velocity sliding at 36.
5. **Yelich**: two slowing-bat signals moving together at 34; the report must flag it and weigh it for age.
6. **Torkelson**: low chase but high whiff and low xBA, so the problem is missing hittable pitches, not discipline.
7. **Clark**: a contact-first rookie with little power. 206 PA is a real first read (200+ PA), but it is one season, so the report should say so and not call it a trend.
8. **Abreu**: a loft-driven power hitter whose damage comes from launch, not elite exit velocity. Platoon role in earlier seasons, more at-bats vs lefties in 2026; judge by share, not raw PA.

## 3. Scoring checklist

### A. Checked by code (free, automatic, pass/fail)
1. Every number in the report appears in the data packet.
2. 600–800 words (about 750 is right).
3. All sections present, in order (the sections the prompt version asks for).
4. No banned wording: "swing-decision score", "force", "Interpretation:", bullet lists, 20–80 grades, ranks cited as numbers ("127th of 135", "98th percentile").
5. Never mentions the method, its bands or thresholds.
6. "(house model)" label on the first xwOBA, xBA and xSLG.
7. About 20 numbers, not 40: no more than 25 cited (title and Sample notes not counted).
8. Not a stat walk: no more than 15% of sentences open with a metric as the subject ("His EV90 was...").

### B. Checked by an AI grader (pass/fail, with a one-line reason)
1. **Top line is right:** the type and value driver match the answer key.
2. **Every claim is supported** by the packet; nothing from outside knowledge.
3. **Sample sizes handled:** under 100 PA = no read; 100–200 = flagged as tentative.
4. **Platoon judged by share**, not by raw PA against lefties.
5. **Combinations read correctly** (e.g. low chase + high whiff ≠ good discipline).
6. **No filler:** no metric singled out just to say it's average. One sentence saying a whole area is unremarkable is fine; listing several average metrics by name is filler.
7. **Change over time:** decline signals flagged when two or more move together.
8. **Findings connect** into how he drives value (the Synthesis, or How he does damage from v10 on) instead of repeating them.
9. **Reads like a profile, not a stat list:** each sentence makes a point and uses a number or two as evidence.

### C. My own score (the gold standard)
For a handful of reports: "Would I publish this?" 1–5, plus one sentence why.
Used to check that the AI grader agrees with me. If it doesn't, the grader gets fixed, not my judgment.

## 4. How a run works
- Each hitter, 3 reports (24 total), so a score reflects the prompt, not one lucky report.
- Eval reports skip the "reuse a saved report" step and **never publish to the website**.
- Rough cost per full run: ~$4 for reports + ~$1 for grading = **~$5**.
- Output: one scorecard (each check, % passed, per hitter) saved with the date and prompt version, so runs can be compared.
