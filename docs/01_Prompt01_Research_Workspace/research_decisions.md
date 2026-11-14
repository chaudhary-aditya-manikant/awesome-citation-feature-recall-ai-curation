# Research Decisions Log

## Project
- **Working title:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation
- **Project stage:** Prompts 01–06 planning and validation artifacts completed; final dataset gate remains open; main model not run
- **Last updated:** 2026-10-30
- **Status vocabulary:** `VERIFIED`, `INFERRED`, `UNKNOWN`, `PENDING`

## Evidence-label policy
- **VERIFIED:** Directly supported by an inspected source, data artifact, or recorded experiment. State the scope of verification.
- **INFERRED:** A plausible interpretation or hypothesis that has not yet been established by the available evidence.
- **UNKNOWN:** Evidence is missing, inaccessible, ambiguous, or insufficient.
- **PENDING:** An action or decision has not yet been completed.

## Decision 001 — Inspect the existing review before defining the gap
- **Status:** VERIFIED — review files received and inspected.
- **Decision:** Use the supplied PDF, LaTeX source, and BibTeX file as the current source of truth for summarizing the review.
- **Reason:** Conclusions should be grounded in the submitted artifact rather than inferred from the title.
- **Source/evidence:** ZIP contents included `Aditya_Chaudhary_MNS2026008.pdf` (16 pages), `main.tex`, and `references.bib`, plus ACM template files.
- **Alternatives considered:** No gap or experiment was selected before document inspection.
- **Next actions:** Finish the targeted reference audit; assess how the original review searched for and selected prior work.

## Existing-review scope summary
- **Status:** VERIFIED — based on the supplied PDF and matching LaTeX source.
- **Review type:** Conceptual literature survey/synthesis; no new implementation experiment is reported.
- **Core concern:** Relevant AI papers may have unequal probabilities of being discovered, surfaced, screened, or retained based on citation prominence and publication language.
- **Framework:** Three interacting categories — citation-based mechanisms, language-based mechanisms, and pipeline-stage mechanisms.
- **Pipeline stages discussed:** Indexing, candidate generation, ranking, screening, citation chaining, retention, and synthesis.
- **Approaches discussed:** RobotAnalyst, ASReview, automated citation searching, scholarly recommender systems, semantic retrieval, and LLM-assisted screening.
- **Candidate evaluation ideas:** Group-conditional recall by citation stratum and language; citation-by-language interaction; separate candidate-generation recall from ranking exposure and screening recall; compare ranking with and without citation/popularity information; document provenance.
- **Explicitly non-empirical item:** The compounded-disadvantage diagram in the review is labeled conceptual/non-empirical.
- **Main limitation visible from inspection:** The review makes a strong claim that none of the empirical approaches summarized in its Table 2 report recall stratified by citation percentile or language, but the PDF does not provide a transparent, reproducible search protocol (databases, full search strings, date range, inclusion/exclusion criteria, deduplication, and screening flow) sufficient to treat that absence claim as exhaustive.
- **Next action:** Recover any search notes / search exports if they exist. Otherwise describe the review honestly as a conceptual synthesis and run a targeted, documented gap search before claiming novelty.

## Decision 002 — Treat the proposed gap as provisional, not established
- **Status:** INFERRED / PENDING empirical and literature validation.
- **Decision:** Frame the current opportunity as testing group-conditional recall and a citation-by-language interaction in a defined scholarly retrieval/curration task, rather than asserting that the whole field has ignored the issue.
- **Reason:** The review points to a plausible measurement gap, but a small comparative table without a reproducible search protocol cannot establish a field-wide absence. Related work already studies popularity bias in scholarly recommenders and language fairness in multilingual information retrieval.
- **Source/evidence:** Supplied review, Sections 6–8; preliminary external checks include Färber et al. (2023), Klimashevskaia et al. (2024), and multilingual IR work listed below.
- **Next actions:** Search for overlap using a documented protocol; distinguish (a) language fairness in multilingual IR, (b) popularity bias in recommendation/ranking, and (c) joint citation × publication-language recall disparity in AI literature curation.

