# Balanced OpenAlex Candidate-Pool Audit — updated 31 October 2026

**Project:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation  
**Student:** MNS2026008  
**Active collection:** balanced OpenAlex candidate pool, citation snapshot 2026-10-30  
**Audit status:** retrieval and automated metadata audit complete; human relevance and publication-language evidence gates remain open.

## Executive result

The active collection contains **2,790 distinct OpenAlex Work IDs**, each with a non-empty abstract. The student's Colab collection manifest records all 132 planned exact-year search/topic route cells (88 search + 44 topic), five DOI seed resolutions, and ten citation-neighbourhood requests as executed, with no logged API errors. Yearly counts range from 247 to 262 over 2015–2025. The revised pool replaces the earlier date-sorted 3,000-record pilot as the active candidate pool; the old pilot is retained only as historical development evidence.

This is a **quota-stratified, multi-route, query-frame candidate pool**, not a census or a probability sample of all scholarly literature. OpenAlex sampling was seeded within each specified query/year frame; route overlap was deduplicated by OpenAlex Work ID. Conclusions must be described as **pool-relative**. The collection's reported count is the returned sample count per frame, not an estimate of the full query-frame population.

## 1. Collection integrity and year balance

| Check | Result |
|---|---:|
| Distinct OpenAlex Work IDs | 2,790 / 2,790 |
| Non-empty abstracts | 2,790 |
| Missing abstracts | 0 |
| Search route/year cells | 88/88 |
| Topic route/year cells | 44/44 |
| Seed DOI resolutions | 5/5 |
| Citation-neighbourhood requests | 10/10 |
| Query log entries | 147 |
| Logged API errors | 0 |
| Sampling seed base | 20261031 |
| Citation snapshot date | 2026-10-30 |

| Publication year | Records |
|---:|---:|
| 2015 | 255 |
| 2016 | 247 |
| 2017 | 252 |
| 2018 | 248 |
| 2019 | 249 |
| 2020 | 254 |
| 2021 | 255 |
| 2022 | 262 |
| 2023 | 257 |
| 2024 | 256 |
| 2025 | 255 |

The 15-record max–min annual difference is a result of per-year quotas. It does not imply equal inclusion probabilities across all works or eliminate retrieval/query-frame bias. OpenAlex search relevance and the specific seed/topic/citation routes remain part of the study's sampling frame.

## 2. Metadata quality and administrative disposition

| Check | Audit finding |
|---|---:|
| Original missing-title records | 19 |
| Source-verified issue-level paratext among those | 6 |
| Unresolved missing-title holds | 13 |
| Missing DOI | 513 |
| `is_retracted=true` in OpenAlex | 4 |
| Type-coded retraction notices | 1 |
| Type-coded errata | 2 |
| Superseded F1000 version | 1 |
| Zero-citation records | 986 |
| Median cited-by count | 2 |
| Maximum cited-by count | 26,052 |

Six of the 19 missing-title DOI records were verified against publisher issue pages as complete journal issues, not standalone articles. These six are excluded from article-level screening and preserved in the audit ledger. Thirteen records remain on source-repair hold; no title has been inferred from the abstract or DOI. See `TITLE_REPAIR_SOURCE_EVIDENCE_31Oct2026.md`.

The eight administrative candidates comprise four OpenAlex retraction flags, one retraction notice, two errata/correction notices, and one superseded F1000Research version. Seven have publisher/authoritative bibliographic source support. The `Movie genres and beyond` record (DOI `10.1109/ICOEI51242.2021.9453021`) remains **pending publisher confirmation**: the work's title and DOI are identifiable, but no authoritative IEEE retraction notice was found in this audit. Do not exclude solely on the OpenAlex flag until this status is independently resolved.

The 513 records without a DOI are not automatically invalid; OpenAlex Work ID is retained as the stable collection identifier. Missing DOI is reported as a limitation and DOI-dependent source verification may be unavailable for some items.

