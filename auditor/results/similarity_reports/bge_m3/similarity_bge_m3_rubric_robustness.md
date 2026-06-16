# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/similarity_predictions/bge_m3/base/skyjury_bench_base_similarity_sbert_ssd2_lbh_zjx_models_BAAI_bge-m3_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.0002^ | 0.504550 | 0.0000 | confidence 0.5011 -> 0.5011 |
| language | 200 | paired_t | 0.1521^ | 0.016898 | 0.0000 | confidence 0.5011 -> 0.5005 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.3142^ | 0.014799 | 0.0000 | confidence 0.5038 -> 0.5027 |
| length | 50 | paired_t | -0.1155^ | 0.790221 | 0.0000 | confidence 0.5038 -> 0.5050 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.2289^ | 0.058594 | 0.0000 | confidence 0.5020 -> 0.5010 |
| length | 50 | paired_t | 0.1761^ | 0.106089 | 0.0000 | confidence 0.5020 -> 0.5003 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.1143^ | 0.784122 | 0.0000 | confidence 0.4970 -> 0.4973 |
| length | 50 | paired_t | -0.1126^ | 0.784822 | 0.0000 | confidence 0.4970 -> 0.4976 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1115^ | 0.216978 | 0.0000 | confidence 0.5014 -> 0.5012 |
| length | 50 | paired_t | 0.0145^ | 0.461954 | 0.0000 | confidence 0.5014 -> 0.5013 |
