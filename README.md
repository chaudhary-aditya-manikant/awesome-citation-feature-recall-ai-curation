# Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation

AI Tools for Research — Lab 2 · Aditya Chaudhary (MNS2026008), IIIT Allahabad · final, 5 November 2026

**Project:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation
**Status:** Complete. Experiments run on the final labels; the pre-registered dataset gate failed, so all results are reported as **exploratory** (as the frozen protocol requires).

## Contents
- Paper: `15_Prompt15_Manuscript/latex/Chaudhary_MNS2026008_Empirical_Paper.pdf` (source `main.tex`)
- Final results: `results/run_20261105_reviewed_preflight`, `..._frozen`, `..._crossfit` (figures in `..._crossfit/figures`)
- Final labels: `data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv` (`label_source` = reviewer or AI first pass)
- Reviewed screening sheet: kept privately because it contains abstracts; the decisions it holds are in `data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv`
- Protocol: Prompt 07 blueprint; Amendments A2, A3 (`06_Evidence_and_Logs/`)
- Colab: `MNS2026008_Colab_Rerun.ipynb`; one-command re-run: `bash code/run_all_provisional.sh <input> <tag> ai`

## Label provenance
1. AI first pass (Claude, Anthropic) on all 2,763 records under Rubric v2, with rationales and confidence; 20% self-consistency audit 549/550.
2. Author (MNS2026008) reviewed 458 records (all AI-relevant/uncertain, 53 borderline, 333 negatives with curation terms); agreement 443/458, κ = 0.88; 15 decisions changed.
3. The other 2,305 clearly off-topic records keep the AI label (`ai_provisional`). Outputs are stamped `MIXED_LABELS_REVIEWER_AND_AI_PROVISIONAL`.

## Key results (exploratory, cross-fitted, K = 20%)
64/2,754 relevant; 7 in the lower-citation half. Lower-citation recall: citation-blind 7/7, citation-aware 3/7 (difference 0.57, 95% CI 0.14–1.00). Overall recall 0.984 vs 0.891.

## Data in this repository

- **Included:** OpenAlex metadata without abstracts (`06_Balanced_Collection_Audit_20261031/audit/candidate_pool_shareable.csv`, `data/shareable/`), the collection manifest and query log, final screening labels with their source and rationale (`data/ai_provisional_20261105/`), and all result files.
- **Not included:** abstract text, the screening workbooks (which contain abstracts) and administrative keys. They are needed only to retrain the models. To regenerate them, re-run the collector (`code/collect_openalex_candidates_balanced.py`) with the parameters in `collection_manifest.json`, then join the labels on `openalex_id`. OpenAlex samples may differ slightly from the 30 October 2026 snapshot.

## Licence

Code: MIT (see `LICENSE`). OpenAlex metadata: CC0. Paper text and figures: © the author.

## Citation

Chaudhary, A. (2026). *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*. AI Tools for Research, IIIT Allahabad.
