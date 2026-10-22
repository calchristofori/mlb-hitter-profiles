# Eval scorecard: prompt v5, effort high

2026-10-22 16:14 · 8 hitters × 3 runs = 24 reports · cost $3.80

**Overall: 303/336 checks passed (90%)**

## By check

| Check | Kind | Passed |
|---|---|---|
| numbers_traceable | code | 21/24 |
| length | code | 20/24 |
| sections | code | 24/24 |
| banned_wording | code | 22/24 |
| no_method_talk | code | 24/24 |
| house_model_label | code | 22/24 |
| top_line_right | AI grader | 20/24 |
| claims_supported | AI grader | 11/24 |
| sample_sizes | AI grader | 24/24 |
| platoon_by_share | AI grader | 24/24 |
| combinations_read | AI grader | 24/24 |
| no_filler | AI grader | 19/24 |
| change_over_time | AI grader | 24/24 |
| synthesis_connects | AI grader | 24/24 |

## By hitter

| Hitter | Tests | numbers_traceable | length | sections | banned_wording | no_method_talk | house_model_label | top_line_right | claims_supported | sample_sizes | platoon_by_share | combinations_read | no_filler | change_over_time | synthesis_connects |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kyle Schwarber | Power over contact | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Luis Arraez | Contact / singles | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Yordan Alvarez | Complete hitter | 2/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Salvador Perez | Chaser, aging | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Christian Yelich | Decline signals | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 |
| Spencer Torkelson | Trap: low chase isn't automatically good | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Max Clark | Small sample | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Wilyer Abreu | Platoon role change | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | 1/3 | 2/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 |

## Every failure, with the reason

**Kyle Schwarber #1** (kyle-schwarber_1.md, 740 words)
- claims_supported: "It has risen in each of the last three seasons" is false: Pulled Air% fell from 30.0% in 2023 to 26.6% in 2024 before rising to 31.1% and 32.2%, so it rose only twice.

**Kyle Schwarber #2** (kyle-schwarber_2.md, 737 words)
- claims_supported: The report says his whiff rate "has crept up for four straight seasons," but the packet shows Whiff% flat from 2025 to 2026 (33.1% to 33.1%, +0.0), and it also asserts that pulled-air power holds "against every pitch group" when no Pulled Air% by pitch group is given.

**Luis Arraez #1** (luis-arraez_1.md, 779 words)
- claims_supported: "he rarely reaches deep counts" relies on count data the packet does not contain, and "The 2026 lift reads as a deliberate attempt to add damage" asserts intent the data cannot show.

**Luis Arraez #2** (luis-arraez_2.md, 745 words)
- numbers_traceable: not in packet: 24%, 30%

**Luis Arraez #3** (luis-arraez_3.md, 792 words)
- numbers_traceable: not in packet: 30%
- house_model_label: first use unlabeled: xBA

**Yordan Alvarez #1** (yordan-alvarez_1.md, 805 words)
- length: 805 words
- claims_supported: "It has been well above the .338 qualified average in every full season" applies the 2026-only qualified average to earlier seasons, and the packet gives no league averages for those years.

**Yordan Alvarez #2** (yordan-alvarez_2.md, 757 words)
- numbers_traceable: not in packet: 110

**Salvador Perez #1** (salvador-perez_1.md, 825 words)
- length: 825 words
- claims_supported: The Synthesis claims fastballs "he still hits as hard as he has in recent seasons," but his fastball EV90 fell from 107.5 to 106.2 and Barrel% from 15.2% to 12.1%; it also says pitchers throw him breaking balls "more than to almost anyone," and the packet gives no rank for pitch share.

**Salvador Perez #2** (salvador-perez_2.md, 755 words)
- claims_supported: The Synthesis says breaking balls are a pitch "which pitchers already feed him more than almost anyone," but the packet gives only his 39.6% share against a 30.5% average, with no rank, so the 'almost anyone' claim is unsupported.

