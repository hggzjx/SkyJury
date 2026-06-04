# SkyJury Cross-Candidate Auditor Report

- method: `dpo`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.0406^ | 0.282172 | 0.0000 | 0.5268 -> 0.5107 |
| language | chosen_only | 200 | -0.0277^ | 0.646135 | 0.0000 | 0.5268 -> 0.5360 |
| language | rejected_only | 200 | 0.1768^** | 0.006599 | 0.1768 | 0.5268 -> 0.4637 |
| length | both | 200 | -0.0568^ | 0.785721 | 0.0000 | 0.5268 -> 0.5532 |
| length | chosen_only | 200 | -0.5872^ | 1.000000 | 0.0000 | 0.5268 -> 0.7934 |
| length | rejected_only | 200 | 0.6180^*** | 0.000100 | 0.6180 | 0.5268 -> 0.2480 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1203^ | 0.214179 | 0.0000 | 0.4628 -> 0.4097 |
| language | chosen_only | 50 | 0.2196^ | 0.065793 | 0.0000 | 0.4628 -> 0.3839 |
| language | rejected_only | 50 | -0.0393^ | 0.606239 | 0.0000 | 0.4628 -> 0.4747 |
| length | both | 50 | -0.2922^ | 0.981002 | 0.0000 | 0.4628 -> 0.5799 |
| length | chosen_only | 50 | -0.5175^ | 1.000000 | 0.0000 | 0.4628 -> 0.6834 |
| length | rejected_only | 50 | 0.3176^ | 0.018698 | 0.0000 | 0.4628 -> 0.3306 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1554^ | 0.151985 | 0.0000 | 0.4897 -> 0.4647 |
| language | chosen_only | 50 | -0.2520^ | 0.971603 | 0.0000 | 0.4897 -> 0.5262 |
| language | rejected_only | 50 | 0.1692^ | 0.129487 | 0.0000 | 0.4897 -> 0.4422 |
| length | both | 50 | -0.1459^ | 0.841716 | 0.0000 | 0.4897 -> 0.5574 |
| length | chosen_only | 50 | -0.9389^ | 1.000000 | 0.0000 | 0.4897 -> 0.9269 |
| length | rejected_only | 50 | 0.7895^*** | 0.000100 | 0.7895 | 0.4897 -> 0.1345 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0919^ | 0.271873 | 0.0000 | 0.6103 -> 0.5878 |
| language | chosen_only | 50 | 0.3387^* | 0.011599 | 0.3387 | 0.6103 -> 0.5180 |
| language | rejected_only | 50 | -0.1946^ | 0.977402 | 0.0000 | 0.6103 -> 0.6229 |
| length | both | 50 | 0.3814^** | 0.002700 | 0.3814 | 0.6103 -> 0.4584 |
| length | chosen_only | 50 | -0.1382^ | 0.838716 | 0.0000 | 0.6103 -> 0.6651 |
| length | rejected_only | 50 | 0.4753^*** | 0.000400 | 0.4753 | 0.6103 -> 0.4012 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0614^ | 0.670533 | 0.0000 | 0.5445 -> 0.5806 |
| language | chosen_only | 50 | -0.4120^ | 0.997200 | 0.0000 | 0.5445 -> 0.7161 |
| language | rejected_only | 50 | 0.4209^** | 0.002700 | 0.4209 | 0.5445 -> 0.3149 |
| length | both | 50 | -0.1363^ | 0.829417 | 0.0000 | 0.5445 -> 0.6171 |
| length | chosen_only | 50 | -0.8224^ | 1.000000 | 0.0000 | 0.5445 -> 0.8982 |
| length | rejected_only | 50 | 0.9530^*** | 0.000100 | 0.9530 | 0.5445 -> 0.1255 |
