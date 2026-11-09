# Prompt 07 — Pre-Experiment Checklist and Protocol Change Log

**Student:** Aditya Chaudhary | **Enrollment:** MNS2026008  
**Project:** *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*  
**Protocol:** Version 1.0, frozen 30 October 2026

This checklist is a compact execution gate for the detailed blueprint in `Prompt07_Frozen_Experiment_Blueprint_MNS2026008.md`. The 28-record pilot and the 30 October date-sorted 3,000-record collection are historical development evidence only. The active candidate pool is the student-run 2,790-record balanced OpenAlex collection described in `06_Balanced_Collection_Audit_20261031/audit/BALANCED_COLLECTION_AUDIT_REPORT_31Oct2026.md`; its dataset gate remains open until human screening, language verification and final preflight pass.

## A. Dataset acceptance (must pass before model fitting)

- [ ] Frozen scope: scholarly-literature discovery/curation methods, publication years 2015–2025.
- [ ] Exact multi-route query strings, source routes, retrieval timestamp, citation snapshot date and any sampling/cap rules archived.
- [ ] Dataset deduplicated by OpenAlex ID/DOI/title-version evidence; duplicate groups recorded.
- [ ] Written inclusion/exclusion rubric applied; uncertain labels resolved or excluded; rationale saved.
- [ ] Label audit documented; independent reviewer used if available, otherwise clearly labelled as a single-reviewer consistency audit.
- [ ] Metadata-language audit completed on a seeded, stratified sample; use “metadata language” unless actual publication language is verified.
- [ ] No duplicate/version group crosses splits.
- [ ] At least 20 relevant lower-citation and 20 relevant higher-citation test records; otherwise no confirmatory citation-group claim.
- [ ] For confirmatory English/non-English comparison, at least 20 relevant test records per group and adequate language validation; otherwise exploratory/omitted.
- [ ] Data manifest, group counts and gate decision saved before test ranking metrics are computed.
- [ ] Abstract plaintext omitted from shared/public outputs unless redistribution is explicitly permitted.

## B. Frozen split, models and metrics

- [ ] `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=20261030)` feasibility verified in the actual environment.
- [ ] Fold 0=test, fold 1=validation, folds 2–4=train; exact split manifest saved.
- [ ] Condition A: word TF–IDF (1,2), `min_df=2`, `max_features=100000`, `sublinear_tf=True`, year feature, Logistic Regression (`C=1.0`, balanced class weights, `liblinear`, `max_iter=2000`, seed `20261030`).
- [ ] Condition B matches A exactly except for standardized `log1p(cited_by_count)`.
- [ ] Text and numeric transforms fit on training records only; no test-derived features or thresholds.
- [ ] Same held-out records and deterministic OpenAlex-ID tie-break for both conditions.
- [ ] Primary metric is lower-citation Recall@K, `K=ceil(0.20*N_test)`; overall Recall@K and Precision@K are guardrails.
- [ ] Primary success rule: paired difference > 0, two-sided 95% paired bootstrap interval excludes zero, and Condition A Precision@K is no more than 0.05 absolute points below B.
- [ ] Bootstrap: 2,000 paired resamples, seed `20261031`; report valid replicate count.
- [ ] Secondary citation gap, conditional language analysis, 10%/30% K sensitivity, top-K disagreement review and efficiency metrics are prespecified.

## C. Reproducibility and freeze

- [ ] Environment, hardware, package versions, actual commands, warnings and runtime will be logged.
- [ ] Expected CSV/table/figure schemas are defined in the blueprint.
- [ ] Test metrics have not been inspected while selecting the protocol.
- [ ] `protocol_change_log.md` exists; the original version will not be overwritten.
- [ ] The software/environment smoke test may be performed before the data gate; fitting either research model and computing held-out research metrics remain blocked until Section A passes.

## Protocol change log

| Amendment ID | Date/time | Exact change | Reason/evidence | Were test outcomes already viewed? | Affected outcomes / post-hoc status |
|---|---|---|---|---|---|
| A1 | 30 Oct 2026 | Clarified the paired bootstrap resampling unit as `duplicate_cluster_id`; used the same resampled cluster sequence for both model conditions. Passed the configured `--seed` to the Logistic Regression estimator as well as the grouped split. Added `--preflight-only` to write the fixed split and data-gate report without model fitting. | Duplicate/version clusters are the independence unit used by grouped partitioning; bootstrapping individual records could split the cluster dependence structure. Seed propagation and a no-fit data gate improve reproducibility and safe sequencing. | No main research test outcomes were viewed; changes were tested only on synthetic fixtures. | Protocol v1.0-A1. Primary question, features, split folds, primary metric, K=20%, decision rule and research hypotheses unchanged. Cluster bootstrap implementation detail is now explicit. |

## Current gate status

**NOT PASSED — do not train or evaluate the main model yet.** The balanced 2,790-record candidate pool is collected and metadata-audited, but it has zero human relevance labels and zero completed publication-language source verifications. Six issue-level missing-title records are excluded with publisher evidence; 13 title holds and one pending retraction source check remain. Complete screening/consistency review and language verification, then record the final gate decision before any comparative test metrics are computed.


## Protocol amendment A3 — 31 October 2026 (before model fitting)

| ID | Date | Change | Reason | Evidence/status | Effect on protocol |
|---|---|---|---|---|---|
| A3 | 31 Oct 2026 | Use the audit-generated `split_group_id` as the sole duplicate/version grouping key for `StratifiedGroupKFold`, split-leakage checks and paired cluster bootstrap. Do not use the incoming OpenAlex `duplicate_cluster_id` column. | The balanced-pool audit found that the incoming `duplicate_cluster_id` had 2,790 distinct values and did not represent the manual version relationship in the manifest. The audited `split_group_id` preserves reviewed version relationships and gives singleton IDs to other works. | The revised code now requires `split_group_id`; two new regression tests verify that a legacy-only group column is rejected and a conflicting legacy column is ignored. Offline suite after later workflow additions: 30 passed in the package-build environment; newest Colab rerun remains pending. No real labels or model outcomes were used. | Corrects the identity field used to implement the already-frozen grouped split and bootstrap. The 5-fold StratifiedGroupKFold design, fold assignment, seed, metrics, feature conditions, K=20%, and success rule remain unchanged.


| A4 | 31 Oct 2026 | Mark the successfully collected 2,790-record seeded exact-year multi-route OpenAlex pool as the active candidate pool; retain the 28-record pilot and 30 Oct 3,000-record date-sorted pool as legacy only. | Live balanced collector manifest shows 132/132 search/topic cells, 5/5 seed resolutions, 10/10 citation-neighbourhood requests, 2,790 unique works, all abstracts present and no logged API errors; annual record counts are 247–262. | No model/test performance metrics were inspected. This is a candidate-pool acquisition update; the pool is not a probability sample/census and all claims remain pool-relative. | Does not change RQs, classifiers, features, split/fold/seed protocol, metrics, primary threshold or success rule. Dataset acceptance remains pending human labels and language verification.
