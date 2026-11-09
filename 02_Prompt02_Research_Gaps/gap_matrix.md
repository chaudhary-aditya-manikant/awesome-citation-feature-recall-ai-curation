# Research Gap Matrix: Citation-Feature Effects on Lower-Citation Recall in AI Literature Curation

**Research topic:** Recall bias toward highly cited and English-language papers in AI literature curation  
**Evidence-check date:** 22 October 2026  
**Scope:** Bounded checks of the supplied review, selected primary papers, and related work. This is not a systematic review. Source verification does not establish research novelty.

> **Current-status note (30 October 2026):** This is the Prompt 02 gap-matrix deliverable based on the literature checks recorded at its stated evidence date. Later dataset feasibility work is documented separately in Prompt 04 and the evidence files in this package. The later OpenAlex pilot does not establish the research gap's novelty or validate the main experiment dataset.


## Status definitions

- **Verified — bounded:** The cited source supports the specific claim stated; this does not imply that every related study has been checked.
- **Partly verified:** Only an abstract, selected passages, or part of the underlying evidence was checked.
- **Inferred:** A plausible interpretation or testable hypothesis, not an established finding.
- **Unknown:** Available checks do not settle the question. Unknown novelty must not be presented as proof of originality.

## 1. Selected source-evidence inventory

