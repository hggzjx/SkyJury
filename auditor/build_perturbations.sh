#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${1:-/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json}"
OUTPUT_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor}"
VERIFIER_PREDICTIONS="${3:-}"
PREFIX="${4:-}"

cd /ssd1/lbh/zjx/skyjury/auditor
cmd=(python build_rubric_perturbations.py
  --data "$DATA_PATH"
  --output-dir "$OUTPUT_DIR")

if [[ -n "$VERIFIER_PREDICTIONS" ]]; then
  cmd+=(--verifier-predictions "$VERIFIER_PREDICTIONS" --success-only)
fi

if [[ -n "$PREFIX" ]]; then
  cmd+=(--prefix "$PREFIX")
fi

"${cmd[@]}"
