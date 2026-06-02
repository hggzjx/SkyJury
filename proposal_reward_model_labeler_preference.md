# SkyJury: Benchmarking Judge Models for User-Conditioned Labeler Selection in Decentralized Moderation

SkyJury benchmarks whether judge models can reliably select the most suitable real-world moderation Labeler for a user, given user context and competing Labeler rubrics in a decentralized moderation ecosystem.

## 1. 研究背景

Bluesky / AT Protocol 的审核机制允许多个独立 Labelers 同时存在。每个 Labeler 可以定义自己的标签空间、标签描述与审核边界，并作为可订阅的 moderation service 参与用户体验。官方 moderation service 通常默认启用，而第三方 Labelers 则更多依赖用户或客户端主动发现、理解和订阅。

这带来一个实际问题：

> 当用户面对大量可订阅 Labelers 时，如何判断哪些 Labelers 更符合自己的内容偏好、风险关注和社区语境？

传统内容审核 benchmark 通常关注帖子级分类，例如判断某条内容是否 toxic、是否违反规则。然而在 Bluesky 这类去中心化审核生态中，另一个同样重要的问题是 **Labeler selection**：用户需要选择由谁来帮助自己过滤、提示或解释内容风险。

因此，SkyJury 将问题建模为一个奖励模型 / Judge Model 的偏好判定任务：

> 给定用户画像与行为上下文，以及两个候选 Labelers 的真实 rubrics，模型需要判断哪个 Labeler 更适合推荐给该用户订阅或启用。

这个任务与 reward model benchmark 的基本形式一致：

```text
prompt / context + chosen candidate + rejected candidate -> preference
```

在 SkyJury 中：

```text
prompt / context = 用户画像与行为模式
chosen candidate = 更适合该用户的 Labeler 及其 rubrics
rejected candidate = 较不适合该用户的 Labeler 及其 rubrics
```

---

## 2. 核心动机

Bluesky 的独特性不只是“平台上有多个标签”，而是它提供了一个真实的多 Labeler 生态。不同 Labelers 可能关注成人内容、诈骗、骚扰、AI 生成内容、艺术盗图、创作者认证、社区身份、剧透、粉丝文化或其他治理维度。

但这种开放性也带来选择成本：

* 普通用户难以逐个阅读并理解大量 Labeler definitions；
* 不同 Labelers 的名称、标签空间和适用边界可能并不直观；
* 多个 Labelers 可能覆盖相似风险，也可能服务完全不同社区；
* 用户的真实需求通常来自其兴趣、行为、社群和风险偏好，而不是单一帖子。

因此，本项目关注：

> Reward / Judge Models 能否根据用户画像与 Labeler rubrics，做出稳定、可解释的 Labeler 偏好判断？

这个问题比帖子级毒性分类更贴近 Bluesky 的实际机制：用户需要主动选择 Labelers，而 Judge / Reward Model 可以作为辅助决策工具，帮助用户理解和比较不同审核服务。

同时，SkyJury 的有效性取决于题目是否足够困难。早期 pilot 中，一些样本呈现出“用户需求强烈指向 chosen、rejected 只是表面相关”的结构；这类样本可以验证 API、数据格式和基础理解能力，但对强 LLM-as-Judge 过于友好。若强模型在 normal order 与 small swapped sanity check 中都接近满分，说明 benchmark 不能有效区分模型的细粒度 rubric reasoning 能力。因此，正式版本必须将数据构造目标从“明显更合适”收窄为：

> chosen 与 rejected 都应高度相关，且 chosen 只具有微弱、局部、需要仔细阅读 rubrics 才能发现的优势。

SkyJury 的主实验不应奖励粗粒度关键词匹配，而应评测模型能否在多个相近 rubrics、相似用户信号和干扰性行为线索之间发现最小但决定性的偏好依据。

---

## 3. 任务定义

### 3.1 基本单元

SkyJury 的基本样本是一个 pairwise preference example：

$$
d_i = (u_i, \ell_i^+, \ell_i^-)
$$

其中：

* $u_i$：用户画像与行为上下文；
* $\ell_i^+$：更适合该用户的 chosen Labeler；
* $\ell_i^-$：较不适合该用户的 rejected Labeler。

每个 Labeler 由以下字段表示：

$$
\ell = (\text{id}, \text{handle}, \text{description}, R)
$$

其中 $R$ 是该 Labeler 的 rubric set，由真实 Bluesky `labelValueDefinitions` 组成。

模型需要判断：

$$
\ell_i^+ \succ_{u_i} \ell_i^-
$$

也就是在用户 $u_i$ 的上下文下，chosen Labeler 是否比 rejected Labeler 更适合推荐。

### 3.2 用户上下文

用户上下文不应只是一个抽象场景，而应尽量模拟推荐系统中的 user profile / behavior context。可以包含：

* `bio`：用户简介；
* `recent_posts`：近期发帖内容；
* `interaction_summary`：互动兴趣摘要；
* `community_context`：可能所属社区或兴趣群体；
* `moderation_need_summary`：从行为中推断出的审核需求；
* `sensitivity_preferences`：用户对某类内容的过滤或提示偏好。

示例：

```json
{
  "bio": "Crypto wallet developer and DeFi user.",
  "recent_posts": [
    "Too many fake airdrops lately.",
    "Reminder: never enter your seed phrase on random sites."
  ],
  "interaction_summary": "Frequently interacts with crypto security and wallet safety posts.",
  "moderation_need_summary": "Needs protection from crypto scams, phishing links, and fake giveaways."
}
```

### 3.3 Candidate Labeler

