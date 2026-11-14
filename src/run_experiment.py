#!/usr/bin/env python3
"""Run a paired citation-feature ablation on an adjudicated OpenAlex CSV.

This script is intentionally fail-closed: it refuses the 28-row pilot, uncertain
labels, missing required columns, duplicate IDs, and a test split without both
citation groups represented by relevant records. It never treats synthetic test
fixtures as research data.
"""
from __future__ import annotations
import argparse
import json
import math
import platform
import time
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MIN_PRIMARY_DENOMINATOR = 10  # minimum relevant lower-citation test records for an interpretable primary estimate

REQUIRED = {
    "openalex_id", "title", "abstract", "year", "citations",
    "metadata_language", "label", "label_status", "split_group_id"
}


def load_and_validate(path: Path, allow_ai_provisional: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if len(df) < 100:
        raise ValueError(
            f"Only {len(df)} rows supplied. The 28-record pilot is not an eligible "
            "evaluation dataset. Construct and adjudicate the larger pool first."
        )
    for c in ["openalex_id", "title", "label_status", "split_group_id"]:
        df[c] = df[c].fillna("").astype(str).str.strip()
    if df.openalex_id.eq("").any() or df.openalex_id.duplicated().any():
        raise ValueError("openalex_id must be present and unique after deduplication")
    if df.split_group_id.eq("").any():
        raise ValueError("split_group_id is required for every record; do not use the unaudited legacy duplicate_cluster_id")
    if not set(df.label.dropna().unique()).issubset({0, 1, 0.0, 1.0}):
        raise ValueError("label must contain only adjudicated binary values 0/1")
    if df.label.isna().any():
        raise ValueError("Unlabelled/uncertain records must be resolved or excluded")
    ok_status = {"adjudicated", "human_adjudicated", "single_reviewer_audited"}
    if allow_ai_provisional:
        # Amendment A3: AI-provisional labels are accepted only on explicit request and
        # every output is stamped as not human-verified.
        ok_status = ok_status | {"ai_provisional"}
    bad = sorted(set(df.label_status.str.lower()) - ok_status)
    if bad:
        raise ValueError(
            "Only adjudicated labels are accepted. Unsupported label_status values: "
            f"{bad}. Do not pass AI-assisted preliminary labels as gold labels."
        )
    df["label"] = df.label.astype(int)
    df["title"] = df.title.fillna("").astype(str)
    df["abstract"] = df.abstract.fillna("").astype(str)
    df["metadata_language"] = df.metadata_language.fillna("unknown").astype(str).str.strip()
    df.loc[df.metadata_language.eq(""), "metadata_language"] = "unknown"
    if (df.title.str.strip() == "").any():
        raise ValueError("Every included record needs a usable title")
    df["year"] = pd.to_numeric(df.year, errors="coerce")
    df["citations"] = pd.to_numeric(df.citations, errors="coerce")
    if df.year.isna().any() or df.citations.isna().any():
        raise ValueError("year and citations must be numeric; resolve missing values")
    if not np.all(np.equal(df.year, np.floor(df.year))):
        raise ValueError("publication year must be an integer")
    if not df.year.between(2015, 2025).all():
        raise ValueError("publication years must be within the frozen 2015–2025 window")
    if not np.all(np.equal(df.citations, np.floor(df.citations))):
        raise ValueError("citation counts must be integers")
    if (df.citations < 0).any():
        raise ValueError("Citation counts cannot be negative")
    if df.label.nunique() != 2:
        raise ValueError("Both positive and negative labels are required")
    if df.split_group_id.duplicated().sum() == 0:
        # Valid: each work may be its own cluster. Group split still applies.
        pass
    return df


def make_pipeline(include_citations: bool, random_state: int) -> Pipeline:
    numeric_cols = ["year"] + (["log_citations"] if include_citations else [])
    features = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                                     max_features=100000, sublinear_tf=True,
                                     lowercase=True, strip_accents="unicode"), "text"),
            ("numeric", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scale", StandardScaler())
            ]), numeric_cols),
        ],
        remainder="drop",
        sparse_threshold=0.3,
    )
    return Pipeline([
        ("features", features),
        ("model", LogisticRegression(C=1.0, max_iter=2000,
                                      class_weight="balanced", solver="liblinear",
                                      random_state=random_state)),
    ])


