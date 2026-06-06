# SkyJury Cross-Candidate Auditor Report

- method: `llm_judge`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.0726^ | 0.149285 | 0.0000 | 0.6086 -> 0.6035 |
| language | chosen_only | 200 | 0.0664^ | 0.176482 | 0.0000 | 0.6086 -> 0.6063 |
| language | rejected_only | 200 | 0.0664^ | 0.182282 | 0.0000 | 0.6086 -> 0.6063 |
| length | both | 200 | 0.0432^ | 0.273873 | 0.0000 | 0.6086 -> 0.6048 |
| length | chosen_only | 200 | 0.0386^ | 0.293871 | 0.0000 | 0.6086 -> 0.6069 |
| length | rejected_only | 200 | 0.0386^ | 0.302170 | 0.0000 | 0.6086 -> 0.6069 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0205^ | 0.549145 | 0.0000 | 0.6386 -> 0.6407 |
| language | chosen_only | 50 | -0.0309^ | 0.585841 | 0.0000 | 0.6386 -> 0.6402 |
| language | rejected_only | 50 | -0.0309^ | 0.578242 | 0.0000 | 0.6386 -> 0.6402 |
| length | both | 50 | -0.1922^ | 0.906509 | 0.0000 | 0.6386 -> 0.6590 |
| length | chosen_only | 50 | -0.1985^ | 0.909509 | 0.0000 | 0.6386 -> 0.6490 |
| length | rejected_only | 50 | -0.1985^ | 0.907709 | 0.0000 | 0.6386 -> 0.6490 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0660^ | 0.344666 | 0.0000 | 0.6109 -> 0.6067 |
| language | chosen_only | 50 | 0.0651^ | 0.344166 | 0.0000 | 0.6109 -> 0.6089 |
| language | rejected_only | 50 | 0.0651^ | 0.344166 | 0.0000 | 0.6109 -> 0.6089 |
| length | both | 50 | 0.1653^ | 0.140486 | 0.0000 | 0.6109 -> 0.5983 |
| length | chosen_only | 50 | 0.1668^ | 0.115788 | 0.0000 | 0.6109 -> 0.6049 |
| length | rejected_only | 50 | 0.1668^ | 0.126687 | 0.0000 | 0.6109 -> 0.6049 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0511^ | 0.370463 | 0.0000 | 0.5693 -> 0.5666 |
| language | chosen_only | 50 | 0.0436^ | 0.385961 | 0.0000 | 0.5693 -> 0.5682 |
| language | rejected_only | 50 | 0.0436^ | 0.385961 | 0.0000 | 0.5693 -> 0.5682 |
| length | both | 50 | 0.0785^ | 0.303670 | 0.0000 | 0.5693 -> 0.5614 |
| length | chosen_only | 50 | 0.0748^ | 0.313969 | 0.0000 | 0.5693 -> 0.5656 |
| length | rejected_only | 50 | 0.0748^ | 0.307869 | 0.0000 | 0.5693 -> 0.5656 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.2826^ | 0.021998 | 0.0000 | 0.6155 -> 0.5998 |
| language | chosen_only | 50 | 0.2864^ | 0.022498 | 0.0000 | 0.6155 -> 0.6079 |
| language | rejected_only | 50 | 0.2864^ | 0.022798 | 0.0000 | 0.6155 -> 0.6079 |
| length | both | 50 | 0.2777^ | 0.030297 | 0.0000 | 0.6155 -> 0.6005 |
| length | chosen_only | 50 | 0.2787^ | 0.032597 | 0.0000 | 0.6155 -> 0.6082 |
| length | rejected_only | 50 | 0.2787^ | 0.032997 | 0.0000 | 0.6155 -> 0.6082 |
