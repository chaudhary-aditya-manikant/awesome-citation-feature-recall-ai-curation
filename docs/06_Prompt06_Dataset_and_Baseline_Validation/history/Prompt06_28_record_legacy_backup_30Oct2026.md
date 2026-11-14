> **SUPERSEDED for dataset sampling decisions on 31 October 2026.** Retained as historical evidence only. Use `Prompt06_Dataset_and_Baseline_Validation_Sheet_MNS2026008_v2_31Oct2026.md` and Protocol Amendment A2 for the current sampling plan and acceptance status.

# Prompt 06 — Dataset and Baseline Validation Sheet

**Student:** Aditya Chaudhary  
**Enrollment:** MNS2026008  
**Course:** AI Tools for Research  
**Project:** *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*  
**Verification date:** 30 October 2026  
**Decision:** **CONDITIONAL GO for construction of a bounded evaluation pool; NO-GO for the main model on the current 28-record pilot.**

## 1. Research question and task definition

The current project plan tests whether adding an explicit citation-derived feature to a lightweight relevance ranker changes the order in which relevant papers are presented for screening. The primary comparison is a citation-blind ranker versus an otherwise identical citation-aware ranker. Recall is measured relative to a documented, relevance-labelled candidate pool; it is not presented as recall over every relevant publication in the world.

For consistency with the existing research log and pilot rubric, the screened literature is defined narrowly as work that directly investigates computational methods or tools for scholarly-literature discovery and curation, including scholarly retrieval, citation searching, ranking, title/abstract screening, study selection, or systematic-review automation. A paper that merely uses AI in medicine, education, or another domain is outside this scope unless the method itself addresses scholarly-literature curation. If the project is instead intended to curate papers about a general AI subfield, that would be a different task and the labels created under this rubric would not transfer.

## 2. Executive recommendation

**Recommended primary data strategy:** construct a bounded, deduplicated, relevance-labelled candidate pool from OpenAlex metadata. OpenAlex is the best fit among the inspected sources for this project's joint metadata requirements because its works records provide identifiers, title, publication year, citation count, and detected metadata language; the abstract is represented as an inverted index. Its API and field definitions are documented publicly, and OpenAlex states that its metadata is released under CC0 [1–4].

**This recommendation is conditional, not a declaration that the current dataset is ready.** The actual 28-record OpenAlex pilot contains six preliminary positive labels and 22 negative labels. Positive labels by metadata-language group are English 4, Indonesian 0, Portuguese 1, and Spanish 1. The Indonesian group therefore has no positive denominator in this pilot; its group recall is **not estimable**, not zero. The pilot cannot support the main ranking evaluation or any conclusion about citation or language bias.

The current dataset-development gate has two parts:

1. Build a frozen candidate pool from a documented, reproducible collection process that does not rely only on the search engine's default ranked results.
2. Apply one written eligibility rubric consistently, then verify the number of relevant records by language and citation group before deciding which subgroup metrics can be interpreted.

SYNERGY is a useful labelled benchmark for checking that the data-loading and screening pipeline works, but its review-specific inclusion labels do not automatically represent relevance to this project's AI-literature-curation task. A newly released human-labelled Zenodo benchmark is another possible screening-method benchmark, but its listed tasks concern materials-science literature and the landing-page evidence inspected here does not establish multilingual suitability or a verified reuse licence. Neither replaces the proposed OpenAlex pool for the joint language/citation question without further checks.

## 3. Dataset candidates and comparison

## 3.1 Post-pilot source audit (30 October 2026)

The first pilots showed that neither the 28-record OpenAlex sample nor SYNERGY `Hall_2011.csv` is eligible for main evaluation. A separate source check was therefore performed before any environment/model work.

