# SkyJury Auditor Robustness Risk Report

- method: `dpo`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/dpo_models/upstage_SOLAR-10.7B-Instruct-v1.0/skyjury_bench_dpo_ssd1_lbh_zjx_models_skyjury_verifier_upstage_SOLAR-10.7B-Instruct-v1.0_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.1439^ | 0.977802 | 0.0000 | confidence 0.4915 -> 0.5450 |
| language | 200 | paired_t | -0.0668^ | 0.845215 | 0.0000 | confidence 0.4915 -> 0.5050 |
| length_language | 200 | paired_t | -0.1609^ | 0.987501 | 0.0000 | confidence 0.4915 -> 0.5600 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1429^ | 0.129187 | 0.0000 | confidence 0.4600 -> 0.4400 |
| length | 50 | paired_t | -0.3333^ | 0.995000 | 0.0000 | confidence 0.4600 -> 0.5599 |
| length_language | 50 | paired_t | -0.1625^ | 0.856014 | 0.0000 | confidence 0.4600 -> 0.5200 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1429^ | 0.937706 | 0.0000 | confidence 0.5000 -> 0.5400 |
| length | 50 | paired_t | -0.1818^ | 0.945905 | 0.0000 | confidence 0.5000 -> 0.5800 |
| length_language | 50 | paired_t | -0.3245^ | 0.993201 | 0.0000 | confidence 0.5000 -> 0.6800 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1429^ | 0.245375 | 0.0000 | confidence 0.4600 -> 0.4600 |
| length | 50 | paired_t | -0.2041^ | 1.000000 | 0.0000 | confidence 0.4600 -> 0.5000 |
| length_language | 50 | paired_t | -0.2041^ | 1.000000 | 0.0000 | confidence 0.4600 -> 0.5000 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1353^ | 0.866513 | 0.0000 | confidence 0.5458 -> 0.5800 |
| length | 50 | paired_t | 0.0123^ | 0.496350 | 0.0000 | confidence 0.5458 -> 0.5400 |
| length_language | 50 | paired_t | 0.0123^ | 0.497050 | 0.0000 | confidence 0.5458 -> 0.5400 |
