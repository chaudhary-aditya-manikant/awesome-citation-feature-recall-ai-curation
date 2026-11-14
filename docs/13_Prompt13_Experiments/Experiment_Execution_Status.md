# Prompt 13 — Experiment Execution Status (final, 5 November 2026)

Final runs on author-reviewed labels (`model_input_reviewed_20261105_private.csv`, 2,754 decided, 64 relevant; status `MIXED_LABELS_REVIEWER_AND_AI_PROVISIONAL`):

| Run | Folder | Result |
|---|---|---|
| Preflight | `results/run_20261105_reviewed_preflight` | gate FAIL (test: 1 lower, 12 higher relevant) |
| Frozen single split | `results/run_20261105_reviewed_frozen` | exploratory; primary not estimable; overall recall A 13/13, B 10/13 |
| Cross-fitted (A3) | `results/run_20261105_reviewed_crossfit` | lower-citation recall 7/7 vs 3/7; Δ = 0.571 (95% CI 0.143–1.000); overall 0.984 vs 0.891 |

Earlier AI-only runs are kept in `results/superseded_ai_only_labels/`.
