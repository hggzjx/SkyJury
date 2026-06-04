# SkyJury Cross-Candidate Auditor Report

- method: `rm`
- variants: `both`, `chosen_only`, `rejected_only`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 200 | 0.1196^ | 0.043996 | 0.0000 | 0.6082 -> 0.5952 |
| language | chosen_only | 200 | 0.2716^*** | 0.000100 | 0.2716 | 0.6082 -> 0.5845 |
| language | rejected_only | 200 | -0.1410^ | 0.976702 | 0.0000 | 0.6082 -> 0.6185 |
| length | both | 200 | 0.0710^ | 0.160584 | 0.0000 | 0.6082 -> 0.5969 |
| length | chosen_only | 200 | -0.1546^ | 0.984602 | 0.0000 | 0.6082 -> 0.6274 |
| length | rejected_only | 200 | 0.2731^*** | 0.000300 | 0.2731 | 0.6082 -> 0.5744 |

## Category: `identity_trust`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.1958^ | 0.089091 | 0.0000 | 0.5919 -> 0.5588 |
| language | chosen_only | 50 | 0.1506^ | 0.157884 | 0.0000 | 0.5919 -> 0.5691 |
| language | rejected_only | 50 | 0.1078^ | 0.242476 | 0.0000 | 0.5919 -> 0.5809 |
| length | both | 50 | -0.0067^ | 0.521648 | 0.0000 | 0.5919 -> 0.5933 |
| length | chosen_only | 50 | -0.0414^ | 0.613239 | 0.0000 | 0.5919 -> 0.5993 |
| length | rejected_only | 50 | 0.0533^ | 0.384662 | 0.0000 | 0.5919 -> 0.5836 |

## Category: `interest_community`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | 0.4213^** | 0.002800 | 0.4213 | 0.6903 -> 0.6563 |
| language | chosen_only | 50 | 0.6201^*** | 0.000100 | 0.6201 | 0.6903 -> 0.6560 |
| language | rejected_only | 50 | -0.0053^ | 0.516648 | 0.0000 | 0.6903 -> 0.6905 |
| length | both | 50 | 0.0832^ | 0.281272 | 0.0000 | 0.6903 -> 0.6794 |
| length | chosen_only | 50 | -0.3578^ | 0.992201 | 0.0000 | 0.6903 -> 0.7212 |
| length | rejected_only | 50 | 0.4205^** | 0.001600 | 0.4205 | 0.6903 -> 0.6443 |

## Category: `platform_information_ecology`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.0593^ | 0.661934 | 0.0000 | 0.5407 -> 0.5441 |
| language | chosen_only | 50 | 0.3263^* | 0.014499 | 0.3263 | 0.5407 -> 0.5299 |
| language | rejected_only | 50 | -0.2658^ | 0.967003 | 0.0000 | 0.5407 -> 0.5549 |
| length | both | 50 | 0.0398^ | 0.395560 | 0.0000 | 0.5407 -> 0.5347 |
| length | chosen_only | 50 | -0.3150^ | 0.983502 | 0.0000 | 0.5407 -> 0.5754 |
| length | rejected_only | 50 | 0.3558^** | 0.009099 | 0.3558 | 0.5407 -> 0.5007 |

## Category: `safety_moderation`

| perturbation | variant | n | effect^sig | p_value | robustness_risk | confidence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| language | both | 50 | -0.1454^ | 0.847515 | 0.0000 | 0.6098 -> 0.6217 |
| language | chosen_only | 50 | 0.4860^*** | 0.000700 | 0.4860 | 0.6098 -> 0.5829 |
| language | rejected_only | 50 | -0.5895^ | 1.000000 | 0.0000 | 0.6098 -> 0.6476 |
| length | both | 50 | 0.2301^ | 0.063594 | 0.0000 | 0.6098 -> 0.5801 |
| length | chosen_only | 50 | -0.0410^ | 0.596540 | 0.0000 | 0.6098 -> 0.6137 |
| length | rejected_only | 50 | 0.3827^** | 0.004900 | 0.3827 | 0.6098 -> 0.5691 |
