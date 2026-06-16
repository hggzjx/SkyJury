#!/usr/bin/env bash
set -euo pipefail

RUN_NAME="${1:-e5}"
DATA_DIR="${2:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
OUTPUT_DIR="${3:-/ssd1/lbh/zjx/skyjury/auditor/results/similarity_predictions}"
DATA_PREFIX="${4:-skyjury_bench}"

SIMILARITY_METHOD="${SIMILARITY_METHOD:-$RUN_NAME}"
MODEL_PATH="${MODEL_PATH:-}"
DEVICE="${DEVICE:-auto}"
CUDA_DEVICES="${CUDA_DEVICES:-}"
DEVICE_MAP="${DEVICE_MAP:-}"
DATA_PARALLEL="${DATA_PARALLEL:-0}"
TORCH_DTYPE="${TORCH_DTYPE:-}"
TRUST_REMOTE_CODE="${TRUST_REMOTE_CODE:-0}"
BATCH_SIZE="${BATCH_SIZE:-32}"
MAX_LENGTH="${MAX_LENGTH:-512}"
PROGRESS_EVERY="${PROGRESS_EVERY:-10}"
LOCAL_FILES_ONLY="${LOCAL_FILES_ONLY:-1}"
POOLING="${POOLING:-mean}"
QUERY_INSTRUCTION="${QUERY_INSTRUCTION:-}"

LOCAL_FILES_ARGS=()
MODEL_ARGS=()
LIMIT_ARGS=()
GPU_ARGS=()
if [[ "$LOCAL_FILES_ONLY" == "1" ]]; then
  LOCAL_FILES_ARGS=(--local-files-only)
fi
if [[ -n "$MODEL_PATH" ]]; then
  MODEL_ARGS=(--model-path "$MODEL_PATH")
fi
if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi
if [[ -n "$CUDA_DEVICES" ]]; then
  GPU_ARGS+=(--cuda-devices "$CUDA_DEVICES")
fi
if [[ -n "$DEVICE_MAP" ]]; then
  GPU_ARGS+=(--device-map "$DEVICE_MAP")
fi
if [[ "$DATA_PARALLEL" == "1" ]]; then
  GPU_ARGS+=(--data-parallel)
fi
if [[ -n "$TORCH_DTYPE" ]]; then
  GPU_ARGS+=(--torch-dtype "$TORCH_DTYPE")
fi
if [[ "$TRUST_REMOTE_CODE" == "1" ]]; then
  GPU_ARGS+=(--trust-remote-code)
fi

DENSE_ARGS=(--pooling "$POOLING")
if [[ -n "$QUERY_INSTRUCTION" ]]; then
  DENSE_ARGS+=(--query-instruction "$QUERY_INSTRUCTION")
fi

BASE_DATA="${DATA_DIR}/${DATA_PREFIX}_base.json"
LENGTH_DATA="${DATA_DIR}/${DATA_PREFIX}_rubric_length.json"
LANGUAGE_DATA="${DATA_DIR}/${DATA_PREFIX}_rubric_language.json"
LENGTH_LANGUAGE_DATA="${DATA_DIR}/${DATA_PREFIX}_rubric_length_language.json"

FIT_DATA_ARGS=(
  --fit-data "$BASE_DATA"
  --fit-data "$LENGTH_DATA"
  --fit-data "$LANGUAGE_DATA"
  --fit-data "$LENGTH_LANGUAGE_DATA"
)

source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/verifier

for variant in base length language length_language; do
  case "$variant" in
    base)
      DATA_PATH="$BASE_DATA"
      ;;
    length)
      DATA_PATH="$LENGTH_DATA"
      ;;
    language)
      DATA_PATH="$LANGUAGE_DATA"
      ;;
    length_language)
      DATA_PATH="$LENGTH_LANGUAGE_DATA"
      ;;
    *)
      echo "Unknown variant: $variant" >&2
      exit 1
      ;;
  esac

  VARIANT_OUTPUT_DIR="${OUTPUT_DIR}/${RUN_NAME}/${variant}"
  echo "Running similarity perturbation: run=${RUN_NAME} method=${SIMILARITY_METHOD} variant=${variant}"
  python run_similarity_model.py \
    --method "$SIMILARITY_METHOD" \
    --data "$DATA_PATH" \
    --output-dir "$VARIANT_OUTPUT_DIR" \
    --device "$DEVICE" \
    --batch-size "$BATCH_SIZE" \
    --max-length "$MAX_LENGTH" \
    --progress-every "$PROGRESS_EVERY" \
    "${DENSE_ARGS[@]}" \
    "${FIT_DATA_ARGS[@]}" \
    "${MODEL_ARGS[@]}" \
    "${GPU_ARGS[@]}" \
    "${LOCAL_FILES_ARGS[@]}" \
    "${LIMIT_ARGS[@]}"
done
