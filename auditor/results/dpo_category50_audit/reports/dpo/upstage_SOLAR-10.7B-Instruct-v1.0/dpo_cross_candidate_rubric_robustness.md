# SkyJury Cross-Candidate Auditor Report

- method: `dpo`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.0668^ | 0.850315 | 0.0000 | 0.4915 -> 0.5050 |
| language | chosen_only | 200 | -0.3708^ | 1.000000 | 0.0000 | 0.4915 -> 0.6100 |
| language | rejected_only | 200 | 0.4280^*** | 0.000100 | 0.4280 | 0.4915 -> 0.3396 |
| length | both | 200 | -0.1439^ | 0.980802 | 0.0000 | 0.4915 -> 0.5450 |
| length | chosen_only | 200 | -0.8524^ | 1.000000 | 0.0000 | 0.4915 -> 0.9100 |
| length | rejected_only | 200 | 0.8229^*** | 0.000100 | 0.8229 | 0.4915 -> 0.0900 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1429^ | 0.129187 | 0.0000 | 0.4600 -> 0.4400 |
| language | chosen_only | 50 | -0.3333^ | 1.000000 | 0.0000 | 0.4600 -> 0.5600 |
| language | rejected_only | 50 | 0.1429^ | 0.016798 | 0.0000 | 0.4600 -> 0.4400 |
| length | both | 50 | -0.3333^ | 0.995700 | 0.0000 | 0.4600 -> 0.5599 |
| length | chosen_only | 50 | -0.5927^ | 1.000000 | 0.0000 | 0.4600 -> 0.7200 |
| length | rejected_only | 50 | 0.5311^*** | 0.000500 | 0.5311 | 0.4600 -> 0.2400 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1429^ | 0.937706 | 0.0000 | 0.5000 -> 0.5400 |
| language | chosen_only | 50 | -0.3693^ | 1.000000 | 0.0000 | 0.5000 -> 0.6200 |
| language | rejected_only | 50 | 0.4103^** | 0.004600 | 0.4103 | 0.5000 -> 0.3579 |
| length | both | 50 | -0.1818^ | 0.942506 | 0.0000 | 0.5000 -> 0.5800 |
| length | chosen_only | 50 | -0.9230^ | 1.000000 | 0.0000 | 0.5000 -> 0.9600 |
| length | rejected_only | 50 | 0.7829^*** | 0.000100 | 0.7829 | 0.5000 -> 0.1200 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1429^ | 0.245375 | 0.0000 | 0.4600 -> 0.4600 |
| language | chosen_only | 50 | -0.3693^ | 1.000000 | 0.0000 | 0.4600 -> 0.5800 |
| language | rejected_only | 50 | 0.5928^*** | 0.000100 | 0.5928 | 0.4600 -> 0.2005 |
| length | both | 50 | -0.2041^ | 1.000000 | 0.0000 | 0.4600 -> 0.5000 |
| length | chosen_only | 50 | -1.0408^ | 1.000000 | 0.0000 | 0.4600 -> 0.9800 |
| length | rejected_only | 50 | 0.9230^*** | 0.000100 | 0.9230 | 0.4600 -> 0.0000 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1353^ | 0.866513 | 0.0000 | 0.5458 -> 0.5800 |
| language | chosen_only | 50 | -0.4102^ | 1.000000 | 0.0000 | 0.5458 -> 0.6800 |
| language | rejected_only | 50 | 0.4929^*** | 0.000600 | 0.4929 | 0.5458 -> 0.3600 |
| length | both | 50 | 0.0123^ | 0.481452 | 0.0000 | 0.5458 -> 0.5400 |
| length | chosen_only | 50 | -0.8928^ | 1.000000 | 0.0000 | 0.5458 -> 0.9800 |
| length | rejected_only | 50 | 1.1171^*** | 0.000100 | 1.1171 | 0.5458 -> 0.0000 |
