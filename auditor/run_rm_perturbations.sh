#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/rm_predictions}"
DATA_PREFIX="${4:-verifier_pilot_rmbench}"
DEVICE="${DEVICE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-1}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
DEVICE_MAP="${DEVICE_MAP:-none}"
LOCAL_FILES_ARGS=()
LIMIT_ARGS=()

if [[ "${LOCAL_FILES_ONLY:-1}" == "1" ]]; then
  LOCAL_FILES_ARGS=(--local-files-only)
fi
if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for perturbation in length language length_language; do
  DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
  PERTURBATION_OUTPUT_DIR="${OUTPUT_DIR}/$(basename "$MODEL_PATH")/${perturbation}"
  python run_reward_model.py \
    --model "$MODEL_PATH" \
    --data "$DATA_PATH" \
    --batch-size "$BATCH_SIZE" \
    --max-length "$MAX_LENGTH" \
    --device "$DEVICE" \
    --torch-dtype "$TORCH_DTYPE" \
    --device-map "$DEVICE_MAP" \
    --output-dir "$PERTURBATION_OUTPUT_DIR" \
    "${LOCAL_FILES_ARGS[@]}" \
    "${LIMIT_ARGS[@]}"
done
