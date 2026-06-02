#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1}"
DATA_PATH="${2:-/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json}"
DEVICE="${DEVICE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-1}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
OUTPUT_DIR="${OUTPUT_DIR:-/ssd1/lbh/zjx/skyjury/verifier/results/reward_models}"
DEVICE_MAP="${DEVICE_MAP:-none}"
LIMIT_ARGS=()
if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

python run_reward_model.py \
  --model "$MODEL_PATH" \
  --data "$DATA_PATH" \
  --output-dir "$OUTPUT_DIR" \
  --batch-size "$BATCH_SIZE" \
  --max-length "$MAX_LENGTH" \
  --device "$DEVICE" \
  --torch-dtype "$TORCH_DTYPE" \
  --device-map "$DEVICE_MAP" \
  --local-files-only \
  "${LIMIT_ARGS[@]}"
