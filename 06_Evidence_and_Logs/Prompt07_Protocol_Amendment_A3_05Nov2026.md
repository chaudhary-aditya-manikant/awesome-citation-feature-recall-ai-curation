# Protocol Amendment A3 — AI-provisional labels and exploratory analysis (5 November 2026)

**Project:** MNS2026008 — Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation
**Recorded:** 5 November 2026, before any model was fitted to the balanced pool and before any test metric was computed.

## 1. Why this amendment exists

The student asked for the full pipeline to be completed now and for the relevance labels to be
verified by the student afterwards. The relevance screening of the 2,763-record queue was therefore
performed by an AI assistant (Claude, Anthropic) applying Annotation Rubric v2. These labels are
**AI-provisional**. They are recorded with `label_status = ai_provisional` and
`reviewer_id = AI-ASSIST-CLAUDE-20261105`, never under the student's name, and every output
produced from them is stamped `AI_PROVISIONAL_LABELS_NOT_HUMAN_VERIFIED`.

## 2. Screening outcome that triggers the amendment

- Decided records: 2,759 (68 relevant, 2,691 not relevant); 4 records remain uncertain and are excluded.
- Prevalence of relevant records: 2.5%.
- Consistency audit: seeded random 20% re-screen (seed 20261030, n = 550) by the same AI screener
  without access to first-pass labels: 549/550 agreement, Cohen's κ = 0.96. This is a self-consistency
  check, not inter-rater agreement.
- With about 68 positives, a single 20% test fold is expected to hold about 13–14 relevant records,
  roughly 6–7 in each citation group. The frozen gate (≥ 20 relevant lower-citation and ≥ 20 relevant
  higher-citation test records) cannot pass.
- Pool expansion, the frozen protocol's first remedy, is not possible in the current environment
  (the OpenAlex API is unreachable), and no re-collection is authorised by this amendment.

## 3. Decisions (made before modelling)

1. **Gate result is reported as FAIL.** No confirmatory citation-group claim will be made.
2. **Frozen analysis is still run, as exploratory.** The frozen single-split design (fold 0 test,
   folds 2–4 train, fixed seed 20261030, `K = ceil(0.20 × N_test)`, identical Logistic Regression
   settings, paired cluster bootstrap) is executed unchanged except that the runner is allowed to
   continue past the failed gate when invoked with `--exploratory-after-gate-failure`. All outputs
   are labelled `EXPLORATORY_GATE_FAILED`.
3. **Added exploratory cross-fitted analysis.** To use every relevant record once as a test case, the
   same five `StratifiedGroupKFold` folds (seed 20261030) are each used as the test fold in turn, with
   the remaining four folds as training data (no tuning, so no validation fold is needed). Recall@K
   is computed within each fold with `K = ceil(0.20 × N_fold)` and pooled across folds
   (relevant-in-top-K summed over folds divided by relevant records summed over folds). The paired
   difference is bootstrapped by resampling `split_group_id` clusters within folds (2,000 replicates,
   seed 20261031). This analysis is **secondary and exploratory**; it was not in the frozen protocol.
4. **Language analysis** remains descriptive only: no publication language has been independently
   verified, and non-English metadata positives are too few for any group comparison.
5. **Nothing else changes.** Model, features, citation transformation, citation-rate grouping
   (age-adjusted rate, median split on the eligible pool), K rule, tie-breaking and success rule are
   as frozen. No result will be used to alter labels, features or cutoffs.

## 4. What must happen before any result is treated as final

1. The student verifies the AI-provisional labels (at minimum all 68 relevant, all 4 uncertain, all
   low-confidence decisions, and a fresh seeded sample of negatives), records their own decisions in the
   screening workbook, and re-runs `code/run_all_provisional.sh` (or the equivalent commands) on the
   human-verified file with `label_status = single_reviewer_audited`.
2. If the student's labels change the gate outcome, the frozen confirmatory analysis is run and
   reported in place of the exploratory one.
3. The manuscript text describing who screened the records must be updated to match.

## Addendum (5 November 2026, after the frozen exploratory run)

The frozen single-split run produced a test fold with **one** relevant lower-citation record. The
paired cluster bootstrap then returned a degenerate interval of [1.0, 1.0] and the mechanical success
rule evaluated to true. This is not interpretable. A reporting guard was added to
`run_experiment.py` *after observing this output*: `primary_estimable` is false when fewer than 10
relevant lower-citation test records are present, and the success rule cannot be met when the primary
estimate is not estimable. The guard changes no estimate; it is disclosed here because it was added
after a result was seen. The frozen-split output is reported as "not estimable"; the cross-fitted
analysis in Section 3.3 is the main exploratory result.


## Reviewer verification (5 November 2026, after the AI-only exploratory runs)

The author (MNS2026008) reviewed 458 records in the review-first sheet (all 72 AI-relevant/uncertain, 53 borderline negatives, 333 negatives containing curation-related terms) and confirmed in writing that they personally reviewed them. Agreement with the AI first pass: 443/458 (κ = 0.88); 15 decisions changed. Reviewed rows are `single_reviewer_audited`; the 2,305 unreviewed off-topic rows remain `ai_provisional`. Reviewer_ID and Review_Date were blank in the returned file and were filled from the author's confirmation; the as-received file is archived unchanged. The full analysis was re-run on these final labels; the AI-only runs are archived as superseded. The gate still fails and results remain exploratory.
