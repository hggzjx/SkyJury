# SkyJury Data Schema

This document defines an executable data schema for collecting the Bluesky / AT Protocol data needed by the SkyJury proposal. The schema is organized around the core benchmark unit:

```text
post x target labeler x context package x companion labelers
```

The minimal collection pipeline is:

1. Build the Labeler Policy Bank.
2. Collect observed post-labeler-label records.
3. Reconstruct context packages around target posts.
4. Identify companion labelers.
5. Run human verification and adjudication.
6. Assign dual-axis difficulty labels.

## 1. `labelers`

Stores each public Labeler's basic identity, policy snapshot, and eligibility status.

| Field | Type | Description |
| --- | --- | --- |
| `labeler_id` | string | Internal primary key. |
| `did` | string | Labeler DID. |
| `handle` | string | Human-readable handle. |
| `service_endpoint` | string | Labeler service endpoint, if available. |
| `snapshot_time` | datetime | Time when the Labeler metadata was collected. |
| `is_active` | boolean | Whether the Labeler was reachable at collection time. |
| `supports_post_labels` | boolean | Whether the Labeler explicitly supports post/content labels. |
| `supports_account_labels` | boolean | Whether the Labeler also supports account labels. |
| `governance_type` | string | Main governance type, e.g. `scam`, `harassment`, `adult`, `misinfo`, `ai_disclosure`. |
| `secondary_types` | json | Optional additional governance types. |
| `policy_text` | text | Raw public policy text or declaration. |
| `policy_source_url` | string | Source URL for the policy text. |
| `policy_clarity_note` | text | Human note on clarity, ambiguity, and stability. |
| `annotation_eligible` | boolean | Whether this Labeler can enter the main benchmark candidate set. |
| `exclusion_reason` | text | Reason for exclusion, if not eligible. |

## 2. `labeler_values`

Stores each Labeler's label space and public definitions.

| Field | Type | Description |
| --- | --- | --- |
| `label_value_id` | string | Internal primary key. |
| `labeler_id` | string | Foreign key to `labelers`. |
| `label_value` | string | Raw label value. |
| `label_display_name` | string | Human-readable label name, if available. |
| `label_definition` | text | Public label definition. |
| `applies_to_post` | boolean | Whether this label applies to posts. |
| `applies_to_account` | boolean | Whether this label applies to accounts. |
| `severity_level` | string | Optional human category: `low`, `medium`, `high`. |
| `boundary_note` | text | Human note on boundary conditions. |
| `is_target_label_candidate` | boolean | Whether this label is suitable for the main experiment. |

## 3. `posts`

Stores target post objects.

| Field | Type | Description |
| --- | --- | --- |
| `post_id` | string | Internal primary key. |
| `post_uri` | string | AT URI of the post. |
| `post_cid` | string | CID of the post. |
| `author_did` | string | Author DID. |
| `author_handle` | string | Author handle. |
| `created_at` | datetime | Post creation time. |
| `text` | text | Post body. |
| `lang` | string | Language code, if available. |
| `has_external_link` | boolean | Whether the post contains an external link. |
| `has_image` | boolean | Whether the post contains an image. |
| `has_video` | boolean | Whether the post contains a video. |
| `reply_parent_uri` | string | Parent post URI, if this is a reply. |
| `quote_uri` | string | Quoted post URI, if any. |
| `thread_root_uri` | string | Root post URI of the thread. |
| `engagement_reply_count` | integer | Reply count at snapshot time. |
| `engagement_repost_count` | integer | Repost count at snapshot time. |
| `engagement_like_count` | integer | Like count at snapshot time. |
| `is_deleted_or_unavailable` | boolean | Whether the post was deleted or unavailable at collection time. |

## 4. `observed_labels`

Stores publicly observed `post-labeler-label` records.

| Field | Type | Description |
| --- | --- | --- |
| `observed_label_id` | string | Internal primary key. |
| `post_id` | string | Foreign key to `posts`. |
| `labeler_id` | string | Foreign key to `labelers`. |
| `label_value` | string | Observed label value. |
| `label_uri` | string | Label record URI, if available. |
| `labeled_at` | datetime | Label creation time, if available. |
| `source_snapshot_time` | datetime | Time when this observation was collected. |
| `is_positive_observation` | boolean | Whether this is used as a high-confidence positive signal. |
| `observation_confidence` | string | Observation confidence, e.g. `high`, `medium`, `low`. |
| `note` | text | Additional observation note. |

## 5. `context_packages`

Stores reconstructed context around each target post.

