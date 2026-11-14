# AI Assistance and Verification Log

**Project:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation  
**Student:** Aditya Chaudhary | **Enrollment:** MNS2026008  
**Updated:** 30 October 2026

This log records the assistance and checks completed so far. It is not a claim that all research materials or results have been independently verified.

## Recorded AI assistance

| Stage | Assistance provided | Student/action evidence | Verification boundary |
|---|---|---|---|
| Prompt 01 | Helped summarise the supplied review scope and maintain a decision log with VERIFIED/INFERRED/UNKNOWN/PENDING labels. | The supplied literature-review files were available in the working conversation; project decisions recorded in `research_decisions.md`. | Log claims are based on the supplied review and recorded source checks, not on an exhaustive review of all related work. |
| Prompt 02 | Proposed five computationally testable research gaps and a source-evidence-to-question-to-experiment matrix. | `gap_matrix.md`. | Gaps are candidates, not proof of novelty; the literature search is bounded and not systematic. |
| Prompt 03 | Compared three methods and pathways; proposed a CPU-feasible TF-IDF/logistic-regression feature ablation. | `Prompt03_Literature_to_Experiment_MNS2026008.md`. | No method has been reproduced and no src/model experiment has been run. Public repository existence is not the same as successful reproduction. |
| Prompt 04 | Drafted scholarly search strings, neighboring-work matrix, dataset/access/licensing audit, compute estimate and go/no-go decision. | `Prompt04_Feasibility_Novelty_Resource_Access_Report_MNS2026008.md` and personalized input. | Literature checking was targeted, not exhaustive. Dataset feasibility remains conditional; novelty is UNKNOWN. |
| SYNERGY metadata pilot | Generated/refined Colab cells for listing/export inspection, schema/missingness checks, language detection, citation grouping and crosstabs; fixed malformed print strings and broadened label parsing after user-reported errors. | The student executed commands in Colab and supplied outputs. See `Metadata_Pilot_Record_MNS2026008.md`. | The assistant did not execute the user's Colab runtime. Only supplied outputs are reported. `Hall_2011.csv` is a feasibility pilot, not the selected main dataset. |
| OpenAlex candidate pilot | Generated Colab query cells and sampling/summary code; interpreted user-provided outputs; helped define a preliminary screening rule and produce label explanations. | `OpenAlex_Candidate_Pool_Pilot_Record.md` and abstract-free 28-record workbook/CSV. | The user executed API calls. The 28 labels remain preliminary and are not independently adjudicated gold labels. Sampling was query-specific and not representative. |
| Prompt 05 | Drafted research problem, RQs/hypotheses, metrics, decision rules, limitations and references. | `research_problem_brief_MNS2026008.md` and personalized Prompt 05 input. | RQs remain conditional on dataset feasibility. Success thresholds and K must be frozen before held-out evaluation; no results are claimed. |
| Prompt 06 | Checked official OpenAlex API/field/search documentation, the SYNERGY repository, the Aigner et al. paper/repository, a 2026 Zenodo human-labelled screening benchmark, ASReview licensing, and scikit-learn split/model documentation. Compared the available data sources and specified the paired citation-blind/citation-aware ranker conditions, data split, metrics, access cautions and fallbacks. | `docs/06_Prompt06_Dataset_and_Baseline_Validation/Prompt06_Dataset_and_Baseline_Validation_Sheet_MNS2026008.md`. | The search was targeted, not an exhaustive systematic review. The final OpenAlex pool has not been constructed/validated, labels remain preliminary, and no model or ranking metrics have been run. Zenodo record file contents/language coverage/licence were not independently downloaded/confirmed; it is only an auxiliary candidate. |
| Prompt 07 | Prepared a frozen experimental blueprint with processing modules, Mermaid flowchart, input/output definitions, pool-construction and label protocol, grouped split, paired model settings, primary/secondary metrics, uncertainty method, resource budget, output schemas, ablation/error analysis, validity threats and protocol amendment procedure. Added a compact pre-experiment checklist and change log. | `docs/07_Prompt07_Frozen_Experiment_Blueprint/Prompt07_Frozen_Experiment_Blueprint_MNS2026008.md` and `docs/07_Prompt07_Frozen_Experiment_Blueprint/Prompt07_PreExperiment_Checklist_and_Change_Log_MNS2026008.md`. | Protocol planning is complete, but the data gate is open. The 28-record pilot is not eligible for main model training/evaluation. No experiment or result was run or fabricated. Software compatibility and runtime remain to be checked in Prompt 08. |
| Packaging | Consolidated files, aligned current status wording, created an abstract-free evidence copy and added this log. | This package. | Raw reconstructed abstract text was excluded. Prompt 07 protocol and checklist are included; dataset construction/acceptance, Prompt 08 environment test, model, experiment, final paper and full reproducibility repository remain pending. |

