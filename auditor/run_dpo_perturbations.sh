#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-/ssd1/lbh/zjx/models/skyjury_verifier/HuggingFaceH4_zephyr-7b-beta}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/dpo_predictions}"
REF_MODEL_PATH="${4:-}"
DATA_PREFIX="${5:-verifier_pilot_rmbench}"
DEVICE="${CUDA_VISIBLE_DEVICES:-auto}"

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for perturbation in length language length_language; do
  DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
  cmd=(python run_dpo_lm.py
    --model "$MODEL_PATH"
    --data "$DATA_PATH"
    --max-length 2048
    --device "$DEVICE"
    --output-dir "$OUTPUT_DIR")

  if [[ -n "$REF_MODEL_PATH" ]]; then
    cmd+=(--ref-model "$REF_MODEL_PATH")
  fi

  "${cmd[@]}"
done
