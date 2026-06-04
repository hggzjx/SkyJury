# GPT-4o Correct-Case Hardening Report

## Run Summary

```text
predictions: /ssd1/lbh/zjx/skyjury/verifier/results/gpt4o_hardening_loop/round_03/skyjury_bench_llm_judge_gpt-4o-ca_predictions.json
dataset: /ssd1/lbh/zjx/skyjury/data/skyjury_bench.json
proposal: /ssd1/lbh/zjx/skyjury/proposal_reward_model_labeler_preference.md
samples: 576
correct: 234
wrong_or_tie: 342
accuracy: 0.4062
target_accuracy: 0.55-0.60
recommended_direction: calibrate
hardening_queue: 226
calibration_queue: 342
```

## Direction Guidance

Current accuracy is below target. Calibrate GPT-4o-wrong/tie cases instead of further hardening.
Keep rejected visible, but increase chosen behavioral priority through saves, reports, follow-up, or high-consequence cases.

## Leakage Diagnostics

```text
correct: strong_target_any=167/234 (71.4%), third_post_strong=99/234 (42.3%)
wrong_or_tie: strong_target_any=197/342 (57.6%), third_post_strong=99/342 (28.9%)
```

## Highest-Accuracy Subsets

```text
medical_community: 4/4 = 1.000
promotion_filtering: 4/4 = 1.000
sports_authenticity: 4/4 = 1.000
adult_creator_discovery: 12/20 = 0.600
art_safety: 12/20 = 0.600
account_verification: 7/12 = 0.583
accessibility: 21/40 = 0.525
news_source_context: 14/28 = 0.500
protocol_infrastructure: 10/20 = 0.500
employment: 8/16 = 0.500
fandom_spoiler: 2/4 = 0.500
urbanism_community: 2/4 = 0.500
politics_filtering: 21/44 = 0.477
fandom_identity: 9/20 = 0.450
science_misinformation: 9/20 = 0.450
gaming_industry: 7/16 = 0.438
crypto_safety: 8/20 = 0.400
verification: 12/32 = 0.375
music_creator: 6/16 = 0.375
fact_checking: 7/20 = 0.350
fandom_content_warnings: 7/20 = 0.350
creator_discovery: 8/24 = 0.333
ai_content: 12/40 = 0.300
adult_filtering: 6/20 = 0.300
spam_behavior: 4/16 = 0.250
developer_identity: 2/8 = 0.250
account_behavior: 1/4 = 0.250
substack_filtering: 1/4 = 0.250
sports_fandom: 8/40 = 0.200
community_identity: 6/32 = 0.188
crypto_spam: 0/4 = 0.000
```

## Top Hardening Queue Items

