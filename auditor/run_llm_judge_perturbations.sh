#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="${1:-gpt-4o-ca}"
CONCURRENCY="${2:-4}"
DATA_DIR="${3:-/ssd1/lbh/zjx/skyjury/data/auditor}"
OUTPUT_DIR="${4:-/ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_predictions}"
DATA_PREFIX="${5:-verifier_pilot_rmbench}"

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for perturbation in length language length_language; do
  DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
  python run_llm_judge.py \
    --model "$MODEL_NAME" \
    --data "$DATA_PATH" \
    --order bidirectional \
    --temperature 0 \
    --concurrency "$CONCURRENCY" \
    --output-dir "$OUTPUT_DIR"
done
