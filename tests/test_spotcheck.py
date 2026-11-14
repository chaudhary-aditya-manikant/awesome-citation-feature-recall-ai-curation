"""Tests for the Amendment A4 spot-check (synthetic data)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from make_spotcheck_sample import draw  # noqa: E402
from score_spotcheck import clopper_pearson, score  # noqa: E402


def _labels(n=500):
    return pd.DataFrame({"screening_id": [f"S{i:04d}" for i in range(n)],
                         "label_source": ["ai_provisional_not_reviewed" if i % 5 else "reviewer_MNS2026008" for i in range(n)],
                         "ai_label": "not_relevant", "final_label": "not_relevant"})


def test_sample_is_seeded_unreviewed_only_and_unique():
    a, b = draw(_labels(), n=50), draw(_labels(), n=50)
    assert a.screening_id.tolist() == b.screening_id.tolist()
    assert a.screening_id.is_unique and (a.label_source == "ai_provisional_not_reviewed").all()


def test_committed_key_matches_seeded_draw():
    labels = pd.read_csv(ROOT / "data/ai_provisional_20261105/final_screening_labels_reviewed_20261105.csv")
    key = pd.read_csv(ROOT / "data/spotcheck_20261110/spotcheck_key.csv")
    assert draw(labels).screening_id.tolist() == key.screening_id.tolist()


def test_clopper_pearson_zero_of_200():
    lo, hi = clopper_pearson(0, 200)
    assert lo == 0 and abs(hi - 0.01828) < 1e-4


def test_score_counts_and_rejects_blank():
    labels = _labels(); s = draw(labels, n=10)
    key = s[["check_id", "screening_id"]].assign(openalex_id="W")
    sheet = pd.DataFrame({"check_id": s.check_id, "Your_Label": ["not_relevant"] * 9 + ["relevant"],
                          "Your_Rationale": "", "Reviewer_ID": "MNS2026008", "Review_Date": "2026-11-10"})
    d, summ = score(sheet, key, labels, 400)
    assert summ["agreement_with_ai"] == 9 and summ["author_relevant"] == 1
    sheet.loc[0, "Your_Label"] = None
    with pytest.raises(ValueError):
        score(sheet, key, labels, 400)


def test_apply_corrections_changes_only_sampled_records():
    from apply_spotcheck_corrections import apply
    labels = pd.DataFrame({"screening_id": ["A", "B", "C", "D"], "final_label": "not_relevant",
                           "label_source": "ai_provisional_not_reviewed"})
    mi = pd.DataFrame({"screening_id": ["A", "B", "C", "D"], "label": 0, "label_status": "ai_provisional"})
    dec = pd.DataFrame({"screening_id": ["A", "B"], "Your_Label": ["relevant", "uncertain"]})
    lab, out, s = apply(labels, mi, dec)
    assert out.screening_id.tolist() == ["A", "C", "D"] and out.label.tolist() == [1, 0, 0]
    assert out.label_status.tolist() == ["single_reviewer_audited", "ai_provisional", "ai_provisional"]
    assert lab.label_source.tolist()[:2] == ["reviewer_spotcheck_20261110"] * 2 and s["relevant_after"] == 1