**Salvador Perez #3** (salvador-perez_3.md, 763 words)
- claims_supported: "backed by hard-hit and barrel rates in the top quarter" is wrong because the fastball Barrel% is in the 73rd percentile, and "pitchers already lean on it more than they do against almost anyone" and "That decline showed up mostly against right-handers" have no support in the packet, which gives no pitch-share rank and no prior-season splits.

**Christian Yelich #1** (christian-yelich_1.md, 831 words)
- length: 831 words
- claims_supported: The Synthesis says "When the ball came off the bat near the top of the league," but the packet gives league context only for 2026, so his past league standing comes from outside the data.

**Christian Yelich #2** (christian-yelich_2.md, 820 words)
- length: 820 words
- claims_supported: The Synthesis says "his launch angle and Pulled Air% have barely moved," but Pulled Air% fell from 11.7% to 8.4% (-3.3 pts) from 2024 to 2025, within the same two-season window the report is describing.
- no_filler: "His launch spread is about average" mentions LA SD only to say it is unremarkable.

**Christian Yelich #3** (christian-yelich_3.md, 764 words)
- no_filler: "His walk rate is roughly average." is a standalone mention of a metric only to say it is average.

**Spencer Torkelson #2** (spencer-torkelson_2.md, 726 words)
- claims_supported: The report says EV90 "has slipped each year from 106.2 in 2023" and "has eroded for three straight seasons," but EV90 rose from 104.4 in 2024 to 104.5 in 2025, so the claim contradicts the packet.

**Spencer Torkelson #3** (spencer-torkelson_3.md, 773 words)
- claims_supported: "EV90 fell for a second straight drop from his 2023 peak" is wrong because EV90 rose from 104.4 to 104.5 in 2025, and "unusual at 26" plus breaking share "elevated every season" (no league average is given for 2024–25) go beyond the packet.

**Max Clark #1** (max-clark_1.md, 749 words)
- top_line_right: The answer key says every read is early and must not be overstated, but the Top line flatly declares "Clark is a contact-first, all-fields hitter" and "a batting-average bat." The only hedge, "In his first MLB look," never says the read is tentative.

**Max Clark #2** (max-clark_2.md, 747 words)
- claims_supported: "pitchers have responded by challenging him in the zone" and "Pitchers appear to know it" go beyond the packet: it has no zone-rate data and no evidence of pitcher intent, only the 64.6% fastball share.

**Max Clark #3** (max-clark_3.md, 733 words)
- top_line_right: The answer key requires every read to be framed as early, but the Top line flatly labels him 'a contact-first, all-fields hitter' with 'very little power', and 'In his first MLB look' does not flag the read as tentative.

**Wilyer Abreu #1** (wilyer-abreu_1.md, 768 words)
- banned_wording: "swing decision(s)" (e.g. "His swing decisions are league average")
- house_model_label: first use unlabeled: xSLG
- top_line_right: The Top line calls him "a loft-driven power hitter" whose "value comes from extra-base damage" and never mentions the key's driver, a platoon role in earlier seasons that became more PA against lefties in 2026.
- no_filler: "IZ Swing%, Chase% and IZ Swing − Chase... all sit near the qualified mean, as does his Whiff%" lists metrics only to say they are average.

**Wilyer Abreu #2** (wilyer-abreu_2.md, 787 words)
- no_filler: The Plate discipline section lists "In-zone swing rate, chase rate, Whiff% and IZ Swing − Chase... all sit near the qualified marks," naming metrics only to say they are average.

**Wilyer Abreu #3** (wilyer-abreu_3.md, 722 words)
- banned_wording: "swing decision(s)" (e.g. "His swing decisions are league average")
- top_line_right: The answer key centers on his shift from a platoon role to more at-bats against lefties in 2026, but the Top line ('a fly-ball power hitter who produces value through extra-base damage') never mentions his platoon role or its change.
- claims_supported: 'the third straight season it rose' is wrong: his xwOBA went .360 → .330 → .347 → .354, which is only two straight rises.
- no_filler: 'IZ Swing − Chase ..., Chase% and Whiff% all sit close to the qualified average' lists metrics only to call them average.

