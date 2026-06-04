#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
RESULT_ROOT="${RESULT_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_category50_audit}"
VERIFIER_RESULTS="${VERIFIER_RESULTS:-/ssd1/lbh/zjx/skyjury/verifier/results}"
DATA_PREFIX="${DATA_PREFIX:-skyjury_bench}"
CONCURRENCY="${CONCURRENCY:-48}"

mkdir -p "$RESULT_ROOT"/{logs,llm_judge_predictions,reports/llm_judge}

latest_prediction() {
  local dir="$1"
  find "$dir" -name '*_predictions.json' -type f | sort | tail -n 1
}

run_one() {
  local model="$1"
  local original_predictions="$2"

  if [[ ! -f "$original_predictions" ]]; then
    echo "Skipping LLM-as-judge auditor for ${model}: missing original predictions: ${original_predictions}" >&2
    return 0
  fi

  local model_report_dir="$RESULT_ROOT/reports/llm_judge/${model}"
  local log_path="$RESULT_ROOT/logs/llm_judge_${model}.log"
  mkdir -p "$model_report_dir"

  {
    echo "============================================================"
    echo "LLM-as-judge auditor: $model"
    echo "original_predictions=$original_predictions"
    echo "data_dir=$DATA_DIR"
    echo "data_prefix=$DATA_PREFIX"
    echo "concurrency=$CONCURRENCY"
    echo "============================================================"

    bash /ssd1/lbh/zjx/skyjury/auditor/run_llm_judge_perturbations.sh \
      "$model" \
      "$CONCURRENCY" \
      "$DATA_DIR" \
      "$RESULT_ROOT/llm_judge_predictions" \
      "$DATA_PREFIX"

    local pred_root="$RESULT_ROOT/llm_judge_predictions/${model}"
    local length_pred language_pred length_language_pred
    length_pred="$(latest_prediction "$pred_root/length")"
    language_pred="$(latest_prediction "$pred_root/language")"
    length_language_pred="$(latest_prediction "$pred_root/length_language")"

    ALLOW_SUBSET=1 bash /ssd1/lbh/zjx/skyjury/auditor/run_audit_report.sh \
      llm_judge \
      "$original_predictions" \
      "$length_pred" \
      "$language_pred" \
      "$length_language_pred" \
      "$model_report_dir"
  } 2>&1 | tee "$log_path"
}

# run_one \
#   "gpt-5-ca" \
#   "$VERIFIER_RESULTS/generative_rm/gpt-5-ca/skyjury_bench_llm_judge_gpt-5-ca_bidirectional_predictions.json"

# run_one \
#   "gpt-4o-ca" \
#   "$VERIFIER_RESULTS/generative_rm/gpt-4o-ca/skyjury_bench_llm_judge_gpt-4o-ca_predictions.json"

# run_one \
#   "deepseek-v4-flash" \
#   "$VERIFIER_RESULTS/generative_rm/deepseek-v4-flash/skyjury_bench_llm_judge_deepseek-v4-flash_predictions.json"

# run_one \
#   "qwen3.5-plus" \
#   "$VERIFIER_RESULTS/generative_rm/qwen3.5-plus/skyjury_bench_llm_judge_qwen3.5-plus_predictions.json"

# run_one \
#   "glm-5" \
#   "$VERIFIER_RESULTS/generative_rm/glm-5/skyjury_bench_llm_judge_glm-5_predictions.json"

run_one \
  "deepseek-v4-pro" \
  "$VERIFIER_RESULTS/generative_rm/deepseek-v4-pro/skyjury_bench_llm_judge_deepseek-v4-pro_predictions.json"

# run_one \
#   "minimax-m2.7" \
#   "$VERIFIER_RESULTS/generative_rm/minimax-m2.7/skyjury_bench_llm_judge_minimax-m2.7_predictions.json"

echo "All LLM-as-judge auditor runs completed."
