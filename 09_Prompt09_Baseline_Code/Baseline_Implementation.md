# Prompt 09 — Baseline and Data-Acquisition Implementation

## Research ranking pipeline

The runnable implementation is `code/run_experiment.py`. It implements a controlled feature ablation using the same train/test records, text representation, publication-year feature, Logistic Regression estimator, regularization and seed in both conditions.

- **Condition A (citation-blind):** TF–IDF title/abstract + publication year.
- **Condition B (citation-aware):** identical features + `log1p(citations)`.
- Both conditions rank the same held-out test records by predicted positive-class probability.
- Primary metric: lower-citation pool-relative Recall@K, with `K = ceil(0.20 × N_test)`.
- Guardrails: overall Recall@K and Precision@K; secondary measures include higher-citation Recall@K, citation-group recall gap, descriptive metadata-language recall, 10%/30% K sensitivity, disagreement/error review and resource timings.
- The grouped split is fixed: 5-fold `StratifiedGroupKFold`, fold 0=test, fold 1=validation, folds 2–4=train. A duplicate/version cluster cannot cross partitions.
- Bootstrap comparison is paired and resamples whole `split_group_id` clusters, using the same sampled clusters for both conditions.

The script fails closed when the data are too small, labels are not explicitly marked adjudicated, IDs/clusters/fields are invalid, or test citation-group positive denominators do not meet the fixed gate. A `--preflight-only` mode creates a gate report and split manifest without training. An ordinary run records the data provenance declaration and SHA-256 input hash, but the code cannot authenticate a person's annotation or licence declaration.

## Candidate data acquisition

`code/collect_openalex_candidates.py` is a separate, bounded OpenAlex collection tool. It covers eight search phrases, four topic routes, five publication-year bands, seed DOI resolution and one-hop citation neighbourhoods. It writes private abstract-bearing data separately from an abstract-free metadata copy, together with raw response records, query URLs/parameters, timestamps, route errors and a collection manifest. It creates no relevance labels. The human reviewer must adjudicate all labels and duplicate/version clusters.

## Important validation boundary

The code and collector have been syntax-checked; the test suite passes; preflight and full model smoke tests have been completed only on synthetic fixtures. No accepted research dataset has been supplied. **Prompt 10 research-baseline validation remains pending.**
