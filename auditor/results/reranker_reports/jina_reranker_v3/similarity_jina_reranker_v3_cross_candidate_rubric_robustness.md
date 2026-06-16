# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.0989^ | 0.078692 | 0.0000 | 0.5096 -> 0.5087 |
| language | chosen_only | 200 | 0.7156^*** | 0.000100 | 0.7156 | 0.5096 -> 0.5055 |
| language | rejected_only | 200 | -0.4321^ | 1.000000 | 0.0000 | 0.5096 -> 0.5128 |
| length | both | 200 | 0.2900^*** | 0.000100 | 0.2900 | 0.5096 -> 0.5013 |
| length | chosen_only | 200 | 1.6951^*** | 0.000100 | 1.6951 | 0.5096 -> 0.4773 |
| length | rejected_only | 200 | -1.3224^ | 1.000000 | 0.0000 | 0.5096 -> 0.5336 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2555^ | 0.042996 | 0.0000 | 0.5134 -> 0.5109 |
| language | chosen_only | 50 | 0.9146^*** | 0.000100 | 0.9146 | 0.5134 -> 0.5073 |
| language | rejected_only | 50 | -0.5052^ | 0.999900 | 0.0000 | 0.5134 -> 0.5169 |
| length | both | 50 | 0.4656^** | 0.001300 | 0.4656 | 0.5134 -> 0.4987 |
| length | chosen_only | 50 | 1.7441^*** | 0.000100 | 1.7441 | 0.5134 -> 0.4798 |
| length | rejected_only | 50 | -0.9425^ | 1.000000 | 0.0000 | 0.5134 -> 0.5322 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0022^ | 0.489951 | 0.0000 | 0.5085 -> 0.5084 |
| language | chosen_only | 50 | 0.8453^*** | 0.000100 | 0.8453 | 0.5085 -> 0.5047 |
| language | rejected_only | 50 | -0.5159^ | 0.999300 | 0.0000 | 0.5085 -> 0.5122 |
| length | both | 50 | 0.3546^* | 0.010799 | 0.3546 | 0.5085 -> 0.5000 |
| length | chosen_only | 50 | 1.8274^*** | 0.000100 | 1.8274 | 0.5085 -> 0.4742 |
| length | rejected_only | 50 | -1.5791^ | 1.000000 | 0.0000 | 0.5085 -> 0.5342 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1717^ | 0.119188 | 0.0000 | 0.5086 -> 0.5069 |
| language | chosen_only | 50 | 1.3087^*** | 0.000100 | 1.3087 | 0.5086 -> 0.5035 |
| language | rejected_only | 50 | -0.4126^ | 0.997900 | 0.0000 | 0.5086 -> 0.5119 |
| length | both | 50 | 0.2697^ | 0.036596 | 0.0000 | 0.5086 -> 0.4994 |
| length | chosen_only | 50 | 1.4540^*** | 0.000100 | 1.4540 | 0.5086 -> 0.4773 |
| length | rejected_only | 50 | -1.2070^ | 1.000000 | 0.0000 | 0.5086 -> 0.5306 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0264^ | 0.577142 | 0.0000 | 0.5082 -> 0.5084 |
| language | chosen_only | 50 | 0.2455^ | 0.046595 | 0.0000 | 0.5082 -> 0.5066 |
| language | rejected_only | 50 | -0.2975^ | 0.979402 | 0.0000 | 0.5082 -> 0.5100 |
| length | both | 50 | 0.0504^ | 0.361664 | 0.0000 | 0.5082 -> 0.5070 |
| length | chosen_only | 50 | 1.8700^*** | 0.000100 | 1.8700 | 0.5082 -> 0.4778 |
| length | rejected_only | 50 | -1.8340^ | 1.000000 | 0.0000 | 0.5082 -> 0.5373 |
