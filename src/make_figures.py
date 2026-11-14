"""Generate manuscript figures from saved cross-fitted outputs (no recomputation)."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

run = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
C = {"citation_blind": "#1b6ca8", "citation_aware": "#d97b29"}
L = {"citation_blind": "Citation-blind (A)", "citation_aware": "Citation-aware (B)"}

m = pd.read_csv(run / "crossfit_pooled_metrics.csv"); m = m[m.k_fraction == 0.20]
groups = [("lower_citation", "Lower-citation"), ("higher_citation", "Higher-citation"), ("overall", "All relevant")]
fig, ax = plt.subplots(figsize=(5.2, 2.9))
for j, (cond, _) in enumerate(C.items()):
    vals = [m[(m.condition == cond) & (m.group == g)].iloc[0] for g, _ in groups]
    xs = [i + (j - 0.5) * 0.36 for i in range(3)]
    ax.bar(xs, [v.recall_at_k for v in vals], 0.34, color=C[cond], label=L[cond])
    for x, v in zip(xs, vals):
        ax.text(x, v.recall_at_k + 0.02, f"{int(v.relevant_in_topk)}/{int(v.relevant)}", ha="center", fontsize=7.5)
ax.set_xticks(range(3), [g[1] for g in groups]); ax.set_ylim(0, 1.3); ax.set_ylabel("Pooled Recall@20%"); ax.set_yticks([0, .2, .4, .6, .8, 1.0])
ax.legend(frameon=False, fontsize=7.5, loc="upper center", ncol=2); fig.tight_layout()
fig.savefig(out / "fig_recall_by_group.pdf"); fig.savefig(out / "fig_recall_by_group.png", dpi=200); plt.close(fig)

p = pd.read_csv(run / "crossfit_relevant_records_ranks.csv"); lo = p[p.low_citation].sort_values("rank_in_fold_citation_blind")
fig, ax = plt.subplots(figsize=(5.2, 2.9))
label_y, last = [], -1e9
for y in sorted(lo.rank_in_fold_citation_aware):
    last = max(y, last + 16); label_y.append(last)
pos = dict(zip(sorted(lo.rank_in_fold_citation_aware.index, key=lambda i: lo.loc[i, "rank_in_fold_citation_aware"]), label_y))
for i, r in lo.iterrows():
    ax.plot([0, 1], [r.rank_in_fold_citation_blind, r.rank_in_fold_citation_aware], color="#7f7f7f", lw=1)
    ax.scatter([0], [r.rank_in_fold_citation_blind], color=C["citation_blind"], zorder=3, s=18)
    ax.scatter([1], [r.rank_in_fold_citation_aware], color=C["citation_aware"], zorder=3, s=18)
    ax.plot([1.01, 1.06], [r.rank_in_fold_citation_aware, pos[i]], color="#bbbbbb", lw=0.6)
    ax.text(1.08, pos[i], f"{r.screening_id} ({int(r.citations)} cit.)", va="center", fontsize=7)
ax.axhline(111, ls="--", lw=0.8, color="black"); ax.text(-0.18, 104, "top-K cutoff (K = 111)", ha="left", fontsize=7.5)
ax.set_xlim(-0.2, 1.6); ax.set_xticks([0, 1], [L["citation_blind"], L["citation_aware"]])
ax.invert_yaxis(); ax.set_ylabel("Rank within test fold (1 = top)"); fig.tight_layout()
fig.savefig(out / "fig_rank_shift_lower_citation.pdf"); fig.savefig(out / "fig_rank_shift_lower_citation.png", dpi=200); plt.close(fig)
print("figures written to", out)
