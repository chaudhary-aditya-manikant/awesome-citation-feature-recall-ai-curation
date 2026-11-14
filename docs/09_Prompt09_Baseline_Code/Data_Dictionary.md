# Input Data Dictionary

The experiment script expects one row per deduplicated work and these columns:

| Column | Meaning | Rules |
|---|---|---|
| `openalex_id` | Stable OpenAlex work ID | Non-empty and unique |
| `title` | Work title | Non-empty |
| `abstract` | Abstract text | Empty allowed by script, but annotate/justify missingness; keep private if terms restrict redistribution |
| `year` | Publication year | Numeric and non-missing |
| `citations` | Citation count at frozen snapshot | Numeric, non-negative |
| `metadata_language` | OpenAlex language metadata | Use `unknown` when missing; do not call it verified publication language unless audited |
| `label` | Final binary relevance label | 0 or 1 only; exclude unresolved records |
| `label_status` | Label provenance status | `adjudicated`, `human_adjudicated`, or `single_reviewer_audited` |
| `split_group_id` | Group ID for versions/duplicates | Non-empty; all related versions share one value |

Recommended additional audit columns (preserve in the source manifest even though the modelling script does not require them): DOI, original metadata language, language verification status, query route(s), collection timestamp, citation snapshot date, label rationale, labeler ID, label date, confidence, second-review label, adjudication note, source URL and licence/access note.
