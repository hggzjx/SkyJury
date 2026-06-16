#!/usr/bin/env bash
set -euo pipefail

METHOD="${1:-e5}"
PREDICTION_ROOT="${2:-/ssd1/lbh/zjx/skyjury/auditor/results/similarity_predictions}"
DATA_PREFIX="${3:-skyjury_bench}"
OUTPUT_DIR="${4:-/ssd1/lbh/zjx/skyjury/auditor/results/similarity_reports/${METHOD}}"
ALLOW_SUBSET="${ALLOW_SUBSET:-1}"

latest_prediction() {
  local dir="$1"
  find "$dir" -maxdepth 1 -name '*_predictions.json' -type f | sort | tail -n 1
}

BASE_DIR="${PREDICTION_ROOT}/${METHOD}/base"
LENGTH_DIR="${PREDICTION_ROOT}/${METHOD}/length"
LANGUAGE_DIR="${PREDICTION_ROOT}/${METHOD}/language"

ORIGINAL_PREDICTIONS="$(latest_prediction "$BASE_DIR")"
LENGTH_PREDICTIONS="$(latest_prediction "$LENGTH_DIR")"
LANGUAGE_PREDICTIONS="$(latest_prediction "$LANGUAGE_DIR")"

if [[ -z "$ORIGINAL_PREDICTIONS" || -z "$LENGTH_PREDICTIONS" || -z "$LANGUAGE_PREDICTIONS" ]]; then
  echo "Could not locate one or more similarity prediction files for ${METHOD}." >&2
  echo "base=$ORIGINAL_PREDICTIONS" >&2
  echo "length=$LENGTH_PREDICTIONS" >&2
  echo "language=$LANGUAGE_PREDICTIONS" >&2
  exit 1
fi

cd /ssd1/lbh/zjx/skyjury/auditor

subset_arg=()
if [[ "$ALLOW_SUBSET" == "1" ]]; then
  subset_arg=(--allow-subset)
fi

python audit_predictions.py \
  --method similarity \
  --original "$ORIGINAL_PREDICTIONS" \
  --perturbed "length=${LENGTH_PREDICTIONS}" \
  --perturbed "language=${LANGUAGE_PREDICTIONS}" \
  --output-dir "$OUTPUT_DIR" \
  --report-name "similarity_${METHOD}_rubric_robustness" \
  "${subset_arg[@]}"

python audit_cross_candidate_perturbations.py \
  --method similarity \
  --original "$ORIGINAL_PREDICTIONS" \
  --perturbed "length=${LENGTH_PREDICTIONS}" \
  --perturbed "language=${LANGUAGE_PREDICTIONS}" \
  --output-dir "$OUTPUT_DIR" \
  --report-name "similarity_${METHOD}_cross_candidate_rubric_robustness" \
  "${subset_arg[@]}"
