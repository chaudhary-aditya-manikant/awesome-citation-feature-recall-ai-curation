# AITR Balanced Collection — audit outputs

This bundle audits the new OpenAlex collection uploaded on 31 October 2026. It is not the 30 October 3,000-row legacy pool.

## Main outputs

- `data/private/candidate_pool_audited_private.csv` — all 2,790 records with abstract and corrected audit fields.
- `data/shareable/candidate_pool_audited_shareable.csv` — same metadata without abstracts.
- `data/private/candidate_pool_human_screening_queue_private.csv` — 2,763 records queued for blinded human title/abstract screening; labels are blank.
- `audit/title_metadata_repair_hold_19.csv` — 19 records with missing title.
- `audit/administrative_exclusion_candidates.csv` — 8 records held out for source-backed administrative reasons.
- `audit/duplicate_version_relationship_ledger.csv` — source-based version, title-collision and erratum relationships.
- `audit/language_verification_sample_200.csv` — stratified sample for publisher/library language verification.
- `workbooks/AITR_Balanced_Human_Screening_Workbook_Blinded.xlsx` — reviewer workbook without citation counts or metadata-language column.
- `workbooks/AITR_Balanced_Metadata_Admin_Crosswalk.xlsx` — separate admin key with citations/language/provenance.

## Crucial integrity rule

No human relevance labels have been generated. The annotation fields must be completed by a human reviewer under the project's Relevance Annotation Rubric v2. AI suggestions, if later added, must be stored separately from human gold labels.

## Next action

Open the blinded human-screening workbook and complete the first batch (B01) using the rubric. Keep the metadata admin crosswalk closed during relevance decisions to avoid citation/language priming. The 200-record language sample requires separate publisher/library evidence entry.

Read `audit/BALANCED_COLLECTION_AUDIT_REPORT_31Oct2026.md` for the complete audit, data gates and source links.

## Reviewer workbooks (created and validated)

- `workbooks/AITR_Balanced_Human_Screening_Workbook_Blinded.xlsx` — 28 batch sheets for 2,763 records; title/abstract only; citation counts, DOI, author IDs, retrieval route and OpenAlex language are omitted. Decision cells are blank.
- `workbooks/AITR_Balanced_Language_Verification_Blinded.xlsx` — 200-record sample; actual publication-language field and source-evidence fields are blank; OpenAlex metadata language is hidden.
- `workbooks/AITR_Balanced_Admin_Crosswalk_Private.xlsx` — private mapping and analysis metadata, including citation counts and metadata-language values. Do not open during blinded relevance screening. Includes title-repair and publisher-source audit sheets.

See `HUMAN_REVIEW_AND_REMAINING_GATES.md` for exact remaining human actions and the final data gate.
