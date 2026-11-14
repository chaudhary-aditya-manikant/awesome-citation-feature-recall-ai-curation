# Software Test Report — Prompt 06 working package v3.1, 31 October 2026

## Environment used

- Package-build environment: Python 3.13 runtime.
- Core dependencies are listed in `requirements.txt`. This result does not substitute for the student's latest Colab environment record.

## Automated tests

Command: `python -m pytest -q tests`  
Observed package-build output: **30 passed in 3.96s**.

Additional independent rerun during the 31 October 2026 progress checkpoint: **30 passed in 1.74s**.

Coverage includes the original validation and bootstrap tests; balanced collector query construction and mocked integration; 132 exact-year route/year cells; reproducible sampling seeds; the 2,965-record design ceiling; citation-neighbourhood sampling; conservative duplicate/title handling; audited `split_group_id` requirements; legacy-only group-field rejection; conflict handling when legacy grouping disagrees; human-screening workbook ID/label/evidence validation; deterministic 20% consistency sample generation; language-workbook sample-ID coverage; pending/invalid language evidence handling; and requiring source notes for verified-unknown language outcomes.

## Syntax check

Command: `python -m py_compile src/*.py`  
Observed: passed.

## Synthetic experiment smoke tests

The pre-existing synthetic preflight-only and end-to-end smoke tests verify software execution only. Synthetic labels, metrics and figures are not study results and must not be reported as research evidence.

## Live user execution evidence

The student supplied a Colab transcript with 18 tests passing before the `split_group_id` and workbook-import changes, and a later balanced OpenAlex collection manifest showing all 147 requests completed with no logged API errors. The latest 30-test package has **not yet been re-run in Colab**.

## What this does not establish

This test report does not verify human relevance labels, publisher-language claims, source-quality, final dataset acceptance, baseline reproduction, research metrics, significance, or novelty. No model has been fitted on the balanced candidate pool.


## 5 November 2026

`python -m pytest -q tests`: **36 passed** (adds `tests/test_ai_provisional_and_crossfit.py`: AI-provisional labels rejected by default, accepted only with flag and matching provenance; gate failure stops without exploratory flag; exploratory output stamped and primary marked not estimable when denominators are tiny; cross-fit runs and stamps outputs).
