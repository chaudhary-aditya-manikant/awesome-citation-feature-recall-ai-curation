#!/usr/bin/env python3
"""Blind spot-check of the AI-only labels (Amendment A4, 10 November 2026).

Draws a seeded simple random sample of records that kept the AI first-pass label without author review
(label_source = ai_provisional_not_reviewed) and writes:
  * a PRIVATE Excel sheet for the author (title, abstract, year; no AI label, no citation count), and
  * a PUBLIC key (check_id -> screening_id, openalex_id) that holds no abstract text.
The sample is drawn before any review, so the error rate it measures is not chosen after the fact.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

SEED = 20261110
N = 200
CHOICES = ["relevant", "not_relevant", "uncertain"]

INSTRUCTIONS = [
    "Blind spot-check of AI-only screening labels (Amendment A4)",
    "",
    "1. For each record, read the title and abstract only. The AI's label and the citation count are hidden on purpose.",
    "2. Choose Your_Label from the dropdown: relevant / not_relevant / uncertain.",
    "3. Write a one-sentence Your_Rationale for every 'relevant' or 'uncertain' choice (optional for not_relevant).",
    "4. Fill Reviewer_ID (MNS2026008) and Review_Date on every row you label.",
    "5. Do not look up the AI label until all 200 rows are done.",
    "",
    "Rubric v2 in short. RELEVANT only if the paper itself studies, builds or evaluates a computational/AI method",
    "whose target task is finding or curating scholarly literature: scholarly search or retrieval, citation searching,",
    "ranking or recommending papers, ML-assisted title/abstract screening, systematic-review automation,",
    "active-learning prioritisation for screening, or evaluating AI tools for that purpose.",
    "NOT RELEVANT if AI is only the subject being reviewed (e.g. 'AI in medicine'), AI is applied to the content of",
    "studies after selection, it is a review method without AI, or it is bibliometric mapping only.",
    "UNCERTAIN if the abstract is missing or ambiguous. Do not guess.",
    "Full rubric: docs/06_Evidence_and_Logs/Annotation_Rubric_v2.md",
]


def draw(labels: pd.DataFrame, n: int = N, seed: int = SEED) -> pd.DataFrame:
    pool = labels[labels.label_source == "ai_provisional_not_reviewed"].sort_values("screening_id")
    if len(pool) < n:
        raise ValueError(f"only {len(pool)} unreviewed records")
    idx = np.random.default_rng(seed).choice(len(pool), size=n, replace=False)
    s = pool.iloc[np.sort(idx)].copy()
    s = s.sample(frac=1, random_state=seed).reset_index(drop=True)  # shuffled order on the sheet
    s.insert(0, "check_id", [f"CHK{i + 1:03d}" for i in range(n)])
    return s


def write_sheet(sample: pd.DataFrame, path: Path) -> None:
    wb = Workbook()
    ws = wb.active; ws.title = "Spotcheck"
    cols = ["check_id", "title", "abstract", "year", "Your_Label", "Your_Rationale", "Reviewer_ID", "Review_Date"]
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="305496")
    for _, r in sample.iterrows():
        ws.append([r.check_id, r.title, r.abstract if isinstance(r.abstract, str) and r.abstract.strip() else "(no abstract)",
                   int(r.year), "", "", "", ""])
    widths = {"A": 9, "B": 45, "C": 90, "D": 7, "E": 15, "F": 40, "G": 13, "H": 12}
    for k, w in widths.items():
        ws.column_dimensions[k].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    dv = DataValidation(type="list", formula1='"' + ",".join(CHOICES) + '"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(f"E2:E{len(sample) + 1}")
    for c in ("E", "F", "G", "H"):
        for cell in ws[c][1:]:
            cell.fill = PatternFill("solid", fgColor="FFF2CC")
    ws.freeze_panes = "B2"
    info = wb.create_sheet("Instructions")
    for line in INSTRUCTIONS:
        info.append([line])
    info["A1"].font = Font(bold=True, size=13); info.column_dimensions["A"].width = 120
    wb.save(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=Path, required=True, help="final_screening_labels_reviewed_20261105.csv")
    ap.add_argument("--queue", type=Path, required=True, help="private screening queue with title/abstract")
    ap.add_argument("--private-out", type=Path, required=True, help="where to write the private .xlsx")
    ap.add_argument("--key-out", type=Path, required=True, help="public key CSV (no abstracts)")
    a = ap.parse_args()
    labels = pd.read_csv(a.labels)
    q = pd.read_csv(a.queue, usecols=["screening_id", "openalex_id", "title", "abstract", "year"])
    s = draw(labels).merge(q, on="screening_id", how="left", validate="one_to_one")
    if s.title.isna().any():
        raise ValueError("sample record missing from queue")
    a.private_out.parent.mkdir(parents=True, exist_ok=True); a.key_out.parent.mkdir(parents=True, exist_ok=True)
    write_sheet(s, a.private_out)
    s[["check_id", "screening_id", "openalex_id"]].to_csv(a.key_out, index=False)
    print(f"{len(s)} records sampled (seed {SEED}) from {int((labels.label_source == 'ai_provisional_not_reviewed').sum())}")


if __name__ == "__main__":
    main()
