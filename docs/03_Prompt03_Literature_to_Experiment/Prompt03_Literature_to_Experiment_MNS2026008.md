# Prompt 03 — Literature-to-Experiment Mapping

**Project:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation  
**Chosen direction:** Pathway C — targeted modification of a lightweight trained ranker  
**Resource assumption:** CPU-only laptop or free Google Colab; approximately three weeks  
**Status:** Experiment plan drafted before the metadata pilots. Subsequent SYNERGY/OpenAlex metadata pilots are documented in Prompt 04 and the evidence folder. No main model or ranking experiment has been run; no main experimental results are claimed.


> **Operational scope for this plan:** the target literature is research on computational/AI methods for scholarly-literature discovery and curation (search, citation search, ranking, title/abstract screening, study selection, and systematic-review automation). It is not a corpus of all AI application papers. The OpenAlex pilot was queried under this narrow scope; labels do not transfer to a different scope.

## 1. Scope and decision

The submitted literature review frames AI-literature curation as a multi-stage pipeline and proposes group-conditional recall, a popularity-aware versus popularity-blind audit, and stage-wise loss analysis. The most relevant portions are the review's comparative table (Section 5 / Table 2 in the submitted source), its section on **popularity-aware versus popularity-blind ranking** (Section 5.4), and its future direction on **popularity-blind auditing** (Section 8.5). The review treats these as proposed directions, not completed empirical findings.

For a three-week project on modest hardware, the recommended experiment is a simple supervised text ranker with one explicit citation-derived feature. Compare:

- **Citation-aware condition:** TF-IDF features from title and abstract, plus publication year as a shared control and one citation-derived popularity feature.
- **Citation-blind condition:** the same TF-IDF features, the same publication-year control, the same labels, data split, classifier and parameters, but with the citation-derived feature removed.

Use logistic regression as the first choice because it is available in scikit-learn, trains quickly on sparse TF-IDF data, and provides a relevance score that can be used to rank papers. This is a **targeted adaptation inspired by the supervised TF-IDF methods in Aigner et al. (2026)**, not an exact reproduction of their original screening model: their paper did not use citation count as a feature. The addition and ablation of citation information are the proposed intervention.

The experiment tests the effect of an **explicit citation feature in this model and corpus**. It does not establish that all scholarly search systems are biased, or that citation popularity is the only mechanism affecting exposure.

## 2. Three published methods from the review that are practical to implement or reproduce

| Published method and source | Algorithm / original evaluation | Code, data or model access | Metrics and limitations | Resource requirement and fit |
|---|---|---|---|---|
| **Aigner et al. (2026), “Comparing supervised machine learning and large language models in title-abstract screening.”** | Four supervised classifiers—Naïve Bayes, SVM, random forest and logistic regression—using TF-IDF text features, compared with Llama-3.1-8B-Instruct on six labelled systematic-review datasets. The paper reports recall, specificity, precision, F1 and accuracy, including bootstrap confidence intervals. | **Verified public access:** the authors' GitHub repository contains notebooks/scripts, preprocessing, analysis and processed datasets: https://github.com/MarcoAigner/automated_title_abstract_screening. The classical models are standard scikit-learn models and do not require pretrained weights. Five datasets are freely available; one dataset is proprietary. Access to the code is verified, but the original clinical review datasets are not a suitable AI-literature benchmark without adaptation. | Performance differed by dataset. The original preprocessing removed records with non-English abstracts (as well as duplicates, very long abstracts and records without abstracts), so its evaluation cannot establish language fairness. Labels are inherited from human reviewers and are not an objective universal truth. | **Low for classical models** on CPU; the authors report the supervised-model training/prediction step took about 40 seconds on their datasets, but the exact time will depend on the new corpus and machine. **Best implementation foundation** for the chosen ranker, with the citation feature explicitly documented as the new change. |
| **ASReview — van de Schoot et al. (2021), “An open source machine learning framework for efficient and transparent systematic reviews.”** | Active learning for screening: the model prioritises records and updates its ordering from human inclusion/exclusion labels. Its simulation tools can evaluate screening trajectories on fully labelled datasets. This is a screening-prioritisation method, not a fixed citation-aware ranker. | **Verified public code:** https://github.com/asreview/asreview. The official project gives installation instructions (`pip install asreview`) and supports user-supplied CSV, RIS and XLSX records. No pretrained model weights are required for a basic active-learning run; the model is trained from labels. | Appropriate measures include recall against records screened, recall-versus-screening-effort curves, and workload needed to reach a target recall. Results depend on the initial labels, learner/query-strategy configuration and stopping rule. It cannot recover papers missing from the initial candidate set. | **Low–moderate** on CPU for a small corpus. A credible alternative if the project shifts toward stage-wise screening loss; **not the main method for the chosen citation-feature ablation**, because citation count is not a built-in intervention in the standard workflow. |
| **Rajit et al. (2025), “Automated citation searching in systematic review production: A simulation study.”** | One-hop citation-network exploration through OpenAlex and Semantic Scholar was simulated across 27 systematic reviews in health, environmental management and social policy. The paper evaluates recall, precision, and F1–F3 and analyses factors such as seed selection and API choice. | **Verified public access reported by the paper:** data are linked at https://github.com/darrenkjr/automated_citation_search_study. The authors also provide an open-source citation-search app at https://github.com/darrenkjr/automated_citationsearch_st. API access and current quotas must still be tested. | The study reported precision/F1 advantages in some comparisons but lower recall/F3 than the reference search strategy. Crucially, the reference strategy's 100% recall was assumed by design rather than independently proven against the full universe of relevant studies. API coverage, seed selection and identifier matching limit retrieval. | **Low CPU cost**, with time spent on API queries, identifiers and data cleaning. Useful as a supplementary candidate-generation method and for understanding Stage 1 losses; it is **not itself the trained ranking model** selected for Pathway C. |

