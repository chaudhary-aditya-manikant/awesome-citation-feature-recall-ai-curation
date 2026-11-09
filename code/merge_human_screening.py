#!/usr/bin/env python3
"""Import blinded human-screening decisions without promoting them to gold labels.

This tool validates the completed Batch_Bxx sheets against the private queue.
It never invents labels, silently resolves uncertainty, or declares the dataset
ready for model fitting. It writes an import ledger and, only after every first-
pass row is labelled, a deterministic 20% single-reviewer consistency-audit ID
sample (plus every uncertain row).

Example:
python code/merge_human_screening.py \
  --workbook 06_Balanced_Collection_Audit_20261031/workbooks/AITR_Balanced_Human_Screening_Workbook_Blinded.xlsx \
  --queue 06_Balanced_Collection_Audit_20261031/data/private/candidate_pool_human_screening_queue_private.csv \
  --output-dir data/human_review_import
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

LABEL_MAP = {"1": 1, "0": 0, "uncertain": "uncertain"}
CONFIDENCE = {"high", "medium", "low"}
REQUIRED_WORKBOOK_COLUMNS = {
    "Screening_ID", "Human_Relevance_Label", "Rationale", "Confidence",
    "Reviewer_ID", "Review_Date", "Second_Screen_Label",
    "Adjudication_Notes", "Adjudicated_Label",
}


def _clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_label(value):
    raw = _clean_text(value).lower()
    if raw == "":
        return None
    if raw in LABEL_MAP:
        return LABEL_MAP[raw]
    # Excel may return numeric cells as floats.
    if raw in {"1.0", "0.0"}:
        return int(float(raw))
    raise ValueError(f"Unsupported label {value!r}; use 1, 0, uncertain, or blank")


def load_batch_decisions(workbook_path: Path) -> pd.DataFrame:
    """Read only Batch_Bxx sheets; instructions/index sheets are excluded."""
    xls = pd.ExcelFile(workbook_path)
    batch_sheets = sorted(s for s in xls.sheet_names if s.startswith("Batch_B"))
    if not batch_sheets:
        raise ValueError("No Batch_Bxx worksheets found in screening workbook")
    pieces = []
    for sheet_name in batch_sheets:
        part = pd.read_excel(workbook_path, sheet_name=sheet_name, dtype={"Screening_ID": str})
        missing = REQUIRED_WORKBOOK_COLUMNS - set(part.columns)
        if missing:
            raise ValueError(f"{sheet_name} is missing required columns: {sorted(missing)}")
        part["Batch_Sheet"] = sheet_name
        pieces.append(part)
    decisions = pd.concat(pieces, ignore_index=True)
    decisions["Screening_ID"] = decisions["Screening_ID"].map(_clean_text)
    if decisions["Screening_ID"].eq("").any():
        raise ValueError("Blank Screening_ID found in workbook")
    if decisions["Screening_ID"].duplicated().any():
        dupes = decisions.loc[decisions["Screening_ID"].duplicated(False), "Screening_ID"].tolist()[:10]
        raise ValueError(f"Duplicate Screening_ID values in workbook: {dupes}")
    return decisions


def validate_against_queue(decisions: pd.DataFrame, queue: pd.DataFrame) -> dict:
    if "screening_id" not in queue.columns:
        raise ValueError("Queue file must contain screening_id")
    expected = set(queue["screening_id"].dropna().astype(str).str.strip())
    observed = set(decisions["Screening_ID"])
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    if missing or unexpected:
        raise ValueError(
            f"Workbook/queue ID mismatch: missing={len(missing)} unexpected={len(unexpected)}; "
            f"missing examples={missing[:5]}, unexpected examples={unexpected[:5]}"
        )

    first_labels = []
    adjudicated = []
    invalid_confidence = []
    incomplete_decision_rows = []
    for row in decisions.itertuples(index=False):
        first = normalize_label(getattr(row, "Human_Relevance_Label"))
        final = normalize_label(getattr(row, "Adjudicated_Label"))
        first_labels.append(first)
        adjudicated.append(final)
        if first is not None:
            confidence = _clean_text(getattr(row, "Confidence")).lower()
            required_meta = {
                "Rationale": _clean_text(getattr(row, "Rationale")),
                "Confidence": confidence if confidence in CONFIDENCE else "",
                "Reviewer_ID": _clean_text(getattr(row, "Reviewer_ID")),
                "Review_Date": _clean_text(getattr(row, "Review_Date")),
            }
            if not all(required_meta.values()):
                incomplete_decision_rows.append(_clean_text(getattr(row, "Screening_ID")))
            if confidence and confidence not in CONFIDENCE:
                invalid_confidence.append((_clean_text(getattr(row, "Screening_ID")), confidence))
        if final is not None and first is None:
            raise ValueError(
                f"Adjudicated_Label supplied before first-pass label for "
                f"{_clean_text(getattr(row, 'Screening_ID'))}"
            )

    n_first = sum(x is not None for x in first_labels)
    n_final = sum(x is not None for x in adjudicated)
    n_uncertain = sum(x == "uncertain" for x in first_labels)
    n_binary = sum(x in {0, 1} for x in first_labels)
    return {
        "queue_records": len(expected),
        "workbook_records": len(decisions),
        "first_pass_labelled": n_first,
        "first_pass_missing": len(decisions) - n_first,
        "first_pass_binary": n_binary,
        "first_pass_uncertain": n_uncertain,
        "adjudicated_labelled": n_final,
        "adjudicated_missing": len(decisions) - n_final,
        "incomplete_decision_metadata_records": len(incomplete_decision_rows),
        "incomplete_decision_metadata_examples": incomplete_decision_rows[:20],
        "invalid_confidence_values": invalid_confidence[:20],
        "id_coverage_exact": True,
        "final_dataset_ready": False,
        "reason": "Import validation is not human adjudication or a passed dataset preflight.",
    }


def create_rescreen_sample(decisions: pd.DataFrame, seed: int = 20261030) -> pd.DataFrame:
    """Select all uncertain + seeded 20% of binary first-pass decisions."""
    first = decisions["Human_Relevance_Label"].map(normalize_label)
    uncertain = decisions.loc[first.eq("uncertain")].copy()
    decided = decisions.loc[first.isin([0, 1])].copy()
    sample_n = int(math.ceil(0.20 * len(decided)))
    if sample_n:
        rng = np.random.default_rng(seed)
        chosen_idx = rng.choice(decided.index.to_numpy(), size=sample_n, replace=False)
        selected = decisions.loc[chosen_idx].copy()
    else:
        selected = decisions.iloc[0:0].copy()
    out = pd.concat([selected.assign(Rescreen_Reason="seeded_20pct_of_decided"),
                     uncertain.assign(Rescreen_Reason="all_uncertain")], ignore_index=True)
    out = out.drop_duplicates("Screening_ID").sort_values("Screening_ID")
    keep = [c for c in ["Screening_ID", "Title", "Abstract", "Human_Relevance_Label", "Rescreen_Reason"] if c in out.columns]
    return out[keep]


def run(workbook_path: Path, queue_path: Path, output_dir: Path, seed: int = 20261030) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    decisions = load_batch_decisions(workbook_path)
    queue = pd.read_csv(queue_path, dtype={"screening_id": str})
    report = validate_against_queue(decisions, queue)

    # Keep raw workbook decisions in an explicit import ledger; do not convert
    # AI suggestions or incomplete human rows into a model label.
    decisions.to_csv(output_dir / "human_screening_decisions_imported.csv", index=False)
    report["rescreen_seed"] = seed
    report["rescreen_sample_created"] = False
    if report["first_pass_missing"] == 0 and report["incomplete_decision_metadata_records"] == 0:
        rescreen = create_rescreen_sample(decisions, seed=seed)
        rescreen.to_csv(output_dir / "single_reviewer_rescreen_sample.csv", index=False)
        report["rescreen_sample_created"] = True
        report["rescreen_sample_records"] = len(rescreen)
        report["rescreen_sample_decided_20pct"] = int((rescreen.Rescreen_Reason == "seeded_20pct_of_decided").sum())
        report["rescreen_sample_uncertain"] = int((rescreen.Rescreen_Reason == "all_uncertain").sum())
    else:
        report["rescreen_sample_records"] = 0
        report["rescreen_note"] = "Complete every first-pass decision and metadata field before generating the consistency-audit sample."

    (output_dir / "screening_import_validation.json").write_text(json.dumps(report, indent=2))
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbook", type=Path, required=True)
    ap.add_argument("--queue", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--rescreen-seed", type=int, default=20261030)
    args = ap.parse_args()
    report = run(args.workbook, args.queue, args.output_dir, args.rescreen_seed)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
