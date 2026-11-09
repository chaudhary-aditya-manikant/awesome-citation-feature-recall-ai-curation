#!/usr/bin/env bash
# Re-run the full analysis on a labelled model-input CSV.
# Usage:  bash code/run_all_provisional.sh <model_input.csv> <run_tag> [ai]
#   third argument "ai" = AI-provisional labels (adds the provenance flags).
# After your own verification, export labels with label_status=single_reviewer_audited
# and run without the third argument.
set -euo pipefail
IN="$1"; TAG="$2"; MODE="${3:-human}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
EXTRA=(); CF=()
if [ "$MODE" = "ai" ]; then EXTRA=(--data-provenance ai-provisional --allow-ai-provisional-labels); CF=(--allow-ai-provisional-labels);
else EXTRA=(--data-provenance student-adjudicated); fi
python code/run_experiment.py --input "$IN" --output "results/${TAG}_preflight" --snapshot-date 2026-10-30 "${EXTRA[@]}" --preflight-only
python code/run_experiment.py --input "$IN" --output "results/${TAG}_frozen" --snapshot-date 2026-10-30 "${EXTRA[@]}" --exploratory-after-gate-failure
(cd code && python run_crossfit_exploratory.py --input "../$IN" --output "../results/${TAG}_crossfit" --snapshot-date 2026-10-30 "${CF[@]}")
python code/make_figures.py "results/${TAG}_crossfit" "results/${TAG}_crossfit/figures"
echo "Done. If the preflight gate PASSES, report the frozen run as confirmatory and the cross-fit as secondary."
