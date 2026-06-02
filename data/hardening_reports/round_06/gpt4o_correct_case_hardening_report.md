# GPT-4o Correct-Case Hardening Report

## Run Summary

```text
predictions: /ssd1/lbh/zjx/skyjury/verifier/results/gpt4o_hardening_loop/round_06/verifier_pilot_rmbench_llm_judge_gpt-4o-ca_predictions.json
dataset: /ssd1/lbh/zjx/skyjury/data/verifier_pilot_rmbench.json
proposal: /ssd1/lbh/zjx/skyjury/proposal_reward_model_labeler_preference.md
samples: 576
correct: 311
wrong_or_tie: 265
accuracy: 0.5399
target_accuracy: 0.55-0.60
recommended_direction: small_local_edits_only
hardening_queue: 304
calibration_queue: 265
```

## Direction Guidance

Current accuracy is near the acceptable hard range. Make only small local edits.

## Leakage Diagnostics

```text
correct: strong_target_any=213/311 (68.5%), third_post_strong=116/311 (37.3%)
wrong_or_tie: strong_target_any=151/265 (57.0%), third_post_strong=85/265 (32.1%)
```

## Highest-Accuracy Subsets

```text
medical_community: 4/4 = 1.000
promotion_filtering: 4/4 = 1.000
sports_authenticity: 4/4 = 1.000
protocol_infrastructure: 16/20 = 0.800
account_verification: 9/12 = 0.750
account_behavior: 3/4 = 0.750
fandom_spoiler: 3/4 = 0.750
urbanism_community: 3/4 = 0.750
crypto_safety: 14/20 = 0.700
accessibility: 26/40 = 0.650
fact_checking: 13/20 = 0.650
developer_identity: 5/8 = 0.625
news_source_context: 17/28 = 0.607
adult_creator_discovery: 12/20 = 0.600
art_safety: 12/20 = 0.600
science_misinformation: 12/20 = 0.600
spam_behavior: 9/16 = 0.562
fandom_identity: 11/20 = 0.550
politics_filtering: 24/44 = 0.545
community_identity: 17/32 = 0.531
ai_content: 20/40 = 0.500
employment: 8/16 = 0.500
gaming_industry: 8/16 = 0.500
substack_filtering: 2/4 = 0.500
verification: 15/32 = 0.469
adult_filtering: 9/20 = 0.450
fandom_content_warnings: 8/20 = 0.400
music_creator: 6/16 = 0.375
sports_fandom: 11/40 = 0.275
creator_discovery: 6/24 = 0.250
crypto_spam: 0/4 = 0.000
```

## Top Hardening Queue Items

