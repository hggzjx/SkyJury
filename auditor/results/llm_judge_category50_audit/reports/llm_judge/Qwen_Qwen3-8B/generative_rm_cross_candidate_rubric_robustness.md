# SkyJury Cross-Candidate Auditor Report

- method: `llm_judge`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 175 | -0.0804^ | 0.882612 | 0.0000 | 0.5568 -> 0.5647 |
| language | chosen_only | 175 | -0.0819^ | 0.857914 | 0.0000 | 0.5568 -> 0.5608 |
| language | rejected_only | 175 | -0.0819^ | 0.855414 | 0.0000 | 0.5568 -> 0.5608 |
| length | both | 150 | 0.1056^ | 0.123788 | 0.0000 | 0.5724 -> 0.5585 |
| length | chosen_only | 150 | 0.1017^ | 0.123088 | 0.0000 | 0.5724 -> 0.5659 |
| length | rejected_only | 150 | 0.1017^ | 0.126487 | 0.0000 | 0.5724 -> 0.5659 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 45 | -0.1226^ | 0.854015 | 0.0000 | 0.5565 -> 0.5668 |
| language | chosen_only | 45 | -0.1174^ | 0.795520 | 0.0000 | 0.5565 -> 0.5613 |
| language | rejected_only | 45 | -0.1174^ | 0.794621 | 0.0000 | 0.5565 -> 0.5613 |
| length | both | 40 | -0.1158^ | 0.711829 | 0.0000 | 0.5635 -> 0.5809 |
| length | chosen_only | 40 | -0.1155^ | 0.762224 | 0.0000 | 0.5635 -> 0.5720 |
| length | rejected_only | 40 | -0.1155^ | 0.772723 | 0.0000 | 0.5635 -> 0.5720 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 45 | -0.1715^ | 0.933507 | 0.0000 | 0.5822 -> 0.5976 |
| language | chosen_only | 45 | -0.1810^ | 0.939706 | 0.0000 | 0.5822 -> 0.5906 |
| language | rejected_only | 45 | -0.1810^ | 0.935406 | 0.0000 | 0.5822 -> 0.5906 |
| length | both | 45 | 0.2306^ | 0.109589 | 0.0000 | 0.5822 -> 0.5565 |
| length | chosen_only | 45 | 0.2204^ | 0.122988 | 0.0000 | 0.5822 -> 0.5698 |
| length | rejected_only | 45 | 0.2204^ | 0.117888 | 0.0000 | 0.5822 -> 0.5698 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 40 | 0.1327^ | 0.282772 | 0.0000 | 0.5635 -> 0.5462 |
| language | chosen_only | 40 | 0.1318^ | 0.281472 | 0.0000 | 0.5635 -> 0.5550 |
| language | rejected_only | 40 | 0.1318^ | 0.284172 | 0.0000 | 0.5635 -> 0.5550 |
| length | both | 33 | 0.1464^ | 0.273973 | 0.0000 | 0.5770 -> 0.5560 |
| length | chosen_only | 33 | 0.1434^ | 0.269473 | 0.0000 | 0.5770 -> 0.5671 |
| length | rejected_only | 33 | 0.1434^ | 0.266673 | 0.0000 | 0.5770 -> 0.5671 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 45 | -0.2510^ | 0.904310 | 0.0000 | 0.5257 -> 0.5462 |
| language | chosen_only | 45 | -0.2425^ | 0.936806 | 0.0000 | 0.5257 -> 0.5356 |
| language | rejected_only | 45 | -0.2425^ | 0.938106 | 0.0000 | 0.5257 -> 0.5356 |
| length | both | 32 | 0.2582^ | 0.144086 | 0.0000 | 0.5650 -> 0.5361 |
| length | chosen_only | 32 | 0.2582^ | 0.140186 | 0.0000 | 0.5650 -> 0.5514 |
| length | rejected_only | 32 | 0.2582^ | 0.138286 | 0.0000 | 0.5650 -> 0.5514 |
