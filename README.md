# Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation

**AI Tools for Research — Lab 2 (implementation study)** · Aditya Chaudhary (MNS2026008), Indian Institute of Information Technology, Allahabad · November 2026

## Research question

Literature search and screening tools often rank papers partly by citation count. This study asks:
**does adding a citation-count feature to a transparent relevance ranker lower the recall of relevant but rarely cited papers in literature screening?**

It follows from the author's literature review, *Recall Bias Toward Highly-Cited and English-Language Papers in AI Literature Curation: A Survey of Mechanisms, Current Approaches, and Research Gaps*, which found that evaluations of screening and citation-searching tools report recall only for whole collections, never split by citation band or language. See `research_decisions.md` for the full path from review to question.

**Design (pathway C, targeted modification).** Two identical TF-IDF + logistic-regression rankers differ in one feature, standardised log(1 + citations). The primary metric is Recall@20% for relevant papers in the lower half of the age-adjusted citation distribution, with grouped five-fold splits.

**Two studies.**
- **Study 1 (pilot, exploratory):** a 2,790-record OpenAlex pool on AI literature curation. The data gate failed (7 rarely cited relevant papers), so it could suggest the effect but not confirm it.
- **Study 2 (confirmatory):** the same hypothesis, pre-registered again and tested on the SYNERGY benchmark (20 systematic reviews, 150,154 records, 2,745 relevant, human labels). The gate passed and the hypothesis was supported.

## Headline result (Study 2, confirmatory)

| Pooled over 20 reviews, K = 20% | Lower-citation relevant | Higher-citation relevant | All relevant | Precision |
|---|---|---|---|---|
| Citation-blind | 742/977 (0.759) | 1424/1768 (0.805) | 0.789 | 0.072 |
| Citation-aware | 691/977 (0.707) | 1486/1768 (0.840) | 0.793 | 0.072 |
| Citation-only | 0/977 | 896/1768 (0.507) | 0.326 | 0.030 |
| Fair re-rank (50% of top-K reserved) | 770/977 (0.788) | 1364/1768 (0.771) | 0.777 | 0.071 |

- **H1 supported.** Removing the citation feature raised lower-citation recall by **0.052** (95% cluster-bootstrap CI 0.033–0.068), with no detectable change in overall recall (−0.004, CI −0.015 to 0.003) or precision.
- **The feature redistributes recall:** higher-citation recall rose by 0.035 with the feature (descriptive, not a pre-registered contrast). Overall recall hides this.
- **H2 supported.** The fair re-rank recovered 0.081 of lower-citation recall (CI 0.062–0.100) at a precision cost of 0.001.
- **Not uniform.** Citation-blind was better in 14 reviews, equal in 4, worse in 1; the largest review showed no difference.
- **Much smaller than the pilot** (0.052 vs 0.57): the pilot had the sign right and the size wrong.

Evidence: `PREREGISTRATION_v2.md`, `configs/study2_protocol.json`, `results/study2_confirmatory/`, and two dated notes written before any result (`docs/06_Evidence_and_Logs/Study2_*.md`): the SYNERGY version, and the switch to the citation counts stored in SYNERGY after OpenAlex's rate limit stopped the live download.

## Study 1 results (pilot, exploratory)

The pre-registered dataset gate (≥ 20 relevant lower-citation records in the test fold) **failed**: only 7 of 64 relevant records were rarely cited. All results are therefore exploratory.

| Cross-fitted, K = 20% | Citation-blind | Citation-aware |
|---|---|---|
| Lower-citation relevant recall | 7/7 (1.000) | 3/7 (0.429) |
| Higher-citation relevant recall | 56/57 (0.982) | 54/57 (0.947) |
| All relevant recall | 63/64 (0.984) | 57/64 (0.891) |

Paired difference in lower-citation recall: 0.57 (95% cluster-bootstrap CI 0.14–1.00).

**Post-hoc reference rankers** (added after the main results; same folds, not pre-registered):

| K = 20% | Lower-citation | All relevant | Precision |
|---|---|---|---|
| Citation-only (rank by citations alone) | 0/7 | 37/64 | 0.067 |
| Fair re-rank (citation-aware, 50% of top-K reserved for lower-citation) | 7/7 | 58/64 | 0.105 |

Reserving slots recovers the rarely cited papers but not the overall recall loss (0.906 vs 0.984 for citation-blind; difference 0.078, CI 0.016–0.145). Source: `results/run_20261105_reviewed_posthoc_comparators/`. The direction is consistent with citation features pushing rarely cited relevant papers down the queue, but it rests on 7 records and a pool whose relevant records came mostly from citation neighbourhoods (46/64).

## Spot-check of AI-only labels (Amendment A4)

A seeded random 200 of the 2,305 records that kept the AI label were re-screened blind by the author (AI label and citations hidden). **Result:** agreement 190/200; 3 missed relevant records (1.5%, exact 95% CI 0.3–4.3%, about 35 of 2,305), all with 0 citations; 7 had no usable abstract. Re-running Study 1 with only these 200 corrected: lower-citation recall 9/10 (blind) vs 3/10 (aware), difference 0.60 (CI 0.33–1.00); gate still fails. Outputs: `results/spotcheck_20261110/`, `results/run_20261110_spotcheck_*`.

The sample was drawn by (`src/make_spotcheck_sample.py`, key in `data/spotcheck_20261110/`). Score with:

```bash
python src/score_spotcheck.py --sheet <returned sheet .xlsx> --key data/spotcheck_20261110/spotcheck_key.csv \
  --labels data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv --output results/spotcheck_20261110
```

