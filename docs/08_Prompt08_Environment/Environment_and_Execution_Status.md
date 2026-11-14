# Prompt 08 — Environment and Execution Status (updated 5 November 2026)

## Environment used for the 5 November analysis runs

| Component | Version |
|---|---|
| Python | 3.13.18 |
| NumPy | 2.5.3 |
| pandas | 3.0.5 |
| scikit-learn | 1.9.1 |
| matplotlib | 3.11.2 |
| Platform | Linux x86_64, glibc 2.39 (cloud container used by the AI assistant) |

Each run writes its own `environment.txt`/`run_summary.json` with these values.

## Executed

- `python -m pytest -q tests`: **36 passed** (30 earlier tests + 6 tests for Amendment A3 behaviour).
- `python -m py_compile src/*.py`: passed.
- Preflight gate, frozen exploratory run and cross-fitted exploratory run on the AI-provisional dataset (see `docs/13_Prompt13_Experiments`).

## Still to do by the student

- Re-run `python -m pytest -q tests` and `bash scripts/run_all.sh ...` in your own Colab/desktop environment and save the output. The container versions above are not a claim about your environment.
- The OpenAlex API was not reachable from the analysis container; the collection itself was run earlier by the student in Colab.
