#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
RESULT_ROOT="${RESULT_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/rm_category50_audit}"
VERIFIER_RESULTS="${VERIFIER_RESULTS:-/ssd1/lbh/zjx/skyjury/verifier/results}"
RM_VERIFIER_SUBDIR="${RM_VERIFIER_SUBDIR:-reward_models}"
DATA_PREFIX="${DATA_PREFIX:-skyjury_bench}"
PROMPT_TEMPLATE="${PROMPT_TEMPLATE:-default}"

mkdir -p "$RESULT_ROOT"/{logs,rm_predictions,reports/rm}

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
  local output_path="$RESULT_ROOT/rm_predictions/${model_name}/base/${DATA_PREFIX}_base_rm_${model_name}_predictions.json"
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
    echo "Skipping RM auditor for ${model_name}: missing full verifier predictions: ${full_predictions}" >&2
    return 0
  fi
  local original_predictions
  original_predictions="$(materialize_base_subset "$full_predictions" "$model_name")"
  local model_report_dir="$RESULT_ROOT/reports/rm/${model_name}"
  local log_path="$RESULT_ROOT/logs/rm_${model_name}.log"
  mkdir -p "$model_report_dir"

  {
    echo "============================================================"
    echo "RM auditor: $model_name"
    echo "model=$model"
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
    MAX_LENGTH="${RM_MAX_LENGTH:-2048}" \
    TORCH_DTYPE="${TORCH_DTYPE:-auto}" \
    PROMPT_TEMPLATE="$PROMPT_TEMPLATE" \
    bash /ssd1/lbh/zjx/skyjury/auditor/run_rm_perturbations.sh \
      "$model" \
      "$DATA_DIR" \
      "$RESULT_ROOT/rm_predictions" \
      "$DATA_PREFIX"

    local pred_root="$RESULT_ROOT/rm_predictions/${model_name}"
    local length_pred language_pred
    length_pred="$(latest_prediction "$pred_root/length")"
    language_pred="$(latest_prediction "$pred_root/language")"

    python /ssd1/lbh/zjx/skyjury/auditor/audit_cross_candidate_perturbations.py \
      --method rm \
      --original "$original_predictions" \
      --perturbed "length=${length_pred}" \
      --perturbed "language=${language_pred}" \
      --output-dir "$model_report_dir" \
      --report-name "rm_cross_candidate_rubric_robustness" \
      --allow-subset
  } 2>&1 | tee "$log_path"
}

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1" \
  "$VERIFIER_RESULTS/$RM_VERIFIER_SUBDIR/RLHFlow_ArmoRM-Llama3-8B-v0.1/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_RLHFlow_ArmoRM-Llama3-8B-v0.1_predictions.json" \
  "${ARMORM_CUDA_DEVICES:-0}" \
  "${ARMORM_DEVICE_MAP:-none}" \
  "${ARMORM_BATCH_SIZE:-4}"

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft" \
  "$VERIFIER_RESULTS/$RM_VERIFIER_SUBDIR/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Ray2333_GRM_Llama3.1_8B_rewardmodel-ft_predictions.json" \
  "${GRM_CUDA_DEVICES:-1}" \
  "${GRM_DEVICE_MAP:-none}" \
  "${GRM_BATCH_SIZE:-4}"

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/openbmb_Eurus-RM-7b" \
  "$VERIFIER_RESULTS/$RM_VERIFIER_SUBDIR/openbmb_Eurus-RM-7b/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_openbmb_Eurus-RM-7b_predictions.json" \
  "${EURUS_CUDA_DEVICES:-2}" \
  "${EURUS_DEVICE_MAP:-none}" \
  "${EURUS_BATCH_SIZE:-4}"

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Llama-3.1-8B-v0.2" \
  "$VERIFIER_RESULTS/$RM_VERIFIER_SUBDIR/Skywork_Skywork-Reward-Llama-3.1-8B-v0.2/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Skywork_Skywork-Reward-Llama-3.1-8B-v0.2_predictions.json" \
  "${SKYWORK_LLAMA_CUDA_DEVICES:-3}" \
  "${SKYWORK_LLAMA_DEVICE_MAP:-none}" \
  "${SKYWORK_LLAMA_BATCH_SIZE:-4}"

run_one \
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Gemma-2-27B-v0.2" \
  "$VERIFIER_RESULTS/$RM_VERIFIER_SUBDIR/Skywork_Skywork-Reward-Gemma-2-27B-v0.2/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Skywork_Skywork-Reward-Gemma-2-27B-v0.2_predictions.json" \
  "${SKYWORK_CUDA_DEVICES:-0,1,2,3}" \
  "${SKYWORK_DEVICE_MAP:-auto}" \
  "${SKYWORK_BATCH_SIZE:-4}"

echo "All RM auditor runs completed."