- pref_0001 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0002 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0003 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Flags announcements falsely claiming partnerships or endorsements to gain credibility and attract investments.
- pref_0004 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0010 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0013 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0014 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0015 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Accounts that frequently or un-apologetically post AI images.
- pref_0016 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0017 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0018 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: `VTuber` is also common in replies, but is less often the reason a post is saved for review: VTubers are content creators of various mediums using 2D/3D/PNG! This one is specifically for those who consider themselves VTubers, but are not attached to a platform like YouTube for proper differentiation.
- pref_0019 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Accounts that regularly plagiarize works, and pass other's works off as their own.
- pref_0020 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0025 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0026 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0027 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This creator is a featured model on Babesky.
- pref_0028 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0029 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0033 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0034 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0035 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This user works in the field of Science Journalism
- pref_0036 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0038 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0039 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This label is given to facts that are not possible to fact-check due to the unavailability of information.To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0040 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0041 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0042 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0043 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Media posted without any alt text provided.
- pref_0044 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0046 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0047 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Vanity label for curated content related to Star Wars
- pref_0048 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0053 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0054 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0055 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Content referencing unfounded claims that Ivermectin is an effective treatment against COVID-19 infections. Ivermectin is an antiparasitic drug used in humans to treat head lice, scabies, strongyloidiasis, and numerous...
- pref_0056 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0059 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Observer Media Group, Inc. (OMG) is a media company that publishes local newspapers and magazines in the U.S. state of Florida. The company publishes seven newspapers, nine quarterly magazines and maintains four news we...
- pref_0061 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0063 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: link is hosted on substack
- pref_0065 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Partial Alt Text`: This post contains multiple still images and only some of them have usable alt text.
- pref_0066 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: `Image lacks ALT` is also common in replies, but is less often the reason a post is saved for review: The post contains an image, but the image does not contain an ALT text.
- pref_0067 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This post contains multiple still images and only some of them have usable alt text.
- pref_0068 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Another visible cluster describes `Image lacks ALT`, but those cases are usually handled without follow-up: The post contains an image, but the image does not contain an ALT text.
- pref_0071 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Nim is a statically typed compiled systems programming language. It combines successful concepts from mature languages like Python, Ada and Modula.
- pref_0072 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0073 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0074 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0076 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0077 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0078 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0079 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Account is hosted by a smaller independent PDS
- pref_0080 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0081 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0087 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: User is a fan of the Arizona Cardinals
- pref_0089 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Fake NHL Account`: An NHL account that is not authenticated, and is otherwise name squatting, impersonating the team, or otherwise not officially the team the account claims to represent.
- pref_0090 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0091 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: A mirror of the X/Twitter feed of an NHL team posted to Bluesky using a bot.
- pref_0092 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0093 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `⚠️ Choose Not To Use Archive Warnings`: This user marked themselves as Choosing Not To Use Archive Warnings (for funsies!)
- pref_0094 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0095 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This user marked themselves as No Archive Warnings Apply (for funsies!)
- pref_0096 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0097 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Chill Larrie 🌶`: Just here to have fun, no drama
- pref_0098 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0099 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Im a beta reader!
- pref_0101 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0103 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This user is not taking commissions at this time.
- pref_0105 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0106 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0107 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Individual is verified as a notable Director.
- pref_0108 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0112 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0114 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0115 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Account verified to be a Canadian journalist from a recognized Canadian journalism platform.
- pref_0116 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0119 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=prompt_contains_direct_target_wording,third_recent_post_contains_target_wording
  third_post: Only a few saved reports include this narrower pattern: A reply to a post that contains a likely political article.
- pref_0120 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0121 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0122 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0123 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: An account that primarily or very frequently discusses politics in the United States of America.

## Top Calibration Queue Items

- pref_0005 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Automated cryptoposting`: Likely automated cryptocurrency-related posting
- pref_0006 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Rug Pull Alert` is also common in replies, but is less often the reason a post is saved for review: Identifies projects that show signs of being abandoned after collecting funds, with founders disappearing or ceasing development.
- pref_0007 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Cryptocurrency spam and marketing
- pref_0008 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Rug Pull Alert`, but those cases are usually handled without follow-up: Identifies projects that show signs of being abandoned after collecting funds, with founders disappearing or ceasing development.
- pref_0009 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=gpt4o_ties_candidates
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `AI Audio Poster`: Accounts that frequently or un-apologetically post AI Audio, such as AI generated voices or instrumentals.
- pref_0011 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Individual that indirectly contain AI generated elements, such as when traced over by a human
- pref_0012 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `AI Slur User`, but those cases are usually handled without follow-up: Uses slurs for AI in earnest (i.e., not mention or mockery of the concept) or defends doing so.
- pref_0021 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `3D Artist`: 3D Artists are content creators who specialize in 3D graphics! From character, environmental, vehicular, etc!
- pref_0022 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Plagiarism Accounts` is also common in replies, but is less often the reason a post is saved for review: Accounts that regularly plagiarize works, and pass other's works off as their own.
- pref_0023 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Video Editors and VFX Artists are content creators that have assisted others or themselves to create edited or add visual effects to video content in various and ways!
- pref_0024 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Reposted Without Permission/Credit`, but those cases are usually handled without follow-up: Reposts/reuploads that were made against the original artist's wishes, often without attribution
- pref_0030 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_ties_candidates
  third_post: `SextPanther` is also common in replies, but is less often the reason a post is saved for review: Indicates this user is a SextPanther creator.
