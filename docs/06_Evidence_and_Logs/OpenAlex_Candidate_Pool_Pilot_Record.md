# OpenAlex Candidate-Pool Pilot Record

**Project:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation  
**Evidence source:** OpenAlex API outputs run by the student in Google Colab and pasted into the project conversation, 29–30 October 2026. The exact API response archive and timestamp were not saved.  
**Status:** Preliminary dataset feasibility evidence; not a benchmark and not an experiment result.

## 1. Objective

**Operational scope used for the pilot:** papers/resources directly studying computational or AI methods for scholarly-literature discovery and curation, including retrieval, citation searching, ranking, title/abstract screening, study selection, and systematic-review automation. This is not the general corpus of all AI application research.

Test whether OpenAlex can provide metadata and candidate records for a bounded study of AI-assisted scholarly literature searching/screening. This pilot checks query behaviour, metadata presence, language codes, and preliminary relevance yield. It does not test any model or establish bias.

## 2. What was run and observed

### 2.1 Topic/language exploration

The student queried OpenAlex topic groups with `has_abstract:true` and publication years `2015–2026`, and grouped results by OpenAlex language metadata. These API totals were the outputs at the time of query and can change as the index changes:

| Topic query | Matching works | English | Other-language examples in the returned top groups |
|---|---:|---:|---|
| Information Retrieval and Search Behavior (`T10286`) | 111,959 | 101,939 | Indonesian 1,467; Portuguese 1,343; Spanish 1,224; French 1,055; German 570; Ukrainian 549; Russian 524; Chinese 430 |
| Natural Language Processing Techniques (`T10181`) | 216,870 | 196,516 | French 3,627; Spanish 2,531; Portuguese 1,701; Russian 1,568; Indonesian 1,453; Ukrainian 1,105; German 902 |
| Text and Document Classification Technologies (`T11550`) | 58,856 | 49,921 | Indonesian 5,293; Portuguese 710; Spanish 570; French 358; Russian 320 |
| Publishing and Scholarly Communication (`T13516`) | 151,393 | 99,818 | Spanish 16,527; Portuguese 8,661; German 5,167; French 4,923; Chinese 2,772 |

These counts describe works that matched the topic filter and the requested metadata/time filters. They are not counts of papers relevant to AI-assisted literature curation. The query used `topics.id` for the table above, so it includes works with that topic assigned; it does not mean every record has that topic as its primary topic.

### 2.2 Targeted language-specific query audit

Four searches were executed with language filters and `has_abstract:true`, publication years 2015–2026, and `search.title_and_abstract` queries. The API-reported matching counts were:

| Language | Query concept | Matching count reported |
|---|---|---:|
| English | Automated/systematic-review screening + AI or ML | 49 |
| Indonesian | Tinjauan sistematis/skrining + kecerdasan buatan/pembelajaran mesin | 13 |
| Portuguese | Revisão sistemática/triagem + inteligência artificial/aprendizado de máquina | 262 |
| Spanish | Revisión sistemática/cribado + inteligencia artificial/aprendizaje automático | 356 |

The queries were translated and not semantically identical; these counts are not directly comparable language prevalence estimates. The output included examples of off-scope records, so relevance screening was required.

### 2.3 Metadata sample

A query-specific sample retrieved 67 unique records: 20 English, 7 Indonesian, 20 Portuguese, and 20 Spanish. Output checks showed no missing title, year, citation count, language code, or reconstructed abstract among these 67 records, and metadata-language values matched the language filter used for each group. This is a check on this sample only, not a general validation of OpenAlex metadata accuracy.

### 2.4 Balanced 28-record relevance pilot

A deterministic sample (`random_state=42`) selected seven records from each language subset of the 67-record sample. The seven Indonesian records were all available from the prior query sample. The relevance rubric was: include works that directly investigate AI/ML/NLP/computational methods for finding, ranking, screening, selecting, or curating scholarly publications; exclude unrelated AI applications or downstream extraction tasks that do not address that central task.

Latest working workbook counts (binary labels; preliminary, AI-assisted and not independently adjudicated):

| Metadata-language group | Relevant (`1`) | Not relevant (`0`) | Total |
|---|---:|---:|---:|
| English | 4 | 3 | 7 |
| Indonesian | 0 | 7 | 7 |
| Portuguese | 1 | 6 | 7 |
| Spanish | 1 | 6 | 7 |
| **Total** | **6** | **22** | **28** |

One Portuguese protocol-preparation paper was included under a broader AI-assisted systematic-review workflow interpretation, but its direct relevance to retrieval/ranking performance is borderline. The workbook records medium confidence for this case. These labels need human audit and must not be called verified ground truth.

## 3. What the pilot supports

- **VERIFIED — bounded to the API outputs:** OpenAlex queries ran from Colab; topic queries returned multilingual records; the sampled metadata fields were present in the 67-record sample; the 28-record working sheet contains 6 preliminary positive and 22 preliminary negative labels.
- **INFERRED:** OpenAlex is a promising candidate source for building a bounded pool, because the relevant metadata fields were available for this small sample.
- **NOT ESTABLISHED:** suitability of the data for the main experiment; adequate positive records within non-English or citation groups; representative retrieval behaviour; publication-language truth; a valid recall denominator; research novelty; presence or absence of citation/language bias.

## 4. Limitations and next gate

1. The 28 papers were sampled from separate language-specific queries. The group counts cannot be interpreted as natural prevalence or as the results of one common-language-neutral retrieval system.
2. Only six preliminary positive labels were recorded. The positive counts are English 4, Indonesian 0, Portuguese 1, and Spanish 1. This is insufficient to evaluate group-conditional recall or train/evaluate a credible ranker.
3. A relevance label derived from a title/abstract rubric is a project-specific annotation. Labels have not been independently adjudicated, and inter-annotator agreement was not measured.
4. OpenAlex `language` is database metadata, not automatically verified full-text publication language. Validate a sample against accessible source records and retain unknown/uncertain statuses in future data work.
5. Citation counts change over time. Record the query date and, for the eventual experiment, a citation snapshot/export date and a pre-defined citation grouping strategy.
6. The complete universe of relevant works is unknown; any recall metric from the constructed pool will be pool-relative.
7. No model was trained, no citation-feature ablation was executed, and no empirical bias result is claimed.

**Decision:** Continue data development conditionally. Do not train the main model on the current pilot. Prompt 06 has compared OpenAlex with relevant labelled screening datasets and documented access/terms and labeling requirements. The final pool and labels remain unvalidated. If there are not enough validated non-English positives, mark language-group analysis not estimable or narrow the study explicitly.

## 5. Data minimisation note

The submission package contains an abstract-free copy of the pilot workbook. Reconstructed plaintext abstracts were used locally during the screening pilot but are not included here. Retain the original working CSV privately and follow relevant source terms; do not publicly redistribute reconstructed plaintext abstracts.


## Data-quality note after final bundle audit

The abstract-free 28-record CSV/XLSX copy has 28 rows and 28 unique OpenAlex IDs, 6 preliminary relevant labels and 22 preliminary non-relevant labels. Required analysis columns (title, year, citation count, metadata language, label, reason, and label-confidence field) are non-missing. DOI is missing for three records. No abstract plaintext column is included in the bundle. These are preliminary AI-assisted labels, not an independently adjudicated reference standard.
