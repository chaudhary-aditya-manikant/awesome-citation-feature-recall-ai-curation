import sys
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import merge_language_verification as m


def review_frame():
    return pd.DataFrame([
        {"Language_Sample_ID":"LANG001", "Verified_Publication_Language":"English",
         "Evidence_Type":"Publisher landing page", "Evidence_URL":"https://publisher.example/article/1",
         "Verifier_ID":"R1", "Verification_Date":"2026-10-31", "Verification_Notes":"Page has English full text and article metadata."},
        {"Language_Sample_ID":"LANG002", "Verified_Publication_Language":"Portuguese",
         "Evidence_Type":"Publisher PDF", "Evidence_URL":"https://publisher.example/article/2.pdf",
         "Verifier_ID":"R1", "Verification_Date":"2026-10-31", "Verification_Notes":"PDF language verified."},
    ])


def key_frame():
    return pd.DataFrame([
        {"Language_Sample_ID":"LANG001", "OpenAlex_ID":"W1", "OpenAlex_Metadata_Language":"en", "Sampling_Stratum":"English", "Design_Weight":2.0},
        {"Language_Sample_ID":"LANG002", "OpenAlex_ID":"W2", "OpenAlex_Metadata_Language":"pt", "Sampling_Stratum":"Non-English", "Design_Weight":3.0},
    ])


def test_language_sample_id_coverage_exact():
    report = m.validate_language_review(review_frame(), key_frame())
    assert report["sample_id_coverage_exact"] is True
    assert report["all_rows_documented"] is True
    assert report["status"] == "DOCUMENTED_PENDING_SOURCE_QUALITY_AUDIT"


def test_incomplete_language_remains_pending():
    df = review_frame()
    df.loc[1, "Verified_Publication_Language"] = None
    report = m.validate_language_review(df, key_frame())
    assert report["pending_language_entries"] == 1
    assert report["all_rows_documented"] is False


def test_missing_evidence_url_is_invalid():
    df = review_frame()
    df.loc[0, "Evidence_URL"] = ""
    report = m.validate_language_review(df, key_frame())
    assert report["invalid_evidence_records"] == 1
    assert report["all_rows_documented"] is False


def test_unknown_requires_explanation_and_source():
    df = review_frame()
    df.loc[0, "Verified_Publication_Language"] = "Unknown"
    df.loc[0, "Verification_Notes"] = ""
    report = m.validate_language_review(df, key_frame())
    assert report["invalid_evidence_records"] == 1
    assert "unknown_language_requires_explanation" in report["invalid_evidence_examples"][0]["issues"]


def test_missing_or_extra_sample_ids_fail():
    df = review_frame().iloc[:1].copy()
    with pytest.raises(ValueError, match="sample ID mismatch"):
        m.validate_language_review(df, key_frame())
