# SkyJury Auditor

SkyJury Auditor measures whether verifier preference confidence is robust to meaning-preserving rubric perturbations.

## Current Data

- Base benchmark: `/ssd1/lbh/zjx/skyjury/data/skyjury_bench.json`
- Auditor datasets: `/ssd1/lbh/zjx/skyjury/data/auditor`
- Default auditor subset: `/ssd1/lbh/zjx/skyjury/data/auditor/category50`

The active auditor files are:

```text
skyjury_bench_base.json
skyjury_bench_rubric_length.json
skyjury_bench_rubric_language.json
skyjury_bench_rubric_perturbation_manifest.json
```

The current auditor evaluation uses a fixed category-balanced subset rather than verifier-success filtering:

```text
50 samples per category x 4 categories = 200 samples
```

This keeps cross-model auditor comparisons aligned on the same sample set while still reporting both overall and per-category robustness.

Build or refresh the subset from the full auditor data:

```bash
python build_category_subset.py \
  --data-dir /ssd1/lbh/zjx/skyjury/data/auditor \
  --output-dir /ssd1/lbh/zjx/skyjury/data/auditor/category50 \
  --prefix skyjury_bench \
  --per-category 50 \
  --seed 13
```

## Build Perturbations

Use the direct LLM perturbation builder:

```bash
source activate rm_dev
cd /ssd1/lbh/zjx/skyjury/auditor

bash build_llm_rubric_perturbations.sh
```

Or run it manually:

```bash
python build_llm_rubric_perturbations.py \
  --data /ssd1/lbh/zjx/skyjury/data/skyjury_bench.json \
  --output-dir /ssd1/lbh/zjx/skyjury/data/auditor \
  --prefix skyjury_bench \
  --model deepseek-v4-flash \
  --concurrency 8 \
  --request-jitter 8 \
  --timeout 180 \
  --retries 8 \
  --max-tokens 12000
```

Perturbations:

- `length`: expand each rubric definition in English while preserving the original scope.
- `language`: translate each original rubric definition into Spanish.

Only candidate Labeler `Rubrics:` sections are changed.

The active cross-candidate auditor reports six robustness risks:

```text
length x {both, chosen_only, rejected_only}
language x {both, chosen_only, rejected_only}
```

## Run Perturbed Verifiers

LLM-as-judge:

```bash
bash run_llm_judge_perturbations.sh gpt-4o-ca 8 \
  /ssd1/lbh/zjx/skyjury/data/auditor/category50 \
  /ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_predictions \
  skyjury_bench
```

Reward model:

```bash
bash run_rm_perturbations.sh
```

By default this loops over the 5 local RM models and uses `BATCH_SIZE=4`.
Pass a model path as the first argument to run a single RM.

DPO/instruction model:

```bash
bash run_dpo_perturbations.sh
```

By default this loops over the 2 local DPO/instruction models and uses `BATCH_SIZE=4`.
Pass a model path as the first argument to run a single DPO model.

LLM-as-judge:

```bash
bash run_llm_judge_perturbations.sh
```

By default this loops over `gpt-5-ca`, `gpt-4o-ca`, `deepseek-v4-flash`, `qwen3.5-plus`, and `glm-5` with concurrency 4.

Full auditor runners by model family:

```bash
bash run_all_rm_auditor.sh
bash run_all_dpo_auditor.sh
bash run_all_llm_judge_auditor.sh
```

## Statistics

All verifier types are converted to preference confidence:

```text
confidence = sigmoid(chosen_score - rejected_score)
```

For LLM-as-judge, `chosen_score` and `rejected_score` are repeated bidirectional selection rates.

The auditor compares original vs perturbed confidence using paired permutation tests over the paired t-statistic, then applies Benjamini-Hochberg correction across the six cross-candidate tests. Reports include overall and per-`category` results. Because perturbed predictions are normally run on the 200-row category-balanced subset while original verifier predictions may be full-set, the all-in-one auditor scripts first materialize the matching base subset from full verifier predictions.

## Report

```bash
python audit_cross_candidate_perturbations.py \
  --method <rm|dpo|llm_judge> \
  --original /path/to/original_predictions.json \
  --perturbed length=/path/to/length_predictions.json \
  --perturbed language=/path/to/language_predictions.json \
  --output-dir /path/to/output_report_dir \
  --report-name <method>_cross_candidate_rubric_robustness \
  --allow-subset
```

Legacy cache-based perturbation scripts were moved to `archive_legacy_20260603/`.
