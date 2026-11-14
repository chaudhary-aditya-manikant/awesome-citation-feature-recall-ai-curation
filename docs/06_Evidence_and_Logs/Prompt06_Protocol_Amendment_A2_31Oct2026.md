# Prompt 06 / Prompt 07 Protocol Amendment A2 — 31 October 2026

**Project:** MNS2026008 — Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation  
**Amendment scope:** Candidate retrieval only.  
**Timing:** Before any model fitting or inspection of model test metrics.  
**Reason:** The 30 October collector reached the 3,000-record cap after only 29 of 60 planned search/topic tasks and produced a strongly uneven publication-year distribution because it selected sorted top-page results in broad year bands.

## Change

Replace the legacy collector for the final candidate pool with `src/collect_openalex_candidates_balanced.py`. It runs 8 text-search routes × 11 exact publication years (88 cells) and 4 topic routes × 11 exact years (44 cells), 20 seeded random records per cell. It then resolves five seed DOIs (up to five records per DOI request) and, for each exact seed match, samples up to 30 incoming citers and 30 outgoing references. Base seed: `20261031`; route-specific seeds are derived deterministically using SHA-256. No publication-date or citation-count sort is used, and every planned route/year is attempted even when the pool is below/above a provisional target count.

With five seeds resolved, the maximum output before overlap/deduplication is 2,965 (132×20 + 10×30 + 5×5), below the frozen 3,000-record cap. If fewer seeds resolve, the actual maximum is lower. The sampling frame is a quota-stratified multi-route pool, not a probability sample of all scholarly publications. Report all executed/failed/zero-result routes and actual counts.

## Preserved design elements

- Research question and frozen target scope/rubric v2.
- OpenAlex as primary metadata source.
- Citation-blind TF–IDF + publication-year Logistic Regression versus identical citation-aware condition with standardized `log1p(cited_by_count)`.
- Citation-rate grouping, lower-citation Recall@K primary metric, grouped split, bootstrap procedure and all minimum dataset gates.
- No model results have been inspected; no outcome-dependent change is authorised by this amendment.

## Status

This amendment changes acquisition sampling only. It does not grant dataset acceptance. The new collector has 8 dedicated offline tests and passes within the package suite (18 tests total). A successful live API run, human eligibility/relevance decisions, publisher/language verification and Prompt 07 data-gate PASS remain necessary before model fitting.


## Duplicate-source clarification — 31 October 2026

The legacy-pool duplicate audit also resolved the Natural Language Generation DOI pair. The official Inderscience page (https://www.inderscience.com/info/inarticle.php?artid=128292) confirms DOI `10.1504/IJIIDS.2023.128292` for the exact title, authors and 2023 journal issue. OpenAlex W4319992562 is retained as canonical; W4316115912 is excluded as duplicate/conflicting DOI metadata. DBLP lists `10.1504/IJIIDS.2023.10053426`; this secondary-source discrepancy is preserved in `data/legacy_pilot_20261030/publisher_doi_resolution.csv`.
