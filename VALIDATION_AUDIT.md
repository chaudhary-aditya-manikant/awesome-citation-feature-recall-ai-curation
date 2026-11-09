# Validation Audit — Prompts 01–07 Package

**Audit date:** 30 October 2026  
**Purpose:** Check internal consistency, pilot arithmetic, source claims that matter for Prompts 04–07, data minimisation, and archive integrity before upload.

## 1. Official assignment alignment

The uploaded assignment PDF was inspected at pages 5–6. It requires:

- Prompt 04: search strings/categories of neighboring work; a matrix of published method, verified contribution/source, limitation, proposed difference and missing evidence; dataset/code/weights/license/protocol access checks; compute/time estimate; fallback; novelty/feasibility matrix and go/no-go decision.
- Prompt 05: a precise problem, two or three research questions, variables, metric, success/decision rule, contradictory observations, and a one-page research brief.
- Prompt 06: primary dataset and two meaningful methods/controls; official-source checks; structure, protocol, license/access, compute, pitfalls; split/leakage design; simplest baseline and independent-verification checklist.

Prompt 07 additionally requires a reproducible frozen protocol, precise inputs/outputs and processing modules, preprocessing, Mermaid architecture/flowchart, partitions, controls/settings, metric directions, seeds, computational budget, expected table/figure formats, a deeper analysis, validity threats, a pre-experiment checklist, and a protocol-change process. These components are present in the Prompt 07 blueprint and checklist. The reports preserve conditional status and do not claim that later model/experiment phases have been completed.

## 2. Pilot arithmetic and data-minimisation checks

The abstract-free CSV included in this package was rebuilt from the latest reviewed binary-label workbook, then read and checked programmatically:

- 28 data rows; 28 unique OpenAlex IDs.
- 4 query-language groups: English 7, Indonesian 7, Portuguese 7, Spanish 7.
- Binary preliminary labels: 6 labelled `1`, 22 labelled `0`.
- Positive/negative counts: English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6.
- Required fields for the pilot analysis (title, year, citation count, metadata language, label, reason and preliminary confidence/status) contain no missing values.
- DOI is missing for 3 records.
- The submitted CSV/XLSX was rebuilt from the latest reviewed binary-label workbook and has no abstract/plaintext-abstract column. The notebook/source working file with reconstructed abstracts is not included. The language-by-label counts were rechecked against the same source workbook: English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6 (positive/negative).

The rebuilt workbook's Summary sheet agrees with the CSV counts and both are derived from the same latest reviewed source workbook. The labels are **preliminary AI-assisted screening labels**, not independently adjudicated gold-standard labels. No inter-annotator agreement was computed. As there are zero Indonesian positives and only one positive in Portuguese and Spanish, these data are not adequate to estimate the intended group-conditional recall. The seven-per-language sampling was imposed by design and does not estimate population language prevalence.

The earlier user-run SYNERGY outputs are recorded separately: 340 rows, four included labels, all 340 observed language values `en`, median citation count 11, and included counts 1 at/below the median and 3 above. The local filename `Hall_2011.csv` is not assumed to match the public repository entry `Hall_2012`.

## 3. Primary-source checks performed