- pref_0031 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: Art with explicit or suggestive sexual themes, including provocative imagery or partial nudity.
- pref_0032 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Tryst`, but those cases are usually handled without follow-up: Indicates this user is a Tryst creator.
- pref_0037 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `False Fact`: This label is given to facts that are deemed to be false. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0045 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=gpt4o_ties_candidates
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `❕Rumors in Replies❕`: Possible rumor spoilers have been found in the replies
- pref_0049 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `US Politics`: Posts about US Politics
- pref_0050 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `True Fact` is also common in replies, but is less often the reason a post is saved for review: This label is given to facts that are deemed to be true. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0051 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Posts about US Politics
- pref_0052 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Satire`, but those cases are usually handled without follow-up: This label is given to satiric posts. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0057 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `U.S. News & World Report`: U.S. News & World Report (USNWR, U.S. NEWS) is an American media company publishing news, consumer advice, rankings, and analysis. The company was launched in 1948 as the merger of domestic-focused weekly newspaper U.S....
- pref_0058 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `True Fact` is also common in replies, but is less often the reason a post is saved for review: This label is given to facts that are deemed to be true. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0060 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Satire`, but those cases are usually handled without follow-up: This label is given to satiric posts. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0062 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Promoted` is also common in replies, but is less often the reason a post is saved for review: This is a paid promotion for visibility.
- pref_0064 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Promoted`, but those cases are usually handled without follow-up: This is a paid promotion for visibility.
- pref_0069 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Python`: Python is a high-level, versatile programming language known for its easy readability and vast ecosystem, used in web development, data science, automation, and more.
- pref_0070 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: `zephyrproject-rtos/zephyr` is also common in replies, but is less often the reason a post is saved for review: Primary Git Repository for the Zephyr Project. Zephyr is a new generation, scalable, optimized, secure RTOS for multiple hardware architectures. https://github.com/zephyrproject-rtos/zephyr
- pref_0075 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: 📓 Storybook for React Native! https://github.com/storybookjs/react-native
- pref_0082 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=gpt4o_ties_candidates
  third_post: `Brooklyn` is also common in replies, but is less often the reason a post is saved for review: Fan of Brooklyn sports teams
