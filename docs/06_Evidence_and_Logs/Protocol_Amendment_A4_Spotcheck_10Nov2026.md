# Protocol Amendment A4: blind spot-check of AI-only labels (10 November 2026)

**Recorded before any record in the sample was reviewed.**

## Why
In Study 1, 2,305 records judged clearly off-topic kept the AI first-pass label without author review. The paper could only say these were "unchecked". This amendment measures how often that AI label is wrong.

## Design (fixed now)
- **Sample:** simple random sample of 200 of the 2,305 records with `label_source = ai_provisional_not_reviewed`, drawn with `numpy.random.default_rng(20261110)` by `src/make_spotcheck_sample.py`. The list is committed in `data/spotcheck_20261110/spotcheck_key.csv`; a test checks that it matches the seeded draw.
- **Blinding:** the author sees title, abstract and year only. The AI label and citation counts are hidden.
- **Rule:** Annotation Rubric v2, unchanged.
- **Outcome:** agreement with the AI label; number judged relevant or uncertain; exact (Clopper-Pearson) 95% interval for the share of AI "not relevant" records that are actually relevant, scaled to the 2,305 records (`src/score_spotcheck.py`).

## What happens with the result
- If no sampled record is judged relevant, the paper reports the upper bound (at most about 1.8%, about 42 of 2,305 records at 95% confidence).
- Any sampled record the author judges relevant or uncertain is corrected in the label file (`label_source = reviewer_spotcheck_20261110`), and Study 1 is re-run. Both the original and corrected results are reported. No other labels change.

## Outcome (recorded after scoring)
- Review completed by the author (MNS2026008) on 10 November 2026, after the sample was drawn. The returned sheet showed 9 November in its date column; `results/spotcheck_20261110/spotcheck_decisions.csv` records the actual completion date.
- Agreement 190/200 (95%). Relevant 3 (1.5%, exact 95% CI 0.31–4.32%; about 35 of 2,305, CI 7–100). Uncertain 7, all with no usable abstract.
- All 3 relevant records have 0 citations and fall in the lower-citation group.
- Corrected labels: 67 relevant, 10 lower-citation; gate FAIL. Cross-fitted K = 20%: blind 9/10, aware 3/10, difference 0.60 (CI 0.33–1.00).
- Applied with `src/apply_spotcheck_corrections.py`; results in `results/spotcheck_20261110/` and `results/run_20261110_spotcheck_*`. The 5 November labels remain the main analysis.
