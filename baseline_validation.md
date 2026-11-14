# Baseline Validation

Baseline: TF-IDF (title + abstract, 1–2-grams, min_df 2, sublinear tf) + standardised year → Logistic Regression (C = 1, balanced, liblinear, seed 20261030). Settings: `configs/frozen_protocol.json`. Code: `src/run_experiment.py`. Detailed reports: `docs/06_Prompt06_Dataset_and_Baseline_Validation/`, `docs/10_Prompt10_Baseline_Validation/`.

## What was checked
| Check | Result | Evidence |
|---|---|---|
| Data schema, required columns, label values, years, citation counts | Pass | `load_and_validate` in `src/run_experiment.py`; `tests/test_validation.py` |
| No `split_group_id` crosses train / validation / test | Pass | leakage assertion in both runners; `results/run_20261105_reviewed_frozen/split_manifest.csv` |
| Every partition contains both classes | Pass (38 / 13 / 13 relevant) | `results/run_20261105_reviewed_preflight/preflight_gate_report.json` |
| Scaling and TF-IDF fitted on training data only | Pass | pipeline design; tests |
| Deterministic results with fixed seeds | Pass | re-runs reproduce identical metric files |
| Settings in config match code defaults | Pass | `tests/test_config_matches_code.py` |
| Full test suite | 58 passed | `python -m pytest -q tests` |

## Measured baseline behaviour
| Setting | Citation-blind baseline | Source |
|---|---|---|
| Frozen test fold (551 records, K = 111) | Recall@20% 13/13 = 1.000; Precision@20% 0.117 | `results/run_20261105_reviewed_frozen/primary_metrics.csv` |
| Cross-fitted, all 5 folds | Recall@20% 63/64 = 0.984; Precision@20% 0.114 | `results/run_20261105_reviewed_crossfit/crossfit_pooled_metrics.csv` |
| Run time | ~1 s fit, ~0.2 s scoring per fold (CPU) | `results/run_20261105_reviewed_frozen/resource_metrics.csv` |

## Deviations and limits (honest record)
- **Not a reproduction of a published system's reported numbers.** No published study reports results on this pool; validation therefore checks correctness and behaviour (sanity, leakage, determinism), not agreement with a reported score.
- **Ceiling effect.** The baseline separates curation papers from the largely off-topic pool easily (≈ 98% recall at 20%), so differences between conditions appear in the tail.
- **Dataset gate failed** (too few relevant lower-citation records), so the comparison is exploratory — see `docs/06_Evidence_and_Logs/Prompt07_Protocol_Amendment_A3_05Nov2026.md`.

## Study 2 (SYNERGY): same baseline, checked again
| Check | Result | Evidence |
|---|---|---|
| Same model and settings as Study 1 | Pass | `run_study2.py` imports `make_pipeline` from `run_experiment.py`; `configs/study2_protocol.json` |
| No title group crosses folds within a review | Pass | assertion in `score_dataset` |
| Protocol frozen before data; script refuses undecided values | Pass | `PREREGISTRATION_v2.md`; `tests/test_study2.py` |
| Deterministic on synthetic data; edge case with no lower-citation relevant records | Pass | `tests/test_study2.py` |
| Pooled counts rebuilt from the committed out-of-fold scores (150,154 records) | Identical | `python src/study2_verify_from_scores.py …` |
| Per-review table sums to the pooled table | Pass | `tests/test_study2.py::test_committed_study2_tables_are_consistent` |

Measured baseline (citation-blind) on SYNERGY, 20 reviews: Recall@20% 2166/2745 = 0.789; Precision@20% 0.072 (`results/study2_confirmatory/study2_pooled_metrics.csv`). No ceiling effect here, unlike Study 1. As in Study 1, this validates correctness and behaviour, not agreement with a published score: SYNERGY's own papers report active-learning simulations under a different protocol.
