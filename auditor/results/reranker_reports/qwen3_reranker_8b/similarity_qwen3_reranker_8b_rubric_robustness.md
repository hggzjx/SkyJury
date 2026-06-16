# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/reranker_predictions/qwen3_reranker_8b/base/skyjury_bench_base_similarity_reranker_ssd2_lbh_zjx_models_Qwen_Qwen3-Reranker-8B_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.1228^ | 0.960604 | 0.0000 | confidence 0.5024 -> 0.5047 |
| language | 200 | paired_t | -0.1836^ | 0.999300 | 0.0000 | confidence 0.5024 -> 0.5049 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.3124^ | 0.999600 | 0.0000 | confidence 0.5030 -> 0.5070 |
| length | 50 | paired_t | -0.1585^ | 0.836016 | 0.0000 | confidence 0.5030 -> 0.5061 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1561^ | 0.898610 | 0.0000 | confidence 0.5046 -> 0.5079 |
| length | 50 | paired_t | -0.3089^ | 0.987001 | 0.0000 | confidence 0.5046 -> 0.5063 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.2079^ | 0.927107 | 0.0000 | confidence 0.5006 -> 0.5026 |
| length | 50 | paired_t | -0.0199^ | 0.554845 | 0.0000 | confidence 0.5006 -> 0.5011 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1208^ | 0.787521 | 0.0000 | confidence 0.5014 -> 0.5021 |
| length | 50 | paired_t | -0.2116^ | 0.928107 | 0.0000 | confidence 0.5014 -> 0.5053 |