| Candidate | Source-reported scale and labels | Metadata / language | Topic fit | Decision |
|---|---|---|---|---|
| OpenAlex custom pool | No labels supplied; independent annotation required. | Official API supports title/abstract-index metadata, year, `cited_by_count`, and detected language; default search relevance incorporates a citation component. Data licence documented as CC0. | Best fit when queries are limited to literature-curation methods. | Selected source strategy, conditional on actual pool and label audit. |
| Mendeley AI decision support in higher education | Source page reports 1,190 unique records, 1,105 screened and 531 included. | Title/abstract/year/citation metadata reported; search restricted to English; CC BY 4.0. | Related AI application literature, not literature-curation methods. | Not primary unless the research scope/title is explicitly changed. |
| CAIR-Nepal AI Bias Research Landscape | 692 curated bibliographic records; no project-specific screening labels reported. | Year/citation metadata reported; actual full schema and language distribution not confirmed in this stage. Licence remains to verify from source text. | Adjacent AI/algorithmic-bias literature, not specifically curation methods. | Not primary without schema/licence audit and independent labels. |
| Zenodo human-labelled screening benchmark | Three screening datasets reported with 440, 205 and 200 records and human relevance labels. | DOI/year/title/abstract/label reported; language group counts and citation fields not established from landing-page description. | Concrete materials, nanopore transport and lithium extraction, not AI literature curation. | Not primary; possible separate pipeline smoke test after licence check. |
| SYNERGY `Hall_2011.csv` pilot | 340 rows; 4 included, 336 excluded. | All explicit language values `en`; public repository name discrepancy unresolved. | Main task fit not established. | NO-GO as primary dataset. |

**Evidence limitation:** For Mendeley, CAIR-Nepal and Zenodo, this is a source-page audit of reported properties, not a claim that every downloadable file was fetched and independently inspected. The actual final dataset remains to be constructed and validated. Full comparison and URLs: `../04_Prompt04_Feasibility/Prompt04_Dataset_Candidate_Comparison_and_Decision_MNS2026008.md`.


| Candidate | What is verified from the source | Fit to this research question | Access, licence and format | Main limitations / decision |
|---|---|---|---|---|
| **A. OpenAlex bounded candidate pool — recommended primary strategy, conditional** | Official Works documentation provides title, publication year, citation count, language and `abstract_inverted_index`. Citation count is `cited_by_count`; language is automatically inferred from metadata and does not necessarily represent full-text language [1–4]. The user-run Colab pilot produced a 67-record metadata sample with no missing values for title, year, citation count, language, or locally reconstructed abstract; a separate balanced 28-record pilot has six preliminary positive labels. | Best available match for obtaining a single record table with citation/year/language metadata while sampling several language groups. It does **not** supply review-specific relevance labels; the study must define and apply its own rubric. | Works API: https://api.openalex.org/works . OpenAlex documents basic API access and a free API key option [4]. OpenAlex says its data is CC0; abstract plaintext is not supplied by the API and is represented as an inverted index for legal reasons [1, 4]. | **Conditional GO for pool construction only.** The current 28 rows are too small and have sparse positives. The pilot was formed from separate language-specific search frames with equal group quotas, so its group shares must not be interpreted as population prevalence. Keep reconstructed abstract plaintext local; do not include it in a public package. Re-fetch the final sample and record the retrieval/citation snapshot date. |
| **B. SYNERGY dataset — secondary pipeline benchmark only** | The official repository describes 169,288 records across 26 systematic reviews, of which 2,834 are labelled included. It provides review-specific eligibility criteria and fields including OpenAlex ID, DOI, title, abstract/inverted abstract, `label_included`, publication year and citation count; the repository states CC0 1.0 [5]. Its current README lists `Hall_2012` as a Computer Science review with 8,793 records and 104 inclusions. | Useful for testing code and evaluation plumbing against published, review-specific inclusion decisions. The selected review criteria are not the same as this project's defined AI-literature-curation criteria. | Official repository and instructions: https://github.com/asreview/synergy-dataset . Dataset DOI: https://doi.org/10.34894/HE6NAQ . The repository states CC0 1.0. | **Not recommended as primary dataset.** In the user-run local export named `Hall_2011.csv`, there were 340 records, four included labels and 340 `en` language values. The correspondence between that local filename/version and the current public repository's `Hall_2012` entry has not been reconciled; do not assume the files are the same dataset. The local run cannot support the multilingual question. The repo's documented citation-count snapshot is 1 April 2023, which differs from a live OpenAlex count. |
| **C. Aigner et al. title/abstract screening data and code — method reference / optional reproduction benchmark** | The 2026 open-access paper compares four supervised models (including logistic regression) and an open-weight LLM across six human-labelled systematic-review datasets. The paper states five datasets are openly available and one is proprietary; the public GitHub repository contains preprocessing, analysis, and classification notebooks [6, 7]. | Closely relevant to the proposed TF–IDF/classical-classifier baseline and screening metrics. | Article: https://doi.org/10.1186/s13643-026-03199-6 . Code: https://github.com/MarcoAigner/automated_title_abstract_screening . The article is CC BY 4.0. Check the repository's applicable licence and each dataset's terms before reusing files or code. | **Useful for method design, not the language comparison.** The authors explicitly removed records with non-English abstracts during preprocessing, so the published benchmark cannot validate non-English group recall. The code repository has not been installed or reproduced in this project. |
| **D. Human-labelled screening benchmark (Li et al., 2026) — supplementary benchmark candidate** | The Zenodo record lists a screening dataset for machine learning in concrete materials science with 440 publications: 272 labelled relevant and 168 irrelevant. It describes DOI, publication year, title, abstract and human relevance labels for its screening datasets [8]. | Could be useful as an external labelled screening task to smoke-test text preprocessing or the basic classifier. It is not the same topic as AI-assisted scholarly-literature curation. | Record: https://zenodo.org/records/21853690 . The record is openly accessible. The specific reuse licence was not resolved from the record details available during this check; verify it before redistributing or incorporating data. | **Not recommended as the primary dataset.** The record does not establish sufficient language diversity for the intended subgroup analysis, and its labels are specific to a materials-science review question. The language and citation metadata would need to be checked or joined by DOI/OpenAlex, and the records must not be re-labelled as if the original labels had the project's meaning. |