- pref_0001 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0002 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0003 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Flags announcements falsely claiming partnerships or endorsements to gain credibility and attract investments.
- pref_0004 [crypto_safety] chosen=cryptolabeler.sats4.life rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0009 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0013 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0015 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Accounts that frequently or un-apologetically post AI images.
- pref_0016 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0017 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0018 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0019 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Accounts that regularly plagiarize works, and pass other's works off as their own.
- pref_0020 [art_safety] chosen=arttheft.bsky.social rejected=creatorlabeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0025 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0026 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0027 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This creator is a featured model on Babesky.
- pref_0028 [adult_creator_discovery] chosen=verified.babesky.com rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0033 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0036 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0038 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0039 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This label is given to facts that are not possible to fact-check due to the unavailability of information.To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0040 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0041 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0043 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Media posted without any alt text provided.
- pref_0044 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0047 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Vanity label for curated content related to Star Wars
- pref_0048 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0053 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0054 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: A smaller set of bookmarked follow-ups mentions `⚠ Misinfo: Vaccines do not cause autism` in this form: Content referencing a fraudulent research study that falsely claimed causative links between the Measles-Mumps-Rubella vaccine and the development of autism in children. This study was retracted after concerns arose reg...
- pref_0055 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Content referencing unfounded claims that Ivermectin is an effective treatment against COVID-19 infections. Ivermectin is an antiparasitic drug used in humans to treat head lice, scabies, strongyloidiasis, and numerous...
- pref_0056 [medical_community] chosen=moderation.medsky.network rejected=moderation.beehivesafety.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0059 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Observer Media Group, Inc. (OMG) is a media company that publishes local newspapers and magazines in the U.S. state of Florida. The company publishes seven newspapers, nine quarterly magazines and maintains four news we...
- pref_0063 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: link is hosted on substack
- pref_0065 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This post contains multiple still images and only some of them have usable alt text.
- pref_0066 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0067 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This post contains multiple still images and only some of them have usable alt text.
- pref_0068 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0071 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Nim is a statically typed compiled systems programming language. It combines successful concepts from mature languages like Python, Ada and Modula.
- pref_0073 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0077 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0079 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Account is hosted by a smaller independent PDS
- pref_0081 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0089 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: An NHL account that is not authenticated, and is otherwise name squatting, impersonating the team, or otherwise not officially the team the account claims to represent.
- pref_0090 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0091 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: A mirror of the X/Twitter feed of an NHL team posted to Bluesky using a bot.
- pref_0092 [sports_authenticity] chosen=nhllabeler.bsky.social rejected=sports-labeler.hooray.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0093 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This user marked themselves as Choosing Not To Use Archive Warnings (for funsies!)
- pref_0095 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This user marked themselves as No Archive Warnings Apply (for funsies!)
- pref_0096 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0099 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Im a beta reader!
- pref_0103 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This user is not taking commissions at this time.
- pref_0105 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0107 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Individual is verified as a notable Director.
- pref_0108 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0113 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0114 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0115 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Account verified to be a Canadian journalist from a recognized Canadian journalism platform.
- pref_0116 [account_verification] chosen=trustcollective.org rejected=label.onlyhumanhub.com reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0119 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=prompt_contains_direct_target_wording,third_recent_post_contains_target_wording
  third_post: Only a few saved reports include this narrower pattern: A reply to a post that contains a likely political article.
- pref_0121 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0122 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0123 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: An account that primarily or very frequently discusses politics in the United States of America.
- pref_0124 [politics_filtering] chosen=pol.conmodsys.net rejected=no-pol-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0127 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: Content is in category "environmental reporting". This label has been generated via machine learning and may not be accurate.
- pref_0129 [news_source_context] chosen=no-opinions.bsky.social rejected=news.aendra.dev reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0131 [news_source_context] chosen=no-opinions.bsky.social rejected=news.aendra.dev reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: An opinion article from a major news source.
- pref_0132 [news_source_context] chosen=no-opinions.bsky.social rejected=news.aendra.dev reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0133 [promotion_filtering] chosen=adcontrols.bsky.social rejected=onlyfilters.dev reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0135 [promotion_filtering] chosen=adcontrols.bsky.social rejected=onlyfilters.dev reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This post is part of a paid partnership.
- pref_0136 [promotion_filtering] chosen=adcontrols.bsky.social rejected=onlyfilters.dev reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0139 [account_behavior] chosen=stechlab-labels.bsky.social rejected=moderation.bsky.app reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This account made profile metadata changes on at least three days in the last 30 days. These changes may be small; but most accounts do not make frequent such changes.
- pref_0141 [urbanism_community] chosen=labeler.urbanism.plus rejected=labeler.bikesky.social reasons=normal_and_swapped_both_correct,gpt4o_margin_is_maximal
- pref_0143 [urbanism_community] chosen=labeler.urbanism.plus rejected=labeler.bikesky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: A rider of an acoustic bike, e-bike, or trike.
- pref_0145 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0148 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0149 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0152 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal
- pref_0155 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This post contains multiple still images and only some of them have usable alt text.
- pref_0159 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Only a few saved reports include this narrower pattern: This post contains multiple still images and only some of them have usable alt text.
- pref_0161 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,third_recent_post_contains_target_wording,gpt4o_margin_is_maximal
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This post contains multiple still images and only some of them have usable alt text.
- pref_0162 [accessibility] chosen=alt-text-labeler.bsky.social rejected=noalt.danirod.es reasons=normal_and_swapped_both_correct,prompt_contains_direct_target_wording,gpt4o_margin_is_maximal

## Top Calibration Queue Items

