#!/usr/bin/env python3
"""Apply the author's spot-check decisions (Amendment A4) to the Study 1 labels.

Only the 200 sampled records change: each takes the author's label and becomes
`single_reviewer_audited`; records the author marked `uncertain` leave the decided set, as in Study 1.
Writes a corrected public label file and (privately) a corrected model input. No other record changes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def apply(labels: pd.DataFrame, model_input: pd.DataFrame, decisions: pd.DataFrame):
    d = decisions.set_index("screening_id").Your_Label
    lab = labels.copy()
    hit = lab.screening_id.isin(d.index)
    lab.loc[hit, "final_label"] = lab.loc[hit, "screening_id"].map(d)
    lab.loc[hit, "label_source"] = "reviewer_spotcheck_20261110"
    mi = model_input.copy()
    sel = mi.screening_id.isin(d.index)
    if sel.sum() != len(d):
        raise ValueError(f"{len(d) - sel.sum()} spot-check records missing from the model input")
    new = mi.loc[sel, "screening_id"].map(d)
    mi.loc[sel, "label"] = (new == "relevant").astype(int)
    mi.loc[sel, "label_status"] = "single_reviewer_audited"
    drop = sel & (mi.screening_id.map(d) == "uncertain")
    mi = mi[~drop].reset_index(drop=True)
    summary = {
        "records_checked": int(len(d)), "changed_to_relevant": int((d == "relevant").sum()),
        "changed_to_uncertain_and_excluded": int((d == "uncertain").sum()),
        "relevant_before": int(model_input.label.sum()), "relevant_after": int(mi.label.sum()),
        "decided_before": int(len(model_input)), "decided_after": int(len(mi)),
        "label_status_after": mi.label_status.value_counts().to_dict(),
    }
    return lab, mi, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=Path, required=True)
    ap.add_argument("--model-input", type=Path, required=True, help="private model input with abstracts")
    ap.add_argument("--decisions", type=Path, required=True, help="results/spotcheck_20261110/spotcheck_decisions.csv")
    ap.add_argument("--labels-out", type=Path, required=True)
    ap.add_argument("--model-input-out", type=Path, required=True)
    a = ap.parse_args()
    lab, mi, summary = apply(pd.read_csv(a.labels), pd.read_csv(a.model_input), pd.read_csv(a.decisions))
    lab.to_csv(a.labels_out, index=False)
    mi.to_csv(a.model_input_out, index=False)
    a.labels_out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
