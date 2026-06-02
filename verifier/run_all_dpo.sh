#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${1:-/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json}"
REF_MODEL_PATH="${REF_MODEL_PATH:-/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-7b}"
CUDA_DEVICES="${CUDA_DEVICES:-0,1,2,3}"
DEVICE="${DEVICE:-cuda}"
DEVICE_MAP="${DEVICE_MAP:-auto}"
MAX_LENGTH="${MAX_LENGTH:-2048}"
MAX_PROMPT_LENGTH="${MAX_PROMPT_LENGTH:-1024}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/ssd1/lbh/zjx/skyjury/verifier/results/dpo_models}"
BATCH_SIZE="${BATCH_SIZE:-1}"

MODELS=(
  "/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-13b"
  "/ssd1/lbh/zjx/models/skyjury_verifier/upstage_SOLAR-10.7B-Instruct-v1.0"
)

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier
mkdir -p "$OUTPUT_ROOT/logs"

echo "SkyJury RewardBench-compatible DPO evaluation"
echo "data=$DATA_PATH"
echo "ref_model=$REF_MODEL_PATH"
echo "cuda_devices=$CUDA_DEVICES"
echo "device=$DEVICE"
echo "device_map=$DEVICE_MAP"
echo "max_length=$MAX_LENGTH"
echo "max_prompt_length=$MAX_PROMPT_LENGTH"
echo "output_root=$OUTPUT_ROOT"
echo

for model in "${MODELS[@]}"; do
  model_name="$(basename "$model")"
  model_output_dir="$OUTPUT_ROOT/$model_name"
  log_path="$OUTPUT_ROOT/logs/${model_name}.log"
  mkdir -p "$model_output_dir"
  export CUDA_VISIBLE_DEVICES="$CUDA_DEVICES"

  if compgen -G "$model_output_dir/*_metrics.json" > /dev/null && [[ "${RERUN_COMPLETED:-0}" != "1" ]]; then
    echo "============================================================"
    echo "Skipping completed DPO model: $model_name"
    echo "output=$model_output_dir"
    echo "Set RERUN_COMPLETED=1 to force rerun."
    echo "============================================================"
    continue
  fi

  echo "============================================================"
  echo "Running DPO model: $model_name"
  echo "model=$model"
  echo "ref_model=$REF_MODEL_PATH"
  echo "cuda_visible_devices=$CUDA_VISIBLE_DEVICES"
  echo "output=$model_output_dir"
  echo "log=$log_path"
  echo "============================================================"

  OUTPUT_DIR="$model_output_dir" \
  DEVICE="$DEVICE" \
  DEVICE_MAP="$DEVICE_MAP" \
  BATCH_SIZE="$BATCH_SIZE" \
  MAX_LENGTH="$MAX_LENGTH" \
  MAX_PROMPT_LENGTH="$MAX_PROMPT_LENGTH" \
  TORCH_DTYPE="$TORCH_DTYPE" \
  bash run_dpo.sh "$model" "$DATA_PATH" "$REF_MODEL_PATH" 2>&1 | tee "$log_path"
done
