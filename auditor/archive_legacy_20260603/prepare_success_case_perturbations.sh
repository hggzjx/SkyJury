#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${1:-/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json}"
VERIFIER_PREDICTIONS="${2:?Usage: prepare_success_case_perturbations.sh <data_json> <verifier_predictions_json> [output_dir] [prefix]}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/data/auditor}"
PREFIX="${4:-verifier_success_cases}"

cd /ssd1/lbh/zjx/skyjury/auditor

python build_rubric_perturbations.py \
  --data "$DATA_PATH" \
  --verifier-predictions "$VERIFIER_PREDICTIONS" \
  --success-only \
  --output-dir "$OUTPUT_DIR" \
  --prefix "$PREFIX"
