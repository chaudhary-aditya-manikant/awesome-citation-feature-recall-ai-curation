# Prompt 05 — Research Problem Brief and Success Criteria

**Student:** Aditya Chaudhary | **Enrollment:** MNS2026008 | **Course:** AI Tools for Research  
**Working title:** *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*  
**Status:** Research questions framed; after a source comparison, the data strategy is a bounded OpenAlex pool with independent labels. The final labelled dataset remains unvalidated; model training is not authorized yet.

## Problem and scope

Prior work documents citation-related ranking effects, language differences in scholarly search, popularity bias in scholarly recommenders, and fairness issues in multilingual retrieval. These are established neighboring areas; they do not establish the outcome of the proposed feature test. The proposed study tests whether adding an explicit citation-derived feature changes how a transparent ranker orders relevant records in a fixed, labelled candidate pool.

**Operational scope:** research that directly investigates computational/AI methods for scholarly-literature discovery and curation, including retrieval, citation searching, ranking, title/abstract screening, study selection and systematic-review automation. It is not a corpus of all AI applications in medicine, education or other domains. A broader AI-paper corpus would need a different set of queries and relevance labels.

## Primary research question (RQ1)

**Does adding `log1p(cited_by_count)` change pool-relative Recall@K for relevant lower-citation records?**

- **Input:** a deduplicated OpenAlex candidate pool with title/abstract representation, year, citation count, metadata language, and documented binary relevance labels.
- **Comparator A:** TF–IDF title/abstract + publication year, ranked by Logistic Regression probability, with no citation feature.
- **Condition B:** identical records, labels, split, features, model and settings, adding only `log1p(cited_by_count)`.
- **Independent variable:** citation-feature condition. **Primary dependent variable:** lower-citation Recall@K; also report overall Recall@K and Precision@K.
- **Cutoff:** fixed at top 20% of the held-out pool (`K = ceil(0.20 × N_test)`). Freeze K, split, citation-group definition and code before test evaluation; if pool size makes this cutoff unstable, document a revised cutoff before testing.
- **Success rule:** the paired difference `Recall@K(blind) − Recall@K(aware)` for lower-citation relevant papers is positive and its prespecified 95% bootstrap interval excludes zero. The citation-blind condition must not have Precision@K more than 0.05 absolute points below the citation-aware condition. Report all precision trade-offs; do not describe a recall gain as a general improvement if this guardrail fails.
- **Contrary observation:** the difference is zero/negative, its interval includes zero, precision falls materially, or subgroup counts are too sparse to estimate recall.

## Secondary questions

**RQ2 — Citation-group disparity:** Does removing the feature reduce the high-versus-low citation Recall@K gap? Use the same paired test pool and report each group’s relevant count, Recall@K and absolute gap. These subgroup estimates are descriptive in the current implementation; do not imply inferential certainty from point estimates. A smaller gap with adequate denominators is consistent with the hypothesis; an unchanged/wider gap is not; sparse groups are inconclusive.

**RQ3 — Language (conditional):** Does the feature effect differ between English and non-English records? Test only if relevant test records are sufficient in each group and language labels are checked. Report denominators and uncertainty; zero relevant records means “not estimable,” not zero recall. If positive non-English counts remain sparse, omit confirmatory language claims rather than interpreting absence of evidence as evidence of no bias.

## Hypotheses and safeguards

- **H1 (tentative):** excluding the citation feature may improve lower-citation Recall@K, potentially trading off precision.
- **H2 (conditional, two-sided):** the effect may vary by language; the current pilot does not justify a directional prediction.

The post-pilot candidate audit compared OpenAlex with Mendeley Data, CAIR-Nepal, Zenodo and SYNERGY. OpenAlex remains the best fit for the unchanged task, but only as a source for a constructed pool requiring independent labels. Mendeley has review-specific labels but is English-only and about higher-education decision support; CAIR-Nepal has citation metadata but no reported project-specific relevance labels; the Zenodo labelled benchmarks concern other scientific domains. The SYNERGY `Hall_2011.csv` export contained 340 records, four included labels and only `en` language values. The 28-record OpenAlex pilot has six preliminary positives and 22 negatives: English 4/3, Indonesian 0/7, Portuguese 1/6, Spanish 1/6. These are preliminary AI-assisted labels, not adjudicated ground truth; the balanced sample is too small and not representative. Do not train the main model on it.

Freeze queries/routes and date range; deduplicate before splitting; record the citation snapshot date; validate OpenAlex metadata language on a sample; and fit TF–IDF only on training data. Recall is relative to the constructed pool, not all relevant papers. **Current decision:** conditional go for constructing and auditing a larger OpenAlex pool; no-go for the main model on the 28-record pilot. The language analysis remains conditional on passing the frozen positive-count and language-validation gates. Novelty remains unknown pending a focused comparison with the closest work.

## Selected related work

1. Beel & Gipp (2009), *Google Scholar’s Ranking Algorithm: The Impact of Citation Counts.* https://doi.org/10.1109/RCIS.2009.5089308
2. Rovira, Codina & Lopezosa (2021), *Language Bias in the Google Scholar Ranking Algorithm.* https://doi.org/10.3390/fi13020031
3. Färber, Coutinho & Yuan (2023), *Biases in scholarly recommender systems: impact, prevalence, and mitigation.* https://doi.org/10.1007/s11192-023-04636-2
4. Yang, Jiang & Baldwin (2024), *Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods.* https://doi.org/10.18653/v1/2024.mrl-1.23
