#!/usr/bin/env python3
"""Rebuild every figure in the paper from result files, live (for the viva).

    python scripts/make_all_figures.py            # rebuild all three figures and open them
    python scripts/make_all_figures.py --no-open  # rebuild only

Figures 1 and 2 (Study 1) are drawn from the cross-fitted results. If `scripts/viva_demo.py --data ...`
has just been run, the freshly retrained results in results/_viva_check/crossfit are used, so the chain
"retrain the rankers -> draw the figure" happens in front of the examiner; otherwise the committed results
are used. Figure 3 (Study 2) is drawn from the committed per-review results.

Output: results/_figures_check/ (never committed). The figures in paper/ are the ones in the PDF.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "_figures_check"
FRESH = ROOT / "results" / "_viva_check" / "crossfit"
COMMITTED = ROOT / "results" / "run_20261105_reviewed_crossfit"
STUDY2 = ROOT / "results" / "study2_confirmatory"


def open_file(p: Path) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(p))  # noqa: S606 - opens the image in the default viewer
        elif sys.platform == "darwin":
            subprocess.run(["open", str(p)], check=False)
        else:
            subprocess.run(["xdg-open", str(p)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:  # opening is a convenience only
        print(f"  (could not open {p.name}: {e})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    s1 = FRESH if (FRESH / "crossfit_relevant_records_ranks.csv").exists() else COMMITTED
    print(f"Study 1 figures from: {s1.relative_to(ROOT)}"
          + ("   (freshly retrained in this session)" if s1 == FRESH else "   (committed results)"))
    subprocess.run([sys.executable, str(ROOT / "src" / "make_figures.py"), str(s1), str(OUT)], check=True)
    print(f"Study 2 figure from:  {STUDY2.relative_to(ROOT)}")
    subprocess.run([sys.executable, str(ROOT / "src" / "make_study2_figure.py"), str(STUDY2), str(OUT)], check=True)

    m = pd.read_csv(s1 / "crossfit_pooled_metrics.csv")
    m = m[(m.k_fraction == 0.2) & (m.group == "lower_citation")].set_index("condition")
    d = pd.read_csv(STUDY2 / "study2_per_dataset.csv")
    den = pd.read_csv(STUDY2 / "study2_per_dataset.csv").query("condition == 'citation_blind'").set_index("dataset").den_low
    d = d[d.condition.isin(["citation_blind", "citation_aware"])].pivot(index="dataset", columns="condition", values="low")
    d = d[den.reindex(d.index) > 0]  # reviews with at least one rarely cited relevant paper (19 of 20)
    better = int((d.citation_blind > d.citation_aware).sum())
    same = int((d.citation_blind == d.citation_aware).sum())
    worse = int((d.citation_blind < d.citation_aware).sum())

    figs = [
        ("fig_recall_by_group", "Figure 1 (paper Fig. 1): Study 1 Recall@20% by citation group",
         f"lower-citation bars: blind {int(m.loc['citation_blind', 'relevant_in_topk'])}/{int(m.loc['citation_blind', 'relevant'])}, "
         f"aware {int(m.loc['citation_aware', 'relevant_in_topk'])}/{int(m.loc['citation_aware', 'relevant'])}"),
        ("fig_rank_shift_lower_citation", "Figure 2 (paper Fig. 2): where the rarely cited relevant papers were ranked",
         "each line is one paper: its rank without vs with the citation feature"),
        ("fig_study2_per_review", "Figure 3 (paper Fig. 3): Study 2 rarely cited recall in each review",
         f"of {len(d)} reviews with rarely cited relevant papers: blind better in {better}, same in {same}, worse in {worse}"),
    ]
    print()
    for name, title, note in figs:
        pdf, png = OUT / f"{name}.pdf", OUT / f"{name}.png"
        ok = pdf.exists() and png.exists()
        print(f"{'OK ' if ok else 'MISSING'} {title}\n      {note}\n      -> {png.relative_to(ROOT)}")
        if ok and not a.no_open:
            open_file(png)
    print(f"\nAll figures rebuilt in {OUT.relative_to(ROOT)}. The paper uses the PDFs of the same names in paper/.")


if __name__ == "__main__":
    main()
