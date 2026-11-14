#!/usr/bin/env python3
"""Figure for Study 2: lower-citation Recall@20% per SYNERGY review, citation-blind vs citation-aware."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def main(results: Path, out: Path) -> None:
    d = pd.read_csv(results / "study2_per_dataset.csv")
    w = d.pivot(index="dataset", columns="condition", values=["low", "den_low"])
    t = pd.DataFrame({"n": w["den_low"]["citation_blind"], "blind": w["low"]["citation_blind"],
                      "aware": w["low"]["citation_aware"]})
    t = t[t.n >= 5].assign(rb=lambda x: x.blind / x.n, ra=lambda x: x.aware / x.n).sort_values("n")
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    y = range(len(t))
    for i, (_, r) in enumerate(t.iterrows()):
        ax.plot([r.ra, r.rb], [i, i], color="#9aa0a6", lw=1.2, zorder=1)
    ax.scatter(t.ra, y, marker="s", s=34, color="#b3541e", label="Citation-aware", zorder=2)
    ax.scatter(t.rb, y, marker="o", s=34, color="#1f5fa8", label="Citation-blind", zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{k.replace('_', ' ')} (n={int(n)})" for k, n in zip(t.index, t.n)], fontsize=7.5)
    ax.set_xlabel("Lower-citation Recall@20%")
    ax.set_xlim(-0.03, 1.03)
    ax.grid(axis="x", color="#e3e3e3", lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout()
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "fig_study2_per_review.pdf")
    fig.savefig(out / "fig_study2_per_review.png", dpi=200)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
