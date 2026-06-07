# SkyJury Cross-Candidate Auditor Report

- method: `llm_judge`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.0741^ | 0.142586 | 0.0000 | 0.6109 -> 0.6053 |
| language | chosen_only | 200 | 0.0699^ | 0.160884 | 0.0000 | 0.6109 -> 0.6083 |
| language | rejected_only | 200 | 0.0699^ | 0.163884 | 0.0000 | 0.6109 -> 0.6083 |
| length | both | 200 | 0.2439^*** | 0.000400 | 0.2439 | 0.6109 -> 0.5905 |
| length | chosen_only | 200 | 0.2394^*** | 0.000800 | 0.2394 | 0.6109 -> 0.6012 |
| length | rejected_only | 200 | 0.2394^*** | 0.000400 | 0.2394 | 0.6109 -> 0.6012 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0195^ | 0.549845 | 0.0000 | 0.6479 -> 0.6490 |
| language | chosen_only | 50 | -0.0325^ | 0.586441 | 0.0000 | 0.6479 -> 0.6488 |
| language | rejected_only | 50 | -0.0325^ | 0.591141 | 0.0000 | 0.6479 -> 0.6488 |
| length | both | 50 | 0.1830^ | 0.106689 | 0.0000 | 0.6479 -> 0.6364 |
| length | chosen_only | 50 | 0.1712^ | 0.118888 | 0.0000 | 0.6479 -> 0.6426 |
| length | rejected_only | 50 | 0.1712^ | 0.121988 | 0.0000 | 0.6479 -> 0.6426 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0470^ | 0.413859 | 0.0000 | 0.6248 -> 0.6217 |
| language | chosen_only | 50 | 0.0498^ | 0.411359 | 0.0000 | 0.6248 -> 0.6232 |
| language | rejected_only | 50 | 0.0498^ | 0.404960 | 0.0000 | 0.6248 -> 0.6232 |
| length | both | 50 | 0.4307^** | 0.001600 | 0.4307 | 0.6248 -> 0.5945 |
| length | chosen_only | 50 | 0.4317^*** | 0.000800 | 0.4317 | 0.6248 -> 0.6103 |
| length | rejected_only | 50 | 0.4317^** | 0.001200 | 0.4317 | 0.6248 -> 0.6103 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0052^ | 0.516348 | 0.0000 | 0.5647 -> 0.5651 |
| language | chosen_only | 50 | -0.0040^ | 0.501550 | 0.0000 | 0.5647 -> 0.5649 |
| language | rejected_only | 50 | -0.0040^ | 0.517548 | 0.0000 | 0.5647 -> 0.5649 |
| length | both | 50 | -0.0046^ | 0.520548 | 0.0000 | 0.5647 -> 0.5651 |
| length | chosen_only | 50 | 0.0016^ | 0.496550 | 0.0000 | 0.5647 -> 0.5646 |
| length | rejected_only | 50 | 0.0016^ | 0.496050 | 0.0000 | 0.5647 -> 0.5646 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2300^ | 0.059194 | 0.0000 | 0.6063 -> 0.5853 |
| language | chosen_only | 50 | 0.2251^ | 0.063994 | 0.0000 | 0.6063 -> 0.5963 |
| language | rejected_only | 50 | 0.2251^ | 0.060994 | 0.0000 | 0.6063 -> 0.5963 |
| length | both | 50 | 0.4050^** | 0.003100 | 0.4050 | 0.6063 -> 0.5661 |
| length | chosen_only | 50 | 0.3969^** | 0.003600 | 0.3969 | 0.6063 -> 0.5871 |
| length | rejected_only | 50 | 0.3969^** | 0.003900 | 0.3969 | 0.6063 -> 0.5871 |
