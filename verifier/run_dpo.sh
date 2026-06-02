#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-13b}"
DATA_PATH="${2:-/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json}"
REF_MODEL_PATH="${3:-/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-7b}"
DEVICE="${DEVICE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-1}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
MAX_PROMPT_LENGTH="${MAX_PROMPT_LENGTH:-1024}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
DEVICE_MAP="${DEVICE_MAP:-auto}"
OUTPUT_DIR="${OUTPUT_DIR:-/ssd1/lbh/zjx/skyjury/verifier/results/dpo_models/$(basename "$MODEL_PATH")}"
LIMIT_ARGS=()
if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

cmd=(python run_dpo_lm.py
  --model "$MODEL_PATH"
  --data "$DATA_PATH"
  --output-dir "$OUTPUT_DIR"
  --batch-size "$BATCH_SIZE"
  --max-length "$MAX_LENGTH"
  --max-prompt-length "$MAX_PROMPT_LENGTH"
  --device "$DEVICE"
  --torch-dtype "$TORCH_DTYPE"
  --device-map "$DEVICE_MAP"
  --local-files-only)

if [[ -n "$REF_MODEL_PATH" ]]; then
  cmd+=(--ref-model "$REF_MODEL_PATH")
fi
cmd+=("${LIMIT_ARGS[@]}")

"${cmd[@]}"
