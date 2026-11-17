#!/usr/bin/env python3
"""Study 2 robustness check at the level of whole reviews (added 17 November 2026; post hoc, not pre-registered).

The pre-registered interval resamples title groups *within* each review and fold, so it treats the 20 SYNERGY
reviews as fixed. This check asks instead: if a different set of reviews had been available, would the
effect still be there? It uses only the committed per-review counts in `study2_per_dataset.csv`.

  1. Review-level bootstrap: resample the 20 reviews with replacement (10,000 replicates, seed 20261031)
     and recompute the pooled difference each time.
  2. Unweighted mean of the per-review differences (each review counts once, whatever its size), with a
     review-level bootstrap interval, over reviews with at least one lower-citation relevant record.
  3. Sign test: in how many reviews was the citation-blind ranker better vs worse (ties dropped).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest


def per_review(results: Path) -> pd.DataFrame:
    d = pd.read_csv(results / "study2_per_dataset.csv")
    low = d.pivot(index="dataset", columns="condition", values="low")
    alls = d.pivot(index="dataset", columns="condition", values="all")
    base = d[d.condition == "citation_blind"].set_index("dataset")
    return pd.DataFrame({"den_low": base.den_low, "den_all": base.den_all,
                         "blind_low": low.citation_blind, "aware_low": low.citation_aware, "fair_low": low.fair_rerank,
                         "blind_all": alls.citation_blind, "aware_all": alls.citation_aware})


def check(t: pd.DataFrame, reps: int = 10000, seed: int = 20261031) -> dict:
    rng = np.random.default_rng(seed)
    n = len(t)
    idx = rng.integers(0, n, (reps, n))
    s = lambda col: t[col].to_numpy()[idx].sum(1)
    q = lambda v: [float(np.quantile(v, .025)), float(np.quantile(v, .975))]
    pooled = lambda a, b, den: (t[a].sum() - t[b].sum()) / t[den].sum()

    u = t[t.den_low > 0]
    per = ((u.blind_low - u.aware_low) / u.den_low).to_numpy()
    idx2 = rng.integers(0, len(u), (reps, len(u)))
    better, worse = int((u.blind_low > u.aware_low).sum()), int((u.blind_low < u.aware_low).sum())
    return {
        "status": "POST_HOC_ROBUSTNESS_NOT_PREREGISTERED", "added_on": "2026-11-17",
        "reviews": n, "replicates": reps, "seed": seed,
        "blind_minus_aware_lower_recall": {
            "point": float(pooled("blind_low", "aware_low", "den_low")),
            "review_level_ci95": q((s("blind_low") - s("aware_low")) / s("den_low"))},
        "fair_minus_aware_lower_recall": {
            "point": float(pooled("fair_low", "aware_low", "den_low")),
            "review_level_ci95": q((s("fair_low") - s("aware_low")) / s("den_low"))},
        "blind_minus_aware_overall_recall": {
            "point": float(pooled("blind_all", "aware_all", "den_all")),
            "review_level_ci95": q((s("blind_all") - s("aware_all")) / s("den_all"))},
        "unweighted_mean_of_per_review_differences": {
            "reviews_with_lower_citation_relevant": int(len(u)),
            "mean": float(per.mean()), "median": float(np.median(per)),
            "review_level_ci95": q(per[idx2].mean(1))},
        "sign_test": {"blind_better": better, "same": int(len(u) - better - worse), "blind_worse": worse,
                      "two_sided_p": float(binomtest(better, better + worse, 0.5).pvalue)},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, required=True, help="results/study2_confirmatory")
    ap.add_argument("--replicates", type=int, default=10000)
    a = ap.parse_args()
    out = check(per_review(a.results), a.replicates)
    (a.results / "study2_review_level_check.json").write_text(json.dumps(out, indent=2) + "\n")
    p = out["blind_minus_aware_lower_recall"]
    m = out["unweighted_mean_of_per_review_differences"]
    s = out["sign_test"]
    print(f"Pooled difference (blind - aware), rarely cited recall: {p['point']:.3f}")
    print(f"  interval resampling papers within reviews (pre-registered): 0.033 to 0.068")
    print(f"  interval resampling whole reviews (this check):          {p['review_level_ci95'][0]:.3f} to {p['review_level_ci95'][1]:.3f}")
    print(f"Average per-review difference (each review counts once): {m['mean']:.3f} "
          f"({m['review_level_ci95'][0]:.3f} to {m['review_level_ci95'][1]:.3f})")
    print(f"Sign test: blind better in {s['blind_better']}, same in {s['same']}, worse in {s['blind_worse']} "
          f"(two-sided p = {s['two_sided_p']:.4f})")


if __name__ == "__main__":
    main()
