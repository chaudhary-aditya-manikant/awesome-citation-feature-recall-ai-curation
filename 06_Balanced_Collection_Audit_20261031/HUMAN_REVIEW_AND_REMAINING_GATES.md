# Human review and remaining evidence workflow — 31 October 2026

## What is already automated and checked

- New OpenAlex candidate pool: 2,790 unique Work IDs; abstracts present for all records.
- All 132 search/topic route-year requests, five seed resolution requests and ten citation-neighbourhood requests are recorded as executed; no API errors were logged.
- Year counts span 2015–2025 and range from 247 to 262.
- Candidate pool has a 2,763-record blinded title/abstract screening queue, a 13-record unresolved title-metadata hold after six of the original 19 missing-title records were source-verified as issue-level paratext and excluded from article screening; eight administrative-exclusion candidates.
- Duplicate/version and administrative source decisions are recorded separately. Seven of eight administrative candidate decisions have publisher or authoritative bibliographic corroboration in the current source audit; the `Movie genres and beyond` OpenAlex retraction flag remains pending publisher confirmation.
- A 200-record publication-language verification sample has been drawn (100 OpenAlex-English, 99 known non-English, 1 unknown). The verifier workbook intentionally hides the OpenAlex language metadata.
- Three workbooks are supplied: blinded human screening, blinded publication-language verification, and a separate private admin crosswalk.

## Human tasks that must not be fabricated

### A. Relevance screening (2,763 records)

Use `workbooks/AITR_Balanced_Human_Screening_Workbook_Blinded.xlsx`. Complete `Batch_B01` first. Values in `Human_Relevance_Label`:

- `1`: directly studies/develops/evaluates a computational/AI method for scholarly-literature discovery or curation.
- `0`: does not meet that target construct.
- `uncertain`: title/abstract evidence is insufficient or ambiguous.

Write a rationale and confidence for every decided item. Do not use citation counts, metadata language, author prestige, venue or country as evidence. Do not convert uncertain to 0.

Once B01 is returned, merge decisions by `Screening_ID`, audit consistency and proceed batch-wise. No assistant-generated suggestion may be recorded as a human gold label.

### B. Publication-language verification (200 records)

Use `workbooks/AITR_Balanced_Language_Verification_Blinded.xlsx`. For each sample row, verify the actual publication language from a publisher article page/PDF or a library/institutional record; record exact source URL, evidence type, verifier and date. The OpenAlex language value is hidden to reduce confirmation bias. Compare against the private `Language_Key` only after verification.

### C. Title metadata repair and issue-level paratext (19 original records)

Use the private admin workbook `Title_Repair_19` and `audit/title_metadata_repair_hold_19.csv`. Six records have now been verified from publisher issue pages as whole-issue/issue-level paratext and are excluded from the article-level pool with evidence in `audit/TITLE_REPAIR_SOURCE_EVIDENCE_31Oct2026.md`. Thirteen still have unresolved title metadata and are not in the 2,763 screening queue. Recover titles only from an identifiable publisher/library source; do not guess from the abstract. If not recoverable, document an administrative exclusion, never a relevance label of 0.

### D. Administrative exclusion candidates (8 records)

See `audit/administrative_exclusion_source_audit_31Oct2026.csv`. Seven have source-based decisions; one retraction flag still needs publisher confirmation. Keep all eight in an audit ledger regardless of primary-pool exclusion.

## Gate after human review

After the human labels and eligibility decisions are returned:

1. Resolve every `uncertain` item by a documented adjudication or leave it excluded from confirmatory training/testing as unresolved.
2. Reconcile the blinded workbook with the private master crosswalk using `Screening_ID`.
3. Remove only documented administrative exclusions and unresolved title metadata holds from the primary candidate pool.
4. Assign group-aware train/validation/test partitions using `split_group_id`; do not split duplicate/version groups.
5. Fit TF–IDF and numeric scaling on training data only.
6. Run preflight and verify the locked test set contains at least 20 relevant lower-citation and 20 relevant higher-citation records. Check language subgroup size separately; do not promise confirmatory language results unless the minimum is met.
7. Preserve the 2026-10-30 citation snapshot and the predeclared split; never redraw to meet a threshold or improve scores.

## Honest gate status

The collection and automated metadata-audit work are complete. Six missing-title issue-level records have source-backed administrative exclusions; 13 missing-title records remain unresolved. Prompt 06 final dataset validation is **not yet signed off** because human relevance labels, 200 source-verified language records and the remaining administrative source check require reviewer/source evidence. No model training or performance results are claimed.