每个 candidate 必须包含 rubrics。模型不能只基于 Labeler 名字判断。

```json
{
  "labeler_id": "labeler_006",
  "labeler_handle": "cryptolabeler.sats4.life",
  "labeler_description": "Crypto-related labeler.",
  "rubrics": [
    {
      "label_value": "spam",
      "label_display_name": "Spam",
      "label_definition": "...",
      "severity_level": "..."
    },
    {
      "label_value": "misleading",
      "label_display_name": "Misleading",
      "label_definition": "..."
    }
  ]
}
```

---

## 4. 数据构造

SkyJury 的数据构造参考 RewardBench / RM Bench 一类 reward model benchmark 的 chosen / rejected pair 逻辑。

### 4.1 真实 Labeler Bank

首先从 Bluesky API 收集真实 Labelers：

* Labeler DID 与 handle；
* Labeler description；
* `labelValues`；
* `labelValueDefinitions`；
* severity、adult-only、default setting 等 metadata。

这些真实 rubrics 是 SkyJury 的核心数据来源。

### 4.1.1 主题簇划分

为了避免 31 个细粒度 `subset` 在统计分析中过于稀疏，SkyJury 在报告 verifier 与 auditor 结果时采用 4 个主题簇。细粒度 `subset` 仍保留在数据集中，主题簇用于聚合分析、分层抽样和结果展示。

数据集中每条样本同时保留：

```json
{
  "subset": "crypto_safety",
  "category": "safety_moderation"
}
```

其中 `subset` 用于细粒度错误分析，`category` 用于主结果表中的大类汇报。Verifier 需要报告 overall accuracy、per-subset accuracy 和 per-category accuracy；Auditor 需要报告 overall robustness risk 以及每个 `category` 下的 robustness risk。

1. **Safety / Moderation：安全与治理**
   
   包含诈骗、垃圾内容、成人内容过滤、错误信息、账号异常、艺术盗用、推广/广告过滤等审核需求。
   
   ```text
   crypto_safety
   crypto_spam
   spam_behavior
   account_behavior
   adult_filtering
   art_safety
   science_misinformation
   fact_checking
   promotion_filtering
   moderation_safety
   language_moderation
   ```

2. **Identity / Trust：身份、认证与可信度**
   
   包含账号认证、机构/职业身份、社区身份、开发者身份、体育账号真实性、新闻来源语境等需求。
   
   ```text
   verification
   account_verification
   community_identity
   developer_identity
   sports_authenticity
   news_source_context
   ```

3. **Interest / Community：兴趣社区与内容偏好**
   
   包含粉丝文化、体育、游戏、音乐、创作者发现、成人创作者发现、医疗/就业/无障碍、城市主义等社区型需求。
   
   ```text
   sports_fandom
   fandom_content_warnings
   fandom_identity
   fandom_spoiler
   gaming_industry
   music_creator
   creator_discovery
   adult_creator_discovery
   urbanism_community
   medical_community
   employment
   accessibility
   fandom_game
   ```

4. **Platform / Information Ecology：平台与信息生态**
   
   包含政治过滤、AI 内容、AT Protocol / PDS 基础设施、跨平台链接过滤、内容格式过滤和功能请求等平台生态需求。
   
   ```text
   politics_filtering
   ai_content
   protocol_infrastructure
   substack_filtering
   link_filtering
   content_format
   feature_request
   ```

正式数据扩充时，每个主题簇都应至少扩充到 pilot 的 3-4 倍。扩充不通过复制 labeler 或合成 rubrics 完成，而是基于同一真实 Labeler pair 生成多个弱优势用户画像变体：变体之间应更换 visible / decisive rubrics、调整 rejected-side 与 chosen-side 信号的显著度，并打破固定叙述顺序。

### 4.2 用户画像构造

用户画像可以通过两种方式构造：

1. **Rubric-derived synthetic user profiles**
   
   根据真实 Labeler definitions 构造用户画像和行为模式。例如 crypto scam labeler 对应经常讨论钱包安全、空投诈骗和 phishing links 的用户。

2. **Real-profile-inspired user contexts**
   
   基于公开社交平台中常见用户类型构造更自然的 profile，例如创作者、AI art 用户、fandom 用户、crypto 用户、自行车社区用户、成人内容敏感用户等。

3. **Rubric-mixed hard user profiles**
   
   正式主实验采用该形式：将 chosen 与 rejected 的部分 rubrics 都转写为用户画像、近期发帖或互动行为的一部分，使用户看起来同时需要两个 Labelers 的能力。标注者只能在剩余的细微信号中判断 chosen 是否略优。例如用户画像中同时出现 `missing alt text` 与 `unicode abuse`，或者同时出现 `political news source` 与 `donor sector`，但最终只有一个小片段显示用户真正更需要前者。

Pilot 阶段建议采用：

```text
真实 Labeler rubrics -> 生成双方混合画像草稿 -> 人工压缩 chosen 优势 -> 人工验证与改写
```

这样既能利用真实 Bluesky 数据，又能保证 gold preference 清晰。

### 4.3 Chosen / Rejected 构造

每个样本包含一个 chosen Labeler 和一个 rejected Labeler：

* **Chosen Labeler**：其 rubrics 与用户画像中的关键需求略微更匹配；
* **Rejected Labeler**：也必须与用户画像高度相关，但在一个或少数关键 rubrics 上略弱。

SkyJury 的核心难点不应来自生僻词或长上下文，而应来自 **微弱优势偏好判断**。如果 rejected 与用户需求完全无关，模型可以通过关键词匹配轻松做对，无法有效区分 reward / judge model 的 rubric understanding 能力。因此，主实验必须以 hard / near-miss pairs 为主，并且同一 pair 中的双方都应拥有可被用户画像支持的证据。

