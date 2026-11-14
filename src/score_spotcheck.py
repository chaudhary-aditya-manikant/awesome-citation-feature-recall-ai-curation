#!/usr/bin/env python3
"""Score the author's blind spot-check against the AI-only labels (Amendment A4).

Reads the returned sheet, joins the public key and the AI labels, and reports agreement, how many
records the author judged relevant or uncertain, and an exact (Clopper-Pearson) 95% interval for the
share of the 2,305 unreviewed records that the AI wrongly called not relevant.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from scipy.stats import beta

VALID = {"relevant", "not_relevant", "uncertain"}


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def score(sheet: pd.DataFrame, key: pd.DataFrame, labels: pd.DataFrame, n_unreviewed: int) -> tuple[pd.DataFrame, dict]:
    s = sheet[["check_id", "Your_Label", "Your_Rationale", "Reviewer_ID", "Review_Date"]].copy()
    s["Your_Label"] = s.Your_Label.astype(str).str.strip().str.lower().str.replace(" ", "_")
    bad = s[~s.Your_Label.isin(VALID)]
    if len(bad):
        raise ValueError(f"{len(bad)} rows without a valid Your_Label, e.g. {bad.check_id.head(5).tolist()}")
    d = s.merge(key, on="check_id", validate="one_to_one").merge(
        labels[["screening_id", "ai_label", "final_label"]], on="screening_id", validate="one_to_one")
    n = len(d)
    agree = int((d.Your_Label == d.final_label).sum())
    rel = int((d.Your_Label == "relevant").sum()); unc = int((d.Your_Label == "uncertain").sum())
    lo, hi = clopper_pearson(rel, n)
    summary = {
        "amendment": "A4 blind spot-check of AI-only labels", "sample_seed": 20261110, "n_checked": n,
        "agreement_with_ai": agree, "agreement_rate": agree / n,
        "author_relevant": rel, "author_uncertain": unc,
        "missed_relevant_rate": rel / n, "missed_relevant_rate_ci95": [lo, hi],
        "estimated_missed_relevant_in_unreviewed": [round(lo * n_unreviewed, 1), round(rel / n * n_unreviewed, 1),
                                                    round(hi * n_unreviewed, 1)],
        "n_unreviewed": n_unreviewed,
    }
    return d, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", type=Path, required=True)
    ap.add_argument("--key", type=Path, required=True)
    ap.add_argument("--labels", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    labels = pd.read_csv(a.labels)
    d, summary = score(pd.read_excel(a.sheet, sheet_name="Spotcheck"), pd.read_csv(a.key), labels,
                       int((labels.label_source == "ai_provisional_not_reviewed").sum()))
    a.output.mkdir(parents=True, exist_ok=True)
    d.to_csv(a.output / "spotcheck_decisions.csv", index=False)  # no abstracts: safe to commit
    (a.output / "spotcheck_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
