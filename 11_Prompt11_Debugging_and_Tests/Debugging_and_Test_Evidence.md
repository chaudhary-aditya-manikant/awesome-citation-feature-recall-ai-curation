# Prompt 11 — Debugging and Test Evidence

**Current software verification: 30 tests passed in the package-build environment (31 October 2026); the newest suite still needs a Colab rerun.** Full console/test detail is in `tests/SOFTWARE_TEST_REPORT.md`.

## Code-review corrections made before any main experiment

1. **Bootstrap unit:** replaced record-wise resampling with paired resampling of complete `duplicate_cluster_id` clusters. This is more coherent with the grouped data split and keeps both feature conditions paired within each resample.
2. **Synthetic provenance:** a synthetic input run is now marked `SOFTWARE_SMOKE_TEST_ONLY`. Other run statuses explicitly say input provenance is a declaration, not independently authenticated.
3. **Model seed:** the configured split seed is passed to Logistic Regression rather than using a hard-coded seed.
4. **Safe outputs:** the experiment script refuses to overwrite a non-empty result directory.
5. **Input safety:** rejects fractional/non-integer citation counts, normalizes missing/blank language metadata to `unknown`, and continues to fail closed on preliminary labels and the 28-row pilot.
6. **Preflight gate:** added `--preflight-only`, which writes gate checks, split manifest and a group profile without fitting a model. A code insertion self-reference was caught during inspection and corrected before the successful preflight test.
7. **Data collector:** added offline-tested OpenAlex parsing, DOI/title normalization, conservative duplicate clustering and deterministic task-construction helpers.

## Tests executed

- Three original validation tests: 28-row pilot rejection, preliminary-label rejection, duplicate OpenAlex ID rejection.
- One citation-count integrity test.
- One paired cluster-bootstrap test.
- Four collector helper tests.
- `python -m py_compile` passed for both scripts.
- Preflight-only and full end-to-end paths were executed against generated synthetic data; both completed. The preflight did not fit models. The end-to-end outputs were tagged synthetic and kept outside the project archive.

These tests do not constitute annotation quality assurance, source verification, baseline reproduction on real data, or evidence of a research effect. No main research-data run has been performed.


4. **Audited split-group mismatch (31 Oct 2026):** the balanced audit states that raw OpenAlex `duplicate_cluster_id` is internally inconsistent and must not be used for leakage prevention. The experiment runner originally required and grouped on that raw field. Corrected the runner and input schema to require audited `split_group_id` for stratified grouped splitting, leakage checks, split manifests and paired cluster bootstrap. Added two regression tests (legacy-only column rejected; conflicting legacy column ignored). Verification: 20 tests passed at the time of the split-key correction and `py_compile` passed. No research labels or empirical metrics were created.


5. **Human-screening import guard:** added `merge_human_screening.py` to check exact Screening_ID coverage, allowed labels, rationale/confidence/reviewer/date completeness and deterministic re-screen selection. It does not promote AI suggestions or create human labels.
6. **Publication-language import guard:** added `merge_language_verification.py` to validate exact Language_Sample_ID coverage, evidence type/URL, verifier/date and notes for unknown outcomes. It expressly cannot prove that a source URL supports the claimed language; that remains a human source-quality check.
7. **Type-scope reviewer context:** added OpenAlex record type and nonstandard-type review flag to all 28 blinded screening batches, with an instruction that type alone cannot justify exclusion. Citation counts and metadata language remain hidden.
8. **Title metadata source audit:** six of 19 missing-title records were verified as issue-level paratext and excluded from article screening; 13 remain held. The one unsupported retraction flag remains pending.

Latest verification: `python -m pytest -q tests` → **30 passed**; `python -m py_compile code/*.py` → passed. These are package-build software checks, not research-data tests. The latest Colab rerun has not yet been supplied.


## 5 November 2026

- Bug class found on real data: with one relevant lower-citation test record the paired bootstrap returned a degenerate [1,1] interval and the success rule fired. Fixed by an estimability guard (min. 10 records), disclosed in Amendment A3 addendum; covered by a test.
- Figure label overlap in the rank-shift plot fixed by label spreading.
- Suite: 36 passed.