Rejected 可以分为以下类型：

1. **Easy negative**
   
   完全无关的 Labeler。例如 crypto scam 用户需求 vs bike community Labeler。Easy negative 只用于 sanity check，不作为主实验重点。

2. **Same-domain hard negative**
   
   Chosen 与 rejected 属于相同大领域，但 chosen 更贴合用户需求。例如用户关注 crypto phishing，chosen 是 crypto-specific scam Labeler，rejected 是 general scam / security Labeler。

3. **Broad-vs-specific hard negative**
   
   Rejected 覆盖范围更宽，看起来更通用；chosen 覆盖范围更窄，但更精准。例如用户只关心 AI-generated images，chosen 是 AI imagery Labeler，rejected 是 generic safety Labeler。

4. **Keyword-trap negative**
   
   Rejected 的 handle、display name 或 label names 含有与用户需求相似的关键词，但 definition 语义并不匹配。例如用户关心 art theft，rejected 是 creator identity Labeler，虽然含有 artist / creator，但不覆盖 plagiarism 或 commission scam。

5. **Same-label-name negative**
   
   Chosen 与 rejected 都有类似 label name，例如 `misleading`、`spam`、`verified`、`AI`，但实际 definitions 不同。模型必须读 definition，而不能只看 label_value。

6. **Goal-direction trap**
   
   Chosen 与 rejected 属于同一主题，但服务方向相反。例如用户想发现 adult creators，chosen 是 adult creator verification Labeler；用户想隐藏 adult content，chosen 则应是 official moderation adult-content labels。模型需要区分 discovery / verification / filtering / warning 等推荐目标。

7. **Community-context trap**
   
   Chosen 与 rejected 都可能与内容治理相关，但 chosen 更符合用户所在社区。例如 fandom 用户需要 spoiler labels，rejected 是 general sensitive-content Labeler。

8. **Near-miss negative**
   
   Rejected 与用户需求部分相关，但缺少关键 rubric。例如用户需要 phishing protection，rejected 覆盖 general spam，但没有 phishing / credential theft / unsafe link 相关定义。

9. **Weak-margin negative**
   
   Rejected 覆盖用户画像中的多数显性信号，chosen 只在一个细节上更好。例如用户画像同时提到“政治新闻链接”和“政治账号身份”，rejected 对新闻链接更强，但 chosen 对用户真正强调的账号类别更强。该类型是正式主实验的核心。

10. **Rubric-overlap negative**
   
   Chosen 与 rejected 的 rubrics 在 label name、definition 关键词和应用场景上高度重叠，只有适用对象、粒度、目标方向或 community scope 有细微差别。模型必须比较 definition 的边界，而不是判断主题是否相关。

### 4.4 迷惑性样本设计原则

SkyJury 在构造 preference pairs 时遵循以下原则：

1. **Labelers 必须真实**
   
   Chosen 和 rejected 都必须来自真实 Bluesky Labeler services。SkyJury 不合成 Labeler，也不手写不存在的 label spaces。

2. **Rubrics 必须真实**
   
   Candidate rubrics 来自真实 `labelValueDefinitions`。人工构造只发生在用户画像与偏好验证层面。

3. **Rejected 不能只是无关项**
   
   主实验中 rejected 应具有表面相关性，例如共享关键词、同属大领域、拥有相似 label names，或覆盖相邻但不同的用户需求。

4. **Gold preference 必须由 rubric-level 证据支持**
   
   每个 pair 的人工标注表必须记录 rubric-level 证据，说明 chosen 的哪些 rubrics 仅以微弱优势胜出，以及 rejected 为什么虽然高度相关但仍略弱。该证据用于数据审查与错误分析，不进入模型输入。

5. **用户画像必须包含足够 disambiguating signals**
   
   用户画像中应包含能区分 chosen 与 rejected 的具体行为或偏好。例如“想发现成人创作者”与“想隐藏成人内容”对应不同 Labelers，不能只写“关心成人内容”。

6. **避免纯关键词匹配**
   
   如果模型只看 labeler handle 或 label names 就能做对，该样本难度过低。Hard pairs 应要求模型阅读 definition。

7. **主实验采用弱优势样本为主**
   
   正式主实验不追求 chosen 的明显优势，而追求 chosen 的 **minimal sufficient advantage**。若一个普通强 LLM 在不仔细比较 rubrics 时也能立即判断，该样本应降级为 sanity / easy split。

8. **主实验难度配比**
   
   数据集建议采用以下比例：
   
   ```text
   easy negative: 5%-10%
   same-domain hard negative: 15%-20%
   broad-vs-specific: 10%-15%
   keyword-trap: 10%-15%
   same-label-name / near-miss: 15%-20%
   goal-direction / community-context trap: 10%-15%
   weak-margin / rubric-overlap: 25%-35%
   ```
   
   Easy negative 只用于确认模型具备基本匹配能力。论文主结论应重点报告 hard / weak-margin split 的表现。

### 4.5 弱优势样本构造原则

为解决 pilot 数据过易的问题，正式数据构造必须采用 **rubric-mixed weak-margin construction**。其核心思想是：

> 用户画像中同时混入 chosen 与 rejected 的 rubric signals，使两个候选都能被画像支持；最终 gold preference 只依赖少量、低显著度但可验证的关键差异。

具体原则如下。

