#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${DATA_PATH:-${1:-/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json}}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/ssd1/lbh/zjx/skyjury/verifier/results/generative_rm}"
ORDER="${ORDER:-bidirectional}"
SAMPLES="${SAMPLES:-1}"
BATCH_SIZE="${BATCH_SIZE:-256}"
MAX_NEW_TOKENS="${MAX_NEW_TOKENS:-128}"
MAX_INPUT_LENGTH="${MAX_INPUT_LENGTH:-4096}"
TEMPERATURE="${TEMPERATURE:-0}"
TOP_P="${TOP_P:-1.0}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-4096}"
TENSOR_PARALLEL_SIZE="${TENSOR_PARALLEL_SIZE:-1}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.90}"
DTYPE="${DTYPE:-auto}"
LIMIT="${LIMIT:-}"

if [[ -n "${MODEL_PATHS:-}" ]]; then
  read -r -a MODEL_LIST <<< "$MODEL_PATHS"
else
  MODEL_LIST=(
    # "/ssd1/lbh/zjx/models/skyjury_verifier/unsloth_Llama-3.1-8B-Instruct"
    "/ssd1/lbh/zjx/models/skyjury_verifier/Qwen_Qwen3-8B"
  )
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for MODEL_PATH in "${MODEL_LIST[@]}"; do
  MODEL_NAME="$(basename "$MODEL_PATH")"
  MODEL_OUTPUT_DIR="${OUTPUT_ROOT}/${MODEL_NAME}"
  echo "============================================================"
  echo "Running vLLM-as-judge verifier"
  echo "model_path=${MODEL_PATH}"
  echo "data=${DATA_PATH}"
  echo "order=${ORDER}"
  echo "samples=${SAMPLES}"
  echo "batch_size=${BATCH_SIZE}"
  echo "output=${MODEL_OUTPUT_DIR}"
  echo "============================================================"

  CMD=(
    python run_vllm_judge.py
    --model-path "$MODEL_PATH"
    --model-name "$MODEL_NAME"
    --data "$DATA_PATH"
    --output-dir "$MODEL_OUTPUT_DIR"
    --order "$ORDER"
    --samples "$SAMPLES"
    --batch-size "$BATCH_SIZE"
    --max-new-tokens "$MAX_NEW_TOKENS"
    --max-model-len "$MAX_MODEL_LEN"
    --temperature "$TEMPERATURE"
    --top-p "$TOP_P"
    --tensor-parallel-size "$TENSOR_PARALLEL_SIZE"
    --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION"
    --dtype "$DTYPE"
  )
  if [[ -n "$LIMIT" ]]; then
    CMD+=(--limit "$LIMIT")
  fi
  "${CMD[@]}"
done
