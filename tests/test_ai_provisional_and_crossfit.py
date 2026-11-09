"""Tests for Amendment A3 behaviour: AI-provisional labels and exploratory modes."""
import subprocess, sys
from pathlib import Path
import numpy as np, pandas as pd, pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from run_experiment import load_and_validate  # noqa: E402


def _frame(n=200, status="ai_provisional"):
    rng = np.random.default_rng(0)
    y = (np.arange(n) % 10 == 0).astype(int)
    return pd.DataFrame({
        "openalex_id": [f"W{i}" for i in range(n)],
        "title": [("screening systematic review ranking " if v else "unrelated topic ") + str(i) for i, v in enumerate(y)],
        "abstract": ["active learning citation screening" if v else "other words here" for v in y],
        "year": rng.integers(2015, 2026, n), "citations": rng.integers(0, 50, n),
        "metadata_language": "en", "label": y, "label_status": status,
        "split_group_id": [f"G{i}" for i in range(n)],
    })


def test_ai_provisional_rejected_by_default(tmp_path):
    p = tmp_path / "d.csv"; _frame().to_csv(p, index=False)
    with pytest.raises(ValueError, match="Only adjudicated labels"):
        load_and_validate(p)


def test_ai_provisional_accepted_only_with_flag(tmp_path):
    p = tmp_path / "d.csv"; _frame().to_csv(p, index=False)
    assert len(load_and_validate(p, allow_ai_provisional=True)) == 200


def test_runner_requires_matching_provenance(tmp_path):
    p = tmp_path / "d.csv"; _frame().to_csv(p, index=False)
    r = subprocess.run([sys.executable, str(ROOT / "code/run_experiment.py"), "--input", str(p),
                        "--output", str(tmp_path / "o"), "--snapshot-date", "2026-10-30",
                        "--allow-ai-provisional-labels"], capture_output=True, text=True)
    assert r.returncode != 0 and "requires --data-provenance ai-provisional" in r.stderr


def test_gate_failure_stops_without_exploratory_flag(tmp_path):
    p = tmp_path / "d.csv"; _frame().to_csv(p, index=False)
    r = subprocess.run([sys.executable, str(ROOT / "code/run_experiment.py"), "--input", str(p),
                        "--output", str(tmp_path / "o"), "--snapshot-date", "2026-10-30",
                        "--data-provenance", "ai-provisional", "--allow-ai-provisional-labels",
                        "--bootstrap", "200"], capture_output=True, text=True)
    assert r.returncode != 0 and "gate failed" in r.stderr


def test_exploratory_run_is_stamped_and_not_estimable(tmp_path):
    p = tmp_path / "d.csv"; _frame().to_csv(p, index=False)
    out = tmp_path / "o"
    r = subprocess.run([sys.executable, str(ROOT / "code/run_experiment.py"), "--input", str(p),
                        "--output", str(out), "--snapshot-date", "2026-10-30",
                        "--data-provenance", "ai-provisional", "--allow-ai-provisional-labels",
                        "--exploratory-after-gate-failure", "--bootstrap", "200"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    pc = pd.read_csv(out / "primary_comparison.csv").iloc[0]
    assert pc.analysis_status == "exploratory" and pc.label_provenance == "ai_provisional_not_human_verified"
    assert not bool(pc.primary_estimable) and not bool(pc.success_rule_met)
    assert (out / "gate_report_FAILED.json").exists()


def test_crossfit_runs_and_stamps(tmp_path):
    p = tmp_path / "d.csv"; _frame().to_csv(p, index=False)
    out = tmp_path / "cf"
    r = subprocess.run([sys.executable, str(ROOT / "code/run_crossfit_exploratory.py"), "--input", str(p),
                        "--output", str(out), "--snapshot-date", "2026-10-30", "--bootstrap", "100",
                        "--allow-ai-provisional-labels"], capture_output=True, text=True, cwd=ROOT / "code")
    assert r.returncode == 0, r.stderr
    s = (out / "crossfit_summary.json").read_text()
    assert "AI_PROVISIONAL_LABELS_NOT_HUMAN_VERIFIED" in s
    oof = pd.read_csv(out / "crossfit_out_of_fold_predictions.csv")
    assert len(oof) == 200 and oof.fold.between(0, 4).all()


def test_crossfit_accepts_merge_output_without_ai_confidence(tmp_path):
    df = _frame(); df["screening_id"] = [f"SCR{i}" for i in range(len(df))]
    p = tmp_path / "d.csv"; df.to_csv(p, index=False)
    r = subprocess.run([sys.executable, str(ROOT / "code/run_crossfit_exploratory.py"), "--input", str(p),
                        "--output", str(tmp_path / "cf"), "--snapshot-date", "2026-10-30", "--bootstrap", "50",
                        "--allow-ai-provisional-labels"], capture_output=True, text=True, cwd=ROOT / "code")
    assert r.returncode == 0, r.stderr