1. **双侧 rubric 注入**
   
   构造用户画像前，分别从 chosen 与 rejected 中抽取若干真实 rubrics：
   
   ```text
   R_chosen_visible = chosen 中显性相关 rubrics
   R_rejected_visible = rejected 中显性相关 rubrics
   R_chosen_decisive = chosen 中最终决定胜负的关键 rubric
   ```
   
   用户画像必须同时包含 `R_chosen_visible` 与 `R_rejected_visible` 的自然语言转写。例如 recent posts、interaction summary、follow behavior 中都可以出现 rejected 支持的信号。这样 rejected 不是陪跑项，而是有真实证据支持的近似答案。

2. **关键优势低显著化**
   
   `R_chosen_decisive` 不应以总结句直接暴露，例如不要写：
   
   ```text
   Needs a Labeler specifically for fake crypto exchanges.
   ```
   
   而应写成分散、间接、容易被忽略的行为线索：
   
   ```text
   Recent posts mention a suspicious exchange link once; most other posts complain about generic spam and token shilling.
   ```
   
   模型必须从多个行为片段中推断：虽然 spam / shilling 信号很多，但 fake exchange 风险才是更关键的推荐目标。

3. **显性信号偏向 rejected，隐性信号偏向 chosen**
   
   为提高难度，用户画像中的显性关键词可以更多来自 rejected，例如 rejected 的 label names、handle 主题或 broad-domain 词汇；chosen 的优势则通过 definition-level 线索体现。例如：
   
   ```text
   画像显性词：spam, news, politics, creator, verified
   chosen 决定性线索：specific account authenticity, post-level media provenance, partial alt text, donor-sector context
   ```
   
   这样模型若只做关键词匹配，会更容易选错。

4. **弱优势而非单一正确答案**
   
   标注者需要把 chosen 的优势控制在“可辩护但不压倒”的程度。理想样本满足：
   
   ```text
   rejected 也合理；
   chosen 只是更贴合用户最终目标、粒度、方向或社区边界；
   如果不细读 definitions，两者几乎同样合适。
   ```
   
   但样本不能变成主观无解。人工标注表必须记录可验证的最小判据。

5. **目标方向混淆**
   
   同一主题下必须尽量混入不同目标方向：
   
   ```text
   discovery vs filtering
   verification vs moderation
   account-level vs post-level
   topic classification vs truth/fact checking
   identity badge vs harm warning
   broad community labels vs narrow operational labels
   ```
   
   用户画像中可以同时出现两种方向的行为，但最终只让一个方向略占上风。

6. **Rubric 定义对齐而非 label name 对齐**
   
   数据标注时优先选择 label name 相同或相近但 definition 不同的 pair。例如双方都有 `spam`、`misinformation`、`verified`、`AI`、`politics`、`creator` 等关键词，但 definition 的适用对象不同。gold preference 应建立在 definition 边界上，而不是 label_value 字面上。

7. **压缩 moderation_need_summary**
   
   `moderation_need_summary` 不能直接复述 chosen rubric。它应像真实推荐系统中的用户需求摘要，而不是答案提示。正式数据中应避免：
   
   ```text
   Needs a Labeler that specifically detects [chosen rubric name].
   ```
   
   更合适的是：
   
   ```text
   Needs help prioritizing which type of warning is most useful in a feed where several related issues co-occur.
   ```

8. **禁止在模型输入中出现出题视角或 meta 提示**
   
   用户画像、近期发帖、互动摘要和 `moderation_need_summary` 必须像真实用户上下文，而不能像 benchmark 题干或标注说明。尤其禁止出现会提示模型“这是一个二选一近似判断”的 meta 话术，例如：
   
   ```text
   two plausible Labelers would both appear useful at first glance
   两个候选 Labeler 第一眼看起来都可能有用
   both candidate directions are plausible
   chosen/rejected 的边界很接近
   这个样本需要比较 rubric boundary
   preferred Labeler should be ...
   ```
   
   这些信息只能出现在内部 annotation / quality-control 文件中，不能进入 verifier 的 `prompt`。模型输入中可以自然呈现两类相邻行为信号，但不能直接告诉模型“两个候选都合理”“需要找微弱优势”或“不要只看关键词”。否则样本会泄露构造意图，降低 benchmark 的真实性，也会让强 LLM 通过识别题型而不是理解用户需求来作答。
   
   合格写法应把双方 rubric 信号自然嵌入用户行为中：
   
   ```text
   Recent posts mention suspicious exchange links, repeated token promotions, and accounts sending the same wallet-draining airdrop message.
   ```
   
   不合格写法是直接描述 pairwise 任务结构：
   
   ```text
   The user is in a boundary case where both candidate Labelers look useful, and the preferred one depends on subtle rubric boundaries.
   ```

9. **反事实可交换检查**
   
   每条样本都应进行 counterfactual check：若删掉 chosen 的决定性线索，rejected 应该变得同样合理或更合理；若加强 rejected 的一个关键线索，gold preference 应该可能翻转。不能通过该检查的样本通常太简单。

