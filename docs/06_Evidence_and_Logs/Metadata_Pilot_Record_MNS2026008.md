# Metadata Feasibility Pilot Record

## Project
- **Project title:** Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation
- **Student / course identifier:** MNS2026008 — AI Tools for Research
- **Pilot date recorded:** 2026-10-29
- **Pilot purpose:** Test whether a candidate labelled review collection has the metadata and group coverage needed for the proposed citation-aware versus citation-blind ranking experiment.
- **Pilot status:** Executed; feasibility result is **NO-GO for the main AI-literature experiment using this collection alone**.
- **Evidence artifact:** Output cells in the student-retained Colab notebook `Recall_Bias_Metadata_Pilot (4).ipynb`, including the final CSV loading, column checks, language counts, citation-group crosstabs, and summary save message. The notebook is not included in this package because it contains reconstructed abstract plaintext; this file preserves the relevant summary without reproducing the abstracts.

## Status-label definitions
- **VERIFIED:** Directly visible in the saved notebook output, bounded to this run and this selected collection.
- **INFERRED:** Interpretation based on the observed data; not itself a measured causal result.
- **UNKNOWN:** Not established by this pilot.
- **PENDING:** Required next action not yet completed.

## Data source and configuration
- **Dataset collection:** SYNERGY+ dataset, version 3.0 as shown in the notebook's installation/download output.
- **Selected review collection:** `Hall_2011.csv`.
- **Final local Colab export used for the pilot:** `/content/synergy_dataset_with_text_metadata/Hall_2011.csv`.
- **Requested fields in export command:** `title`, `abstract`, `cited_by_count`, `publication_year`, `language`, and `language_fasttext`.
- **Other columns present:** `openalex_id`, `doi`, `lens_id`, `label_included`.
- **Abstract handling:** The package asked whether to reconstruct inverted abstracts locally; `Y` was entered. Reconstructed plaintext abstracts must remain local and must not be republished or redistributed, consistent with the package notice.
- **Notebook / code:** `Recall_Bias_Metadata_Pilot (4).ipynb`. This record documents notebook outputs; it does not claim an independent reproduction outside the recorded Colab run.

## Observed results

### Schema and missingness

| Check | Recorded result | Status |
|---|---|---|
| CSV exists | Yes | VERIFIED |
| Rows | 340 | VERIFIED |
| Columns | 10 | VERIFIED |
| `title` | 340/340 non-missing | VERIFIED |
| `abstract` | 340/340 non-missing | VERIFIED |
| `cited_by_count` | 340/340 non-missing | VERIFIED |
| `publication_year` | 340/340 non-missing | VERIFIED |
| `label_included` | 340/340 non-missing | VERIFIED |
| `language` | 340/340 non-missing | VERIFIED |
| Explicit language values | `en` for all 340 records | VERIFIED |
| `language_fasttext` | Column is present in the schema; full value coverage was not separately summarized in the saved output | UNKNOWN |

**Columns observed:** `openalex_id`, `doi`, `lens_id`, `title`, `abstract`, `cited_by_count`, `publication_year`, `language`, `language_fasttext`, `label_included`.

### Inclusion labels

| `label_included` value | Number of records | Status |
|---|---:|---|
| `0` | 336 | VERIFIED |
| `1` | 4 | VERIFIED |
| **Total** | **340** | **VERIFIED** |

The notebook treats label `1` as included/relevant and label `0` as excluded/not included for this review collection. These are review-specific screening labels, not universal relevance judgements for AI literature.

### Language group

| Language group from the explicit `language` field | Records |
|---|---:|
| English (`en`) | 340 |
| Non-English / other | 0 |
| Unknown | 0 |

This is a distribution within the selected collection, not evidence that SYNERGY as a whole contains no non-English records. The field is database language metadata; this pilot did not independently verify the language of each full-text publication.

### Citation split and included records

- **Observed median citation count:** 11.0.
- **At or below the collection median:** 174 records.
- **Above the collection median:** 166 records.

| Citation group | All records | Included-labelled records (`label_included = 1`) |
|---|---:|---:|
| At or below median (≤ 11) | 174 | 1 |
| Above median (> 11) | 166 | 3 |
| **Total** | **340** | **4** |

These are descriptive counts from this collection. The notebook notes that citation counts are age-dependent and that publication year and citation snapshot date need consideration in a substantive experiment.

## Interpretation

- **VERIFIED:** The selected export contains 340 records and all required columns for a basic metadata pilot; title, abstract, citation count, year, inclusion label, and explicit language field are non-missing in the output.
- **VERIFIED:** The collection has four included-labelled records and all 340 records have the explicit language value `en`.
- **VERIFIED:** The within-collection citation median is 11.0, with 174 records at/below the median and 166 above it; the four included-labelled records split 1 and 3 across these groups.
- **INFERRED:** With no non-English records and only four included-labelled records, this collection cannot support a useful English-versus-non-English recall comparison, and group-recall estimates based on four positives would be highly unstable.
- **INFERRED:** The first displayed titles relate to fault prediction, fault detection, and fault-tolerant systems. The pilot has not established that this collection is a suitable corpus for an AI-literature-curation claim.
- **UNKNOWN:** Whether this collection could support a differently scoped software-engineering review-screening study; whether any larger or other SYNERGY collections have suitable non-English records; and the exact language-field accuracy for these records.
- **UNKNOWN:** Novelty of the proposed project. This pilot tests data feasibility, not research novelty.

## Decision

**Decision: NO-GO for using `Hall_2011.csv` alone as the main dataset for the proposed joint citation-by-language AI-literature experiment.** Do not train the primary ranker or claim citation/language bias from these counts.

**Reason:** The selected collection has no non-English records, only four included-labelled records, and its fit to AI-literature curation is not established.

**Permitted use:** Retain this as a documented feasibility/pipeline pilot. It shows that the schema-loading and basic group-count code ran on a real exported collection, but it does not validate the hypothesis.

## Next actions

1. **PENDING:** Find or construct a bounded, on-topic AI-literature pool with title/abstract, citation count, publication year, usable language metadata, and enough independently judged relevant papers in the target groups.
2. **PENDING:** Decide and document the label source and relevance-judgement protocol. Do not treat SYNERGY review inclusion labels as universal AI-paper relevance labels.
3. **PENDING:** Check language distribution and included-label counts before model training; retain unknown language separately and validate metadata language on a sample if used.
4. **PENDING:** Normalize/stratify citations with publication year or a defensible citation snapshot, and record the snapshot date.
5. **PENDING:** Only after the dataset passes the pilot, run the planned citation-aware and citation-blind conditions on the same fixed pool/split and report group denominators and uncertainty.

## Claims that must not be made from this pilot

- Do not say that citation bias has been demonstrated.
- Do not say that non-English AI papers have lower recall; this collection contains no non-English records.
- Do not describe the four positive labels as a representative AI-literature ground truth.
- Do not claim a trained model, ranking experiment, ablation, or main hypothesis test has been run.
- Do not publish reconstructed plaintext abstracts from the SYNERGY export.

## Reproducibility note

The results above were transcribed from the outputs stored in the uploaded Colab notebook. The notebook reports the final file shape and columns, explicit language counts, label counts, citation median, group crosstabs, and a saved summary table. This report is a research record, not the raw data; reconstructed abstract plaintext is intentionally not included.
