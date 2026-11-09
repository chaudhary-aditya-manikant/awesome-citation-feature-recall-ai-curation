import sys
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import merge_human_screening as m


def sample_decisions():
    return pd.DataFrame([
        {"Screening_ID":"SCR0001", "Human_Relevance_Label":1, "Rationale":"Directly evaluates an ML paper recommender.",
         "Confidence":"high", "Reviewer_ID":"R1", "Review_Date":"2026-10-31", "Second_Screen_Label":None,
         "Adjudication_Notes":None, "Adjudicated_Label":None, "Title":"A", "Abstract":"text"},
        {"Screening_ID":"SCR0002", "Human_Relevance_Label":0, "Rationale":"Does not concern scholarly-literature curation.",
         "Confidence":"medium", "Reviewer_ID":"R1", "Review_Date":"2026-10-31", "Second_Screen_Label":None,
         "Adjudication_Notes":None, "Adjudicated_Label":None, "Title":"B", "Abstract":"text"},
        {"Screening_ID":"SCR0003", "Human_Relevance_Label":"uncertain", "Rationale":"Abstract does not describe method sufficiently.",
         "Confidence":"low", "Reviewer_ID":"R1", "Review_Date":"2026-10-31", "Second_Screen_Label":None,
         "Adjudication_Notes":None, "Adjudicated_Label":None, "Title":"C", "Abstract":"text"},
    ])


def test_normalize_label_accepts_expected_values():
    assert m.normalize_label(1) == 1
    assert m.normalize_label(0.0) == 0
    assert m.normalize_label("uncertain") == "uncertain"
    assert m.normalize_label(None) is None


def test_normalize_label_rejects_unapproved_values():
    with pytest.raises(ValueError):
        m.normalize_label("yes")


def test_queue_coverage_requires_exact_screening_ids():
    decisions = sample_decisions()
    queue = pd.DataFrame({"screening_id":["SCR0001", "SCR0002", "SCR0003"]})
    report = m.validate_against_queue(decisions, queue)
    assert report["id_coverage_exact"] is True
    assert report["first_pass_labelled"] == 3
    assert report["first_pass_uncertain"] == 1


def test_missing_decision_metadata_is_reported():
    decisions = sample_decisions()
    decisions.loc[0, "Rationale"] = None
    queue = pd.DataFrame({"screening_id":["SCR0001", "SCR0002", "SCR0003"]})
    report = m.validate_against_queue(decisions, queue)
    assert report["incomplete_decision_metadata_records"] == 1
    assert report["final_dataset_ready"] is False


def test_rescreen_sample_is_reproducible_and_includes_all_uncertain():
    decisions = sample_decisions()
    # Add 20 binary decisions so the 20% sample is predictable and non-trivial.
    extra = []
    for i in range(4, 24):
        extra.append({"Screening_ID":f"SCR{i:04d}", "Human_Relevance_Label":i % 2,
                      "Title":f"T{i}", "Abstract":"text"})
    decisions = pd.concat([decisions, pd.DataFrame(extra)], ignore_index=True)
    a = m.create_rescreen_sample(decisions, seed=20261030)
    b = m.create_rescreen_sample(decisions, seed=20261030)
    assert a.Screening_ID.tolist() == b.Screening_ID.tolist()
    assert "SCR0003" in set(a.Screening_ID)
    assert int((a.Rescreen_Reason == "seeded_20pct_of_decided").sum()) == 5
    assert int((a.Rescreen_Reason == "all_uncertain").sum()) == 1
