# Prompt 04 Addendum — Dataset Candidate Comparison and Decision

**Student:** Aditya Chaudhary  
**Enrollment:** MNS2026008  
**Course:** AI Tools for Research  
**Project:** *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*  
**Review date:** 30 October 2026  
**Purpose:** Reconcile the earlier conditional feasibility decision with the observed pilots and publicly documented alternative datasets before moving to the next implementation phase.

## Decision in brief

**Selected data strategy: construct a bounded, on-topic candidate pool from OpenAlex and independently label it under a frozen eligibility rubric. Status: CONDITIONAL GO for pool construction; NO-GO for model training until the dataset acceptance gate passes.** This is a decision about the source strategy, not a claim that a final dataset already exists.

The current 28-record OpenAlex pilot is not an eligible evaluation set. Its six labels are preliminary and AI-assisted; it has no Indonesian positives and only one each in Portuguese and Spanish. The SYNERGY `Hall_2011.csv` pilot is also a no-go for the intended joint question: 340 records, four review-included records, and all language values `en`. Neither pilot demonstrates citation or language bias.

## Candidate comparison matrix

| Candidate | Topic fit to literature-curation question | Record-level labels | Citation/year/text metadata | Language suitability | Access/licence evidence | Decision |
|---|---|---|---|---|---|---|
| **A. OpenAlex-derived custom pool** | **Best fit** if routes are limited to scholarly retrieval, citation searching, ranking/recommendation, title/abstract screening, study selection, and evidence-synthesis automation. | No project-specific labels supplied; requires independent screening and an audit trail. | Official API supports works metadata including title, publication year, `cited_by_count`, language and abstract-inverted-index fields. Text search's relevance score includes a citation-count component, so default top-ranked results alone are not a neutral candidate frame. | Potentially multilingual, but group coverage and metadata accuracy must be measured in the actual pool. Treat field as **metadata language**, not verified publication language, until audited. | OpenAlex documentation states its data are CC0 and basic API access is available. Follow current API limits and keep credentials private. | **Preferred source strategy, conditional.** Construct and audit a larger pool; do not train on the current pilot. |
| **B. Mendeley Data: AI-based decision support in higher education** | AI-topic corpus, but the included studies concern decision support in higher education, **not tools for literature curation**. Using it as the main corpus would change the research task and require a revised title/question. | Source page reports record-level screening decisions: 1,105 records screened, 531 included. Labels are specific to that review's criteria. | Source description reports title/abstract, year, citations and other metadata in the corpus files. | Explicitly English-only search (`language:en`); unsuitable for an English/non-English comparison. | Mendeley Data page states CC BY 4.0. Dataset: https://data.mendeley.com/datasets/x3nd2k9dkn/1 | **Not primary** for current question. Possible pipeline or scope-changed citation-ablation benchmark only. |
| **C. CAIR-Nepal AI Bias Research Landscape** | AI/algorithmic-bias research landscape, adjacent to AI research but not specifically literature-curation methods. | The dataset description does not report project-specific include/exclude screening labels; these would need to be created and validated. | Public description reports 692 records (2012–2026), with year and OpenAlex-derived citation metadata; availability/completeness of title/abstract and all fields must be inspected in the actual file before use. | No verified record-level language-group counts in the page description. Do not assume multilingual coverage. | Official page: https://www.cair-nepal.org/publications/datasets/ai-bias-research-landscape/ . Exact licence/access terms were not established from the retrieved page description and remain **UNKNOWN**. | **Not primary** without file inspection, label creation and scope change. Useful as a lead, not a validated dataset. |
| **D. SYNERGY `Hall_2011.csv` pilot** | Scope match to AI-literature curation not established; the records appeared related to fault prediction/detection and fault-tolerant systems. | 4 positive and 336 negative review-specific labels. | In the executed export, 340 rows; title, abstract, year, citations and language field were present. | All 340 explicit language values were `en`. | SYNERGY repository documents dataset CC0, but the local `Hall_2011` name does not match the current public README's `Hall_2012` collection; discrepancy unresolved. https://github.com/asreview/synergy-dataset | **NO-GO** as the main dataset for this project. Retain only as pilot evidence. |
| **E. Zenodo human-labelled literature-screening benchmarks** | Publicly described benchmark topics include concrete materials science, nanopore transport and lithium extraction, not AI-literature curation. | Human relevance labels are available for 440, 205 and 200 records respectively, under each benchmark's own inclusion criteria. | Zenodo description reports DOI, year, title, abstract and binary labels for screening datasets. Citation metadata is not established as a complete required field set in the summary. | Language coverage and language-group positive counts are not reported in the retrieved record description. | Official record: https://zenodo.org/records/21853690 . Exact licence and any redistribution conditions must be confirmed before reuse; not treated as verified here. | **Not primary** for current question. Could be a separate software smoke test if its licence and data are checked. |

