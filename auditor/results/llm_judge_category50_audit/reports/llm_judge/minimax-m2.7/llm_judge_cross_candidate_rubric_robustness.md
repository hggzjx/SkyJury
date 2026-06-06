# SkyJury Cross-Candidate Auditor Report

- method: `llm_judge`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 199 | -0.0308^ | 0.675932 | 0.0000 | 0.5987 -> 0.6015 |
| language | chosen_only | 199 | -0.0376^ | 0.695330 | 0.0000 | 0.5987 -> 0.6004 |
| language | rejected_only | 199 | -0.0376^ | 0.703930 | 0.0000 | 0.5987 -> 0.6004 |
| length | both | 200 | -0.0479^ | 0.758024 | 0.0000 | 0.5982 -> 0.6031 |
| length | chosen_only | 200 | -0.0561^ | 0.791621 | 0.0000 | 0.5982 -> 0.6010 |
| length | rejected_only | 200 | -0.0561^ | 0.782522 | 0.0000 | 0.5982 -> 0.6010 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 49 | 0.0312^ | 0.425257 | 0.0000 | 0.6415 -> 0.6386 |
| language | chosen_only | 49 | 0.0319^ | 0.413059 | 0.0000 | 0.6415 -> 0.6401 |
| language | rejected_only | 49 | 0.0319^ | 0.411259 | 0.0000 | 0.6415 -> 0.6401 |
| length | both | 50 | 0.0087^ | 0.472153 | 0.0000 | 0.6386 -> 0.6377 |
| length | chosen_only | 50 | 0.0110^ | 0.477352 | 0.0000 | 0.6386 -> 0.6381 |
| length | rejected_only | 50 | 0.0110^ | 0.472953 | 0.0000 | 0.6386 -> 0.6381 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.2568^ | 0.962004 | 0.0000 | 0.6063 -> 0.6239 |
| language | chosen_only | 50 | -0.2584^ | 0.963004 | 0.0000 | 0.6063 -> 0.6152 |
| language | rejected_only | 50 | -0.2584^ | 0.963804 | 0.0000 | 0.6063 -> 0.6152 |
| length | both | 50 | -0.1419^ | 0.838916 | 0.0000 | 0.6063 -> 0.6195 |
| length | chosen_only | 50 | -0.1468^ | 0.841316 | 0.0000 | 0.6063 -> 0.6131 |
| length | rejected_only | 50 | -0.1468^ | 0.842916 | 0.0000 | 0.6063 -> 0.6131 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0407^ | 0.391461 | 0.0000 | 0.5832 -> 0.5784 |
| language | chosen_only | 50 | 0.0316^ | 0.414559 | 0.0000 | 0.5832 -> 0.5814 |
| language | rejected_only | 50 | 0.0316^ | 0.409459 | 0.0000 | 0.5832 -> 0.5814 |
| length | both | 50 | 0.0264^ | 0.438356 | 0.0000 | 0.5832 -> 0.5800 |
| length | chosen_only | 50 | 0.0092^ | 0.476352 | 0.0000 | 0.5832 -> 0.5826 |
| length | rejected_only | 50 | 0.0092^ | 0.476152 | 0.0000 | 0.5832 -> 0.5826 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0137^ | 0.525747 | 0.0000 | 0.5647 -> 0.5659 |
| language | chosen_only | 50 | -0.0256^ | 0.569243 | 0.0000 | 0.5647 -> 0.5658 |
| language | rejected_only | 50 | -0.0256^ | 0.572343 | 0.0000 | 0.5647 -> 0.5658 |
| length | both | 50 | -0.1252^ | 0.804420 | 0.0000 | 0.5647 -> 0.5751 |
| length | chosen_only | 50 | -0.1342^ | 0.821918 | 0.0000 | 0.5647 -> 0.5703 |
| length | rejected_only | 50 | -0.1342^ | 0.820818 | 0.0000 | 0.5647 -> 0.5703 |