## Preliminary reference verification
- **VERIFIED:** Färber, Coutinho, and Yuan, “Biases in scholarly recommender systems: impact, prevalence, and mitigation,” *Scientometrics* (2023), DOI `10.1007/s11192-023-04636-2`. Publisher page inspected: https://link.springer.com/article/10.1007/s11192-023-04636-2
- **VERIFIED:** Klimashevskaia et al., “A survey on popularity bias in recommender systems,” *User Modeling and User-Adapted Interaction* (2024), DOI `10.1007/s11257-024-09406-0`. Publisher page inspected: https://link.springer.com/article/10.1007/s11257-024-09406-0
- **VERIFIED:** Aigner et al., “Comparing supervised machine learning and large language models in title-abstract screening,” *Systematic Reviews* (2026), DOI `10.1186/s13643-026-03199-6`. Publisher page inspected: https://link.springer.com/article/10.1186/s13643-026-03199-6
- **VERIFIED:** Fleurence et al., “The Use of Generative Artificial Intelligence in Systematic Literature Reviews: A Rapid Review of the Literature,” *Value in Health* (online 2026), DOI `10.1016/j.jval.2026.06.012`. PubMed page inspected: https://pubmed.ncbi.nlm.nih.gov/42447981/
- **VERIFIED:** Rajit et al., “Automated citation searching in systematic review production: A simulation study,” *Research Synthesis Methods* (2025), DOI `10.1017/rsm.2024.15`. Publisher/PubMed pages inspected: https://www.cambridge.org/core/journals/research-synthesis-methods/article/automated-citation-searching-in-systematic-review-production-a-simulation-study/8B102232B819BB01644FB37BA1376CCA and https://pubmed.ncbi.nlm.nih.gov/41626901/
- **VERIFIED:** Nørgaard, Lie, and Lund, “Predictors of citation rates and the problem of citation bias: a scoping review,” DOI `10.1016/j.jclinepi.2025.112057`; online 2025, issue dated 2026. PubMed page inspected: https://pubmed.ncbi.nlm.nih.gov/41265666/
- **VERIFIED:** Hirt et al., “Guidance on terminology, application, and reporting of citation searching: The TARCiS statement,” *BMJ* (2024), DOI `10.1136/bmj-2023-078384`. Publisher page inspected: https://www.bmj.com/content/385/bmj-2023-078384
- **VERIFIED — directly relevant overlap to include in next search:** Yang et al., “Language Fairness in Multilingual Information Retrieval” (SIGIR 2024), DOI `10.1145/3626772.3657943`, and Yang, Jiang, and Baldwin, “Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods” (MRL 2024), DOI `10.18653/v1/2024.mrl-1.23`. This means language fairness in general IR is established related work; the precise joint gap for AI-paper curation remains UNKNOWN.
- **Audit scope caution:** These are targeted checks, not a complete audit of all references in `references.bib`; the remaining references and the accuracy of every sentence-level claim remain PENDING.

## Research gap and novelty
- **Proposed gap:** UNKNOWN pending a reproducible targeted literature search.
- **Candidate contribution (INFERRED):** A controlled audit of how citation prominence and publication language jointly relate to retrieval/retention of relevant AI papers, with explicit age/topic controls and stage-separated metrics.
- **Evidence against novelty / related work:** Popularity bias in scholarly recommendation is covered by Färber et al. (2023) and Klimashevskaia et al. (2024); language fairness in multilingual IR is studied by Yang et al. (2024). The overlap between those literatures and group-conditional recall specifically in AI-paper curation needs investigation.
- **Next action:** Record databases, search strings, search dates, deduplication and screening criteria; build a paper-by-paper comparison matrix before writing a novelty claim.

## Research questions and hypotheses

**Historical note:** The initial entries below were pending before Prompt 05 was prepared. They are superseded by Decision 006 near the end of this log and by `research_problem_brief_MNS2026008.md`.

- **Current primary RQ (INFERRED, conditional on data gate):** On a fixed, relevance-labelled candidate pool, does adding the explicit `log1p(cited_by_count)` feature change pool-relative Recall@K for lower-citation relevant records compared with an otherwise identical ranker without that feature?
- **Current secondary RQ (INFERRED):** Does removing the citation feature change the recall gap between pre-defined lower- and higher-citation groups?
- **Conditional language RQ (INFERRED / PENDING adequate positives):** Does the feature effect differ between English and non-English metadata-language groups if each has enough relevant test records and language labels are suitably checked?
- **Operational definitions:** See Prompt 05 brief. The candidate pool, labels, citation grouping and language metadata are not yet validated for the main experiment.
- **Next action:** Prompt 06 dataset and comparator verification before training.

