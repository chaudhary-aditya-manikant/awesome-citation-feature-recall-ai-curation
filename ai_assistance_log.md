# AI Assistance Log — prompts, AI proposals and human verification

**Project:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation
**Student:** Aditya Chaudhary (MNS2026008), IIIT Allahabad · **Period:** 28 October – 14 November 2026
**AI tool:** Claude (Anthropic), used as a supervised research assistant and pair programmer through the course's AI Prompt Studio (Prompts 01–18), each adapted with the project's own files, outputs and evidence.

**Disclosure (brief §10).** AI support was used for ideation, literature mapping, code generation, debugging, first-pass relevance screening, analysis, visualisation and writing. Every reference was checked against its DOI, publisher or PubMed record; every reported number traces to a result file produced by the code in `src/`; final relevance decisions on all relevant and boundary records were made by the author. Evidence labels follow the brief: **VERIFIED** (checked against a source or a real run), **INFERRED** (plausible, needs testing), **UNKNOWN** (no evidence).

Detailed dated records: `docs/06_Evidence_and_Logs/AI_Assistance_and_Verification_Log.md` and `docs/18_Prompt18_AI_Accountability/AI_Use_and_Verification_Report.md`.

---

## 1. Prompt-by-prompt record

| Prompt | Task | AI proposal | Human decision / input | Verification | Output |
|---|---|---|---|---|---|
| 01 | Research workspace | Summary of the review's scope; decision log with evidence labels | Supplied the review (PDF, LaTeX, BibTeX) as source of truth | Summary checked against the review text | `docs/01_…/research_decisions.md` |
| 02 | Research gaps | Five testable gaps with source passages | Approved the gap: no study reports recall split by citation band or language | Each gap traced to a review section; novelty marked UNKNOWN | `docs/02_…/gap_matrix.md` |
| 03 | Literature → experiment | Three pathways; CPU-feasible TF-IDF + logistic-regression ablation | Approved pathway C (one isolated feature change) for CPU/time limits | Methods mapped to original papers | `docs/03_…` |
| 04 | Feasibility, novelty, access | Search strings, dataset/licence comparison, go/no-go | Approved OpenAlex (CC0) after comparison with SYNERGY, Mendeley and Zenodo candidates | Source pages and licences checked | `docs/04_…` |
| 05 | Questions and success criteria | RQ1–RQ3, metric, decision rule | Approved one primary question; language kept conditional | Brief reviewed before implementation | `docs/05_…/research_problem_brief_MNS2026008.md` |
| 06 | Dataset and comparators | Collector code, pilot queries, audit workflow | **Ran all OpenAlex collection and pilot queries in Colab** and supplied the outputs | Duplicate, paratext and retraction checks against publisher pages | `data/collection_audit_20261031/` |
| 07 | Frozen blueprint | Grouped split, K, gate, bootstrap, success rule, threats | Protocol frozen before any model was fitted | Pre-experiment checklist; amendments logged with dates | `docs/07_…`, `configs/frozen_protocol.json` |
| 08 | Environment | Requirements, environment test | Colab environment used for collection and pilot | Test suite run; versions recorded per run | `docs/08_…`, `requirements*.txt` |
| 09 | Baseline code | `src/run_experiment.py` in small cycles with tests | Code read and run; outputs inspected | Unit and integration tests | `src/`, `tests/` |
| 10 | Baseline validation | Leakage, determinism and sanity checks | Proceeded only after the checks passed | `baseline_validation.md` | `results/…_frozen/` |
| 11 | Debugging | Fixes for errors from real runs (see §3) | Errors reported from genuine runs | Each fix covered by a test | `docs/11_…` |
| 12 | Contribution | Contribution boundary; what is not claimed | Approved claims at course-study level, no novelty claim | Checked against related work | `docs/12_…` |
| 13 | Evaluation | Metric and cross-fit code, paired bootstrap | Ran on final labels | All tables regenerated from CSVs | `results/run_20261105_reviewed_*` |
| 14 | Interpretation | Observations vs. mechanisms vs. limits | Reported as exploratory because the gate failed | Claims checked against result files | `docs/14_…` |
| 15 | Manuscript | LaTeX draft, abstract written last | Text and numbers checked against results | Compiled; every number traced to a file | `paper/` |
| 16 | Peer review | Major/minor concerns, remedies | Addressed label provenance and fold concentration | Review checklist | `docs/16_…` |
| 17 | Repository | README, structure, reproduction commands | Repository created and pushed by the author | Re-run reproduced committed results exactly | this repository |
| 18 | AI accountability | This log | Final check by the author before submission | Compiled from the dated logs in `docs/` | `ai_assistance_log.md` |

---

## 2. Significant AI-assisted activities