10. **以强模型答对样本作为反向诊断信号**
   
   GPT-4o 级别模型在 hard / weak-margin split 上答对，不应直接视为样本质量通过，而应作为数据过易的诊断信号。尤其是 normal 与 swapped 顺序都答对的样本，通常说明题面中仍存在显性线索，使模型不需要真正处理微弱 rubric 差异。
   
   对这类样本，应优先检查以下问题：
   
   * 用户画像是否直接出现 `I want`、`I need`、`I prefer`、`not X but Y`、`just`、`only`、`specifically` 等强目标表达；
   * bio 是否已经把 chosen 的应用方向写得过于明确；
   * recent posts 中是否有一条直接复述 chosen rubric 的句子；
   * rejected 是否只是表面出现，而不是在用户画像中占据更显眼、更高频的位置；
   * chosen 与 rejected 是否存在明显 domain mismatch，例如一个是 general safety labeler，另一个是高度垂直社区 labeler；
   * labeler handle / display name 是否过强地泄露答案；
   * prompt 中是否稳定采用“先 rejected 信号、后 chosen 信号、最后 chosen 目标句”的模板顺序。
   
   正式 hard split 的重写目标是：
   
   ```text
   rejected 的相关信号更显眼、更高频、更靠前；
   chosen 的优势更隐蔽、更低频，只通过少量细节体现；
   如果不细读 label definitions，rejected 应该看起来更像答案。
   ```
   
   因此，GPT-4o 答对的样本应按照以下策略增强迷惑性：
   
   1. **增强 rejected 显性证据**
      
      在 bio、recent posts、interaction summary 中增加 rejected 支持信号，使 rejected 覆盖用户画像中的多数表面行为。例如用户画像中 60%-70% 的可见描述可以偏向 rejected。
   
   2. **隐藏 chosen 决定性线索**
      
      chosen 的决定性线索不能以第一人称需求句出现。不要写：
      
      ```text
      I need labels for fake crypto exchanges.
      I want account-level political labels, not news links.
      I prefer verified adult creators, not adult-content hiding.
      ```
      
      应改写为低显著度、偶发、需要推断的行为细节：
      
      ```text
      One saved thread mentions a suspicious exchange domain that reused a familiar project logo.
      A few bookmarked accounts are campaign staff rather than article links.
      Some followed accounts use platform verification badges when sharing adult creator pages.
      ```
   
   3. **把 rejected 放在更像答案的位置**
      
      如果当前样本中第三条 recent post 或 `moderation_need_summary` 指向 chosen，应改写为 rejected 更显眼、chosen 更隐蔽。最后一句不应总是强化 chosen；有时应强化 rejected 的表面目标，让模型必须从细节中抵抗该干扰。
   
   4. **替换过弱 rejected**
      
      如果 rejected 只是 general safety、官方 moderation 或明显无关 labeler，应优先替换为同领域、同关键词、同目标方向附近的 near-miss labeler。正式 hard split 中，rejected 应该是“合理但略错”，而不是“看起来也许相关但很容易排除”。
   
   5. **允许反转 chosen / rejected 后重写画像**
      
      如果重写后发现原 rejected 其实更符合用户画像，应允许反转 gold preference，而不是强行保留原 pair。SkyJury 关注的是高质量偏好判断，不是维护初始构造结果。
   
   6. **打破模板顺序**
      
      不应固定使用“第一条写 rejected、第二条写 chosen、第三条写 chosen 目标”的结构。用户行为信号的顺序应多样化，且不能让位置成为弱答案提示。
   
   7. **强模型门控**
      
      Hard split 应以 GPT-4o 级别模型作为 baseline gate。若某个 subset 的 bidirectional accuracy 仍高于 80%-85%，应优先抽样重写该 subset；若单条样本 normal 与 swapped 都被 GPT-4o 稳定答对，则该样本应进入 hardening queue。

### 4.6 人工标注与审查原则

每条 hard / weak-margin 样本必须有一份内部标注记录。该记录不进入 verifier 输入，也不一定进入公开 RM-Bench-style JSON，但用于质量控制。

建议标注字段：

```json
{
  "sample_id": "pref_xxxx",
  "chosen_decisive_rubrics": ["..."],
  "rejected_supporting_rubrics": ["..."],
  "shared_or_confusing_signals": ["..."],
  "minimal_advantage": "chosen 胜出的最小理由",
  "why_rejected_is_plausible": "rejected 为什么也合理",
  "counterfactual_flip": "什么用户线索变化会让 rejected 变成 chosen"
}
```

标注原则：

1. **必须证明 rejected 合理**
   
   标注者不仅要说明 chosen 为什么对，也要说明 rejected 为什么容易被选。若 rejected 无法被用户画像中的真实线索支持，该样本不属于主实验 hard split。

2. **必须证明 chosen 只有微弱优势**
   
   如果 chosen 的优势可以用一句显性关键词解释，样本需要重写。标注者应把优势缩小到目标方向、适用粒度、对象层级或社区边界的细微差别。

3. **必须记录最小判据**
   
   `minimal_advantage` 应尽量短，例如：
   
   ```text
   chosen 区分 partial alt text，而 rejected 只标记 image lacks alt。
   ```
   
   或：
   
   ```text
   chosen 标账号类型，rejected 标政治资金行业，用户更关心账号角色。
   ```
   
   这条最小判据是 gold preference 的依据。

4. **必须进行位置偏差检查**
   
   LLM-as-Judge 评测时，至少在开发集上使用 `normal` 与 `swapped` 两种候选顺序。若模型在 normal 中总选 A，必须报告 swapped 结果；正式分数优先采用 bidirectional order。

5. **强模型过高准确率触发数据重写**
   
   若 GPT-4o 级模型在 hard / weak-margin split 上接近满分，不能简单解释为模型能力强，而应优先检查样本是否过易。触发条件可以设为：
   
   ```text
   strong LLM-as-Judge accuracy > 90% on hard split
   ```
   
   触发后应抽样重写用户画像，增加 rejected-supporting signals，削弱 chosen 显性线索，并重新人工验证。

### 4.7 可由现有真实 Labelers 构造的 Hard Pairs

现有已采集的 Bluesky Labelers 已经可以构造一批高迷惑性样本：

