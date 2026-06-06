#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="${1:-all}"
CONCURRENCY="${2:-4}"
DATA_DIR="${3:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
OUTPUT_DIR="${4:-/ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_category50_audit/llm_judge_predictions}"
DATA_PREFIX="${5:-skyjury_bench}"
SAMPLES="${SAMPLES:-5}"
TEMPERATURE="${TEMPERATURE:-0.5}"
MAX_TOKENS="${MAX_TOKENS:-1024}"
REASONING_EFFORT="${REASONING_EFFORT:-minimal}"
LIMIT_ARGS=()

DEFAULT_MODELS=(
  "gpt-5-ca"
  "gpt-4o-ca"
  "deepseek-v4-flash"
  "qwen3.5-plus"
  "glm-5"
)

if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

if [[ "$MODEL_NAME" == "all" ]]; then
  MODELS=("${DEFAULT_MODELS[@]}")
else
  MODELS=("$MODEL_NAME")
fi

for model in "${MODELS[@]}"; do
  for perturbation in length language; do
    DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
    PERTURBATION_OUTPUT_DIR="${OUTPUT_DIR}/${model}/${perturbation}"
    echo "Running LLM judge perturbation: model=${model} perturbation=${perturbation} concurrency=${CONCURRENCY}"
    python run_llm_judge.py \
      --model "$model" \
      --data "$DATA_PATH" \
      --order bidirectional \
      --samples "$SAMPLES" \
      --temperature "$TEMPERATURE" \
      --max-tokens "$MAX_TOKENS" \
      --reasoning-effort "$REASONING_EFFORT" \
      --concurrency "$CONCURRENCY" \
      --output-dir "$PERTURBATION_OUTPUT_DIR" \
      "${LIMIT_ARGS[@]}"
  done
done
