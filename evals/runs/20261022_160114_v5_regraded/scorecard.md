# Eval scorecard: prompt v5, effort high

2026-10-22 16:30 · 8 hitters × 3 runs = 24 reports · cost $3.94

**Overall: 300/336 checks passed (89%)**

## By check

| Check | Kind | Passed |
|---|---|---|
| numbers_traceable | code | 21/24 |
| length | code | 20/24 |
| sections | code | 24/24 |
| banned_wording | code | 22/24 |
| no_method_talk | code | 24/24 |
| house_model_label | code | 22/24 |
| top_line_right | AI grader | 21/24 |
| claims_supported | AI grader | 8/24 |
| sample_sizes | AI grader | 24/24 |
| platoon_by_share | AI grader | 24/24 |
| combinations_read | AI grader | 23/24 |
| no_filler | AI grader | 19/24 |
| change_over_time | AI grader | 24/24 |
| synthesis_connects | AI grader | 24/24 |

## By hitter

| Hitter | Tests | numbers_traceable | length | sections | banned_wording | no_method_talk | house_model_label | top_line_right | claims_supported | sample_sizes | platoon_by_share | combinations_read | no_filler | change_over_time | synthesis_connects |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kyle Schwarber | Power over contact | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Luis Arraez | Contact / singles | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Yordan Alvarez | Complete hitter | 2/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Salvador Perez | Chaser, aging | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Christian Yelich | Decline signals | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 1/3 | 3/3 | 3/3 | 2/3 | 1/3 | 3/3 | 3/3 |
| Spencer Torkelson | Trap: low chase isn't automatically good | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Max Clark | Small sample | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Wilyer Abreu | Platoon role change | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 |

## Every failure, with the reason

**Kyle Schwarber #1** (kyle-schwarber_1.md, 740 words)
- claims_supported: The report says Pulled Air% "has risen in each of the last three seasons," but the packet says it "rose 2 seasons in a row (2024 → 2026)" and it fell from 30.0% in 2023 to 26.6% in 2024.

**Kyle Schwarber #2** (kyle-schwarber_2.md, 737 words)
- claims_supported: "Has risen each of the last three seasons, from 26.6% in 2024" overstates the packet's "rose 2 seasons in a row" (2023 was 30.0%), and "whiff rate, which has crept up for four straight seasons" contradicts the packet's "flat in 2026" (33.1% both years).

**Kyle Schwarber #3** (kyle-schwarber_3.md, 752 words)
- claims_supported: The report says Pulled Air% "has climbed each of the last three seasons," but the packet's trend column says it "rose 2 seasons in a row (2024 → 2026)" after falling from 30.0% in 2023 to 26.6% in 2024.

**Luis Arraez #1** (luis-arraez_1.md, 779 words)
- claims_supported: Several claims are not supported by the packet: "his exit velocity has drifted down since his 2023 peak" is wrong because EV90 peaked at 99.4 in 2022 and rose in 2026; "produces the least exit velocity in the league" overstates a rank of 133 of 135; and "he rarely reaches deep counts" uses count data the packet does not contain.

**Luis Arraez #2** (luis-arraez_2.md, 745 words)
- numbers_traceable: not in packet: 24%, 30%

**Luis Arraez #3** (luis-arraez_3.md, 792 words)
- numbers_traceable: not in packet: 30%
- house_model_label: first use unlabeled: xBA

**Yordan Alvarez #1** (yordan-alvarez_1.md, 805 words)
- length: 805 words
- claims_supported: "It has been well above the .338 qualified average in every full season" compares every season, including pre-2024 ones, to the 2026 qualified average, even though the packet says seasons before 2024 have no league context and must not be compared with the league.

**Yordan Alvarez #2** (yordan-alvarez_2.md, 757 words)
- numbers_traceable: not in packet: 110

**Yordan Alvarez #3** (yordan-alvarez_3.md, 759 words)
- claims_supported: The Synthesis says "Offspeed pitches off the plate are the one thing he expands for," but the packet shows he also chases breaking balls above the qualified average (32.4% vs 30.1%, 35th percentile), so offspeed is not the only pitch group he expands on.

**Salvador Perez #1** (salvador-perez_1.md, 825 words)
- length: 825 words
- claims_supported: The Synthesis says fastballs are pitches 'he still hits as hard as he has in recent seasons', but fastball EV90 fell to 106.2 from 107.5 and 107.7 and Barrel% fell to 12.1% from 15.2%; 'pitchers rarely have to come into the zone' also cites zone data the packet does not contain.