- pref_0083 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: A Fan of the Chicago White Sox
- pref_0084 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `Baltimore`, but those cases are usually handled without follow-up: Fan of Baltimore sports teams
- pref_0085 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Kansas City Chiefs`: User is a fan of the Kansas City Chiefs
- pref_0086 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_ties_candidates
  third_post: `Kansas City Royals` is also common in replies, but is less often the reason a post is saved for review: A Fan of the Kansas City Royals
- pref_0088 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `Boston Red Sox`, but those cases are usually handled without follow-up: A Fan of the Boston Red Sox
- pref_0100 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `⚠️ Graphic Depictions of Violence`, but those cases are usually handled without follow-up: This user marked themselves as Graphic Depictions of Violence (for funsies!)
- pref_0102 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: `Animator` is also common in replies, but is less often the reason a post is saved for review: Artists who work in any medium of animation, whether 2d, 3d, digital, or traditional
- pref_0104 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `people who do perform with their voice`, but those cases are usually handled without follow-up: i messed this one up
- pref_0109 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_ties_candidates
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Verified Human`: An account with this label is a verified human. The person that owns the account proved they are human by supplying their passport and we have verified that no other account with this passport exists.
- pref_0110 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `🏛 Government` is also common in replies, but is less often the reason a post is saved for review: Account connected to a government, a government office, or a politician.
- pref_0111 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: An account with this label is a verified human. The person that owns the account proved they are human by supplying their passport and we have verified that no other account with this passport exists.
- pref_0117 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Politcal News Link Reply`: A reply to a post that contains a likely political article.
- pref_0118 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `US Political News Source` is also common in replies, but is less often the reason a post is saved for review: A news source or journalist that primarily or frequently covers politics in the United States of America.
- pref_0125 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Arts & Culture`: Content is in category "arts & culture". This label has been generated via machine learning and may not be accurate.
- pref_0126 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `True Fact` is also common in replies, but is less often the reason a post is saved for review: This label is given to facts that are deemed to be true. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0128 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Satire`, but those cases are usually handled without follow-up: This label is given to satiric posts. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0137 [account_behavior] chosen=stechlab-labels.bsky.social rejected=moderation.bsky.app reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `No break greater than 2 hrs yesterday`: This account has posted without meaningful breaks in the last 24 hours, with no gap between posts that was longer than 2 hours. This behavior may be consistent with an organization account, a bot, accounts with multiple...
- pref_0143 [urbanism_community] chosen=labeler.urbanism.plus rejected=labeler.bikesky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: A rider of an acoustic bike, e-bike, or trike.
- pref_0147 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: Media posted without any alt text provided.
- pref_0151 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: Media posted without any alt text provided.
- pref_0153 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Partial Alt Text`: This post contains multiple still images and only some of them have usable alt text.
- pref_0156 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Misused Alt Text`, but those cases are usually handled without follow-up: Media posted with alt text describing it in a way that can't be understood without access to the media, such as captions that assume the reader can see the image.
- pref_0157 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Partial Alt Text`: This post contains multiple still images and only some of them have usable alt text.
- pref_0160 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Misused Alt Text`, but those cases are usually handled without follow-up: Media posted with alt text describing it in a way that can't be understood without access to the media, such as captions that assume the reader can see the image.
- pref_0169 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Image lacks ALT`: The post contains an image, but the image does not contain an ALT text.
- pref_0170 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Missing Alt Text` is also common in replies, but is less often the reason a post is saved for review: This post contains one or more still images and none of them has usable alt text.
- pref_0171 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: The post contains an image, but the image does not contain an ALT text.
- pref_0172 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Partial Alt Text`, but those cases are usually handled without follow-up: This post contains multiple still images and only some of them have usable alt text.
- pref_0173 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Image lacks ALT`: The post contains an image, but the image does not contain an ALT text.
- pref_0174 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Missing Alt Text` is also common in replies, but is less often the reason a post is saved for review: This post contains one or more still images and none of them has usable alt text.
- pref_0175 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: The post contains an image, but the image does not contain an ALT text.
- pref_0176 [accessibility] chosen=noalt.danirod.es rejected=alt-text-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Partial Alt Text`, but those cases are usually handled without follow-up: This post contains multiple still images and only some of them have usable alt text.
- pref_0185 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `AI / Machine Learning 🤖`: Works primarily in artificial intelligence or ML
- pref_0186 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Science Communication` is also common in replies, but is less often the reason a post is saved for review: This user works in the field of Science Communication
- pref_0187 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Works in biological or life sciences
- pref_0188 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Forensic Science`, but those cases are usually handled without follow-up: This user works in the field of Forensic Science
- pref_0189 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `AI / Machine Learning 🤖`: Works primarily in artificial intelligence or ML
- pref_0190 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: `Science Communication` is also common in replies, but is less often the reason a post is saved for review: This user works in the field of Science Communication
- pref_0191 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Works in biological or life sciences
- pref_0192 [science_misinformation] chosen=zktls-verifier-v0.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `Forensic Science`, but those cases are usually handled without follow-up: This user works in the field of Forensic Science
- pref_0196 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `Likely AI Account`, but those cases are usually handled without follow-up: This Account is likely posting AI generated content.
- pref_0200 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `Likely AI Account`, but those cases are usually handled without follow-up: This Account is likely posting AI generated content.
- pref_0201 [ai_content] chosen=ai-labeler.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Likely AI Account`: This Account is likely posting AI generated content.
- pref_0203 [ai_content] chosen=ai-labeler.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: This Account is likely posting AI generated content.
- pref_0204 [ai_content] chosen=ai-labeler.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `AI Imagery Post`, but those cases are usually handled without follow-up: Individual posts containing AI Imagery.
- pref_0205 [ai_content] chosen=ai-labeler.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Likely AI Account`: This Account is likely posting AI generated content.
- pref_0207 [ai_content] chosen=ai-labeler.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: This Account is likely posting AI generated content.
- pref_0208 [ai_content] chosen=ai-labeler.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: Another visible cluster describes `AI Imagery Post`, but those cases are usually handled without follow-up: Individual posts containing AI Imagery.
- pref_0209 [ai_content] chosen=antiantiai.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Problem Not Otherwise Specified`: Catch-all for serious problem users who are maybe not problems for AI-related reasons.
- pref_0212 [ai_content] chosen=antiantiai.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Another visible cluster describes `LLM Text Poster`, but those cases are usually handled without follow-up: Accounts that frequently or un-apologetically post LLM generated posts, articles, or other texts containing LLM generated content
- pref_0213 [ai_content] chosen=antiantiai.bsky.social rejected=labeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Saved-review notes that later become moderation decisions repeatedly use this narrower boundary: `Problem Not Otherwise Specified`: Catch-all for serious problem users who are maybe not problems for AI-related reasons.

## Required Rewrite Direction

- Make rejected evidence more visible, frequent, and early.
- Hide chosen advantage in one or two low-salience details.
- Remove direct target wording from user-facing prompt fields.
- Replace broad rejected labelers with same-domain near misses when possible.
- If the rewritten profile truly favors rejected, flip chosen/rejected and update annotations.
