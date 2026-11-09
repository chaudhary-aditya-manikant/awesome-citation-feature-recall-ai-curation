# Prompt 17 — Reproducibility and Repository Checklist (updated 5 November 2026)

| Item | Status |
|---|---|
| Code: collection, audit, experiment runner, cross-fit, figures, merge/validation tools | Present in `code/` |
| Tests | 36 passing (`tests/`) |
| Protocol and amendments | Prompt07 blueprint; Amendments A2, A3 (`06_Evidence_and_Logs/`) |
| Data — shareable | `06_Balanced_Collection_Audit_20261031/audit/candidate_pool_shareable.csv` (no abstracts); `data/ai_provisional_20261105/` labels + rationales |
| Data — private (do not publish) | `06_Balanced_Collection_Audit_20261031/data/private/` (abstracts), admin crosswalk workbook |
| Results | `results/run_20261105_*` with run summaries, split manifests, predictions, metrics, figures |
| One-command re-run | `bash code/run_all_provisional.sh <input> <tag> [ai]` |
| Manuscript | `15_Prompt15_Manuscript/latex/` (source + PDF) |
| Environment record | `08_Prompt08_Environment/`, `requirements*.txt`, per-run `environment.txt` |
| Licence | OpenAlex metadata CC0; add a code licence (e.g., MIT) before publishing |
| GitHub | Not pushed from this session (no valid token). Exclude `data/private/` and private workbooks when pushing. |