## Code/data verification status

- **User-run and output observed:** SYNERGY export and metadata pilot; OpenAlex topic/language queries; language-specific search queries; 67-record metadata sample; balanced 28-record pilot and its current workbook counts.
- **Assistant-authored code:** Colab snippets for API access and data inspection/sampling were drafted in chat and manually run by the user. The exact full execution environment, package versions, API response snapshots and response timestamps were not fully archived.
- **Code not yet run:** TF-IDF/logistic-regression ranker, citation-aware versus citation-blind feature ablation, ranking metrics, significance/uncertainty analysis, plots, full experiment scripts.
- **Labels:** six positive and 22 negative labels in the latest pilot workbook. The positive/negative decisions were made with AI assistance and should be audited. No second reviewer or inter-annotator-agreement analysis is recorded.
- **Access/licensing:** references and official sources were checked on a bounded basis and the relevant statuses are in Prompt 04. No repository installation/reproduction is claimed unless specifically documented.
- **Integrity:** no experiment metric, bias finding, p-value, reproduction success, or novelty conclusion has been fabricated. The exact novelty of the candidate contribution remains UNKNOWN.

## Current stop/go state

**CONDITIONAL GO** for continued dataset construction. **NO-GO** for training/evaluating the main model on the current 28-record sample. Next: build and audit the larger candidate pool, count relevant records by language/citation group, and record the data gate decision. The Prompt 07 protocol is frozen; proceed to Prompt 08 environment testing only after the dataset gate passes or the research question is formally narrowed under the documented fallback.


## Source-comparison update — 30 October 2026
- **AI assistance:** Compared candidate dataset source descriptions and drafted a candidate decision matrix; revised Prompt 04/05/06 consistency language and the research decision log.
- **Source pages checked:** OpenAlex API/search documentation; Mendeley Data record `x3nd2k9dkn/1`; CAIR-Nepal AI Bias Research Landscape page; Zenodo record `21853690`; ASReview SYNERGY repository.
- **Verified from source descriptions:** Mendeley page reports 1,190 retrieved unique records, 1,105 screened records, 531 included records, English-only search and CC BY 4.0; CAIR-Nepal page reports 692 records with publication years and OpenAlex-derived citation metadata; Zenodo page lists human-labelled screening sets of 440, 205 and 200 records in three non-target domains; OpenAlex documentation states CC0 data and documents that citation counts contribute to default relevance score.
- **Not independently verified in this stage:** actual downloads/full schemas of Mendeley, CAIR-Nepal and Zenodo files; CAIR-Nepal and Zenodo licence conditions; language distributions in those candidate files; final OpenAlex pool, independent labels, group counts and any model results. These remain UNKNOWN/PENDING.
- **Integrity rule:** No dataset access, code execution, label adjudication, environment test, model run, or experiment result is claimed by this source-page comparison.

## Additional verification update — 30 October 2026

- Tightened the relevance definition after inspecting the 28-row metadata-only pilot; broad protocol drafting alone is no longer treated as sufficient for a positive label.
- Added a targeted literature update for 2025–2026 work on scholarly recommender bias, OpenAlex language metadata, title/abstract screening, multilingual retrieval, scientific publication ranking, and AI-assisted evidence synthesis.
- Added the executable paired-ablation pipeline and input-validation tests. Three automated tests passed in the package environment. A separate end-to-end smoke test used synthetic data only; no synthetic metrics were retained as research findings.
- Aligned the pipeline with the frozen Prompt 07 grouped split, feature settings, model settings, fixed citation snapshot date, tie-break, K, bootstrap seed, and success rule.
- The main dataset, human adjudication, language audit, main model run, empirical manuscript and similarity-check report remain unavailable/not completed. No empirical findings are claimed.
