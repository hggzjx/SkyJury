# SkyJury Auditor Robustness Risk Report

- method: `rm`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/reward_models/Skywork_Skywork-Reward-Gemma-2-27B-v0.2/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Skywork_Skywork-Reward-Gemma-2-27B-v0.2_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | 0.0710^ | 0.158784 | 0.0000 | confidence 0.6082 -> 0.5969 |
| language | 200 | paired_t | 0.1196^ | 0.045595 | 0.0000 | confidence 0.6082 -> 0.5952 |
| length_language | 200 | paired_t | 0.1233^ | 0.046695 | 0.0000 | confidence 0.6082 -> 0.5830 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1958^ | 0.089091 | 0.0000 | confidence 0.5919 -> 0.5588 |
| length | 50 | paired_t | -0.0067^ | 0.519648 | 0.0000 | confidence 0.5919 -> 0.5933 |
| length_language | 50 | paired_t | 0.1050^ | 0.234477 | 0.0000 | confidence 0.5919 -> 0.5667 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.4213^** | 0.002800 | 0.4213 | confidence 0.6903 -> 0.6563 |
| length | 50 | paired_t | 0.0832^ | 0.286471 | 0.0000 | confidence 0.6903 -> 0.6794 |
| length_language | 50 | paired_t | 0.2250^ | 0.060594 | 0.0000 | confidence 0.6903 -> 0.6465 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0593^ | 0.661934 | 0.0000 | confidence 0.5407 -> 0.5441 |
| length | 50 | paired_t | 0.0398^ | 0.393161 | 0.0000 | confidence 0.5407 -> 0.5347 |
| length_language | 50 | paired_t | 0.2062^ | 0.074193 | 0.0000 | confidence 0.5407 -> 0.5029 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1454^ | 0.847515 | 0.0000 | confidence 0.6098 -> 0.6217 |
| length | 50 | paired_t | 0.2301^ | 0.054995 | 0.0000 | confidence 0.6098 -> 0.5801 |
| length_language | 50 | paired_t | -0.0321^ | 0.583342 | 0.0000 | confidence 0.6098 -> 0.6159 |
