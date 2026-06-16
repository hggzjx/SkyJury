#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
RESULT_ROOT="${RESULT_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/dpo_category50_audit}"
VERIFIER_RESULTS="${VERIFIER_RESULTS:-/ssd1/lbh/zjx/skyjury/verifier/results}"
DPO_VERIFIER_SUBDIR="${DPO_VERIFIER_SUBDIR:-dpo_models}"
REF_MODEL_PATH="${REF_MODEL_PATH:-/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-7b}"
DATA_PREFIX="${DATA_PREFIX:-skyjury_bench}"
PROMPT_TEMPLATE="${PROMPT_TEMPLATE:-default}"

mkdir -p "$RESULT_ROOT"/{logs,dpo_predictions,reports/dpo}

safe_name() {
  basename "$1" | tr '/:' '__'
}

latest_prediction() {
  local dir="$1"
  find "$dir" -name '*_predictions.json' -type f | sort | tail -n 1
}

materialize_base_subset() {
  local full_predictions="$1"
  local model_name="$2"
  local output_path="$RESULT_ROOT/dpo_predictions/${model_name}/base/${DATA_PREFIX}_base_dpo_${model_name}_predictions.json"
  python /ssd1/lbh/zjx/skyjury/auditor/materialize_base_subset.py \
    --base-data "$DATA_DIR/${DATA_PREFIX}_base.json" \
    --full-predictions "$full_predictions" \
    --output "$output_path" >/dev/null
  printf '%s\n' "$output_path"
}

run_one() {
  local model="$1"
  local full_predictions="$2"
  local cuda_devices="$3"
  local device_map="$4"
  local batch_size="$5"

  local model_name
  model_name="$(safe_name "$model")"
  if [[ ! -f "$full_predictions" ]]; then
    echo "Skipping DPO auditor for ${model_name}: missing full verifier predictions: ${full_predictions}" >&2
    return 0
  fi
  local original_predictions
  original_predictions="$(materialize_base_subset "$full_predictions" "$model_name")"
  local model_report_dir="$RESULT_ROOT/reports/dpo/${model_name}"
  local log_path="$RESULT_ROOT/logs/dpo_${model_name}.log"
  mkdir -p "$model_report_dir"

  {
    echo "============================================================"
    echo "DPO auditor: $model_name"
    echo "model=$model"
    echo "ref_model=$REF_MODEL_PATH"
    echo "original_predictions=$original_predictions"
    echo "data_dir=$DATA_DIR"
    echo "data_prefix=$DATA_PREFIX"
    echo "cuda_devices=$cuda_devices"
    echo "device_map=$device_map"
    echo "batch_size=$batch_size"
    echo "prompt_template=$PROMPT_TEMPLATE"
    echo "============================================================"

    CUDA_VISIBLE_DEVICES="$cuda_devices" \
    DEVICE=cuda \
    DEVICE_MAP="$device_map" \
    BATCH_SIZE="$batch_size" \
    MAX_LENGTH="${DPO_MAX_LENGTH:-2048}" \
    MAX_PROMPT_LENGTH="${MAX_PROMPT_LENGTH:-1024}" \
    TORCH_DTYPE="${TORCH_DTYPE:-auto}" \
    PROMPT_TEMPLATE="$PROMPT_TEMPLATE" \
    bash /ssd1/lbh/zjx/skyjury/auditor/run_dpo_perturbations.sh \
      "$model" \
      "$DATA_DIR" \
      "$RESULT_ROOT/dpo_predictions" \
      "$REF_MODEL_PATH" \
      "$DATA_PREFIX"

    local pred_root="$RESULT_ROOT/dpo_predictions/${model_name}"
    local length_pred language_pred
    length_pred="$(latest_prediction "$pred_root/length")"
    language_pred="$(latest_prediction "$pred_root/language")"

    python /ssd1/lbh/zjx/skyjury/auditor/audit_cross_candidate_perturbations.py \
      --method dpo \
      --original "$original_predictions" \
      --perturbed "length=${length_pred}" \
      --perturbed "language=${language_pred}" \
      --output-dir "$model_report_dir" \
      --report-name "dpo_cross_candidate_rubric_robustness" \
      --allow-subset
  } 2>&1 | tee "$log_path"
}

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-13b" \
  "$VERIFIER_RESULTS/$DPO_VERIFIER_SUBDIR/allenai_tulu-2-dpo-13b/skyjury_bench_dpo_ssd1_lbh_zjx_models_skyjury_verifier_allenai_tulu-2-dpo-13b_predictions.json" \
  "${TULU_CUDA_DEVICES:-0,1,2,3}" \
  "${TULU_DEVICE_MAP:-auto}" \
  "${TULU_BATCH_SIZE:-16}"

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/upstage_SOLAR-10.7B-Instruct-v1.0" \
  "$VERIFIER_RESULTS/$DPO_VERIFIER_SUBDIR/upstage_SOLAR-10.7B-Instruct-v1.0/skyjury_bench_dpo_ssd1_lbh_zjx_models_skyjury_verifier_upstage_SOLAR-10.7B-Instruct-v1.0_predictions.json" \
  "${SOLAR_CUDA_DEVICES:-0,1,2,3}" \
  "${SOLAR_DEVICE_MAP:-auto}" \
  "${SOLAR_BATCH_SIZE:-16}"

echo "All DPO auditor runs completed."
