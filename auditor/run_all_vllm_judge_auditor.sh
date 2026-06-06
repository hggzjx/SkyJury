#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-all}"
DATA_DIR="${DATA_DIR:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_category50_audit}"
VERIFIER_RESULTS="${VERIFIER_RESULTS:-/ssd1/lbh/zjx/skyjury/verifier/results/generative_rm}"
DATA_PREFIX="${DATA_PREFIX:-skyjury_bench}"
ORDER="${ORDER:-bidirectional}"
SAMPLES="${SAMPLES:-5}"
BATCH_SIZE="${BATCH_SIZE:-256}"
MAX_NEW_TOKENS="${MAX_NEW_TOKENS:-128}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-4096}"
TEMPERATURE="${TEMPERATURE:-0.5}"
TOP_P="${TOP_P:-1.0}"
TENSOR_PARALLEL_SIZE="${TENSOR_PARALLEL_SIZE:-1}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.90}"
DTYPE="${DTYPE:-auto}"
PERMUTATIONS="${PERMUTATIONS:-10000}"
ALPHA="${ALPHA:-0.05}"
LIMIT_ARGS=()

DEFAULT_MODELS=(
  # "/ssd1/lbh/zjx/models/skyjury_verifier/unsloth_Llama-3.1-8B-Instruct"
  "/ssd1/lbh/zjx/models/skyjury_verifier/Qwen_Qwen3-8B"
)

if [[ -n "${LIMIT:-}" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
fi

materialize_base_subset() {
  local full_predictions="$1"
  local model_name="$2"
  local output_path="${OUTPUT_ROOT}/llm_judge_predictions/${model_name}/base/${DATA_PREFIX}_base_vllm_judge_${model_name}_predictions.json"
  python /ssd1/lbh/zjx/skyjury/auditor/materialize_base_subset.py \
    --base-data "$DATA_DIR/${DATA_PREFIX}_base.json" \
    --full-predictions "$full_predictions" \
    --output "$output_path" >/dev/null
  printf '%s\n' "$output_path"
}

source activate rm_dev

if [[ "$MODEL_PATH" == "all" ]]; then
  MODELS=("${DEFAULT_MODELS[@]}")
else
  MODELS=("$MODEL_PATH")
fi

for model_path in "${MODELS[@]}"; do
  model_name="$(basename "$model_path")"
  full_predictions="${VERIFIER_RESULTS}/${model_name}/skyjury_bench_vllm_judge_${model_name}_predictions.json"
  base_output_dir="${OUTPUT_ROOT}/llm_judge_predictions/${model_name}/base"

  if [[ -f "$full_predictions" ]]; then
    echo "============================================================"
    echo "Materializing vLLM judge base from full verifier predictions: ${model_name}"
    echo "============================================================"
    original_predictions="$(materialize_base_subset "$full_predictions" "$model_name")"
  else
    echo "============================================================"
    echo "Running vLLM judge base: ${model_name}"
    echo "============================================================"
    cd /ssd1/lbh/zjx/skyjury/verifier
    python run_vllm_judge.py \
      --model-path "$model_path" \
      --model-name "$model_name" \
      --data "${DATA_DIR}/${DATA_PREFIX}_base.json" \
      --output-dir "$base_output_dir" \
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
    original_predictions="$(find "$base_output_dir" -maxdepth 1 -name '*_predictions.json' | sort | tail -n 1)"
  fi

  cd /ssd1/lbh/zjx/skyjury/auditor
  bash run_vllm_judge_perturbations.sh \
    "$model_path" \
    "$DATA_DIR" \
    "${OUTPUT_ROOT}/llm_judge_predictions" \
    "$DATA_PREFIX"

  length_predictions="$(find "${OUTPUT_ROOT}/llm_judge_predictions/${model_name}/length" -maxdepth 1 -name '*_predictions.json' | sort | tail -n 1)"
  language_predictions="$(find "${OUTPUT_ROOT}/llm_judge_predictions/${model_name}/language" -maxdepth 1 -name '*_predictions.json' | sort | tail -n 1)"
  report_dir="${OUTPUT_ROOT}/reports/llm_judge/${model_name}"
  mkdir -p "$report_dir"

  python audit_cross_candidate_perturbations.py \
    --method llm_judge \
    --original "$original_predictions" \
    --perturbed "length=${length_predictions}" \
    --perturbed "language=${language_predictions}" \
    --output-dir "$report_dir" \
    --report-name "llm_judge_cross_candidate_rubric_robustness" \
    --permutations "$PERMUTATIONS" \
    --alpha "$ALPHA" \
    --allow-subset
done