### Evidence from the current OpenAlex pilot

The outputs supplied from Colab show the following:

- The 67-record metadata sample had 67 unique OpenAlex IDs, no missing titles, publication years, citation counts, language values, or reconstructed abstracts, and the language codes agreed with the query-language groups assigned in that sample.
- The balanced 28-record pilot had seven records per query-language group. The current colour-preserved workbook has six preliminary positive labels and 22 negative labels: English 4/3, Indonesian 0/7, Portuguese 1/6, and Spanish 1/6.
- Earlier exploratory outputs reported 111,959 works matching the broad `topics.id:T10286` query with an abstract and years 2015–2026; that filter refers to works having the topic among their assigned topics, not necessarily as their primary topic. Those broad counts are not the size of a relevance-labelled corpus. A later request used `primary_topic.id` with `sample=10`; its returned ten records are a sample, not evidence that only ten eligible works exist.
- The 28-record language quotas were imposed by the pilot design. They are useful for discovering whether the screening rubric works in each language, but are not an estimate of the language distribution in OpenAlex or in AI literature.

## 4. Collection protocol recommended for the primary pool

### 4.1 Freeze the target scope

- **Target task:** computational methods or tools for scholarly retrieval, citation searching, relevance ranking, title/abstract screening, study selection, and systematic-review automation.
- **Publication window:** use 2015–2025 for the main pool so the window consists of complete calendar years at the time of collection. The earlier exploratory queries included 2026 and should not silently be merged into this final window.
- **Work eligibility:** require a usable title and abstract representation; retain DOI/OpenAlex ID, publication year, type, metadata language, citation count, retrieval route and collection date. Predefine included publication types after inspecting the API's actual `type` values; do not add or remove work types after viewing model performance.
- **Language groups:** start with English, Indonesian, Portuguese and Spanish because these were the four groups tested. Expand to another language only if the same screening rubric and metadata validation can be maintained.

### 4.2 Avoid selecting the pool only by default search rank

OpenAlex's default text-search `relevance_score` is based on text similarity and also incorporates citation count, with the citation contribution capped; it is therefore not an independent citation-blind ordering [3]. Do not build the evaluation pool solely from the first page/top-ranked search results and then claim an unbiased test of citation-feature effects.

For the next pool version:

1. Use a pre-specified set of topical filters and multilingual queries; retain every exact query and filter.
2. Where sampling from a filtered universe, use the API's documented `sample` parameter with a recorded seed rather than arbitrary page numbers or the top-ranked page [4].
3. Preserve the `retrieval_route` for every record (topic-filter sample, language-specific query, or other approved route). Deduplicate the union by OpenAlex ID, DOI and normalized title before screening.
4. Treat the resulting pool as a **constructed reference pool**. If language-specific query routes are required, recall comparisons are conditional on this pool and the routes used; they do not measure complete database coverage or natural language prevalence.
5. Freeze the candidate pool, label file, primary metric and K before the held-out model evaluation. Do not modify queries after seeing model results to improve a favoured outcome.

### 4.3 Language and citation metadata

- OpenAlex's `language` field is an automated classification of work metadata (title/abstract), not a guaranteed label of the complete publication text [1]. Céspedes et al. manually assessed 6,836 articles and reported that 14.7% of records in their validation sample had a false-positive language assignment overall; performance differed by language [9]. Validate a sample against the available article text or a reliable publisher/source record, and call the variable **metadata language** unless publication language is independently verified.
- `cited_by_count` reflects matched incoming citations and changes as the OpenAlex graph is updated [2]. Fetch the citation count once for the final dataset and save the retrieval date/snapshot. Raw counts are age-dependent; predefine citation groups within publication-year bands (for example, below/above the within-year median) and retain publication year as a shared control in both rankers.
- Use `log1p(cited_by_count)` as the one citation-derived model feature specified in Prompt 05. Keep year, text features, labels, training/test indices, model settings and evaluation code identical across the paired conditions.
- Reconstructed abstract text must remain local. Do not distribute reconstructed plaintext abstracts in the submission ZIP or a public repository. Share IDs, allowed metadata, query/provenance files, code and aggregate results only where permitted by the applicable terms.

### 4.4 Label protocol

The final positive label means the record directly studies computational methods/tools for scholarly-literature retrieval, ranking, citation searching, screening, selection or curation. The negative label means the record is outside that scope. A paper about using AI for disease detection, clinical outcome extraction, or a different application is not positive simply because it mentions AI or systematic reviews.

The 28-record labels are preliminary AI-assisted decisions, not an established gold standard. Apply the same written eligibility rules to the larger pool, preserve the reason for each decision, deduplicate before labeling, and record borderline disagreements. Where a second reviewer is available, independently check a stratified subset and report the disagreement-resolution rule. If a group contains no relevant test records, its recall is **not estimable**, not zero.

## 5. Baseline and comparator plan

The primary comparison must isolate one feature. Both conditions use the same candidate records and human-screened labels, the same title/abstract text, a shared publication-year control, the same Logistic Regression classifier, the same training/test split, and the same hyperparameters. Only the citation-derived feature changes.

| Condition | Inputs and method | Role | Expected compute | Main risk |
|---|---|---|---|---|
| **Baseline A — citation-blind ranker** | TF–IDF features from title + abstract, plus the shared publication-year feature; Logistic Regression. Sort test records by predicted probability of relevance. | Reference condition for the primary hypothesis. It tests ranking without an explicit citation-count input. | Low; CPU-only; no GPU or pretrained model required. Exact runtime has not been measured on the final pool. | It may perform poorly on a small, noisy or inconsistently labelled dataset; this is a data/model limitation, not evidence for citation bias. |
| **Condition B — citation-aware ranker** | Identical to A, plus `log1p(cited_by_count)` as one citation-derived feature. | Targeted modification. The A-vs-B difference estimates the effect of adding this explicit feature under this specific protocol. | Low incremental compute; same classifier and text pipeline as A. | Citation count is age-dependent and the model may learn confounding. Publication year must remain a shared control; counts require a frozen snapshot date. |

This is a controlled two-condition comparison rather than a claim about the internal rankers used by Google Scholar, OpenAlex, ASReview or any commercial service. The output is a supervised classifier score used to rank a fixed candidate pool; it should not be described as a dedicated pairwise learning-to-rank algorithm.

