# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/reranker_predictions/bge_reranker_v2_m3/base/skyjury_bench_base_similarity_reranker_ssd2_lbh_zjx_models_BAAI_bge-reranker-v2-m3_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 200 | paired_t | -0.0131^ | 0.572843 | 0.0000 | confidence 0.4644 -> 0.4681 |
| language | 200 | paired_t | 0.1386^ | 0.027097 | 0.0000 | confidence 0.4644 -> 0.4468 |

## Category: `identity_trust`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.2588^ | 0.037296 | 0.0000 | confidence 0.4810 -> 0.4669 |
| length | 50 | paired_t | -0.0173^ | 0.559844 | 0.0000 | confidence 0.4810 -> 0.4851 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.2075^ | 0.081292 | 0.0000 | confidence 0.5081 -> 0.4797 |
| length | 50 | paired_t | 0.0626^ | 0.329467 | 0.0000 | confidence 0.5081 -> 0.4920 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.2204^ | 0.063094 | 0.0000 | confidence 0.4114 -> 0.3899 |
| length | 50 | paired_t | -0.0931^ | 0.743626 | 0.0000 | confidence 0.4114 -> 0.4396 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 50 | paired_t | 0.0350^ | 0.408359 | 0.0000 | confidence 0.4572 -> 0.4508 |
| length | 50 | paired_t | 0.0053^ | 0.485451 | 0.0000 | confidence 0.4572 -> 0.4556 |