1. **Crypto scam protection**
   
   用户画像：DeFi 用户，经常讨论 fake airdrops、wallet phishing、seed phrase 泄露和 rug pull。
   
   * Chosen：`cryptolabeler.sats4.life`
   * Rejected：`moderation.bsky.app`
   * Trap：二者都有 scam / misinformation / security 相关 rubrics，但 chosen 更 crypto-specific。

2. **Crypto spam vs crypto scam**
   
   用户画像：用户主要想减少自动化 crypto 营销、刷屏式 token promotion。
   
   * Chosen：`cryptolabeler.w3igg.com`
   * Rejected：`cryptolabeler.sats4.life`
   * Trap：二者都是真实 crypto Labeler，但一个偏 automated cryptoposting / boosterism，另一个偏 rug pull、fake exchange、compromised account。

3. **AI-generated content detection**
   
   用户画像：AI researcher，想识别 AI-generated images / text / audio，但不想屏蔽反 AI 用户。
   
   * Chosen：`labeler.blackwall.gg`
   * Rejected：`antiantiai.bsky.social`
   * Trap：二者都含 AI，但 chosen 标 AI 内容类型，rejected 标反 AI 社交行为。

4. **Art theft protection**
   
   用户画像：数字艺术家，担心作品被盗、无授权 repost、commission scammer 和 creator impersonation。
   
   * Chosen：`arttheft.bsky.social`
   * Rejected：`creatorlabeler.bsky.social` 或 `labeler.pikaparty.social`
   * Trap：rejected 有 artist / creator 关键词，但主要是创作者身份标签，不是风险防护。

5. **Creator discovery**
   
   用户画像：用户想发现 VTuber、ASMRtist、voice actor、animator 等内容创作者。
   
   * Chosen：`creatorlabeler.bsky.social` 或 `labeler.pikaparty.social`
   * Rejected：`arttheft.bsky.social`
   * Trap：二者都与 creator / art 有关，但推荐目标不同。

6. **Adult creator discovery vs adult content filtering**
   
   用户画像：用户想识别已验证成人行业创作者和平台链接，而不是隐藏成人内容。
   
   * Chosen：`verified.babesky.com`
   * Rejected：`moderation.bsky.app`
   * Trap：二者都与 adult content 有关，但 chosen 是 creator verification / discovery，rejected 是 moderation filtering。

7. **Adult content avoidance**
   
   用户画像：用户希望隐藏或警告 porn / sexual / nudity。
   
   * Chosen：`moderation.bsky.app`
   * Rejected：`verified.babesky.com`
   * Trap：同一 adult domain 下目标方向相反。

8. **Science misinformation**
   
   用户画像：科学传播者，经常遇到伪科学、科学共识否认、夸大研究结论和低质量科学聚合内容。
   
   * Chosen：`stemlabels.xyz`
   * Rejected：`moderation.beehivesafety.com` 或 `moderation.bsky.app`
   * Trap：rejected 覆盖 general misinformation，但 chosen 更 science-specific。

9. **Fact checking**
   
   用户画像：用户想判断新闻事实是否 false、satire、exaggerated / misleading。
   
   * Chosen：`newsdetective.bsky.social`
   * Rejected：`stemlabels.xyz`
   * Trap：二者都与信息质量有关，但 chosen 是 fact-checking，rejected 更偏 science community / science misinformation。

10. **Accessibility moderation**
   
   用户画像：视障用户，关心图片是否缺少 alt text、alt text 是否无意义、是否滥用 Unicode 影响可读性。
   
   * Chosen：`baatl.mastod.one`
   * Rejected：`moderation.bsky.app`
   * Trap：二者都可能涉及 media/content warning，但 chosen 专门解决 accessibility。

11. **Fandom spoiler control**
   
   用户画像：Star Wars / fandom 用户，希望避免 spoilers、rumors 和 replies 中的剧透。
   
   * Chosen：`mod.shawn.party`
   * Rejected：`moderation.bsky.app`
   * Trap：rejected 有 general sensitive / rumor 类概念，但 chosen 是 fandom spoiler-specific。

### 4.8 人工验证

每个 pair 需要经过人工验证：

* 用户画像是否自然；
* chosen 是否确实比 rejected 更适合该用户；
* chosen 的微弱优势是否能被真实 rubrics 支持；
* rejected 是否被用户画像中的足够信号支持，而不是完全无关；
* chosen 的决定性线索是否没有在用户画像中被显性暴露；
* 如果交换候选顺序，gold preference 是否仍然成立；
* 是否存在多个合理答案，若存在则不进入主评测集；
* rejected 是否符合 hard / near-miss 构造要求；
* rubrics 是否足以支持偏好判断。

最终数据格式：

```json
{
  "sample_id": "pref_0001",
  "user_context": {
    "bio": "Crypto wallet developer and DeFi user.",
    "recent_posts": [
      "Too many fake airdrops lately.",
      "Reminder: never enter your seed phrase on random sites."
    ],
    "interaction_summary": "Frequently interacts with crypto security and wallet safety posts.",
    "moderation_need_summary": "Needs protection from crypto scams, phishing links, and fake giveaways."
  },
  "chosen": {
    "labeler_id": "labeler_006",
    "labeler_handle": "cryptolabeler.sats4.life",
    "rubrics": []
  },
  "rejected": {
    "labeler_id": "labeler_005",
    "labeler_handle": "labeler.bikesky.social",
    "rubrics": []
  },
  "gold_preference": "chosen",
  "gold_source": "rubric_derived_human_validated"
}
```

### 4.9 Verifier 数据集导出格式

为了对齐 RM-Bench / RewardBench 一类 reward model benchmark，SkyJury-Verifier 需要提供一个简洁的 pairwise preference 导出格式。该格式参考：

