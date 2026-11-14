#!/usr/bin/env python3
"""Study 2: confirmatory citation-feature test on the SYNERGY benchmark.

Within each dataset, five StratifiedGroupKFold folds (seed 20261030) are each used once as
the test fold. Four conditions are scored on every test fold:
  citation_blind  - Study 1 model without the citation feature
  citation_aware  - Study 1 model with standardised log(1 + citations)
  citation_only   - ranks by log(1 + citations) alone (no training)
  fair_rerank     - citation_aware scores, with a reserved share of top-K slots for
                    lower-citation records (share fixed in the protocol)
Recall@K uses K = ceil(f * N_fold) per fold and is pooled over folds and datasets.
Paired differences are bootstrapped by resampling split_group_id clusters within
dataset x fold. The run refuses to start while the protocol contains DECIDE values.
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

from run_experiment import make_pipeline

CONDS = ["citation_blind", "citation_aware", "citation_only", "fair_rerank"]
REQUIRED = {"dataset", "openalex_id", "title", "abstract", "year", "citations", "label", "split_group_id"}
def undecided(cfg) -> list[str]:
    """Paths of protocol values the author has not yet decided (strings starting with DECIDE)."""
    out = []
    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                if not k.startswith("_"):
                    walk(v, f"{path}.{k}" if path else k)
        elif isinstance(x, str) and x.startswith("DECIDE"):
            out.append(path)
    walk(cfg, "")
    return out


CONTRASTS = [("citation_blind", "citation_aware"),   # primary (H1)
             ("fair_rerank", "citation_aware"),      # H2: does the simple fix recover recall?
             ("citation_blind", "citation_only")]


def load_protocol(path: Path) -> dict:
    cfg = json.loads(path.read_text())
    todo = undecided(cfg)
    if todo:
        raise SystemExit(f"Protocol not frozen; the author must decide: {todo}")
    return cfg


def select_topk(scores: np.ndarray, ids: np.ndarray, low: np.ndarray, frac: float,
                reserved: float | None = None) -> np.ndarray:
    """Boolean top-K mask; ties broken by id. With `reserved`, the best-scoring
    lower-citation records fill round(reserved*K) slots first."""
    n = len(scores)
    k = max(1, int(math.ceil(frac * n)))
    tie = ids if np.issubdtype(np.asarray(ids).dtype, np.integer) else np.asarray(ids).astype(str)
    order = np.lexsort((tie, -scores))
    sel = np.zeros(n, bool)
    if reserved:
        sel[order[low[order]][:int(round(reserved * k))]] = True
    rest = order[~sel[order]][:max(0, k - int(sel.sum()))]
    sel[rest] = True
    return sel


def load(path: Path, min_incl: int) -> pd.DataFrame:
    df = pd.read_csv(path)
    miss = REQUIRED - set(df.columns)
    if miss:
        raise ValueError(f"Missing columns: {sorted(miss)}")
    df = df.dropna(subset=["year", "citations", "label"]).copy()
    df["title"] = df.title.fillna("").astype(str)
    df["abstract"] = df.abstract.fillna("").astype(str)
    df["openalex_id"] = df.openalex_id.astype(str)
    if df.duplicated(["dataset", "openalex_id"]).any():
        raise ValueError("duplicate openalex_id within a dataset")
    if not set(df.label.unique()) <= {0, 1}:
        raise ValueError("labels must be 0/1")
    keep = df.groupby("dataset").label.transform("sum") >= min_incl
    return df[keep].reset_index(drop=True)


def score_dataset(d: pd.DataFrame, snapshot_year: int, seed: int) -> pd.DataFrame:
    d = d.copy()
    d["citation_rate"] = d.citations / np.maximum(1, snapshot_year - d.year + 1)
    d["low_citation"] = d.citation_rate <= d.citation_rate.median()
    d["text"] = (d.title + " " + d.abstract).str.strip()
    d["log_citations"] = np.log1p(d.citations)
    d["fold"] = -1
    skf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
    for i, (tr, te) in enumerate(skf.split(d, d.label, groups=d.split_group_id)):
        assert not set(d.split_group_id.iloc[tr]) & set(d.split_group_id.iloc[te])
        d.loc[d.index[te], "fold"] = i
        train, test = d.iloc[tr], d.iloc[te]
        for cond, use_c in (("citation_blind", False), ("citation_aware", True)):
            m = make_pipeline(use_c, seed).fit(train, train.label.to_numpy())
            d.loc[test.index, f"score_{cond}"] = m.predict_proba(test)[:, 1]
    d["score_citation_only"] = d.log_citations
    d["score_fair_rerank"] = d.score_citation_aware
    return d


class Part:
    """One dataset x fold test set as numpy arrays (fast to resample)."""
    def __init__(self, df: pd.DataFrame, id_rank: dict):
        self.scores = {c: df[f"score_{c}"].to_numpy(float) for c in CONDS}
        self.ids = df.openalex_id.map(id_rank).to_numpy(np.int64)
        self.low = df.low_citation.to_numpy(bool)
        self.y = df.label.to_numpy() == 1
        self.groups = [np.asarray(v) for v in pd.Series(np.arange(len(df))).groupby(df.split_group_id.to_numpy()).groups.values()]

    def take(self, idx: np.ndarray) -> "Part":
        q = object.__new__(Part)
        q.scores = {c: s[idx] for c, s in self.scores.items()}
        q.ids, q.low, q.y, q.groups = self.ids[idx], self.low[idx], self.y[idx], None
        return q


def part_hits(p: "Part", cond: str, frac: float, reserved: float) -> dict:
    sel = select_topk(p.scores[cond], p.ids, p.low, frac, reserved if cond == "fair_rerank" else None)
    y, lo = p.y, p.low
    return {"low": int((y & lo & sel).sum()), "high": int((y & ~lo & sel).sum()),
            "all": int((y & sel).sum()), "sel": int(sel.sum()),
            "den_low": int((y & lo).sum()), "den_high": int((y & ~lo).sum()), "den_all": int(y.sum())}


def pooled(parts, frac, reserved) -> dict:
    out = {}
    for c in CONDS:
        tot = {}
        for p in parts:
            for k, v in part_hits(p, c, frac, reserved).items():
                tot[k] = tot.get(k, 0) + v
        out[c] = tot
    return out


def rates(t: dict) -> dict:
    f = lambda a, b: a / b if b else float("nan")
    return {"recall_lower": f(t["low"], t["den_low"]), "recall_higher": f(t["high"], t["den_high"]),
            "recall_overall": f(t["all"], t["den_all"]), "precision": f(t["all"], t["sel"])}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--protocol", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--bootstrap", type=int, default=None)
    a = ap.parse_args()
    cfg = load_protocol(a.protocol)
    if a.output.exists() and any(a.output.iterdir()):
        raise FileExistsError(f"Output directory not empty: {a.output}")
    a.output.mkdir(parents=True, exist_ok=True)
    seed, bseed = cfg["split"]["seed"], cfg["bootstrap"]["seed"]
    reps = a.bootstrap or cfg["bootstrap"]["replicates"]
    reserved = float(cfg["fair_rerank_reserved_fraction"])
    snap_year = pd.Timestamp(cfg["data"]["citation_snapshot_date"]).year
    manifest = a.input.parent / "synergy_manifest.json"
    if manifest.exists():
        ref = json.loads(manifest.read_text()).get("citation_reference_year")
        if ref and int(ref) != snap_year:
            print(f"Citation counts refer to {ref} (see manifest), not {snap_year}: using {ref} for the age adjustment.")
            snap_year = int(ref)

    df = load(a.input, int(cfg["data"]["min_inclusions_per_dataset"]))
    scored = pd.concat([score_dataset(d, snap_year, seed) for _, d in df.groupby("dataset")], ignore_index=True)
    id_rank = {v: i for i, v in enumerate(sorted(scored.openalex_id.astype(str).unique()))}
    parts = [Part(p, id_rank) for _, p in scored.groupby(["dataset", "fold"])]

    rows = []
    for frac in [cfg["k_fraction"], *cfg["sensitivity_k_fractions"]]:
        for c, t in pooled(parts, frac, reserved).items():
            rows.append({"k_fraction": frac, "condition": c, **t, **rates(t)})
    metrics = pd.DataFrame(rows)
    metrics.to_csv(a.output / "study2_pooled_metrics.csv", index=False)

    per_ds = []
    for name, d in scored.groupby("dataset"):
        for c, t in pooled([Part(p, id_rank) for _, p in d.groupby("fold")], cfg["k_fraction"], reserved).items():
            per_ds.append({"dataset": name, "condition": c, **t, **rates(t)})
    pd.DataFrame(per_ds).to_csv(a.output / "study2_per_dataset.csv", index=False)

    base = pooled(parts, cfg["k_fraction"], reserved)
    gate = cfg["gate"]
    gate_pass = (base["citation_blind"]["den_low"] >= int(gate["min_relevant_lower_citation"]) and
                 base["citation_blind"]["den_high"] >= int(gate["min_relevant_higher_citation"]))

    rng = np.random.default_rng(bseed)
    boot = {f"{x}-{y}": {"lower": [], "overall": [], "precision": []} for x, y in CONTRASTS}
    for _ in range(reps):
        sub = []
        for p in parts:
            pick = rng.integers(0, len(p.groups), len(p.groups))
            sub.append(p.take(np.concatenate([p.groups[j] for j in pick])))
        r = {c: rates(t) for c, t in pooled(sub, cfg["k_fraction"], reserved).items()}
        for x, y in CONTRASTS:
            b = boot[f"{x}-{y}"]
            b["lower"].append(r[x]["recall_lower"] - r[y]["recall_lower"])
            b["overall"].append(r[x]["recall_overall"] - r[y]["recall_overall"])
            b["precision"].append(r[x]["precision"] - r[y]["precision"])

    point = {c: rates(t) for c, t in base.items()}
    con = []
    for x, y in CONTRASTS:
        for m, key in (("lower", "recall_lower"), ("overall", "recall_overall"), ("precision", "precision")):
            v = np.array(boot[f"{x}-{y}"][m], float)
            v = v[~np.isnan(v)]
            con.append({"contrast": f"{x} - {y}", "metric": key, "point": point[x][key] - point[y][key],
                        "ci95_low": float(np.quantile(v, .025)) if len(v) else None,
                        "ci95_high": float(np.quantile(v, .975)) if len(v) else None,
                        "valid_replicates": int(len(v))})
    con = pd.DataFrame(con)
    con.to_csv(a.output / "study2_paired_contrasts.csv", index=False)

    prim = con[(con.contrast == "citation_blind - citation_aware") & (con.metric == "recall_lower")].iloc[0]
    prec = con[(con.contrast == "citation_blind - citation_aware") & (con.metric == "precision")].iloc[0]
    max_loss = float(cfg["success_rule"]["max_overall_precision_loss_of_blind"])
    h1 = bool(gate_pass and prim.ci95_low is not None and prim.point > 0 and prim.ci95_low > 0 and -prec.point <= max_loss)
    summary = {
        "status": "CONFIRMATORY" if gate_pass else "GATE_FAILED_EXPLORATORY",
        "gate_pass": gate_pass, "H1_supported": h1,
        "relevant_lower": base["citation_blind"]["den_low"], "relevant_higher": base["citation_blind"]["den_high"],
        "datasets": int(scored.dataset.nunique()), "records": int(len(scored)), "relevant": int(scored.label.sum()),
        "input_sha256": hashlib.sha256(a.input.read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256(a.protocol.read_bytes()).hexdigest(),
        "bootstrap_replicates": reps, "citation_reference_year": int(snap_year),
    }
    (a.output / "study2_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    scored.drop(columns=["text", "abstract"]).to_csv(a.output / "study2_out_of_fold_scores.csv", index=False)
    print(metrics[metrics.k_fraction == cfg["k_fraction"]].to_string(index=False))
    print(con.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