- pref_0005 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Likely automated cryptocurrency-related posting
- pref_0006 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Crypto boosterism` in this form: Cryptocurrency shilling that isn't outright spam
- pref_0007 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Cryptocurrency spam and marketing
- pref_0008 [crypto_spam] chosen=cryptolabeler.w3igg.com rejected=cryptolabeler.sats4.life reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Likely automated cryptocurrency-related posting
- pref_0010 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Indirect AI Imagery Poster` in this form: Accounts that are known to post works that indirectly use AI imagery, such as tracing over them.
- pref_0011 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Individual that indirectly contain AI generated elements, such as when traced over by a human
- pref_0012 [ai_content] chosen=labeler.blackwall.gg rejected=antiantiai.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Accounts that regularly post promotional material for generative AI products
- pref_0014 [ai_content] chosen=labeler.blackwall.gg rejected=ai-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `AI Imagery Post` in this form: Individual that indirectly contain AI generated elements, such as when traced over by a human
- pref_0021 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: 3D Artists are content creators who specialize in 3D graphics! From character, environmental, vehicular, etc!
- pref_0022 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `VTuber` in this form: VTubers are content creators of various mediums using 2D/3D/PNG! This one is specifically for those who consider themselves VTubers, but are not attached to a platform like YouTube for proper differentiation.
- pref_0023 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Video Editors and VFX Artists are content creators that have assisted others or themselves to create edited or add visual effects to video content in various and ways!
- pref_0024 [creator_discovery] chosen=creatorlabeler.bsky.social rejected=arttheft.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Cosplayers are content creators who dress up as characters from television, film, video games, or anime!
- pref_0029 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Art with explicit or suggestive sexual themes, including provocative imagery or partial nudity.
- pref_0030 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Sexually Suggestive (Cartoon)` in this form: Art with explicit or suggestive sexual themes, including provocative imagery or partial nudity.
- pref_0031 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: Art with explicit or suggestive sexual themes, including provocative imagery or partial nudity.
- pref_0032 [adult_filtering] chosen=moderation.bsky.app rejected=verified.babesky.com reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Art with explicit or suggestive sexual themes, including provocative imagery or partial nudity.
- pref_0034 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Science Communication` in this form: This user works in the field of Science Communication
- pref_0035 [science_misinformation] chosen=stemlabels.xyz rejected=moderation.beehivesafety.com reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: This user works in the field of Science Journalism
- pref_0037 [fact_checking] chosen=newsdetective.bsky.social rejected=stemlabels.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This label is given to facts that are deemed to be false. To see why this post was labeled this way (or to disagree) go to newsdetective.org.
- pref_0042 [accessibility] chosen=baatl.mastod.one rejected=moderation.bsky.app reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Meaningless Alt Text` in this form: Media posted with alt text that conveys effectively nothing at all (such as just the words "alt text").
- pref_0045 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Possible rumor spoilers have been found in the replies
- pref_0046 [fandom_spoiler] chosen=mod.shawn.party rejected=moderation.bsky.app reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `❕Spoilers in Replies❕` in this form: Possible spoilers have been found in the replies
- pref_0049 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Posts about US Politics
- pref_0050 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `US Politics` in this form: Posts about US Politics
- pref_0051 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: Posts about US Politics
- pref_0052 [politics_filtering] chosen=uspol-labeler.bsky.social rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Posts about US Politics
- pref_0057 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: U.S. News & World Report (USNWR, U.S. NEWS) is an American media company publishing news, consumer advice, rankings, and analysis. The company was launched in 1948 as the merger of domestic-focused weekly newspaper U.S....
- pref_0058 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Boston Globe Media Partners` in this form: Boston Globe Media is a locally owned independent media company that serves Boston and the surrounding region with award-winning journalism from the largest newsroom in New England. Boston Globe Media brands include The...
- pref_0060 [news_source_context] chosen=media-ownership.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: DPG Media Group is a Belgian media group. It is active in Belgium and the Netherlands. The exact ownership structure is not clear; it is believed that the group is mainly owned by the Belgian Van Thillo family. The comp...
- pref_0061 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: link is hosted on substack
- pref_0062 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `substack` in this form: link is hosted on substack
- pref_0064 [substack_filtering] chosen=labeler.antisubstack.fyi rejected=adcontrols.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: link is hosted on substack
- pref_0069 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Python is a high-level, versatile programming language known for its easy readability and vast ecosystem, used in web development, data science, automation, and more.
- pref_0070 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Go` in this form: Go (also known as Golang) is an open-source programming language designed for simplicity, reliability, and efficiency, particularly for building large-scale systems.
- pref_0072 [developer_identity] chosen=dev-labels.bsky.social rejected=github-labeler.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Dart is a client-optimized programming language for fast apps on any platform, developed by Google, and often used with the Flutter framework.
- pref_0074 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `bluesky-social/social-app` in this form: The Bluesky Social application for Web, iOS, and Android https://github.com/bluesky-social/social-app
- pref_0075 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: 📓 Storybook for React Native! https://github.com/storybookjs/react-native
- pref_0076 [developer_identity] chosen=github-labeler.bsky.social rejected=dev-labels.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: A React Rich Text Editor that's block-based (Notion style) and extensible. Built on top of Prosemirror and Tiptap. https://github.com/TypeCellOS/BlockNote
- pref_0080 [protocol_infrastructure] chosen=pds.labeler.tny.im rejected=dev-labels.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Account is hosted by the eurosky.social PDS
- pref_0082 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Baltimore Orioles` in this form: A Fan of the Baltimore Orioles
- pref_0083 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: A Fan of the Chicago White Sox
- pref_0084 [sports_fandom] chosen=mlb.blueskysportslabeler.xyz rejected=sports-labeler.hooray.social reasons=gpt4o_ties_candidates
  third_post: One recurring saved-note detail uses this boundary: A fan of the Toronto Blue Jays