## Data and methods
- **Feasibility-pilot dataset and provenance:** **VERIFIED, bounded to the notebook output.** SYNERGY+ v3.0 collection `Hall_2011.csv`, exported with title, abstract, citation-count, publication-year, language, and inclusion-label fields. Final Colab path recorded in `Metadata_Pilot_Record_MNS2026008.md`.
- **Pilot collection size:** **VERIFIED:** 340 records, 10 columns; title, abstract, `cited_by_count`, `publication_year`, `label_included`, and `language` were non-missing for all 340 records in the notebook output.
- **Pilot relevance labels:** **VERIFIED:** `label_included=1` for 4 records and `0` for 336. These are review-specific inclusion labels, not universal AI-literature relevance judgements.
- **Pilot language distribution:** **VERIFIED:** explicit `language` value `en` on 340/340 records. There are no non-English records in this selected collection; language-field accuracy was not independently validated against full text.
- **Main experiment dataset:** **NOT SELECTED.** `Hall_2011.csv` is unsuitable as the sole main dataset for the planned joint citation-by-language AI-literature experiment because it has no non-English group, only four inclusion-positive records, and its AI-literature scope is not established.
- **Baseline / model:** **PENDING.** No model has been trained.
- **Implementation status:** Metadata feasibility pilot executed; main ranking experiment not started.
- **Next action:** Find an on-topic AI-literature pool with adequate label and language-group coverage; verify actual positive counts and group denominators before model training.

## Experiments and results
- **Experiment configuration run:** Metadata feasibility pilot only. The notebook loaded `/content/synergy_dataset_with_text_metadata/Hall_2011.csv` and reported schema/missingness, language counts, inclusion-label counts, a citation median split, and crosstabs.
- **Execution evidence:** **VERIFIED from saved notebook outputs:** 340 records; all six required columns non-missing; `language=en` for all 340; labels `0=336`, `1=4`; citation median 11.0; at/below median 174 records (1 included-labelled); above median 166 records (3 included-labelled).
- **Main experiment results:** NONE. No ranking model, citation-feature ablation, group-conditional recall evaluation, or hypothesis test has been run.
- **Interpretation and limitations:** The pilot dataset cannot support an English/non-English comparison, and four included-labelled records are inadequate for stable recall estimation. The citation counts are descriptive and potentially age-dependent. Do not infer causal citation bias from these crosstabs.
- **Detailed record:** `Metadata_Pilot_Record_MNS2026008.md`.
- **Rule:** Never enter a metric or describe a main experiment as run without inspectable execution output and configuration.

## Reproducibility
- **Code repository / commit:** UNKNOWN.
- **Environment and dependencies:** PENDING.
- **Data acquisition and access instructions:** PENDING.
- **Random seeds and configurations:** PENDING.
- **Next action:** Record these once an implementation and experiment protocol exist.

## Change history
- **2026-10-20:** Initialized project log before review was inspected.
- **2026-10-20:** Inspected the uploaded 16-page PDF, LaTeX source, and bibliography; summarized the review as a conceptual synthesis with a proposed empirical measurement gap. Marked the gap provisional because no reproducible search protocol is evident in the supplied document.
- **2026-10-20:** Verified selected reference metadata on publisher/PubMed/ACL pages. Identified existing related work on scholarly popularity bias and language fairness in multilingual IR. No project experiment has been run; no dataset, baseline, or metric result has been asserted.

## Decision 003 — Record five computationally testable gaps
- **Status:** INFERRED / awaiting feasibility checks.
- **Decision:** Prioritize (1) joint citation-by-language group-conditional recall, (2) popularity-blind citation-signal ablation, and (3) stage-separated attrition measurement. Keep multilingual expansion and active-learning seed composition as further experiments.
- **Reason:** These align closely with the review's stated problem and can be tested with a narrow AI subfield if a defensible relevant-paper denominator and inspectable pipeline outputs can be obtained.
- **Specific review evidence:** Table 2 (PDF p. 10); Sections 7.1–7.6 (pp. 11–12); Sections 8.1–8.8 (pp. 12–15); Equations (2), (9), and (10); Figures 3 and 4.
- **Key uncertainty:** The review's selected Table 2 does not establish field-wide novelty. Citation × language interaction is a candidate question, not a verified novel contribution.
- **Next action:** Inspect search records/screening outputs if available; select one narrow AI topic; identify a viable labeled corpus before baseline selection.

