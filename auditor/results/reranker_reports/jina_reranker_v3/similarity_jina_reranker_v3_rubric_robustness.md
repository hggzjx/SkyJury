# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/reranker_predictions/jina_reranker_v3/base/skyjury_bench_base_similarity_reranker_ssd2_lbh_zjx_models_jinaai_jina-reranker-v3_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | 0.2900^*** | 0.000100 | 0.2900 | confidence 0.5096 -> 0.5013 |
| language | 200 | paired_t | 0.0989^ | 0.081492 | 0.0000 | confidence 0.5096 -> 0.5087 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.2555^ | 0.042996 | 0.0000 | confidence 0.5134 -> 0.5109 |
| length | 50 | paired_t | 0.4656^*** | 0.000700 | 0.4656 | confidence 0.5134 -> 0.4987 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0022^ | 0.489951 | 0.0000 | confidence 0.5085 -> 0.5084 |
| length | 50 | paired_t | 0.3546^** | 0.007199 | 0.3546 | confidence 0.5085 -> 0.5000 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.1717^ | 0.119188 | 0.0000 | confidence 0.5086 -> 0.5069 |
| length | 50 | paired_t | 0.2697^ | 0.032597 | 0.0000 | confidence 0.5086 -> 0.4994 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | -0.0264^ | 0.577142 | 0.0000 | confidence 0.5082 -> 0.5084 |
| length | 50 | paired_t | 0.0504^ | 0.372463 | 0.0000 | confidence 0.5082 -> 0.5070 |
