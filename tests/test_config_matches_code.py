"""configs/frozen_protocol.json must match the defaults hard-coded in the runners."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "configs/frozen_protocol.json").read_text())
RUN = (ROOT / "src/run_experiment.py").read_text()
CF = (ROOT / "src/run_crossfit_exploratory.py").read_text()


def test_seeds_and_bootstrap():
    assert f'default={CFG["split"]["seed"]}' in RUN and f'default={CFG["split"]["seed"]}' in CF
    assert f'default={CFG["bootstrap"]["replicates"]}' in RUN
    assert str(CFG["bootstrap"]["seed"]) in RUN and str(CFG["bootstrap"]["seed"]) in CF


def test_model_settings():
    m = CFG["model"]
    assert f'ngram_range=({m["ngram_range"][0]}, {m["ngram_range"][1]})' in RUN
    assert f'min_df={m["min_df"]}' in RUN
    assert f'C={m["C"]}' in RUN and f'max_iter={m["max_iter"]}' in RUN
    assert f'class_weight="{m["class_weight"]}"' in RUN and f'solver="{m["solver"]}"' in RUN


def test_metric_and_gate_settings():
    assert f'default={CFG["metrics"]["k_fraction"]:.2f}' in RUN
    assert f'n_splits={CFG["split"]["n_splits"]}' in RUN
    g = CFG["dataset_gate"]["min_relevant_lower_citation_in_test"]
    assert re.search(rf"low_pos >= {g}\b", RUN)
    assert f'MIN_PRIMARY_DENOMINATOR = {CFG["estimability_guard"]["min_primary_denominator"]}' in RUN
    for f in CFG["metrics"]["sensitivity_k_fractions"]:
        assert f"{f:.2f}" in CF
