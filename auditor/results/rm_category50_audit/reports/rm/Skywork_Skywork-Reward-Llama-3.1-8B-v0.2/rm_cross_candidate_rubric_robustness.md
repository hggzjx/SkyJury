# SkyJury Cross-Candidate Auditor Report

- method: `rm`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.0588^ | 0.205479 | 0.0000 | 0.6514 -> 0.6403 |
| language | chosen_only | 200 | 0.3997^*** | 0.000100 | 0.3997 | 0.6514 -> 0.5900 |
| language | rejected_only | 200 | -0.2711^ | 0.999900 | 0.0000 | 0.6514 -> 0.6948 |
| length | both | 200 | -0.0115^ | 0.569543 | 0.0000 | 0.6514 -> 0.6546 |
| length | chosen_only | 200 | 0.0243^ | 0.364564 | 0.0000 | 0.6514 -> 0.6458 |
| length | rejected_only | 200 | 0.0487^ | 0.246575 | 0.0000 | 0.6514 -> 0.6407 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0320^ | 0.406659 | 0.0000 | 0.6853 -> 0.6815 |
| language | chosen_only | 50 | 0.4353^** | 0.001200 | 0.4353 | 0.6853 -> 0.5956 |
| language | rejected_only | 50 | -0.4935^ | 1.000000 | 0.0000 | 0.6853 -> 0.7253 |
| length | both | 50 | 0.2454^ | 0.048195 | 0.0000 | 0.6853 -> 0.6303 |
| length | chosen_only | 50 | 0.4176^** | 0.001600 | 0.4176 | 0.6853 -> 0.5778 |
| length | rejected_only | 50 | -0.0367^ | 0.600540 | 0.0000 | 0.6853 -> 0.6888 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0576^ | 0.342966 | 0.0000 | 0.7295 -> 0.7166 |
| language | chosen_only | 50 | 0.2628^ | 0.031297 | 0.0000 | 0.7295 -> 0.6958 |
| language | rejected_only | 50 | -0.1268^ | 0.794221 | 0.0000 | 0.7295 -> 0.7553 |
| length | both | 50 | -0.1178^ | 0.785721 | 0.0000 | 0.7295 -> 0.7639 |
| length | chosen_only | 50 | -0.1217^ | 0.788621 | 0.0000 | 0.7295 -> 0.7605 |
| length | rejected_only | 50 | -0.1431^ | 0.837216 | 0.0000 | 0.7295 -> 0.7653 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0426^ | 0.380862 | 0.0000 | 0.5434 -> 0.5362 |
| language | chosen_only | 50 | 0.4030^** | 0.001600 | 0.4030 | 0.5434 -> 0.4849 |
| language | rejected_only | 50 | -0.5543^ | 1.000000 | 0.0000 | 0.5434 -> 0.6046 |
| length | both | 50 | -0.1616^ | 0.870913 | 0.0000 | 0.5434 -> 0.5911 |
| length | chosen_only | 50 | -0.1244^ | 0.801720 | 0.0000 | 0.5434 -> 0.5669 |
| length | rejected_only | 50 | -0.0247^ | 0.562244 | 0.0000 | 0.5434 -> 0.5494 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0921^ | 0.262874 | 0.0000 | 0.6475 -> 0.6270 |
| language | chosen_only | 50 | 0.5607^*** | 0.000100 | 0.5607 | 0.6475 -> 0.5836 |
| language | rejected_only | 50 | -0.2285^ | 0.945705 | 0.0000 | 0.6475 -> 0.6943 |
| length | both | 50 | 0.0542^ | 0.353265 | 0.0000 | 0.6475 -> 0.6331 |
| length | chosen_only | 50 | -0.1639^ | 0.866113 | 0.0000 | 0.6475 -> 0.6779 |
| length | rejected_only | 50 | 0.3729^** | 0.004700 | 0.3729 | 0.6475 -> 0.5592 |
