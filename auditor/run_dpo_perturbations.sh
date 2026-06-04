#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-all}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/dpo_predictions}"
REF_MODEL_PATH="${4:-/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-7b}"
DATA_PREFIX="${5:-skyjury_bench}"
DEVICE="${DEVICE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-4}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
MAX_PROMPT_LENGTH="${MAX_PROMPT_LENGTH:-1024}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
DEVICE_MAP="${DEVICE_MAP:-auto}"
REF_FREE_TYPE="${REF_FREE_TYPE:-avg}"
LOCAL_FILES_ARGS=()
LIMIT_ARGS=()

DEFAULT_MODELS=(
  "/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-13b"
  "/ssd1/lbh/zjx/models/skyjury_verifier/upstage_SOLAR-10.7B-Instruct-v1.0"
)

if [[ "${LOCAL_FILES_ONLY:-1}" == "1" ]]; then
  LOCAL_FILES_ARGS=(--local-files-only)
fi
if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

if [[ "$MODEL_PATH" == "all" ]]; then
  MODELS=("${DEFAULT_MODELS[@]}")
else
  MODELS=("$MODEL_PATH")
fi

for model in "${MODELS[@]}"; do
  for perturbation in length language; do
    DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
    PERTURBATION_OUTPUT_DIR="${OUTPUT_DIR}/$(basename "$model")/${perturbation}"
    echo "Running DPO perturbation: model=$(basename "$model") perturbation=${perturbation} batch_size=${BATCH_SIZE}"
    cmd=(python run_dpo_lm.py
      --model "$model"
      --data "$DATA_PATH"
      --batch-size "$BATCH_SIZE"
      --max-length "$MAX_LENGTH"
      --max-prompt-length "$MAX_PROMPT_LENGTH"
      --device "$DEVICE"
      --torch-dtype "$TORCH_DTYPE"
      --device-map "$DEVICE_MAP"
      --ref-free-type "$REF_FREE_TYPE"
      --output-dir "$PERTURBATION_OUTPUT_DIR"
      "${LOCAL_FILES_ARGS[@]}")

    if [[ -n "$REF_MODEL_PATH" ]]; then
      cmd+=(--ref-model "$REF_MODEL_PATH")
    fi
    cmd+=("${LIMIT_ARGS[@]}")

    "${cmd[@]}"
  done
done
