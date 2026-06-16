# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/similarity_predictions/kalm_gemma3_12b/base/skyjury_bench_base_similarity_sbert_ssd2_lbh_zjx_models_tencent_KaLM-Embedding-Gemma3-12B-2511_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | 0.0689^ | 0.169483 | 0.0000 | confidence 0.5038 -> 0.5033 |
| language | 200 | paired_t | -0.0989^ | 0.919008 | 0.0000 | confidence 0.5038 -> 0.5043 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1630^ | 0.869813 | 0.0000 | confidence 0.5099 -> 0.5108 |
| length | 50 | paired_t | 0.2765^ | 0.027397 | 0.0000 | confidence 0.5099 -> 0.5082 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0760^ | 0.695730 | 0.0000 | confidence 0.5024 -> 0.5028 |
| length | 50 | paired_t | 0.0675^ | 0.321568 | 0.0000 | confidence 0.5024 -> 0.5019 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1327^ | 0.821318 | 0.0000 | confidence 0.5010 -> 0.5015 |
| length | 50 | paired_t | 0.0049^ | 0.489351 | 0.0000 | confidence 0.5010 -> 0.5009 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0545^ | 0.650135 | 0.0000 | confidence 0.5018 -> 0.5022 |
| length | 50 | paired_t | -0.0723^ | 0.695530 | 0.0000 | confidence 0.5018 -> 0.5023 |
