#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${DATA_PATH:-${1:-/ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json}}"
CONCURRENCY="${CONCURRENCY:-${2:-48}}"
SLOW_CONCURRENCY="${SLOW_CONCURRENCY:-48}"
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

if [[ -n "${MODELS:-}" ]]; then
  read -r -a MODEL_LIST <<< "$MODELS"
else
  MODEL_LIST=(
    # "gpt-4o-ca"
    # "deepseek-v4-flash"
    # "gpt-5-ca"
    # "gpt-5-nano"
    # "glm-5"
    # "gemini-2.5-pro"
    "qwen3.5-plus"
  )
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for MODEL_NAME in "${MODEL_LIST[@]}"; do
  MODEL_CONCURRENCY="$CONCURRENCY"
  case "$MODEL_NAME" in
    gpt-5*|qwen3.5-plus)
      MODEL_CONCURRENCY="$SLOW_CONCURRENCY"
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
  echo "timeout=${TIMEOUT}"
  echo "retries=${RETRIES}"
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
    --timeout "$TIMEOUT"
    --concurrency "$MODEL_CONCURRENCY"
    --retries "$RETRIES"
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