def recall_at_k(y: np.ndarray, selected: np.ndarray, mask: np.ndarray | None = None) -> float:
    if mask is None:
        mask = np.ones(len(y), dtype=bool)
    denom = int(np.sum((y == 1) & mask))
    if denom == 0:
        return float("nan")
    return float(np.sum((y == 1) & mask & selected) / denom)


def precision_at_k(y: np.ndarray, selected: np.ndarray) -> float:
    n = int(selected.sum())
    return float(np.sum((y == 1) & selected) / n) if n else float("nan")


def rank_metrics(y, scores, low_mask, high_mask, lang, ids, fraction=0.20):
    n = len(y)
    k = max(1, int(math.ceil(fraction * n)))
    order = np.lexsort((np.asarray(ids), -scores))
    selected = np.zeros(n, dtype=bool)
    selected[order[:k]] = True
    out = {
        "K": k,
        "N_test": n,
        "overall_recall_at_k": recall_at_k(y, selected),
        "overall_precision_at_k": precision_at_k(y, selected),
        "lower_citation_recall_at_k": recall_at_k(y, selected, low_mask),
        "higher_citation_recall_at_k": recall_at_k(y, selected, high_mask),
        "lower_citation_relevant_n": int(np.sum((y == 1) & low_mask)),
        "higher_citation_relevant_n": int(np.sum((y == 1) & high_mask)),
    }
    out["absolute_citation_recall_gap"] = abs(
        out["lower_citation_recall_at_k"] - out["higher_citation_recall_at_k"]
    ) if np.isfinite(out["lower_citation_recall_at_k"]) and np.isfinite(out["higher_citation_recall_at_k"]) else float("nan")
    for group in sorted(set(lang)):
        mask = np.asarray(lang) == group
        out[f"language_recall::{group}"] = recall_at_k(y, selected, mask)
        out[f"language_relevant_n::{group}"] = int(np.sum((y == 1) & mask))
    return out, selected, order


