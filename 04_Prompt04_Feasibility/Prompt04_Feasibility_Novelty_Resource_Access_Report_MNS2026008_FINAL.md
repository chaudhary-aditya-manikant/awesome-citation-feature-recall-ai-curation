> **POST-PILOT REVISION — 30 October 2026.** This report has been reconciled against the executed SYNERGY and OpenAlex pilots and a source-checked comparison of alternative data candidates. The selected strategy is a bounded, independently labelled OpenAlex pool focused on literature-curation methods. This is **CONDITIONAL GO for dataset construction only** and **NO-GO for main-model training until the Prompt 07 dataset acceptance gate passes**. The full candidate comparison and source-specific limitations are in [Prompt 04 Dataset Candidate Comparison and Decision](Prompt04_Dataset_Candidate_Comparison_and_Decision_MNS2026008.md). The source choice is selected; the final labelled dataset is not yet validated.

# PROMPT 04 — FINAL FEASIBILITY, NOVELTY AND RESOURCE-ACCESS REPORT

**Student:** Aditya Chaudhary  
**Enrollment number:** MNS2026008  
**Course:** AI Tools for Research  
**Project:** *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*  
**Evidence-check date:** 30 October 2026 (finalized after the SYNERGY and OpenAlex pilot runs)  
**Scope:** A bounded, source-checked feasibility and novelty assessment of the reviewed literature, candidate methods, dataset/API access, license evidence, and the user-run SYNERGY/OpenAlex pilots. This is not an exhaustive systematic novelty review.

**Operational scope for the pilot:** the target papers are studies/resources that directly examine computational or AI methods for scholarly-literature discovery and curation (retrieval, citation searching, ranking, title/abstract screening, study selection, and systematic-review automation). This is narrower than all AI application literature, and it is the scope used for the existing pilot labels. A change to a general AI-domain corpus would require a new eligibility rubric and relabelling.


## 1. Decision summary

**Revised Prompt 04 decision: CONDITIONAL GO for constructing and auditing a bounded OpenAlex pool; NO-GO for training or evaluating the main model on the current 28-record pilot.** The final data source strategy is selected, but the final labelled dataset is not validated. See the companion dataset-candidate comparison and decision matrix for Mendeley, CAIR-Nepal, Zenodo and SYNERGY alternatives. CPU-only implementation of the proposed lightweight ranker appears feasible, but the required candidate pool, labels, and group counts have not passed the data-feasibility gate.

The following priorities remain provisional:

1. **Gap 1 (core measurement):** pool-relative recall by citation group and language group, only if a suitably sized and relevance-labelled pool can be built.
2. **Gap 4 (main experiment):** compare a lightweight citation-aware ranker with an otherwise identical citation-blind ranker, removing one citation-derived feature.
3. **Gap 3 (by-product):** log ranking-stage loss only where the required candidate and ranking logs exist.
4. **Gap 2 (exploratory):** analyse a citation-by-language interaction only if relevant-paper counts support interpretable estimates.

**Pilot evidence recorded:** A SYNERGY-package export named `Hall_2011.csv` was inspected and rejected as the main dataset: 340 records, four review-included records, all 340 language-field values `en`, and no established fit to AI-literature curation. The current public SYNERGY README lists `Hall_2012` (Computer Science) among its collections rather than `Hall_2011`; the discrepancy between the installed/downloaded package listing and current public repository version has not been reconciled, so the names should not be assumed equivalent. OpenAlex topic and language-specific queries were then tested. In the 67-record export, all records had nonempty title, year, citation count, language field, and locally reconstructed abstract; the language codes matched the groups assigned by the query. A balanced 28-record pilot was created (seven English, seven Indonesian, seven Portuguese and seven Spanish). In the latest working color-preserved workbook, six records are labelled relevant (`1`) and 22 not relevant (`0`): English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6. These are AI-assisted/preliminary screening decisions, including a borderline Portuguese case provisionally assigned `1`; they are **not independently validated gold-standard labels**.

The results indicate that OpenAlex is a promising *metadata/candidate source to investigate*, but **the present 28-record sample is not suitable for the main experiment**. It has only six preliminary positives, no positive Indonesian records, one each in Portuguese and Spanish, and was assembled from separate language-specific search strings. It must not be treated as representative of natural group prevalence or as an unbiased common-frame retrieval benchmark. Search queries and pool-construction routes must be frozen and documented before outcome evaluation; relevance labels must be checked against a written criterion, with uncertainty/disagreement recorded. If sufficient non-English positives cannot be obtained, the language comparison must be marked exploratory/not estimable and the main experiment narrowed to citation-group ranking only if the citation-group positive counts are adequate.

The broad subject is not new. Previous work has studied citation effects in Google Scholar ranking, language effects in scholarly search, popularity bias in scholarly recommender systems, and language fairness in multilingual information retrieval. The defensible contribution remains a transparent, controlled single-feature ablation with group-conditional evaluation on a bounded, documented pool. **Novelty remains UNKNOWN** until a more comprehensive literature search and close reading of the closest methods are completed.

The recommended primary data strategy is a **bounded AI-literature-curation pool collected through OpenAlex and independently labelled**. This is a source-strategy decision, not final dataset acceptance; the pilot gate has not passed for the main experiment. SYNERGY `Hall_2011.csv` may be retained only as a documented feasibility/pipeline pilot, not as the primary dataset for the intended AI-specific language comparison.

### Evidence status conventions

- **VERIFIED — bounded:** supported by a primary publication page, official repository, or official documentation for the specific claim stated.
- **INFERRED:** a design recommendation or interpretation that must be tested.
- **UNKNOWN:** cannot be settled without additional inspection, data, or execution.
- **PENDING:** a future task or check that must be completed before the main experiment; pending items do not mean this feasibility report is unfinished.

