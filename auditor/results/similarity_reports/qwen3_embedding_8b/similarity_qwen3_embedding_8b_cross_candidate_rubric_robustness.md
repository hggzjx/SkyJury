# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.0361^ | 0.694131 | 0.0000 | 0.5046 -> 0.5048 |
| language | chosen_only | 200 | 0.0036^ | 0.480052 | 0.0000 | 0.5046 -> 0.5045 |
| language | rejected_only | 200 | -0.0595^ | 0.798920 | 0.0000 | 0.5046 -> 0.5048 |
| length | both | 200 | -0.0195^ | 0.612839 | 0.0000 | 0.5046 -> 0.5048 |
| length | chosen_only | 200 | -0.3605^ | 1.000000 | 0.0000 | 0.5046 -> 0.5081 |
| length | rejected_only | 200 | 0.4031^*** | 0.000100 | 0.4031 | 0.5046 -> 0.5013 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0689^ | 0.317968 | 0.0000 | 0.5064 -> 0.5062 |
| language | chosen_only | 50 | 0.5305^*** | 0.000300 | 0.5305 | 0.5064 -> 0.5052 |
| language | rejected_only | 50 | -0.3260^ | 0.986601 | 0.0000 | 0.5064 -> 0.5074 |
| length | both | 50 | 0.2389^ | 0.050195 | 0.0000 | 0.5064 -> 0.5047 |
| length | chosen_only | 50 | -0.6370^ | 0.999900 | 0.0000 | 0.5064 -> 0.5108 |
| length | rejected_only | 50 | 1.0292^*** | 0.000100 | 1.0292 | 0.5064 -> 0.5004 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0481^ | 0.366863 | 0.0000 | 0.5077 -> 0.5074 |
| language | chosen_only | 50 | 0.2305^ | 0.055094 | 0.0000 | 0.5077 -> 0.5067 |
| language | rejected_only | 50 | -0.2029^ | 0.917808 | 0.0000 | 0.5077 -> 0.5084 |
| length | both | 50 | 0.0387^ | 0.396660 | 0.0000 | 0.5077 -> 0.5072 |
| length | chosen_only | 50 | -0.0999^ | 0.753025 | 0.0000 | 0.5077 -> 0.5088 |
| length | rejected_only | 50 | 0.1878^ | 0.094991 | 0.0000 | 0.5077 -> 0.5061 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0084^ | 0.515048 | 0.0000 | 0.4996 -> 0.4996 |
| language | chosen_only | 50 | -0.4108^ | 0.996500 | 0.0000 | 0.4996 -> 0.5011 |
| language | rejected_only | 50 | 0.4119^** | 0.002400 | 0.4119 | 0.4996 -> 0.4980 |
| length | both | 50 | -0.0622^ | 0.668333 | 0.0000 | 0.4996 -> 0.5005 |
| length | chosen_only | 50 | -0.1305^ | 0.815818 | 0.0000 | 0.4996 -> 0.5009 |
| length | rejected_only | 50 | 0.0468^ | 0.370063 | 0.0000 | 0.4996 -> 0.4992 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1801^ | 0.893311 | 0.0000 | 0.5046 -> 0.5059 |
| language | chosen_only | 50 | -0.1034^ | 0.761324 | 0.0000 | 0.5046 -> 0.5052 |
| language | rejected_only | 50 | -0.1747^ | 0.883912 | 0.0000 | 0.5046 -> 0.5054 |
| length | both | 50 | -0.1774^ | 0.889811 | 0.0000 | 0.5046 -> 0.5068 |
| length | chosen_only | 50 | -0.7767^ | 1.000000 | 0.0000 | 0.5046 -> 0.5119 |
| length | rejected_only | 50 | 0.6290^*** | 0.000200 | 0.6290 | 0.5046 -> 0.4995 |
