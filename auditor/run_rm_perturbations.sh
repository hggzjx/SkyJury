#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-all}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/rm_predictions}"
DATA_PREFIX="${4:-skyjury_bench}"
DEVICE="${DEVICE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-4}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
DEVICE_MAP="${DEVICE_MAP:-none}"
LOCAL_FILES_ARGS=()
LIMIT_ARGS=()

DEFAULT_MODELS=(
  "/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft"
  "/ssd1/lbh/zjx/models/skyjury_verifier/openbmb_Eurus-RM-7b"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Llama-3.1-8B-v0.2"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Gemma-2-27B-v0.2"
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
  for perturbation in length language length_language; do
    DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
    PERTURBATION_OUTPUT_DIR="${OUTPUT_DIR}/$(basename "$model")/${perturbation}"
    echo "Running RM perturbation: model=$(basename "$model") perturbation=${perturbation} batch_size=${BATCH_SIZE}"
    python run_reward_model.py \
      --model "$model" \
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
done
