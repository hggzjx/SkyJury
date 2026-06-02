#!/usr/bin/env bash
set -euo pipefail

METHOD="${1:?Usage: run_audit_report.sh <rm|dpo|llm_judge> <original_predictions> <length_predictions> <language_predictions> <length_language_predictions> [output_dir]}"
ORIGINAL_PREDICTIONS="${2:?Missing original predictions JSON}"
LENGTH_PREDICTIONS="${3:?Missing length perturbation predictions JSON}"
LANGUAGE_PREDICTIONS="${4:?Missing language perturbation predictions JSON}"
LENGTH_LANGUAGE_PREDICTIONS="${5:?Missing length+language perturbation predictions JSON}"
OUTPUT_DIR="${6:-/ssd1/lbh/zjx/skyjury/auditor/results}"
ALLOW_SUBSET="${ALLOW_SUBSET:-1}"

cd /ssd1/lbh/zjx/skyjury/auditor

python audit_predictions.py \
  --method "$METHOD" \
  --original "$ORIGINAL_PREDICTIONS" \
  --perturbed "length=${LENGTH_PREDICTIONS}" \
  --perturbed "language=${LANGUAGE_PREDICTIONS}" \
  --perturbed "length_language=${LENGTH_LANGUAGE_PREDICTIONS}" \
  --output-dir "$OUTPUT_DIR" \
  --report-name "${METHOD}_rubric_robustness" \
  $([[ "$ALLOW_SUBSET" == "1" ]] && printf '%s' '--allow-subset')
