#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-all}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/vllm_judge_predictions}"
DATA_PREFIX="${4:-skyjury_bench}"
ORDER="${ORDER:-bidirectional}"
SAMPLES="${SAMPLES:-5}"
BATCH_SIZE="${BATCH_SIZE:-256}"
MAX_NEW_TOKENS="${MAX_NEW_TOKENS:-128}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-4096}"
TEMPERATURE="${TEMPERATURE:-0}"
TOP_P="${TOP_P:-1.0}"
TENSOR_PARALLEL_SIZE="${TENSOR_PARALLEL_SIZE:-1}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.90}"
DTYPE="${DTYPE:-auto}"
LIMIT_ARGS=()

DEFAULT_MODELS=(
  "/ssd1/lbh/zjx/models/skyjury_verifier/unsloth_Llama-3.1-8B-Instruct"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Qwen_Qwen3-8B"
)

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

for model_path in "${MODELS[@]}"; do
  model_name="$(basename "$model_path")"
  for perturbation in length language length_language; do
    DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
    PERTURBATION_OUTPUT_DIR="${OUTPUT_DIR}/${model_name}/${perturbation}"
    echo "Running vLLM judge perturbation: model=${model_name} perturbation=${perturbation}"
    python run_vllm_judge.py \
      --model-path "$model_path" \
      --model-name "$model_name" \
      --data "$DATA_PATH" \
      --output-dir "$PERTURBATION_OUTPUT_DIR" \
      --order "$ORDER" \
      --samples "$SAMPLES" \
      --batch-size "$BATCH_SIZE" \
      --max-new-tokens "$MAX_NEW_TOKENS" \
      --max-model-len "$MAX_MODEL_LEN" \
      --temperature "$TEMPERATURE" \
      --top-p "$TOP_P" \
      --tensor-parallel-size "$TENSOR_PARALLEL_SIZE" \
      --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION" \
      --dtype "$DTYPE" \
      "${LIMIT_ARGS[@]}"
  done
done
