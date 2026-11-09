"""Unit checks for fail-closed input validation; fixtures are synthetic only."""
import importlib.util
from pathlib import Path
import pandas as pd
import pytest

SCRIPT = Path(__file__).parents[1] / "code" / "run_experiment.py"
spec = importlib.util.spec_from_file_location("run_experiment", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fixture(n=120):
    return pd.DataFrame({
        "openalex_id": [f"W{i}" for i in range(n)],
        "title": [f"Synthetic title {i}" for i in range(n)],
        "abstract": [f"Synthetic abstract about research screening {i}" for i in range(n)],
        "year": [2018 + i % 8 for i in range(n)],
        "citations": [i * 3 for i in range(n)],
        "metadata_language": ["en" if i % 2 else "es" for i in range(n)],
        "label": [i % 2 for i in range(n)],
        "label_status": ["adjudicated"] * n,
        "split_group_id": [f"G{i}" for i in range(n)],
        "duplicate_cluster_id": [f"LEGACY_{i}" for i in range(n)],
    })


def test_refuses_28_record_pilot(tmp_path):
    p = tmp_path / "pilot.csv"
    fixture(28).to_csv(p, index=False)
    with pytest.raises(ValueError, match="28-record pilot"):
        mod.load_and_validate(p)


def test_refuses_preliminary_ai_labels(tmp_path):
    d = fixture(120)
    d.loc[0, "label_status"] = "preliminary_ai_assisted"
    p = tmp_path / "bad.csv"
    d.to_csv(p, index=False)
    with pytest.raises(ValueError, match="Only adjudicated labels"):
        mod.load_and_validate(p)


def test_refuses_duplicate_ids(tmp_path):
    d = fixture(120)
    d.loc[1, "openalex_id"] = d.loc[0, "openalex_id"]
    p = tmp_path / "dupe.csv"
    d.to_csv(p, index=False)
    with pytest.raises(ValueError, match="unique"):
        mod.load_and_validate(p)


def test_refuses_fractional_citation_counts(tmp_path):
    d = fixture(120)
    d["citations"] = d["citations"].astype(float)
    d.loc[0, "citations"] = 2.5
    p = tmp_path / "fractional.csv"
    d.to_csv(p, index=False)
    with pytest.raises(ValueError, match="citation counts must be integers"):
        mod.load_and_validate(p)


def test_paired_cluster_bootstrap_returns_cluster_interval():
    import numpy as np
    n = 160
    y = np.array([1] * 80 + [0] * 80)
    low = np.array([True] * 40 + [False] * 40 + [True] * 40 + [False] * 40)
    scores_a = np.linspace(1.0, 0.0, n)
    scores_b = np.linspace(0.9, 0.1, n)
    ids = np.array([f"W{i}" for i in range(n)])
    clusters = np.array([f"C{i // 2}" for i in range(n)])
    result = mod.paired_cluster_bootstrap(
        y, scores_a, scores_b, low, ids, clusters, iterations=200, seed=11
    )
    assert result["unit"] == "split_group_id"
    assert result["method"] == "paired_cluster_percentile_bootstrap"
    assert result["valid_replicates"] >= 100
    assert result["ci95_low"] is not None


def test_requires_reviewed_split_group_not_legacy_duplicate_field(tmp_path):
    d = fixture(120)
    d = d.drop(columns=["split_group_id"])
    p = tmp_path / "legacy_group_only.csv"
    d.to_csv(p, index=False)
    with pytest.raises(ValueError, match="Missing required columns"):
        mod.load_and_validate(p)


def test_uses_reviewed_split_group_even_when_legacy_field_disagrees(tmp_path):
    d = fixture(120)
    d["duplicate_cluster_id"] = [f"WRONG_{i}" for i in range(120)]
    p = tmp_path / "reviewed_group.csv"
    d.to_csv(p, index=False)
    loaded = mod.load_and_validate(p)
    assert loaded["split_group_id"].tolist() == [f"G{i}" for i in range(120)]
