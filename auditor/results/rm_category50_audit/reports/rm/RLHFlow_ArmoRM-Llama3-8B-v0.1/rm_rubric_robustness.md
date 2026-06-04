# SkyJury Auditor Robustness Risk Report

- method: `rm`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/reward_models/RLHFlow_ArmoRM-Llama3-8B-v0.1/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_RLHFlow_ArmoRM-Llama3-8B-v0.1_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | 0.0784^ | 0.149285 | 0.0000 | confidence 0.5024 -> 0.5016 |
| language | 200 | paired_t | 0.0939^ | 0.106289 | 0.0000 | confidence 0.5024 -> 0.5018 |
| length_language | 200 | paired_t | 0.0870^ | 0.115788 | 0.0000 | confidence 0.5024 -> 0.5006 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1762^ | 0.115288 | 0.0000 | confidence 0.5048 -> 0.5023 |
| length | 50 | paired_t | 0.2055^ | 0.075192 | 0.0000 | confidence 0.5048 -> 0.5007 |
| length_language | 50 | paired_t | 0.0776^ | 0.289271 | 0.0000 | confidence 0.5048 -> 0.5029 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1172^ | 0.205179 | 0.0000 | confidence 0.5024 -> 0.5023 |
| length | 50 | paired_t | -0.0939^ | 0.749025 | 0.0000 | confidence 0.5024 -> 0.5027 |
| length_language | 50 | paired_t | 0.2993^ | 0.021598 | 0.0000 | confidence 0.5024 -> 0.4969 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1782^ | 0.110489 | 0.0000 | confidence 0.5010 -> 0.5008 |
| length | 50 | paired_t | -0.0535^ | 0.638036 | 0.0000 | confidence 0.5010 -> 0.5012 |
| length_language | 50 | paired_t | 0.2378^ | 0.049095 | 0.0000 | confidence 0.5010 -> 0.4974 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1705^ | 0.874613 | 0.0000 | confidence 0.5015 -> 0.5017 |
| length | 50 | paired_t | -0.0632^ | 0.637636 | 0.0000 | confidence 0.5015 -> 0.5018 |
| length_language | 50 | paired_t | -0.1708^ | 0.878212 | 0.0000 | confidence 0.5015 -> 0.5053 |
