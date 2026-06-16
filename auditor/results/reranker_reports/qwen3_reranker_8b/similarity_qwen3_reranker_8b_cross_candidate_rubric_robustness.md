# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.1836^ | 0.999600 | 0.0000 | 0.5024 -> 0.5049 |
| language | chosen_only | 200 | 0.1790^** | 0.004000 | 0.1790 | 0.5024 -> 0.5021 |
| language | rejected_only | 200 | -0.2062^ | 1.000000 | 0.0000 | 0.5024 -> 0.5052 |
| length | both | 200 | -0.1228^ | 0.958304 | 0.0000 | 0.5024 -> 0.5047 |
| length | chosen_only | 200 | 0.2965^*** | 0.000100 | 0.2965 | 0.5024 -> 0.4997 |
| length | rejected_only | 200 | -0.3208^ | 1.000000 | 0.0000 | 0.5024 -> 0.5074 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.3124^ | 0.999600 | 0.0000 | 0.5030 -> 0.5070 |
| language | chosen_only | 50 | 0.3127^ | 0.015298 | 0.0000 | 0.5030 -> 0.5028 |
| language | rejected_only | 50 | -0.3362^ | 0.999900 | 0.0000 | 0.5030 -> 0.5073 |
| length | both | 50 | -0.1585^ | 0.842016 | 0.0000 | 0.5030 -> 0.5061 |
| length | chosen_only | 50 | 0.3630^*** | 0.000100 | 0.3630 | 0.5030 -> 0.5005 |
| length | rejected_only | 50 | -0.3161^ | 1.000000 | 0.0000 | 0.5030 -> 0.5086 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1561^ | 0.898610 | 0.0000 | 0.5046 -> 0.5079 |
| language | chosen_only | 50 | 0.2329^ | 0.092091 | 0.0000 | 0.5046 -> 0.5045 |
| language | rejected_only | 50 | -0.1618^ | 0.973603 | 0.0000 | 0.5046 -> 0.5080 |
| length | both | 50 | -0.3089^ | 0.987001 | 0.0000 | 0.5046 -> 0.5063 |
| length | chosen_only | 50 | 0.4182^*** | 0.000300 | 0.4182 | 0.5046 -> 0.5041 |
| length | rejected_only | 50 | -0.4206^ | 1.000000 | 0.0000 | 0.5046 -> 0.5069 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.2079^ | 0.927107 | 0.0000 | 0.5006 -> 0.5026 |
| language | chosen_only | 50 | 0.3647^*** | 0.001000 | 0.3647 | 0.5006 -> 0.4997 |
| language | rejected_only | 50 | -0.3121^ | 0.999300 | 0.0000 | 0.5006 -> 0.5035 |
| length | both | 50 | -0.0199^ | 0.550645 | 0.0000 | 0.5006 -> 0.5011 |
| length | chosen_only | 50 | 0.3786^*** | 0.000100 | 0.3786 | 0.5006 -> 0.4948 |
| length | rejected_only | 50 | -0.3343^ | 1.000000 | 0.0000 | 0.5006 -> 0.5068 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1208^ | 0.787521 | 0.0000 | 0.5014 -> 0.5021 |
| language | chosen_only | 50 | -0.1039^ | 0.763224 | 0.0000 | 0.5014 -> 0.5016 |
| language | rejected_only | 50 | -0.0992^ | 0.737826 | 0.0000 | 0.5014 -> 0.5020 |
| length | both | 50 | -0.2116^ | 0.928607 | 0.0000 | 0.5014 -> 0.5053 |
| length | chosen_only | 50 | 0.3206^*** | 0.000100 | 0.3206 | 0.5014 -> 0.4994 |
| length | rejected_only | 50 | -0.3589^ | 1.000000 | 0.0000 | 0.5014 -> 0.5074 |
