#!/usr/bin/env bash
set -euo pipefail

DATA_PATH="${DATA_PATH:-/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json}"
DATA_DIR="${DATA_DIR:-/ssd1/lbh/zjx/skyjury/data/auditor/category50}"
RESULT_ROOT="${RESULT_ROOT:-/ssd1/lbh/zjx/skyjury/auditor/results/rm_dpo_category50_audit}"
VERIFIER_RESULTS="${VERIFIER_RESULTS:-/ssd1/lbh/zjx/skyjury/verifier/results}"
REF_MODEL_PATH="${REF_MODEL_PATH:-/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-7b}"
DATA_PREFIX="${DATA_PREFIX:-skyjury_bench}"

mkdir -p "$RESULT_ROOT"/{logs,rm_predictions,dpo_predictions,reports}

safe_name() {
  basename "$1" | tr '/:' '__'
}

latest_prediction() {
  local dir="$1"
  find "$dir" -name '*_predictions.json' -type f | sort | tail -n 1
}

run_rm_audit() {
  local model="$1"
  local original_predictions="$2"
  local cuda_devices="$3"
  local device_map="$4"
  local batch_size="$5"

  local model_name
  model_name="$(safe_name "$model")"
  local prefix="$DATA_PREFIX"
  local model_report_dir="$RESULT_ROOT/reports/rm/${model_name}"
  local log_path="$RESULT_ROOT/logs/rm_${model_name}.log"
  mkdir -p "$model_report_dir"

  {
    echo "============================================================"
    echo "RM auditor: $model_name"
    echo "model=$model"
    echo "original_predictions=$original_predictions"
    echo "data_prefix=$prefix"
    echo "perturbation_source=existing"
    echo "cuda_devices=$cuda_devices"
    echo "device_map=$device_map"
    echo "batch_size=$batch_size"
    echo "============================================================"

    CUDA_VISIBLE_DEVICES="$cuda_devices" \
    DEVICE=cuda \
    DEVICE_MAP="$device_map" \
    BATCH_SIZE="$batch_size" \
    MAX_LENGTH="${RM_MAX_LENGTH:-2048}" \
    TORCH_DTYPE="${TORCH_DTYPE:-auto}" \
    bash /ssd1/lbh/zjx/skyjury/auditor/run_rm_perturbations.sh \
      "$model" \
      "$DATA_DIR" \
      "$RESULT_ROOT/rm_predictions" \
      "$prefix"

    local pred_root="$RESULT_ROOT/rm_predictions/${model_name}"
    local length_pred language_pred length_language_pred
    length_pred="$(latest_prediction "$pred_root/length")"
    language_pred="$(latest_prediction "$pred_root/language")"
    length_language_pred="$(latest_prediction "$pred_root/length_language")"

    ALLOW_SUBSET=1 bash /ssd1/lbh/zjx/skyjury/auditor/run_audit_report.sh \
      rm \
      "$original_predictions" \
      "$length_pred" \
      "$language_pred" \
      "$length_language_pred" \
      "$model_report_dir"
  } 2>&1 | tee "$log_path"
}

run_dpo_audit() {
  local model="$1"
  local original_predictions="$2"
  local cuda_devices="$3"
  local device_map="$4"
  local batch_size="$5"

  local model_name
  model_name="$(safe_name "$model")"
  local prefix="$DATA_PREFIX"
  local model_report_dir="$RESULT_ROOT/reports/dpo/${model_name}"
  local log_path="$RESULT_ROOT/logs/dpo_${model_name}.log"
  mkdir -p "$model_report_dir"

  {
    echo "============================================================"
    echo "DPO auditor: $model_name"
    echo "model=$model"
    echo "ref_model=$REF_MODEL_PATH"
    echo "original_predictions=$original_predictions"
    echo "data_prefix=$prefix"
    echo "perturbation_source=existing"
    echo "cuda_devices=$cuda_devices"
    echo "device_map=$device_map"
    echo "batch_size=$batch_size"
    echo "============================================================"

    CUDA_VISIBLE_DEVICES="$cuda_devices" \
    DEVICE=cuda \
    DEVICE_MAP="$device_map" \
    BATCH_SIZE="$batch_size" \
    MAX_LENGTH="${DPO_MAX_LENGTH:-2048}" \
    MAX_PROMPT_LENGTH="${MAX_PROMPT_LENGTH:-1024}" \
    TORCH_DTYPE="${TORCH_DTYPE:-auto}" \
    bash /ssd1/lbh/zjx/skyjury/auditor/run_dpo_perturbations.sh \
      "$model" \
      "$DATA_DIR" \
      "$RESULT_ROOT/dpo_predictions" \
      "$REF_MODEL_PATH" \
      "$prefix"

    local pred_root="$RESULT_ROOT/dpo_predictions/${model_name}"
    local length_pred language_pred length_language_pred
    length_pred="$(latest_prediction "$pred_root/length")"
    language_pred="$(latest_prediction "$pred_root/language")"
    length_language_pred="$(latest_prediction "$pred_root/length_language")"

    ALLOW_SUBSET=1 bash /ssd1/lbh/zjx/skyjury/auditor/run_audit_report.sh \
      dpo \
      "$original_predictions" \
      "$length_pred" \
      "$language_pred" \
      "$length_language_pred" \
      "$model_report_dir"
  } 2>&1 | tee "$log_path"
}

