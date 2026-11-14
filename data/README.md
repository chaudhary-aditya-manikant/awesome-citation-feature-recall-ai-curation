# Data: sources, licences and what is included

| Study | Source | Licence | In this repository | Not in this repository |
|---|---|---|---|---|
| Study 1 (pilot) | OpenAlex API, snapshot 30 Oct 2026 | CC0 (metadata) | `collection_audit_20261031/` (abstract-free pool, query log, audit), `ai_provisional_20261105/` and `spotcheck_20261110/` (labels with source and rationale) | Abstract text (publisher copyright); rebuild with `src/collect_openalex_candidates_balanced.py` and the manifest |
| Study 2 (confirmatory) | SYNERGY v1.0, De Bruin et al. 2023, doi:10.34894/HE6NAQ, read with the `synergy-dataset` Python package | CC0 | `study2/synergy_manifest.json` (records and inclusions per review, file hash, citation source and reference year); out-of-fold scores in `results/study2_confirmatory/` | The downloaded records with abstracts; rebuild with `notebooks/Study2_SYNERGY_Colab.ipynb` (sets `SYNERGY_SET=synergy`, `--citations package`) |

No API keys, private data or restricted files are stored here. The rest of this file documents the Study 1 collection workflow.

---

# Candidate data workflow

## Purpose and safety boundary

`src/collect_openalex_candidates.py` constructs a bounded OpenAlex candidate pool using the eight search routes and four topic routes in the frozen plan, plus a one-hop citation neighbourhood around seed papers. It does **not** create relevance labels, adjudicate duplicates, or establish publication-language truth. It is an acquisition tool only.

OpenAlex currently documents `abstract_inverted_index` as the abstract representation; plaintext is reconstructed locally for title/abstract annotation. The API does not ship plaintext abstracts. Keep `candidate_pool_private.csv`, `raw_records.jsonl`, and all abstract-bearing data in a private working directory unless source terms and the instructor explicitly permit redistribution.

## Run

From the repository root:

```bash
python src/collect_openalex_candidates.py \
  --output-dir data/private_collection_20261030 \
  --seeds data/seed_papers.csv \
  --per-route-year 100 \
  --max-unique 3000
```

The collector uses the public API without a key for this bounded first-page collection. For heavier use, set `OPENALEX_API_KEY` in the environment; never hard-code a key or place it in logs. The script limits calls to at most 100 records per route/year and does not require cursor paging. The route/year first-page results are a purposive candidate pool, not a random or representative sample. Its alternating publication-date sort only avoids using one global relevance-ranked result list; it does not remove query coverage or truncation bias. If a topic ID is stale or unavailable, that route error is retained in `collection_errors.json`; do not silently omit it in the report.

OpenAlex `language` is detected from metadata and must be treated as a metadata field, not verified publication language. The `abstract_inverted_index` must be reconstructed for local screening; keep this plaintext local. Record the captured citation snapshot date and never compare counts from different snapshots as if static.

## Files created

- `candidate_pool_private.csv`: private working table, includes reconstructed abstract text and blank human-label fields.
- `candidate_pool_shareable.csv`: abstract-free metadata copy; still a candidate pool, not adjudicated data.
- `raw_records.jsonl`: raw OpenAlex record objects for provenance.
- `query_log.jsonl`: route IDs, exact parameters/URLs (no API key), retrieval timestamps and API counts.
- `collection_manifest.json`: dates, query totals, counts and errors.
- `collection_errors.json`: failed/invalid route information.

The collector only assigns duplicate/version clusters conservatively from exact DOI or exact normalized title + year + first-author ID. It retains all records within a cluster and marks multi-record clusters `needs_canonical_review`; a human must decide the canonical record or document an ambiguous version relationship before the model dataset is frozen.

## Human screening sequence

1. Review all candidate records using `Annotation_Rubric_v2.md` without looking at citations, language, source route, or prestige.
2. Label `relevant`, `not_relevant`, or `uncertain` during screening. Do not force uncertain cases into a binary class.
3. Resolve every uncertain case; preserve original label, reviewer, rationale and adjudication.
4. Review duplicate clusters and keep one canonical work per paper; preserve the cluster map.
5. Audit metadata language on the frozen stratified sample required by Prompt 07.
6. Export a final CSV that meets `docs/09_Prompt09_Baseline_Code/input_schema.csv`. Do not run the model until the Prompt 07 data gate has passed.

The candidate collector has offline unit tests and a mocked integration test for output separation/provenance logging. A live OpenAlex collection must be run by the student from Colab or a network-enabled machine; this runtime could not resolve the API host during this audit.
