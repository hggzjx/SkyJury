# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.1386^ | 0.028797 | 0.0000 | 0.4644 -> 0.4468 |
| language | chosen_only | 200 | 0.2356^*** | 0.000900 | 0.2356 | 0.4644 -> 0.4449 |
| language | rejected_only | 200 | -0.0308^ | 0.673033 | 0.0000 | 0.4644 -> 0.4674 |
| length | both | 200 | -0.0131^ | 0.567943 | 0.0000 | 0.4644 -> 0.4681 |
| length | chosen_only | 200 | -0.6123^ | 1.000000 | 0.0000 | 0.4644 -> 0.6031 |
| length | rejected_only | 200 | 0.6187^*** | 0.000100 | 0.6187 | 0.4644 -> 0.3333 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2588^ | 0.037296 | 0.0000 | 0.4810 -> 0.4669 |
| language | chosen_only | 50 | 0.1216^ | 0.197080 | 0.0000 | 0.4810 -> 0.4760 |
| language | rejected_only | 50 | 0.2180^ | 0.066693 | 0.0000 | 0.4810 -> 0.4708 |
| length | both | 50 | -0.0173^ | 0.551345 | 0.0000 | 0.4810 -> 0.4851 |
| length | chosen_only | 50 | -0.7298^ | 1.000000 | 0.0000 | 0.4810 -> 0.6274 |
| length | rejected_only | 50 | 0.5994^*** | 0.000100 | 0.5994 | 0.4810 -> 0.3571 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2075^ | 0.081292 | 0.0000 | 0.5081 -> 0.4797 |
| language | chosen_only | 50 | 0.3326^ | 0.014099 | 0.0000 | 0.5081 -> 0.4789 |
| language | rejected_only | 50 | 0.0049^ | 0.494951 | 0.0000 | 0.5081 -> 0.5077 |
| length | both | 50 | 0.0626^ | 0.331867 | 0.0000 | 0.5081 -> 0.4920 |
| length | chosen_only | 50 | -0.7096^ | 1.000000 | 0.0000 | 0.5081 -> 0.6632 |
| length | rejected_only | 50 | 0.7348^*** | 0.000100 | 0.7348 | 0.5081 -> 0.3392 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2204^ | 0.063094 | 0.0000 | 0.4114 -> 0.3899 |
| language | chosen_only | 50 | 0.3970^** | 0.001700 | 0.3970 | 0.4114 -> 0.3841 |
| language | rejected_only | 50 | -0.1855^ | 0.893811 | 0.0000 | 0.4114 -> 0.4239 |
| length | both | 50 | -0.0931^ | 0.742526 | 0.0000 | 0.4114 -> 0.4396 |
| length | chosen_only | 50 | -0.6779^ | 1.000000 | 0.0000 | 0.4114 -> 0.5975 |
| length | rejected_only | 50 | 0.7077^*** | 0.000100 | 0.7077 | 0.4114 -> 0.2672 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0350^ | 0.408359 | 0.0000 | 0.4572 -> 0.4508 |
| language | chosen_only | 50 | 0.1450^ | 0.169683 | 0.0000 | 0.4572 -> 0.4408 |
| language | rejected_only | 50 | -0.0701^ | 0.686631 | 0.0000 | 0.4572 -> 0.4673 |
| length | both | 50 | 0.0053^ | 0.483652 | 0.0000 | 0.4572 -> 0.4556 |
| length | chosen_only | 50 | -0.3633^ | 0.992401 | 0.0000 | 0.4572 -> 0.5243 |
| length | rejected_only | 50 | 0.4430^** | 0.001400 | 0.4430 | 0.4572 -> 0.3697 |