## Targeted original-publication audit — 2026-10-20
- **VERIFIED:** Przybyła et al. (2018) RobotAnalyst reports an evaluation on 22 reference collections and workload reductions to 95% recall on 19; reports user complacency and stopping-criterion concerns. Original record: https://pmc.ncbi.nlm.nih.gov/articles/PMC6175382/
- **VERIFIED:** Rajit et al. (2025) evaluates one-hop OpenAlex/Semantic Scholar automated citation searching on 27 reviews from health, environmental management, and social policy, not an AI paper corpus. Authors report higher precision/F1 but lower recall/F3 than the reference search and discuss API/identifier coverage and imperfect reference-standard assumptions. https://www.cambridge.org/core/journals/research-synthesis-methods/article/automated-citation-searching-in-systematic-review-production-a-simulation-study/8B102232B819BB01644FB37BA1376CCA
- **VERIFIED:** Aigner et al. (2026) compares four TF-IDF-based supervised methods and Llama-3.1-8B-Instruct on six labelled systematic-review datasets. The original limitations include fixed prompting, retrospective-data/pretraining overlap risk, metadata noise/duplicates, subjective human labels, and non-English abstract filtering in data preparation. It is not a direct multilingual-recall evaluation. https://link.springer.com/article/10.1186/s13643-026-03199-6
- **VERIFIED:** Fleurence et al. (2026) is a rapid review of 115 studies of GenAI across systematic-review tasks, not a single AI-paper retrieval benchmark. https://pubmed.ncbi.nlm.nih.gov/42447981/
- **VERIFIED:** Duyx et al. (2017) meta-analyzes 52 studies of outcome-related citation bias; it supports the plausibility that citation rates reflect processes beyond relevance, but does not measure literature-retrieval recall. https://pubmed.ncbi.nlm.nih.gov/28603008/
- **VERIFIED — table-entry caution:** Wang & Blei (2011) proposes collaborative topic modeling combining collaborative filtering and topic modeling on CiteULike data. Its introduction criticizes citation-following for favoring highly cited papers. The review's Table 2 may conflate this criticism with the proposed model; verify before calling the proposed model itself popularity-biased “by design.” https://www.cs.columbia.edu/~blei/papers/WangBlei2011.pdf
- **VERIFIED:** Färber et al. (2023) and Klimashevskaia et al. (2024) are surveys/taxonomies of scholarly recommender bias and popularity bias; treat them as prior synthesis, not direct empirical tests of the project's joint recall hypothesis. https://link.springer.com/article/10.1007/s11192-023-04636-2 and https://link.springer.com/article/10.1007/s11257-024-09406-0
- **UNKNOWN:** Whether all references and all sentence-level summaries in the supplied review are accurate. The audit remains targeted, not exhaustive.

## Methodological claims to revise or qualify
- Narrow “none of the systems report…” to “none of the empirical systems in the selected comparison table report…” unless a documented wider literature search supports the broad claim.
- Rephrase the statement that “most systems report only final screening recall”: Table 2 combines stage-heterogeneous tasks, including citation retrieval and reviews of GenAI applications, so consistent stage-by-stage comparison is not currently established.
- Treat early-label/seed composition bias in ASReview as an inferred mechanism until an original source explicitly reports and tests it.
- Do not present evidence from health/environmental/social-policy systematic reviews as direct evidence of recall disparities in AI paper retrieval.

## Change history (additional)
- **2026-10-20:** Completed targeted checks of original RobotAnalyst, Rajit et al., Aigner et al., Fleurence et al., Duyx et al., Wang & Blei, Färber et al., and Klimashevskaia et al. Distinguished original-author-reported limitations from project-level hypotheses.
- **2026-10-20:** Drafted five computational gaps and ranked a group-conditional recall audit, popularity-signal ablation, and stage-separated attrition audit as the three strongest initial directions. No dataset or experiment selected/run.

## Decision 004 — Record SYNERGY metadata feasibility pilot
- **Date:** 2026-10-29
- **Status:** VERIFIED for observed export/schema/counts; INFERRED for suitability interpretation.
- **Decision:** Preserve `Hall_2011.csv` as a feasibility and pipeline pilot only. Do not use it alone for the planned AI-literature citation-by-language main experiment.
- **Observed evidence:** The final exported CSV has 340 rows and 10 columns. The notebook shows 340/340 non-missing title, abstract, citation-count, publication-year, inclusion-label, and explicit language values. Labels are `0=336`, `1=4`. Language metadata is `en` for all 340 rows. Citation median is 11.0: 174 records are at/below median (1 included-labelled), and 166 are above median (3 included-labelled).
- **Reason:** There are no non-English records and only four included-labelled records. The selected review's topic fit to AI-literature curation is not established. Group recall for English versus non-English is not estimable from this collection; the positive-label count is too small for stable recall estimates.
- **Alternative rejected for now:** Train the planned citation-aware/citation-blind model on this collection. This would not answer the language-comparison question and risks overinterpreting a four-positive sample.
- **Permitted use:** Document as a genuine feasibility/pipeline pilot. Do not claim this result demonstrates bias, tests the main hypothesis, or establishes novelty.
- **Next action:** Build or select a bounded AI-literature pool; document provenance, relevance labels, language metadata validation, citation snapshot/date, and subgroup denominators before model training.
- **Detailed evidence:** `Metadata_Pilot_Record_MNS2026008.md`, based on saved outputs in the student-retained Colab notebook `Recall_Bias_Metadata_Pilot (4).ipynb`. The notebook is not included in this archive because it contains reconstructed abstract plaintext; the pilot results are summarized in the evidence record.



