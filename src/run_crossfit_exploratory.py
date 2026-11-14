#!/usr/bin/env python3
"""Exploratory cross-fitted citation-feature ablation (Protocol Amendment A3).

Uses the same five StratifiedGroupKFold folds as the frozen runner (seed 20261030).
Each fold serves once as the test fold; the other four folds are the training data.
Both conditions (citation-blind and citation-aware) use the frozen pipeline from
run_experiment.py. Recall@K is computed within each fold with K = ceil(f * N_fold)
and pooled across folds. The paired difference is bootstrapped by resampling
split_group_id clusters within folds.

All outputs are exploratory. They are not a substitute for the frozen
confirmatory analysis, which requires the dataset gate to pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from run_experiment import load_and_validate, make_pipeline

CONDITIONS = [("citation_blind", False), ("citation_aware", True)]


def topk_mask(scores: np.ndarray, ids: np.ndarray, fraction: float) -> np.ndarray:
    k = max(1, int(math.ceil(fraction * len(scores))))
    sel = np.zeros(len(scores), dtype=bool)
    sel[np.lexsort((ids.astype(str), -scores))[:k]] = True
    return sel


def pooled(df: pd.DataFrame, cond: str, fraction: float, mask: pd.Series | None = None) -> dict:
    hits = rel = selected = selected_rel = 0
    for _, part in df.groupby("fold"):
        sel = topk_mask(part[f"score_{cond}"].to_numpy(), part.openalex_id.to_numpy(), fraction)
        y = part.label.to_numpy() == 1
        m = np.ones(len(part), bool) if mask is None else mask.loc[part.index].to_numpy(bool)
        hits += int(np.sum(y & m & sel)); rel += int(np.sum(y & m))
        selected += int(sel.sum()); selected_rel += int(np.sum(y & sel))
    return {"relevant_in_topk": hits, "relevant": rel,
            "recall_at_k": hits / rel if rel else float("nan"),
            "precision_at_k": selected_rel / selected if selected else float("nan")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--snapshot-date", required=True)
    ap.add_argument("--seed", type=int, default=20261030)
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--allow-ai-provisional-labels", action="store_true")
    args = ap.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)

    df = load_and_validate(args.input, allow_ai_provisional=args.allow_ai_provisional_labels)
    ai_provisional = bool((df.label_status.str.lower() == "ai_provisional").any())
    snapshot_year = pd.Timestamp(args.snapshot_date).year
    df["citation_rate"] = df.citations / np.maximum(1, snapshot_year - df.year + 1)
    median = float(df.citation_rate.median())
    df["low_citation"] = df.citation_rate <= median
    df["text"] = (df.title + " " + df.abstract).str.strip()
    df["log_citations"] = np.log1p(df.citations)

    folds = list(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=args.seed)
                 .split(df, df.label, groups=df.split_group_id))
    df["fold"] = -1
    for i, (_, te) in enumerate(folds):
        df.loc[df.index[te], "fold"] = i
    for i, (tr, te) in enumerate(folds):
        assert not set(df.split_group_id.iloc[tr]) & set(df.split_group_id.iloc[te])
        train, test = df.iloc[tr], df.iloc[te]
        for cond, use_c in CONDITIONS:
            model = make_pipeline(use_c, args.seed)
            model.fit(train, train.label.to_numpy())
            df.loc[test.index, f"score_{cond}"] = model.predict_proba(test)[:, 1]

    low, high = df.low_citation, ~df.low_citation
    rows = []
    for frac in (0.10, 0.20, 0.30):
        for cond, _ in CONDITIONS:
            for gname, gmask in (("overall", None), ("lower_citation", low), ("higher_citation", high)):
                r = pooled(df, cond, frac, gmask)
                rows.append({"k_fraction": frac, "condition": cond, "group": gname, **r})
    metrics = pd.DataFrame(rows)
    metrics.to_csv(args.output / "crossfit_pooled_metrics.csv", index=False)

    per_fold = []
    for f, part in df.groupby("fold"):
        for cond, _ in CONDITIONS:
            sel = topk_mask(part[f"score_{cond}"].to_numpy(), part.openalex_id.to_numpy(), 0.20)
            y = part.label.to_numpy() == 1
            lo = part.low_citation.to_numpy(bool)
            per_fold.append({"fold": f, "condition": cond, "N": len(part), "K": int(sel.sum()),
                             "relevant": int(y.sum()), "relevant_low": int((y & lo).sum()),
                             "relevant_high": int((y & ~lo).sum()),
                             "hits_overall": int((y & sel).sum()), "hits_low": int((y & lo & sel).sum()),
                             "hits_high": int((y & ~lo & sel).sum())})
    pd.DataFrame(per_fold).to_csv(args.output / "crossfit_per_fold.csv", index=False)

    # Paired cluster bootstrap within folds for the 20% primary contrasts.
    rng = np.random.default_rng(20261031)
    groups = {f: part for f, part in df.groupby("fold")}
    cluster_index = {f: {g: idx.to_numpy() for g, idx in part.groupby("split_group_id").groups.items()}
                     for f, part in groups.items()}
    diffs = {"lower_citation": [], "higher_citation": [], "overall": [], "precision": []}
    for _ in range(args.bootstrap):
        num = {c: {"low": 0, "high": 0, "all": 0, "sel_rel": 0, "sel": 0} for c, _ in CONDITIONS}
        den = {"low": 0, "high": 0, "all": 0}
        for f, part in groups.items():
            keys = list(cluster_index[f])
            pick = rng.choice(len(keys), size=len(keys), replace=True)
            idx = np.concatenate([cluster_index[f][keys[j]] for j in pick])
            sub = df.loc[idx]
            y = sub.label.to_numpy() == 1
            lo = sub.low_citation.to_numpy(bool)
            den["low"] += int((y & lo).sum()); den["high"] += int((y & ~lo).sum()); den["all"] += int(y.sum())
            for cond, _ in CONDITIONS:
                sel = topk_mask(sub[f"score_{cond}"].to_numpy(), sub.openalex_id.to_numpy(), 0.20)
                num[cond]["low"] += int((y & lo & sel).sum()); num[cond]["high"] += int((y & ~lo & sel).sum())
                num[cond]["all"] += int((y & sel).sum()); num[cond]["sel_rel"] += int((y & sel).sum())
                num[cond]["sel"] += int(sel.sum())
        if min(den.values()) == 0:
            continue
        a, b = num["citation_blind"], num["citation_aware"]
        diffs["lower_citation"].append(a["low"] / den["low"] - b["low"] / den["low"])
        diffs["higher_citation"].append(a["high"] / den["high"] - b["high"] / den["high"])
        diffs["overall"].append(a["all"] / den["all"] - b["all"] / den["all"])
        diffs["precision"].append(a["sel_rel"] / a["sel"] - b["sel_rel"] / b["sel"])

    def point(group, frac=0.20, metric="recall_at_k"):
        m = metrics[(metrics.k_fraction == frac) & (metrics.group == group)].set_index("condition")[metric]
        return float(m["citation_blind"] - m["citation_aware"])

    contrasts = []
    for name, group, metric in [("lower_citation_recall", "lower_citation", "recall_at_k"),
                                ("higher_citation_recall", "higher_citation", "recall_at_k"),
                                ("overall_recall", "overall", "recall_at_k"),
                                ("overall_precision", "overall", "precision_at_k")]:
        key = {"lower_citation_recall": "lower_citation", "higher_citation_recall": "higher_citation",
               "overall_recall": "overall", "overall_precision": "precision"}[name]
        d = np.asarray(diffs[key])
        contrasts.append({"contrast_blind_minus_aware": name, "point_estimate": point(group, metric=metric),
                          "ci95_low": float(np.quantile(d, 0.025)) if len(d) else None,
                          "ci95_high": float(np.quantile(d, 0.975)) if len(d) else None,
                          "valid_replicates": int(len(d))})
    pd.DataFrame(contrasts).to_csv(args.output / "crossfit_paired_contrasts.csv", index=False)

    for cond, _ in CONDITIONS:
        df[f"rank_in_fold_{cond}"] = df.groupby("fold")[f"score_{cond}"].rank(ascending=False, method="first").astype(int)
        df[f"topk20_{cond}"] = False
        for f, part in df.groupby("fold"):
            df.loc[part.index, f"topk20_{cond}"] = topk_mask(part[f"score_{cond}"].to_numpy(), part.openalex_id.to_numpy(), 0.20)
    keep = ["openalex_id", "fold", "year", "citations", "citation_rate", "low_citation", "metadata_language",
            "label", "score_citation_blind", "score_citation_aware", "rank_in_fold_citation_blind",
            "rank_in_fold_citation_aware", "topk20_citation_blind", "topk20_citation_aware"]
    df[keep].to_csv(args.output / "crossfit_out_of_fold_predictions.csv", index=False)
    pos = df[df.label == 1][keep + [c for c in ("screening_id", "ai_confidence", "label_status") if c in df.columns]]
    pos.sort_values(["low_citation", "citations"]).to_csv(args.output / "crossfit_relevant_records_ranks.csv", index=False)

    summary = {
        "status": "|".join(filter(None, ["EXPLORATORY_CROSSFIT_AMENDMENT_A3",
                                         ("MIXED_LABELS_REVIEWER_AND_AI_PROVISIONAL" if df.label_status.str.lower().nunique() > 1
                                          else "AI_PROVISIONAL_LABELS_NOT_HUMAN_VERIFIED") if ai_provisional else ""])),
        "label_status_counts": {str(k): int(v) for k, v in df.label_status.str.lower().value_counts().items()},
        "input_file_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "n_records": int(len(df)), "n_relevant": int(df.label.sum()),
        "n_relevant_lower_citation": int((df.label.eq(1) & low).sum()),
        "n_relevant_higher_citation": int((df.label.eq(1) & high).sum()),
        "citation_rate_median": median, "split_seed": args.seed, "bootstrap_seed": 20261031,
        "bootstrap_replicates_requested": args.bootstrap,
        "metadata_language_relevant_counts": df[df.label == 1].metadata_language.value_counts().to_dict(),
        "note": "Pool-relative, exploratory. The frozen dataset gate failed; no confirmatory claim is supported.",
    }
    (args.output / "crossfit_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(metrics[metrics.k_fraction == 0.20].to_string(index=False))
    print(pd.DataFrame(contrasts).to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
