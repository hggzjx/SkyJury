# SkyJury Auditor Robustness Risk Report

- method: `rm`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/reward_models/Skywork_Skywork-Reward-Llama-3.1-8B-v0.2/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Skywork_Skywork-Reward-Llama-3.1-8B-v0.2_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.0115^ | 0.561444 | 0.0000 | confidence 0.6514 -> 0.6546 |
| language | 200 | paired_t | 0.0588^ | 0.207379 | 0.0000 | confidence 0.6514 -> 0.6403 |
| length_language | 200 | paired_t | 0.0700^ | 0.168783 | 0.0000 | confidence 0.6514 -> 0.6186 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0320^ | 0.406659 | 0.0000 | confidence 0.6853 -> 0.6815 |
| length | 50 | paired_t | 0.2454^ | 0.044596 | 0.0000 | confidence 0.6853 -> 0.6303 |
| length_language | 50 | paired_t | 0.0400^ | 0.389761 | 0.0000 | confidence 0.6853 -> 0.6677 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0576^ | 0.342966 | 0.0000 | confidence 0.7295 -> 0.7166 |
| length | 50 | paired_t | -0.1178^ | 0.786821 | 0.0000 | confidence 0.7295 -> 0.7639 |
| length_language | 50 | paired_t | 0.2281^ | 0.062794 | 0.0000 | confidence 0.7295 -> 0.6315 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0426^ | 0.380862 | 0.0000 | confidence 0.5434 -> 0.5362 |
| length | 50 | paired_t | -0.1616^ | 0.867413 | 0.0000 | confidence 0.5434 -> 0.5911 |
| length_language | 50 | paired_t | -0.0205^ | 0.559044 | 0.0000 | confidence 0.5434 -> 0.5547 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0921^ | 0.262874 | 0.0000 | confidence 0.6475 -> 0.6270 |
| length | 50 | paired_t | 0.0542^ | 0.353865 | 0.0000 | confidence 0.6475 -> 0.6331 |
| length_language | 50 | paired_t | 0.0620^ | 0.342066 | 0.0000 | confidence 0.6475 -> 0.6205 |