---

# Decision update after OpenAlex candidate-pool pilot (30 October 2026)

## Current state

The earlier SYNERGY metadata pilot is retained as a completed feasibility check. `Hall_2011.csv` had 340 records, four review-included labels, and all 340 explicit language values were `en`. It is a **NO-GO as the sole dataset** for the intended joint citation/language experiment.

The user then successfully queried OpenAlex from Google Colab. Broad topic filters showed multilingual work metadata in the investigated topic areas. Topic and language-specific query counts varied substantially by query. In the tested language-specific search configuration, reported matching counts were 49 English, 13 Indonesian, 262 Portuguese, and 356 Spanish. A retrieved sample contained 67 unique records (20 English, 7 Indonesian, 20 Portuguese, 20 Spanish); all had non-missing title, publication year, citation count, language, and abstract fields in the output checks, and the observed language codes agreed with the selected language filters.

A balanced 28-record pilot was then created with seven records per group. The current labelled workbook contains six preliminary relevant labels and 22 preliminary non-relevant labels: English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6. These labels are AI-assisted preliminary judgements and should be human-audited against the written screening rubric before use as final ground truth.

## Updated status labels

- **VERIFIED:** OpenAlex API queries executed in Colab; a 67-record metadata sample was created; the 28-record balanced pilot has 28 binary labels in the current workbook; the tested metadata fields were non-missing in those 67 records.
- **INFERRED:** OpenAlex is a promising candidate metadata source, but the current query and annotation pilot does not constitute a representative or sufficiently labelled benchmark for the main experiment.
- **UNKNOWN:** Whether a better-defined, larger and deduplicated AI-literature pool can yield enough human-verified relevant papers within each citation and language group; whether metadata language agrees with publication language for each candidate; and whether the current search routes adequately represent records a target retrieval workflow would return.
- **PENDING:** Build and verify a larger candidate pool under a pre-specified protocol; audit labels; calculate positive counts by subgroup; then decide whether language-stratified recall is estimable.

## Current decision

**CONDITIONAL GO for continued data construction; NO-GO for training/evaluating the main model on the current 28-record sample.** The sample has only six preliminary positives and none in Indonesian; it was constructed with separate language-specific queries and should not be used to infer natural prevalence or demonstrate bias. Do not treat the positive counts as independently validated gold labels.

## Next actions

1. Freeze one narrow target task/subtopic and publication-year range.
2. Pre-specify multilingual query strings and at least one complementary candidate-discovery route if feasible; retain search date, query, route and identifiers for each record.
3. Deduplicate before annotation and create a written inclusion/exclusion guide.
4. Human-review the preliminary labels and record a short reason for every inclusion/exclusion. Preserve unresolved items as uncertain until evidence resolves them; do not force binary labels for convenience.
5. Build a larger pool and count relevant records by language and citation group. If language subgroup positives remain sparse, mark that analysis exploratory/not estimable or narrow the project to citation-aware versus citation-blind ranking.
6. Prompt 04 feasibility assessment has now been finalized in `Prompt04_Feasibility_Novelty_Resource_Access_Report_MNS2026008_FINAL.md` with a CONDITIONAL GO / current-pilot NO-GO decision. Prompts 05 and 06 have since been completed. The next gate is to construct and audit the larger candidate pool, then freeze the experimental protocol in Prompt 07 only if the data-feasibility criteria are met.

## Research integrity note

The 28-record pilot is feasibility evidence only. It does not establish that citation or language bias exists, does not provide a complete universe of relevant papers, and is not sufficient for a main-model evaluation. Labelled work is preliminary; OpenAlex language should be described as metadata language unless publication language is independently checked. Keep reconstructed abstracts local and follow data source terms when sharing outputs.


## Decision 005 — Finalize Prompt 04 deliverable and transition to Prompt 05 (30 October 2026)