**Optional external comparator, only if the core study is completed:** ASReview is a documented open-source active-learning framework for systematic-review screening under Apache 2.0 [10, 11]. It is a useful related method, but its iterative label-acquisition protocol is not a drop-in citation-feature ablation. Adding it to the primary comparison would create extra design choices and is not required for the minimum viable study.

## 6. Evaluation design and leakage controls

1. **Freeze scope and labels first.** Store OpenAlex IDs, DOI where available, query route, collection date, label, reason, metadata language, publication year, cited-by count and citation snapshot date.
2. **Deduplicate before splitting.** Deduplicate by OpenAlex ID, DOI and normalized title; review likely preprint/published-version pairs so the same work does not appear in both train and test.
3. **Holdout design.** Once subgroup and label counts permit, use a 70/30 train/test split stratified on the binary relevance label, with a fixed seed (42) as a reproducible starting configuration. Aigner et al. used a stratified 70/30 split with `random_state=42` in their title/abstract benchmark [6]. If enough data exist, repeat with pre-specified seeds as a sensitivity analysis. Do not force subgroup stratification when the cells are too small; instead report that subgroup evaluation is not estimable.
4. **Prevent feature leakage.** Fit TF–IDF vocabulary/IDF and numerical preprocessing on training records only. Keep the test data untouched while choosing settings. Use exactly the same rows and split for A and B.
5. **Freeze K.** Choose the screening budget K before test scoring. A percentage of held-out candidates can be used to make the budget scale with the test set, but record the exact rule and K calculation before seeing results.
6. **Primary metric:** lower-citation **pool-relative Recall@K**: the number of relevant lower-citation test records in the top K divided by all relevant lower-citation test records in that test pool. If the denominator is zero or too sparse for a useful interval, report not estimable rather than 0.
7. **Secondary metrics:** overall Recall@K and Precision@K; high- versus low-citation Recall@K and their gap; language-stratified Recall@K only where label and language validation support it; NDCG@K as a secondary ranking measure. Report positive denominators and uncertainty, not only point estimates.
8. **Primary comparison:** `Recall@K_B - Recall@K_A` for lower-citation relevant test records. A higher point estimate alone is not enough to claim improvement; the Prompt 07 protocol must set the uncertainty method, minimum subgroup adequacy rule and acceptable precision trade-off before looking at the held-out results.
9. **Interpretation:** the result applies to this constructed pool and the explicit feature change. It is not causal evidence about hidden features of deployed search engines, not absolute recall over all relevant literature, and not proof of a universal citation or language bias.

### Leakage, confounding and validity risks

- **Age/citation confounding:** older works have more time to gain citations. Record the citation snapshot and define citation groups within year.
- **Search-frame bias:** language-specific queries and OpenAlex's search ranking can affect which records enter the pool. Document collection routes; use seeded sampling from filtered universes and avoid building the pool only from default top-ranked results.
- **Language label error:** OpenAlex detects metadata language, which may differ from publication language. Validate sampled records and report uncertainty.
- **Label-source effects:** systematic-review labels are tied to a particular review's eligibility criteria; custom OpenAlex labels must use this project's written scope consistently.
- **Duplicate leakage:** preprints, conference versions and final articles can split across train/test unless deduplicated or clustered.
- **Sparse groups:** a few positive records make Recall@K unstable. Do not interpret a missing denominator or wide interval as absence of bias.
- **Incomplete relevance universe:** the pool omits relevant works not retrieved by the documented routes. All recall must be called pool-relative.
- **Query and date drift:** the API and citation graph change. Archive query parameters, seeds, IDs, export date and counts at data freeze.

## 7. Resource estimate and three-week feasibility

