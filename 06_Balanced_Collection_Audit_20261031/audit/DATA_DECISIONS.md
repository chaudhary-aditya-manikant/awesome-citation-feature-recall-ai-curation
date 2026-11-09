# Balanced-pool data decisions (31 October 2026)

1. Treat the new 2,790-row collection as the active candidate pool; retain the 30 October collection as legacy pilot only.
2. OpenAlex work IDs are unique; missing DOI is not an exclusion by itself.
3. Exclude retracted records and retraction/erratum notices from the primary candidate pool but retain them in the audit ledger. Confirm retraction status from publisher evidence before freezing.
4. F1000Research v1 (DOI ending `.1`) and v2 (DOI ending `.2`) are one work; retain v2 as canonical and exclude v1 from the primary pool. Keep version rows and their separate citation counts in the provenance ledger.
5. Similar-title records with different DOI, author and abstract are retained separately; do not deduplicate by title alone.
6. All title-missing records are held for title metadata repair, not labelled irrelevant.
7. Non-standard OpenAlex work types are flagged for scope review, not automatically excluded.
8. All human relevance labels remain blank until completed by a human using the supplied rubric.
9. `metadata_language` is an automatically detected title/abstract metadata language, not a verified full-text language. Use the 200-record sample to perform publisher/library verification.
10. The original `duplicate_cluster_id` field is not used for leakage prevention because its contents conflict with the manifest. The reviewed `split_group_id` is used instead.