- **Status:** VERIFIED that the report deliverable is complete; INFERRED that the planned model remains computationally feasible; UNKNOWN whether a sufficiently labelled multilingual pool can be built within the time budget.
- **Prompt 04 output:** `Prompt04_Feasibility_Novelty_Resource_Access_Report_MNS2026008_FINAL.md` and the personalized Prompt 04 input file are finalized.
- **Decision:** CONDITIONAL GO for continued project planning and dataset construction; NO-GO for training/evaluating the main model on the current 28-record pilot. The assessment is complete even though the data-feasibility gate is not passed.
- **Updated evidence:** OpenAlex topic and language-specific queries were executed; a 67-record sample had non-missing sampled metadata fields; a 28-record stratified pilot was labelled preliminarily with six `1` and 22 `0` labels (English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6). These labels remain AI-assisted and not independently validated.
- **Additional caveat:** The installed SYNERGY package/export showed `Hall_2011.csv`, while the current public SYNERGY README lists `Hall_2012` as its Computer Science collection. The package/version/name relationship remains UNKNOWN.
- **Next action:** Proceed to Prompt 05 to define the research problem, RQs and success criteria conditionally. Do not train the model until Prompt 06's dataset/comparator checks and the label/group adequacy gate pass.


## Decision 006 — Frame research questions and success criteria (Prompt 05, 30 October 2026)

- **Status:** Prompt 05 research brief drafted; data feasibility remains conditional.
- **Decision:** Keep the primary candidate study as a controlled feature ablation: TF–IDF title/abstract + publication year + `log1p(cited_by_count)` versus the same model without the citation-derived feature. Logistic-regression scores would be used to rank the fixed candidates; this is a ranker built from a relevance classifier, not a claim that logistic regression is a dedicated learning-to-rank method.
- **Primary outcome:** Pool-relative Recall@K for pre-defined lower-citation relevant records, with overall Recall@K and Precision@K as guardrails. The value of K and decision rules must be frozen before held-out evaluation.
- **Secondary outcomes:** Change in the lower-vs-higher citation recall gap; language-group recall only if metadata language is checked and the final test pool has adequate positive counts. The language field will be called “metadata language” unless publication language is independently verified.
- **Evidence basis:** The source-backed adjacent work is listed in `gap_matrix.md`, Prompt 03, and Prompt 04. The pilot results below are observations from user-run Colab outputs and preliminary labels; they are not results of the main experiment.
- **VERIFIED — bounded pilot evidence:** SYNERGY `Hall_2011.csv` contained 340 records, four review-included labels, and all 340 language codes `en`; it is unsuitable as the sole dataset for a multilingual AI-curation study. The OpenAlex metadata sample had 67 unique records with required metadata non-missing. A later balanced 28-record sample contains six preliminary positive labels and 22 negative labels (English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6).
- **INFERRED:** OpenAlex is a promising candidate source but the current query-specific pilot is not a validated, representative or sufficiently labelled benchmark.
- **UNKNOWN:** Exact novelty; whether a larger on-topic pool can produce enough verified positive cases by citation and language group; whether all metadata-language labels match publication language.
- **PENDING:** Human-audit pilot labels, build a pre-specified larger candidate pool, document query routes/date/deduplication, establish label quality and subgroup denominators, Prompt 06 validation is complete; proceed to Prompt 07 only after the larger pool and subgroup denominators pass the data-feasibility criteria.
- **Research integrity:** No main model was trained. No ranking, group-recall, or bias result is claimed. The 28-record labels remain preliminary and were not independently adjudicated by a second reviewer.


## Decision 007 — Verify datasets and comparators (Prompt 06, 30 October 2026)

