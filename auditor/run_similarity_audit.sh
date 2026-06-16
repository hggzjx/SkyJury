#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
DATA_PREFIX="${DATA_PREFIX:-skyjury_bench}"
PREDICTION_ROOT="${PREDICTION_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/similarity_predictions}"
REPORT_ROOT="${REPORT_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/similarity_reports}"

CUDA_DEVICES="${CUDA_DEVICES:-0,1,2,3}"
DEVICE="${DEVICE:-cuda}"
DATA_PARALLEL="${DATA_PARALLEL:-1}"
TORCH_DTYPE="${TORCH_DTYPE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-4}"
MAX_LENGTH="${MAX_LENGTH:-512}"
PROGRESS_EVERY="${PROGRESS_EVERY:-10}"
LOCAL_FILES_ONLY="${LOCAL_FILES_ONLY:-1}"
SIMILARITY_METHOD="${SIMILARITY_METHOD:-sbert}"
ALLOW_SUBSET="${ALLOW_SUBSET:-1}"
RUN_MODEL_NAMES="${RUN_MODEL_NAMES:-}"

MODEL_NAMES=(
  "bge_m3"
  "qwen3_embedding_8b"
  "kalm_gemma3_12b"
  "bge_reranker_v2_m3"
  "qwen3_reranker_8b"
  "jina_reranker_v3"
)

MODEL_PATHS=(
  "/ssd2/lbh/zjx/models/BAAI_bge-m3"
  "/ssd2/lbh/zjx/models/Qwen_Qwen3-Embedding-8B"
  "/ssd2/lbh/zjx/models/tencent_KaLM-Embedding-Gemma3-12B-2511"
  "/ssd2/lbh/zjx/models/BAAI_bge-reranker-v2-m3"
  "/ssd2/lbh/zjx/models/Qwen_Qwen3-Reranker-8B"
  "/ssd2/lbh/zjx/models/jinaai_jina-reranker-v3"
)

MODEL_METHODS=(
  "$SIMILARITY_METHOD"
  "$SIMILARITY_METHOD"
  "$SIMILARITY_METHOD"
  "reranker"
  "reranker"
  "reranker"
)

MODEL_POOLINGS=(
  "cls"
  "last_token"
  "last_token"
  "mean"
  "mean"
  "mean"
)

MODEL_QUERY_INSTRUCTIONS=(
  ""
  "Given a user profile, retrieve the labeler policy description that best matches the user's moderation needs"
  "Given a user profile, retrieve the labeler policy description that best matches the user's moderation needs"
  ""
  ""
  ""
)

MODEL_TRUST_REMOTE_CODES=(
  "0"
  "0"
  "1"
  "0"
  "1"
  "1"
)

require_model() {
  local model_path="$1"
  if [[ ! -d "$model_path" ]]; then
    echo "Missing model directory: $model_path" >&2
    exit 1
  fi
  if [[ -f "$model_path/model.safetensors.index.json" ]]; then
    python - "$model_path" <<'PY'
import json
import sys
from pathlib import Path

model_dir = Path(sys.argv[1])
index = json.load(open(model_dir / "model.safetensors.index.json"))
missing = sorted({name for name in index.get("weight_map", {}).values() if not (model_dir / name).exists()})
if missing:
    print(f"Incomplete sharded model at {model_dir}; missing: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)
PY
  fi
}

should_run_model() {
  local candidate="$1"
  if [[ -z "$RUN_MODEL_NAMES" ]]; then
    return 0
  fi
  local selected
  for selected in $RUN_MODEL_NAMES; do
    if [[ "$candidate" == "$selected" ]]; then
      return 0
    fi
  done
  return 1
}

for i in "${!MODEL_NAMES[@]}"; do
  name="${MODEL_NAMES[$i]}"
  if ! should_run_model "$name"; then
    echo "Skipping similarity audit for ${name}; not in RUN_MODEL_NAMES"
    continue
  fi
  model_path="${MODEL_PATHS[$i]}"
  method="${MODEL_METHODS[$i]}"
  pooling="${MODEL_POOLINGS[$i]}"
  query_instruction="${MODEL_QUERY_INSTRUCTIONS[$i]}"
  model_trust_remote_code="${MODEL_TRUST_REMOTE_CODES[$i]}"
  require_model "$model_path"

  echo "Running similarity audit predictions for ${name}: ${model_path}"
  MODEL_PATH="$model_path" \
  DEVICE="$DEVICE" \
  CUDA_DEVICES="$CUDA_DEVICES" \
  DATA_PARALLEL="$DATA_PARALLEL" \
  TORCH_DTYPE="$TORCH_DTYPE" \
  BATCH_SIZE="$BATCH_SIZE" \
  MAX_LENGTH="$MAX_LENGTH" \
  PROGRESS_EVERY="$PROGRESS_EVERY" \
  LOCAL_FILES_ONLY="$LOCAL_FILES_ONLY" \
  SIMILARITY_METHOD="$method" \
  POOLING="$pooling" \
  QUERY_INSTRUCTION="$query_instruction" \
  TRUST_REMOTE_CODE="$model_trust_remote_code" \
  bash /ssd1/lbh/zjx/skyjury/auditor/run_similarity_perturbations.sh \
    "$name" \
    "$DATA_DIR" \
    "$PREDICTION_ROOT" \
    "$DATA_PREFIX"

  echo "Generating similarity audit reports for ${name}"
  ALLOW_SUBSET="$ALLOW_SUBSET" \
  bash /ssd1/lbh/zjx/skyjury/auditor/run_similarity_audit_report.sh \
    "$name" \
    "$PREDICTION_ROOT" \
    "$DATA_PREFIX" \
    "${REPORT_ROOT}/${name}"
done