### Why these three

They cover three relevant pieces of the curation pipeline and have accessible software or reproducible material. For the chosen experiment, Aigner et al. provide the most practical model foundation; ASReview provides a well-established screening alternative; and Rajit et al. provide a citation-based candidate-generation method that can inform a later stage-wise analysis.

The review also discusses Wang and Blei's **Collaborative Topic Modeling for Recommending Scientific Articles** (2011), which combines topic modeling and collaborative filtering using CiteULike user–article libraries. This is directly relevant to citation-informed recommendation, but it has a more involved model and a historical user–article dataset; I did not verify a maintained, ready-to-run src/data package during this check. It is better treated as related work rather than the three-week minimum implementation. Citation: https://www.cs.columbia.edu/~blei/papers/WangBlei2011.pdf.

## 3. Compare the three approved experimental pathways

| Pathway | Smallest working baseline | Testable question | Expected resource burden | Evidence required | Assessment |
|---|---|---|---|---|---|
| **A. Reproduction plus extension** | Re-run the public Rajit et al. automated citation-searching analysis on a small, accessible example or reproduce its retrieval procedure, then add citation/language-group metrics to an AI-paper collection. | Does one-hop citation searching show different pool-relative recall by citation and publication-language group in a bounded AI topic? | **Medium–high.** Requires understanding their original data protocol, API configuration and seeds, then building a new AI-topic benchmark. | Reproduction log; original-vs-reproduced metrics where the published benchmark permits; API snapshots; deduplicated AI records; relevance labels; group-conditional recall; analysis of discrepancies. | Credible, but it studies **candidate generation**, not the selected ranking-feature intervention. Language-group counts may be too sparse. |
| **B. Controlled comparison** | Compare a TF-IDF logistic-regression ranker with ASReview's active-learning prioritisation on the same fully labelled candidate pool and a matched screening budget. | Which approach recovers more relevant papers overall and within citation/language groups at the same screening effort? | **Medium.** Both methods can run on CPU, but protocol matching and ASReview simulation configuration add complexity. | Identical initial candidate pool and relevance labels; fixed or matched screening budget; configuration logs; recall/precision by group; screening-effort curves; error analysis. | Useful comparison, but the two methods differ in interaction/feedback mechanics, making the result less isolated than a single-feature ablation. |
| **C. Targeted modification — selected** | Train a TF-IDF + logistic-regression ranker with one citation-derived feature; compare it with the **same model without that feature**. | Holding text, candidate set, labels, train/test partitions, year control and model configuration constant, does adding citation information change overall ranking quality and pool-relative recall for lower-citation and non-English relevant papers? | **Low–medium.** Small CPU-feasible text model; primary effort is collecting and relevance-labelling a defensible corpus and checking group sizes. | Frozen candidate pool; source and citation-count snapshot date; verified language labels; human relevance decisions; identical splits and settings; ranked scores; overall and group metrics with uncertainty; documented failure cases. | **Recommended.** It changes one defined feature, preserves a direct comparator and matches the review's popularity-blind audit. The claim must remain limited to the explicit feature and tested corpus. |