- **Prompt 06 deliverable:** `docs/06_Prompt06_Dataset_and_Baseline_Validation/Prompt06_Dataset_and_Baseline_Validation_Sheet_MNS2026008.md`.
- **Decision:** OpenAlex remains the preferred source for constructing a bounded candidate pool because the source provides citation, year and detected metadata-language fields. This is a conditional data-source recommendation, not a declaration that the final dataset has passed validation.
- **Current dataset gate:** NO-GO for training or evaluating the main model on the 28-record pilot. It has six preliminary positive labels and 22 negatives: English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6. Group recall for Indonesian is not estimable from this sample because there are no positive records in that group. The balanced group quotas were set by the pilot design and do not estimate real-world language prevalence.
- **Alternatives checked:** SYNERGY has human-labelled, review-specific screening data and is appropriate for pipeline tests, but its review criteria do not match the project's task automatically. The current official SYNERGY README lists `Hall_2012` as a Computer Science review; the earlier local `Hall_2011.csv` artifact (340 rows, four included, all `en`) has not been reconciled to that public entry. A new Zenodo human-labelled screening benchmark has 440 ML-in-concrete records, 272 relevant and 168 irrelevant; it is a separate materials-science screening task and has not been verified as multilingual or licensed for redistribution. Aigner et al. (2026) provide a close TF-IDF/classical-model method reference, but their published preprocessing excluded non-English abstracts.
- **Baseline pair:** (A) citation-blind TF–IDF title/abstract + publication-year feature with Logistic Regression; (B) identical model and data plus `log1p(cited_by_count)`. This paired comparison changes one citation-derived feature. A separate ASReview active-learning comparison is optional and not required for the minimum viable experiment because it changes the workflow rather than isolating the citation feature.
- **Important construction control:** OpenAlex's default text-search relevance score includes citation count. The final pool must not be built solely from default top-ranked search results. Record query route, filter, random sample seed, deduplication and retrieval date; report pool-relative recall only.
- **Access/language conditions:** OpenAlex metadata is documented as CC0, but reconstructed plaintext abstracts must remain local and must not be included in the shared package. Its language field is inferred from metadata and may be inaccurate; validate a sample against publication text or a reliable source and use the term “metadata language” unless the actual publication language has been checked. Freeze the citation snapshot date because citation counts change.
- **VERIFIED:** Official sources for OpenAlex fields/search/access, SYNERGY's schema and CC0 statement, Aigner et al.'s published method and repository, the Zenodo benchmark description, ASReview's software licence, and scikit-learn's Logistic Regression documentation were checked on 30 October 2026. The user's actual Colab outputs are recorded separately in the evidence folder.
- **INFERRED:** A small TF–IDF/Logistic Regression model is computationally feasible on CPU; the main resource burden is construction and quality control of the labelled pool.
- **UNKNOWN/PENDING:** Whether a larger, narrow, relevance-labelled pool will contain enough verified positive records per language and citation group; whether the final language groups are adequately validated; exact novelty.
- **Next gate:** Fix scope and years (recommended 2015–2025 for the main data freeze), build and deduplicate a larger pool, audit labels and language metadata, count relevant test records by group, then freeze the protocol in Prompt 07 only if the subgroup plan is defensible. If non-English positives remain sparse, keep the citation-feature comparison and report language metrics as exploratory/not estimable rather than claiming a language effect.


## Decision 008 — Freeze the operational scope used for the pilot (30 October 2026)

- **Decision:** For consistency across the OpenAlex pilot and Prompts 03–06, the target literature is research on computational/AI methods for scholarly-literature discovery and curation: search, citation searching, ranking, title/abstract screening, study selection, and systematic-review automation. It is not all AI application research.
- **Reason:** The actual query strings and preliminary labels target this narrow task. Changing the scope now to all AI publications would invalidate the existing labels and require a new dataset/rubric.
- **Status:** Operational scope is fixed for planning. The 28-record pilot is still too small and its labels are preliminary; scope clarification does not make it an adequate evaluation dataset.
- **Next gate:** Build a larger candidate pool with a documented, multi-route collection protocol, validate labels and language metadata, and count positives by language/citation group before model training.


## Decision 009 — Freeze experiment blueprint (Prompt 07, 30 October 2026)

- **Prompt 07 output:** `docs/07_Prompt07_Frozen_Experiment_Blueprint/Prompt07_Frozen_Experiment_Blueprint_MNS2026008.md` and `docs/07_Prompt07_Frozen_Experiment_Blueprint/Prompt07_PreExperiment_Checklist_and_Change_Log_MNS2026008.md`.
- **Status:** protocol specification frozen; data acceptance gate remains open. This is not evidence that the main experiment has run.
- **Frozen primary design:** Condition A is TF–IDF title/abstract plus publication year and Logistic Regression; Condition B is identical except for the addition of standardized `log1p(cited_by_count)`. The primary metric is lower-citation pool-relative Recall@K with `K = ceil(0.20 × N_test)`.
- **Frozen controls:** multi-route OpenAlex pool construction; 2015–2025 publication window; deduplication/version grouping before split; label and metadata-language audit; fixed grouped split seed `20261030`; same records and settings for both rankers; train-only preprocessing; paired bootstrap seed `20261031`; primary success and precision guardrail; predeclared ablation/error analysis and resource reporting.
- **Mandatory stop condition:** do not train or inspect comparative test results on the existing 28-record pilot. The larger pool must have adjudicated labels and at least 20 relevant lower-citation and 20 relevant higher-citation test records for confirmatory citation-group analysis. Confirmatory English/non-English analysis additionally requires at least 20 relevant test records in each group and language validation. These are operational gates for this project, not universal statistical guarantees.
- **Expected outputs:** dataset/split manifests, test predictions, primary/subgroup/resource metrics, dataset profile and comparison tables, figures, error-analysis CSV, run log and environment record. They must be generated by actual execution; no result values have been created or anticipated.
- **VERIFIED:** Prompt 07 official assignment asks for a reproducible blueprint, precise inputs/outputs, modules, preprocessing, Mermaid diagram, partitions, controls/settings, metrics and direction, seeds, budget, expected output formats, at least one deeper analysis, validity threats, pre-experiment checklist, and a protocol-change process. These components are included in the deliverables.
- **UNKNOWN/PENDING:** whether the larger candidate pool will pass the data gate; final label quality and subgroup denominators; actual software compatibility/runtime; all empirical results; exact novelty.
- **Next permitted phase:** Prompt 08 environment check only after dataset construction and the gate decision are recorded. If data feasibility fails, follow the predeclared fallback/narrowing rule; do not change the protocol to chase a favourable result.


