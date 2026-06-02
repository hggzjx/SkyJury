#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-/ssd1/lbh/zjx/models/skyjury_verifier/OpenAssistant_reward-model-deberta-v3-large-v2}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/rm_predictions}"
DATA_PREFIX="${4:-verifier_pilot_rmbench}"
DEVICE="${CUDA_VISIBLE_DEVICES:-auto}"

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for perturbation in length language length_language; do
  DATA_PATH="${DATA_DIR}/${DATA_PREFIX}_rubric_${perturbation}.json"
  python run_reward_model.py \
    --model "$MODEL_PATH" \
    --data "$DATA_PATH" \
    --batch-size 4 \
    --max-length 2048 \
    --device "$DEVICE" \
    --output-dir "$OUTPUT_DIR"
done