**Label caveat:** The current pilot workbook is a feasibility annotation sheet. “Relevant” labels are operational decisions based on this project's rubric, not factually inherent labels. A human needs to audit these decisions before they serve as evaluation ground truth; a second reviewer on a subset is preferable if feasible.

## 2. Novelty verification and closest related work

### Search process

**Date:** 29–30 October 2026.  
**Sources checked:** publisher pages (Springer Nature), ACL Anthology, the MDPI journal page, official GitHub repositories, SYNERGY dataset documentation, and OpenAlex's official help documentation. Searches were bounded around the closest concepts and known papers, not exhaustive across every scholarly index or supplementary file.

Search strings used or represented in the search pass:

1. `("citation count" OR "citation-based ranking" OR "citation-aware ranking") AND (scholarly OR academic OR scientific papers)`
2. `"Google Scholar" AND "citation counts" AND ranking algorithm`
3. `"Language Bias in the Google Scholar Ranking Algorithm"`
4. `("popularity bias" OR "citation bias") AND (scholarly recommender OR scientific publication ranking)`
5. `("citation-blind" OR "popularity-blind" OR "without citation features") AND scholarly ranking`
6. `("language fairness" OR "language bias") AND multilingual information retrieval AND ranking`
7. `("title abstract screening" AND supervised machine learning AND systematic review AND logistic regression)`
8. `site:github.com/MarcoAigner/automated_title_abstract_screening`
9. `site:github.com/asreview/synergy-dataset cited_by_count language`
10. `site:help.openalex.org/data/works/attributes language cited_by_count abstract`

The search and source checks confirm meaningful overlap but **do not establish novelty**. Search-engine queries and primary-source checks were bounded and targeted; they were not a reproducible multi-database systematic review with full screening and deduplication. A claim that citation bias or language bias in scholarly search has never been studied would be incorrect. The strings above are supplied for reproducible follow-up as well as describing the concepts searched; do not represent them as exhaustive coverage.

### Specific neighboring-work categories to inspect

1. **Citation-aware academic search ranking:** reverse-engineering or empirical studies of citation counts and academic search rank.
2. **Language disparities in scholarly search:** studies comparing rank/visibility for English and non-English papers within academic search engines.
3. **Popularity bias in scholarly recommender systems:** work on citation/popularity features, long-tail exposure and mitigation.
4. **Fair multilingual information retrieval:** language-group ranking metrics, fairness interventions and multilingual query parity.
5. **Automated systematic-review screening:** supervised TF-IDF/classical classifiers, active learning, LLM-based screening and label/benchmark design.
6. **Citation-based retrieval / citation searching:** forward/backward citation expansion and its precision/recall trade-offs; this is related but methodologically different from the proposed single-feature ranker.
7. **Bibliographic metadata validity:** language detection/metadata accuracy and the effect of publication age on citation counts.
8. **Evaluation of incomplete relevance pools:** pool-relative recall, known-item/reference-set construction and the limits of interpreting a constructed pool as the complete relevant universe.

### Related-work matrix