## Decision 007 — Source comparison after pilot (30 October 2026)
- **Status:** VERIFIED source-page properties; final dataset **PENDING**.
- **Decision:** Retain a bounded OpenAlex pool as the primary data-source strategy for the unchanged literature-curation question. Do not treat the source selection as final dataset acceptance.
- **Evidence:** OpenAlex provides citation/year/language and title/abstract-index metadata under CC0, but has no project-specific relevance labels and its default search relevance score includes a citation component. Mendeley Data has 1,105 screened records and 531 review-specific inclusions but is English-only and concerns AI decision support in higher education rather than literature curation. CAIR-Nepal's AI Bias Research Landscape has 692 records and citation metadata but no reported project-specific relevance labels; language distribution and licence text still require actual-file/source verification. The Zenodo labelled benchmarks concern other domains. The executed SYNERGY `Hall_2011.csv` pilot has 340 rows, four positives and all `en` language values.
- **Consequence:** Prompt 04 has been revised and a candidate-comparison matrix added. Prompt 05/06 now state the conditional dataset status consistently. Prompt 07's protocol remains frozen as a method, but no model/environment work should be represented as complete and model training remains blocked until the acceptance gate passes.
- **Guardrails:** Do not claim bias, novelty, a validated multilingual benchmark, or main model results. Do not redistribute reconstructed abstract plaintext. Language subgroup analysis is confirmatory only if the final human-verified positive denominators and language audit pass the Prompt 07 gate.
- **Primary source links:** https://help.openalex.org/api/ ; https://help.openalex.org/api/searching/ ; https://data.mendeley.com/datasets/x3nd2k9dkn/1 ; https://www.cair-nepal.org/publications/datasets/ai-bias-research-landscape/ ; https://zenodo.org/records/21853690 ; https://github.com/asreview/synergy-dataset

## Decision update — 30 October 2026

The project title has been narrowed to **Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation**. Language remains a conditional descriptive analysis rather than a co-primary claim. A stricter annotation rubric is required because some preliminary pilot positives were broader AI-assisted review workflow records rather than direct literature-curation methods. The current 28-row pilot remains ineligible for modelling. The code and software tests are now present, but the full dataset and actual experiment are still pending. Novelty remains unknown after targeted checks of closely related 2025–2026 work.


## Decision 010 — Software implementation hardening and acquisition path (30 October 2026)

- **Completed:** added the bounded OpenAlex candidate collector; exact seed DOI list; human annotation template; cluster-aware duplicate grouping; private/shareable export separation; route/query/time logs; and offline tests.
- **Completed:** hardened the experiment implementation with paired cluster bootstrap, explicit synthetic-run status, input SHA-256, passed-through model seed, no-overwrite run directories, numeric validation, and a preflight-only data gate.
- **VERIFIED (software only):** 10 tests pass; both Python scripts compile; synthetic preflight and synthetic end-to-end smoke tests complete. The smoke test output is not research evidence.
- **UNKNOWN/PENDING:** live OpenAlex collection, final candidate count, human relevance labels, canonical duplicate decisions, validated publication language, accepted data gate, actual research baseline and main results.
- **Network limitation:** the current audit runtime could not resolve the OpenAlex API host. The collector is included and offline-tested, but its live execution must be performed in a network-enabled student environment.
- **Protocol amendment A1:** bootstrap now resamples whole duplicate/version clusters in paired fashion; configured seed is applied to estimator; preflight mode separates data-gate review from model fitting. No primary research question, held-out fold, metric or success rule changed.
- **Next action:** perform live collection, annotation, duplicate and language audits in the ordered sequence in `docs/NEXT_ACTIONS.md`. Do not enter Prompt 10 research validation until the actual candidate dataset passes the manual and mechanical gates.