| Study / method | Finding relevant to this project | Limitation for this project | Evidence status |
|---|---|---|---|
| Przybyła et al. (2018), RobotAnalyst | Evaluated 22 systematic-review reference collections and 43,610 abstract-level decisions. Screening effort needed to identify 95% of abstract-level inclusions was reduced in 19 of 22 collections. | Addresses screening prioritisation and workload; does not provide recall jointly stratified by citation prominence and publication language in the checked passages. | **Verified — bounded.** [PubMed](https://pubmed.ncbi.nlm.nih.gov/29956486/); [DOI](https://doi.org/10.1002/jrsm.1311). |
| Rajit et al. (2025), automated citation searching | Evaluated 27 systematic reviews using OpenAlex and Semantic Scholar and reported precision/F1 trade-offs with lower recall/F3 than the reference strategy. The reference strategy's recall was assumed to be 100% by design. | The assumed reference recall is not independent proof that the complete universe of relevant papers was found. The checked text does not provide joint citation-by-language recall. | **Verified — bounded.** [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12621532/). |
| Aigner et al. (2026), title/abstract screening | Evaluated six systematic-review datasets using supervised models and Llama-3.1-8B-Instruct; performance varied by dataset. The checked methods state that records with non-English abstracts, duplicates, exceptionally long abstracts, and records without abstracts were removed during preprocessing. | An evaluation that excludes records with non-English abstracts cannot establish comparative model performance for English and non-English papers. | **Verified — selected claims.** [Publisher page](https://link.springer.com/article/10.1186/s13643-026-03199-6). |
| Fleurence et al. (2026), rapid review of generative AI for systematic reviews | The abstract reports 115 included studies, including 51 on title/abstract screening and 33 on data extraction, and states that selected high-quality evaluations reported sensitivity of at least 90%. The full review describes a 94.4%–99.8% range for selected evaluations in its title/abstract-screening discussion. | These review-level summaries should not be generalized to every tool or task without checking the original studies, denominators, and evaluation conditions. | **Verified — review-level claim; partly verified — original-study audit.** [PubMed](https://pubmed.ncbi.nlm.nih.gov/42447981/); [DOI](https://doi.org/10.1016/j.jval.2026.06.012). |
| Beel and Gipp (2009), citation counts and Google Scholar ranking | Empirically studies the influence of citation counts on Google Scholar ranking. | Historical and system-specific evidence; it does not establish current behavior across all search and curation systems. | **Verified — bounded.** [DOI](https://doi.org/10.1109/RCIS.2009.5089308). |
| Rovira, Codina, and Lopezosa (2021), language bias in Google Scholar ranking | Directly studies language-specific ranking and citation-based rank. In their sample, 91% of non-English documents appeared below result 900, compared with 3.7% of English documents. | The percentages are specific to that study and are not universal rates or a direct AI-literature recall benchmark. | **Verified — bounded.** [Full paper](https://www.mdpi.com/1999-5903/13/2/31); [DOI](https://doi.org/10.3390/fi13020031). |
| Yang, Jiang, and Baldwin (2024), multilingual information retrieval | Examines language bias and mitigation methods in multilingual information retrieval. | Establishes relevant adjacent work on language fairness, but is not itself a direct study of AI-literature curation. | **Verified — bounded.** [ACL Anthology](https://aclanthology.org/2024.mrl-1.23/). |
| Céspedes et al. (2025), OpenAlex language metadata | Examines language metadata coverage and accuracy, including manual checks of 6,836 articles and inaccuracies in language labels. | A database language field should not automatically be treated as ground truth. | **Verified — bounded.** Relevant if OpenAlex is used; validate labels or conduct a sensitivity analysis. [DOI](https://doi.org/10.1002/asi.24979). |
| Barragán et al. (2026), AI resources for title/abstract screening | Scoping review of AI resources for title-and-abstract screening. | Shows screening automation is an established research area; does not itself answer whether citation-by-language losses are measured at each pipeline stage. | **Verified — bounded.** [DOI](https://doi.org/10.1002/cesm.70098). |
| Khatoon and Amjad (2026), scientific-publication ranking | Proposes a ranking framework using temporal relevance, lexical relevance, and citation behavior. | Relevant prior citation-aware ranking work; does not by itself establish the effect of removing citation features on group-conditional recall. | **Verified — bounded.** [DOI](https://doi.org/10.3390/computers15090594). |

## 2. Research gap matrix

| Candidate gap and basis in the review | Research question | Proposed test or evidence needed | Verification status and limitations |
|---|---|---|---|
| **1. Group-conditional recall.** The review discusses denominator uncertainty and group-conditional recall. | Do pool-relative retrieval-recall rates differ across citation and publication-language groups among relevant AI papers? | Build a bounded, relevance-labelled pool using documented discovery routes. Record citation count and language, plus year and subfield where available. Report overall and group-conditional recall with uncertainty. | **Source claim: verified on a bounded basis. Novelty: unknown.** The inspected main texts of RobotAnalyst, Rajit et al., and Aigner et al. do not report recall jointly stratified by citation prominence and publication language. Other systems and supplements were not exhaustively checked. Recall will be pool-relative, not absolute. |
| **2. Citation × language interaction.** The review proposes a possible interaction and compounded disadvantage. | After suitable controls, does the association between citation prominence and retrieval success differ between English and non-English AI papers? | Compare an additive model with a citation-by-language interaction model on a labelled pool. Report effect sizes and uncertainty; control for publication year and field where possible and inspect sparse cells. | **Related overlap: verified. Exact AI-curation novelty: unknown.** Rovira et al. examine language-specific Google Scholar ranking and citation-based rank; Yang et al. study multilingual-IR language fairness. A systematic novelty search has not been completed. Observational results would not by themselves establish causation. |
| **3. Stage-wise loss.** The review describes candidate generation, ranking, and screening as distinct stages. | At which pipeline stage are relevant papers lost, and do losses differ by citation or language group? | Log candidate identifiers, ranks, and screening decisions. Estimate stage-specific attrition by group and identify transitions where relevant records disappear. | **Pipeline framing: verified. Field-wide absence: unknown.** The inspected systems use different metrics and do not establish a complete group-stratified audit. Feasibility depends on access to candidate lists, ranks/scores, and screening logs. |
| **4. Popularity-blind ranking.** The review discusses citation confounding and popularity-blind ranking. | Does removing explicit citation-count features improve recall for lower-citation papers while preserving overall relevance? | Use the same candidate set, queries, labels, text features, and preprocessing. Compare transparent citation-aware and citation-blind rankers; report overall precision/recall and group-conditional recall. | **Rationale: supported by adjacent work. Effect and novelty: unknown until tested and searched.** A controllable citation-aware comparator is required. Do not assume that tools such as RobotAnalyst or ASReview use citation-aware ranking by default, and do not infer proprietary ranking internals. |
| **5. Multilingual query expansion.** The review discusses language and database-coverage differences. | Does multilingual or translated query expansion recover more relevant non-English AI papers at a comparable screening budget? | Compare English-only retrieval with pre-specified translated or multilingual terms. Measure pool-relative recall, precision, unique relevant records, and screening load at a matched budget. | **Language-bias background: verified. Query-expansion benefit and novelty: unknown.** Validate translations and language labels, confirm the available search/API terms, and ensure the pool includes enough non-English records. OpenAlex language-metadata errors are a relevant consideration if that source is used. |

## 3. Provisional prioritisation

This ranking reflects feasibility and the measurement logic of the proposed project. It is **not** a ranking of novelty.

| Rank | Candidate | Significance | Main resources | Main feasibility risk |
|---|---|---|---|---|
| 1 | Group-conditional recall benchmark | Provides the measurement basis for subsequent comparisons. | Bounded relevant-paper pool, documented multi-route search, citation/language metadata, relevance labels. | Requires adequate labels and enough non-English and lower-citation records. |
| 2 | Citation × language interaction | Tests whether the two dimensions may be associated with a compounded retrieval disadvantage. | Benchmark dataset plus adequate group counts and relevant covariates. | Sparse citation-by-language groups may make estimates unstable. |
| 3 | Popularity-blind ranking audit | Tests a concrete mitigation rather than relying only on aggregate metrics. | Fixed candidate set and labels; transparent citation-aware and citation-blind rankers. | Requires an auditable comparator and control of all other ranking inputs. |

## 4. Overall conclusion and limitations

The reviewed and checked sources establish that citation-related ranking, language bias in scholarly search, multilingual information retrieval, and automated screening are existing research areas. A broad claim that these topics have never been studied is not supported.

A bounded audit of joint citation- and publication-language differences in AI-literature retrieval remains a candidate research direction, but its novelty has **not** been established. A systematic search should document databases, exact queries, search dates, eligibility criteria, deduplication, and screening decisions before a novelty claim is made.

No dataset has been selected, no baseline has been run, and no experiment or empirical result is claimed here. The proposed tests depend on dataset access and licence, relevance-label provenance, language metadata quality, non-English coverage, and sufficient sample sizes.

## References checked

- Przybyła et al. (2018). *Prioritising references for systematic reviews with RobotAnalyst: a user study.* https://doi.org/10.1002/jrsm.1311
- Rajit et al. (2025). *Automated citation searching in systematic review production: A simulation study.* https://pmc.ncbi.nlm.nih.gov/articles/PMC12621532/
- Fleurence et al. (2026). *The Use of Generative Artificial Intelligence in Systematic Literature Reviews: A Rapid Review of the Literature.* https://doi.org/10.1016/j.jval.2026.06.012
- Aigner et al. (2026). *Comparing supervised machine learning and large language models in title-abstract screening.* https://doi.org/10.1186/s13643-026-03199-6
- Beel and Gipp (2009). *Google Scholar's Ranking Algorithm: The Impact of Citation Counts (An Empirical Study).* https://doi.org/10.1109/RCIS.2009.5089308
- Rovira, Codina, and Lopezosa (2021). *Language Bias in the Google Scholar Ranking Algorithm.* https://doi.org/10.3390/fi13020031
- Yang, Jiang, and Baldwin (2024). *Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods.* https://aclanthology.org/2024.mrl-1.23/
- Céspedes et al. (2025). *Evaluating the linguistic coverage of OpenAlex: An assessment of metadata accuracy and completeness.* https://doi.org/10.1002/asi.24979
- Barragán et al. (2026). Review of AI resources for title-and-abstract screening. https://doi.org/10.1002/cesm.70098
- Khatoon and Amjad (2026). *A Ranking Framework of Scientific Publications Using Temporal and Lexical Relevance and Citation Behavior.* https://doi.org/10.3390/computers15090594
- Gusenbauer and Haddaway (2020). *Which academic search systems are suitable for systematic reviews or meta-analyses?* https://doi.org/10.1002/jrsm.1378


## Scope clarification after the metadata pilots (30 October 2026)

**Operational scope used in this submission:** the target literature is work that directly studies computational/AI methods for scholarly-literature discovery and curation (search, citation search, ranking, title/abstract screening, study selection, and systematic-review automation). It is **not** a corpus of all papers about AI applications in medicine, education, or other domains. The current 28-record pilot was built to test this narrow scope; its labels do not transfer to a broader AI-domain corpus.

This operational scope is the one used to screen the 28-record OpenAlex pilot. The pilot results do not establish prevalence, retrieval recall, or research bias. The language-specific queries and quota-balanced sample do not form a population-representative benchmark. The final evaluation pool must be rebuilt under a frozen collection protocol before any model result is interpreted.

## 3. Literature update and novelty downgrade (30 October 2026)

The targeted follow-up search adds several directly relevant 2026 sources and makes the novelty boundary narrower:

- **Khatoon and Amjad (2026)** propose a scientific-publication ranking framework that combines temporal, lexical relevance and citation-behaviour signals. The article explicitly discusses the limited evaluation of individual signals. This is close to the project's feature-ablation rationale and prevents any claim that combining or removing citation-related ranking signals is itself new. The remaining candidate distinction is the specific outcome: group-conditional Recall@K for lower-citation *relevant* records in a defined AI-literature-curation pool. [Article](https://www.mdpi.com/2073-431X/15/9/594), DOI: https://doi.org/10.3390/computers15090594.
- **Fleurence et al. (2026)** review 115 studies on generative AI across systematic-review tasks, with 51 title/abstract-screening studies and 33 data-extraction studies. This further confirms that AI-assisted review workflows are a mature and fast-moving research area; it does not specifically test the proposed citation-feature ablation. [PubMed](https://pubmed.ncbi.nlm.nih.gov/42447981/), DOI: https://doi.org/10.1016/j.jval.2026.06.012.
- **Barragán et al. (2026)** conduct a scoping review of AI resources for title/abstract screening, including 174 unique studies in the final analysis. This is additional evidence against broad novelty claims about AI screening resources. [PubMed](https://pubmed.ncbi.nlm.nih.gov/42621567/), DOI: https://doi.org/10.1002/cesm.70098.
- **Adam et al. (2025), AHRQ rapid review update**, includes 95 studies and reports task-dependent performance; its review methods excluded non-English studies, which is a limitation when using it to describe multilingual evidence. [NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK620201/), DOI: https://doi.org/10.23970/AHRQEPCWHITEPAPERMACHINE2.

### Revised novelty assessment

**Novelty remains UNKNOWN and is not claimed.** The proposed work is a narrow, course-scale empirical ablation with a specific group-conditional recall outcome. The current literature search does not prove that no equivalent study exists. The study should be described as a replication/extension or exploratory controlled comparison unless a systematic, documented search identifies a clear and defensible novelty distinction. A successful experiment may still be useful pedagogically even if it is not publication-level novel.
