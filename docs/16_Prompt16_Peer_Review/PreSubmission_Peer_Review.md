# Prompt 16 — Pre-submission Technical Review of the Empirical Paper (5 November 2026)

Review of `paper/main.tex` (7 pages), written as a critical internal review. It was produced with AI assistance and is not an independent external review.

## Summary judgement
The paper is honest about its limits and every number traces to saved outputs. It is not yet suitable as a final empirical submission because its labels are AI-provisional and its primary analysis is exploratory.

## Major issues
1. **Label provenance (addressed 5 Nov).** The author reviewed the 458 relevant, uncertain and boundary records; 2,305 off-topic records keep AI labels. This is disclosed in Section 3.3 and the acknowledgement. A further check of a random sample of the unreviewed records would strengthen the claim that no relevant records were missed.
2. **Denominator.** The lower-citation group has 7 relevant records (spread across all five folds). The bootstrap interval ignores fold-composition dependence. Consider reporting a leave-one-record-out or exact sign analysis, or simply avoiding interval-based language beyond "consistent direction".
3. **Collection confound.** 72% of relevant records come from citation neighbourhoods. A sensitivity analysis excluding citation-route records (or stratifying by route) would show whether the effect survives; this is not pre-registered and must be labelled as such if added.
4. **Ceiling effect.** The citation-blind ranker reaches 0.985 overall recall at 20%; differences appear only in the tail. Reporting rank-based measures (e.g., mean rank of relevant lower-citation records) would be more informative.

## Minor issues
- The amendment-addendum guard (min. 10 lower-citation records) was added after seeing an output; it is disclosed, but say so again in the limitations.
- Add the exact query strings and seed DOIs in an appendix table.
- State the median citation rate and its computation once in the abstract or methods (done in methods).

## Checks performed
Numbers in the abstract, Tables 1–2, Figures 1–2 and Sections 5.1–5.6 were compared against `crossfit_pooled_metrics.csv`, `crossfit_paired_contrasts.csv`, `crossfit_relevant_records_ranks.csv`, `primary_comparison.csv` and the preflight report: all match.
