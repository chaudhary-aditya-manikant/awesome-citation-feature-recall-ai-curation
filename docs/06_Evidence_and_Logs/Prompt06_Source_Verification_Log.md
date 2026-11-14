# Prompt 06 — Source Verification Log

**Date:** 30 October 2026

This log records the primary online sources checked for the Prompt 06 dataset-and-baseline validation sheet. The dataset candidate decision is conditional; source availability does not mean a repository has been installed, data downloaded, or model reproduced.

| Source | Claims checked | Boundary / result |
|---|---|---|
| [OpenAlex Works attributes](https://help.openalex.org/data/works/attributes/) | `language`, `publication_year`, `abstract_inverted_index`, `cited_by_count`. | Official field documentation checked. `language` is inferred from metadata and is not guaranteed to equal full-text language; abstracts are represented as inverted indexes. |
| [OpenAlex Citations](https://help.openalex.org/data/works/citations/) | Meaning of citation count. | Official documentation confirms citations are built from matched references; final count snapshot date should be recorded. |
| [OpenAlex Search](https://github.com/ourresearch/openalex-help/blob/main/content/api/searching.md) | Default search relevance behavior. | Official documentation indicates the default relevance score uses text similarity and a citation-count contribution. Do not use default top-ranked results as the only candidate pool. |
| [OpenAlex API reference](https://help.openalex.org/api/) and [API quick reference](https://help.openalex.org/api/llm-quick-reference/) | API access, filters, random sampling, seeds and CC0 data statement. | Official docs checked. User-run pilot already successfully queried the API; final data snapshot has not been frozen. |
| [SYNERGY repository](https://github.com/asreview/synergy-dataset) | Record counts, review-specific labels, fields, dataset licence and the current published collection list. | Public README reports 169,288 records, 26 reviews, 2,834 included records, and CC0 1.0. Current published list contains `Hall_2012` for Computer Science; the local `Hall_2011.csv` file mapping remains unresolved. |
| [Aigner et al. (2026) article](https://doi.org/10.1186/s13643-026-03199-6) and [code repository](https://github.com/MarcoAigner/automated_title_abstract_screening) | TF–IDF/classical ML comparators, labelled reviews, public code availability, exclusion of non-English abstracts in preprocessing. | Article and repository pages checked. Repository was not cloned, installed or reproduced. |
| [Céspedes et al. (2025)](https://doi.org/10.1002/asi.24979) | OpenAlex language metadata quality. | The published study reports language-label errors in its manually checked sample, so the project should validate metadata language. The study's sample error rate is not assumed to be this project's sample error rate. |
| [SYNERGY/ASReview method paper](https://doi.org/10.1038/s42256-020-00287-7) and [ASReview repository](https://github.com/asreview/asreview) | Active-learning screening method and software licence. | Paper and official repository checked; Apache 2.0 is stated in the repository. ASReview was not installed or run. |
| [Zenodo human-labelled benchmark record](https://zenodo.org/records/21853690) and [associated preprint](https://www.alphaxiv.org/abs/2609.automating-literature-screening-llms) | Dataset description and relevance-label counts. | Landing page lists 440 literature-screening records for ML in concrete (272 relevant, 168 irrelevant), as well as other separate tasks. The exact file schema, language coverage and licence were not verified by downloading the CSV; the dataset is treated only as an auxiliary candidate. |
| [scikit-learn LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) and [cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html) | Sparse matrix support, class imbalance and split design. | Official documentation checked. No project classifier has been trained. |

## Searches used

- `site:github.com/asreview/synergy-dataset label_included cited_by_count language`
- `site:help.openalex.org/data/works/attributes abstract_inverted_index language cited_by_count`
- `site:help.openalex.org/api/searching relevance_score citation count`
- `site:github.com/MarcoAigner/automated_title_abstract_screening non-English abstracts TF-IDF logistic regression`
- `"Evaluating the linguistic coverage of OpenAlex" language metadata accuracy`
- `"Human-labeled benchmarks for automated literature screening and knowledge synthesis" Zenodo`
- `site:github.com/asreview/asreview Apache 2.0 license`
- `scikit-learn LogisticRegression sparse matrix documentation`

## Verification boundary

The checked sources support the statements in the Prompt 06 sheet. The searches were targeted rather than exhaustive. No repository was reproduced, no new dataset was downloaded in this research step, and no model metric was generated. The user's OpenAlex/SYNERGY pilot outputs remain the only reported local data executions.

## Follow-up checks — 30 October 2026

| Source | New verification | Project implication |
|---|---|---|
| [AHRQ 2025 rapid review update](https://www.ncbi.nlm.nih.gov/books/NBK620201/) | Publisher/NCBI metadata reports 95 included studies and DOI 10.23970/AHRQEPCWHITEPAPERMACHINE2. The methods describe searches of PubMed, Embase and ACM DL and note English-language study scope. | Use as evidence that AI-assisted evidence synthesis is established; do not use it to claim multilingual evidence coverage. |
| [Fleurence et al. (2026)](https://pubmed.ncbi.nlm.nih.gov/42447981/) | PubMed metadata and abstract report 115 included studies; 51 title/abstract-screening and 33 data-extraction studies. | Broad AI-in-systematic-review claims are not novel; performance is task- and workflow-dependent. |
| [Barragán et al. (2026)](https://pubmed.ncbi.nlm.nih.gov/42621567/) | PubMed metadata reports 174 unique studies, 2019–2026, in a scoping review of AI resources for title/abstract screening. | Additional close prior work; no broad novelty claim is justified. |
| [Khatoon and Amjad (2026)](https://doi.org/10.3390/computers15090594) | DOI and article title verified. Search-indexed article text describes a ranking framework combining temporal, lexical-relevance and citation-behaviour signals and discusses feature contribution. | Closely related citation-feature ranking work; the current candidate contribution is narrowed to group-conditional lower-citation Recall@K, and novelty remains unknown. |
| [Gusenbauer & Haddaway (2020)](https://doi.org/10.1002/jrsm.1378) | PubMed and publisher metadata verify the title, authors, year, volume, pages and DOI; the study evaluates 28 academic search systems. | Reinforces that retrieval quality and system choice are established empirical topics. |
| [Rajit et al. (2025)](https://doi.org/10.1017/rsm.2024.15) | PubMed record verifies DOI 10.1017/rsm.2024.15, 27 systematic reviews, and recall/precision/F-score comparisons for OpenAlex and Semantic Scholar citation searching. | Use exact DOI 10.1017/rsm.2024.15; do not substitute the PMC identifier as the DOI. |
| [Zenodo benchmark record](https://zenodo.org/records/21853690) | Landing page metadata shows DOI 10.5281/zenodo.21853690, while the suggested citation text on that same page refers to 10.5281/zenodo.21853689. The licence field was not established from the captured page. | DOI discrepancy is explicitly flagged; do not redistribute until the canonical citation and licence are verified. |

These were targeted checks, not a comprehensive systematic search. Search snippets and abstracts were used where full text could not be opened; no unsupported claim of full-text review is made.