## 4. Recommended minimum viable experiment for three weeks

### 4.1 Research question

**On a bounded, relevance-labelled AI-literature candidate pool, does adding a citation-derived popularity feature to a lightweight TF-IDF relevance ranker change recall@K for lower-citation papers and non-English papers, compared with the same ranker without that feature?**

Treat citation × language interaction as exploratory only if enough relevant examples occur in each group. Gap 3 (stage-wise loss) can be recorded as a by-product only when candidate-generation and ranking logs are available; do not expand the core project to full pipeline instrumentation.

### 4.2 Model conditions

- **Shared text features:** title + abstract transformed with TF-IDF.
- **Shared control:** publication year, represented identically in both conditions, to reduce age-related confounding.
- **Citation-aware ranker:** TF-IDF + publication year + one explicit citation-derived feature. Prefer a citation percentile within publication-year bands, or document and use a `log1p(cited_by_count)` feature with publication year retained in both models.
- **Citation-blind ranker:** exactly the same pipeline, with the citation-derived feature removed and nothing else intentionally changed.
- **Scoring/ranking:** logistic regression predicts the probability that a record is relevant; sort the held-out candidates by that score. The model's probability score is being used to create a ranking; this is not a claim that logistic regression is a dedicated learning-to-rank algorithm.

Do not add a language feature to the ranker for this experiment. Use publication language to define evaluation groups. Otherwise, removing citation information would no longer be the only intended intervention.

### 4.3 Corpus and labels

1. Select one narrow AI subtopic and a fixed publication-date range before evaluation.
2. Run a small metadata pilot first. Check how many records have usable titles/abstracts, citation counts and language metadata, and whether there are enough non-English records and lower-citation relevant papers.
3. Construct a bounded reference pool using a documented search query and, if feasible, one supplementary discovery route. Deduplicate records, then label relevance using explicit inclusion criteria. The pool must not be described as the complete universe of relevant AI papers.
4. Freeze the candidate IDs, relevance decisions, metadata snapshot date, preprocessing, citation-group definition, and train/test protocol before comparing model outputs.
5. Use a held-out test set or the same pre-specified folds for both rankers. No test relevance labels may be used for training, feature selection, or threshold selection.

A practical initial target is a few hundred candidate records, subject to the pilot. This is a feasibility target, not a statistically justified sample size. If a subgroup has too few relevant test records for stable estimates, widen the corpus/topic or report the subgroup as exploratory; do not conceal sparse coverage.

### 4.4 Metrics

Primary metric:

\[
\operatorname{Recall}_{g}@K =
\frac{\text{relevant test papers in group }g\text{ appearing in the top }K}
{\text{all relevant test papers in group }g}
\]

Report at least:

- overall recall@K and precision@K;
- recall@K for lower- and higher-citation groups;
- recall@K for English and non-English publication-language groups;
- NDCG@K as a secondary ranking-quality measure;
- counts/denominators for every subgroup, plus uncertainty intervals where the sample supports them;
- a short review of relevant papers moved down or lost when citation information is included.

Choose K before evaluating results, based on a plausible screening budget. Define citation groups in advance; for example, use within-year citation percentiles rather than raw citation thresholds alone. Citation counts change over time, so record the retrieval/snapshot date. Because language metadata may be wrong or missing, manually validate a sample and distinguish “non-English” from “language unknown.”

### 4.5 Three-week execution plan

| Time | Work | Deliverable / decision gate |
|---|---|---|
| **Days 1–3** | Select the subtopic and date range; test OpenAlex or another chosen source; inspect group counts, abstracts and metadata completeness. | Metadata pilot. **Go/no-go:** if non-English coverage is too small, broaden/revise the corpus before implementation. |
| **Days 4–7** | Deduplicate and label a bounded candidate pool; define inclusion rules and citation groups; lock evaluation budget K. | Versioned dataset/label file and data-protocol note. |
| **Days 8–11** | Implement TF-IDF + logistic regression; train the citation-aware and citation-blind conditions using identical splits and parameters. Unit-test the feature columns and rank outputs. | Runnable baseline, ablation variant and logs. |
| **Days 12–15** | Compute metrics on held-out data; check ID/label alignment, subgroup denominators and uncertainty; compare results. | Result CSV, tables and at least one plot. |
| **Days 16–18** | Examine failure cases, sensitivity to K and citation grouping; record any protocol changes and rerun where needed. | Deeper analysis and limitations. |
| **Days 19–21** | Freeze results; write the method/evaluation note and reproduction instructions; update `research_decisions.md` and `ai_assistance_log.md` with genuine actions. | Reproducible Prompt 03–experiment package. |

