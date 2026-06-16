# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.0989^ | 0.914609 | 0.0000 | 0.5038 -> 0.5043 |
| language | chosen_only | 200 | 1.9013^*** | 0.000100 | 1.9013 | 0.5038 -> 0.4966 |
| language | rejected_only | 200 | -1.5814^ | 1.000000 | 0.0000 | 0.5038 -> 0.5115 |
| length | both | 200 | 0.0689^ | 0.171583 | 0.0000 | 0.5038 -> 0.5033 |
| length | chosen_only | 200 | 0.8313^*** | 0.000100 | 0.8313 | 0.5038 -> 0.4992 |
| length | rejected_only | 200 | -0.8074^ | 1.000000 | 0.0000 | 0.5038 -> 0.5078 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1630^ | 0.869813 | 0.0000 | 0.5099 -> 0.5108 |
| language | chosen_only | 50 | 1.7415^*** | 0.000100 | 1.7415 | 0.5099 -> 0.5031 |
| language | rejected_only | 50 | -1.6719^ | 1.000000 | 0.0000 | 0.5099 -> 0.5175 |
| length | both | 50 | 0.2765^ | 0.027897 | 0.0000 | 0.5099 -> 0.5082 |
| length | chosen_only | 50 | 0.8088^*** | 0.000100 | 0.8088 | 0.5099 -> 0.5068 |
| length | rejected_only | 50 | -0.2646^ | 0.963304 | 0.0000 | 0.5099 -> 0.5112 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0760^ | 0.695730 | 0.0000 | 0.5024 -> 0.5028 |
| language | chosen_only | 50 | 2.2288^*** | 0.000100 | 2.2288 | 0.5024 -> 0.4963 |
| language | rejected_only | 50 | -1.6213^ | 1.000000 | 0.0000 | 0.5024 -> 0.5089 |
| length | both | 50 | 0.0675^ | 0.319268 | 0.0000 | 0.5024 -> 0.5019 |
| length | chosen_only | 50 | 0.7580^*** | 0.000100 | 0.7580 | 0.5024 -> 0.4968 |
| length | rejected_only | 50 | -1.0453^ | 1.000000 | 0.0000 | 0.5024 -> 0.5075 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1327^ | 0.821318 | 0.0000 | 0.5010 -> 0.5015 |
| language | chosen_only | 50 | 2.4703^*** | 0.000100 | 2.4703 | 0.5010 -> 0.4948 |
| language | rejected_only | 50 | -2.2474^ | 1.000000 | 0.0000 | 0.5010 -> 0.5077 |
| length | both | 50 | 0.0049^ | 0.496450 | 0.0000 | 0.5010 -> 0.5009 |
| length | chosen_only | 50 | 1.1663^*** | 0.000100 | 1.1663 | 0.5010 -> 0.4953 |
| length | rejected_only | 50 | -1.2669^ | 1.000000 | 0.0000 | 0.5010 -> 0.5066 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0545^ | 0.650135 | 0.0000 | 0.5018 -> 0.5022 |
| language | chosen_only | 50 | 2.1946^*** | 0.000100 | 2.1946 | 0.5018 -> 0.4921 |
| language | rejected_only | 50 | -1.5632^ | 1.000000 | 0.0000 | 0.5018 -> 0.5119 |
| length | both | 50 | -0.0723^ | 0.691631 | 0.0000 | 0.5018 -> 0.5023 |
| length | chosen_only | 50 | 0.8402^*** | 0.000100 | 0.8402 | 0.5018 -> 0.4981 |
| length | rejected_only | 50 | -0.9246^ | 1.000000 | 0.0000 | 0.5018 -> 0.5060 |
