# One-page research brief (Gate G1, brief §11 template)

**Aditya Chaudhary (MNS2026008)** · *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*

| Field | Project information |
|---|---|
| **Review topic and key papers** | Review: *Recall Bias Toward Highly-Cited and English-Language Papers in AI Literature Curation: A Survey of Mechanisms, Current Approaches, and Research Gaps* (Lab 1). Key verified sources: Beel & Gipp 2009 (Google Scholar weights citation counts in ranking); van de Schoot et al. 2021 (ASReview); Przybyła et al. 2018 (RobotAnalyst); Callaghan & Müller-Hansen 2020 (stopping criteria); Färber et al. 2023 (bias in scholarly recommenders). |
| **Research gap** | The screening and citation-searching evaluations compared in the review report recall for the whole collection only, never split by citation band or language (review §§ on current approaches and gaps). VERIFIED for the cited studies; field-wide absence INFERRED. |
| **Research question** | Primary: does adding a log(1 + citations) feature to a transparent relevance ranker lower Recall@20% for relevant, rarely cited papers? Supporting: does it change the higher/lower-citation recall gap? Language effect: conditional on verified languages (not met). |
| **Study pathway** | C, targeted modification: two otherwise identical rankers differ only in the citation feature. |
| **Dataset or measurement setup** | Study 2: SYNERGY v1.0 (CC0), 20 systematic reviews, 150,154 records, 2,745 human inclusions; grouped 5-fold within each review. Study 1: OpenAlex (CC0), snapshot 30 Oct 2026; quota-stratified pool of 2,790 records (2,754 eligible; 64 relevant). Grouped 5-fold `StratifiedGroupKFold` on `split_group_id`, seed 20261030. |
| **Baseline/comparators** | Baseline: TF-IDF (title + abstract) + year → Logistic Regression (scikit-learn, open source). Condition: baseline + citation feature. Post-hoc references: citation-only ranker; fair re-rank. |
| **Primary metric and control** | Lower-citation Recall@20% (age-adjusted citation rate ≤ pool median); paired cluster bootstrap (2,000 replicates, seed 20261031). Held constant: records, labels, folds, features other than citations, model settings. |
| **Computing and risks** | CPU only; whole analysis < 1 min. Risks: too few rarely cited relevant records (gate ≥ 20, **failed**: 7), collection confound (46/64 relevant via citation routes), AI first-pass labels on 2,305 unreviewed off-topic records. Fallback: report as exploratory (Amendment A3). |
| **First executable milestone** | Collector + metadata audit run in Colab (31 Oct 2026); baseline validated (`baseline_validation.md`). |

**Outcome, Study 1 (pilot):** exploratory. The citation-blind ranker retrieved 7/7 rarely cited relevant papers and the citation-aware ranker 3/7 (Δ = 0.57, 95% CI 0.14–1.00).

**Outcome, Study 2 (confirmatory, SYNERGY, 20 reviews):** gate passed (977 / 1,768 relevant records per citation group). Citation-blind 742/977 vs citation-aware 691/977 (Δ = 0.052, 95% CI 0.033–0.068); overall recall unchanged. H1 and H2 supported.