run_rm_audit \
  "/ssd1/lbh/zjx/models/skyjury_verifier/RLHFlow_ArmoRM-Llama3-8B-v0.1" \
  "$VERIFIER_RESULTS/reward_models/RLHFlow_ArmoRM-Llama3-8B-v0.1/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_RLHFlow_ArmoRM-Llama3-8B-v0.1_predictions.json" \
  "${ARMORM_CUDA_DEVICES:-0}" \
  "${ARMORM_DEVICE_MAP:-none}" \
  "${ARMORM_BATCH_SIZE:-1}"

run_rm_audit \
  "/ssd1/lbh/zjx/models/skyjury_verifier/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft" \
  "$VERIFIER_RESULTS/reward_models/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Ray2333_GRM_Llama3.1_8B_rewardmodel-ft_predictions.json" \
  "${GRM_CUDA_DEVICES:-1}" \
  "${GRM_DEVICE_MAP:-none}" \
  "${GRM_BATCH_SIZE:-1}"

run_rm_audit \
  "/ssd1/lbh/zjx/models/skyjury_verifier/openbmb_Eurus-RM-7b" \
  "$VERIFIER_RESULTS/reward_models/openbmb_Eurus-RM-7b/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_openbmb_Eurus-RM-7b_predictions.json" \
  "${EURUS_CUDA_DEVICES:-2}" \
  "${EURUS_DEVICE_MAP:-none}" \
  "${EURUS_BATCH_SIZE:-1}"

run_rm_audit \
  "/ssd1/lbh/zjx/models/skyjury_verifier/Skywork_Skywork-Reward-Gemma-2-27B-v0.2" \
  "$VERIFIER_RESULTS/reward_models/Skywork_Skywork-Reward-Gemma-2-27B-v0.2/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Skywork_Skywork-Reward-Gemma-2-27B-v0.2_predictions.json" \
  "${SKYWORK_CUDA_DEVICES:-0,1,2,3}" \
  "${SKYWORK_DEVICE_MAP:-auto}" \
  "${SKYWORK_BATCH_SIZE:-1}"

run_dpo_audit \
  "/ssd1/lbh/zjx/models/skyjury_verifier/allenai_tulu-2-dpo-13b" \
  "$VERIFIER_RESULTS/dpo_models/allenai_tulu-2-dpo-13b/skyjury_bench_dpo_ssd1_lbh_zjx_models_skyjury_verifier_allenai_tulu-2-dpo-13b_predictions.json" \
  "${TULU_CUDA_DEVICES:-0,1,2,3}" \
  "${TULU_DEVICE_MAP:-auto}" \
  "${TULU_BATCH_SIZE:-1}"

run_dpo_audit \
  "/ssd1/lbh/zjx/models/skyjury_verifier/upstage_SOLAR-10.7B-Instruct-v1.0" \
  "$VERIFIER_RESULTS/dpo_models/upstage_SOLAR-10.7B-Instruct-v1.0/skyjury_bench_dpo_ssd1_lbh_zjx_models_skyjury_verifier_upstage_SOLAR-10.7B-Instruct-v1.0_predictions.json" \
  "${SOLAR_CUDA_DEVICES:-0,1,2,3}" \
  "${SOLAR_DEVICE_MAP:-auto}" \
  "${SOLAR_BATCH_SIZE:-1}"

echo "All RM/DPO auditor runs completed."
