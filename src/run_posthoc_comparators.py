#!/usr/bin/env python3
"""POST-HOC comparators for Study 1 (added 10 November 2026, after the cross-fitted results were seen).

Not part of the frozen protocol. Uses only the committed cross-fitted out-of-fold predictions, so the
two pre-registered rankers are not refitted or changed. Adds two reference rankers on the same folds:

  citation_only  ranks each test fold by log(1 + citations) alone (no text, no training): how far ranking
                 by citations alone would go.
  fair_rerank    keeps the citation-aware scores but reserves a fixed share of the top-K slots for the
                 best-scoring lower-citation records: a simple mitigation.

The reserved share is fixed at 0.5 by default and was not tuned. Recall@K uses K = ceil(f * N_fold) per fold,
pooled over folds; paired differences use the same within-fold split_group_id cluster bootstrap
(2,000 replicates, seed 20261031) as the cross-fitted analysis.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

CONDS = ["citation_blind", "citation_aware", "citation_only", "fair_rerank"]
CONTRASTS = [("citation_blind", "citation_only"), ("fair_rerank", "citation_aware"), ("citation_blind", "fair_rerank")]


def select_topk(scores, ids, low, frac, reserved=None):
    n = len(scores)
    k = max(1, int(math.ceil(frac * n)))
    order = np.lexsort((ids.astype(str), -scores))
    sel = np.zeros(n, bool)
    if reserved:
        sel[order[low[order]][:int(round(reserved * k))]] = True
    for j in order:
        if sel.sum() >= k:
            break
        sel[j] = True
    return sel


def totals(parts, frac, reserved):
    out = {}
    for c in CONDS:
        t = dict(low=0, high=0, all=0, sel=0, den_low=0, den_high=0, den_all=0)
        for p in parts:
            lo = p.low_citation.to_numpy(bool)
            sel = select_topk(p[f"score_{c}"].to_numpy(), p.openalex_id.to_numpy(), lo, frac,
                              reserved if c == "fair_rerank" else None)
            y = p.label.to_numpy() == 1
            t["low"] += int((y & lo & sel).sum()); t["high"] += int((y & ~lo & sel).sum())
            t["all"] += int((y & sel).sum()); t["sel"] += int(sel.sum())
            t["den_low"] += int((y & lo).sum()); t["den_high"] += int((y & ~lo).sum()); t["den_all"] += int(y.sum())
        out[c] = t
    return out


def rates(t):
    f = lambda a, b: a / b if b else float("nan")
    return {"recall_lower": f(t["low"], t["den_low"]), "recall_higher": f(t["high"], t["den_high"]),
            "recall_overall": f(t["all"], t["den_all"]), "precision": f(t["all"], t["sel"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True, type=Path, help="crossfit_out_of_fold_predictions.csv")
    ap.add_argument("--groups", required=True, type=Path, help="CSV with openalex_id, split_group_id")
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--reserved", type=float, default=0.5)
    ap.add_argument("--bootstrap", type=int, default=2000)
    a = ap.parse_args()
    if a.output.exists() and any(a.output.iterdir()):
        raise FileExistsError(f"Output directory not empty: {a.output}")
    a.output.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(a.predictions)
    g = pd.read_csv(a.groups, usecols=["openalex_id", "split_group_id"]).drop_duplicates("openalex_id")
    df = df.merge(g, on="openalex_id", how="left", validate="one_to_one")
    if df.split_group_id.isna().any():
        raise ValueError("every prediction needs a split_group_id")
    df["low_citation"] = df.low_citation.astype(str).str.lower().isin(["true", "1"])
    df["score_citation_only"] = np.log1p(df.citations)
    df["score_fair_rerank"] = df.score_citation_aware
    parts = [p for _, p in df.groupby("fold")]

    rows = []
    for frac in (0.10, 0.20, 0.30):
        for c, t in totals(parts, frac, a.reserved).items():
            rows.append({"k_fraction": frac, "condition": c, **t, **rates(t)})
    pd.DataFrame(rows).to_csv(a.output / "posthoc_pooled_metrics.csv", index=False)

    rng = np.random.default_rng(20261031)
    clusters = [[idx.to_numpy() for _, idx in p.groupby("split_group_id").groups.items()] for p in parts]
    boot = {f"{x} - {y}": {k: [] for k in ("recall_lower", "recall_overall", "precision")} for x, y in CONTRASTS}
    for _ in range(a.bootstrap):
        sub = [df.loc[np.concatenate([cl[j] for j in rng.integers(0, len(cl), len(cl))])] for cl in clusters]
        r = {c: rates(t) for c, t in totals(sub, 0.20, a.reserved).items()}
        for x, y in CONTRASTS:
            for k in boot[f"{x} - {y}"]:
                boot[f"{x} - {y}"][k].append(r[x][k] - r[y][k])
    base = {c: rates(t) for c, t in totals(parts, 0.20, a.reserved).items()}
    con = []
    for x, y in CONTRASTS:
        for k, v in boot[f"{x} - {y}"].items():
            v = np.asarray(v, float); v = v[~np.isnan(v)]
            con.append({"contrast": f"{x} - {y}", "metric": k, "point": base[x][k] - base[y][k],
                        "ci95_low": float(np.quantile(v, .025)) if len(v) else None,
                        "ci95_high": float(np.quantile(v, .975)) if len(v) else None, "valid_replicates": int(len(v))})
    con = pd.DataFrame(con)
    con.to_csv(a.output / "posthoc_paired_contrasts.csv", index=False)
    (a.output / "posthoc_summary.json").write_text(json.dumps({
        "status": "POST_HOC_NOT_PREREGISTERED|EXPLORATORY_GATE_FAILED",
        "added_on": "2026-11-10", "reserved_fraction": a.reserved, "bootstrap_replicates": a.bootstrap,
        "bootstrap_seed": 20261031, "source_predictions": str(a.predictions.name)}, indent=2) + "\n")
    print(pd.DataFrame(rows).query("k_fraction == 0.2")[["condition", "low", "den_low", "all", "den_all",
                                                          "recall_lower", "recall_overall", "precision"]].to_string(index=False))
    print(con.to_string(index=False))


if __name__ == "__main__":
    main()
