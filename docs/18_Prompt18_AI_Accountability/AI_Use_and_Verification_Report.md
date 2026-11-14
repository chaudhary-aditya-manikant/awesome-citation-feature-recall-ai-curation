# Prompt 18 — AI Assistance, Accountability and Verification Report

**Project:** Citation-feature effects on ranking recall in AI literature curation

## AI assistance used

AI assistance was used for research-workflow planning, candidate literature mapping, source-check preparation, annotation-rubric drafting, Python implementation and code review, test creation, and documentation. The student remains responsible for source verification, understanding the code, actual data decisions, and all submitted claims.

## Verification performed in this package

- The prior literature update contains source links and explicit novelty limitations; the review is targeted, not systematic/exhaustive.
- The 28-row pilot was inspected. Its preliminary labels are not ground truth; rubric v2 requires narrow task-based relevance and human re-adjudication.
- The original three input-validation tests and six additional checks (citation integer integrity, cluster bootstrap, and four collector helper tests and one mocked collector integration test) were executed: **10 passed**.
- Both Python scripts passed syntax compilation.
- A synthetic preflight-only gate path and a synthetic end-to-end model smoke test completed. These verify software behavior only; all metrics from synthetic data are excluded from research claims.
- Code review identified and corrected record-wise bootstrap resampling, synthetic-run status labelling, model seed propagation, potential output overwrite, missing/invalid numeric handling, and the need for a no-fit preflight gate.
- A bounded OpenAlex collector and an offline test suite were added. The collector was not live-run because the audit runtime could not resolve the OpenAlex API host.

## What remains unknown or not performed

- No human annotation or second-reviewer adjudication was performed by the assistant.
- No final candidate dataset, data licence audit or language-ground-truth audit is available.
- No accepted research baseline was trained; no research metrics, p-values, confidence intervals or bias findings exist.
- The student's own Colab/desktop environment has not been verified.
- No Turnitin/iThenticate/institutional similarity report was run.
- No GitHub repository, commit or public dataset licence is claimed unless supplied and verified by the student.

## Real AI limitations / verification examples

1. The original pilot's broad positive labels did not consistently meet the narrower target construct; the rubric was tightened and the labels were marked preliminary rather than accepted.
2. Initial code review found record-wise bootstrap resampling despite cluster-grouped splitting; this was changed to a paired cluster bootstrap and covered by a test.
3. Synthetic full-pipeline execution could have been misread as completed research; explicit `SOFTWARE_SMOKE_TEST_ONLY` status and input provenance declarations were added.
4. The preflight gate insertion initially contained a self-reference; inspection caught and corrected it before the passing execution check.

## Student responsibilities before submission

1. Verify the original literature sources and every citation supporting a claim.
2. Run the candidate collector in a network-enabled environment and preserve the genuine output/query logs.
3. Screen and adjudicate the data under rubric v2; document duplicate and language audits.
4. Review, understand and run the code; save actual environment, data hash and experiment logs.
5. Interpret only measured results and disclose all limitations and AI assistance under institute rules.


## Additional verified activity — 31 October 2026

- **Task:** audit the live balanced OpenAlex candidate pool and prepare reviewer workflows.
- **AI-assisted work:** inspected collection manifest/logs and candidate CSV; generated blinded screening and language-verification workbooks plus a separate private admin crosswalk; compiled a row-level source audit for eight administrative-exclusion candidates.
- **Human verification required:** the workbooks contain no human relevance labels; source language must be verified by a reviewer against publisher/library evidence. Seven administrative candidate decisions have publisher or authoritative bibliographic support in the current review; the movie-genres retraction flag remains pending a publisher notice.
- **Code correction:** detected that the experiment runner used the raw `duplicate_cluster_id` field despite the balanced audit requiring `split_group_id`. Changed the runner/schema and added two tests. The corrected package-build suite passed 20 tests. The Colab transcript supplied earlier predates this correction; a fresh Colab test run remains necessary.
- **Limit:** no AI-generated relevance decision was written into the human-label columns; no research model was fit and no empirical result was claimed.


## Additional package work — balanced pool follow-up, 31 October 2026

- **Human-label boundary:** no relevance label was generated or written by the assistant. The 2,763-record workbook is blinded and blank. The rubric and screen-import validator preserve human responsibility for final decisions.
- **Type-scope workflow:** added the source `OpenAlex_Record_Type` and a nonstandard-type flag to each batch as reviewer context. Workbook instructions say type alone is not an exclusion reason.
- **Language verification:** added a separate import validator that checks sample IDs and required evidence fields. It does not infer publication language or validate the truth of a supplied URL; human source inspection remains required.
- **Title metadata:** searched publisher issue pages for the 19 missing-title records. Six DOI records were corroborated as whole-issue/issue-level paratext and are excluded from the article pool; 13 remain unresolved and held rather than guessed.
- **Administrative source review:** seven of eight candidates have publisher/authoritative support. The `Movie genres and beyond` OpenAlex retraction flag remains unresolved because no publisher retraction notice was found; it stays on hold.
- **Current software evidence:** updated the import and source-review workflow and ran 30 package-build tests successfully; `py_compile src/*.py` passed. The latest Colab rerun remains a student-execution task.
- **No empirical analysis:** no baseline or experiment has been run on the balanced pool; no result, p-value, citation effect, or language bias is claimed.


## 5 November 2026 — AI screening and analysis (important)

- **What the AI did:** at the student's explicit request, Claude (Anthropic) screened all 2,763 queue records against Rubric v2 and assigned **AI-provisional** labels with coded rationales and confidence; ran a seeded 20% self-consistency re-screen (549/550 agreement, κ = 0.96); adjudicated uncertain records; built the model input; extended the runner (opt-in AI-provisional mode, exploratory mode, estimability guard); wrote the cross-fit script, figures and the empirical manuscript draft; updated Prompt 08–18 documents.
- **What the AI did not do:** it did not enter anything in the human decision columns of the screening workbooks, did not record any label under the student's name, and did not verify publication languages.
- **Disclosure obligations:** the labels are not human judgements. Until the student verifies them, the manuscript, results and any submission must describe them as AI-provisional. They are not recorded as the student's own judgement anywhere in the package.
- **Verification route:** `data/collection_audit_20261031/workbooks/AITR_Balanced_Human_Screening_Workbook_AI_Prefilled_20261105.xlsx` shows AI suggestions in yellow columns next to blank human columns.
- **Post-hoc change disclosed:** the estimability guard (Amendment A3 addendum) was added after the frozen run produced a degenerate interval.


## Final update (5 November 2026)

- The author reviewed 458 records (all AI-relevant/uncertain and boundary cases) and made the final decision on each, changing 15 AI labels (agreement 443/458, κ = 0.88). The author confirmed personally reviewing them; Reviewer_ID/Review_Date were filled from that confirmation.
- 2,305 clearly off-topic records keep the AI first-pass label and are disclosed as such in the manuscript.
- Final analyses and the manuscript use these labels; AI-only runs are archived as superseded.
- A bug found when re-running on merged labels (cross-fit script assumed an AI-only column) was fixed and covered by a test (39 tests pass).
