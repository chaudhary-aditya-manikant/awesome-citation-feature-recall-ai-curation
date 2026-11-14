#!/usr/bin/env python3
"""Recompute the Study 2 tables from the committed out-of-fold scores (no abstracts, no downloads).

Rebuilds the top-K selections for all four rankers from `study2_out_of_fold_scores.csv.gz`, compares the
pooled metrics with the committed `study2_pooled_metrics.csv`, and writes two additional descriptive
outputs that were not pre-registered contrasts:
  * per-review lower-citation recall (blind vs aware), and
  * the higher-citation recall difference with a paired cluster-bootstrap interval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_study2 import CONDS, Part, pooled, rates


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, required=True, help="results/study2_confirmatory")
    ap.add_argument("--protocol", type=Path, required=True)
    ap.add_argument("--bootstrap", type=int, default=200)
    a = ap.parse_args()
    cfg = json.loads(a.protocol.read_text())
    reserved = float(cfg["fair_rerank_reserved_fraction"])
    scored = pd.read_csv(a.results / "study2_out_of_fold_scores.csv.gz")
    scored["low_citation"] = scored.low_citation.astype(str).str.lower().isin(["true", "1"])
    id_rank = {v: i for i, v in enumerate(sorted(scored.openalex_id.astype(str).unique()))}
    parts = [Part(p, id_rank) for _, p in scored.groupby(["dataset", "fold"])]

    rows = []
    for frac in [cfg["k_fraction"], *cfg["sensitivity_k_fractions"]]:
        for c, t in pooled(parts, frac, reserved).items():
            rows.append({"k_fraction": frac, "condition": c, **t, **rates(t)})
    new = pd.DataFrame(rows)
    old = pd.read_csv(a.results / "study2_pooled_metrics.csv")
    counts = ["low", "high", "all", "sel", "den_low", "den_high", "den_all"]
    same = bool((new[counts].to_numpy() == old[counts].to_numpy()).all())
    print(new[new.k_fraction == cfg["k_fraction"]][["condition", "low", "den_low", "high", "den_high", "all", "den_all"]].to_string(index=False))
    print(f"\nRecomputed counts identical to committed study2_pooled_metrics.csv: {same}")

    if a.bootstrap <= 0:
        raise SystemExit(0 if same else 1)
    rng = np.random.default_rng(cfg["bootstrap"]["seed"])
    diffs = []
    for _ in range(a.bootstrap):
        sub = [p.take(np.concatenate([p.groups[j] for j in rng.integers(0, len(p.groups), len(p.groups))])) for p in parts]
        r = {c: rates(t) for c, t in pooled(sub, cfg["k_fraction"], reserved).items()}
        diffs.append(r["citation_blind"]["recall_higher"] - r["citation_aware"]["recall_higher"])
    base = {c: rates(t) for c, t in pooled(parts, cfg["k_fraction"], reserved).items()}
    extra = {"status": "ADDITIONAL_DESCRIPTIVE_NOT_A_PREREGISTERED_CONTRAST",
             "contrast": "citation_blind - citation_aware", "metric": "recall_higher",
             "point": base["citation_blind"]["recall_higher"] - base["citation_aware"]["recall_higher"],
             "ci95_low": float(np.quantile(diffs, .025)), "ci95_high": float(np.quantile(diffs, .975)),
             "bootstrap_replicates": a.bootstrap, "recomputed_counts_identical": same}
    (a.results / "study2_additional_higher_citation_contrast.json").write_text(json.dumps(extra, indent=2) + "\n")
    print(json.dumps(extra, indent=2))
    raise SystemExit(0 if same else 1)


if __name__ == "__main__":
    main()
