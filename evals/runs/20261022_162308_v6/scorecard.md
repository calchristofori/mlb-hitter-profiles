# Eval scorecard: prompt v6, effort high

2026-10-22 16:30 · 8 hitters × 3 runs = 24 reports · cost $6.38

**Overall: 282/336 checks passed (84%)**

## By check

| Check | Kind | Passed |
|---|---|---|
| numbers_traceable | code | 18/24 |
| length | code | 0/24 |
| sections | code | 24/24 |
| banned_wording | code | 23/24 |
| no_method_talk | code | 23/24 |
| house_model_label | code | 22/24 |
| top_line_right | AI grader | 20/24 |
| claims_supported | AI grader | 16/24 |
| sample_sizes | AI grader | 23/24 |
| platoon_by_share | AI grader | 24/24 |
| combinations_read | AI grader | 22/24 |
| no_filler | AI grader | 19/24 |
| change_over_time | AI grader | 24/24 |
| synthesis_connects | AI grader | 24/24 |

## By hitter

| Hitter | Tests | numbers_traceable | length | sections | banned_wording | no_method_talk | house_model_label | top_line_right | claims_supported | sample_sizes | platoon_by_share | combinations_read | no_filler | change_over_time | synthesis_connects |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kyle Schwarber | Power over contact | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Luis Arraez | Contact / singles | 2/3 | 0/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Yordan Alvarez | Complete hitter | 2/3 | 0/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| Salvador Perez | Chaser, aging | 1/3 | 0/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| Christian Yelich | Decline signals | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 1/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| Spencer Torkelson | Trap: low chase isn't automatically good | 1/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Max Clark | Small sample | 3/3 | 0/3 | 3/3 | 3/3 | 2/3 | 3/3 | 0/3 | 1/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| Wilyer Abreu | Platoon role change | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 |

## Every failure, with the reason

**Kyle Schwarber #1** (kyle-schwarber_1.md, 873 words)
- length: 873 words
- claims_supported: "He misses more than almost anyone, on every pitch group" overstates the packet, where his fastball Whiff% ranks 112 of 135 (17th percentile); "has climbed each of the last three seasons" for breaking share also overstates three data points (31.6%, 37.0%, 37.9%), which show only two increases.

**Kyle Schwarber #2** (kyle-schwarber_2.md, 919 words)
- length: 919 words

**Kyle Schwarber #3** (kyle-schwarber_3.md, 873 words)
- length: 873 words

**Luis Arraez #1** (luis-arraez_1.md, 895 words)
- numbers_traceable: not in packet: 30%
- length: 895 words

**Luis Arraez #2** (luis-arraez_2.md, 900 words)
- length: 900 words

**Luis Arraez #3** (luis-arraez_3.md, 977 words)
- length: 977 words
- banned_wording: bullet list

**Yordan Alvarez #1** (yordan-alvarez_1.md, 987 words)
- numbers_traceable: not in packet: 110
- length: 987 words
- claims_supported: "offspeed pitches off the plate" and "offspeed stuff below the zone" make pitch-location claims the packet cannot support, since it has only zone and chase rates with no location data.

**Yordan Alvarez #2** (yordan-alvarez_2.md, 959 words)
- length: 959 words
- claims_supported: "The fewer swings in the zone drive that decline, not more chasing" is contradicted by the packet: from 2022 to 2026 IZ Swing% fell only 1.2 points (63.7% to 62.5%) while Chase% rose 2.9 points (24.8% to 27.7%), so more chasing drove most of the decline.
- combinations_read: The report misreads the IZ Swing% and Chase% components of the falling IZ Swing − Chase, saying it "reflects fewer swings at strikes rather than more chasing" when rising Chase% is the larger contributor.

**Yordan Alvarez #3** (yordan-alvarez_3.md, 951 words)
- length: 951 words
- house_model_label: first use unlabeled: xSLG

**Salvador Perez #1** (salvador-perez_1.md, 860 words)
- length: 860 words
- house_model_label: first use unlabeled: xSLG
- sample_sizes: The report says "Offspeed results are too thin to read" and the Sample notes say "offspeed results (83 PA ending) are no read," but 83 PA ending is above the 50-PA threshold, so the sample rule is misapplied (the 176-PA lefty split is correctly flagged as tentative).

**Salvador Perez #2** (salvador-perez_2.md, 942 words)
- numbers_traceable: not in packet: 15, 600
- length: 942 words
- claims_supported: The report says his "breaking-ball Chase% ranked dead last," but the packet shows 133 of 135, and it says fastball "Hard-hit% and Barrel% in the top quarter" when Barrel% is at the 73rd percentile.