**A. Choosing the research question**
- *AI proposal:* five gaps from the review; recommended a single-feature ablation as the most feasible design.
- *Human decision:* approved the citation-feature gap and pathway C; kept the language question conditional rather than dropping it.
- *Verification:* gap passages checked in the review; supporting papers checked against DOI records (e.g., Beel & Gipp 2009 on citation weighting in Google Scholar).
- *Outcome:* `research_decisions.md`, `docs/05_…`.

**B. Data collection and audit**
- *AI proposal:* OpenAlex collector with quota sampling, query log and audit scripts.
- *Human decision:* ran the collection and pilots in Colab; proceeded with the balanced pool (Amendment A2) instead of the legacy pool.
- *Verification:* 19 missing-title and 8 administrative records checked against publisher pages; 6 whole-issue records excluded, 13 held rather than guessed.
- *Outcome:* 2,790-record audited pool, 27 records withheld before screening.

**C. Relevance screening**
- *AI proposal:* first-pass labels for 2,763 records under Rubric v2, each with a rationale and confidence; 20% self-consistency re-screen (549/550).
- *Human decision:* reviewed all 458 relevant, uncertain and boundary records and made the final decision on each.
- *Verification:* agreement with the AI 443/458 (κ = 0.88); **15 AI decisions changed by the author**.
- *Outcome:* `data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv` with a `label_source` column.

**D. Experiment and analysis**
- *AI proposal:* runner, cross-fitted analysis, sensitivity and error analysis, figures.
- *Human decision:* when the dataset gate failed, the author approved reporting the result as exploratory instead of confirmatory (Amendment A3, recorded before fitting).
- *Verification:* seeds fixed; re-runs reproduce committed result files byte for byte; 58 tests pass.
- *Outcome:* `results/run_20261105_reviewed_*`, Figures 1–2.

**D2. Post-hoc reference rankers (10 November 2026)**
- *AI proposal:* add a citation-only ranker and a simple mitigation (reserve part of the top-K for lower-citation records) to meet the brief's "at least two methods/controls" more fully, computed from the committed predictions without refitting the pre-registered rankers.
- *Human decision:* the author asked for the comparison and accepted the AI's default reserved share of 0.5, which was set before anything was computed and not tuned; both rankers are labelled post-hoc in the paper.
- *Verification:* 3 new tests; pooled counts checked against the per-fold predictions; the citation-blind and citation-aware rows reproduce the cross-fit file exactly.
- *Outcome:* `results/run_20261105_reviewed_posthoc_comparators/`, Table 3 of the paper.

**D3. Blind spot-check of AI-only labels (10 November 2026, Amendment A4)**
- *AI proposal:* measure the error rate of the 2,305 unreviewed AI labels with a seeded random sample of 200, re-screened blind (AI label and citations hidden), with an exact confidence interval.
- *Human decision:* the author agreed to do the check and screens all 200 records personally under Rubric v2.
- *Verification:* sample list committed before review; a test confirms it matches the seeded draw; tests for scoring and correction.
- *Outcome:* the author agreed with the AI on 190/200; **3 relevant papers the AI had missed** (all uncited, non-English or regional) and 7 without usable abstracts. Study 1 re-run with the corrections: effect unchanged (9/10 vs 3/10). Files: `data/spotcheck_20261110/`, `results/spotcheck_20261110/`, `results/run_20261110_spotcheck_*`.

