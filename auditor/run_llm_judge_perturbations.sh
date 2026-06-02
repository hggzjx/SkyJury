#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="${1:-gpt-4o-ca}"
CONCURRENCY="${2:-4}"
DATA_DIR="${3:-/ssd1/lbh/zjx/skyjury/data/auditor}"
OUTPUT_DIR="${4:-/ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_predictions}"
DATA_PREFIX="${5:-verifier_pilot_rmbench}"
SAMPLES="${SAMPLES:-10}"
TEMPERATURE="${TEMPERATURE:-0}"
MAX_TOKENS="${MAX_TOKENS:-1024}"
REASONING_EFFORT="${REASONING_EFFORT:-minimal}"
LIMIT_ARGS=()

if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for perturbation in length language length_language; do
  DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
  PERTURBATION_OUTPUT_DIR="${OUTPUT_DIR}/${MODEL_NAME}/${perturbation}"
  python run_llm_judge.py \
    --model "$MODEL_NAME" \
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