## 3. Duplicate and version handling

- There are zero repeated OpenAlex Work IDs and zero repeated normalized DOI values in the incoming file.
- The incoming OpenAlex `duplicate_cluster_id` is not trustworthy for split grouping: it contains effectively one ID per work, whereas the manifest reports duplicate clusters. The audit-generated `split_group_id` is the authoritative grouping field.
- `split_group_id` contains 2,789 groups for 2,790 records: one verified two-record F1000Research version group; all other works are singleton groups.
- F1000Research DOI `.1` is the superseded v1 and DOI `.2` is the later publisher-listed v2. Retain v2 as canonical in the primary pool; preserve v1 as an administrative version record and keep both version IDs connected through the same `split_group_id`.
- Two exact generic *Editorial* title/year pairs have distinct DOI and record metadata; they are retained as separate candidates rather than auto-merged. Their content must still be evaluated under the inclusion rubric.
- The 2018 and 2019 *Self-Tuned Descriptive Document Clustering Using a Predictive Network* records have distinct DOI, authors, venues and abstracts and are retained separately.
- The erratum to the 2015 text-mining systematic review is a correction notice, not a duplicate. The erratum is excluded; its primary review remains a separate work.

For every split, leakage audit and paired cluster bootstrap, use `split_group_id` only. The experiment runner now rejects inputs that provide only the legacy group column and uses `split_group_id` even when a conflicting legacy field is present.

## 4. Screening and exclusion queues

The 2,790 records have these mutually exclusive pre-screen dispositions:

| Disposition | Records | Treatment |
|---|---:|---|
| Ready for title/abstract human screen | 2,139 | Human relevance screening required |
| Non-standard type scope review | 624 | Human content-based scope decision required; type alone is not grounds for exclusion |
| Missing-title metadata hold | 13 | Not eligible for screening until repaired or documented as unrecoverable |
| Issue-level paratext, source verified | 6 | Exclude from article-level pool; retain evidence |
| OpenAlex retraction-flag candidates | 4 | Administrative exclusion candidates; one publisher-source case remains unconfirmed |
| Erratum/correction notices | 2 | Exclude notices; retain linked primary works |
| Retraction notice | 1 | Exclude notice; retain link to retracted original |
| Superseded version | 1 | Exclude v1; retain v2 canonical |

The 2,139 ready + 624 type-scope-review records form the **2,763-record blinded human screening queue**. The workbook has 28 batches; `Batch_B01` contains 108 records. All human label, rationale, confidence and adjudication fields are blank. AI-generated triage is not substituted for human gold labels.

## 5. Language metadata and verification

OpenAlex metadata-language counts are: English `en` = 2,560 (91.8%); known non-English language codes = 229 (8.2%); unknown = 1. These values describe OpenAlex's automatically detected title/abstract metadata language, not verified publication language. A blinded 200-record stratified sample is prepared: 100 metadata-English, 99 known non-English distributed across the observed language strata, and the one metadata-unknown record. The private `Language_Key` stores the sampling stratum and design weights. The reviewer workbook hides OpenAlex language metadata until verification entries are recorded.

**No publication language in the 200-record sample has yet been independently verified.** Publication-language analysis must remain unreported/conditional until each sampled item has a publisher article page/PDF or reliable institutional/library evidence URL, verifier and date.

## 6. Data access, licensing and rights

OpenAlex documents its dataset as CC0/public-domain metadata for reuse. This statement applies to the OpenAlex dataset, not automatically to publisher full-text content or PDFs. The shareable CSV omits abstract text; the private screening CSV retains abstracts for internal adjudication. No publisher full-text PDFs are included. Any later use of full text must respect the individual source's licence and terms. OpenAlex Work IDs and DOI values are included for traceability. The data acquisition/query log and snapshot date are retained.

## 7. Baseline/comparator design (specified, not yet empirically validated)

The frozen controlled feature ablation is:

