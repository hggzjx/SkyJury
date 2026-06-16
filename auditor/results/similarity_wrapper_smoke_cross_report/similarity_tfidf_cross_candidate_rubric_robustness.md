# SkyJury Cross-Candidate Auditor Report

- method: `similarity`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 2 | 1.1510^ | 0.247975 | 0.0000 | 0.5552 -> 0.5310 |
| language | chosen_only | 2 | 9.1716^ | 0.252275 | 0.0000 | 0.5552 -> 0.4914 |
| language | rejected_only | 2 | -2.6760^ | 1.000000 | 0.0000 | 0.5552 -> 0.5942 |
| length | both | 2 | 0.9775^ | 0.498050 | 0.0000 | 0.5552 -> 0.5162 |
| length | chosen_only | 2 | 1.9787^ | 0.256474 | 0.0000 | 0.5552 -> 0.4932 |
| length | rejected_only | 2 | -2.5633^ | 1.000000 | 0.0000 | 0.5552 -> 0.5779 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 2 | 1.1510^ | 0.243676 | 0.0000 | 0.5552 -> 0.5310 |
| language | chosen_only | 2 | 9.1716^ | 0.241376 | 0.0000 | 0.5552 -> 0.4914 |
| language | rejected_only | 2 | -2.6760^ | 1.000000 | 0.0000 | 0.5552 -> 0.5942 |
| length | both | 2 | 0.9775^ | 0.503350 | 0.0000 | 0.5552 -> 0.5162 |
| length | chosen_only | 2 | 1.9787^ | 0.246275 | 0.0000 | 0.5552 -> 0.4932 |
| length | rejected_only | 2 | -2.5633^ | 1.000000 | 0.0000 | 0.5552 -> 0.5779 |
