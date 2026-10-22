# Eval scorecard: prompt v7, effort high

2026-10-22 16:52 · 8 hitters × 3 runs = 24 reports · cost $6.72

**Overall: 323/384 checks passed (84%)**

## By check

| Check | Kind | Passed |
|---|---|---|
| numbers_traceable | code | 23/24 |
| number_count | code | 15/24 |
| length | code | 7/24 |
| sections | code | 24/24 |
| banned_wording | code | 22/24 |
| no_method_talk | code | 24/24 |
| house_model_label | code | 22/24 |
| top_line_right | AI grader | 18/24 |
| claims_supported | AI grader | 16/24 |
| sample_sizes | AI grader | 23/24 |
| platoon_by_share | AI grader | 24/24 |
| combinations_read | AI grader | 22/24 |
| no_filler | AI grader | 17/24 |
| change_over_time | AI grader | 24/24 |
| reads_like_profile | AI grader | 18/24 |
| synthesis_connects | AI grader | 24/24 |

## By hitter

| Hitter | Tests | numbers_traceable | number_count | length | sections | banned_wording | no_method_talk | house_model_label | top_line_right | claims_supported | sample_sizes | platoon_by_share | combinations_read | no_filler | change_over_time | reads_like_profile | synthesis_connects |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kyle Schwarber | Power over contact | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Luis Arraez | Contact / singles | 2/3 | 2/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 |
| Yordan Alvarez | Complete hitter | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Salvador Perez | Chaser, aging | 3/3 | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 |
| Christian Yelich | Decline signals | 3/3 | 1/3 | 0/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | 2/3 | 3/3 |
| Spencer Torkelson | Trap: low chase isn't automatically good | 3/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Max Clark | Small sample | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 0/3 | 1/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | 3/3 |
| Wilyer Abreu | Platoon role change | 3/3 | 2/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 1/3 | 3/3 |

## Every failure, with the reason

**Kyle Schwarber #2** (kyle-schwarber_2.md, 859 words)
- length: 859 words

**Kyle Schwarber #3** (kyle-schwarber_3.md, 812 words)
- length: 812 words

**Luis Arraez #1** (luis-arraez_1.md, 808 words)
- length: 808 words
- claims_supported: The Synthesis says "Fastballs, especially from left-handers, let pitchers fill the zone... and invite weak, grounded contact," but the packet has no fastball-by-pitcher-hand split and no fastball ground-ball data.
- reads_like_profile: The batted-ball section strings metrics together one after another: "His LA median climbed to 16.0, his fly balls rose and his grounders fell, and his Pulled Air%... reached a career high but stayed below the qualified average."

**Luis Arraez #2** (luis-arraez_2.md, 786 words)
- reads_like_profile: Some sentences walk through metrics one after another, such as "His median launch angle climbed to 16.0 from 13.0, his ground-ball rate fell below average, and Pulled Air%... reached a career high while staying below the league average," and the Expected stats section steps through xwOBA, xBA, xISO and xSLG in sequence.

**Luis Arraez #3** (luis-arraez_3.md, 878 words)
- numbers_traceable: not in packet: 20
- number_count: 26 numbers
- length: 878 words
- claims_supported: "yet he sees almost none of them" misstates a 23.5% breaking-ball share, and "Pitchers have adjusted to him" implies a change the data does not show, since his fastball share was flat at 64.7% to 65.9% to 65.7%.

**Yordan Alvarez #1** (yordan-alvarez_1.md, 860 words)
- length: 860 words

**Yordan Alvarez #2** (yordan-alvarez_2.md, 851 words)
- length: 851 words
- house_model_label: first use unlabeled: xSLG

**Yordan Alvarez #3** (yordan-alvarez_3.md, 818 words)
- length: 818 words
- sample_sizes: The 184-PA vs-LHP split is read with full confidence in the platoon section ("Against lefties he is a lesser version of himself... His results there also lagged his contact"), and the only tentative flag is tucked into the Sample notes.

**Salvador Perez #1** (salvador-perez_1.md, 822 words)
- number_count: 32 numbers
- length: 822 words
- house_model_label: first use unlabeled: xBA, xSLG
- claims_supported: "the 2026 slide shows up mainly against right-handers" is unsupported because the packet has platoon splits only for 2026, so no year-over-year split comparison is possible.
- no_filler: "His xBA was dead average." singles out a metric only to say it is average and makes no further point.

**Salvador Perez #2** (salvador-perez_2.md, 809 words)
- number_count: 26 numbers
- length: 809 words

**Salvador Perez #3** (salvador-perez_3.md, 818 words)
- number_count: 33 numbers
- length: 818 words
- claims_supported: The platoon section says righties are "where the 2026 decline concentrates" and "righties are now handling him," but the packet has 2026 splits only, so no change by pitcher hand can be shown.
- no_filler: "His xBA (house model) sits right at league average" is a standalone sentence singling out one metric only to say it is average.

**Christian Yelich #1** (christian-yelich_1.md, 856 words)
- length: 856 words
- combinations_read: The report pairs a 23.3% chase rate with a 29.6% whiff rate and still calls it good discipline ("The approach still works," "plate discipline as the skill still holding up"), which is exactly the low-chase/high-whiff misread the check names.