- **Condition A — citation-blind:** word TF–IDF over title + abstract (`ngram_range=(1,2)`, `min_df=2`, `max_features=100000`, `sublinear_tf=True`) plus standardized publication year; Logistic Regression (`C=1.0`, `class_weight=balanced`, `solver=liblinear`, `max_iter=2000`, seed `20261030`).
- **Condition B — citation-aware:** exactly the same records, split, text representation, year feature and classifier, adding only standardized `log1p(cited_by_count)`.

Citations and verified language are not used as general predictors; the citation count is the single intentional feature change for Condition B. Language and citation groups are evaluation strata. Text and numeric scaling are fitted on training data only. The citation snapshot is fixed at 2026-10-30. Primary outcome is lower-citation-group Recall@K with `K=ceil(0.20*N_test)`; overall Recall@K/Precision@K are guardrails. Pairwise bootstrap resamples the audited `split_group_id` groups (2,000 replicates under the frozen protocol).

These are **planned comparator methods**, not verified baselines on the accepted research dataset. No model has been trained on the balanced pool and no research performance number exists.

## 8. Leakage controls and preflight requirements

1. Build the final eligible pool only after human label adjudication and administrative exclusions.
2. Use `split_group_id` for `StratifiedGroupKFold`, split manifest, leakage check and cluster bootstrap.
3. Fit TF–IDF and scalers on training data only.
4. Keep citations and verified language out of Condition A; add only `log1p(cited_by_count)` in Condition B.
5. Preserve the fixed citation snapshot 2026-10-30 and seed/fold assignments in the split manifest.
6. Do not redraw splits to meet subgroup minimums or improve metrics.
7. Run preflight before any model fit. The held-out test fold must contain at least 20 relevant lower-citation and 20 relevant higher-citation records; confirmatory language subgroup analysis has its own minimum and source-verification requirement.

## 9. Prompt 06 completion status

**Completed and evidenced:** live candidate collection by student in Colab; 132 route/year cells; collection logs and UTC run times; year-balance audit; metadata and administrative flag checks; source verification of six issue-level title records; 7/8 administrative source decisions; duplicate/version ledger; audit-derived `split_group_id`; data access/licence statement; two comparator specifications; 2,763-record blinded screening workbook; 200-record blinded language-verification workbook; import-validation utilities; software tests.

**Still open and not fabricated:** human relevance/eligibility decisions for 2,763 records; documented handling of all 13 unresolved missing-title records; publisher confirmation or an explicit pending limitation for the `Movie genres and beyond` OpenAlex retraction flag; source verification of all 200 language sample entries; final adjudicated CSV and split manifest; Prompt 07 data preflight. The 624 non-standard work-type flags require content-based review and cannot be automatically excluded by type.

**Current conclusion:** Prompt 06's data acquisition, audit, comparator design and reviewer-workflow deliverables are substantially complete. The final dataset-acceptance gate remains **OPEN**. No baseline execution, research metrics or empirical conclusion is claimed. The assignment's G2 gate additionally requires an executable baseline, measured output and a validation report; those remain subsequent work.

## 10. Key source links

- OpenAlex CC0 data and terms: https://help.openalex.org/api/ and https://help.openalex.org/data/how-its-built/
- OpenAlex `sample` and `seed` API quick reference: https://help.openalex.org/api/llm-quick-reference/
- OpenAlex sampling recipe: https://help.openalex.org/how-to/api-recipes/
- OpenAlex Works language field: https://help.openalex.org/data/works/attributes/
- F1000Research version page: https://f1000research.com/articles/12-512
- Publisher issue-page evidence for the six source-confirmed paratext records: see `TITLE_REPAIR_SOURCE_EVIDENCE_31Oct2026.md`.
- Publisher/authoritative administrative status evidence: `ADMINISTRATIVE_SOURCE_VERIFICATION_31Oct2026.md` and `administrative_exclusion_source_audit_31Oct2026.csv`.
