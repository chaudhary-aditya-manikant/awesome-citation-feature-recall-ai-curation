#!/usr/bin/env python3
"""Validate blinded publication-language review entries without guessing.

The script imports Verify_200 from the blinded language workbook, validates
sample-ID coverage against the private Language_Key sheet, and writes the
reviewer-entered values unchanged. It does not infer or auto-fill any language.
A completed workbook is still evidence awaiting a human source-quality audit.

Example:
python code/merge_language_verification.py \
  --workbook 06_Balanced_Collection_Audit_20261031/workbooks/AITR_Balanced_Language_Verification_Blinded.xlsx \
  --admin-workbook 06_Balanced_Collection_Audit_20261031/workbooks/AITR_Balanced_Admin_Crosswalk_Private.xlsx \
  --output-dir data/language_review_import
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

REQUIRED_COLUMNS = {
    "Language_Sample_ID", "Verified_Publication_Language", "Evidence_Type",
    "Evidence_URL", "Verifier_ID", "Verification_Date", "Verification_Notes",
}
ALLOWED_EVIDENCE_TYPES = {
    "Publisher landing page", "Publisher PDF", "Institutional repository",
    "Library catalogue", "Other",
}
UNKNOWN_VALUES = {"unknown", "not verifiable", "not_verifiable", "unable to verify", "unverified"}


def _text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def load_review_workbook(workbook_path: Path) -> pd.DataFrame:
    xls = pd.ExcelFile(workbook_path)
    if "Verify_200" not in xls.sheet_names:
        raise ValueError("Language workbook must contain Verify_200 sheet")
    df = pd.read_excel(workbook_path, sheet_name="Verify_200", dtype={"Language_Sample_ID": str})
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Verify_200 is missing columns: {sorted(missing)}")
    df["Language_Sample_ID"] = df["Language_Sample_ID"].map(_text)
    if df["Language_Sample_ID"].eq("").any():
        raise ValueError("Blank Language_Sample_ID found")
    if df["Language_Sample_ID"].duplicated().any():
        raise ValueError("Duplicate Language_Sample_ID values found")
    return df


def load_language_key(admin_workbook_path: Path) -> pd.DataFrame:
    xls = pd.ExcelFile(admin_workbook_path)
    if "Language_Key" not in xls.sheet_names:
        raise ValueError("Private admin workbook must contain Language_Key sheet")
    key = pd.read_excel(admin_workbook_path, sheet_name="Language_Key", dtype={"Language_Sample_ID": str})
    required = {"Language_Sample_ID", "OpenAlex_ID", "OpenAlex_Metadata_Language", "Sampling_Stratum", "Design_Weight"}
    missing = required - set(key.columns)
    if missing:
        raise ValueError(f"Language_Key is missing columns: {sorted(missing)}")
    key["Language_Sample_ID"] = key["Language_Sample_ID"].map(_text)
    if key["Language_Sample_ID"].duplicated().any():
        raise ValueError("Duplicate Language_Sample_ID values in Language_Key")
    return key


def validate_language_review(review: pd.DataFrame, key: pd.DataFrame) -> dict:
    expected = set(key["Language_Sample_ID"])
    observed = set(review["Language_Sample_ID"])
    missing_ids = sorted(expected - observed)
    unexpected_ids = sorted(observed - expected)
    if missing_ids or unexpected_ids:
        raise ValueError(
            f"Language sample ID mismatch: missing={len(missing_ids)}, unexpected={len(unexpected_ids)}; "
            f"missing examples={missing_ids[:5]}, unexpected examples={unexpected_ids[:5]}"
        )

    pending = []
    invalid = []
    unknown_documented = 0
    for row in review.to_dict("records"):
        sid = _text(row.get("Language_Sample_ID"))
        lang = _text(row.get("Verified_Publication_Language"))
        evidence = _text(row.get("Evidence_Type"))
        url = _text(row.get("Evidence_URL"))
        verifier = _text(row.get("Verifier_ID"))
        date = _text(row.get("Verification_Date"))
        notes = _text(row.get("Verification_Notes"))

        if not lang:
            pending.append(sid)
            continue
        issues = []
        if evidence not in ALLOWED_EVIDENCE_TYPES:
            issues.append("unsupported_or_missing_evidence_type")
        if not _is_http_url(url):
            issues.append("missing_or_invalid_evidence_url")
        if not verifier:
            issues.append("missing_verifier_id")
        if not date:
            issues.append("missing_verification_date")
        if lang.lower() in UNKNOWN_VALUES and not notes:
            issues.append("unknown_language_requires_explanation")
        if issues:
            invalid.append({"Language_Sample_ID": sid, "issues": issues})
        elif lang.lower() in UNKNOWN_VALUES:
            unknown_documented += 1

    completed = len(review) - len(pending)
    fully_documented = completed == len(key) and len(invalid) == 0
    return {
        "sample_records_expected": len(expected),
        "workbook_records": len(review),
        "sample_id_coverage_exact": True,
        "completed_language_entries": completed,
        "pending_language_entries": len(pending),
        "invalid_evidence_records": len(invalid),
        "documented_unknown_or_not_verifiable": unknown_documented,
        "pending_sample_ids_first_25": pending[:25],
        "invalid_evidence_examples": invalid[:25],
        "all_rows_documented": fully_documented,
        "status": "DOCUMENTED_PENDING_SOURCE_QUALITY_AUDIT" if fully_documented else "INCOMPLETE_OR_INVALID",
        "important_limit": "This tool checks completeness and URL/evidence fields only; a human must inspect that each cited source actually establishes the publication language.",
    }


def run(workbook_path: Path, admin_workbook_path: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    review = load_review_workbook(workbook_path)
    key = load_language_key(admin_workbook_path)
    report = validate_language_review(review, key)
    review.to_csv(output_dir / "language_verification_entries_imported_blinded.csv", index=False)
    (output_dir / "language_verification_import_report.json").write_text(json.dumps(report, indent=2))
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbook", type=Path, required=True)
    ap.add_argument("--admin-workbook", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(run(args.workbook, args.admin_workbook, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
