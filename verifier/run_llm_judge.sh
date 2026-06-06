#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${DATA_PATH:-${1:-/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json}}"
CONCURRENCY="${CONCURRENCY:-${2:-48}}"
SLOW_CONCURRENCY="${SLOW_CONCURRENCY:-24}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/ssd1/lbh/zjx/skyjury/verifier/results/generative_rm}"
ORDER="${ORDER:-bidirectional}"
TEMPERATURE="${TEMPERATURE:-0}"
MAX_TOKENS="${MAX_TOKENS:-1024}"
REASONING_EFFORT="${REASONING_EFFORT:-minimal}"
TIMEOUT="${TIMEOUT:-60}"
RETRIES="${RETRIES:-6}"
RETRY_SLEEP="${RETRY_SLEEP:-3}"
LIMIT="${LIMIT:-}"
CONTINUE_ON_ERROR="${CONTINUE_ON_ERROR:-1}"

if [[ -n "$LIMIT" ]]; then
  OUTPUT_ROOT="${OUTPUT_ROOT}/debug_limit_${LIMIT}"
fi

if [[ -n "${MODELS:-}" ]]; then
  read -r -a MODEL_LIST <<< "$MODELS"
else
  MODEL_LIST=(
    # "gpt-4o-ca"
    # "deepseek-v4-flash"
    # "gpt-5-ca"
    "gpt-5-nano-ca"
    # "qwen3.5-plus"
    # "deepseek-v4-pro"
    # "minimax-m2.7"
  )
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for MODEL_NAME in "${MODEL_LIST[@]}"; do
  MODEL_CONCURRENCY="$CONCURRENCY"
  MODEL_TIMEOUT="$TIMEOUT"
  MODEL_RETRIES="$RETRIES"
  case "$MODEL_NAME" in
    gpt-5*)
      MODEL_CONCURRENCY="$SLOW_CONCURRENCY"
      ;;
    qwen3.5-plus)
      MODEL_CONCURRENCY="${QWEN_CONCURRENCY:-8}"
      MODEL_TIMEOUT="${QWEN_TIMEOUT:-180}"
      MODEL_RETRIES="${QWEN_RETRIES:-8}"
      ;;
    glm-5)
      MODEL_CONCURRENCY="${GLM_CONCURRENCY:-8}"
      MODEL_TIMEOUT="${GLM_TIMEOUT:-180}"
      MODEL_RETRIES="${GLM_RETRIES:-8}"
      ;;
  esac

  MODEL_OUTPUT_DIR="${OUTPUT_ROOT}/${MODEL_NAME}"
  echo "============================================================"
  echo "Running LLM-as-judge verifier"
  echo "model=${MODEL_NAME}"
  echo "data=${DATA_PATH}"
  echo "concurrency=${MODEL_CONCURRENCY}"
  echo "order=${ORDER}"
  echo "max_tokens=${MAX_TOKENS}"
  echo "reasoning_effort=${REASONING_EFFORT}"
  echo "timeout=${MODEL_TIMEOUT}"
  echo "retries=${MODEL_RETRIES}"
  echo "output=${MODEL_OUTPUT_DIR}"
  if [[ -n "$LIMIT" ]]; then
    echo "limit=${LIMIT}"
  fi
  echo "============================================================"

  CMD=(
    python run_llm_judge.py
    --model "$MODEL_NAME"
    --data "$DATA_PATH"
    --order "$ORDER"
    --temperature "$TEMPERATURE"
    --max-tokens "$MAX_TOKENS"
    --reasoning-effort "$REASONING_EFFORT"
    --timeout "$MODEL_TIMEOUT"
    --concurrency "$MODEL_CONCURRENCY"
    --retries "$MODEL_RETRIES"
    --retry-sleep "$RETRY_SLEEP"
    --output-dir "$MODEL_OUTPUT_DIR"
  )
  if [[ -n "$LIMIT" ]]; then
    CMD+=(--limit "$LIMIT")
  fi

  if "${CMD[@]}"; then
    :
  else
    STATUS=$?
    echo "ERROR: model=${MODEL_NAME} failed with exit_status=${STATUS}" >&2
    if [[ "$CONTINUE_ON_ERROR" != "1" ]]; then
      exit "$STATUS"
    fi
  fi
done
