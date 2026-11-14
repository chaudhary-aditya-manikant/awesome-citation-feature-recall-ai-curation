# Pre-registration v2: Study 2 (confirmatory)
**Author:** Aditya Chaudhary (MNS2026008) · **Frozen on:** 13/11/2026, before any SYNERGY data were downloaded (protocol: `configs/study2_protocol.json`)

> **How to use this file.** Every ✍️ is yours to write in your own words: a decision plus one to three sentences of reasoning. Do not paste AI text into the ✍️ fields. These paragraphs are your evidence that "the reasoning is yours". Commit this file **before** you run the data fetch, so the git timestamp proves the order.

## 1. Why Study 2 exists
Study 1 (pilot, exploratory) found that adding a citation feature lowered lower-citation Recall@20% from 7/7 to 3/7 (paired difference 0.57, 95% CI 0.14–1.00). Its pre-registered gate failed because only 7 relevant records were rarely cited, and 46/64 relevant records came via citation routes.

✍️ **In your words: what did Study 1 teach you, and why is a new dataset the right next step rather than re-analysing Study 1?**

Study 1 showed a promising exploratory result, suggesting that citation-based ranking may disadvantage lower-citation papers. However, the number of relevant records was too small to establish a reliable conclusion. I am conducting Study 2 using a larger dataset to obtain stronger evidence and determine whether the observation from Study 1 holds consistently.

## 2. Hypotheses
- **H1 (primary):** On SYNERGY, the citation-blind ranker achieves higher lower-citation Recall@20% than the citation-aware ranker.
- **H2 (secondary):** Reserving top-K slots for lower-citation records (fair re-rank) recovers lower-citation recall compared with citation-aware, at a precision cost of no more than the threshold in §5.
- **H3 (descriptive):** The citation-only ranker shows how much ranking by citations alone would favour highly cited records.

✍️ **Do you keep, change or drop H2/H3? Why?**

I am keeping H2 and H3 because they provide useful additional perspectives on the behaviour of the ranking models. H2 helps evaluate whether fair re-ranking can improve the visibility of lower-citation papers without causing a significant loss in overall precision. H3 helps demonstrate how ranking based only on citations favours highly cited papers. These hypotheses were also useful in the exploratory analysis of Study 1.

## 3. Data decisions
| Decision | Your choice ✍️ | Your reason ✍️ |
|---|---|---|
| Datasets: all SYNERGY or a subset | All SYNERGY datasets | Using all available SYNERGY datasets will provide a broader evaluation and reduce dependence on a small or selectively chosen sample. |
| `min_inclusions_per_dataset` | 20 | Keeping reviews with at least 20 relevant papers provides a sufficiently large sample for meaningful evaluation and comparison. |
| Citation snapshot date | 13/11/2026 (date of data collection) | Citation counts will be collected at the time of conducting Study 2 to maintain a consistent reference point across all included papers. |
| How duplicates are grouped (default: same normalised title within a dataset) | Same normalised title within a dataset | Papers with the same normalised title within a dataset will be treated as duplicates to avoid counting the same paper multiple times. |

**Threat you must address:** OpenAlex citation counts are measured *today*, years after each review was done. An included paper may have gained citations *because* the review cited it.

✍️ **How do you handle this: accept it as a stated limitation, restrict to reviews published recently, or something else?**

I will accept this as a limitation and explicitly mention it in the final research paper. Since citation counts are collected today rather than at the time each review was conducted, older papers may have had more time to accumulate citations. Additionally, being included in a review may itself contribute to a paper receiving more citations. This limitation will be acknowledged when interpreting the results.

## 4. Gate (decide before seeing any data)
| | Your value ✍️ | Your reason ✍️ |
|---|---|---|
| Minimum relevant lower-citation records (pooled over datasets and folds) | 50 | Study 1 used a threshold of 20, but the available number of lower-citation relevant records was insufficient to establish a strong conclusion. Increasing the threshold to 50 will require a larger evidence base for the confirmatory evaluation. |
| Minimum relevant higher-citation records | 50 | Keeping the same minimum requirement for higher-citation records will provide a more balanced basis for comparing the two citation groups. |

If the gate fails, Study 2 is reported as exploratory, exactly as Study 1 was.

## 5. Conditions, metric and success rule
- Conditions: `citation_blind`, `citation_aware`, `citation_only`, `fair_rerank`. The model is identical to Study 1.
- Fair re-rank reserved fraction ✍️ **0.5** (reason: I am retaining the value of 0.5 from Study 1 to maintain consistency in the fair re-ranking approach and avoid introducing an unnecessary change in the experimental configuration.)
- Metric: Recall@20% for lower- and higher-citation relevant records; sensitivity at 10% and 30%.
- **H1 supported** if the gate passes, the blind − aware difference is > 0, its 95% paired cluster-bootstrap CI lower bound is > 0, and the blind model loses no more than ✍️ **0.05** overall precision (reason: I am retaining the value of 0.05 from Study 1 because I do not have a strong methodological reason to change this threshold. Keeping it also allows the evaluation to remain consistent with the original study.)

## 6. What will not change after data are seen
The model, features, folds, seeds, K rule, gate, thresholds and success rule. Any change after this date is recorded as a dated amendment and labelled post-hoc.

## 7. Author's sign-off
Aditya Chaudhary 13/11/2026