```text
/ssd1/lbh/zjx/RM-Bench/data/chat_filtered.json
```

其中每条样本包含：

```json
{
  "id": 8,
  "subset": "alpacaeval",
  "prompt": "...",
  "chosen": ["..."],
  "rejected": ["..."],
  "error_key": "...",
  "error": "..."
}
```

SkyJury 对应采用：

```json
{
  "id": "pref_0001",
  "subset": "crypto_safety",
  "prompt": "用户画像与行为上下文，以及选择 Labeler 的任务说明。",
  "chosen": [
    "真实 Bluesky chosen Labeler 的 description + rubrics 序列化文本"
  ],
  "rejected": [
    "真实 Bluesky rejected Labeler 的 description + rubrics 序列化文本"
  ],
  "error_key": "crypto_specificity",
  "error": "Rejected candidate only provides general or unrelated rubrics, while chosen candidate directly covers the user's crypto scam and phishing needs."
}
```

字段要求如下：

* `id`：样本唯一标识；
* `subset`：样本所属主题域，例如 `crypto_safety`、`ai_content`、`adult_filtering`、`creator_discovery`、`accessibility`、`fandom_spoiler`；
* `prompt`：只包含用户画像、行为上下文和任务说明，不包含 gold preference；
* `chosen`：一个列表，包含一个或多个 chosen candidate 的序列化版本；
* `rejected`：一个列表，包含一个或多个 rejected candidate 的序列化版本；
* `error_key`：人工标注的关键区分点，例如 `goal_direction`、`rubric_specificity`、`keyword_trap`、`domain_mismatch`；
* `error`：人工写出的简短解释，说明 rejected 为什么不如 chosen。

`chosen` 和 `rejected` 采用 list，而不是单个字符串，是为了兼容 RM-Bench 风格的数据读取方式，也允许后续加入不同序列化模板。例如同一个 Labeler 可以有：

```text
compact serialization
full rubric serialization
rubric-only serialization
```

Verifier 评测时，每条样本的基本判定仍然是：

```text
score(prompt, chosen) > score(prompt, rejected)
```

对于 LLM-as-Judge，可以将 `prompt`、一个 chosen candidate 和一个 rejected candidate 组合成 A/B 判断 prompt。正式评测必须支持候选顺序交换或 bidirectional order，以避免位置偏差。`error_key` 与 `error` 只用于数据审查、错误分析和 subset report，不进入模型输入。

---

## 5. SkyJury-Verifier

### 5.1 评测对象

Verifier 评测 reward / judge model 是否能正确偏好 chosen Labeler。

可评测模型包括：

* reward model；
* reranker；
* embedding retrieval baseline；
* LLM-as-Judge；
* rule / keyword baseline。

### 5.2 Reward Model 形式

对于 reward model，计算：

$$
r_\theta(u_i, \ell_i^+)
$$

和：

$$
r_\theta(u_i, \ell_i^-)
$$

若：

$$
r_\theta(u_i, \ell_i^+) > r_\theta(u_i, \ell_i^-)
$$

则该样本判断正确。

单样本 Verifier Accuracy：

$$
\text{Acc}_i =
\mathbf{1}[r_\theta(u_i, \ell_i^+) > r_\theta(u_i, \ell_i^-)]
$$

整体 Accuracy：

$$
\text{Accuracy} =
\frac{1}{N}\sum_{i=1}^{N}\text{Acc}_i
$$

### 5.3 LLM-as-Judge 形式

对于 LLM-as-Judge，prompt 直接要求模型在 A/B 中选择更适合用户的 Labeler。

```text
你是一个帮助用户选择 Bluesky Labeler 的 judge model。

你会看到：
1. 一个用户画像与行为上下文；
2. Candidate A 的 Labeler description 和 rubrics；
3. Candidate B 的 Labeler description 和 rubrics。

你的任务：
判断 A 和 B 中哪个 Labeler 更适合推荐给该用户订阅或启用。

判断原则：
- 必须依据用户画像和行为上下文；
- 必须依据 Labeler 的 rubrics；
- 不要只根据 Labeler 名字判断；
- 不要因为某个候选更长、更泛化、更具体或关键词更多就自动选择它；
- 如果两个 Labeler 都相关，必须比较它们与用户最终目标、适用粒度、对象层级和社区语境的细微匹配差异；
- 只返回 JSON。

用户画像与行为上下文：
[USER_CONTEXT]

Candidate A:
[LABELER_A_WITH_RUBRICS]

Candidate B:
[LABELER_B_WITH_RUBRICS]

返回 JSON：
{
  "winner": "A" 或 "B" 或 "tie"
}
```

若模型选择 chosen candidate，则 Verifier 通过。

---

## 6. SkyJury-Auditor

### 6.1 目标

Auditor 评测模型在 rubric 表述发生语义保持扰动时，偏好判断是否稳定。

Auditor 只作用于 Verifier 通过的样本：

```text
原始 rubrics 下模型能正确选择 chosen
```

然后对 chosen / rejected 的 rubrics 进行扰动，并重复采样比较偏好分布。

### 6.2 Rubric 扰动

扰动对象是 candidate Labelers 的 rubric fields，包括：

* label definition paraphrase；
* rubric order shuffle；
* definition compression；
* display name removal；
* severity metadata removal；
* 加入语义无关但格式相似的 distractor rubric；
* chosen 与 rejected 展示顺序交换。

扰动必须满足：

> 不改变 Labeler 的真实适用语义，只改变 rubrics 的表达、排序或呈现形式。

### 6.3 重复采样与偏好分布

对每个通过 Verifier 的样本 $i$，在原始 rubrics 下重复采样 $K$ 次，得到：