| Claim used in the package | Verification result | Boundary |
|---|---|---|
| OpenAlex supplies `publication_year`, `cited_by_count`, `language`, and `abstract_inverted_index`. | Verified against the official Works attributes page: https://help.openalex.org/data/works/attributes/ | Field availability does not mean every record has a value; final pool missingness must be rechecked. |
| OpenAlex abstracts are represented as inverted indexes rather than shipped as plaintext; `language` is inferred from metadata. | Verified against the official Works attributes page and the language-metadata evaluation. | Local reconstruction is not grounds to publish/redistribute plaintext abstracts; language field may be wrong. |
| OpenAlex data are CC0 and basic API use is available free; a free key increases API budget. | Verified against https://help.openalex.org/api/ , https://help.openalex.org/api/authentication/ and https://help.openalex.org/access/pricing/ | Service usage/budget is not the same as data licensing; snapshots/citation counts change over time. |
| OpenAlex default text-search relevance score incorporates both text similarity and citation count. | Verified against official OpenAlex search documentation: https://github.com/ourresearch/openalex-help/blob/main/content/api/searching.md | Therefore do not rely only on default top-ranked search results for a bias audit. |
| Current OpenAlex topic assignment uses title, abstract and source metadata without citation counts; the documentation notes that an earlier classifier operated differently. | Verified against current topic documentation: https://help.openalex.org/data/topics/ | Use topics as one route, not the only source of candidates; document all routes. |
| SYNERGY has 169,288 records from 26 reviews and 2,834 inclusion labels; current README lists `Hall_2012` as 8,793 records/104 included and states CC0. | Verified against https://github.com/asreview/synergy-dataset | The local `Hall_2011.csv` export/version mismatch remains unresolved and is explicitly not assumed equivalent. |
| Aigner et al. (2026) compares four supervised classifiers and an LLM on six review datasets; preprocessing removed non-English or otherwise unsuitable abstracts. | Verified against https://doi.org/10.1186/s13643-026-03199-6 and https://github.com/MarcoAigner/automated_title_abstract_screening | The paper is CC BY 4.0; no repository-level code licence was located in this check. The code was not installed/reproduced and should not be reused/redistributed without licence resolution. |
| The Zenodo 2026 record describes 440 ML-in-concrete screening records (272 relevant/168 irrelevant). | Verified against https://zenodo.org/records/21853690 | Exact file schema, language coverage and reuse licence were not confirmed by downloading the CSV; treat only as an auxiliary candidate. |
| OpenAlex language labels are not perfectly accurate. | Verified against Céspedes et al. (2025), https://doi.org/10.1002/asi.24979 | The study’s error findings are not assumed to equal the error rate in this pilot. |
| ASReview repository states Apache 2.0. | Verified against https://github.com/asreview/asreview | Repository not installed/run for this project. |
| Rajit et al. (2025) citation-search study covers 27 systematic reviews; its reference method assumes 100% recall by design. | Verified against https://pmc.ncbi.nlm.nih.gov/articles/PMC12621532/ and https://doi.org/10.1017/rsm.2024.15 | This assumption is not independent evidence of complete recall over all relevant literature. |
| Färber et al. (2023), Rovira et al. (2021), Yang et al. (2024), Khatoon & Amjad (2026), and Fleurence et al. (2026) bibliographic details/title claims used in the reports. | Verified against publisher/official records: https://doi.org/10.1007/s11192-023-04636-2 ; https://doi.org/10.3390/fi13020031 ; https://aclanthology.org/2024.mrl-1.23/ ; https://doi.org/10.3390/computers15090594 ; https://doi.org/10.1016/j.jval.2026.06.012 | These sources establish adjacent work, not that the proposed experiment is novel. Novelty remains UNKNOWN. |
| Barragán et al. (2026) scoping review citation. | Verified against https://doi.org/10.1002/cesm.70098 | A scoping review is not a replacement for a systematic novelty search for the precise contribution. |

## 4. Consistency checks and fixes included in this version

- The operational scope is explicitly stated: the pilot target is research on computational/AI methods for scholarly-literature discovery/curation, not all AI application research.
- Prompt 01 log, Prompt 02 gap matrix, Prompt 03 mapping, Prompt 04 report, Prompt 05 brief and Prompt 06 sheet use the same pilot scope and conditional dataset status.
- The `Hall_2011.csv` vs public `Hall_2012` discrepancy is recorded as unresolved rather than silently reconciled.
- OpenAlex text-search citation influence is documented; the main pool must not be constructed only from default ranked search results.
- Aigner repository and Zenodo file licences are treated as unresolved where the inspected pages do not establish the applicable reuse terms.
- The main dataset decision remains conditional and the 28-record pilot is explicitly no-go for main-model evaluation.
- Reconstructed abstract plaintext is omitted from the uploaded evidence copy.

