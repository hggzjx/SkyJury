# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/verifier/results/similarity_smoke/base/skyjury_bench_base_similarity_tfidf_tfidf_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 8 | paired_t | 0.7058^ | 0.059406 | 0.0000 | confidence 0.5491 -> 0.5283 |
| language | 8 | paired_t | 0.8951^ | 0.069307 | 0.0000 | confidence 0.5491 -> 0.5220 |

## Category: `interest_community`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 1 | paired_t | 0.0000^** | 0.009901 | 0.0000 | confidence 0.5770 -> 0.5102 |
| length | 1 | paired_t | 0.0000^** | 0.009901 | 0.0000 | confidence 0.5770 -> 0.5260 |

## Category: `platform_information_ecology`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 3 | paired_t | 3.1934^ | 0.138614 | 0.0000 | confidence 0.5460 -> 0.5088 |
| length | 3 | paired_t | 0.6055^ | 0.396040 | 0.0000 | confidence 0.5460 -> 0.5414 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 4 | paired_t | 0.3112^ | 0.267327 | 0.0000 | confidence 0.5444 -> 0.5348 |
| length | 4 | paired_t | 0.7188^ | 0.237624 | 0.0000 | confidence 0.5444 -> 0.5191 |