**D4. Study 2: pre-registered confirmatory test on SYNERGY (13–14 November 2026)**
- *AI proposal:* after the pilot's gate failed, test the same hypothesis on a large human-labelled benchmark; candidate datasets (SYNERGY, CSMeD) with their trade-offs; options for each protocol value; code for the fetch, the four-ranker analysis, tests and a Colab notebook.
- *Human decision:* the author chose to run Study 2 on SYNERGY and set the gate (50 per citation group, stricter than the pilot's 20), the minimum of 20 inclusions per review, the reserved share (0.5) and the precision limit (0.05), and wrote the reason for each in `PREREGISTRATION_v2.md` before any data were downloaded. The AI pointed out that the author's first draft reason for the gate described it as a citation threshold, and that the citation-timing answer missed reverse causation; the author rewrote both. The author ran every step in Colab.
- *Verification:* protocol file refuses to run with undecided values; 56 tests before the run; pooled counts rebuilt identically from the committed scores for 150,154 records; per-review table checked against the pooled table.
- *Outcome:* gate passed (977 / 1,768); H1 supported (Δ = 0.052, CI 0.033–0.068); H2 supported. `results/study2_confirmatory/`, Section 6 of the paper.

**E. Manuscript**
- *AI proposal:* LaTeX draft built from the result files.
- *Human decision:* checked text and numbers; limitations and label provenance stated explicitly.
- *Verification:* every number in the abstract, tables and figures compared with the CSV outputs.
- *Outcome:* `paper/` (7 pages, ACM format).

---

## 3. Real AI limitations, manual corrections and purposeful verification

1. **Pilot labels too broad.** AI-assisted pilot labels counted general protocol papers as relevant. After inspection the rubric was tightened to the narrow target task (Rubric v2) and the pilot labels were marked preliminary.
2. **Wrong bootstrap unit.** Generated code resampled individual records although splits were grouped by version cluster. Changed to a paired cluster bootstrap; covered by a test.
3. **Wrong grouping column.** The runner used `duplicate_cluster_id` while the audit required `split_group_id`. Corrected, with two new tests.
4. **Synthetic smoke test could be mistaken for results.** Added an explicit `SOFTWARE_SMOKE_TEST_ONLY` status so that synthetic runs can never be reported as findings.
5. **AI screening errors.** The author's review changed 15 AI decisions: 4 relevant → not relevant, 2 uncertain → not relevant, 1 uncertain → relevant, 8 → uncertain.
6. **Degenerate statistic on real data.** With one lower-citation test record the bootstrap interval was [1, 1] and the success rule fired mechanically. An estimability guard was added and disclosed as a post-hoc change (Amendment A3 addendum).
7. **Bugs found only on real data.** The cross-fit script assumed an AI-only column; the merge script clashed with empty label columns; `run_all.sh` failed on absolute paths. All fixed and covered by tests.
8. **Colab errors in pilot code.** Malformed print strings and narrow label parsing were reported from the Colab runs and corrected.
9. **AI screener missed rarely cited relevant papers.** The blind spot-check found 3 relevant records among 200 the AI had called off-topic, all uncited. The AI's misses fall on exactly the group the study measures; this is reported as a limitation.
10. **Wrong dataset version downloaded.** The AI-written fetch script relied on the package default, which had changed to a different collection (SYNERGY+ 3.0) with many records lacking OpenAlex ids; the first run read 0 records. The original SYNERGY was then selected explicitly and the change recorded before any result.
11. **Fragile id detection.** The AI's first two fixes for finding the OpenAlex id column still returned 0 records on real data; the third version checks every column and was tested on four layouts before reuse.
12. **Rate limit not anticipated.** The live OpenAlex download stopped twice at 90,100 of 166,085 records. The citation counts stored in SYNERGY were used instead, recorded as deviation D1 before any result.
13. **Pilot overstated the effect size.** Study 1's point estimate (0.57 on 7 records) was about ten times the confirmed effect (0.052 on 977). The pilot is reported as exploratory for this reason.
14. **Dependencies not pinned.** The AI's `requirements.txt` allowed a range of library versions. On the author's laptop (scikit-learn 1.5.2) the retrained Study 1 rankers gave the same counts and point estimates but a slightly different bootstrap interval (0.167 instead of 0.143). The author re-ran in a clean environment with the original versions, which reproduced every number, and the versions are now pinned.
15. **Unverifiable claim removed.** A sentence stating what a cited study did not report was reduced to what could be checked.

---

## 4. Decisions that depended on human judgement or approval

- Approval of the gap, question and pathway, and of keeping the language question conditional.
- The final relevance decision on every relevant and boundary record.
- Requesting the reference rankers and accepting that they are reported as post-hoc.
- Approval of reporting the result as **exploratory** after the gate failed, rather than lowering the threshold or relabelling records.
- Running the data collection in Colab and checking its outputs before they were used.
- Choosing to run a second, confirmatory study, and every pre-registered value and reason in `PREREGISTRATION_v2.md`.
- Accepting deviation D1 (stored citation counts) rather than waiting for the rate limit to clear.

The interpretation that the citation advantage of relevant records is partly a collection effect (46/64 reached through citation neighbourhoods) was proposed during analysis and accepted by the author; it is stated as a limitation in the paper.

## 5. Lessons about AI-assisted ("vibe") coding from this project

- Generated code that runs is not the same as correct code: three of the bugs above appeared only on real data, after synthetic tests had passed.
- Short cycles of *specify → generate → test → run on real data* caught problems early; every fix was locked in with a test.
- Statistical code needs the same scrutiny as research claims: the grouped bootstrap and the degenerate interval were design errors, not syntax errors.
- Freezing the protocol before seeing results made the failed gate an honest finding instead of a temptation to tune.
- Code tested only on synthetic data failed three times on the real SYNERGY files; each fix needed the real error message. Scripts that print a sample of the real data on failure would have saved two rounds.
- A small pilot can get the direction right and the size badly wrong; the confirmatory study was needed to learn the size.

## 6. Remaining risks

- 2,305 clearly off-topic records keep AI first-pass labels (disclosed in the paper).
- Publication languages are unverified, so no language claim is made.
- Study 1's effect rests on 7 lower-citation relevant records (10 after the spot-check).
- Study 2's effect is small, varies between reviews, and comes mostly from medical reviews; its citation counts post-date the reviews.
- A fresh OpenAlex pull may differ slightly from the 30 October 2026 snapshot.
