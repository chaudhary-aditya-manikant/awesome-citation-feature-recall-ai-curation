"""Tests for the post-hoc reference rankers (synthetic data; software checks only)."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from run_posthoc_comparators import select_topk  # noqa: E402


def test_reserved_slots_fill_with_best_lower_citation_records():
    s = np.arange(10, 0, -1, dtype=float); ids = np.array(list("abcdefghij"))
    low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], bool)
    sel = select_topk(s, ids, low, 0.4, reserved=0.5)  # K = 4, 2 reserved
    assert sel.sum() == 4 and sel[[0, 1, 8, 9]].all()


def test_without_reservation_is_plain_topk():
    s = np.array([.2, .9, .5, .9]); ids = np.array(["d", "c", "b", "a"])
    sel = select_topk(s, ids, np.ones(4, bool), 0.5)
    assert sel.tolist() == [False, True, False, True]


def test_end_to_end_on_synthetic_predictions(tmp_path):
    rng = np.random.default_rng(1); n = 300
    pred = pd.DataFrame({"openalex_id": [f"W{i}" for i in range(n)], "fold": np.arange(n) % 5,
                         "citations": rng.integers(0, 100, n), "low_citation": rng.random(n) < .5,
                         "label": (np.arange(n) % 7 == 0).astype(int),
                         "score_citation_blind": rng.random(n), "score_citation_aware": rng.random(n)})
    p = tmp_path / "pred.csv"; pred.to_csv(p, index=False)
    g = tmp_path / "g.csv"; pd.DataFrame({"openalex_id": pred.openalex_id, "split_group_id": pred.openalex_id}).to_csv(g, index=False)
    o = tmp_path / "out"
    subprocess.run([sys.executable, str(ROOT / "src/run_posthoc_comparators.py"), "--predictions", str(p),
                    "--groups", str(g), "--output", str(o), "--bootstrap", "20"], check=True, capture_output=True)
    m = pd.read_csv(o / "posthoc_pooled_metrics.csv")
    assert set(m.condition) == {"citation_blind", "citation_aware", "citation_only", "fair_rerank"}
    assert json.loads((o / "posthoc_summary.json").read_text())["status"].startswith("POST_HOC")
    r = m[m.k_fraction == 0.2].set_index("condition")
    assert r.loc["fair_rerank", "low"] >= r.loc["citation_aware", "low"]  # reservation never lowers lower-citation hits
