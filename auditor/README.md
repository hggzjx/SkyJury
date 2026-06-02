# SkyJury Auditor

SkyJury Auditor measures whether a verifier is robust to meaning-preserving rubric perturbations.
It follows the RewardAuditor framing, but adapts the statistic for SkyJury's labeler-preference task.

## Verifier-to-Auditor Flow

The intended evaluation line is:

```text
original dataset -> verifier predictions -> keep verifier-success cases -> rubric perturbations -> verifier rerun -> auditor report
```

The auditor should normally operate only on cases that the verifier originally answered correctly. This avoids measuring robustness on examples where the verifier had already failed before any perturbation.

Prepare perturbation datasets from verifier-success cases:

```bash
bash /ssd1/lbh/zjx/skyjury/auditor/prepare_success_case_perturbations.sh \
  /ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json \
  /path/to/original_verifier_predictions.json \
  /ssd1/lbh/zjx/skyjury/data/auditor \
  verifier_success_cases
```

This creates:

- `verifier_success_cases_rubric_length.json`
- `verifier_success_cases_rubric_language.json`
- `verifier_success_cases_rubric_length_language.json`

## Perturbations

The auditor builds three rubric-only variants from `data/verifier_pilot_rmbench.json`:

- `length`: lengthens rubric definitions with a semantic-preserving operational restatement.
- `language`: adds Chinese language variation while anchoring the original definition.
- `length_language`: combines longer wording and language variation.

Only the candidate Labeler `Rubrics:` sections are changed. User profiles, chosen/rejected identities, handles, display names, and descriptions are left untouched.

Build the perturbation datasets:

```bash
bash /ssd1/lbh/zjx/skyjury/auditor/build_perturbations.sh
```

Outputs are written to `/ssd1/lbh/zjx/skyjury/data/auditor/`.

## Verifier Runs

Run the same verifier on the original data and the three perturbed datasets.

For LLM-as-judge perturbations:

```bash
bash /ssd1/lbh/zjx/skyjury/auditor/run_llm_judge_perturbations.sh \
  gpt-4o-ca \
  8 \
  /ssd1/lbh/zjx/skyjury/data/auditor \
  /ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_predictions \
  verifier_success_cases
```

For sequence-classification reward models:

```bash
bash /ssd1/lbh/zjx/skyjury/auditor/run_rm_perturbations.sh /path/to/rm
```

For DPO/instruction models:

```bash
bash /ssd1/lbh/zjx/skyjury/auditor/run_dpo_perturbations.sh /path/to/dpo
```

## Statistics

For RM and DPO outputs, the auditor follows the RewardAuditor paired-test style, but uses SkyJury preference confidence rather than loss:

1. Compute margin: `chosen_score - rejected_score`.
2. Transform margin to preference confidence: `sigmoid(chosen_score - rejected_score)`.
3. Compare original vs perturbed confidence with a paired permutation test over the paired t-statistic.
4. Use Cohen's d as the effect size.

The RM/DPO test is one-sided in the degradation direction:

- `delta = original_confidence - perturbed_confidence`
- small p-values indicate perturbed rubrics significantly decrease preference confidence for the verified chosen labeler.

For LLM-as-judge outputs, each repeated judge call is converted to one of:

- `chosen`
- `rejected`
- `tie`

The statistic is mean per-sample Jensen-Shannon Distance between original and perturbed outcome distributions. The permutation test shuffles repeated outcomes between the original and perturbed conditions within each sample.

All perturbation tests are then corrected with Benjamini-Hochberg control. The report uses the compact format:

```text
effect_size^significance
```

Examples: `0.0023^**`, `-0.1841^*`, `0.0312^`.

Reports include both an overall table and one table per `category`:

- `safety_moderation`
- `identity_trust`
- `interest_community`
- `platform_information_ecology`

## Generate Robustness Risk Report

Pass the original prediction file and the three perturbed prediction files explicitly:

```bash
bash /ssd1/lbh/zjx/skyjury/auditor/run_audit_report.sh \
  llm_judge \
  /path/to/original_predictions.json \
  /path/to/length_predictions.json \
  /path/to/language_predictions.json \
  /path/to/length_language_predictions.json
```

Reports are saved under `/ssd1/lbh/zjx/skyjury/auditor/results/`.

`run_audit_report.sh` allows subset alignment by default, so the original prediction file can be full-size while the perturbed prediction files contain only verifier-success cases. Set `ALLOW_SUBSET=0` before the command if strict full-dataset alignment is required.
