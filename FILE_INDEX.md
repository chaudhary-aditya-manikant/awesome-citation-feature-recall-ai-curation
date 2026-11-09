# File Index — AI Tools for Research, MNS2026008

| Component | Location | Current status |
|---|---|---|
| Research workspace/decisions | `01_Prompt01_Research_Workspace/` | Planning history; 28-record pilot is historical only |
| Research gap matrix | `02_Prompt02_Research_Gaps/` | Prepared; five gaps/verification notes |
| Literature-to-experiment map | `03_Prompt03_Literature_to_Experiment/` | Prepared; sources require normal primary-source checking |
| Feasibility | `04_Prompt04_Feasibility/` | Prepared; pilot findings historical |
| Research brief | `05_Prompt05_Research_Brief/` | Prepared |
| Active balanced collection audit | `06_Balanced_Collection_Audit_20261031/` | 2,790-record balanced collection; audit, CSVs, source ledgers and reviewer workbooks |
| Prompt 06 validation | `06_Prompt06_Dataset_and_Baseline_Validation/Prompt06_Dataset_and_Baseline_Validation_Sheet_MNS2026008.md` | Updated balanced dataset report; final acceptance gate open |
| Prompt 06 source repair | `06_Balanced_Collection_Audit_20261031/audit/TITLE_REPAIR_SOURCE_EVIDENCE_31Oct2026.md` | Six source-verified issue-level exclusions; 13 open holds |
| Blinded screening workbook | `06_Balanced_Collection_Audit_20261031/workbooks/AITR_Balanced_Human_Screening_Workbook_Blinded.xlsx` | 28 batches, 2,763 records; human labels blank |
| Blinded language workbook | `06_Balanced_Collection_Audit_20261031/workbooks/AITR_Balanced_Language_Verification_Blinded.xlsx` | 200 sample, source checks blank |
| Private admin crosswalk | `06_Balanced_Collection_Audit_20261031/workbooks/AITR_Balanced_Admin_Crosswalk_Private.xlsx` | Private mapping and source ledger; do not use during blinded screen |
| Frozen experiment blueprint | `07_Prompt07_Frozen_Experiment_Blueprint/` | Frozen; data preflight pending |
| Environment | `08_Prompt08_Environment/` | Earlier Colab setup; rerun current tests |
| Baseline/collector code | `code/` | Balanced collector, experiment runner, import validators |
| Human screen importer | `code/merge_human_screening.py` | Validates Screening_IDs/labels/metadata; creates seeded consistency sample |
| Language importer | `code/merge_language_verification.py` | Validates 200 sample ID coverage and evidence fields; does not infer language |
| Tests | `tests/` | 30 offline tests pass in package-build environment; rerun in Colab |
| Prompt 10–14 | `10_...` through `14_...` | Baseline, experiments and results still pending |
| Prompt 15–18 | `15_...` through `18_...` | Manuscript/review/repository/accountability to be finalized from actual evidence |

**Privacy:** do not upload or publish `data/private/`, private crosswalk workbooks or abstract-bearing CSVs to a public repository. The shareable data CSV omits abstracts; still review source-specific terms before release.

- `06_Prompt06_Dataset_and_Baseline_Validation/PROMPT06_PROGRESS_CHECKPOINT_31OCT2026.md` — current reconciled status and remaining gates.
- `06_Balanced_Collection_Audit_20261031/workbooks/AITR_B01_First_Human_Screening_Batch.xlsx` — standalone blinded first human-screening batch (108 records).