## Repository structure

```
README.md                  this file
requirements.txt           dependencies (tested versions: requirements-tested-container.txt)
configs/                   frozen experimental settings (frozen_protocol.json)
data/README.md             data access, licence and what is (not) included
data/collection_audit_20261031/   pool manifest, query log, audit outputs (metadata only)
data/ai_provisional_20261105/     screening labels with source, rationale and confidence
notebooks/                 Colab notebook that re-runs tests and analysis
src/                       collection, experiment, cross-fit, merge and figure code
scripts/run_all.sh         one command: preflight gate → frozen run → cross-fit → figures
scripts/viva_demo.py       live re-run with an identical-results check (Windows-friendly)
results/                   genuine metric files, logs, predictions and figures
paper/                     LaTeX source, bibliography, figures and compiled PDF
tests/                     58 automated tests
PREREGISTRATION_v2.md      Study 2 pre-registration (author's decisions and reasons)
research_brief.md          one-page research brief (brief §11 template)
research_decisions.md      literature-to-experiment decisions
baseline_validation.md     baseline checks and deviations
ai_assistance_log.md       significant AI assistance and human verification
docs/demo_and_viva.md      five-minute demonstration script and viva preparation
docs/                      full provenance: Prompt 01–18 outputs, protocol amendments, audits
```

## Reproduce

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests                        # 58 tests, ~30 s
bash scripts/run_all.sh <model_input.csv> <tag> ai
```

**Library versions matter for exact reproduction.** `requirements.txt` pins the versions that reproduce every committed number, checked on Linux and on the author's Windows laptop (14 November 2026). With older libraries (scikit-learn 1.5.2, numpy 2.1.2) the retrained Study 1 rankers gave the same K = 20% counts and point estimates (7/7 vs 3/7, difference 0.571), but the bootstrap interval moved slightly (0.167–1.00 instead of 0.143–1.00). Use a clean environment:

```bash
python -m venv ~/aitr_env && source ~/aitr_env/Scripts/activate    # Linux/macOS: source ~/aitr_env/bin/activate
python -m pip install -r requirements.txt
```

**Live check (any OS):** `python scripts/viva_demo.py` re-runs the tests and post-hoc rankers and confirms the outputs are identical to the committed ones. Add `--data <private model input>` to refit both rankers as well (about 1.5 minutes).

`run_all.sh` writes `results/<tag>_preflight`, `results/<tag>_frozen`, `results/<tag>_crossfit` (with figures) and `results/<tag>_posthoc_comparators`. Seeds are fixed (split 20261030, bootstrap 20261031); re-running on the same input reproduces the committed result files exactly. The whole analysis runs on a CPU in under a minute. In Colab, use `notebooks/MNS2026008_Colab_Rerun.ipynb`.

**Input data.** The model input needs abstract text, which is not redistributed here (publisher copyright). To rebuild it, run `src/collect_openalex_candidates_balanced.py` with the parameters in `data/collection_audit_20261031/audit/collection_manifest.json` (snapshot 30 October 2026), then join the labels in `data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv` on `openalex_id`. A fresh OpenAlex pull may differ slightly from the snapshot. **[TEST REQUIRED]** for a fresh pull; the committed results were produced from the snapshot.

**Paper.** Compile `paper/main.tex` with pdfLaTeX (Overleaf or TeX Live): `pdflatex main; bibtex main; pdflatex main; pdflatex main`.

**Study 2.** Rebuild the confirmatory table from the committed scores (no downloads, about 20 s):

```bash
cd src && python study2_verify_from_scores.py --results ../results/study2_confirmatory --protocol ../configs/study2_protocol.json
```

To repeat Study 2 from the public SYNERGY release, run `notebooks/Study2_SYNERGY_Colab.ipynb` (about 15–20 minutes in Colab).

## Label provenance (Study 1)

1. An AI first pass (Claude, Anthropic) applied the written rubric to all 2,763 screening records, with a rationale and confidence for each (20% self-consistency check: 549/550).
2. The author reviewed the 458 relevant, uncertain and boundary records and made the final decision on each (agreement with the AI 443/458, κ = 0.88; 15 decisions changed).
3. The remaining 2,305 clearly off-topic records keep the AI label (`label_source = ai_provisional_not_reviewed`). Outputs are stamped `MIXED_LABELS_REVIEWER_AND_AI_PROVISIONAL`.
4. A seeded random 200 of those 2,305 were re-screened blind by the author on 10 November 2026 (Amendment A4): 190 agreed, 3 were relevant, 7 uncertain. The corrected labels are in `data/spotcheck_20261110/`.

## Limitations

- **Study 1:** exploratory (gate failed); 7 lower-citation relevant records (10 after the spot-check corrections); collection-route confound; 2,105 records keep AI-only labels; one OpenAlex snapshot.
- **Study 2:** the effect is small and differs between reviews; the reviews are mostly in medicine and the health and behavioural sciences, so it confirms the effect for systematic-review screening in general, not specifically for AI literature; citation counts were collected after the reviews were published; the citation source was changed before any result (deviation D1); the interval reflects resampling within folds only.
- **Both:** one linear ranker; publication languages not verified, so no language claim is made.

## Licence and citation

Code: MIT (see `LICENSE`). OpenAlex metadata: CC0. Paper text and figures: © the author.

Chaudhary, A. (2026). *Effect of Citation-Count Features on Lower-Citation Recall in AI Literature Curation*. AI Tools for Research, IIIT Allahabad.