| Published work | What the source establishes | Overlap with this project | What it does not establish for this project | Status |
|---|---|---|---|---|
| Beel and Gipp (2009), *Google Scholar's Ranking Algorithm: The Impact of Citation Counts (An Empirical Study)*, [DOI](https://doi.org/10.1109/RCIS.2009.5089308) | Their empirical study analyses citation counts and Google Scholar ranking; the authors report that highly cited articles were more often placed higher. | Direct prior work on explicit citation prominence and scholarly ranking. | Does not establish the result of removing one citation feature from this project's own supervised ranker or evaluate the same language-group protocol. It is historical and platform-specific. | **VERIFIED — bounded** by original paper/author source. |
| Rovira, Codina and Lopezosa (2021), *Language Bias in the Google Scholar Ranking Algorithm*, [DOI](https://doi.org/10.3390/fi13020031) | The study reports substantial rank differences for English and non-English records in its Google Scholar sample; it also finds that citation ranking does not explain non-English placement in the same way. In the sample, 91% of non-English records were beyond result 900, compared with 3.7% of English records. | Directly overlaps the language-bias and ranking motivation. | Does not provide a contemporary, generalizable rate for all scholarly systems or the proposed controlled feature ablation. The percentages are specific to the sample and platform. | **VERIFIED — bounded** by the article page. |
| Jordan and Tsai (online 2024; journal volume 2025), *Ranking ‘by Relevance’ in Academic Literature Searches: Prevalence, Definitions, and Implications*, [DOI](https://doi.org/10.1007/s42438-024-00530-z) | Discusses relevance ranking, opacity, subjective relevance definitions and possible compounding of publishing/search biases. | Supports inspecting how academic literature search ranks records and limits the claim that relevance is neutral or transparent. | Does not run this project's citation-feature ablation or provide its group-conditional measurements. | **VERIFIED — publication metadata and article page**; detailed methods-level audit not completed. |
| Färber, Coutinho and Yuan (2023), *Biases in scholarly recommender systems: impact, prevalence, and mitigation*, [DOI](https://doi.org/10.1007/s11192-023-04636-2) | Reviews bias types in scholarly recommender systems, including system-induced bias and popularity bias, and discusses mitigation/evaluation. | Strong adjacent work on popularity bias in scholarly recommendations; rules out a broad claim that scholarly popularity bias is unstudied. | Does not by itself answer the exact performance effect of excluding a citation feature in this proposed ranker on this pool. | **VERIFIED — publisher page and abstract**, not an exhaustive audit of every cited mitigation study. |
| Yang, Jiang and Baldwin (2024), *Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods*, [ACL Anthology](https://aclanthology.org/2024.mrl-1.23/) | Evaluates language fairness in multilingual retrieval using traditional retrieval methods and neural rankers and proposes a language-bias mitigation loss. | Strong methodological overlap on language-group retrieval fairness. | Not directly a scholarly-literature citation-feature ablation; its document/query setting differs. | **VERIFIED — official ACL Anthology record and abstract.** |
| Aigner et al. (2026), *Comparing supervised machine learning and large language models in title-abstract screening*, [DOI](https://doi.org/10.1186/s13643-026-03199-6), [official code](https://github.com/MarcoAigner/automated_title_abstract_screening) | Compares supervised classifiers and Llama-3.1-8B-Instruct across six systematic-review datasets; the repository contains notebooks, processed data and an environment file. | Practical foundation for a low-cost supervised text classifier and metrics code. | The paper's preprocessing removed records with non-English abstracts, among other exclusions. Its published evaluation therefore cannot directly establish language-group performance for non-English records. The original model is not the citation-aware ranker proposed here. | **VERIFIED — repository exists and its README documents code/data; not installed or reproduced.** |
| Rajit et al. (2025), *Automated citation searching in systematic review production: A simulation study*, [DOI](https://doi.org/10.1017/rsm.2024.15), [article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12621532/), [code repository](https://github.com/darrenkjr/automated_citation_search_study) | Simulates citation searching across 27 systematic reviews using OpenAlex and Semantic Scholar and reports precision/recall trade-offs. Its reference-strategy recall was set to 100% by assumption/design. | Relevant alternative for candidate generation and for documenting the unknown relevant-paper denominator. | The method is citation-graph searching, not a trained ranker with one explicit citation feature removed. The reference 100% recall is not independent proof of complete recall in the universe. | **VERIFIED — article and repository links found; repository not run.** |
| van de Schoot et al. (2021), ASReview, [DOI](https://doi.org/10.1038/s42256-020-00287-7), [official repository](https://github.com/asreview/asreview) | Publishes an open-source active-learning framework for transparent systematic-review screening; the repository documents installation and simulation tools. | Relevant comparator/alternative for screening-stage prioritisation. | Active learning changes ranking based on iterative labels; it is not equivalent to the static citation-feature ablation, and citation-feature support has not been verified for the intended configuration. | **VERIFIED — official repository and paper page; not installed.** |
| Céspedes et al. (2025), *Evaluating the linguistic coverage of OpenAlex: An assessment of metadata accuracy and completeness*, [DOI](https://doi.org/10.1002/asi.24979) | Evaluates coverage and accuracy of language metadata, including manual checks of 6,836 articles and label inaccuracies. | Directly relevant to whether a database's language label can be used as ground truth. | Does not establish the error rate in the particular topic-specific sample to be constructed here. | **VERIFIED — bibliographic record and bounded source checks.** |

### Novelty boundary

The controlled feature ablation may be a defensible course-level experiment, but it is **not yet a verified novel contribution**. Before making a novelty claim, compare the exact feature set, corpus, training protocol, subgroup definitions, cutoff metric and evaluation design against the closest work on citation-aware ranking, academic search bias, scholarly recommender popularity bias and fair retrieval. The experiment can still be valuable if the question is carefully bounded and the results are negative, as the assignment states.

## 3. Feasibility and novelty matrix

| Published method / dataset | VERIFIED contribution (with source) | Limitation | Proposed difference | Access status | Evidence still missing | CPU/3-week feasibility |
|---|---|---|---|---|---|---|
| Aigner et al. supervised title/abstract screening | The open-access 2026 paper compares supervised classifiers with an LLM across six review datasets; article licence is CC BY 4.0. The public GitHub repository visibly contains notebooks, data and an environment file. [Paper](https://doi.org/10.1186/s13643-026-03199-6); [repository](https://github.com/MarcoAigner/automated_title_abstract_screening) | Preprocessing excluded records with non-English abstracts; its experiment does not evaluate this project's explicit citation-feature ablation. The repository listing does not show a separate code licence, so reuse rights for repository code are **UNKNOWN** until checked. | Use the published study as methodological context; implement the small text baseline independently and add one citation feature in only one condition. Do not describe this as reproducing Aigner et al. | **Article and public repository verified; code installation/reproduction not tested; repository-code licence unresolved.** | Check repository/data licence, dependencies and data provenance if reproducing; no pretrained model weights are needed for the proposed logistic-regression ranker. | **High** for a simple independent scikit-learn baseline; do not reproduce the LLM arm. |
| ASReview | Open-source active-learning screening; installation and simulation documented. [Repository](https://github.com/asreview/asreview) | Iterative label-informed prioritisation is a different design from the proposed single-feature ablation. | Use only as contextual related work or optional tool comparison; not required for the minimum viable experiment. | **Public repository verified; not installed.** | Verify whether intended feature/custom ranking hook can use citation information before suggesting direct use. | **Moderate**; unnecessary scope for the core study. |
| Rajit et al. automated citation searching | Study and public code/data link; 27 reviews and OpenAlex/Semantic Scholar. [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12621532/) | Citation-network expansion, not a trained feature ablation. API quota, seed choice and review domain matter. | Provides an alternative candidate-generation pathway or optional stage-wise context; not the selected core model. | **Official paper and repository links verified; execution/API use untested.** | Confirm code dependencies, seed lists, repository reproducibility and API limits if reused. | **Medium** for full reproduction; not recommended as main three-week experiment. |
| SYNERGY dataset | Official repository describes 169,288 records from 26 reviews, 2,834 inclusion labels and CC0 1.0 for the dataset; key fields include titles/abstracts, publication year, citation count and references. [Official repository](https://github.com/asreview/synergy-dataset) | Mixed-domain review-screening benchmark, mainly medicine/psychology. The current README lists `Hall_2012` as the computer-science collection, while the installed package/list in the user's Colab showed `Hall_2011.csv`; that version/name discrepancy is unresolved. The language field is not a documented core benchmark variable. | Suitable for testing data loading and screening code, or for a separately reframed general review-screening study only if a selected dataset's scope/fields/group sizes are verified. | **Repository and CC0 dataset licence verified; user's package/export did run, but the relationship of local `Hall_2011` to current public SYNERGY README remains unknown. Other review collections not inspected.** | Resolve collection/version identity; inspect a candidate review's schema, language metadata and relevant positives per group; confirm source terms for abstract use. | **High** for a pipeline smoke test; **conditional/low** for the intended AI-specific multilingual claim. |
| Custom bounded AI-literature pool via OpenAlex | Official Works documentation exposes title, abstract inverted index, publication year, `cited_by_count` and detected metadata language. The Works API queries successfully returned records in the user's Colab. [Works attributes](https://help.openalex.org/data/works/attributes/); [API reference](https://help.openalex.org/api/) | OpenAlex does not provide project-specific relevance labels. `language` is detected from title/abstract metadata, not verified full-text publication language. The official text-search relevance score includes text similarity and a capped citation-count component, so top-ranked text-search results must not be treated as citation-neutral. Topic classification is a different route: current topic documentation says the newer classifier assigns a work’s topics from title/abstract/source without using citation counts. Because OpenAlex topic methods have changed over time, do not treat a single topic filter as a complete or universally neutral discovery route; document the API/documentation date and combine prespecified routes. Language-specific translated queries are also not directly comparable as estimates of natural prevalence. | Best current metadata source to investigate for a bounded AI-literature corpus. Use topic filters and prespecified multi-route searches/sampling, log every route, and design a relevance-label audit before modelling. | **API calls and sample retrieval verified from user-provided Colab outputs; no model trained. Basic API access is documented as free; a key was used in the pilot.** | Larger fixed pool, deduplication, relevance-label protocol, adequate positives by group, publication-language validation, exact metadata pull date, and stable citation snapshot handling. | **Conditional**; current 28-record sample is not sufficient. |

## 4. Dataset and access audit

**Post-pilot source comparison:** The complete source-checked matrix covering OpenAlex, Mendeley Data, CAIR-Nepal, Zenodo and SYNERGY is maintained in [Prompt04_Dataset_Candidate_Comparison_and_Decision_MNS2026008.md](Prompt04_Dataset_Candidate_Comparison_and_Decision_MNS2026008.md). Its key decision is to retain OpenAlex only as a conditional pool-construction strategy; the final dataset still must pass the acceptance gates.

### Option A — SYNERGY

**Verified from the official repository:** SYNERGY contains 169,288 records from 26 systematic reviews with 2,834 inclusion labels; the stated dataset licence is CC0 1.0. The repository documents the command-line acquisition route `pip install synergy-dataset`, followed by `python -m synergy_dataset get`. The documented record variables include a work identifier, DOI, inclusion label, title, abstract, publication year, references, and citation count as of 1 April 2023. [SYNERGY README](https://github.com/asreview/synergy-dataset)

Its computer-science-labelled collections include `Hall_2012` (8,793 records, 104 included), `Radjenovic_2013` (5,935 records, 48 included), and `Smid_2020` (2,627 records, 27 included). The topic labels alone do not prove that these review collections are relevant to AI literature curation. The README's listed key variables do not explicitly include language. In the tested `Hall_2011.csv` export, however, the language field was present and all 340 values were `en`; the selected collection had no non-English records. Other SYNERGY collections have not been tested for language coverage. **Their non-English group counts and group-level positive counts remain UNKNOWN.**

**Recommendation:** use SYNERGY as a pipeline smoke test if convenient. Do not rely on it for an AI-specific language-bias conclusion unless one review is demonstrably on-topic and all required groups are adequately represented. If it becomes the main dataset, state the change in research scope explicitly.

### Option B — build a bounded AI-literature pool through OpenAlex

**Verified from official documentation:** OpenAlex Work records support title/abstract metadata, publication year, citation count and a detected `language` field. Basic API access is free. The documentation says a free API key increases the daily budget and is required for cursor paging beyond the first page; rate and paging limits must be respected. [Works attributes](https://help.openalex.org/data/works/attributes/), [API authentication and limits](https://help.openalex.org/api/authentication/).

**Important measurement issue:** the OpenAlex `language` field is automatically detected from title/abstract metadata; it is not necessarily the language of the full text. Research evaluating OpenAlex linguistic metadata found inaccuracies that can overestimate English and underestimate other languages. Label the variable **metadata language (English / non-English / unknown)** unless publication language is independently checked, and validate a sample against accessible articles. Keep unknown values separate rather than treating them as English. [Céspedes et al. (2025)](https://doi.org/10.1002/asi.24979).

**Abstract handling:** OpenAlex stores abstracts as inverted indexes rather than serving plaintext abstracts. The pilot reconstructed abstracts locally for screening. Do not place reconstructed abstract text in the upload package, report, or public repository; only metadata, labels and aggregate results are included in this report. Verify terms before any redistribution.

OpenAlex does not provide your project-specific relevance labels. You must collect candidate records using a documented topic query and any planned supplementary discovery route, remove duplicates, and apply explicit inclusion/exclusion criteria to titles and abstracts. The candidate pool is constructed and incomplete, so all recall estimates are **pool-relative**. A narrow AI topic and fixed date interval are preferable to attempting to cover all AI research.

**Code, model weights, licence and benchmark protocol:** The chosen model is a proposed, independently implemented TF-IDF + logistic-regression classifier/ranker, so no external pretrained model weights are required. A Python/scikit-learn implementation has not yet been written or run. The Aigner paper is open access under CC BY 4.0, but the public repository's code licence was not established from the repository file listing; do not copy its code until that is verified. ASReview's official software repository lists Apache 2.0, but ASReview is an optional contextual comparator, not the chosen core model. The public SYNERGY dataset is CC0 1.0; the particular local Hall_2011/Hall_2012 discrepancy remains unresolved. No standard benchmark protocol was found/verified for this exact citation-feature ablation and multilingual group-recall question, so the project must define and freeze a transparent protocol in Prompt 07. [Aigner paper](https://link.springer.com/article/10.1186/s13643-026-03199-6); [ASReview repository](https://github.com/asreview/asreview); [SYNERGY repository](https://github.com/asreview/synergy-dataset).

**Pilot result (30 October 2026):** The user successfully called the OpenAlex API and explored topic counts and language-specific queries. Four topic filters showed multilingual metadata in the broader topic pools. One localized title/abstract query configuration returned reported matching counts of 49 English, 13 Indonesian, 262 Portuguese and 356 Spanish records. A later pilot export requested up to 20 records per language, returning 20 English, 7 Indonesian, 20 Portuguese and 20 Spanish records (67 unique records). These counts belong to the specific filters/query versions used; the requested sample size and results returned are not estimates of the underlying language populations. All 67 had non-missing title, year, citation count, language and abstract fields in the exported sample, and the explicit language codes agreed with their assigned query-language groups. A balanced 28-record pilot was then sampled with seven records per language group. The current workbook contains six preliminary relevant labels and 22 preliminary not-relevant labels (English 4/3; Indonesian 0/7; Portuguese 1/6; Spanish 1/6).

**Additional topic-filter exploration (user-run Colab, 30 October 2026):** OpenAlex topic/language grouping returned the following matching counts with `topics.id` plus an abstract and 2015–2026 publication-year filter: `T10286` Information Retrieval and Search Behavior — 111,959; `T10181` Natural Language Processing Techniques — 216,870; `T11550` Text and Document Classification Technologies — 58,856; `T13516` Publishing and Scholarly Communication — 151,393. These are topic-filter counts, **not** relevant-paper counts. The corresponding language buckets showed multilingual metadata, including English, Indonesian, Portuguese, Spanish and others. The current OpenAlex documentation distinguishes `topics.id` (a work may carry the topic among its top topics) from `primary_topic.id` (the principal topic), so the counts cannot be read as AI-curation study counts. [OpenAlex topic documentation](https://help.openalex.org/data/topics/).

**Search behaviour matters:** OpenAlex's official text-search documentation says the default `relevance_score` is based on text similarity plus a capped contribution from citation count. Thus top-ranked text-search records can be citation-influenced. The current topic documentation says the current classifier assigns topics from title, abstract and source without using citations, and notes that a previous classifier operated differently. Any future pool design must distinguish topic-filtered retrieval from text-ranked search, log the route, and avoid claiming either is a neutral census of relevant literature. [OpenAlex search documentation](https://help.openalex.org/api/searching/).

**Interpretation:** The metadata route works for a small sample, but relevance yield is low and non-English positives are sparse. Because the four language groups were retrieved with separate language-specific queries, this pilot cannot be treated as a common-frame, representative comparison of retrieval recall. All six positive labels require human review for consistent criterion application; the 28-record sample is not sufficient for model evaluation. **Recommendation:** continue with OpenAlex only as a candidate-source route, not yet as a validated benchmark. Next construct a pre-specified, bounded candidate pool using documented search strings and, where feasible, more than one discovery route; deduplicate; use a written relevance rubric; and measure group counts before deciding whether to proceed. If enough positive non-English records cannot be secured, reframe language recall as exploratory/not estimable and concentrate on the citation ablation only if citation-group positives are adequate.

## 5. Audit of the selected experiment

### Research question

**On a bounded, relevance-labelled AI-literature pool, does adding an explicit citation-derived feature to a lightweight TF-IDF relevance ranker change overall ranking quality and pool-relative recall for lower-citation and non-English/metadata-language groups, compared with the same ranker without that feature?**

The experiment tests the behaviour of the specified ranker on a specified candidate pool. It does not establish causal effects across all scholarly search systems.

### Smallest defensible design

1. **Topic and time window:** choose one narrow AI subtopic and a fixed publication-year range before analysing model performance.
2. **Candidate pool:** collect records using a documented query, plus a second discovery route if feasible (for example, references/citations or a pre-specified additional query). Save source route and retrieved IDs. Deduplicate by OpenAlex ID/DOI, then normalized title with manual review of ambiguous matches.
3. **Relevance labels:** write inclusion/exclusion criteria before labelling. Record who labelled each item. If feasible, have a second person independently check a subset and resolve disagreement. Labels from AI-only decisions should not be accepted without human verification.
4. **Split:** after deduplication, create one fixed stratified train/test split (or pre-specified repeated stratified splits if enough examples). Fit all text transforms on training data only. Do not use test labels for model fitting, feature choice, tuning or cutoff selection. Keep the exact same split(s) for both conditions.
5. **Shared text features:** TF-IDF from title and abstract, with identical tokenization and preprocessing.
6. **Shared year control:** publication year is included identically in both conditions. This helps make the citation comparison less confounded by publication age, but it does not eliminate all field/age differences.
7. **Citation-aware condition:** TF-IDF + publication year + the single pre-specified citation-derived feature, recommended as `log1p(cited_by_count)` from a recorded metadata snapshot date.
8. **Citation-blind condition:** same pipeline with only `log1p(cited_by_count)` removed. Keep classifier, class weighting (if used), regularization, seeds, train/test split, scoring, and evaluation code identical. The models should not include language as an input feature; language is an evaluation grouping variable.
9. **Ranking:** use the logistic-regression predicted relevance score to sort the held-out candidate records. Describe this as a supervised classifier used for ranking, not as a dedicated learning-to-rank algorithm.
10. **Citation groups:** predefine lower/higher groups using citation percentiles within publication-year bands if sufficient data permit; otherwise use a clearly stated and justified cutoff. Do not choose group cutoffs after viewing favourable results. Record the citation snapshot date.
11. **Language groups:** use verified publication language where possible. If relying on OpenAlex's automatic field, call it metadata language and retain unknown/unassigned as a separate status. Validate a sample against accessible paper text.
12. **Screening budget:** define the primary top-K cutoff before evaluation. A budget such as top 20% of held-out candidates can be chosen after the pilot and then frozen for both models. Report each subgroup's number of relevant test records.

### Metrics

**Primary metric:** recall at a pre-specified screening budget, overall and by group:

`Recall_g@K = relevant test records from group g in the top K / all relevant test records in group g`.

Report the difference between citation-blind and citation-aware recall for lower-citation records as the main targeted contrast, and also report results for the language groups if there are enough labelled relevant records. The group-conditional denominator is the number of relevant records in that group in the held-out **constructed pool**; recall is not absolute corpus-wide recall.

**Secondary metrics:** precision@K and NDCG@K overall, with group counts and uncertainty intervals where sample size allows. Work-saved-at-95%-recall is appropriate only if the screening protocol and data let you measure it meaningfully and the method actually reaches 95% recall.

**Deeper analysis:** inspect relevant papers whose rank changed most when the citation feature was removed; examine metric sensitivity to the pre-specified K or to a justified citation-group definition. Stage-wise loss is a by-product only if candidates and transitions are logged. If only a single candidate pool and final rank are available, call it ranking-stage loss, not full-pipeline loss.

### Main validity threats

- **Incomplete denominator:** the reference pool cannot represent all relevant AI papers. Report pool-relative recall and describe how the pool was assembled.
- **Search selection bias:** if initial queries fail to retrieve non-English papers, ranking metrics cannot recover records that never entered the pool. Document search routes and consider pre-specified multilingual terms where appropriate.
- **Citation-age relationship:** older papers have more time to accrue citations. Use publication year as a shared control, record the citation snapshot, and report a within-year normalization sensitivity check if the data support it.
- **Language metadata errors:** automatic metadata language can differ from full-text language. Validate a sample; keep unknown labels explicit.
- **Sparse subgroups:** group recall is unstable when only a few relevant held-out papers are present. Report numerators/denominators, uncertainty and when estimates are not interpretable.
- **Label bias:** manual relevance labels may reflect the chosen screening protocol. If SYNERGY is used, inclusion labels come from review authors and reflect their criteria and prior search/screening process.
- **Data leakage:** remove duplicates before splitting; fit TF-IDF and feature transformations on training data only; freeze the split and settings before test evaluation.
- **Causal overclaim:** a change between two rankers identifies a difference under this protocol, not a universal causal effect of citation information in production search engines.

## 6. Comparison of experiment pathways

| Pathway | Smallest working baseline | Testable question | Resource burden | Evidence required | Decision |
|---|---|---|---|---|---|
| **A. Reproduction + extension** | Reproduce Rajit et al.'s automated citation-search procedure, then add group-conditional measurements. | Does the reported citation-search behaviour carry over to a bounded AI collection and differ by citation/language group? | Medium–high: original protocol, seed choices, APIs and data mapping must be reproduced before extension. | Original-method checks, actual retrieval logs, reproducibility discrepancies, group labels and extension metrics. | Viable fallback, but not the simplest main study in three weeks. |
| **B. Controlled comparison** | Compare keyword retrieval with one-hop citation retrieval on a shared labelled pool. | Do the retrieval routes recover different relevant papers across the groups? | Medium: multi-route pool assembly and matching retrieval settings add work. | Queries, seed lists, identifiers, labels, deduplication and comparable recall/precision results. | Useful if ranker feature ablation is blocked; it answers a somewhat different question. |
| **C. Targeted modification (chosen)** | TF-IDF + logistic regression + publication year + one citation feature, compared to the same model without that feature. | Does the citation feature change group-conditional recall and overall ranking quality? | Low compute; medium data/label burden. The model is small enough for CPU. | Fixed split, identical conditions, real predictions, metrics by group, failure cases and reproducible commands. | **Preferred**, conditional on dataset and group-count pilot. |

## 7. Fallback and go/no-go decision

### Preferred route

Use a small, bounded OpenAlex AI-literature pool for the primary experiment because it best preserves the project topic. Do not collect the entire AI corpus. Start with a small pilot to estimate metadata completeness, group sizes and the time needed for relevance annotation.

### Fallback 1 — expand the custom corpus carefully

If the first query yields too few non-English or lower-citation relevant records, broaden the date range or pre-specify supplementary multilingual queries and a second discovery route. Record each change and deduplicate again before labelling. Do not add queries only after observing an unfavourable model result.

### Fallback 2 — narrow the claims honestly

If the non-English relevant group remains too small after a reasonable pilot, keep the citation-aware versus citation-blind experiment and treat language-group results as exploratory or **not estimable**. Do not present a sparse estimate as evidence that no language disparity exists. The core result can then be a citation-group ranking audit, with the language limitation clearly stated.

### Fallback 3 — SYNERGY for pipeline validation

Use SYNERGY to test that data loading, TF-IDF/logistic regression, ranking and metrics run correctly. A SYNERGY-only experiment must be described as a systematic-review screening benchmark, not as direct proof about AI-literature curation, unless the selected dataset and group distributions pass the relevance/domain checks.

### Revised decision

**CONDITIONAL GO for continued dataset construction; NO-GO for the main model experiment on the current 28-record pilot.** The proposed small model is computationally feasible on a CPU-only laptop or free Colab. Data feasibility is not yet established because the pilot contains only six preliminary relevant labels, with no positive Indonesian records and only one positive record in each of Portuguese and Spanish. Separate language-specific searches also mean the records are not a neutral sample of all records that a single retrieval workflow would return.

The metadata pilot itself is complete and should be recorded as such. The next gate is a **candidate-pool and relevance-label pilot**, not training. Define one narrow research subtopic and date window, document the queries and additional discovery routes in advance, deduplicate records, and apply a written relevance rubric. Then count relevant examples by language and citation group. Do not tune the query to produce a desired bias result. Use pool-relative metrics only and explain the incomplete-denominator limitation.

| Phase | Work | Gate/evidence |
|---|---|---|
| **Completed: metadata feasibility** | Tested SYNERGY `Hall_2011.csv`; rejected it as the main dataset. Queried OpenAlex topic and language-specific results; checked required metadata fields; created a balanced 28-record preliminary label pilot. | Evidence is recorded in the Metadata Pilot Record and current annotated workbook. Current pilot: 28 records, 6 preliminary relevant, 22 preliminary not relevant. |
| **Next: pool design and label validation** | Fix topic/date range and search plan; add more than one retrieval route if feasible; preserve query/source route and dates; deduplicate; refine the rubric; human-check labels and a subset with a second reviewer if available. | Versioned candidate pool, screening guide, label audit, and counts by language/citation group. Stop/reframe if relevant subgroup counts are sparse. |
| **Then: feasibility gate / Prompt 04 revision** | Decide whether language-group evaluation remains primary, exploratory, or not estimable; update the go/no-go matrix and fallback. | A documented decision based on actual relevant group counts, not just total metadata counts. |
| **After gate: Prompt 05–07** | Finalize research questions and success criteria; verify the selected dataset and comparators; freeze the evaluation protocol. | Reviewed research brief, dataset validation sheet, and frozen protocol. |
| **Only then: implementation** | Implement and test TF-IDF + logistic regression with and without one citation feature; use identical splits and pipeline settings. | Executable baseline, feature-ablation test, actual held-out metrics, uncertainty, and error analysis. |

The original three-week compute estimate remains plausible for the model itself, but the annotation/pool-building effort is the present bottleneck. If that effort cannot produce sufficient relevant records across language groups, narrow the experiment rather than proceed with unstable subgroup estimates.

## 8. Computational and time estimate

**Hardware assumption:** CPU-only student laptop or free Google Colab; no paid GPU assumed. The proposed experiment uses TF-IDF vectorization plus logistic regression and one numeric citation-derived feature, not a large language model. No pretrained weights are required for this design.

| Work package | Estimated time within the three-week window | Compute/resource need | Risk / gate |
|---|---:|---|---|
| Finalize corpus scope, query plan and data-access checks | 1–2 days | OpenAlex API, browser, local CSV/metadata handling | Topic/query mismatch may reduce relevant-paper yield; document query strings before final pool creation. |
| Retrieve, deduplicate, validate metadata and label a bounded candidate pool | 4–7 days (may expand) | API/network, spreadsheet/CSV, manual abstract screening; second reviewer desirable for a subset | **Main bottleneck.** Current 28-record pilot is too small; stop or narrow if sufficient positive groups cannot be assembled. |
| Implement the two logistic-regression conditions | 1–3 days after data gate | CPU; pandas/scikit-learn; a small corpus should fit ordinary RAM | Low compute risk; code has not yet been written or executed. |
| Evaluate metrics, bootstrap/uncertainty if justified, inspect errors and subgroup counts | 2–4 days | CPU, reproducible scripts and saved predictions | Sparse positives make recall estimates unstable; report denominators and intervals where estimable. |
| Write and review results/reproducibility package | 3–5 days | Markdown/LaTeX, figures, README, AI-use log | Time is tight if annotation or dataset access takes longer than planned. |

**Feasibility judgement:** model compute is **likely feasible** within three weeks on CPU. Data access and human label quality are **conditional** and currently dominate feasibility. These are planning estimates, not elapsed-time measurements. The current notebook confirms metadata queries and export only; it does not confirm installation/reproduction of Aigner, ASReview or Rajit code, nor any trained model or experimental metric.

## 9. Prompt 04 completion checklist and post-Prompt-04 tasks

### Prompt 04 deliverable (complete)

- [x] Personalized candidate study, hardware and time window stated.
- [x] Bounded novelty search strings and neighboring-work categories provided; scope limits disclosed.
- [x] Related-work matrix provided with VERIFIED contribution/source, limitation, proposed difference and missing evidence.
- [x] Dataset/code/weights/licence/benchmark access audit provided; unresolved cases clearly marked UNKNOWN.
- [x] User-run SYNERGY and OpenAlex pilot results recorded with their limitations.
- [x] CPU/time constraints estimated and principal bottleneck identified.
- [x] Viable bounded experimental question, fallback paths and explicit final decision provided.

### Post-Prompt-04 tasks (required before main implementation)

- [ ] Human-audit the six preliminary positives and a sample of negatives against the written relevance rule; resolve the borderline Portuguese decision transparently.
- [ ] Freeze the narrow scope, completed-year publication window, multilingual search strings and supplementary discovery routes.
- [ ] Construct and deduplicate a larger pool, recording query, source route, and collection date for each record.
- [ ] Validate a sample of metadata-language fields against accessible publication text; keep unknown or uncertain language separately.
- [ ] Count human-reviewed relevant records by language and citation group; if positives remain sparse, mark language metrics not estimable or narrow the research question.
- [ ] Record the citation-count pull date and prespecify `log1p(cited_by_count)` as the feature; include publication year identically in both conditions.
- [ ] Only after the data gate passes, freeze train/test splits and fit all learned text transforms on training data only.
- [ ] Keep records, labels, splits, model settings, seeds, K and evaluation code identical across citation-aware and citation-blind rankers.
- [ ] Report subgroup denominators, uncertainty and failure cases; never interpret sparse estimates as absence of bias.
- [ ] Verify licenses/terms for all data/software used, keep API keys private, and do not redistribute reconstructed abstract plaintext.
- [ ] Save commands, package versions, configurations, predictions, metrics and genuine execution logs.

## 10. Overall conclusion and final decision

The OpenAlex route has passed a small technical metadata test but has **not** passed the relevance-label and subgroup-adequacy gate. The latest working 28-record workbook contains six preliminary `1` labels and 22 `0` labels: English 4/3, Indonesian 0/7, Portuguese 1/6 and Spanish 1/6. These records were selected from language-specific queries and the labels remain AI-assisted/preliminary. They must not be used to estimate main-model performance or claim citation or language bias. The SYNERGY `Hall_2011.csv` run remains a documented **NO-GO as the sole dataset** for the combined AI-literature language analysis because it contained four review-included records and no non-English records. The local collection name also does not match the current public README's `Hall_2012` label, which remains unresolved.

**Prompt 04 deliverable is revised after the pilot and candidate-source audit.** The decision is **CONDITIONAL GO for constructing and annotating the selected OpenAlex pool; NO-GO for training on the present pilot**. This distinction is intentional: Prompt 04 can be completed by documenting that the preferred approach is not yet feasible on the current data. Prompt 05 subsequently framed the research questions and success criteria, and Prompt 06 completed the dataset/comparator validation sheet. The final dataset remains unvalidated; Prompt 07 should freeze the protocol only after the larger pool and subgroup denominators pass the data-feasibility gate. If a larger, responsibly constructed pool cannot provide enough relevant records across the intended groups, narrow the experiment to citation-group ranking and mark language-group evaluation not estimable rather than force the original multilingual claim. Novelty remains **UNKNOWN** because the bounded search is not exhaustive.

**Work actually completed:** official Prompt 04 requirements reviewed; source/repository/API checks performed; user-run Colab outputs document topic/language queries and metadata checks; a 28-record balanced pilot and preliminary labelled workbook exist. **Not completed by design:** independent validation of all labels, a larger reference pool, the main model, controlled ranking comparison, or empirical bias evaluation. These are later project tasks, not missing sections of this Prompt 04 report.

## References and official resources

1. Beel, J., & Gipp, B. (2009). *Google Scholar's Ranking Algorithm: The Impact of Citation Counts (An Empirical Study).* https://doi.org/10.1109/RCIS.2009.5089308
2. Rovira, C., Codina, L., & Lopezosa, C. (2021). *Language Bias in the Google Scholar Ranking Algorithm.* https://doi.org/10.3390/fi13020031
3. Jordan, K., & Tsai, S. P. (2025, published online 24 Dec 2024). *Ranking ‘by Relevance’ in Academic Literature Searches: Prevalence, Definitions, and Implications.* https://doi.org/10.1007/s42438-024-00530-z
4. Färber, M., Coutinho, M., & Yuan, S. (2023). *Biases in scholarly recommender systems: impact, prevalence, and mitigation.* https://doi.org/10.1007/s11192-023-04636-2
5. Yang, J., Jiang, F., & Baldwin, T. (2024). *Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods.* https://aclanthology.org/2024.mrl-1.23/
6. Aigner, M. F., et al. (2026). *Comparing supervised machine learning and large language models in title-abstract screening.* https://doi.org/10.1186/s13643-026-03199-6. Official code: https://github.com/MarcoAigner/automated_title_abstract_screening
7. Rajit, D., et al. (2025). *Automated citation searching in systematic review production: A simulation study.* https://doi.org/10.1017/rsm.2024.15. Article: https://pmc.ncbi.nlm.nih.gov/articles/PMC12621532/. Code: https://github.com/darrenkjr/automated_citation_search_study
8. van de Schoot, R., et al. (2021). *An open source machine learning framework for efficient and transparent systematic reviews.* https://doi.org/10.1038/s42256-020-00287-7. Repository: https://github.com/asreview/asreview
9. De Bruin, J., Ma, Y., Ferdinands, G., Teijema, J., & Van de Schoot, R. (2023). *SYNERGY - Open machine learning dataset on study selection in systematic reviews*, V1. https://doi.org/10.34894/HE6NAQ. Repository/documentation: https://github.com/asreview/synergy-dataset
10. OpenAlex Help Center. *Works attributes.* https://help.openalex.org/data/works/attributes/
11. OpenAlex Help Center. *API authentication and limits.* https://help.openalex.org/api/authentication/
12. OpenAlex Help Center. *Pricing and data licence (CC0).* https://help.openalex.org/access/pricing/
13. Céspedes, L., et al. (2025). *Evaluating the linguistic coverage of OpenAlex: An assessment of metadata accuracy and completeness.* https://doi.org/10.1002/asi.24979
14. OpenAlex Help Center. *Search — Querying* (text search uses text similarity and a capped citation-count component in its default relevance score). https://help.openalex.org/api/searching/
15. OpenAlex Help Center. *Topics — Aboutness* (topic assignment, `topics.id` vs `primary_topic.id`, and current topic-classifier description). https://help.openalex.org/data/topics/
16. OpenAlex Help Center. *API reference* (free basic access; an API key raises request budget). https://help.openalex.org/api/
17. OpenAlex Help Center. *Works attributes* (language is detected from metadata; abstracts are returned as inverted indexes). https://help.openalex.org/data/works/attributes/

## Literature and scope addendum — 30 October 2026

A targeted follow-up check found additional close work: Khatoon and Amjad (2026) propose a scientific-publication ranking framework combining temporal relevance, lexical relevance and citation behaviour; Fleurence et al. (2026) review 115 GenAI studies across systematic-review tasks; Barragán et al. (2026) review AI resources for title/abstract screening; and Adam et al. (2025) update the AHRQ evidence map to 95 studies. These sources further weaken broad novelty claims. The selected course experiment is therefore framed narrowly as a controlled citation-feature ablation with lower-citation pool-relative Recall@K as its primary outcome. Novelty remains unverified. The title has been narrowed accordingly; language analysis is conditional and descriptive unless a larger, independently audited dataset supports it.