- pref_0085 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_prefers_rejected
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: User is a fan of the Kansas City Chiefs
- pref_0086 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Cincinnati Bengals` in this form: User is a fan of the Cincinnati Bengals
- pref_0087 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: User is a fan of the Arizona Cardinals
- pref_0088 [sports_fandom] chosen=nfl.sickos.club rejected=mlb.blueskysportslabeler.xyz reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: User is a fan of the Carolina Panthers
- pref_0094 [fandom_content_warnings] chosen=ao3labeler.bsky.social rejected=label.directioners.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `⚠️ Graphic Depictions of Violence` in this form: This user marked themselves as Graphic Depictions of Violence (for funsies!)
- pref_0097 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Just here to have fun, no drama
- pref_0098 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: A smaller set of bookmarked follow-ups mentions `No Theories 🚫` in this form: No Conspiracy Theories Please!
- pref_0100 [fandom_identity] chosen=label.directioners.social rejected=ao3labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: One recurring saved-note detail uses this boundary: I Love Theories!
- pref_0101 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This user works in 2D!
- pref_0102 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `3D` in this form: This user works in 3D!
- pref_0104 [creator_discovery] chosen=furskycreators.bsky.social rejected=creatorlabeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: One recurring saved-note detail uses this boundary: This user is open for commission work!
- pref_0106 [account_verification] chosen=verified.observer rejected=creatorlabeler.blackwall.gg reasons=gpt4o_ties_candidates
  third_post: A smaller set of bookmarked follow-ups mentions `Verified` in this form: This account has been safely and independently verified as the true account of this individual.
- pref_0109 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_prefers_rejected
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: An account with this label is a verified human. The person that owns the account proved they are human by supplying their passport and we have verified that no other account with this passport exists.
- pref_0110 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Verified Human` in this form: An account with this label is a verified human. The person that owns the account proved they are human by supplying their passport and we have verified that no other account with this passport exists.
- pref_0111 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Only a few saved reports include this narrower pattern: An account with this label is a verified human. The person that owns the account proved they are human by supplying their passport and we have verified that no other account with this passport exists.
- pref_0112 [account_verification] chosen=label.onlyhumanhub.com rejected=trustcollective.org reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: An account with this label is a verified human. The person that owns the account proved they are human by supplying their passport and we have verified that no other account with this passport exists.
- pref_0117 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: A reply to a post that contains a likely political article.
- pref_0118 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Political News Link` in this form: A post that includes a link to a likely political article.
- pref_0120 [politics_filtering] chosen=no-pol-labeler.bsky.social rejected=pol.conmodsys.net reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: A post that includes a link to a likely political article.
- pref_0125 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: Content is in category "arts & culture". This label has been generated via machine learning and may not be accurate.
- pref_0126 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Culture & Arts` in this form: Content is in category "culture & arts". This label has been generated via machine learning and may not be accurate.
- pref_0128 [news_source_context] chosen=news.aendra.dev rejected=newsdetective.bsky.social reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: Content is in category "entertainment". This label has been generated via machine learning and may not be accurate.
- pref_0130 [news_source_context] chosen=no-opinions.bsky.social rejected=news.aendra.dev reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Opinion Article 📰` in this form: An opinion article from a major news source.
- pref_0137 [account_behavior] chosen=stechlab-labels.bsky.social rejected=moderation.bsky.app reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This account has posted without meaningful breaks in the last 24 hours, with no gap between posts that was longer than 2 hours. This behavior may be consistent with an organization account, a bot, accounts with multiple...
- pref_0138 [account_behavior] chosen=stechlab-labels.bsky.social rejected=moderation.bsky.app reasons=gpt4o_prefers_rejected
  third_post: A smaller set of bookmarked follow-ups mentions `No break greater than 1 hr yesterday` in this form: This account has posted without meaningful breaks in the last 24 hours, with no gap between posts that was longer than 1 hour. This behavior may be consistent with an organization account, a bot, accounts with multiple...
- pref_0140 [account_behavior] chosen=stechlab-labels.bsky.social rejected=moderation.bsky.app reasons=gpt4o_ties_candidates
  third_post: One recurring saved-note detail uses this boundary: This account made profile metadata changes on at least five days in the last 30 days. These changes may be small; but most accounts do not make frequent such changes.
- pref_0142 [urbanism_community] chosen=labeler.urbanism.plus rejected=labeler.bikesky.social reasons=gpt4o_ties_candidates
  third_post: A smaller set of bookmarked follow-ups mentions `Urbanist Parent` in this form: Parents who want kids to safely travel and play outside
- pref_0144 [urbanism_community] chosen=labeler.urbanism.plus rejected=labeler.bikesky.social reasons=gpt4o_ties_candidates
  third_post: One recurring saved-note detail uses this boundary: My ride costs more than your car.
- pref_0146 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: A smaller set of bookmarked follow-ups mentions `Meaningless Alt Text` in this form: Media posted with alt text that conveys effectively nothing at all (such as just the words "alt text").
- pref_0147 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: Media posted without any alt text provided.
- pref_0150 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: A smaller set of bookmarked follow-ups mentions `Meaningless Alt Text` in this form: Media posted with alt text that conveys effectively nothing at all (such as just the words "alt text").
- pref_0151 [accessibility] chosen=baatl.mastod.one rejected=alt-text-labeler.bsky.social reasons=gpt4o_ties_candidates
  third_post: Only a few saved reports include this narrower pattern: Media posted without any alt text provided.
- pref_0153 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This post contains multiple still images and only some of them have usable alt text.
- pref_0154 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Missing Alt Text` in this form: This post contains one or more still images and none of them has usable alt text.
- pref_0156 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: This post contains one or more still images and none of them has usable alt text.
- pref_0157 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: Follow-up notes and saved reports repeatedly include this narrower detail: This post contains multiple still images and only some of them have usable alt text.
- pref_0158 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: A smaller set of bookmarked follow-ups mentions `Missing Alt Text` in this form: This post contains one or more still images and none of them has usable alt text.
- pref_0160 [accessibility] chosen=alt-text-labeler.bsky.social rejected=baatl.mastod.one reasons=gpt4o_prefers_rejected,rejected_margin_is_maximal,normal_and_swapped_both_wrong
  third_post: One recurring saved-note detail uses this boundary: This post contains one or more still images and none of them has usable alt text.

## Required Rewrite Direction

- Keep rejected as the visible surface answer, but reduce rejected dominance.
- Increase chosen behavioral priority with saves, reports, follow-up, or high-consequence cases.
- Do not restore direct target wording such as `I want` or `I need`.
- If calibrated evidence truly favors rejected, flip chosen/rejected and update annotations.