## 5. Remaining research limits (not package defects)

- The literature search is targeted, not exhaustive; novelty remains UNKNOWN.
- The final candidate pool has not been built or accepted; labels and subgroup counts are not yet sufficient. The protocol is frozen, but the data gate remains open.
- No model has been trained, no main ranking metric has been computed and no bias result is claimed.
- The final dataset, final licence/reuse terms, publication-language ground truth and subgroup adequacy must be checked before Prompt 08/main experiment.

## 6. Package validation

The release archive was rebuilt after removing redundant personalized prompt-input copies, normalizing the Prompt 06 folder name, and adding the Prompt 07 blueprint/checklist. Before release, the package was checked for:

- ZIP integrity;
- consistency of the 28-record CSV label totals and language-group counts;
- absence of abstract/plaintext-abstract columns in the shared CSV and workbook;
- presence of the seven main prompt deliverables;
- broken relative Markdown links; and
- SHA-256 checksums for the packaged files; and
- inclusion of the Prompt 07 blueprint/checklist and consistency of the updated status and decision log.

At that earlier release stage, the archive passed ZIP integrity, checksum-manifest verification and relative Markdown-link checks; it contained 19 files at that time. This file-count statement is historical and is superseded by the current release checks recorded in Section 10 below. Those checks establish packaging consistency, not the scientific validity of preliminary labels or the novelty of the proposed study.

## Bibliographic identifier note

The Zenodo benchmark landing page inspected on 30 October 2026 displays DOI `10.5281/zenodo.21853690` in its DOI metadata, while the page’s suggested citation text contains `10.5281/zenodo.21853689`. The package links to the landing-page URL and treats the reuse licence as unresolved; verify the DOI against the canonical metadata before citing or reusing the benchmark.


## Dataset candidate comparison addendum — 30 October 2026

- Added `04_Prompt04_Feasibility/Prompt04_Dataset_Candidate_Comparison_and_Decision_MNS2026008.md`.
- Revised Prompt 04's decision summary and dataset-audit references.
- Updated Prompt 05 and Prompt 06 to distinguish a selected source strategy from a validated final dataset.
- Added Decision 007 to the research log and source-comparison entry to the AI-assistance log.
- External source-page audit does not establish that candidate B/C/E downloadable files were fetched or their full schemas/licences independently checked. These remain explicitly pending.
- No main model, baseline, ranking evaluation, or experimental metric was executed or fabricated.

## 7. Second audit — implementation and literature update (30 October 2026)

### Literature and scope

- Added verified adjacent work on scholarly recommender bias (Färber et al., 2023), multilingual retrieval fairness (Yang et al., 2024), language ranking in Google Scholar (Rovira et al., 2021), OpenAlex language metadata quality (Céspedes et al., 2025), AI screening (Aigner et al., 2026; Barragán et al., 2026), and GenAI in systematic reviews (Adam et al., 2025; Fleurence et al., 2026).
- Added Khatoon and Amjad (2026), a close citation-aware publication-ranking framework. This materially weakens broad novelty claims; the candidate contribution is narrowed to the group-conditional lower-citation Recall@K outcome, and novelty remains unverified.
- Confirmed that the AHRQ 2025 update includes 95 studies and has an English-language evidence scope. It must not be used as evidence of multilingual coverage.
- Verified Rajit et al. (2025) DOI as `10.1017/rsm.2024.15`.
- Flagged the Zenodo landing page's conflicting DOI strings (`.21853690` in record metadata vs `.21853689` in suggested citation) and unresolved licence status.

### Method/code consistency

