# SkyJury Auditor Robustness Risk Report

- method: `similarity`
- original_predictions: `/ssd1/lbh/zjx/skyjury/auditor/results/similarity_wrapper_smoke/tfidf/base/skyjury_bench_base_similarity_tfidf_tfidf_predictions.json`
- audited_cases: `verifier-success subset`
- multiple-testing control: Benjamini-Hochberg (BH)

## Overall

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| length | 2 | paired_t | 0.9775^ | 0.503150 | 0.0000 | confidence 0.5552 -> 0.5162 |
| language | 2 | paired_t | 1.1510^ | 0.253275 | 0.0000 | confidence 0.5552 -> 0.5310 |

## Category: `safety_moderation`

| perturbation | n | statistic | effect^sig | p_value | robustness_risk | summary |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| language | 2 | paired_t | 1.1510^ | 0.243676 | 0.0000 | confidence 0.5552 -> 0.5310 |
| length | 2 | paired_t | 0.9775^ | 0.493851 | 0.0000 | confidence 0.5552 -> 0.5162 |
