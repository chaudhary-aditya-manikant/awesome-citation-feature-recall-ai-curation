# Five-minute demonstration and viva preparation

All numbers below come from files in `results/`. Rehearse aloud at least twice and time it. Explain the answers in your own words; don't read them out.

## The story in four sentences

1. My review found that screening tools report recall for the whole collection, never split by how cited the papers are.
2. **Study 1 (pilot):** on my own 2,790-record pool, removing the citation feature kept 7 of 7 rarely cited relevant papers in the top 20% against 3 of 7, but 7 papers is too few, so my own data rule failed and I reported it as exploratory.
3. **Study 2 (confirmatory):** I pre-registered the same hypothesis again and tested it on SYNERGY, 20 systematic reviews with human labels. The rule passed (977 rarely cited relevant papers) and the hypothesis was supported: 742 against 691 of 977, a difference of 5.2 points (95% interval 3.3 to 6.8).
4. The effect is real but about ten times smaller than the pilot suggested, and the citation feature does not lower overall recall: it moves recall from rarely cited to highly cited papers, which a whole-collection figure cannot show.

## Demonstration script (about 5 minutes)

| Time | Show | Say (in your own words) |
|---|---|---|
| 0:00–0:40 | `research_brief.md` | The gap from my review and the question: does a citation feature push relevant but rarely cited papers out of the top of the queue? |
| 0:40–1:20 | `configs/frozen_protocol.json`, `PREREGISTRATION_v2.md` | One change only: two identical TF-IDF + logistic-regression rankers, one with log(1 + citations). Grouped folds. Recall@20% for the lower half of age-adjusted citation rate. Rules fixed before the data: a gate of 20 in Study 1, and 50 per group in Study 2. |
| 1:20–2:30 | Terminal (start it at 0:00 so it finishes in time): `python scripts/viva_demo.py --skip-tests --data data/private/model_input_reviewed_20261105_private.csv` | It refits both Study 1 rankers, re-runs the reference rankers, and rebuilds the Study 2 table from the saved scores for 150,154 records. It checks everything against the committed results and ends with "identical: True" (about 2 minutes on the laptop without the tests; about 4 with them). Explain the design while it runs. |
| 2:30–3:15 | Figure 1, Table 2 (Study 1) | The gate failed: 7 of 64 relevant papers were rarely cited. 7/7 against 3/7, difference 0.57, interval 0.14 to 1.00. Exploratory. My blind spot-check of 200 AI labels found 3 missed relevant papers, all uncited. |
| 3:15–4:20 | Table 4, Figure 3 (Study 2) | New pre-registration, new data. Gate passed: 977 and 1,768. 742 against 691 of 977: +5.2 points, interval excludes zero. Overall recall unchanged, because highly cited papers gained what rarely cited ones lost. Better in 14 reviews, equal in 4, worse in 1. The fair re-rank recovers 8.1 points at almost no precision cost. |
| 4:20–5:00 | `ai_assistance_log.md` §3–§4 | AI wrote most of the code and drafts. I chose the question and design, reviewed 458 + 200 labels, set and justified every Study 2 rule before the data, and ran everything. AI errors I had to catch: wrong bootstrap unit, the meaningless [1, 1] interval, the wrong SYNERGY version. |

**Shorter version (no private data, about 1 minute):** `python scripts/viva_demo.py` runs the tests, the reference rankers and the Study 2 table.

**Before the viva:** open Git Bash in the project folder and activate the project environment with `source ~/aitr_env/Scripts/activate` (you should see `(aitr_env)`). Without it the laptop's older libraries are used and the Study 1 interval comes out slightly different. Run the 58 tests once beforehand (`python -m pytest -q tests`, about 100 s) so you can say they pass, then use `--skip-tests` in the live demo.

**Backup if the live run fails:** open `results/study2_confirmatory/study2_pooled_metrics.csv`, `results/run_20261105_reviewed_crossfit/crossfit_pooled_metrics.csv` and the figures in `paper/`.

## Likely viva questions

**Design**
1. *Why change only one feature?* So that any difference between the two rankers can only come from the citation feature. That makes it an ablation, not a comparison of two systems.
2. *Why TF-IDF + logistic regression, not a neural model?* Transparent, fast on a CPU, standard in screening research (e.g. ASReview). The question is about the feature, not the strongest model.
3. *Why grouped folds?* Versions of the same paper share words. If one is in training and one in test, the test is too easy (leakage).
4. *Why Recall@20% and not accuracy?* In screening, people read the top of the queue and stop. With about 2% relevant, accuracy is meaningless.
5. *Why an age-adjusted citation rate?* A new paper has had no time to be cited. Dividing by years since publication stops "new" being confused with "ignored".
6. *Why a cluster bootstrap?* Records in a group are not independent. Resampling groups, paired across rankers, gives an honest interval. The AI's first version resampled records; I corrected it.

