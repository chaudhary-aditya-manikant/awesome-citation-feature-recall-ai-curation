# Relevance Annotation Rubric v2 — Human Screening Guide

**Use only after retrieval and deduplication.** Annotate title and abstract (and full text only when needed and lawfully accessible). Do not infer relevance from citation count, author prestige, venue, country, or language.

## Target construct

A record is **relevant (1)** only when the paper itself studies, develops, evaluates, or substantively analyses a computational/AI method or tool whose target task is scholarly-literature discovery or curation. This includes:

- scholarly search/retrieval, citation searching, or paper discovery;
- ranking/recommendation of scholarly papers;
- ML/AI-assisted title/abstract screening or study selection;
- automation of systematic-review/evidence-synthesis identification or screening;
- active-learning prioritisation of records for human screening;
- evaluation of AI tools specifically for scholarly literature curation.

A record is **not relevant (0)** when AI is merely the subject matter being reviewed, or AI is applied downstream to the content of studies rather than to the discovery/selection/curation of scholarly records.

## Decision rules

| Situation | Label | Reason |
|---|---:|---|
| Develops/evaluates an ML model to rank or screen research-paper records | 1 | Direct target task |
| Evaluates a systematic-review screening tool on title/abstract records | 1 | Direct target task |
| Uses ChatGPT to draft a review protocol but does not evaluate retrieval/screening/selection | 0 or uncertain | Workflow assistance alone is outside narrow target |
| Uses AI to extract outcomes, classify clinical findings, or analyse full-text study content after selection | 0 | Downstream evidence extraction/analysis, not literature curation |
| Reviews AI use in medicine, education, agriculture, law, etc. | 0 | AI is the subject, not the curation method |
| Uses PRISMA or systematic review methodology but no AI/computational curation method | 0 | Review method alone is insufficient |
| Bibliometric mapping of AI research without evaluating scholarly search/curation methods | 0 | Descriptive bibliometrics is outside target |
| Title suggests relevance but abstract is missing/ambiguous | uncertain | Do not guess |
| Record is a dataset descriptor or protocol only | uncertain unless it clearly provides/evaluates a target curation dataset/tool | Apply same rule consistently |

## Annotation procedure

1. Read title and abstract without looking at citation count.
2. Apply the target construct and decision table.
3. Record `label` as `1`, `0`, or `uncertain`.
4. Record a one-sentence evidence-based rationale referencing the method/task described, not generic keywords.
5. Record `labeler_id`, `label_date`, `label_confidence` (high/medium/low), and whether the decision was independently reviewed.
6. Escalate all uncertain records. Do not convert uncertainty into a negative by default.
7. If a second reviewer is available, independently double-screen all uncertain records and a seeded random 20% of decided records. Resolve disagreements by discussion and preserve both original labels plus adjudication.
8. If only one reviewer is available, re-screen uncertain records and a seeded random 20% after a time gap. This is a consistency audit, not independent inter-rater agreement.

## Important boundary correction to the 28-record pilot

The earlier pilot labelled some broad ChatGPT-assisted systematic-review protocol/workflow records as positive. Under this stricter v2 rubric, protocol drafting alone is not sufficient; the record must directly study the retrieval, ranking, screening, or selection function. The original pilot labels are therefore **not transferable gold labels** and must be re-adjudicated from full titles/abstracts. Abstract text was not included in the shared pilot CSV, so this re-adjudication cannot be completed from the archive alone.