**Christian Yelich #2** (christian-yelich_2.md, 889 words)
- number_count: 30 numbers
- length: 889 words
- banned_wording: bullet list
- top_line_right: The Top line says exit velocity 'slipped to league average while his swing-and-miss stayed high', but it never frames this as a slowing bat or weighs it for his age, which is the answer key's core finding; that framing appears only in the Synthesis.
- claims_supported: 'Even in the flatter years since, hard contact and walks kept him above average' compares 2020–2023 seasons with the league, which the packet says cannot be done before 2024; 'pull tendency [is] essentially unchanged' also glosses over Pull% moving 46.9→38.4→42.4 and Pulled Air% falling from 11.7% to 8.7%.
- reads_like_profile: Several sentences string numbers together, e.g. 'fell for a second straight season, from .375 in 2024 to .315, below the qualified average of .338' and 'a .293 xwOBA against lefties (tentative, 130 PA) and .322 against righties.'

**Christian Yelich #3** (christian-yelich_3.md, 813 words)
- number_count: 27 numbers
- length: 813 words
- no_filler: 'He sprays the ball to all fields at a roughly average pull rate, and his launch spread is ordinary' singles out Pull% and LA SD by name only to say they are average.

**Spencer Torkelson #1** (spencer-torkelson_1.md, 837 words)
- number_count: 27 numbers
- length: 837 words
- top_line_right: The Top line casts him as "a launch-angle slugger" whose value comes from pulled air and barrels, while the key's thesis is a contact problem (low chase, high whiff, low xBA, missing hittable pitches); the Top line never mentions low xBA or says the problem is not discipline.
- claims_supported: The Synthesis says his approach will "leave him behind in counts, where spin and changeups beat him," but the packet has no count data, so this claim goes beyond it.

**Spencer Torkelson #2** (spencer-torkelson_2.md, 799 words)
- top_line_right: The Top line casts him as "a lift-and-pull power hitter who gets to damage through launch angle" and only notes a "rise in swing-and-miss"; it never names the answer key's core read that low chase with high whiff and low xBA means he is missing hittable pitches.
- combinations_read: It says his EV90 "reads as hard-hit and barrel rates that come from angle more than raw exit velocity," but Hard-hit% is defined purely by exit velocity and cannot come from launch angle, so this is a misread even though the chase/whiff reading is correct.

**Spencer Torkelson #3** (spencer-torkelson_3.md, 849 words)
- number_count: 26 numbers
- length: 849 words

**Max Clark #1** (max-clark_1.md, 745 words)
- top_line_right: The answer key's point is that every read is early, but the Top line flatly asserts "Clark is a contact-and-speed hitter" and that "his value came almost entirely through batting average" without flagging that this rests on one 206-PA season.
- claims_supported: The Synthesis says his contact strength "showed up against every pitch group in his swing data," but his breaking-ball Whiff% of 30.4% is slightly worse than the 30.2% qualified average, so that claim is not supported by the packet.
- no_filler: It names several average metrics one by one, including "His median launch angle sits close to average," "chasing at a roughly average rate," and "His walk rate is a bit below average," without these making a distinct point.
- reads_like_profile: Sentences string stats together, such as "his Whiff% of 10.8% reflects excellent contact, but his xwOBA, Hard-hit% and a Barrel% of 1.1% all trail the average badly," and the launch-angle sentence that walks through median, spread and Sweet spot% in turn.

**Max Clark #2** (max-clark_2.md, 794 words)
- banned_wording: scouting grades
- top_line_right: The answer key's main point is that every read is early, but the Top line flatly labels him a "contact-first, all-fields line-drive hitter" whose line "grades below average," and the soft "for now" does not say the sample is early.
- claims_supported: The packet has no zone-rate data, so the claim that pitchers "challenge him in the zone with heavy fastball usage rather than working around him" is unsupported, and the general line that fastballs are "the pitch most hitters miss least but rarely hit softly" comes from outside knowledge.
- no_filler: "His median launch angle is near average, his launch spread is slightly tighter than average" and "His walk rate is slightly below average" single out individual metrics just to call them about average.

**Max Clark #3** (max-clark_3.md, 773 words)
- top_line_right: The answer key's top line is that every read is early, but the Top line states a settled type ('a contact-first, all-fields hitter whose value rests on making contact') and only says 'In his first big-league season' without flagging the read as early or tentative.

**Wilyer Abreu #1** (wilyer-abreu_1.md, 894 words)
- length: 894 words
- no_filler: The plate discipline section names several average metrics one by one, "chases at an average rate. His IZ Swing − Chase... and his whiff rate both land near the middle," instead of dismissing the area in one sentence.
- reads_like_profile: Several sentences string stats together, e.g. "His fastball Whiff% of 23.7% is in the bottom quarter..., his chase rate against fastballs has climbed two straight seasons, and his xwOBA on them is slightly below average."

**Wilyer Abreu #2** (wilyer-abreu_2.md, 846 words)
- number_count: 28 numbers
- length: 846 words
- reads_like_profile: Several sentences string stats together, e.g. "His K% has fallen two seasons in a row, from 28.0% in 2024 to 20.7%, as his Whiff% came down from 29.6%" (three numbers) and the fastball sentence chaining whiff rate, chase rate and xwOBA one after another.

**Wilyer Abreu #3** (wilyer-abreu_3.md, 799 words)
- no_filler: After saying "His swing rates are average," the discipline section singles out more average metrics by name: IZ Swing − Chase "lands mid-pack" and Chase% "remains average."

