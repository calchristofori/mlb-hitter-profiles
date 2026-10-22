# Eval scorecard: prompt v8, effort high

2026-10-22 17:03 · 8 hitters × 3 runs = 24 reports · cost $6.34

**Overall: 331/384 checks passed (86%)**

## By check

| Check | Kind | Passed |
|---|---|---|
| numbers_traceable | code | 22/24 |
| number_count | code | 21/24 |
| length | code | 5/24 |
| sections | code | 24/24 |
| banned_wording | code | 23/24 |
| no_method_talk | code | 24/24 |
| house_model_label | code | 23/24 |
| top_line_right | AI grader | 21/24 |
| claims_supported | AI grader | 11/24 |
| sample_sizes | AI grader | 22/24 |
| platoon_by_share | AI grader | 24/24 |
| combinations_read | AI grader | 23/24 |
| no_filler | AI grader | 20/24 |
| change_over_time | AI grader | 24/24 |
| reads_like_profile | AI grader | 20/24 |
| synthesis_connects | AI grader | 24/24 |

## By hitter

| Hitter | Tests | numbers_traceable | number_count | length | sections | banned_wording | no_method_talk | house_model_label | top_line_right | claims_supported | sample_sizes | platoon_by_share | combinations_read | no_filler | change_over_time | reads_like_profile | synthesis_connects |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kyle Schwarber | Power over contact | 3/3 | 2/3 | 1/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 |
| Luis Arraez | Contact / singles | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Yordan Alvarez | Complete hitter | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Salvador Perez | Chaser, aging | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| Christian Yelich | Decline signals | 3/3 | 2/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Spencer Torkelson | Trap: low chase isn't automatically good | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 |
| Max Clark | Small sample | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 2/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 |
| Wilyer Abreu | Platoon role change | 3/3 | 2/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 |

## Every failure, with the reason

**Kyle Schwarber #1** (kyle-schwarber_1.md, 770 words)
- number_count: 27 numbers
- banned_wording: scouting grades

**Kyle Schwarber #2** (kyle-schwarber_2.md, 851 words)
- length: 851 words
- claims_supported: "He still posts an above-average xwOBA against breaking balls when he makes contact" misstates the packet, because the .321 breaking-ball xwOBA counts every PA ending on that group, strikeouts included, not just contact.

**Kyle Schwarber #3** (kyle-schwarber_3.md, 823 words)
- length: 823 words
- reads_like_profile: Several passages walk through numbers one after another, such as the plate discipline run "His Whiff% of 33.1%... His K% climbed to 31.4%... His BB% of 15.0%... His Chase% has risen" and the stacked "His EV90, Hard-hit% and Barrel% all fell from 2025, and his strikeout rate rose."

**Luis Arraez #1** (luis-arraez_1.md, 825 words)
- length: 825 words

**Luis Arraez #2** (luis-arraez_2.md, 903 words)
- length: 903 words
- claims_supported: The Synthesis says he has "the tightest launch in the league", but the packet ranks his LA SD 3 of 135, not first (the batted-ball section correctly says "third-tightest").

**Luis Arraez #3** (luis-arraez_3.md, 807 words)
- length: 807 words
- claims_supported: "He swings often" and "He swings freely" are not supported, since the packet gives no overall swing rate and shows IZ Swing% below average (63.5% vs 66.8%); "he rarely works deep counts" also relies on count data not in the packet.

**Yordan Alvarez #1** (yordan-alvarez_1.md, 843 words)
- length: 843 words

**Yordan Alvarez #2** (yordan-alvarez_2.md, 803 words)
- length: 803 words
- claims_supported: The Synthesis says he "rarely chases" and the Top line says he takes "almost everything else," but his 27.7% Chase% ranks only 51 of 135 (63rd percentile), and the report itself earlier calls it "slightly better than average."

**Yordan Alvarez #3** (yordan-alvarez_3.md, 864 words)
- length: 864 words
- claims_supported: "A ground-ball-heavy approach against lefties" contradicts the packet, where his 37.2% GB% vs LHP is still below the 41.0% qualified average.
- sample_sizes: "his EV90 on them has fallen two seasons in a row" reads the 2025 offspeed EV90, which rests on only 30 PA ending, a sample under 50 PA that should get no read.

**Salvador Perez #1** (salvador-perez_1.md, 853 words)
- length: 853 words
- no_filler: "His xBA (house model) sits right at league average" is a standalone sentence that singles out one metric only to call it average.

**Salvador Perez #2** (salvador-perez_2.md, 827 words)
- numbers_traceable: not in packet: 25
- length: 827 words
- claims_supported: "His xBA (house model) is league-average, so the drop came from power" is not supported: xBA also fell from .277 (82nd pctl) to .253 (49th), so part of the xwOBA drop came from xBA, not power alone.

