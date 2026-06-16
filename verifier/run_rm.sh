#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${1:-/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json}"
CUDA_DEVICES="${CUDA_DEVICES:-0,1,2,3}"
DEVICE="${DEVICE:-cuda}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/ssd1/lbh/zjx/skyjury/verifier/results/reward_models}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
DEVICE_MAP="${DEVICE_MAP:-auto}"
PROMPT_TEMPLATE="${PROMPT_TEMPLATE:-default}"

MODELS=(
  "/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft"
  "/ssd1/lbh/zjx/models/skyjury_verifier/openbmb_Eurus-RM-7b"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Llama-3.1-8B-v0.2"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Gemma-2-27B-v0.2"
)

batch_size_for_model() {
  local model="$1"
  case "$model" in
    *Skywork-Reward-Gemma-2-27B-v0.2*) echo "${SKYWORK_BATCH_SIZE:-4}" ;;
    *Skywork-Reward-Llama-3.1-8B-v0.2*) echo "${SKYWORK_LLAMA_BATCH_SIZE:-8}" ;;
    *ArmoRM-Llama3-8B-v0.1*) echo "${ARMORM_BATCH_SIZE:-4}" ;;
    *GRM_Llama3.1_8B_rewardmodel-ft*) echo "${GRM_BATCH_SIZE:-4}" ;;
    *Eurus-RM-7b*) echo "${EURUS_BATCH_SIZE:-4}" ;;
    *) echo "${BATCH_SIZE:-4}" ;;
  esac
}

cuda_devices_for_model() {
  local model="$1"
  case "$model" in
    *ArmoRM-Llama3-8B-v0.1*) echo "${ARMORM_CUDA_DEVICES:-0}" ;;
    *GRM_Llama3.1_8B_rewardmodel-ft*) echo "${GRM_CUDA_DEVICES:-1}" ;;
    *Eurus-RM-7b*) echo "${EURUS_CUDA_DEVICES:-2}" ;;
    *Skywork-Reward-Llama-3.1-8B-v0.2*) echo "${SKYWORK_LLAMA_CUDA_DEVICES:-3}" ;;
    *Skywork-Reward-Gemma-2-27B-v0.2*) echo "${SKYWORK_CUDA_DEVICES:-$CUDA_DEVICES}" ;;
    *) echo "$CUDA_DEVICES" ;;
  esac
}

device_map_for_model() {
  local model="$1"
  case "$model" in
    *Skywork-Reward-Gemma-2-27B-v0.2*) echo "${SKYWORK_DEVICE_MAP:-auto}" ;;
    *Skywork-Reward-Llama-3.1-8B-v0.2*) echo "${SKYWORK_LLAMA_DEVICE_MAP:-none}" ;;
    *) echo "${SINGLE_GPU_DEVICE_MAP:-none}" ;;
  esac
}

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier
mkdir -p "$OUTPUT_ROOT/logs"

echo "SkyJury RewardBench-compatible RM evaluation"
echo "data=$DATA_PATH"
echo "cuda_devices_pool=$CUDA_DEVICES"
echo "device=$DEVICE"
echo "max_length=$MAX_LENGTH"
echo "output_root=$OUTPUT_ROOT"
echo "prompt_template=$PROMPT_TEMPLATE"
echo

for model in "${MODELS[@]}"; do
  model_name="$(basename "$model")"
  model_output_dir="$OUTPUT_ROOT/$model_name"
  log_path="$OUTPUT_ROOT/logs/${model_name}.log"
  mkdir -p "$model_output_dir"
  batch_size="$(batch_size_for_model "$model")"
  model_cuda_devices="$(cuda_devices_for_model "$model")"
  model_device_map="$(device_map_for_model "$model")"
  export CUDA_VISIBLE_DEVICES="$model_cuda_devices"

  if compgen -G "$model_output_dir/*_metrics.json" > /dev/null && [[ "${RERUN_COMPLETED:-0}" != "1" ]]; then
    echo "============================================================"
    echo "Skipping completed RM: $model_name"
    echo "output=$model_output_dir"
    echo "Set RERUN_COMPLETED=1 to force rerun."
    echo "============================================================"
    continue
  fi

  echo "============================================================"
  echo "Running RM: $model_name"
  echo "model=$model"
  echo "cuda_visible_devices=$CUDA_VISIBLE_DEVICES"
  echo "device_map=$model_device_map"
  echo "batch_size=$batch_size"
  echo "output=$model_output_dir"
  echo "log=$log_path"
  echo "============================================================"

  python run_reward_model.py \
    --model "$model" \
    --data "$DATA_PATH" \
    --output-dir "$model_output_dir" \
    --batch-size "$batch_size" \
    --max-length "$MAX_LENGTH" \
    --device "$DEVICE" \
    --torch-dtype "$TORCH_DTYPE" \
    --device-map "$model_device_map" \
    --prompt-template "$PROMPT_TEMPLATE" \
    --local-files-only \
    ${LIMIT:+--limit "$LIMIT"} \
    2>&1 | tee "$log_path"
done
