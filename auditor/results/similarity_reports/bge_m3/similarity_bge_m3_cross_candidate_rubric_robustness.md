# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.1521^* | 0.016898 | 0.1521 | 0.5011 -> 0.5005 |
| language | chosen_only | 200 | 1.5004^*** | 0.000100 | 1.5004 | 0.5011 -> 0.4970 |
| language | rejected_only | 200 | -1.5565^ | 1.000000 | 0.0000 | 0.5011 -> 0.5045 |
| length | both | 200 | -0.0002^ | 0.503850 | 0.0000 | 0.5011 -> 0.5011 |
| length | chosen_only | 200 | 0.2364^*** | 0.000900 | 0.2364 | 0.5011 -> 0.4996 |
| length | rejected_only | 200 | -0.2429^ | 0.999500 | 0.0000 | 0.5011 -> 0.5025 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.3142^* | 0.014799 | 0.3142 | 0.5038 -> 0.5027 |
| language | chosen_only | 50 | 1.3844^*** | 0.000100 | 1.3844 | 0.5038 -> 0.4998 |
| language | rejected_only | 50 | -1.4771^ | 1.000000 | 0.0000 | 0.5038 -> 0.5067 |
| length | both | 50 | -0.1155^ | 0.789921 | 0.0000 | 0.5038 -> 0.5050 |
| length | chosen_only | 50 | -0.1144^ | 0.786121 | 0.0000 | 0.5038 -> 0.5046 |
| length | rejected_only | 50 | -0.0512^ | 0.632737 | 0.0000 | 0.5038 -> 0.5042 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2289^ | 0.058594 | 0.0000 | 0.5020 -> 0.5010 |
| language | chosen_only | 50 | 1.4925^*** | 0.000100 | 1.4925 | 0.5020 -> 0.4979 |
| language | rejected_only | 50 | -1.2414^ | 1.000000 | 0.0000 | 0.5020 -> 0.5051 |
| length | both | 50 | 0.1761^ | 0.116188 | 0.0000 | 0.5020 -> 0.5003 |
| length | chosen_only | 50 | 0.3954^** | 0.004400 | 0.3954 | 0.5020 -> 0.4990 |
| length | rejected_only | 50 | -0.1844^ | 0.893411 | 0.0000 | 0.5020 -> 0.5033 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1143^ | 0.784122 | 0.0000 | 0.4970 -> 0.4973 |
| language | chosen_only | 50 | 1.2573^*** | 0.000100 | 1.2573 | 0.4970 -> 0.4932 |
| language | rejected_only | 50 | -1.6482^ | 1.000000 | 0.0000 | 0.4970 -> 0.5010 |
| length | both | 50 | -0.1126^ | 0.787021 | 0.0000 | 0.4970 -> 0.4976 |
| length | chosen_only | 50 | 0.4043^** | 0.003600 | 0.4043 | 0.4970 -> 0.4953 |
| length | rejected_only | 50 | -0.5781^ | 1.000000 | 0.0000 | 0.4970 -> 0.4993 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1115^ | 0.216978 | 0.0000 | 0.5014 -> 0.5012 |
| language | chosen_only | 50 | 2.1615^*** | 0.000100 | 2.1615 | 0.5014 -> 0.4972 |
| language | rejected_only | 50 | -2.2631^ | 1.000000 | 0.0000 | 0.5014 -> 0.5054 |
| length | both | 50 | 0.0145^ | 0.459254 | 0.0000 | 0.5014 -> 0.5013 |
| length | chosen_only | 50 | 0.4123^** | 0.002800 | 0.4123 | 0.5014 -> 0.4996 |
| length | rejected_only | 50 | -0.4821^ | 0.999000 | 0.0000 | 0.5014 -> 0.5032 |