**Salvador Perez #3** (salvador-perez_3.md, 863 words)
- numbers_traceable: not in packet: 600
- length: 863 words
- no_filler: "His xBA (house model) of .253 is league average" singles out a metric only to say it is average, adding nothing to the argument.

**Christian Yelich #1** (christian-yelich_1.md, 904 words)
- length: 904 words
- claims_supported: The Synthesis says his offense "has always been built on ... well-above-average exit velocity," which compares pre-2024 seasons with the league even though the packet gives no league context before 2024.
- combinations_read: The Top line calls him "well-disciplined" despite a 29.6% Whiff%, and the batted-ball section calls it "real exit velocity spent on the ground" with "xISO lags his exit velocity" when EV90 (104.4) is at the league average, so there is no high-EV/low-xISO gap to read.

**Christian Yelich #2** (christian-yelich_2.md, 910 words)
- length: 910 words
- top_line_right: The Top line says 'that exit velocity faded to league average and his whiffs stayed high, so his patience no longer covers the gap'. It frames him as 'a selective, ground-ball hitter' but never names the slowing bat at 34 or weighs it for age, which is the answer key's driver.

**Christian Yelich #3** (christian-yelich_3.md, 909 words)
- length: 909 words
- claims_supported: "His fastball whiff rate has risen in each of the last three seasons" overstates the packet, which has only 2024-2026 pitch-group rows (15.3% → 21.6% → 23.3%), so there are two rises and no evidence of a rise into 2024.

**Spencer Torkelson #1** (spencer-torkelson_1.md, 885 words)
- numbers_traceable: not in packet: 5%
- length: 885 words

**Spencer Torkelson #2** (spencer-torkelson_2.md, 928 words)
- numbers_traceable: not in packet: 10%, 5%
- length: 928 words

**Spencer Torkelson #3** (spencer-torkelson_3.md, 873 words)
- length: 873 words

**Max Clark #1** (max-clark_1.md, 907 words)
- length: 907 words
- top_line_right: The answer key's point is that every read is early, but the Top line flatly labels him 'a contact-first, all-fields hitter whose bat-to-ball skill and above-average speed carry a batting-average profile' and only notes 'his first 206 big-league plate appearances' without calling the read early or tentative.

**Max Clark #2** (max-clark_2.md, 862 words)
- length: 862 words
- no_method_talk: "threshold"
- top_line_right: The answer key requires every read to be framed as early, but the Top line states flatly that "his value came from batting average" and that he is "a contact-first hitter"; only "In his first 206 big-league PA" hints at sample size, and it never says the read is tentative.
- claims_supported: "leave his xISO among the weakest marks you will see for an everyday outfielder" makes a positional comparison the packet does not support, since no rank or percentile is given and there is no outfielder comparison group.

**Max Clark #3** (max-clark_3.md, 911 words)
- length: 911 words
- top_line_right: The answer key requires the report to say every read is early, but the Top line states a settled type as fact ("Clark is a contact-first, all-fields hitter... his value came almost entirely through batting average"), and the only nod to sample size is "In his first 206 MLB plate appearances."
- claims_supported: "a hitter who squares the ball up" is not supported by the packet, which shows Hard-hit% of 38.0% (vs 41.0% average) and Barrel% of 2.1% (vs 8.3%).
- no_filler: The batted-ball section lists several average metrics by name: "His median launch angle sits near the league average, his launch spread is slightly tighter than average, his Sweet spot% is a touch above average."

**Wilyer Abreu #1** (wilyer-abreu_1.md, 974 words)
- length: 974 words
- no_filler: After saying discipline was "league average almost across the board," the plate discipline section names average metrics one by one: "IZ Swing − Chase... sits in the 54th percentile, and his whiff rate is near average," plus Chase% that "remains only average."

**Wilyer Abreu #2** (wilyer-abreu_2.md, 899 words)
- length: 899 words
- no_filler: The plate discipline section names several average metrics: "in-zone swing rate, chase rate and whiff rate all sat near the qualified average," which is listing average metrics by name rather than one summary of the area.

**Wilyer Abreu #3** (wilyer-abreu_3.md, 861 words)
- length: 861 words
- no_filler: The Plate discipline section names several average metrics: "His in-zone swing rate, Chase% and IZ Swing − Chase... all sit near the qualified average," then adds "BB% is a tick above average" and Chase% "still sits at the league average."

