# SkyJury Cross-Candidate Auditor Report

- method: `rm`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.0939^ | 0.098090 | 0.0000 | 0.5024 -> 0.5018 |
| language | chosen_only | 200 | 0.1406^** | 0.003600 | 0.1406 | 0.5024 -> 0.5018 |
| language | rejected_only | 200 | 0.0033^ | 0.482852 | 0.0000 | 0.5024 -> 0.5024 |
| length | both | 200 | 0.0784^ | 0.154885 | 0.0000 | 0.5024 -> 0.5016 |
| length | chosen_only | 200 | -0.0482^ | 0.740026 | 0.0000 | 0.5024 -> 0.5027 |
| length | rejected_only | 200 | 0.1129^ | 0.037496 | 0.0000 | 0.5024 -> 0.5014 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1762^ | 0.115288 | 0.0000 | 0.5048 -> 0.5023 |
| language | chosen_only | 50 | 0.0435^ | 0.464854 | 0.0000 | 0.5048 -> 0.5044 |
| language | rejected_only | 50 | 0.1976^ | 0.125587 | 0.0000 | 0.5048 -> 0.5027 |
| length | both | 50 | 0.2055^ | 0.080392 | 0.0000 | 0.5048 -> 0.5007 |
| length | chosen_only | 50 | 0.1908^ | 0.098590 | 0.0000 | 0.5048 -> 0.5032 |
| length | rejected_only | 50 | 0.1427^ | 0.198280 | 0.0000 | 0.5048 -> 0.5022 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1172^ | 0.205179 | 0.0000 | 0.5024 -> 0.5023 |
| language | chosen_only | 50 | 0.7207^*** | 0.000100 | 0.7207 | 0.5024 -> 0.5018 |
| language | rejected_only | 50 | -0.4400^ | 0.998200 | 0.0000 | 0.5024 -> 0.5029 |
| length | both | 50 | -0.0939^ | 0.740326 | 0.0000 | 0.5024 -> 0.5027 |
| length | chosen_only | 50 | -0.2464^ | 0.954905 | 0.0000 | 0.5024 -> 0.5031 |
| length | rejected_only | 50 | 0.1244^ | 0.199580 | 0.0000 | 0.5024 -> 0.5021 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1782^ | 0.110489 | 0.0000 | 0.5010 -> 0.5008 |
| language | chosen_only | 50 | 0.8284^*** | 0.000100 | 0.8284 | 0.5010 -> 0.5001 |
| language | rejected_only | 50 | -0.7411^ | 1.000000 | 0.0000 | 0.5010 -> 0.5017 |
| length | both | 50 | -0.0535^ | 0.649835 | 0.0000 | 0.5010 -> 0.5012 |
| length | chosen_only | 50 | -0.2913^ | 0.978702 | 0.0000 | 0.5010 -> 0.5019 |
| length | rejected_only | 50 | 0.3289^ | 0.013199 | 0.0000 | 0.5010 -> 0.5003 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1705^ | 0.874613 | 0.0000 | 0.5015 -> 0.5017 |
| language | chosen_only | 50 | 0.6966^*** | 0.000100 | 0.6966 | 0.5015 -> 0.5009 |
| language | rejected_only | 50 | -0.7232^ | 1.000000 | 0.0000 | 0.5015 -> 0.5023 |
| length | both | 50 | -0.0632^ | 0.644536 | 0.0000 | 0.5015 -> 0.5018 |
| length | chosen_only | 50 | -0.4467^ | 0.997500 | 0.0000 | 0.5015 -> 0.5025 |
| length | rejected_only | 50 | 0.1652^ | 0.138186 | 0.0000 | 0.5015 -> 0.5009 |
