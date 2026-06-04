# SkyJury Cross-Candidate Auditor Report

- method: `rm`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.1414^ | 0.974903 | 0.0000 | 0.5111 -> 0.5260 |
| language | chosen_only | 200 | 0.3901^*** | 0.000100 | 0.3901 | 0.5111 -> 0.4884 |
| language | rejected_only | 200 | -0.4353^ | 1.000000 | 0.0000 | 0.5111 -> 0.5486 |
| length | both | 200 | -0.1801^ | 0.994501 | 0.0000 | 0.5111 -> 0.5408 |
| length | chosen_only | 200 | -0.7727^ | 1.000000 | 0.0000 | 0.5111 -> 0.6347 |
| length | rejected_only | 200 | 0.6951^*** | 0.000100 | 0.6951 | 0.5111 -> 0.4084 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1546^ | 0.837816 | 0.0000 | 0.4936 -> 0.5137 |
| language | chosen_only | 50 | 0.5323^*** | 0.000300 | 0.5323 | 0.4936 -> 0.4616 |
| language | rejected_only | 50 | -0.4228^ | 1.000000 | 0.0000 | 0.4936 -> 0.5442 |
| length | both | 50 | -0.3888^ | 0.995900 | 0.0000 | 0.4936 -> 0.5660 |
| length | chosen_only | 50 | -0.5165^ | 0.999400 | 0.0000 | 0.4936 -> 0.5752 |
| length | rejected_only | 50 | 0.1336^ | 0.178482 | 0.0000 | 0.4936 -> 0.4710 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0510^ | 0.636036 | 0.0000 | 0.5569 -> 0.5609 |
| language | chosen_only | 50 | 0.4229^** | 0.001600 | 0.4229 | 0.5569 -> 0.5327 |
| language | rejected_only | 50 | -0.4795^ | 0.999600 | 0.0000 | 0.5569 -> 0.5868 |
| length | both | 50 | -0.2372^ | 0.946405 | 0.0000 | 0.5569 -> 0.5988 |
| length | chosen_only | 50 | -0.7556^ | 1.000000 | 0.0000 | 0.5569 -> 0.7023 |
| length | rejected_only | 50 | 0.9187^*** | 0.000100 | 0.9187 | 0.5569 -> 0.4409 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.2976^ | 0.979302 | 0.0000 | 0.4605 -> 0.4785 |
| language | chosen_only | 50 | 0.5776^*** | 0.000300 | 0.5776 | 0.4605 -> 0.4326 |
| language | rejected_only | 50 | -1.0683^ | 1.000000 | 0.0000 | 0.4605 -> 0.5058 |
| length | both | 50 | 0.0903^ | 0.270173 | 0.0000 | 0.4605 -> 0.4487 |
| length | chosen_only | 50 | -0.9794^ | 1.000000 | 0.0000 | 0.4605 -> 0.5950 |
| length | rejected_only | 50 | 1.1348^*** | 0.000100 | 1.1348 | 0.4605 -> 0.3113 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1314^ | 0.815218 | 0.0000 | 0.5336 -> 0.5509 |
| language | chosen_only | 50 | 0.1087^ | 0.231377 | 0.0000 | 0.5336 -> 0.5267 |
| language | rejected_only | 50 | -0.2506^ | 0.956704 | 0.0000 | 0.5336 -> 0.5576 |
| length | both | 50 | -0.1096^ | 0.781822 | 0.0000 | 0.5336 -> 0.5498 |
| length | chosen_only | 50 | -0.9636^ | 1.000000 | 0.0000 | 0.5336 -> 0.6663 |
| length | rejected_only | 50 | 0.9652^*** | 0.000100 | 0.9652 | 0.5336 -> 0.4104 |
