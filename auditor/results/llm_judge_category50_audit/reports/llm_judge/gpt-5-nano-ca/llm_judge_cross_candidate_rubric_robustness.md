# SkyJury Cross-Candidate Auditor Report

- method: `llm_judge`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | -0.0051^ | 0.526047 | 0.0000 | 0.5404 -> 0.5410 |
| language | chosen_only | 200 | -0.0046^ | 0.522148 | 0.0000 | 0.5404 -> 0.5407 |
| language | rejected_only | 200 | -0.0046^ | 0.519848 | 0.0000 | 0.5404 -> 0.5407 |
| length | both | 200 | -0.0368^ | 0.684732 | 0.0000 | 0.5404 -> 0.5457 |
| length | chosen_only | 200 | -0.0360^ | 0.689531 | 0.0000 | 0.5404 -> 0.5430 |
| length | rejected_only | 200 | -0.0360^ | 0.686331 | 0.0000 | 0.5404 -> 0.5430 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0586^ | 0.333767 | 0.0000 | 0.5277 -> 0.5217 |
| language | chosen_only | 50 | 0.0607^ | 0.341366 | 0.0000 | 0.5277 -> 0.5245 |
| language | rejected_only | 50 | 0.0607^ | 0.334367 | 0.0000 | 0.5277 -> 0.5245 |
| length | both | 50 | -0.4228^ | 0.997600 | 0.0000 | 0.5277 -> 0.5883 |
| length | chosen_only | 50 | -0.4325^ | 0.998000 | 0.0000 | 0.5277 -> 0.5580 |
| length | rejected_only | 50 | -0.4325^ | 0.998300 | 0.0000 | 0.5277 -> 0.5580 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0922^ | 0.735226 | 0.0000 | 0.5462 -> 0.5563 |
| language | chosen_only | 50 | -0.0915^ | 0.742126 | 0.0000 | 0.5462 -> 0.5511 |
| language | rejected_only | 50 | -0.0915^ | 0.734227 | 0.0000 | 0.5462 -> 0.5511 |
| length | both | 50 | 0.0966^ | 0.253575 | 0.0000 | 0.5462 -> 0.5347 |
| length | chosen_only | 50 | 0.1026^ | 0.240376 | 0.0000 | 0.5462 -> 0.5401 |
| length | rejected_only | 50 | 0.1026^ | 0.241076 | 0.0000 | 0.5462 -> 0.5401 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.0921^ | 0.271573 | 0.0000 | 0.5323 -> 0.5265 |
| language | chosen_only | 50 | 0.0911^ | 0.262674 | 0.0000 | 0.5323 -> 0.5294 |
| language | rejected_only | 50 | 0.0911^ | 0.276072 | 0.0000 | 0.5323 -> 0.5294 |
| length | both | 50 | 0.0952^ | 0.268073 | 0.0000 | 0.5323 -> 0.5177 |
| length | chosen_only | 50 | 0.0999^ | 0.247375 | 0.0000 | 0.5323 -> 0.5248 |
| length | rejected_only | 50 | 0.0999^ | 0.239776 | 0.0000 | 0.5323 -> 0.5248 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0312^ | 0.575042 | 0.0000 | 0.5555 -> 0.5594 |
| language | chosen_only | 50 | -0.0334^ | 0.599940 | 0.0000 | 0.5555 -> 0.5576 |
| language | rejected_only | 50 | -0.0334^ | 0.596040 | 0.0000 | 0.5555 -> 0.5576 |
| length | both | 50 | 0.0981^ | 0.245675 | 0.0000 | 0.5555 -> 0.5420 |
| length | chosen_only | 50 | 0.0945^ | 0.257374 | 0.0000 | 0.5555 -> 0.5489 |
| length | rejected_only | 50 | 0.0945^ | 0.253775 | 0.0000 | 0.5555 -> 0.5489 |
