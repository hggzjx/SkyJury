# SkyJury Auditor Robustness Risk Report

- method: `rm`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/reward_models/openbmb_Eurus-RM-7b/skyjury_bench_rm_ssd1_lbh_zjx_models_skyjury_verifier_openbmb_Eurus-RM-7b_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.1374^ | 0.972303 | 0.0000 | confidence 0.4892 -> 0.5675 |
| language | 200 | paired_t | -0.0483^ | 0.765723 | 0.0000 | confidence 0.4892 -> 0.5150 |
| length_language | 200 | paired_t | -0.0991^ | 0.928107 | 0.0000 | confidence 0.4892 -> 0.5550 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.2919^ | 0.989401 | 0.0000 | confidence 0.3746 -> 0.4800 |
| length | 50 | paired_t | -0.1423^ | 0.848215 | 0.0000 | confidence 0.3746 -> 0.4500 |
| length_language | 50 | paired_t | -0.2298^ | 0.955604 | 0.0000 | confidence 0.3746 -> 0.5200 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0042^ | 0.481052 | 0.0000 | confidence 0.5424 -> 0.5400 |
| length | 50 | paired_t | -0.2446^ | 0.957904 | 0.0000 | confidence 0.5424 -> 0.6800 |
| length_language | 50 | paired_t | -0.0821^ | 0.724628 | 0.0000 | confidence 0.5424 -> 0.6000 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0325^ | 0.472653 | 0.0000 | confidence 0.4800 -> 0.4600 |
| length | 50 | paired_t | -0.1345^ | 0.852315 | 0.0000 | confidence 0.4800 -> 0.5600 |
| length_language | 50 | paired_t | -0.0604^ | 0.689131 | 0.0000 | confidence 0.4800 -> 0.5200 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0365^ | 0.618938 | 0.0000 | confidence 0.5600 -> 0.5800 |
| length | 50 | paired_t | -0.0343^ | 0.571743 | 0.0000 | confidence 0.5600 -> 0.5800 |
| length_language | 50 | paired_t | -0.0309^ | 0.615938 | 0.0000 | confidence 0.5600 -> 0.5800 |
