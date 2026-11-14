# Research Decisions — literature to experiment

Project: *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation* · Aditya Chaudhary (MNS2026008)
Labels: **VERIFIED** (checked against a source or a real run), **INFERRED** (plausible, not yet tested), **UNKNOWN** (no evidence).
Full dated log: `docs/01_Prompt01_Research_Workspace/research_decisions.md`.

## 1. From the review to the question
| Step | Decision | Status / evidence |
|---|---|---|
| Source review | *Recall Bias Toward Highly-Cited and English-Language Papers in AI Literature Curation: A Survey of Mechanisms, Current Approaches, and Research Gaps* (ATR review, MNS2026008) | VERIFIED — PDF, LaTeX and BibTeX inspected |
| Gap taken from the review | The evaluations it compares (RobotAnalyst, ASReview, automated citation searching, LLM screening) report recall for the whole collection only, never split by citation band or language; Google Scholar is known to weight citation counts in ranking (Beel & Gipp 2009) | VERIFIED for the cited studies; the field-wide absence is INFERRED |
| Question | Does adding a citation-count feature to a transparent ranker lower Recall@K for relevant, rarely cited papers? | Narrowed from the review's citation × language agenda to one isolated mechanism |
| Pathway | C — targeted modification: one feature added to a baseline, everything else fixed | Brief §3 |
| Language (RQ3) | Kept conditional: only if publication languages were verified and groups large enough | Not met — UNKNOWN |

## 2. Data and baseline
| Decision | Reason | Evidence |
|---|---|---|
| OpenAlex (CC0) as the data source | Open, licensed for reuse, citation counts and language metadata included | `docs/04_Prompt04_Feasibility/` |
| Quota-stratified pool: 8 English keyword queries, 4 topic filters, citation neighbourhoods of 5 seeds; 20 records per query-year; 2015–2025; seeded random sampling | Avoid citation-sorted sampling; balance years | `data/collection_audit_20261031/audit/collection_manifest.json` |
| Metadata audit before screening (27 records withheld; version groups in `split_group_id`) | Prevent duplicate/version leakage across splits | `data/collection_audit_20261031/audit/` |
| Baseline: TF-IDF (title + abstract) + year + Logistic Regression | Transparent, fast, standard in screening research; isolates the citation feature | `src/run_experiment.py`, `configs/frozen_protocol.json` |

## 3. Protocol
| Decision | Date | Record |
|---|---|---|
| Frozen blueprint: grouped 5-fold split, fold 0 test, K = 20%, gate ≥ 20 relevant per citation group in test, paired cluster bootstrap | 30–31 Oct 2026 | `docs/07_Prompt07_Frozen_Experiment_Blueprint/` |
| Amendment A2 (balanced pool replaces legacy pool) | 31 Oct 2026 | `docs/06_Evidence_and_Logs/Prompt06_Protocol_Amendment_A2_31Oct2026.md` |
| Amendment A3: gate cannot pass → report as exploratory; add cross-fitted analysis (recorded before any model was fitted) | 5 Nov 2026 | `docs/06_Evidence_and_Logs/Prompt07_Protocol_Amendment_A3_05Nov2026.md` |
| A3 addendum: estimability guard (≥ 10 lower-citation relevant test records), added after a degenerate result was seen; disclosed | 5 Nov 2026 | same file |

## 4. Screening
| Decision | Evidence |
|---|---|
| AI first pass on all 2,763 records under Rubric v2 with rationale and confidence; 20% self-consistency audit (549/550) | `data/ai_provisional_20261105/ai_provisional_screening_labels.csv`, `ai_consistency_audit_20pct.csv` |
| Author reviewed 458 relevant / uncertain / boundary records; agreement 443/458 (κ = 0.88); 15 decisions changed; 9 uncertain excluded | `data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv` |
| 2,305 clearly off-topic records keep the AI label (disclosed in the paper) | same file, `label_source` column |

## 5. Outcome
- Gate **failed** (test fold: 1 lower-citation, 12 higher-citation relevant). Results are exploratory — VERIFIED from `results/run_20261105_reviewed_preflight/`.
- Cross-fitted: lower-citation Recall@20% 7/7 (citation-blind) vs 3/7 (citation-aware); Δ = 0.57, 95% CI 0.14–1.00 — VERIFIED from `results/run_20261105_reviewed_crossfit/`.
- Post-hoc reference rankers (added 10 Nov 2026, after the main results, not pre-registered): citation-only 0/7 lower-citation, 37/64 overall; fair re-rank (50% of top-K reserved, share fixed before computing) 7/7 and 58/64 — VERIFIED from `results/run_20261105_reviewed_posthoc_comparators/`.
- Blind spot-check (Amendment A4, 10 Nov 2026): 190/200 agreement; 3 missed relevant (all 0 citations), 7 uncertain; corrected re-run 9/10 vs 3/10, Δ 0.60 (CI 0.33–1.00) — VERIFIED from `results/spotcheck_20261110/` and `results/run_20261110_spotcheck_crossfit/`.
- Study 2 (pre-registered 13 Nov 2026, run 14 Nov 2026 on SYNERGY): gate passed (977 lower-citation, 1,768 higher-citation relevant records; 20 reviews; 150,154 records). Citation-blind 742/977 vs citation-aware 691/977 at K = 20%, Δ = 0.052 (CI 0.033–0.068); overall recall Δ = −0.004 (CI −0.015 to 0.003); fair re-rank − aware = 0.081 (CI 0.062–0.100). H1 and H2 supported — VERIFIED from `results/study2_confirmatory/`; counts rebuilt identically from the committed scores.
- Study 2 deviations recorded before any result: original SYNERGY selected explicitly (package default had changed to SYNERGY+); citation counts taken from the SYNERGY release after OpenAlex rate-limited the live download twice (D1) — VERIFIED, `docs/06_Evidence_and_Logs/Study2_*.md`.
- Effect size differs from the pilot by an order of magnitude and varies by review (14 better, 4 equal, 1 worse) — VERIFIED from `study2_per_dataset.csv`. Why the largest review shows no effect — UNKNOWN.
- Interpretation that citation features push rarely cited relevant papers down — INFERRED (7 records; collection confound: 46/64 relevant via citation routes).
