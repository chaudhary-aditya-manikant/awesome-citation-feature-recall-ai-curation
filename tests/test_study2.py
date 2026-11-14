"""Tests for Study 2 (synthetic data only - these are software checks, not results)."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

KIT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KIT / "src")]
from run_study2 import select_topk, load_protocol  # noqa: E402
from study2_fetch_synergy import add_split_groups  # noqa: E402


def test_topk_size_and_ties():
    s = np.array([.9, .9, .1, .5]); ids = np.array(["b", "a", "c", "d"]); low = np.zeros(4, bool)
    sel = select_topk(s, ids, low, 0.5)
    assert sel.sum() == 2 and sel[0] and sel[1]


def test_reserved_slots_go_to_lower_citation():
    s = np.arange(10, 0, -1, dtype=float); ids = np.array(list("abcdefghij"))
    low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], bool)
    sel = select_topk(s, ids, low, 0.4, reserved=0.5)   # K=4, 2 reserved
    assert sel.sum() == 4 and sel[8] and sel[9] and sel[0] and sel[1]


def test_protocol_refuses_undecided(tmp_path):
    p = tmp_path / "p.json"; p.write_text(json.dumps({"x": "DECIDE (int)"}))
    with pytest.raises(SystemExit):
        load_protocol(p)


def test_split_groups_merge_same_title():
    df = pd.DataFrame({"dataset": ["A", "A", "B"], "openalex_id": ["W1", "W2", "W3"],
                       "title": ["Deep Learning!", "deep learning", "Deep learning"]})
    g = add_split_groups(df).split_group_id.tolist()
    assert g[0] == g[1] and g[2] != g[0]


def synthetic(tmp_path):
    rng = np.random.default_rng(0)
    rows = []
    for ds in ["D1", "D2"]:
        for i in range(400):
            y = int(rng.random() < 0.15)
            cit = int(rng.poisson(20 if y else 8))
            rows.append({"dataset": ds, "openalex_id": f"{ds}W{i}", "title": ("screening recall " if y else "other topic ") + str(i),
                         "abstract": "systematic review" if y else "unrelated words", "year": int(rng.integers(2005, 2024)),
                         "citations": cit, "label": y, "split_group_id": f"{ds}|W{i}"})
    p = tmp_path / "in.csv"; pd.DataFrame(rows).to_csv(p, index=False)
    cfg = json.loads((KIT / "configs/study2_protocol.json").read_text())
    cfg["frozen_on"] = "2026-11-09"; cfg["data"].update(min_inclusions_per_dataset=10, citation_snapshot_date="2026-11-09")
    cfg["fair_rerank_reserved_fraction"] = 0.5
    cfg["gate"] = {"min_relevant_lower_citation": 5, "min_relevant_higher_citation": 5}
    cfg["success_rule"]["max_overall_precision_loss_of_blind"] = 0.05
    c = tmp_path / "proto.json"; c.write_text(json.dumps(cfg))
    return p, c


def test_end_to_end_synthetic_is_deterministic(tmp_path):
    p, c = synthetic(tmp_path)
    outs = []
    for run in ("r1", "r2"):
        o = tmp_path / run
        subprocess.run([sys.executable, str(KIT / "src/run_study2.py"), "--input", str(p), "--protocol", str(c),
                        "--output", str(o), "--bootstrap", "50"], check=True, cwd=KIT / "src", capture_output=True)
        outs.append((o / "study2_paired_contrasts.csv").read_text())
        s = json.loads((o / "study2_summary.json").read_text())
        assert s["datasets"] == 2 and s["status"] in {"CONFIRMATORY", "GATE_FAILED_EXPLORATORY"}
        m = pd.read_csv(o / "study2_pooled_metrics.csv")
        assert set(m.condition) == {"citation_blind", "citation_aware", "citation_only", "fair_rerank"}
    assert outs[0] == outs[1]


def test_no_lower_citation_relevant_does_not_crash(tmp_path):
    p, c = synthetic(tmp_path)
    d = pd.read_csv(p); d.loc[d.label == 1, "citations"] = 10_000; d.to_csv(p, index=False)
    o = tmp_path / "z"
    subprocess.run([sys.executable, str(KIT / "src/run_study2.py"), "--input", str(p), "--protocol", str(c),
                    "--output", str(o), "--bootstrap", "10"], check=True, cwd=KIT / "src", capture_output=True)
    s = json.loads((o / "study2_summary.json").read_text())
    assert s["gate_pass"] is False and s["H1_supported"] is False


def test_pick_id_finds_ids_in_index_or_column():
    from study2_fetch_synergy import _pick_id
    a = pd.DataFrame({"title": ["a", "b"]}, index=pd.Index(["https://openalex.org/W2011", "https://openalex.org/W2022"], name="id")).reset_index()
    assert _pick_id(a).tolist() == ["W2011", "W2022"]
    b = pd.DataFrame({"openalex_id": ["https://openalex.org/W3033", None], "title": ["a", "b"]})
    assert _pick_id(b).tolist()[0] == "W3033" and pd.isna(_pick_id(b).tolist()[1])
    assert _pick_id(pd.DataFrame({"title": ["a"]})).isna().all()


def test_committed_study2_tables_are_consistent():
    r = KIT / "results" / "study2_confirmatory"
    m = pd.read_csv(r / "study2_pooled_metrics.csv"); p = pd.read_csv(r / "study2_per_dataset.csv")
    s = json.loads((r / "study2_summary.json").read_text())
    k = m[m.k_fraction == 0.2].set_index("condition")
    for c in ("citation_blind", "citation_aware", "fair_rerank", "citation_only"):
        assert p[p.condition == c].low.sum() == k.loc[c, "low"] and p[p.condition == c]["all"].sum() == k.loc[c, "all"]
    assert s["gate_pass"] and s["relevant_lower"] == k.loc["citation_blind", "den_low"] == 977
    c = pd.read_csv(r / "study2_paired_contrasts.csv")
    prim = c[(c.contrast == "citation_blind - citation_aware") & (c.metric == "recall_lower")].iloc[0]
    assert abs(prim.point - (742 - 691) / 977) < 1e-9 and prim.ci95_low > 0
