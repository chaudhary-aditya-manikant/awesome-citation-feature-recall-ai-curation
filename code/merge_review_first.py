#!/usr/bin/env python3
"""Merge the review-first sheet into a model input with per-record label provenance.

Rows where the reviewer filled Your_Label use that label with
label_status=single_reviewer_audited; all other rows keep the AI-provisional label
(label_status=ai_provisional). Records labelled uncertain by the final source are
excluded from the binary model input and listed in the summary.

Usage:
  python code/merge_review_first.py --sheet <AITR_Review_First_Sheet.xlsx> \
      --ai-labels data/ai_provisional_20261105/ai_provisional_screening_labels.csv \
      --queue 06_Balanced_Collection_Audit_20261031/data/private/candidate_pool_human_screening_queue_private.csv \
      --out 06_Balanced_Collection_Audit_20261031/data/private/model_input_reviewed.csv
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

SHEETS = ["1_Must_Check", "2_Borderline", "3_Skim_Titles"]
VALID = {"relevant", "not_relevant", "uncertain"}


def read_reviews(path: Path) -> pd.DataFrame:
    frames = []
    for s in SHEETS:
        df = pd.read_excel(path, sheet_name=s, dtype=str)
        df["sheet"] = s
        frames.append(df)
    r = pd.concat(frames, ignore_index=True)
    r["Your_Label"] = r["Your_Label"].fillna("").str.strip().str.lower()
    bad = sorted(set(r.Your_Label) - VALID - {""})
    if bad:
        raise ValueError(f"Invalid Your_Label values: {bad}")
    if r.Screening_ID.duplicated().any():
        raise ValueError("Duplicate Screening_ID in review sheet")
    return r


def merge(sheet: Path, ai_labels: Path, queue: Path) -> tuple[pd.DataFrame, dict]:
    r = read_reviews(sheet)
    ai = pd.read_csv(ai_labels)
    m = ai.merge(r[["Screening_ID", "Your_Label", "Your_Rationale", "Reviewer_ID", "sheet"]],
                 left_on="screening_id", right_on="Screening_ID", how="left")
    checked = m.Your_Label.fillna("").ne("")
    m["final_label"] = m.ai_label.where(~checked, m.Your_Label)
    m["label_status"] = "ai_provisional"
    m.loc[checked, "label_status"] = "single_reviewer_audited"
    q = pd.read_csv(queue, low_memory=False)
    q = q.drop(columns=[c for c in ("label", "label_status", "final_label", "ai_label") if c in q.columns])
    full = q.merge(m[["screening_id", "final_label", "label_status", "ai_label"]], on="screening_id", how="inner")
    dec = full[full.final_label.isin(["relevant", "not_relevant"])].copy()
    dec["label"] = (dec.final_label == "relevant").astype(int)
    cols = ["openalex_id", "title", "abstract", "year", "citations", "metadata_language", "label",
            "label_status", "split_group_id", "language_verification_status", "screening_id"]
    changed = m[checked & m.Your_Label.ne(m.ai_label)]
    summary = {
        "records_in_queue": int(len(m)), "records_checked_by_reviewer": int(checked.sum()),
        "checked_by_sheet": m[checked].sheet.value_counts().to_dict(),
        "reviewer_changed_ai_label": int(len(changed)),
        "changes": changed[["screening_id", "ai_label", "Your_Label"]].to_dict("records"),
        "final_relevant": int(dec.label.sum()), "final_decided": int(len(dec)),
        "excluded_uncertain": int((full.final_label == "uncertain").sum()),
        "label_status_counts": dec.label_status.value_counts().to_dict(),
    }
    return dec[cols], summary


def main() -> None:
    ap = argparse.ArgumentParser()
    for a in ("--sheet", "--ai-labels", "--queue", "--out"):
        ap.add_argument(a, required=True, type=Path)
    args = ap.parse_args()
    dec, summary = merge(args.sheet, args.ai_labels, args.queue)
    dec.to_csv(args.out, index=False)
    args.out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