| Field | Type | Description |
| --- | --- | --- |
| `context_id` | string | Internal primary key. |
| `target_post_id` | string | Foreign key to `posts`. |
| `context_version` | string | Version identifier for this context package. |
| `parent_post_ids` | json | Parent post IDs included in the context. |
| `quote_post_ids` | json | Quoted post IDs included in the context. |
| `reply_post_ids` | json | Reply post IDs included in the context. |
| `linked_url_list` | json | External URLs appearing in the context. |
| `linked_url_summaries` | json | Brief descriptions or summaries of external URLs. |
| `author_background_note` | text | Minimal author background needed for moderation judgment. |
| `context_text_bundle` | text | Serialized context text used in model prompts. |
| `evidence_distribution_note` | text | Note on where evidence is located. |
| `has_noise` | boolean | Whether the context includes clear irrelevant or weakly relevant noise. |
| `requires_cross_turn_resolution` | boolean | Whether cross-turn or pronoun/context resolution is required. |
| `context_sufficiency_note` | text | Note on whether the context is sufficient for judgment. |
| `context_quality_status` | string | `usable`, `insufficient`, or `broken`. |

## 6. `sample_units`

Main benchmark table. Each row represents one evaluable `post x target_labeler` unit.

| Field | Type | Description |
| --- | --- | --- |
| `sample_id` | string | Internal primary key. |
| `post_id` | string | Foreign key to `posts`. |
| `context_id` | string | Foreign key to `context_packages`. |
| `target_labeler_id` | string | Target Labeler ID. |
| `target_label_value_gold` | string | Final gold label for the target Labeler. |
| `gold_source_type` | string | `observed_positive`, `human_adjudicated`, or `hybrid`. |
| `is_main_experiment_eligible` | boolean | Whether this unit enters the main experiment. |
| `eligibility_note` | text | Reason for inclusion or exclusion. |
| `context_difficulty` | string | `easy` or `hard`. |
| `policy_difficulty` | string | `easy` or `hard`. |
| `difficulty_cell` | string | `EE`, `HE`, `EH`, or `HH`. |
| `boundary_case_flag` | boolean | Whether this is a policy boundary case. |
| `multi_risk_flag` | boolean | Whether multiple governance risks are present. |
| `high_disagreement_flag` | boolean | Whether annotators strongly disagreed. |
| `final_review_status` | string | `approved`, `rejected`, or `exploratory`. |

## 7. `companion_labelers`

Stores companion Labelers associated with each sample unit. This table is central for constructing multi-Labeler policy conditions.

| Field | Type | Description |
| --- | --- | --- |
| `companion_id` | string | Internal primary key. |
| `sample_id` | string | Foreign key to `sample_units`. |
| `companion_labeler_id` | string | Foreign key to `labelers`. |
| `companion_gold_label` | string | Final gold label for this companion Labeler on the same post. |
| `is_actively_relevant` | boolean | Whether this companion Labeler is genuinely relevant to the post. |
| `is_inactive_control` | boolean | Whether this companion is used as an inactive control. |
| `relevance_strength` | string | `weak`, `medium`, or `strong`. |
| `rubric_overlap_with_target` | string | `low`, `medium`, or `high`. |
| `interference_risk_note` | text | Note on possible target-rule confusion. |
| `used_in_policy_stack` | boolean | Whether this companion is included in the formal prompt condition. |

## 8. `annotations`

Stores individual human annotation records.

| Field | Type | Description |
| --- | --- | --- |
| `annotation_id` | string | Internal primary key. |
| `sample_id` | string | Foreign key to `sample_units`. |
| `annotator_id` | string | Annotator identifier. |
| `target_label_decision` | string | Annotator's target Labeler decision. |
| `target_rule_triggered` | boolean | Whether the target rule is triggered. |
| `companion_decisions` | json | Annotator decisions for companion Labelers. |
| `context_difficulty_vote` | string | `easy` or `hard`. |
| `policy_difficulty_vote` | string | `easy` or `hard`. |
| `confidence` | string | Annotator confidence, e.g. `low`, `medium`, `high`. |
| `evidence_note` | text | Evidence cited by the annotator. |
| `ambiguity_note` | text | Ambiguity or boundary concerns. |
| `submitted_at` | datetime | Annotation submission time. |

## 9. `adjudications`

Stores final adjudicated labels and difficulty assignments.

| Field | Type | Description |
| --- | --- | --- |
| `adjudication_id` | string | Internal primary key. |
| `sample_id` | string | Foreign key to `sample_units`. |
| `final_target_label` | string | Final target Labeler gold label. |
| `final_companion_map` | json | Final companion Labeler labels and relevance decisions. |
| `final_context_difficulty` | string | Final `easy` or `hard` context difficulty. |
| `final_policy_difficulty` | string | Final `easy` or `hard` policy difficulty. |
| `final_difficulty_cell` | string | Final `EE`, `HE`, `EH`, or `HH` cell. |
| `adjudicator_id` | string | Adjudicator identifier. |
| `adjudication_note` | text | Final explanation or adjudication note. |
| `resolved_at` | datetime | Adjudication time. |

## Minimal Implementation Order

For the first pilot, implement the tables in this order:

1. `labelers`
2. `labeler_values`
3. `posts`
4. `observed_labels`
5. `context_packages`
6. `sample_units`
7. `companion_labelers`
8. `annotations`
9. `adjudications`

The first four tables are enough to verify whether Bluesky API access can support the basic Policy Bank and observed-label collection. The remaining tables are needed once context reconstruction and human verification begin.
