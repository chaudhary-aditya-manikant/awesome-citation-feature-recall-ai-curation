import sys
from pathlib import Path
import pandas as pd, pytest
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "code"))
from merge_review_first import merge  # noqa: E402

def _setup(tmp_path, your=("relevant", "", "not_relevant")):
    ids = ["SCR1", "SCR2", "SCR3"]
    pd.DataFrame({"screening_id": ids, "ai_label": ["relevant", "not_relevant", "relevant"]}).to_csv(tmp_path / "ai.csv", index=False)
    pd.DataFrame({"screening_id": ids, "openalex_id": ["W1", "W2", "W3"], "title": ["a", "b", "c"], "abstract": "x",
                  "year": 2020, "citations": 1, "metadata_language": "en", "split_group_id": ["G1", "G2", "G3"],
                  "language_verification_status": "unverified", "label": "", "label_status": ""}).to_csv(tmp_path / "q.csv", index=False)
    with pd.ExcelWriter(tmp_path / "s.xlsx") as w:
        pd.DataFrame({"Screening_ID": ["SCR1", "SCR3"], "Your_Label": [your[0], your[2]], "Your_Rationale": "", "Reviewer_ID": "AC"}).to_excel(w, sheet_name="1_Must_Check", index=False)
        pd.DataFrame({"Screening_ID": ["SCR2"], "Your_Label": [your[1]], "Your_Rationale": "", "Reviewer_ID": ""}).to_excel(w, sheet_name="2_Borderline", index=False)
        pd.DataFrame(columns=["Screening_ID", "Your_Label", "Your_Rationale", "Reviewer_ID"]).to_excel(w, sheet_name="3_Skim_Titles", index=False)

def test_reviewer_overrides_and_provenance(tmp_path):
    _setup(tmp_path)
    dec, s = merge(tmp_path / "s.xlsx", tmp_path / "ai.csv", tmp_path / "q.csv")
    d = dec.set_index("screening_id")
    assert d.loc["SCR3", "label"] == 0 and d.loc["SCR3", "label_status"] == "single_reviewer_audited"
    assert d.loc["SCR2", "label_status"] == "ai_provisional"
    assert s["reviewer_changed_ai_label"] == 1 and s["records_checked_by_reviewer"] == 2

def test_invalid_label_rejected(tmp_path):
    _setup(tmp_path, your=("yes", "", ""))
    with pytest.raises(ValueError, match="Invalid Your_Label"):
        merge(tmp_path / "s.xlsx", tmp_path / "ai.csv", tmp_path / "q.csv")
