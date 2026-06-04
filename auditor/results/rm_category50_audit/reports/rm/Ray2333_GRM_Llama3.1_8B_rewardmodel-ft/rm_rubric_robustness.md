# SkyJury Auditor Robustness Risk Report

- method: `rm`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/reward_models/Ray2333_GRM_Llama3.1_8B_rewardmodel-ft/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_Ray2333_GRM_Llama3.1_8B_rewardmodel-ft_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.1801^ | 0.994401 | 0.0000 | confidence 0.5111 -> 0.5408 |
| language | 200 | paired_t | -0.1414^ | 0.977302 | 0.0000 | confidence 0.5111 -> 0.5260 |
| length_language | 200 | paired_t | -0.0226^ | 0.620838 | 0.0000 | confidence 0.5111 -> 0.5167 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1546^ | 0.837816 | 0.0000 | confidence 0.4936 -> 0.5137 |
| length | 50 | paired_t | -0.3888^ | 0.996000 | 0.0000 | confidence 0.4936 -> 0.5660 |
| length_language | 50 | paired_t | -0.2204^ | 0.935506 | 0.0000 | confidence 0.4936 -> 0.5370 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0510^ | 0.636036 | 0.0000 | confidence 0.5569 -> 0.5609 |
| length | 50 | paired_t | -0.2372^ | 0.951105 | 0.0000 | confidence 0.5569 -> 0.5988 |
| length_language | 50 | paired_t | -0.0697^ | 0.683232 | 0.0000 | confidence 0.5569 -> 0.5799 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.2976^ | 0.979302 | 0.0000 | confidence 0.4605 -> 0.4785 |
| length | 50 | paired_t | 0.0903^ | 0.260774 | 0.0000 | confidence 0.4605 -> 0.4487 |
| length_language | 50 | paired_t | 0.0524^ | 0.354265 | 0.0000 | confidence 0.4605 -> 0.4521 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1314^ | 0.815218 | 0.0000 | confidence 0.5336 -> 0.5509 |
| length | 50 | paired_t | -0.1096^ | 0.769923 | 0.0000 | confidence 0.5336 -> 0.5498 |
| length_language | 50 | paired_t | 0.1416^ | 0.165183 | 0.0000 | confidence 0.5336 -> 0.4978 |
