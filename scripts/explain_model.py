#!/usr/bin/env python3
"""Show the model working, step by step, on one test fold (for the viva).

    python scripts/explain_model.py --data data/private/model_input_reviewed_20261105_private.csv

Uses exactly the same code as the study (make_pipeline from src/run_experiment.py, same seed, same folds),
but on one fold only and with printed explanations:
  1. the data and the fold;
  2. the two rankers and what each one can see;
  3. what each ranker learned, including the weight it puts on citations;
  4. where the rarely cited relevant papers of this fold land in each ranking;
  5. a what-if: the same paper with 100 citations instead of 0 (illustration only).
The ranks printed in step 4 equal those in results/run_20261105_reviewed_crossfit/crossfit_relevant_records_ranks.csv.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from run_experiment import load_and_validate, make_pipeline  # noqa: E402

SEED, SNAPSHOT_YEAR = 20261030, 2026


def ranks(scores: np.ndarray, ids: np.ndarray) -> np.ndarray:
    """Rank 1 = highest score; ties broken by id (as in the study)."""
    order = np.lexsort((ids.astype(str), -scores))
    r = np.empty(len(scores), int)
    r[order] = np.arange(1, len(scores) + 1)
    return r


def line(t: str = "") -> None:
    print("\n" + "=" * 78 + (f"\n{t}\n" + "=" * 78 if t else ""))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--fold", type=int, default=2, help="test fold to show (fold 2 holds 3 of the 7 papers)")
    a = ap.parse_args()

    line("STEP 1. The data")
    df = load_and_validate(a.data, allow_ai_provisional=True)
    df["citation_rate"] = df.citations / np.maximum(1, SNAPSHOT_YEAR - df.year + 1)
    df["low_citation"] = df.citation_rate <= df.citation_rate.median()
    df["text"] = (df.title + " " + df.abstract).str.strip()
    df["log_citations"] = np.log1p(df.citations)
    print(f"{len(df):,} papers, {int(df.label.sum())} relevant "
          f"({int((df.label.eq(1) & df.low_citation).sum())} of them rarely cited).")
    print("Each paper has: title + abstract (text), publication year, citation count, and a label (relevant or not).")

    folds = list(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
                 .split(df, df.label, groups=df.split_group_id))
    tr, te = folds[a.fold]
    train, test = df.iloc[tr], df.iloc[te]
    k = math.ceil(0.20 * len(test))
    print(f"\nFive folds, seed {SEED}. Showing fold {a.fold}: train on {len(train):,} papers, "
          f"test on {len(test)} papers.")
    print(f"A reviewer reads the top 20% of the test queue: K = ceil(0.2 x {len(test)}) = {k} papers.")
    print(f"No paper group appears in both train and test: "
          f"{not set(train.split_group_id) & set(test.split_group_id)}")

    line("STEP 2. Two rankers: identical except for ONE feature")
    models = {}
    for name, use_c in (("citation_blind", False), ("citation_aware", True)):
        m = make_pipeline(use_c, SEED).fit(train, train.label.to_numpy())
        models[name] = m
        feats = "TF-IDF words of title+abstract, year" + (", log(1 + citations)" if use_c else "")
        print(f"{name:15s} sees: {feats}")
    print("Both are scikit-learn pipelines: TfidfVectorizer + StandardScaler -> LogisticRegression (C=1, balanced).")

    line("STEP 3. What the rankers learned")
    aware = models["citation_aware"]
    names = aware.named_steps["features"].get_feature_names_out()
    coef = aware.named_steps["model"].coef_[0]
    w = dict(zip(names, coef))
    print(f"Weight on log(1 + citations) in the citation-aware ranker: {w['numeric__log_citations']:+.3f}")
    print("  A positive weight means: more citations -> higher score -> higher in the queue.")
    print(f"Weight on publication year: {w['numeric__year']:+.3f}")
    text = [(n.replace("text__", ""), c) for n, c in zip(names, coef) if n.startswith("text__")]
    top = sorted(text, key=lambda x: -x[1])[:10]
    print("Words that most increase the relevance score (both rankers learn similar words):")
    print("  " + ", ".join(f"'{t}'" for t, _ in top))

    line(f"STEP 4. Where the rarely cited relevant papers of fold {a.fold} land")
    ids = test.openalex_id.to_numpy()
    r = {n: ranks(m.predict_proba(test)[:, 1], ids) for n, m in models.items()}
    sel = test.label.eq(1).to_numpy() & test.low_citation.to_numpy()
    rows = test.loc[sel, ["screening_id", "year", "citations"]].copy()
    rows["rank_blind"] = r["citation_blind"][sel]
    rows["rank_aware"] = r["citation_aware"][sel]
    rows["read_by_reviewer?"] = [("yes" if b <= k else "NO") + " -> " + ("yes" if c <= k else "NO")
                                 for b, c in zip(rows.rank_blind, rows.rank_aware)]
    print(rows.sort_values("rank_blind").to_string(index=False))
    print(f"\n(rank 1 = top of the queue; the reviewer stops after rank {k})")
    for n, col in (("citation_blind", "rank_blind"), ("citation_aware", "rank_aware")):
        print(f"{n:15s}: {int((rows[col] <= k).sum())} of {len(rows)} rarely cited relevant papers in the top {k}")

    line("STEP 5. What-if (illustration, not part of the study)")
    worst = rows.sort_values("rank_aware").iloc[-1]
    one = test[test.screening_id == worst.screening_id].copy()
    print(f"Take {worst.screening_id}: {int(worst.citations)} citations, rank {int(worst.rank_aware)} "
          "under the citation-aware ranker.")
    for c in (0, 10, 100):
        x = test.copy()
        x.loc[one.index, "citations"] = c
        x["log_citations"] = np.log1p(x.citations)
        rk = ranks(aware.predict_proba(x)[:, 1], ids)[test.index.get_indexer(one.index)][0]
        print(f"  same text, {c:>3d} citations -> rank {rk}")
    print("Only the citation count changed; the text did not. That is the bias the study measures.")


if __name__ == "__main__":
    main()
