# SkyJury Cross-Candidate Auditor Report

- method: `rm`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.0483^ | 0.772423 | 0.0000 | 0.4892 -> 0.5150 |
| language | chosen_only | 200 | -0.1914^ | 0.996100 | 0.0000 | 0.4892 -> 0.5661 |
| language | rejected_only | 200 | 0.1416^ | 0.024898 | 0.0000 | 0.4892 -> 0.4246 |
| length | both | 200 | -0.1374^ | 0.974903 | 0.0000 | 0.4892 -> 0.5675 |
| length | chosen_only | 200 | -0.7715^ | 1.000000 | 0.0000 | 0.4892 -> 0.8800 |
| length | rejected_only | 200 | 0.6700^*** | 0.000100 | 0.6700 | 0.4892 -> 0.1597 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.2919^ | 0.989401 | 0.0000 | 0.3746 -> 0.4800 |
| language | chosen_only | 50 | -0.3506^ | 0.996800 | 0.0000 | 0.3746 -> 0.4800 |
| language | rejected_only | 50 | 0.0405^ | 0.454855 | 0.0000 | 0.3746 -> 0.3600 |
| length | both | 50 | -0.1423^ | 0.846515 | 0.0000 | 0.3746 -> 0.4500 |
| length | chosen_only | 50 | -0.6130^ | 1.000000 | 0.0000 | 0.3746 -> 0.6800 |
| length | rejected_only | 50 | 0.2600^ | 0.051795 | 0.0000 | 0.3746 -> 0.2800 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0042^ | 0.481052 | 0.0000 | 0.5424 -> 0.5400 |
| language | chosen_only | 50 | 0.1208^ | 0.161284 | 0.0000 | 0.5424 -> 0.4943 |
| language | rejected_only | 50 | 0.0037^ | 0.463054 | 0.0000 | 0.5424 -> 0.5407 |
| length | both | 50 | -0.2446^ | 0.960104 | 0.0000 | 0.5424 -> 0.6800 |
| length | chosen_only | 50 | -0.6913^ | 1.000000 | 0.0000 | 0.5424 -> 0.9000 |
| length | rejected_only | 50 | 0.6400^*** | 0.000100 | 0.6400 | 0.5424 -> 0.2188 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0325^ | 0.472653 | 0.0000 | 0.4800 -> 0.4600 |
| language | chosen_only | 50 | -0.4372^ | 0.999700 | 0.0000 | 0.4800 -> 0.6700 |
| language | rejected_only | 50 | 0.3455^ | 0.009699 | 0.0000 | 0.4800 -> 0.3200 |
| length | both | 50 | -0.1345^ | 0.854015 | 0.0000 | 0.4800 -> 0.5600 |
| length | chosen_only | 50 | -0.9230^ | 1.000000 | 0.0000 | 0.4800 -> 0.9400 |
| length | rejected_only | 50 | 0.8859^*** | 0.000100 | 0.8859 | 0.4800 -> 0.0401 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0365^ | 0.618938 | 0.0000 | 0.5600 -> 0.5800 |
| language | chosen_only | 50 | -0.1428^ | 0.801420 | 0.0000 | 0.5600 -> 0.6199 |
| language | rejected_only | 50 | 0.1575^ | 0.107489 | 0.0000 | 0.5600 -> 0.4776 |
| length | both | 50 | -0.0343^ | 0.567943 | 0.0000 | 0.5600 -> 0.5800 |
| length | chosen_only | 50 | -0.8864^ | 1.000000 | 0.0000 | 0.5600 -> 1.0000 |
| length | rejected_only | 50 | 0.9230^*** | 0.000100 | 0.9230 | 0.5600 -> 0.1000 |