**Study 1**
7. *Your gate failed. Why keep Study 1?* It is the pilot. It showed the measurement works and which direction to test, and it showed how much data a real test needs. I report it as exploratory.
8. *Why not lower the gate to 7?* Changing the rule after seeing the data is p-hacking.
9. *What is the collection confound?* 46 of 64 relevant papers came from citation neighbourhoods of 5 seed papers, a route that finds well-cited papers by construction.
10. *Who labelled Study 1?* AI first pass on 2,763 records; I reviewed all 458 relevant, uncertain and boundary records (15 changed, κ = 0.88) and then a blind random 200 of the rest (190 agreed, 3 relevant missed, 7 uncertain). 2,105 keep the AI label; estimated about 35 relevant papers missed among them.

**Study 2**
11. *Why a second study instead of fixing the first?* Re-analysing data whose result I had already seen would not be a test. New data under rules fixed in advance is.
12. *What exactly was pre-registered?* H1 (blind beats aware on lower-citation Recall@20%), H2 (the fair re-rank), the gate of 50 per group, reviews with at least 20 inclusions, reserved share 0.5, precision limit 0.05, same model and seeds. All in `PREREGISTRATION_v2.md`, written before download.
13. *Why 50 for the gate?* (Your own reason from the pre-registration: 20 was the pilot's rule and the pilot still had too little evidence, so the confirmatory test needed a larger base.)
14. *You deviated from the pre-registration. Explain.* Twice, both before any result. The download tool's default had changed to SYNERGY+, so I selected the original SYNERGY that I had named. And OpenAlex's rate limit stopped the live citation download twice at 90,100 records, so I used the citation counts stored in SYNERGY. Both are written up with dates.
15. *The effect is only 5 points. Does it matter?* It is 51 more relevant papers found among 977 at the same reading effort, with no loss in overall recall or precision. Small, but free. And it shows why overall recall hides the problem.
16. *Why is it so much smaller than Study 1?* Seven records cannot estimate a size; the pilot's interval ran from 0.14 to 1.00. Also the pilot pool was built through citation links, which exaggerates the citation advantage of relevant papers.
17. *Is it consistent?* Mostly: 14 reviews better, 4 equal, 1 worse (Moran 2021). The largest review (Walker 2018, 360 of the 977) shows no difference; without it the pooled difference is 0.083. I don't know why that review differs.
18. *SYNERGY is medical. Your title says AI literature curation.* Study 1 is the AI-curation pool. Study 2 confirms the mechanism for screening in general; two of its reviews are software engineering (Hall 2012: 9/9 against 7/9). I state this as a limit on external validity.
19. *Citation counts were taken after the reviews. Problem?* Yes, a stated threat: older papers had longer to be cited, and a paper may be cited because a review included it. Both make relevant papers look more cited than they were at screening time.
20. *Is the citation-only result meaningful?* Only as a reference point. Zero of 977 is nearly true by construction, because the lower-citation group is defined by what that ranker sorts on.

**AI use**
21. *What did the AI get wrong?* Pilot labels too broad; record-level bootstrap; wrong grouping column; the [1, 1] interval; 3 missed relevant papers in my spot-check; in Study 2, the wrong SYNERGY version, id detection that failed twice on real data, and no handling of the rate limit.
22. *What was your own contribution?* Be specific: the gap and single-feature design, running all collection, 458 + 200 label reviews, reporting Study 1 as exploratory, deciding to run Study 2, every pre-registered value and reason, running Study 2, accepting the deviation.
23. *What next?* A second model family, citation counts as of each review's date, a full review of the 2,105 AI-only labels, and a labelled AI-literature pool large enough to pass the gate.

**Rerun on request**
- All tests: `python -m pytest -q tests`
- Study 2 table from saved scores: `cd src && python study2_verify_from_scores.py --results ../results/study2_confirmatory --protocol ../configs/study2_protocol.json`
- Study 1 full pipeline (needs the private input): `bash scripts/run_all.sh <input.csv> <tag> ai`
- Study 2 from scratch: `notebooks/Study2_SYNERGY_Colab.ipynb` in Colab
