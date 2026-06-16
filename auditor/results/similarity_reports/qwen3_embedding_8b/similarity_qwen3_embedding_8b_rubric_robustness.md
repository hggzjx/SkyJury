# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/similarity_predictions/qwen3_embedding_8b/base/skyjury_bench_base_similarity_sbert_ssd2_lbh_zjx_models_Qwen_Qwen3-Embedding-8B_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.0195^ | 0.599940 | 0.0000 | confidence 0.5046 -> 0.5048 |
| language | 200 | paired_t | -0.0361^ | 0.705329 | 0.0000 | confidence 0.5046 -> 0.5048 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0689^ | 0.317968 | 0.0000 | confidence 0.5064 -> 0.5062 |
| length | 50 | paired_t | 0.2389^ | 0.051595 | 0.0000 | confidence 0.5064 -> 0.5047 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0481^ | 0.366863 | 0.0000 | confidence 0.5077 -> 0.5074 |
| length | 50 | paired_t | 0.0387^ | 0.385461 | 0.0000 | confidence 0.5077 -> 0.5072 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0084^ | 0.515048 | 0.0000 | confidence 0.4996 -> 0.4996 |
| length | 50 | paired_t | -0.0622^ | 0.671833 | 0.0000 | confidence 0.4996 -> 0.5005 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1801^ | 0.893311 | 0.0000 | confidence 0.5046 -> 0.5059 |
| length | 50 | paired_t | -0.1774^ | 0.889111 | 0.0000 | confidence 0.5046 -> 0.5068 |