## Why OpenAlex remains the least misleading choice

OpenAlex is not a ready-labelled benchmark. It is the most on-topic route among the candidates reviewed because the target corpus itself can be defined as research about scholarly-literature curation, and the source exposes the core bibliographic metadata needed for the controlled ranker. The cost is annotation work and the risk that the constructed pool is sparse or selection-biased. That risk must be measured, not hidden.

The current default search score is not citation-neutral: OpenAlex's official search documentation states that text similarity and a capped citation-count contribution both affect relevance ranking. Therefore the acquisition plan must log multiple prespecified routes, avoid selecting only the top-ranked records, deduplicate, and report the resulting pool as constructed and incomplete. Language comparisons must use validated metadata-language groups and must not equate a language-specific query sample with the natural prevalence of that language.

## Pre-registered acceptance gates for the final pool

Before modelling, the data log must show:

1. A fixed scope, publication window, query-route list, acquisition timestamp, route provenance, and API parameters.
2. A deduplicated pool with title, year, citation snapshot, language metadata, abstract availability, label, label rationale, and source route.
3. Written inclusion/exclusion criteria applied consistently across citation and language groups.
4. Human review of every final label; uncertain records adjudicated or excluded. If no second reviewer is available, use a seeded recheck as a consistency audit and state that it is not inter-rater validation.
5. Language metadata validation against a reliable publisher/library record for a stratified sample.
6. Positive-label counts by split, citation group and metadata-language group. Use the Prompt 07 minimum denominators; where they fail, narrow or mark the corresponding comparison not estimable rather than changing the threshold after seeing test scores.
7. No reconstructed abstract plaintext in the shared submission archive.

## Final Prompt 04 decision

- **GO:** continue construction and audit of a bounded OpenAlex pool for the narrowly defined literature-curation task.
- **NO-GO:** use the existing 28-record OpenAlex pilot or `Hall_2011.csv` as the main model evaluation set.
- **CONDITIONAL:** retain confirmatory language-group analysis only if the audited final pool passes the frozen positive-count and language-validation gates. If it fails, the report must explicitly narrow the empirical claim to citation-feature ablation within the bounded pool, or stop if even citation-group denominators are inadequate.
- **UNKNOWN:** exact novelty; whether the full on-topic pool will contain enough human-verified relevant non-English records; the final annotation workload; and final subgroup estimability.

## Source checks

1. OpenAlex API reference and data/licence documentation: https://help.openalex.org/api/ ; https://help.openalex.org/data/works/attributes/ ; https://help.openalex.org/api/searching/ . The search page explains the citation contribution to relevance score; the API page documents CC0 data.
2. Mendeley Data, *Reproducibility data and code for A Systematic Literature Review of AI-Based Decision Support in Higher Education (2015–2026)*: https://data.mendeley.com/datasets/x3nd2k9dkn/1 . Page description reports 1,190 retrieved unique records, 1,105 screened records, 531 included records, English-only filters and CC BY 4.0.
3. CAIR-Nepal, *AI Bias Research Landscape*: https://www.cair-nepal.org/publications/datasets/ai-bias-research-landscape/ . Page description reports 692 curated records with publication years and OpenAlex-derived citation metadata; record-level labels and language-group counts were not established.
4. Zenodo, *Human-labeled benchmarks for automated literature screening and knowledge synthesis*: https://zenodo.org/records/21853690 . Page description lists three domain-specific screening datasets with human labels; they are not on-topic for AI-literature curation.
5. ASReview SYNERGY dataset repository: https://github.com/asreview/synergy-dataset . Current README collection naming does not reconcile the local `Hall_2011.csv` export with the listed `Hall_2012` collection.

**Evidence rule:** properties described by a public landing-page summary are source-verified only to the extent stated on that page. Actual files, their current hashes, complete schemas, licence text and language distribution have not been independently inspected for candidates B, C or E in this stage. These items remain **PENDING**, not assumed true.