## 5. What must be personally verified before coding

- **Original method:** Read Aigner et al.'s methods and code structure; record exactly which parts are reused and which parts are changed. Do not claim the original paper included citation features.
- **Code and license:** Confirm the repositories' current license, package requirements and any third-party dataset terms. A public repository does not automatically grant rights to redistribute every dataset it references.
- **Data access:** Test a small API query, save the real response and record the query date. OpenAlex supports free basic API use; larger collection/paging may require a free API key, and requests are rate-limited. Official documentation: https://help.openalex.org/api/authentication/.
- **Metadata quality:** Check citation counts, publication year, language labels and abstracts on a sample. Do not equate missing language metadata with English or silently discard non-English records.
- **Language interpretation:** Decide whether the grouping is publication language, abstract language or full-text language. These are not interchangeable. For the core research question, use publication language where defensible and report metadata validation.
- **Relevance labels:** Write inclusion/exclusion criteria before annotation; retain the label source and adjudication notes. If only one reviewer labels the corpus, disclose that limitation and independently check a sample if possible.
- **Feature isolation:** Confirm that the citation-aware and citation-blind versions differ only in the single citation-derived input. Keep year and text features, model, parameter settings, train/test folds, K and evaluation code identical.
- **Confounding:** Older papers often have more citations. Prefer within-publication-year citation percentiles or retain publication year as a shared control; interpret results as the effect of the explicit citation feature under this protocol, not proof of a universal causal mechanism.
- **Sample sufficiency:** Count relevant papers within each citation/language group in the held-out pool. If numbers are sparse, do not present unstable subgroup estimates as definitive.
- **Reproducibility:** Save raw metadata responses or permitted snapshots, IDs, labels, citations-count timestamp, query string, package versions, random seed/split, commands, result CSVs and figures.

## 6. Evidence boundary and conclusion

This plan does not report results or establish novelty. The review's comparative analysis includes published work on supervised screening, active learning, citation searching, and scholarly recommender bias. The proposed study is a controlled feature ablation inspired by those sources, with the citation feature as the only intended change. It can test whether that explicit feature changes ranking performance and group-conditional recall in the selected corpus; it cannot establish the behavior of all AI literature-curation systems.

The complete relevant-paper universe is not known, so the reported recall is **pool-relative recall**. Any conclusion about non-English papers depends on language metadata quality and adequate group sizes. If the metadata pilot finds too few non-English or lower-citation relevant papers, adjust the corpus before running the main comparison rather than reporting a false sense of certainty.

## References and implementation links

- Aigner, M. F., Ganzinger, M., Probst, P., Rinckens, M., & Pausch, T. M. (2026). *Comparing supervised machine learning and large language models in title-abstract screening*. https://doi.org/10.1186/s13643-026-03199-6. Code: https://github.com/MarcoAigner/automated_title_abstract_screening
- van de Schoot, R., et al. (2021). *An open source machine learning framework for efficient and transparent systematic reviews*. https://doi.org/10.1038/s42256-020-00287-7. Code: https://github.com/asreview/asreview
- Rajit, D., Du, L., Teede, H., & Enticott, J. (2025). *Automated citation searching in systematic review production: A simulation study*. https://doi.org/10.1017/rsm.2024.15. Code/data: https://github.com/darrenkjr/automated_citation_search_study
- Färber, M., Coutinho, M., & Yuan, S. (2023). *Biases in scholarly recommender systems: impact, prevalence, and mitigation*. https://doi.org/10.1007/s11192-023-04636-2
- Wang, C., & Blei, D. M. (2011). *Collaborative Topic Modeling for Recommending Scientific Articles*. https://www.cs.columbia.edu/~blei/papers/WangBlei2011.pdf
