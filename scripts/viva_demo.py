#!/usr/bin/env python3
"""Live demonstration for the viva: re-run the analysis and prove it reproduces the committed results.

Works on Windows, macOS, Linux and Colab (no bash needed). Run from the project folder:

    python scripts/viva_demo.py                      # part A: tests + post-hoc rankers + Study 2 table (public files only)
    python scripts/viva_demo.py --data data/private/model_input_reviewed_20261105_private.csv
                                                     # part A + part B: full cross-fitted analysis from raw labels

Outputs go to results/_viva_check/ (deleted and rebuilt each time, never committed).
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "results" / "_viva_check"
COMMITTED = ROOT / "results" / "run_20261105_reviewed"


def step(title: str) -> None:
    print("\n" + "=" * 72 + f"\n{title}\n" + "=" * 72, flush=True)


def run(args: list[str], cwd: Path = ROOT, quiet: bool = True) -> None:
    """Run one pipeline step; its detailed output goes to results/_viva_check/log.txt."""
    if not quiet:
        subprocess.run([sys.executable, *args], cwd=cwd, check=True)
        return
    with open(CHECK / "log.txt", "a", encoding="utf-8") as log:
        r = subprocess.run([sys.executable, *args], cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
    if r.returncode:
        raise SystemExit(f"Step failed: {' '.join(args)} (see results/_viva_check/log.txt)")
    print(f"  ok: {Path(args[0]).name if not args[0].startswith('-') else 'pytest'}")


def same(new: Path, old: Path) -> bool:
    ok = filecmp.cmp(new, old, shallow=False)
    print(f"  {'IDENTICAL' if ok else 'DIFFERENT'}  {new.name}  vs committed {old.parent.name}/{old.name}")
    return ok


def show(csv: Path, k: float = 0.2) -> None:
    import pandas as pd
    d = pd.read_csv(csv)
    if "k_fraction" in d.columns:
        d = d[d.k_fraction == k]
    print(d.to_string(index=False))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, help="private model input with abstracts (enables part B)")
    ap.add_argument("--skip-tests", action="store_true")
    a = ap.parse_args()
    if CHECK.exists():
        shutil.rmtree(CHECK)
    CHECK.mkdir(parents=True)
    t0, all_ok = time.time(), True

    if not a.skip_tests:
        step("1. Automated tests")
        run(["-m", "pytest", "-q", "tests"], quiet=False)

    step("2. Post-hoc reference rankers, re-run from the committed predictions")
    run(["run_posthoc_comparators.py",
         "--predictions", "../results/run_20261105_reviewed_crossfit/crossfit_out_of_fold_predictions.csv",
         "--groups", "../data/collection_audit_20261031/data/shareable/candidate_pool_audited_shareable.csv",
         "--output", str(CHECK / "posthoc")], cwd=ROOT / "src")
    for f in ("posthoc_pooled_metrics.csv", "posthoc_paired_contrasts.csv"):
        all_ok &= same(CHECK / "posthoc" / f, ROOT / "results/run_20261105_reviewed_posthoc_comparators" / f)

    if a.data:
        step("3. Full cross-fitted analysis from the labelled data (both rankers refitted)")
        data = a.data.resolve()
        run(["src/run_experiment.py", "--input", str(data), "--output", str(CHECK / "preflight"),
             "--snapshot-date", "2026-10-30", "--data-provenance", "ai-provisional",
             "--allow-ai-provisional-labels", "--preflight-only"])
        run(["run_crossfit_exploratory.py", "--input", str(data), "--output", str(CHECK / "crossfit"),
             "--snapshot-date", "2026-10-30", "--allow-ai-provisional-labels"], cwd=ROOT / "src")
        for f in ("crossfit_pooled_metrics.csv", "crossfit_paired_contrasts.csv"):
            all_ok &= same(CHECK / "crossfit" / f, Path(f"{COMMITTED}_crossfit") / f)
        print("\nRecall@20% by citation group:")
        show(CHECK / "crossfit" / "crossfit_pooled_metrics.csv")
        print("\nPaired difference, citation-blind minus citation-aware:")
        show(CHECK / "crossfit" / "crossfit_paired_contrasts.csv")
    else:
        print("\n(Part B skipped: pass --data <private model input> to refit both rankers live.)")

    step("4. Study 2 (SYNERGY): rebuild the confirmatory table from the committed scores for 150,154 records")
    r = subprocess.run([sys.executable, "study2_verify_from_scores.py", "--results", "../results/study2_confirmatory",
                        "--protocol", "../configs/study2_protocol.json", "--bootstrap", "0"], cwd=ROOT / "src")
    all_ok &= r.returncode == 0

    step("Summary")
    print("Post-hoc rankers at K = 20%:")
    show(CHECK / "posthoc" / "posthoc_pooled_metrics.csv")
    print(f"\nAll re-run outputs identical to committed results: {all_ok}   ({time.time() - t0:.0f} s)")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
