# SkyJury Auditor Robustness Risk Report

- method: `llm_judge`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/llm_judge_category50_audit/llm_judge_predictions/deepseek-v4-pro/base/skyjury_bench_base_llm_judge_deepseek-v4-pro_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 198 | paired_t | -0.0326^ | 0.672533 | 0.0000 | confidence 0.5840 -> 0.5867 |
| language | 200 | paired_t | -0.0238^ | 0.636136 | 0.0000 | confidence 0.5855 -> 0.5873 |
| length_language | 198 | paired_t | -0.0528^ | 0.769523 | 0.0000 | confidence 0.5852 -> 0.5900 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1564^ | 0.134187 | 0.0000 | confidence 0.6386 -> 0.6275 |
| length | 49 | paired_t | 0.0993^ | 0.254775 | 0.0000 | confidence 0.6367 -> 0.6286 |
| length_language | 50 | paired_t | 0.0693^ | 0.320368 | 0.0000 | confidence 0.6386 -> 0.6325 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.2207^ | 0.063594 | 0.0000 | confidence 0.6063 -> 0.5905 |
| length | 49 | paired_t | 0.2380^ | 0.050995 | 0.0000 | confidence 0.6037 -> 0.5888 |
| length_language | 49 | paired_t | 0.2439^ | 0.050395 | 0.0000 | confidence 0.6037 -> 0.5851 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1712^ | 0.887411 | 0.0000 | confidence 0.5462 -> 0.5605 |
| length | 50 | paired_t | -0.1878^ | 0.903910 | 0.0000 | confidence 0.5462 -> 0.5648 |
| length_language | 49 | paired_t | -0.2517^ | 0.954305 | 0.0000 | confidence 0.5472 -> 0.5728 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.2593^ | 0.960804 | 0.0000 | confidence 0.5508 -> 0.5709 |
| length | 50 | paired_t | -0.1866^ | 0.899410 | 0.0000 | confidence 0.5508 -> 0.5656 |
| length_language | 50 | paired_t | -0.2011^ | 0.913709 | 0.0000 | confidence 0.5508 -> 0.5693 |