| Resource | Estimate / evidence status | Plan |
|---|---|---|
| API/data access | OpenAlex basic API access is publicly documented; user-run requests already succeeded [4]. | No GPU needed for metadata collection. Record the final API parameters and collection date. Keep API credentials out of shared files. |
| Annotation | **Primary bottleneck; duration not measured.** Current pilot required 28 records but yielded only six preliminary positives. | First run a fixed-scope candidate-pool pilot with enough records per language to estimate relevant-label yield. Expand only if label quality and subgroup counts are promising. |
| Training | TF–IDF + Logistic Regression is a standard CPU-compatible sparse-text pipeline; scikit-learn documents sparse input support [12]. | Use a CPU laptop or free Colab, cap TF–IDF vocabulary/`min_df` if needed, and run a small environment test before the full split. No LLM weights/GPU are required. Actual runtime and memory remain unmeasured until the final pool and code are run. |
| Three-week work plan | **Plausible for the lightweight model, conditional on data readiness.** The exact annotation burden is unknown. | Days 1–4: freeze scope and construct/inspect a larger candidate pool. Days 5–9: screen, deduplicate and audit labels/metadata. Days 10–12: decide subgroup estimability and freeze the protocol. Days 13–16: implement and validate A/B. Days 17–19: compute metrics and inspect failures. Days 20–21: document results and reproducibility. If the label gate fails, do not pretend the experiment fits; narrow the question. |

## 8. Go/no-go decision and fallback

**Current decision: CONDITIONAL GO for the OpenAlex pool-building stage; NO-GO for training/evaluating the main model on the current 28-record pilot.** The main model is computationally realistic on a CPU, but data quality and group-label sufficiency are not established.

**Preferred path:** construct a fixed, multilingual, relevance-labelled OpenAlex pool for the narrow task in Section 1, with the year range and queries frozen before model evaluation. Use the paired citation-blind/citation-aware Logistic Regression conditions described above.

**Fallback 1 — citation effect only:** if enough relevant records can be found for lower/higher citation groups but non-English positives remain sparse, keep the paired citation-feature experiment and label language-group analysis exploratory or not estimable. Do not claim a tested language effect.

**Fallback 2 — benchmark pipeline validation:** use an appropriate SYNERGY review or the Zenodo human-labelled screening data to test ingestion, label handling and metrics separately. Report this as a pipeline/reference benchmark on that dataset's topic, not as evidence about AI-literature language bias; do not mix review-specific labels from incompatible topics into the OpenAlex labels.

**Fallback 3 — stop/narrow:** if the on-topic pool cannot yield a defensible set of relevant records and adequate denominators, narrow the study to a clearly bounded citation-ranking audit or choose a different research question. Do not create a desired result by cherry-picking records or changing inclusion criteria after the model scores are inspected.

## 9. Independent verification checklist

- [ ] Freeze the operational scope and publication window (recommended main pool: 2015–2025).
- [ ] Save the exact OpenAlex filters, multilingual query strings, sampling seeds and collection date.
- [ ] Do not select the final pool only from default relevance-ranked search results; record each retrieval route.
- [ ] Reconcile field schemas and save a metadata-only snapshot with OpenAlex ID, DOI, title, year, `cited_by_count`, `language`, work type, and abstract availability indicator.
- [ ] Keep reconstructed abstract plaintext local; exclude it from public/shared archives.
- [ ] Deduplicate by OpenAlex ID, DOI and normalized title before labels and split.
- [ ] Apply the written inclusion/exclusion rubric and preserve reasons and provenance; audit the current 28 pilot labels before they are treated as final.
- [ ] Verify a sample of language labels against the actual publication or a reliable publisher record.
- [ ] Record citation-count snapshot date; predefine year-normalized citation groups and the `log1p(cited_by_count)` feature.
- [ ] Count verified positives by language and citation group; identify zero/low denominators before model work.
- [ ] Freeze split, TF–IDF fit rules, classifier parameters, K, primary metric, uncertainty method and precision trade-off before held-out evaluation.
- [ ] Confirm identical rows/settings for the citation-blind and citation-aware conditions; verify that citation count is the only changed feature.
- [ ] Verify software and data licences for any external src/dataset reused; cite SYNERGY and any borrowed benchmark appropriately.
- [ ] Save package versions, environment output, query parameters, ID lists, predictions, metric files and actual execution logs after the experiment is run.

## 10. Final recommendation