- Aligned the implementation with the Prompt 07 frozen grouped 5-fold split (fold 0 test, fold 1 validation, folds 2–4 training), same text/year features, citation feature only in Condition B, Logistic Regression settings, fixed tie-break, K, bootstrap seed and decision rule.
- Added explicit citation snapshot date; no dynamic current-date assumption is used for citation-age adjustment.
- Added fail-closed input checks, dataset/split manifests, primary and sensitivity metrics, paired bootstrap, disagreement file, resource timings and figures generated from actual run data.
- Added a flag that prevents confirmatory language claims unless the test language groups meet the count gate and the supplied language verification field is fully verified.

### Software verification

- `python -m pytest -q`: **10 passed**. Tests cover input integrity, cluster bootstrap, offline collector helpers and mocked collection orchestration.
- `python -m py_compile code/run_experiment.py`: passed.
- A 1,200-record synthetic end-to-end smoke test completed with a 720/240/240 grouped train/validation/test partition and generated the expected output types. Synthetic metrics were not retained or represented as findings.
- Environment used for this software check: Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0.

### Remaining blockers

The archive still lacks the full candidate dataset, human-adjudicated labels, language audit, actual research-data run, empirical results, final manuscript PDF/source, repository commit and student demonstration. Therefore the package is a validated planning/code progress package, not a completed empirical paper.


## 8. Third audit — candidate acquisition and implementation hardening (30 October 2026)

### Added artifacts and code changes

- Added `code/collect_openalex_candidates.py`, `data/seed_papers.csv`, an annotation template, and the private/shareable collection instructions. The collector includes eight search routes, four topic routes, five year bands (2015–2025), seed DOI resolution and one-hop citation neighbourhoods; query parameters, URLs without API keys, timestamps, errors and manifests are logged. It does not assign labels.
- Changed the bootstrap unit to paired `duplicate_cluster_id` resampling, applied the frozen seed to both split and model, recorded input SHA-256/provenance declaration, prevented output overwrite and added a no-fit `--preflight-only` mode.
- The preflight report now records mechanical dataset checks and split counts without training either model. The provenance flag is explicitly a declaration, not authentication.
- Added four collector helper tests, two experiment integrity tests and one mocked collector integration test to the original three tests.

### Actual software verification

- `python -m pytest -q`: **10 passed**.
- `python -m py_compile code/run_experiment.py code/collect_openalex_candidates.py`: passed.
- Synthetic preflight-only check: passed all mechanical checks on the synthetic fixture and wrote gate report/split manifest/group profile; no estimator fitting occurred.
- Synthetic end-to-end check: completed with status `SOFTWARE_SMOKE_TEST_ONLY`; synthetic metrics were excluded from the research archive and are not findings.
- Exact environment versions are recorded in `requirements-tested-container.txt`; this is an isolated-container snapshot, not the student's machine.

### Limitations that remain

The live OpenAlex API collector was not executed because DNS resolution failed in this runtime. The actual candidate data, human annotations, duplicate decisions, publication-language verification, dataset gate, research baseline, experiment outputs, manuscript and repository commit remain outstanding. The current archive is a software-tested progress package, not an empirical paper.


## 9. Collector integration test addendum — 30 October 2026

- Added `tests/test_collection_integration.py`, which monkeypatches the OpenAlex transport and runs the collection orchestration without network access.
- Verified private abstract-bearing CSV vs abstract-free shareable CSV separation, pending human labels, raw/query log creation, and citation-neighbourhood request counts.
- Updated the suite result to **10 passed**. This test is an offline simulated response test, not a live OpenAlex collection.
- Collector manifest now records the number of logged requests and citation-neighbourhood requests, and returns a non-zero status if no records were collected.


## 10. Final package verification — 30 October 2026

The current working package was rechecked after the collector integration test and documentation updates. The nine-test milestone has been superseded by **10 passing tests**. The pilot CSV remains abstract-free; no synthetic run outputs, raw API records or private collection directories are packaged; relative Markdown links resolve; and the no-fit preflight path passed on a synthetic fixture. Final ZIP integrity and checksums are verified after archive creation and are reported in the hand-off message.