**Salvador Perez #3** (salvador-perez_3.md, 763 words)
- claims_supported: "That decline showed up mostly against right-handers" has no basis because the packet has no prior-season platoon splits; "historically scattered" launch contradicts his 80th-percentile LA SD in 2024; and "barrel rates in the top quarter" misstates the 73rd percentile on fastballs.

**Christian Yelich #1** (christian-yelich_1.md, 831 words)
- length: 831 words
- claims_supported: The Synthesis says "When the ball came off the bat near the top of the league," but the packet forbids league comparisons before 2024, 2024 has no percentile, and 2025 EV90 was only the 67th percentile, so the claim is unsupported.

**Christian Yelich #2** (christian-yelich_2.md, 820 words)
- length: 820 words
- top_line_right: The Top line calls him "a disciplined ground-ball hitter" whose "main remaining strength is refusing pitches off the plate," and says whiffs "stayed high" without framing the EV drop and whiff rise as a slowing bat or weighing it for age 34, which is the answer key's point.
- claims_supported: "A low-launch profile works when exit velocity is elite, and for most of his career it was" is a league comparison for pre-2024 seasons, which the packet says have no league context.
- combinations_read: It calls low chase paired with a 29.6% Whiff% a strength ("Discipline is still his strength"; "What remains is zone control"), which is the low-chase/high-whiff misread the check names.
- no_filler: "His launch spread is about average" singles out LA SD only to call it average, and "swings at strikes at a league-average rate" does the same for IZ Swing%.

**Christian Yelich #3** (christian-yelich_3.md, 764 words)
- no_filler: The standalone sentence "His walk rate is roughly average." singles out one metric just to say it is average.

**Spencer Torkelson #2** (spencer-torkelson_2.md, 726 words)
- claims_supported: "has slipped each year from 106.2 in 2023" and "EV90 has eroded for three straight seasons" are contradicted by the packet, where EV90 rose from 104.4 to 104.5 in 2025 and the trend column says it "fell in 2026 only."

**Spencer Torkelson #3** (spencer-torkelson_3.md, 773 words)
- claims_supported: "EV90 fell for a second straight drop from his 2023 peak" contradicts the packet: EV90 rose from 104.4 to 104.5 in 2024→2025, and the trend column says "fell in 2026 only"; "has been elevated every season" for breaking share also lacks prior-season league averages to support it.

**Max Clark #1** (max-clark_1.md, 749 words)
- top_line_right: The answer key requires the report to say every read is early and not overstate, but the Top line declares a settled type ('a contact-first, all-fields hitter... a batting-average bat with very little extra-base damage'), and 'In his first MLB look' never flags the read as early or tentative.

**Max Clark #2** (max-clark_2.md, 747 words)
- claims_supported: "pitchers have responded by challenging him in the zone" is not supported, since the packet has no zone-rate data and only shows fastball share (64.6%), and "Pitchers appear to know it" asserts pitcher intent the data cannot show.

**Max Clark #3** (max-clark_3.md, 733 words)
- top_line_right: The answer key's central point is that every read is early, but the Top line flatly asserts 'Clark is a contact-first, all-fields hitter'; 'In his first MLB look' is the only hedge and does not mark the read as early or tentative.
- claims_supported: 'he uses the opposite field more than most' has no league Oppo% in the packet, and 'Pitchers fill the zone with fastballs' implies zone-rate data the packet does not contain.

**Wilyer Abreu #1** (wilyer-abreu_1.md, 768 words)
- banned_wording: "swing decision(s)"
- house_model_label: first use unlabeled: xSLG
- claims_supported: The Synthesis says "Three seasons of falling strikeouts," but the packet's trend column shows K% "fell 2 seasons in a row (2024 → 2026)" after rising from 2023 to 2024.
- no_filler: Plate discipline names several average metrics just to call them average ("IZ Swing%, Chase% and IZ Swing − Chase ... all sit near the qualified mean, as does his Whiff%"), and Expected stats adds "His xBA (house model) sits at the qualified average."

**Wilyer Abreu #2** (wilyer-abreu_2.md, 787 words)
- no_filler: The plate discipline section lists several average metrics by name ("In-zone swing rate, chase rate, Whiff% and IZ Swing − Chase (in-zone swing rate minus chase rate) all sit near the qualified marks") right after already saying the approach is "league average almost across the board," which is filler.

**Wilyer Abreu #3** (wilyer-abreu_3.md, 722 words)
- banned_wording: "swing decision(s)"
- claims_supported: "the third straight season it rose" is wrong: the packet says xwOBA "rose 2 seasons in a row (2024 → 2026)" after falling from .360 in 2023 to .330 in 2024.
- no_filler: "IZ Swing − Chase..., Chase% and Whiff% all sit close to the qualified average" names several average metrics just to call them average.

