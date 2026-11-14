# Prompt 10 — Baseline Validation (final, 5 November 2026)

| Check | Result |
|---|---|
| Both conditions fit/score on frozen split | Yes (`results/run_20261105_reviewed_frozen`) |
| Leakage check (`split_group_id`) | Passed |
| All partitions contain both classes | Yes (38 / 13 / 13 relevant) |
| Dataset gate | FAIL (1 lower, 12 higher relevant in test) |
| Citation-blind baseline, frozen test fold | Recall@20% 13/13, Precision@20% 0.117 |
| Citation-aware, frozen test fold | Recall@20% 10/13, Precision@20% 0.090 |
| Cross-fitted baseline | Recall@20% 63/64 (0.984), Precision@20% 0.114 |

The citation-blind ranker is near the recall ceiling at 20%, so condition differences appear in the tail.
