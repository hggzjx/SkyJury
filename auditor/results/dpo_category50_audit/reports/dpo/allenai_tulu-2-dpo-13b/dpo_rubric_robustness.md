# SkyJury Auditor Robustness Risk Report

- method: `dpo`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/dpo_models/allenai_tulu-2-dpo-13b/skyjury_bench_dpo_ssd1_lbh_zjx_models_skyjury_verifier_allenai_tulu-2-dpo-13b_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.0568^ | 0.791021 | 0.0000 | confidence 0.5268 -> 0.5532 |
| language | 200 | paired_t | 0.0406^ | 0.287171 | 0.0000 | confidence 0.5268 -> 0.5107 |
| length_language | 200 | paired_t | -0.0451^ | 0.735726 | 0.0000 | confidence 0.5268 -> 0.5511 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1203^ | 0.214179 | 0.0000 | confidence 0.4628 -> 0.4097 |
| length | 50 | paired_t | -0.2922^ | 0.981402 | 0.0000 | confidence 0.4628 -> 0.5799 |
| length_language | 50 | paired_t | -0.2432^ | 0.960604 | 0.0000 | confidence 0.4628 -> 0.5828 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1554^ | 0.151985 | 0.0000 | confidence 0.4897 -> 0.4647 |
| length | 50 | paired_t | -0.1459^ | 0.843816 | 0.0000 | confidence 0.4897 -> 0.5574 |
| length_language | 50 | paired_t | -0.1666^ | 0.877312 | 0.0000 | confidence 0.4897 -> 0.5874 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0919^ | 0.271873 | 0.0000 | confidence 0.6103 -> 0.5878 |
| length | 50 | paired_t | 0.3814^ | 0.003400 | 0.0000 | confidence 0.6103 -> 0.4584 |
| length_language | 50 | paired_t | 0.2727^ | 0.030297 | 0.0000 | confidence 0.6103 -> 0.4903 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0614^ | 0.670533 | 0.0000 | confidence 0.5445 -> 0.5806 |
| length | 50 | paired_t | -0.1363^ | 0.830317 | 0.0000 | confidence 0.5445 -> 0.6171 |
| length_language | 50 | paired_t | 0.0007^ | 0.500150 | 0.0000 | confidence 0.5445 -> 0.5440 |