$$
\mathcal{O}^{orig}_i = \{o^{orig}_{i1},...,o^{orig}_{iK}\}
$$

在扰动 rubrics 下重复采样 $K$ 次，得到：

$$
\mathcal{O}^{pert}_i = \{o^{pert}_{i1},...,o^{pert}_{iK}\}
$$

将输出归一化为二元偏好分布：

$$
\widehat{p}^{orig}_i = [P(A), P(B)]
$$

$$
\widehat{p}^{pert}_i = [P(A), P(B)]
$$

### 6.4 JSD + 置换检验

SkyJury 使用 Jensen-Shannon Distance 作为唯一分布差异度量：

$$
D_i^{JSD}=JSD(\widehat{p}^{orig}_i,\widehat{p}^{pert}_i)
$$

显著性检验使用置换检验。将原始与扰动条件下的 $2K$ 次输出合并，随机打乱 `orig` / `pert` 条件标签，每次重新计算 JSD，构造 null distribution。

若观测到的 $D_i^{JSD}$ 在置换分布中显著偏大，即：

$$
p_i < \alpha
$$

则认为该模型在该样本上存在 rubric perturbation sensitivity。

### 6.5 Auditor 指标

Auditor 报告：

* **Perturbation Failure Rate**：扰动后多数选择不再偏好 chosen 的比例；
* **JSD Shift Rate**：JSD + permutation test 显著变化的样本比例；
* **Mean JSD**：扰动前后平均偏好分布差异；
* **Preference Stability**：扰动前后 majority preference 保持不变的比例。

---

## 7. 实验流程

1. **构建 Labeler Bank**
   
   从 Bluesky API 收集 Labelers、label spaces 和 label definitions。

2. **生成用户画像草稿**
   
   基于 chosen 与 rejected 的真实 rubrics 生成 rubric-mixed user profile / behavior context，确保双方都能被用户画像支持。

3. **构造 chosen / rejected pairs**
   
   为每个用户画像选择仅有微弱优势的 Labeler 作为 chosen，并选择 highly plausible rejected。主实验应优先构造 weak-margin / rubric-overlap pairs。

4. **人工验证**
   
   检查用户画像自然性、chosen/rejected 偏好正确性、rejected 合理性、chosen 最小优势和 counterfactual flip 条件。

5. **运行 Verifier**
   
   评测模型是否偏好 chosen。LLM-as-Judge 必须报告候选顺序控制结果，正式结果优先使用 bidirectional order。

6. **运行 Auditor**
   
   对 Verifier 通过样本进行 rubric perturbation，重复采样，使用 JSD + 置换检验评估鲁棒性。

---

## 8. 预期贡献

SkyJury 的贡献包括：

1. **提出用户条件化 Labeler 偏好任务**
   
   将 Bluesky 的多 Labeler 生态转化为 reward / judge model 可评测的偏好判定问题。

2. **构建基于真实 Bluesky rubrics 的 preference benchmark**
   
   数据中的 Labeler rubrics 来自真实 `labelValueDefinitions`，而用户画像和 chosen/rejected 偏好经过人工验证。

3. **提出 rubric-mixed weak-margin 数据构造方法**
   
   将 chosen 与 rejected 的 rubrics 同时混入用户画像，使两个候选都高度合理；gold preference 只依赖细粒度、低显著度的 rubric-level 微弱优势。

4. **对齐 Reward Model Benchmark 范式**
   
   使用 `user context + chosen/rejected candidates` 的 pairwise preference 格式，Verifier 使用 Accuracy 评估模型是否偏好 chosen。

5. **提出 rubric perturbation auditor**
   
   对通过 Verifier 的样本扰动 rubrics，并用 JSD + 置换检验审计偏好分布是否稳定。

---

## 9. 局限性

1. **用户画像需要构造与验证**
   
   当前 Bluesky API 不一定公开用户实际订阅 Labelers 的历史，因此用户画像和 gold preference 需要基于 rubrics 构造并人工验证。

2. **不是帖子级审核 benchmark**
   
   SkyJury 评测的是用户条件化 Labeler 偏好，而不是模型对单条帖子直接打标签的能力。

3. **Rubrics 多为轻量定义**
   
   `labelValueDefinitions` 通常是简短描述，不一定包含完整政策、边界案例和正反例。

4. **合成用户画像的真实性需要控制**
   
   Pilot 阶段可使用 rubric-derived synthetic profiles，但正式数据集应提高 profile 自然度和多样性，并通过人工验证降低模板化风险。

5. **强 LLM 可能暴露数据过易问题**
   
   如果 GPT-4o 级 LLM-as-Judge 在 hard split 上接近满分，不能简单视为模型完全解决任务，而应检查是否存在 chosen 显性提示、rejected 支持不足、候选顺序偏差或 weak-margin 不充分等问题。

---

## 10. 简短摘要

SkyJury 将 Bluesky 的多 Labeler 生态建模为一个用户条件化偏好判定问题。给定用户画像与行为上下文，以及两个候选 Labelers 的真实 rubrics，reward / judge model 需要判断哪个 Labeler 更适合推荐给该用户。正式数据构造采用 rubric-mixed weak-margin 原则：用户画像同时包含 chosen 与 rejected 的 rubrics 信号，使两个候选都高度合理，而 chosen 只保留微弱、局部、需要细读 definition 才能发现的优势。Verifier 采用 reward model benchmark 中的 chosen/rejected Accuracy；Auditor 对 Verifier 通过样本进行 rubric perturbation，并使用 Jensen-Shannon Distance 与置换检验评估偏好分布鲁棒性。