The **selected primary data-source strategy is a bounded OpenAlex pool with independent labels; the final labelled dataset is not yet validated**. This choice is based on its combined citation/year/language metadata and the successful metadata retrieval pilot, not on any claim that the 28-record sample is adequate. SYNERGY and the 2026 Zenodo benchmark are documented fallback resources for separate pipeline validation, while Aigner et al. provide a close published model-screening benchmark and public code repository. None of those alternatives has been verified as a ready-made multilingual, AI-literature-curation benchmark that satisfies all requirements.

The two primary comparison conditions are fixed: (A) TF–IDF title/abstract plus publication year with Logistic Regression, and (B) the same pipeline plus `log1p(cited_by_count)`. This is the simplest credible CPU-only experiment for isolating the explicit citation feature. The next research gate is to build and audit the larger pool and verify subgroup denominators. No model has been trained, no main ranking metric has been computed, and no citation or language bias result is claimed.

## Sources checked

1. OpenAlex Help Center. **Works attributes** — `language`, `publication_year`, `abstract_inverted_index`, `cited_by_count`, and other work fields. https://help.openalex.org/data/works/attributes/
2. OpenAlex Help Center. **Citations — Works** — definition of `cited_by_count` and citation matching. https://help.openalex.org/data/works/citations/
3. OpenAlex Help Center. **Searching** — text search and relevance scoring; OpenAlex's published search documentation notes that citation count contributes to the default relevance score. https://github.com/ourresearch/openalex-help/blob/main/content/api/searching.md
4. OpenAlex Help Center. **API reference / LLM Quick Reference** — access, filtering, sampling, page limits, seeds, and metadata licence statements. https://help.openalex.org/api/ ; https://help.openalex.org/api/llm-quick-reference/
5. ASReview. **SYNERGY dataset README** — collection size, labels, data fields, citation snapshot, and CC0 licence. https://github.com/asreview/synergy-dataset . Dataset DOI: https://doi.org/10.34894/HE6NAQ
6. Aigner, M. F., Ganzinger, M., Probst, P., Rinckens, M., & Pausch, T. M. (2026). **Comparing supervised machine learning and large language models in title-abstract screening.** *Systematic Reviews*, 15, 190. https://doi.org/10.1186/s13643-026-03199-6
7. Aigner et al. **Official code repository.** https://github.com/MarcoAigner/automated_title_abstract_screening
8. Li, Z., He, Q., Chen, W., Yang, K., & Gong, K. (2026). **Human-labeled benchmarks for automated literature screening and knowledge synthesis.** Zenodo record. https://zenodo.org/records/21853690 . Related preprint: https://www.alphaxiv.org/abs/2609.automating-literature-screening-llms
9. Céspedes, L., et al. (2025). **Evaluating the linguistic coverage of OpenAlex: An assessment of metadata accuracy and completeness.** *Journal of the Association for Information Science and Technology*, 76(6), 884–895. https://doi.org/10.1002/asi.24979
10. ASReview. **Official software repository and licence (Apache 2.0).** https://github.com/asreview/asreview
11. van de Schoot, R., et al. (2021). **An open source machine learning framework for efficient and transparent systematic reviews.** *Nature Machine Intelligence*, 3, 125–133. https://doi.org/10.1038/s42256-020-00287-7
12. scikit-learn. **LogisticRegression API reference** — supports dense and sparse matrices. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
13. scikit-learn. **Cross-validation and data splitting** — stratification, grouped splits and risks with rare classes. https://scikit-learn.org/stable/modules/cross_validation.html

**Search date:** 30 October 2026. The checks were targeted to official documentation, published papers, and repositories named in the project. They support the dataset/baseline recommendation above but do not constitute an exhaustive systematic review of all datasets or prove novelty.


## Additional source-integrity note (30 October 2026)

The Zenodo landing page for the human-labelled screening benchmarks displays DOI `10.5281/zenodo.21853690` in its record metadata, while its suggested citation text on the same page refers to `10.5281/zenodo.21853689`. This is an internal metadata/citation discrepancy on the source page. The package therefore links to the landing page and records the discrepancy; it does not silently choose one DOI for formal citation. Verify the canonical DOI with the record owner or the Zenodo DOI resolver before including this dataset in a formal bibliography. The dataset remains auxiliary only; its review-specific labels do not directly represent this project's AI-literature-curation relevance definition.