def paired_cluster_bootstrap(y, scores_a, scores_b, low_mask, ids,
                              cluster_ids, iterations, seed):
    """Paired percentile bootstrap resampling duplicate/version clusters.

    Every record in a sampled cluster is retained together. The same sampled
    cluster sequence is used for both ranking conditions, preserving pairing.
    This matches the grouped split's independence unit more closely than
    resampling individual records.
    """
    rng = np.random.default_rng(seed)
    cluster_ids = np.asarray(cluster_ids).astype(str)
    unique_clusters = np.unique(cluster_ids)
    member_indices = {g: np.flatnonzero(cluster_ids == g) for g in unique_clusters}
    diffs = []
    for _ in range(iterations):
        sampled_clusters = rng.choice(unique_clusters, size=len(unique_clusters), replace=True)
        idx = np.concatenate([member_indices[g] for g in sampled_clusters])
        y_b = np.asarray(y)[idx]
        low_b = np.asarray(low_mask)[idx]
        scores_a_b = np.asarray(scores_a)[idx]
        scores_b_b = np.asarray(scores_b)[idx]
        ids_b = np.asarray(ids)[idx].astype(str)
        den = int(np.sum((y_b == 1) & low_b))
        if den == 0:
            continue
        k = max(1, int(math.ceil(0.20 * len(idx))))
        selected_a = np.zeros(len(idx), dtype=bool)
        selected_b = np.zeros(len(idx), dtype=bool)
        selected_a[np.lexsort((ids_b, -scores_a_b))[:k]] = True
        selected_b[np.lexsort((ids_b, -scores_b_b))[:k]] = True
        recall_a = np.sum((y_b == 1) & low_b & selected_a) / den
        recall_b = np.sum((y_b == 1) & low_b & selected_b) / den
        diffs.append(float(recall_a - recall_b))
    if len(diffs) < max(100, iterations // 2):
        return {"valid_replicates": len(diffs), "ci95_low": None, "ci95_high": None,
                "warning": "Too few valid cluster-bootstrap replicates; interval not reported."}
    lo, hi = np.quantile(diffs, [0.025, 0.975])
    return {"valid_replicates": len(diffs), "ci95_low": float(lo), "ci95_high": float(hi),
            "unit": "split_group_id", "method": "paired_cluster_percentile_bootstrap"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", default=Path("results"), type=Path)
    ap.add_argument("--test-size", default=0.20, type=float)
    ap.add_argument("--seed", default=20261030, type=int)
    ap.add_argument("--bootstrap", default=2000, type=int)
    ap.add_argument("--snapshot-date", required=True, help="UTC citation snapshot date YYYY-MM-DD")
    ap.add_argument("--data-provenance", choices=["unverified", "synthetic", "student-adjudicated", "ai-provisional"],
                    default="unverified",
                    help="Provenance declaration; the script cannot independently authenticate labels")
    ap.add_argument("--preflight-only", action="store_true",
                    help="Write the split and dataset-gate report, but do not fit either model")
    ap.add_argument("--allow-ai-provisional-labels", action="store_true",
                    help="Amendment A3: accept label_status=ai_provisional; outputs are stamped as not human-verified")
    ap.add_argument("--exploratory-after-gate-failure", action="store_true",
                    help="Amendment A3: continue after a recorded gate FAIL; all outputs are labelled exploratory")
    args = ap.parse_args()
    if args.allow_ai_provisional_labels and args.data_provenance != "ai-provisional":
        raise ValueError("--allow-ai-provisional-labels requires --data-provenance ai-provisional")
    if not 0.1 <= args.test_size <= 0.4:
        raise ValueError("test-size must be between 0.10 and 0.40")
    if not args.output.exists():
        args.output.mkdir(parents=True, exist_ok=False)
    elif any(args.output.iterdir()):
        raise FileExistsError(
            f"Output directory is not empty: {args.output}. Use a new run directory; "
            "previous results must not be overwritten."
        )
    df = load_and_validate(args.input, allow_ai_provisional=args.allow_ai_provisional_labels)
    ai_provisional = bool((df.label_status.str.lower() == "ai_provisional").any())
    label_status_counts = {str(k): int(v) for k, v in df.label_status.str.lower().value_counts().items()}
    mixed_labels = ai_provisional and len(label_status_counts) > 1
    ai_stamp = ("MIXED_LABELS_REVIEWER_AND_AI_PROVISIONAL" if mixed_labels
                else "AI_PROVISIONAL_LABELS_NOT_HUMAN_VERIFIED")

    # Exposure-adjusted citation rate and median are computed once on the frozen pool.
    # The snapshot date is explicit so later reruns cannot silently change citation age.
    snapshot_ts = pd.Timestamp(args.snapshot_date, tz="UTC")
    snapshot_year = int(snapshot_ts.year)
    if snapshot_ts > pd.Timestamp.now(tz="UTC"):
        raise ValueError("snapshot-date cannot be in the future")
    df["citation_rate"] = df.citations / np.maximum(1, snapshot_year - df.year + 1)
    citation_median = float(df.citation_rate.median())
    df["low_citation"] = df.citation_rate <= citation_median

    # Frozen protocol: 5-fold stratified grouped split; fold 0=test, fold 1=validation,
    # folds 2-4=train. No seed retries are allowed to obtain preferred group counts.
    if args.test_size != 0.20:
        raise ValueError("Protocol v1.0 fixes the held-out test fold at approximately 20%; do not change test-size")
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=args.seed)
    folds = list(splitter.split(df, df.label, groups=df.split_group_id))
    test_idx = folds[0][1]
    val_idx = folds[1][1]
    train_idx = np.concatenate([folds[i][1] for i in (2, 3, 4)])
    train = df.iloc[train_idx].copy().reset_index(drop=True)
    validation = df.iloc[val_idx].copy().reset_index(drop=True)
    test = df.iloc[test_idx].copy().reset_index(drop=True)
    if (set(train.split_group_id) & set(test.split_group_id)
            or set(train.split_group_id) & set(validation.split_group_id)
            or set(test.split_group_id) & set(validation.split_group_id)):
        raise RuntimeError("Duplicate cluster leakage across partitions")
    if train.label.nunique() < 2:
        raise ValueError("Training split has only one class; enlarge/rebalance pool before modelling")
    if test.label.nunique() < 2:
        raise ValueError("Test split has only one class; revise the pool/split before modelling")
    if validation.label.nunique() < 2:
        raise ValueError("Validation split has only one class; revise the pool/split before modelling")

    low = test.low_citation.to_numpy(bool)
    high = ~low
    low_pos = int(np.sum((test.label.to_numpy() == 1) & low))
    high_pos = int(np.sum((test.label.to_numpy() == 1) & high))
    split_parts = {"train": train, "validation": validation, "test": test}
    split_positive_counts = {}
    split_rows = []
    for part_name, part in split_parts.items():
        low_group = part.low_citation.astype(bool)
        split_positive_counts[part_name] = {
            "lower_citation_relevant": int(((part.label == 1) & low_group).sum()),
            "higher_citation_relevant": int(((part.label == 1) & ~low_group).sum()),
            "total_relevant": int(part.label.sum()),
            "total_records": int(len(part)),
        }
        split_rows.extend({"openalex_id": row.openalex_id,
                           "split_group_id": row.split_group_id,
                           "split": part_name, "seed": args.seed}
                          for row in part[["openalex_id", "split_group_id"]].itertuples(index=False))
    gate_checks = {
        "at_least_100_deduplicated_rows": len(df) >= 100,
        "training_has_both_classes": train.label.nunique() == 2,
        "validation_has_both_classes": validation.label.nunique() == 2,
        "test_has_both_classes": test.label.nunique() == 2,
        "duplicate_clusters_do_not_cross_splits": not (
            set(train.split_group_id) & set(test.split_group_id)
            or set(train.split_group_id) & set(validation.split_group_id)
            or set(test.split_group_id) & set(validation.split_group_id)
        ),
        "test_has_at_least_20_lower_citation_relevant": low_pos >= 20,
        "test_has_at_least_20_higher_citation_relevant": high_pos >= 20,
    }
    gate_report = {
        "dataset_gate_status": "PASS" if all(gate_checks.values()) else "FAIL",
        "input_provenance_declaration": args.data_provenance,
        "input_file_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "protocol_split_seed": args.seed,
        "citation_snapshot_date": snapshot_ts.date().isoformat(),
        "citation_rate_median": citation_median,
        "n_total": int(len(df)),
        "split_positive_counts": split_positive_counts,
        "checks": gate_checks,
        "language_gate": "separate conditional gate: requires independently verified publication language and >=20 relevant test records per compared group",
        "note": "A PASS is a mechanical data gate only; it does not authenticate human labels, licences, or annotation quality.",
    }
    if args.preflight_only:
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "preflight_gate_report.json").write_text(
            json.dumps(gate_report, indent=2), encoding="utf-8")
        pd.DataFrame(split_rows).to_csv(args.output / "preflight_split_manifest.csv", index=False)
        profile_rows = []
        for part_name, part in split_parts.items():
            temp = part.copy()
            temp["split"] = part_name
            profile_rows.append(temp.groupby(
                ["split", "low_citation", "metadata_language", "label"], dropna=False
            ).size().reset_index(name="n"))
        pd.concat(profile_rows, ignore_index=True).to_csv(
            args.output / "preflight_group_profile.csv", index=False)
        print(json.dumps(gate_report, indent=2))
        return
    gate_failed = not all(gate_checks.values())
    if gate_failed and args.exploratory_after_gate_failure:
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "gate_report_FAILED.json").write_text(json.dumps(gate_report, indent=2), encoding="utf-8")
        pd.DataFrame(split_rows).to_csv(args.output / "split_manifest.csv", index=False)
    elif gate_failed:
        failed = [name for name, passed in gate_checks.items() if not passed]
        raise ValueError(
            f"Dataset acceptance gate failed: {failed}. Use --preflight-only to save the full gate report."
        )

    for part in (train, test):
        part["text"] = (part.title + " " + part.abstract).str.strip()
        part["log_citations"] = np.log1p(part.citations)
    y_train = train.label.to_numpy()
    y_test = test.label.to_numpy()
    lang = test.metadata_language.fillna("unknown").astype(str).to_numpy()
    predictions = test[["openalex_id", "year", "citations", "metadata_language",
                        "label", "low_citation", "split_group_id"]].copy()
    scores = {}
    metrics = {}
    run_times = {}
    for name, use_cites in [("citation_blind", False), ("citation_aware", True)]:
        model = make_pipeline(use_cites, args.seed)
        start = time.perf_counter()
        model.fit(train, y_train)
        fit_s = time.perf_counter() - start
        start = time.perf_counter()
        score = model.predict_proba(test)[:, 1]
        predict_s = time.perf_counter() - start
        scores[name] = score
        m, selected, order = rank_metrics(y_test, score, low, high, lang, test.openalex_id.to_numpy())
        metrics[name] = m
        predictions[f"score_{name}"] = score
        order_ids = np.lexsort((test.openalex_id.to_numpy(), -score))
        ranks = np.empty(len(score), dtype=int)
        ranks[order_ids] = np.arange(1, len(score) + 1)
        predictions[f"rank_{name}"] = ranks
        predictions[f"topk_{name}"] = selected
        run_times[name] = {"fit_seconds": fit_s, "predict_seconds": predict_s}

    delta = metrics["citation_blind"]["lower_citation_recall_at_k"] - metrics["citation_aware"]["lower_citation_recall_at_k"]
    boot = paired_cluster_bootstrap(
        y_test, scores["citation_blind"], scores["citation_aware"], low,
        test.openalex_id.to_numpy(), test.split_group_id.to_numpy(),
        args.bootstrap, 20261031
    )
    precision_delta = (metrics["citation_blind"]["overall_precision_at_k"]
                       - metrics["citation_aware"]["overall_precision_at_k"])
    lang_positive_counts = test.assign(_positive=(test.label == 1)).groupby(
        "metadata_language", dropna=False)["_positive"].sum().to_dict()
    language_verified = ("language_verification_status" in test.columns
                         and test["language_verification_status"].fillna("").astype(str).str.lower().eq("verified").all())
    language_confirmatory_eligible = bool(
        language_verified and len(lang_positive_counts) >= 2
        and all(int(v) >= 20 for k, v in lang_positive_counts.items()
                if str(k).lower() not in {"unknown", "nan", ""})
    )
    # Reporting guard added 5 Nov 2026 (Amendment A3 addendum) after a run with a single
    # lower-citation relevant test record produced a degenerate [1, 1] bootstrap interval.
    # It does not change any estimate; it only prevents the success rule from firing when
    # the primary denominator is too small for the comparison to be meaningful.
    primary_estimable = bool(metrics["citation_blind"]["lower_citation_relevant_n"] >= MIN_PRIMARY_DENOMINATOR)
    success_rule_met = bool(
        primary_estimable and
        delta > 0 and boot.get("ci95_low") is not None and boot["ci95_low"] > 0
        and precision_delta >= -0.05
    )
    pd.DataFrame([{
        "primary_metric": "lower_citation_recall_at_k",
        "citation_blind": metrics["citation_blind"]["lower_citation_recall_at_k"],
        "citation_aware": metrics["citation_aware"]["lower_citation_recall_at_k"],
        "delta_blind_minus_aware": float(delta),
        "paired_bootstrap_ci95_low": boot.get("ci95_low"),
        "paired_bootstrap_ci95_high": boot.get("ci95_high"),
        "valid_bootstrap_replicates": boot.get("valid_replicates"),
        "K": metrics["citation_blind"]["K"],
        "N_test": metrics["citation_blind"]["N_test"],
        "lower_citation_relevant_n": metrics["citation_blind"]["lower_citation_relevant_n"],
        "higher_citation_relevant_n": metrics["citation_blind"]["higher_citation_relevant_n"],
        "precision_delta_blind_minus_aware": float(precision_delta),
        "success_rule_met": success_rule_met,
        "primary_estimable": primary_estimable,
        "analysis_status": ("exploratory" if (gate_failed or ai_provisional) else "confirmatory"),
        "label_provenance": (("mixed_reviewer_and_ai_provisional" if mixed_labels else "ai_provisional_not_human_verified") if ai_provisional else args.data_provenance),
    }]).to_csv(args.output / "primary_comparison.csv", index=False)
    summary = {
        "status": ("SOFTWARE_SMOKE_TEST_ONLY" if args.data_provenance == "synthetic"
                   else "|".join(filter(None, [
                       "EXPLORATORY_GATE_FAILED" if gate_failed else "",
                       ai_stamp if ai_provisional else "",
                       "COMPUTATION_COMPLETED_INPUT_PROVENANCE_NOT_INDEPENDENTLY_AUTHENTICATED"]))),
        "confirmatory": not gate_failed and not ai_provisional,
        "label_status_counts": label_status_counts,
        "input_provenance_declaration": args.data_provenance,
        "input_file_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "dataset_gate": gate_report,
        "split_seed": args.seed,
        "model_seed": args.seed,
        "bootstrap_seed": 20261031,
        "bootstrap_unit": "split_group_id",
        "test_size": args.test_size,
        "citation_snapshot_date": snapshot_ts.date().isoformat(),
        "snapshot_year_used_for_age_adjustment": snapshot_year,
        "citation_rate_median": citation_median,
        "n_total": len(df), "n_train": len(train), "n_validation": len(validation), "n_test": len(test),
        "positive_total": int(df.label.sum()), "positive_train": int(train.label.sum()),
        "positive_test": int(test.label.sum()),
        "metrics": metrics,
        "primary_delta_blind_minus_aware_lower_citation_recall": float(delta),
        "precision_delta_blind_minus_aware": float(precision_delta),
        "primary_success_rule_met": success_rule_met,
        "primary_estimable": primary_estimable,
        "min_primary_denominator": MIN_PRIMARY_DENOMINATOR,
        "language_group_positive_counts_test": {str(k): int(v) for k, v in lang_positive_counts.items()},
        "language_confirmatory_eligible": language_confirmatory_eligible,
        "language_analysis_status": "confirmatory_gate_passed" if language_confirmatory_eligible else "descriptive_only_metadata_language_not_fully_verified_or_group_counts_insufficient",
        "success_rule": "delta_low > 0, 95% paired bootstrap lower bound > 0, and "
                        "citation-blind Precision@K is no more than 0.05 absolute points below citation-aware",
        "paired_bootstrap": boot,
        "runtime": run_times,
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "pandas": pd.__version__, "numpy": np.__version__,
                        "scikit_learn": sklearn.__version__},
        "interpretation_limit": "All recall values are relative to the constructed candidate pool. "
                                "Language metrics are descriptive unless metadata language is audited "
                                "and group positive-count gates pass.",
    }
    # Figures are generated only from the actual saved metrics for this run.
    metric_names = ["overall_recall_at_k", "lower_citation_recall_at_k", "overall_precision_at_k"]
    metric_labels = ["Overall Recall@K", "Lower-citation Recall@K", "Precision@K"]
    x = np.arange(len(metric_names))
    width = 0.36
    fig, ax = plt.subplots(figsize=(9, 5))
    vals_a = [metrics["citation_blind"][m] for m in metric_names]
    vals_b = [metrics["citation_aware"][m] for m in metric_names]
    ax.bar(x - width / 2, vals_a, width, label="Citation-blind")
    ax.bar(x + width / 2, vals_b, width, label="Citation-aware")
    ax.set_ylabel("Metric value")
    ax.set_ylim(0, 1)
    ax.set_xticks(x, metric_labels, rotation=10, ha="right")
    ax.legend()
    ax.set_title("Primary ranking metrics at the frozen top-K cutoff")
    fig.tight_layout()
    fig.savefig(args.output / "Figure_1_primary_metrics.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    group_labels = ["Lower citation", "Higher citation"]
    vals_a = [metrics["citation_blind"]["lower_citation_recall_at_k"],
              metrics["citation_blind"]["higher_citation_recall_at_k"]]
    vals_b = [metrics["citation_aware"]["lower_citation_recall_at_k"],
              metrics["citation_aware"]["higher_citation_recall_at_k"]]
    x = np.arange(2)
    ax.bar(x - width / 2, vals_a, width, label="Citation-blind")
    ax.bar(x + width / 2, vals_b, width, label="Citation-aware")
    ax.set_ylabel("Recall@K")
    ax.set_ylim(0, 1)
    ax.set_xticks(x, group_labels)
    ax.legend()
    ax.set_title("Recall@K by citation group (show denominators in table)")
    fig.tight_layout()
    fig.savefig(args.output / "Figure_2_citation_group_recall.png", dpi=200)
    plt.close(fig)

    # Prespecified sensitivity cutoffs (10% and 30%); 20% remains primary.
    sensitivity_rows = []
    for fraction in (0.10, 0.30):
        for name in ("citation_blind", "citation_aware"):
            m, _, _ = rank_metrics(y_test, scores[name], low, high, lang,
                                   test.openalex_id.to_numpy(), fraction=fraction)
            sensitivity_rows.append({"cutoff_fraction": fraction, "condition": name, **m})
    pd.DataFrame(sensitivity_rows).to_csv(args.output / "sensitivity_metrics.csv", index=False)

    # Transparent record-level disagreement table for manual review; it is not auto-adjudication.
    top_a = predictions["topk_citation_blind"].to_numpy(bool)
    top_b = predictions["topk_citation_aware"].to_numpy(bool)
    changed = top_a != top_b
    errors = predictions.loc[changed, ["openalex_id", "label", "low_citation",
                                       "metadata_language", "score_citation_blind",
                                       "score_citation_aware", "rank_citation_blind",
                                       "rank_citation_aware", "topk_citation_blind",
                                       "topk_citation_aware"]].copy()
    errors["review_status"] = "requires_human_error_review"
    errors.to_csv(args.output / "error_analysis.csv", index=False)

    # Dataset profile with explicit denominators; no abstract text is exported.
    profile = df.groupby(["low_citation", "metadata_language", "label"], dropna=False).size().reset_index(name="n")
    profile.to_csv(args.output / "dataset_profile.csv", index=False)
    resource_rows = [{"condition": name, **times} for name, times in run_times.items()]
    pd.DataFrame(resource_rows).to_csv(args.output / "resource_metrics.csv", index=False)

    split_rows = []
    for part_name, part in [("train", train), ("validation", validation), ("test", test)]:
        split_rows.extend({"openalex_id": row.openalex_id,
                           "split_group_id": row.split_group_id,
                           "split": part_name, "seed": args.seed}
                          for row in part[["openalex_id", "split_group_id"]].itertuples(index=False))
    pd.DataFrame(split_rows).to_csv(args.output / "split_manifest.csv", index=False)
    manifest_cols = [c for c in ["openalex_id", "doi", "title", "year", "citations",
                                  "metadata_language", "original_metadata_language",
                                  "language_verification_status", "label", "label_status",
                                  "label_rationale", "labeler_id", "split_group_id",
                                  "source_routes", "collection_timestamp", "citation_snapshot_date",
                                  "citation_rate", "low_citation"] if c in df.columns]
    df[manifest_cols].to_csv(args.output / "dataset_manifest.csv", index=False)
    predictions.to_csv(args.output / "test_predictions.csv", index=False)
    pd.DataFrame([{"condition": k, **v} for k, v in metrics.items()]).to_csv(args.output / "primary_metrics.csv", index=False)
    subgroup_rows = []
    for condition, values in metrics.items():
        for group_name, recall_key, n_key in [
            ("lower_citation", "lower_citation_recall_at_k", "lower_citation_relevant_n"),
            ("higher_citation", "higher_citation_recall_at_k", "higher_citation_relevant_n"),
        ]:
            subgroup_rows.append({"condition": condition, "group_type": "citation",
                                  "group": group_name, "relevant_n": values[n_key],
                                  "recall_at_k": values[recall_key]})
        for key, value in values.items():
            if key.startswith("language_recall::"):
                lang_group = key.split("::", 1)[1]
                subgroup_rows.append({"condition": condition, "group_type": "metadata_language",
                                      "group": lang_group,
                                      "relevant_n": values.get(f"language_relevant_n::{lang_group}", 0),
                                      "recall_at_k": value})
    pd.DataFrame(subgroup_rows).to_csv(args.output / "subgroup_metrics.csv", index=False)
    (args.output / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.output / "environment.txt").write_text(json.dumps(summary["environment"], indent=2), encoding="utf-8")
    (args.output / "run_log.txt").write_text(
        f"Command: python src/run_experiment.py --input {args.input} --output {args.output} "
        f"--test-size {args.test_size} --seed {args.seed} --bootstrap {args.bootstrap} "
        f"--snapshot-date {args.snapshot_date} --data-provenance {args.data_provenance}\n"
        f"Input provenance declaration: {args.data_provenance} (not independently authenticated by script)\n"
        f"Input SHA-256: {summary['input_file_sha256']}\n"
        f"UTC completed: {pd.Timestamp.now(tz='UTC').isoformat()}\n"
        f"Rows: {len(df)}; train: {len(train)}; test: {len(test)}\n"
        f"Primary delta (blind - aware): {delta:.6f}\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