**Salvador Perez #3** (salvador-perez_3.md, 778 words)
- claims_supported: "Pitchers have adjusted" claims a change in how he was pitched, but his breaking-ball share was 39.3% in 2024, 37.1% in 2025 and 39.6% in 2026, so the packet shows no clear adjustment; "has always come from" also reaches beyond the three seasons in the packet.

**Christian Yelich #1** (christian-yelich_1.md, 831 words)
- length: 831 words

**Christian Yelich #2** (christian-yelich_2.md, 835 words)
- length: 835 words
- top_line_right: The Top line frames him as "a disciplined ground-ball hitter" whose value rests on "laying off pitches" and only notes that "his exit velocity fell and his miss rate stayed high", without naming the slowing bat at 34 that the answer key makes the headline.
- claims_supported: The Synthesis says "His launch angle and pull tendency have held steady over the same span", but the packet shows Pulled Air% falling from 11.7% to 8.4% and Pull% swinging -8.5 then +4.0 points over that span.
- combinations_read: Despite a 29.6% Whiff% well above average, the report labels him "a disciplined ground-ball hitter" and says "His approach at the plate is intact", reading low chase with high whiff as good discipline.

**Christian Yelich #3** (christian-yelich_3.md, 861 words)
- number_count: 28 numbers
- length: 861 words

**Spencer Torkelson #1** (spencer-torkelson_1.md, 877 words)
- length: 877 words
- house_model_label: first use unlabeled: xSLG

**Spencer Torkelson #2** (spencer-torkelson_2.md, 791 words)
- claims_supported: "Since 2025 his share has been at or above theirs" is false for 2026, when his 29.2% share vs LHP was below the 31.0% same-handed average.
- reads_like_profile: "His .248 xwOBA on them is in the bottom tenth, his 41.8% Whiff% is near the bottom, and the breaking-ball xwOBA has fallen two seasons in a row" strings stats one after another rather than making a point with one or two numbers.

**Spencer Torkelson #3** (spencer-torkelson_3.md, 833 words)
- length: 833 words
- claims_supported: "he gets no infield hits to cushion the strikeouts" is a factual claim about infield hits, and the packet has no infield-hit data, so it goes beyond what the packet supports.

**Max Clark #1** (max-clark_1.md, 766 words)
- numbers_traceable: not in packet: 200
- claims_supported: "Detroit used him as an everyday player" is not supported by a 206-PA season, and "Pitchers are not afraid to throw him strikes" asserts a zone-rate fact that the packet does not contain.
- sample_sizes: The report says the 67 PA vs LHP are "too few for any read" but then concludes "the overall picture is the same low-power hitter on both sides," which reads the sub-100 PA lefty split anyway.

**Max Clark #2** (max-clark_2.md, 805 words)
- length: 805 words
- top_line_right: The answer key requires the report to say every read is early, but the Top line states the profile flatly ("bat-to-ball skill and above-average speed carry his offense") and only mentions "his first 206 MLB plate appearances" without calling the read tentative or early.
- no_filler: Several metrics are singled out only to call them average: "His BB% is a touch below average" and "Against breaking balls, his whiff rate is average."

**Max Clark #3** (max-clark_3.md, 723 words)
- top_line_right: The answer key's main point is that every read is early, but the Top line states a firm type and driver ("contact-first, all-fields line-drive hitter... value came almost entirely from batting average") and only says "In his first MLB season," without flagging the profile as tentative.
- claims_supported: The line "a hitter who barrels the ball on a line to all fields" contradicts the packet's 2.1% Barrel%, which the report itself calls "a fraction of the qualified average."
- no_filler: It singles out average metrics with no point attached, in "His launch angle and its spread are close to league norms" and "His walk rate sits just under average."

**Wilyer Abreu #1** (wilyer-abreu_1.md, 829 words)
- length: 829 words
- claims_supported: "Spin feeds that profile, which is why pitchers have largely stopped throwing it to him" asserts a cause and a decline the packet does not show, since breaking share actually rose in 2026 (22.5% to 24.2%) and no pitcher intent is in the data.
- reads_like_profile: "His K% has fallen two seasons in a row, from 28.0% to 20.7%, and his BB% has climbed two seasons in a row to 10.4%" strings two stats and three numbers together in one sentence, which reads as a walk through numbers.

**Wilyer Abreu #2** (wilyer-abreu_2.md, 848 words)
- length: 848 words
- no_filler: The plate-discipline section names several average metrics one by one ("chases at roughly league-average rates," "IZ Swing − Chase... lands near average," "His Whiff% is also average") instead of one summary sentence.

**Wilyer Abreu #3** (wilyer-abreu_3.md, 836 words)
- number_count: 27 numbers
- length: 836 words
- reads_like_profile: Several sentences walk through stats in sequence, e.g. "His K% has fallen two seasons in a row, from 28.0% in 2024 to 20.7%, and his 10.4% BB% is above average..." and "His 23.7% fastball Whiff% is in the bottom quarter..., his fastball xwOBA is slightly below average, and his fastball Chase% has risen two seasons in a row."

