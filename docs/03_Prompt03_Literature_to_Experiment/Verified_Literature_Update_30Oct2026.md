# Literature-to-Experiment Update — 30 October 2026

**Scope:** targeted verification of closely related work, not a systematic review. Searches covered citation-count effects in scholarly search, scholarly recommender-system bias, language fairness in multilingual IR, and machine-learning support for systematic-review screening.

## What the literature already establishes

1. **Citation counts can affect scholarly search ranking.** Beel and Gipp's empirical study analysed 1,364,757 articles and reported that citation counts were a highly weighted factor in Google Scholar ranking, while also noting query-dependent exceptions. This concerns Google Scholar's ranking at the time of their study; it does not establish how OpenAlex or current commercial systems rank results. [1]
2. **Scholarly recommender systems have multiple bias sources.** Färber, Coutinho and Yuan review human-caused and system-caused biases, including popularity bias, and propose a framework for detecting and mitigating them. This substantially overlaps with any broad claim that popularity bias in scholarly recommendation is unexplored. [2]
3. **Language fairness in multilingual retrieval is an established research area.** Yang, Jiang and Baldwin evaluate traditional and neural multilingual retrieval and propose a mitigation loss; their setup is not identical to scholarly-literature curation, but it means a general “language bias in retrieval is unexplored” claim is untenable. [3]
4. **Language effects have been examined in Google Scholar.** Rovira, Codina and Lopezosa study language bias in Google Scholar's ranking. Their findings should not be generalized to every scholarly database or to the OpenAlex API. [4]
5. **Screening automation is evaluated with recall as a central safety measure.** The 2022 systematic review/meta-analysis reports different recall/precision trade-offs depending on the operating point and argues that high recall should be prioritized. [5]
6. **Recent evidence reviews broaden the automation landscape.** The 2025 AHRQ rapid-review update included 95 studies. It reports variable performance across tasks, promising but variable screening results, and inconsistent fully automated LLM screening. Importantly for this project, its search/screening process excluded non-English studies, so it cannot establish multilingual coverage or language fairness. [6]
7. **Stopping rules remain a methodological issue.** Callaghan and Müller-Hansen (2020), and the 2024 discussion of robust stopping criteria, emphasize that recall is not directly known during live screening and that stopping claims require uncertainty-aware evidence. These are related to screening safety but do not test citation-feature ablation. [7,8]

## Consequence for this project

The project must not claim that citation/popularity bias, language bias, or recall-aware screening is a new topic. The most defensible course-scale question is narrower: **in a fixed, explicitly constructed candidate pool of papers about AI/computational scholarly-literature curation, what is the paired change in lower-citation pool-relative Recall@K when the same transparent Logistic Regression ranker is given an explicit citation-count feature?**

Language is retained as a conditional descriptive dimension only if the pool has adequate positive examples and metadata-language labels are independently audited. The current 28-record pilot fails this requirement (zero Indonesian positives and only one positive in each of Portuguese and Spanish). It cannot support a confirmatory language result.

## Research gap statement (carefully bounded)

The targeted search identified established work on citation-sensitive scholarly search, popularity bias in scholarly recommenders, language bias in academic search, multilingual retrieval fairness, and recall-oriented systematic-review screening. The remaining candidate gap is not a general absence of these topics. It is the **specific, controlled measurement of the incremental effect of an explicit citation-count feature on lower-citation relevant-record recall in a defined AI-literature-curation candidate pool**, using a matched text/year baseline and transparent pool-relative metrics. This gap is **candidate / not yet demonstrated novel** until a fuller search identifies and compares any directly equivalent feature-ablation studies.

## Verified references

[1] Beel, J., & Gipp, B. (2009). Google Scholar's Ranking Algorithm: The Impact of Citation Counts (An Empirical Study). *Proceedings of the 3rd IEEE International Conference on Research Challenges in Information Science*, 439–446. https://doi.org/10.1109/RCIS.2009.5089308

[2] Färber, M., Coutinho, M., & Yuan, S. (2023). Biases in scholarly recommender systems: impact, prevalence, and mitigation. *Scientometrics, 128*, 2703–2736. https://doi.org/10.1007/s11192-023-04636-2

[3] Yang, J., Jiang, F., & Baldwin, T. (2024). Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods. *Proceedings of the Fourth Workshop on Multilingual Representation Learning*, 280–292. https://doi.org/10.18653/v1/2024.mrl-1.23

[4] Rovira, C., Codina, L., & Lopezosa, C. (2021). Language Bias in the Google Scholar Ranking Algorithm. *Future Internet, 13*(2), 31. https://doi.org/10.3390/fi13020031

[5] Feng, Y., et al. (2022). Automated medical literature screening using artificial intelligence: a systematic review and meta-analysis. *Journal of the American Medical Informatics Association, 29*(8), 1425–1432. https://doi.org/10.1093/jamia/ocac066

[6] Adam, G. P., Davies, M., George, J., Caputo, E., Htun, J. M., Coppola, E. L., Holmer, H., Kuhn, E., Kooistra, O., Wethington, H., Ivlev, I., Balk, E. M., & Trikalinos, T. A. (2025). *Machine Learning Tools To (Semi-)Automate Evidence Synthesis: A Rapid Review and Evidence Map, 2025 Review Update*. AHRQ Publication No. 25-EHC038. https://doi.org/10.23970/AHRQEPCWHITEPAPERMACHINE2

[7] Callaghan, M. W., & Müller-Hansen, F. (2020). Statistical stopping criteria for automated screening in systematic reviews. *Systematic Reviews, 9*, 273. https://doi.org/10.1186/s13643-020-01521-4

[8] (2024). Computer-assisted screening in systematic evidence synthesis requires robust and well-evaluated stopping criteria. *Systematic Reviews*. https://doi.org/10.1186/s13643-024-02699-7

[9] Sandner, E., Gütl, C., Jakovljevic, I., & Wagner, A. (2024). Screening Automation in Systematic Reviews: Analysis of Tools and Their Machine Learning Capabilities. *Studies in Health Technology and Informatics, 313*, 179–185. https://doi.org/10.3233/SHTI240034

## Verification notes

- DOI/title/author/year metadata for [1]–[5], [7], and [9] were checked against publisher, author, PubMed, or ACL pages during this update.
- [6] is a government evidence-review update page, not a journal article; cite it as a report/web resource.
- [8] Publisher metadata verified: Callaghan et al. (2024), *Systematic Reviews*, 13, article 284, published 22 November 2024. Cite as Callaghan et al. because the author list is extensive.
- This search was targeted and selective. It does not support a PRISMA-style claim of exhaustive coverage.
