# SkyJury Cross-Candidate Auditor Report

- method: `llm_judge`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.0238^ | 0.630937 | 0.0000 | 0.5855 -> 0.5873 |
| language | chosen_only | 200 | -0.0287^ | 0.656934 | 0.0000 | 0.5855 -> 0.5866 |
| language | rejected_only | 200 | -0.0287^ | 0.661834 | 0.0000 | 0.5855 -> 0.5866 |
| length | both | 198 | -0.0326^ | 0.678832 | 0.0000 | 0.5840 -> 0.5867 |
| length | chosen_only | 198 | -0.0374^ | 0.698530 | 0.0000 | 0.5840 -> 0.5856 |
| length | rejected_only | 198 | -0.0374^ | 0.698430 | 0.0000 | 0.5840 -> 0.5856 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1564^ | 0.134187 | 0.0000 | 0.6386 -> 0.6275 |
| language | chosen_only | 50 | 0.1558^ | 0.149385 | 0.0000 | 0.6386 -> 0.6332 |
| language | rejected_only | 50 | 0.1558^ | 0.144286 | 0.0000 | 0.6386 -> 0.6332 |
| length | both | 49 | 0.0993^ | 0.242476 | 0.0000 | 0.6367 -> 0.6286 |
| length | chosen_only | 49 | 0.0918^ | 0.264674 | 0.0000 | 0.6367 -> 0.6330 |
| length | rejected_only | 49 | 0.0918^ | 0.271373 | 0.0000 | 0.6367 -> 0.6330 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2207^ | 0.063594 | 0.0000 | 0.6063 -> 0.5905 |
| language | chosen_only | 50 | 0.2165^ | 0.071793 | 0.0000 | 0.6063 -> 0.5987 |
| language | rejected_only | 50 | 0.2165^ | 0.070393 | 0.0000 | 0.6063 -> 0.5987 |
| length | both | 49 | 0.2380^ | 0.057694 | 0.0000 | 0.6037 -> 0.5888 |
| length | chosen_only | 49 | 0.2296^ | 0.060994 | 0.0000 | 0.6037 -> 0.5965 |
| length | rejected_only | 49 | 0.2296^ | 0.059694 | 0.0000 | 0.6037 -> 0.5965 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1712^ | 0.887411 | 0.0000 | 0.5462 -> 0.5605 |
| language | chosen_only | 50 | -0.1780^ | 0.886311 | 0.0000 | 0.5462 -> 0.5536 |
| language | rejected_only | 50 | -0.1780^ | 0.892411 | 0.0000 | 0.5462 -> 0.5536 |
| length | both | 50 | -0.1878^ | 0.898610 | 0.0000 | 0.5462 -> 0.5648 |
| length | chosen_only | 50 | -0.1968^ | 0.911009 | 0.0000 | 0.5462 -> 0.5557 |
| length | rejected_only | 50 | -0.1968^ | 0.909809 | 0.0000 | 0.5462 -> 0.5557 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.2593^ | 0.960804 | 0.0000 | 0.5508 -> 0.5709 |
| language | chosen_only | 50 | -0.2633^ | 0.965403 | 0.0000 | 0.5508 -> 0.5608 |
| language | rejected_only | 50 | -0.2633^ | 0.961504 | 0.0000 | 0.5508 -> 0.5608 |
| length | both | 50 | -0.1866^ | 0.904810 | 0.0000 | 0.5508 -> 0.5656 |
| length | chosen_only | 50 | -0.1879^ | 0.894611 | 0.0000 | 0.5508 -> 0.5582 |
| length | rejected_only | 50 | -0.1879^ | 0.899110 | 0.0000 | 0.5508 -> 0.5582 |
