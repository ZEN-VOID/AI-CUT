---
name: comic-novel-adaptation
description: Use when 任意文本、图片、视频或热点新闻事件需要被改编为适合后续漫画生成的强情节小说底稿，尤其适合要先做来源归一、事实边界判断、章节化推进与章末钩子设计的场景。
governance_tier: full
---

# 漫画小说改编

## 概述

本技能把任意资料改编为“适合继续做漫画生成”的小说底稿，而不是只把原材料换一种说法复述。

核心目标有三个：

- 保住来源材料的有效事实、情绪核与卖点。
- 把素材改造成章节化、场景化、强钩子化的漫画小说。
- 让成稿天然具备后续漫画分镜、角色立绘与画面提示词蒸馏所需的视觉锚点。
- 让氛围层与视觉冲击点在正文阶段就被预先设计，而不是写完后才被动补桥接。
- 在需要兼容解说漫时，让正文描述既能成为漫画画面母稿，也能成为可直接朗读的沉浸式旁白素材。

默认概念：

- 默认输入以文本为主，但允许图片、视频、新闻事件、网络热搜与多源混合输入。
- 默认输出不是“传统长篇纯文学”，而是“强情节、强角色、强画面、强章末钩子”的漫画小说底稿。
- 默认每章都必须留下未闭合缺口，不把真相讲尽，不把冲突结清，不把情感彻底落地。

## Skill Execution Rule (Mandatory)

硬规则：

- 先做来源归一与事实边界判断，再做文学化改编。
- 先锁定“这是给漫画继续消费的小说底稿”，再决定文风、节奏与章节密度。
- 先锁定高冲击画面候选与氛围压力场，再决定正文的展开顺序与停笔位置。
- 若用户要求兼容解说漫，正文必须同时满足“可画”和“可念”：画面要清，旁白要顺，句子要短，声压要稳。
- 改编不是照抄。可以重组、压缩、扩写、补桥，但不得把核心卖点改没。
- 图片/视频输入不得直接写成空泛描述，必须先还原事件链、冲突链与视觉锚点。
- 新闻/热搜输入默认进入“事实锚定”模式：已知事实与虚构扩写必须可区分，不能把虚构段落冒充现实事实。
- 若用户未指定类型，优先按素材天然势能选择：悬疑、甜宠、复仇、玄幻、穿越重生、都市成长等最能放大原素材冲突的路由。

## Business Requirement Analysis Contract (Mandatory)

在真正下笔前，至少先锁定以下分析字段：

| analysis_field | 要回答的问题 | 默认要求 |
| --- | --- | --- |
| `business_goal` | 这篇稿子要服务什么后续动作 | 默认服务“漫画生成前的小说母稿” |
| `business_object` | 原始输入到底是什么 | 文本 / 图片 / 视频 / 新闻热搜 / 多源混合 |
| `core_sell_point` | 最值得追更的卖点是什么 | 人物关系、反转、悬念、欲望、复仇、甜虐、奇观至少锁一个 |
| `constraint_profile` | 哪些边界不能越 | 事实边界、平台安全、角色年龄、暴力尺度、用户明示禁区 |
| `success_criteria` | 什么叫改编成功 | 读得下去、看得见、能分镜、有钩子、可继续生成漫画 |
| `topology_fit` | 哪种思行网络最合适 | 单源走串行主干，多源与新闻热点走“归一 + 分支 + 汇流” |
| `step_strategy` | 本轮重点在哪 | 事实抽取、类型放大、章节骨架、正文落地、钩子强化 |
| `manga_impact_profile` | 哪几处必须具备页级/格级冲击力 | 默认至少锁定 3 个高冲击画面候选 + 1 个翻页停笔点 |
| `voice_immersion_profile` | 如果要兼容解说漫，旁白读出来靠什么成立 | 默认锁定 旁白节奏、句长控制、声画同命题、冗余剔除 |

## Context Preload (Mandatory)

- 每次调用本技能时，先读取同目录 `CONTEXT.md`。
- 冲突优先级：用户显式请求 > 仓库 `AGENTS.md` > 本 `SKILL.md` > `CONTEXT.md`。
- 新失败模式、可复用成功模式、来源类型适配经验与钩子写法增量都必须回写 `CONTEXT.md`。

## Reference Loading Guide (Mandatory)

主合同只保留骨架、门禁与字段真源。长细则下沉到 `references/`：

- [references/source-intake-and-mode-selection.md](references/source-intake-and-mode-selection.md)
  - 来源归一、模式选择、多源合并、类型判型。
- [references/comic-novel-writing-spec.md](references/comic-novel-writing-spec.md)
  - 漫画小说成稿规格、章节节奏、视觉锚点与对白密度。
- [references/hook-ending-playbook.md](references/hook-ending-playbook.md)
  - 章末钩子公式、分类型示例、强化与避坑。
- [references/hotsearch-news-adaptation.md](references/hotsearch-news-adaptation.md)
  - 新闻/热搜改编的事实边界、热点选题公式与近期参考。
- [/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md](/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md)
  - 当用户要求“解说漫兼容 / 旁白可朗读”时，继承其“旁白主导、同命题声画配对、动作画面承载无台词推进”的约束，但本技能仍以小说主稿为主，不直接改写成格式化对白稿。

## Total Input Contract

### 必需输入

- `source_material`
  - 原始素材本体，可以是文本、图片描述、视频内容摘要、新闻事件或多源集合。
- `adaptation_goal`
  - 若用户未给，默认为“改编为可继续用于漫画生成的精彩漫画小说底稿”。

### 可选输入

- `source_type`
  - `text | image | video | news_event | hot_search | mixed`
- `target_genre`
  - `言情甜宠 | 虐恋 | 悬疑惊悚 | 玄幻修仙 | 系统 | 穿越重生 | 复仇 | 都市成长 | 科幻 | 校园`
- `target_audience`
- `length_target`
  - `short_burst | mini_serial | medium_arc`
- `chapter_count`
- `truth_boundary`
  - `faithful | inspired_by | free_reimagining`
- `hook_intensity`
  - `balanced | strong | relentless`
- `delivery_flavor`
  - `standard_comic | explainer_comic_compatible`
- `narration_density`
  - `lean | standard | rich`
- `output_mode`
  - `reply_only | full_package`

### 禁止输入

- 要求逐段照抄受版权保护长文本并仅做表面换词。
- 未声明为虚构衍生时，把现实新闻改写成伪纪实。
- 仅给“热点名词”却要求编出具体事实结论。

### 输入处理原则

1. 默认先识别来源类型；未声明时自动判型。
2. 图片/视频先抽“事件链 + 角色关系 + 视觉奇点”，再进入文学改编。
3. 新闻/热搜先抽“已知事实 + 公共情绪 + 未解问题”，再决定是纪实改编还是灵感衍生。
4. 多源输入必须先定权重与主锚点，避免一稿多主。

## Visual Maps

```mermaid
flowchart TD
    A["N1 锁定任务与素材"] --> B["N2 来源归一与抽取事实/画面/情绪"]
    B --> C["N3 锁定事实边界与改编模式"]
    C --> D["N4 放大类型卖点与角色冲突"]
    D --> E["N5 生成章节骨架与节奏表"]
    E --> F["N6 写场景正文"]
    F --> G["N7 注入章末钩子"]
    G --> H["N8 补漫画可视化锚点"]
    H --> I["N9 汇流验收并输出"]
```

```mermaid
flowchart LR
    A["source_type"] --> B{{"类型判型"}}
    B -->|"text"| C["剧情强化改编"]
    B -->|"image"| D["单帧推演改编"]
    B -->|"video"| E["镜头序列改编"]
    B -->|"news_event / hot_search"| F["事实锚定改编"]
    B -->|"mixed"| G["多源归一改编"]
    F --> H{{"truth_boundary"}}
    H -->|"faithful"| I["纪实外壳 + 戏剧组织"]
    H -->|"inspired_by"| J["事实锚点 + 虚构人物线"]
    H -->|"free_reimagining"| K["仅保留议题核与情绪核"]
```

```mermaid
erDiagram
    SOURCE_INPUT ||--|| SOURCE_DIGEST : normalizes
    SOURCE_DIGEST ||--|| ADAPTATION_BRIEF : drives
    ADAPTATION_BRIEF ||--o{ CHAPTER_UNIT : expands
    CHAPTER_UNIT ||--o{ HOOK_ENDING : closes_with
    CHAPTER_UNIT ||--o{ VISUAL_ANCHOR : exposes
    VISUAL_ANCHOR }o--|| COMIC_NOVEL_OUTPUT : supports
```

## Topology Contract (Mandatory)

### Topology Fit

- 单一文本源：串行主干即可。
- 图片/视频源：需要在“来源归一”阶段增加视觉转事件分支。
- 新闻/热搜源：必须在“事实边界”处增加强门禁。
- 多源混合：采用“多源归一 -> 主锚点裁决 -> 统一骨架 -> 汇流验收”。

### Route Priority (Mandatory)

1. 先判定 `source_type`。
2. 再判定 `truth_boundary`。
3. 再判定 `target_genre` 与 `core_sell_point`。
4. 最后才决定章节长度、语言风格与钩子强度。

### Variable Register

| variable | 取值 | 作用 |
| --- | --- | --- |
| `source_type` | `text / image / video / news_event / hot_search / mixed` | 决定素材归一路由 |
| `truth_boundary` | `faithful / inspired_by / free_reimagining` | 决定事实与虚构的分界 |
| `length_target` | `short_burst / mini_serial / medium_arc` | 决定章节数与场景密度 |
| `hook_intensity` | `balanced / strong / relentless` | 决定每章结尾的悬停力度 |
| `impact_density` | `lean / standard / heavy` | 决定高冲击画面候选与大格镜头密度 |
| `delivery_flavor` | `standard_comic / explainer_comic_compatible` | 决定正文是否兼容解说漫旁白朗读 |
| `narration_density` | `lean / standard / rich` | 决定旁白浓度与句长节奏 |
| `output_mode` | `reply_only / full_package` | 决定是仅回复还是附完整桥接包 |

### Scenario Table

| 场景 | 默认路由 | 风险 |
| --- | --- | --- |
| 原文小说/帖文/故事梗概 | 剧情强化改编 | 复述味过重 |
| 一张图/海报/角色照 | 单帧推演改编 | 情节空心化 |
| 短视频/采访/直播片段 | 镜头序列改编 | 时间线混乱 |
| 新闻事件/网络热搜 | 事实锚定改编 | 虚构越界、立场漂移 |
| 多图 + 文本 + 热搜评论 | 多源归一改编 | 多主线互相污染 |

### Strategy Mapping Matrix

| source_type | 第一优先 | 第二优先 | 第三优先 |
| --- | --- | --- | --- |
| `text` | 冲突主线 | 角色欲望 | 章末钩子 |
| `image` | 画面奇点 | 事件前因后果 | 人物关系 |
| `video` | 场景序列 | 情绪推进 | 节点反转 |
| `news_event` | 事实边界 | 公共情绪 | 议题戏剧化 |
| `hot_search` | 爆点命名 | 社会讨论缺口 | 虚构承载角色 |
| `mixed` | 主锚点裁决 | 素材去重归一 | 风格统一 |

## Thinking-Action Node Contract (Mandatory)

每个思行节点都必须回答 6 件事：

| 槽位 | 含义 |
| --- | --- |
| `must_lock` | 本节点必须锁住什么 |
| `actions` | 实际执行动作 |
| `outputs` | 产出什么中间结果 |
| `evidence` | 依据什么做判断 |
| `route_out` | 下一步去哪 |
| `rework_trigger` | 何时返工 |

## Thinking-Action Node Network

| node_id | 状态 | 目标 |
| --- | --- | --- |
| `N1-INTAKE-LOCK` | intake | 锁定任务目标、素材范围与默认输出 |
| `N2-SOURCE-NORMALIZE` | normalize | 把不同来源压成统一素材摘要 |
| `N3-TRUTH-BOUNDARY` | guard | 锁定事实边界、改编模式与禁区 |
| `N4-STORY-ENGINE` | design | 生成人物关系、冲突核、卖点核 |
| `N5-CHAPTER-SCAFFOLD` | structure | 生成章节骨架与节奏表 |
| `N6-SCENE-WRITE` | draft | 写成漫画小说正文 |
| `N7-HOOK-INJECT` | tension | 为每章收束钩子 |
| `N8-VISUAL-READY-POLISH` | bridge | 补足漫画生成所需的视觉锚点 |
| `N9-ACCEPTANCE-GATE` | converge | 验收、返工或交付 |

## Node Execution Playbook (Mandatory)

### Step 1. `N1-INTAKE-LOCK`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | `source_material`、`adaptation_goal`、是否需要落盘 |
| `actions` | 识别来源类型与用户显式限制 |
| `outputs` | `task_brief` |
| `evidence` | 用户原始请求与素材 |
| `route_out` | 完成后进入 `N2` |
| `rework_trigger` | 输入不完整到无法判断来源类型 |

### Step 2. `N2-SOURCE-NORMALIZE`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 来源摘要必须统一为“事实/画面/情绪/关系/未解点” |
| `actions` | 文本抽情节；图片抽前后因；视频抽时间序列；新闻抽事实表 |
| `outputs` | `source_digest` |
| `evidence` | 原材料本体，不引用不存在的细节 |
| `route_out` | 单源直进 `N3`；多源先做主锚点裁决后进 `N3` |
| `rework_trigger` | 抽取结果只剩抽象评价、没有可写场景 |

### Step 3. `N3-TRUTH-BOUNDARY`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | `truth_boundary` 与禁区说明 |
| `actions` | 判断哪些内容可虚构、哪些只能保守转述 |
| `outputs` | `adaptation_mode`、`boundary_note` |
| `evidence` | 来源类型、题材风险、用户限制 |
| `route_out` | 进入 `N4` |
| `rework_trigger` | 把现实事实和虚构情节混成一个口径 |

### Step 4. `N4-STORY-ENGINE`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 主角、对手、欲望、代价、反转潜力 |
| `actions` | 把来源摘要转成可连载的剧情发动机，并预锁高冲击画面候选、氛围压力场与旁白沉浸口径 |
| `outputs` | `adaptation_brief`、`impact_beats`、`voice_brief` |
| `evidence` | 卖点核、情绪核、关系核 |
| `route_out` | 进入 `N5` |
| `rework_trigger` | 只有设定没有冲突，或只有情节没有角色驱动，或读完仍说不出哪几格应该炸开，或旁白读出来会拖、会虚、会绕 |

### Step 5. `N5-CHAPTER-SCAFFOLD`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 章节目标、每章推进点、章末缺口 |
| `actions` | 按长度目标生成章节骨架、场景顺序与冲击镜头落位 |
| `outputs` | `chapter_plan`、`impact_map` |
| `evidence` | 类型节奏、读者期待、后续漫画消费需求 |
| `route_out` | 进入 `N6` |
| `rework_trigger` | 章节互相重复，或章末没有未闭合问题，或高冲击画面全堆在同一区段 |

### Step 6. `N6-SCENE-WRITE`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 正文必须是“可见场景”，不是纯摘要 |
| `actions` | 写对话、动作、环境、冲突升级与情绪推进，并让氛围层服务于可拆镜头的压迫感、翻页张力和旁白朗读时的沉浸声压 |
| `outputs` | `comic_novel_draft` |
| `evidence` | `chapter_plan` 与写作规格 |
| `route_out` | 进入 `N7` |
| `rework_trigger` | 摘要味过重、解释多于场景、画面感不足，或氛围句无法转成可拍摄镜头，或句子朗读时明显啰嗦、泄气 |

### Step 7. `N7-HOOK-INJECT`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 每章结尾必须有明确钩子类型 |
| `actions` | 根据题材匹配钩子，并保留缺口 |
| `outputs` | `hook_pack` |
| `evidence` | 章节冲突峰值与下章期待 |
| `route_out` | 进入 `N8` |
| `rework_trigger` | 把话说完、把真相抖尽、把情绪落死 |

### Step 8. `N8-VISUAL-READY-POLISH`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 角色外观、场景奇点、动作节点、情绪镜头 |
| `actions` | 为后续漫画生成补充视觉桥接层，并明确大格候选、翻页点与冲击画面说明 |
| `outputs` | `visual_bridge` |
| `evidence` | 正文场景与角色行动 |
| `route_out` | 进入 `N9` |
| `rework_trigger` | 读完正文仍无法拆成镜头或页级画面，或无法指出哪几处值得做大格/跨页 |

### Step 9. `N9-ACCEPTANCE-GATE`

| 槽位 | 内容 |
| --- | --- |
| `must_lock` | 是否达到“能追更、能分镜、能继续生成漫画” |
| `actions` | 按评分矩阵验收并给出返工入口 |
| `outputs` | 最终交付与验收结论 |
| `evidence` | Field Master + Pass Table |
| `route_out` | 通过则交付；失败则回到对应节点 |
| `rework_trigger` | 任一关键字段未过验收 |

## Mandatory Workflow

1. 先判型，不直接写。
2. 先归一来源，再做文学化。
3. 先锁定事实边界，再放大戏剧性。
4. 先有章节骨架，再写正文。
5. 先锁高冲击画面候选与翻页停笔点，再细写正文。
6. 每章必须带钩子。
7. 交付前必须补视觉桥接层。

## Atmosphere And Manga Impact Contract (Mandatory)

- 氛围感不是抽象修辞加法，而是正文里的“情绪压力场”；必须能被翻译成光线、声场、距离、物件、湿度、留白和动作停顿。
- 每个核心章节或单章主稿，默认至少预锁以下内容：
  - `3` 处高冲击画面候选
  - `1` 处翻页停笔点
  - `1` 条贯穿性的氛围母题
- 高冲击画面优先落在：异常首次显形、关系突然失衡、真相半揭、危险逼近、代价显影。
- 氛围句若只提升“文气”却不能帮助分镜、构图、明暗或页节奏，一律视为低增益句，必须删改。
- 对恐怖、悬疑、惊悚题材，优先用“声源不见、空间逼仄、物件失常、光线异常、动作迟滞”制造压迫，而不是堆砌抽象形容词。

## Explainer-Comic Compatibility Contract (Mandatory)

- 当 `delivery_flavor=explainer_comic_compatible` 或用户显式要求“解说漫兼容”时，正文必须满足双重消费：
  - 作为漫画母稿时，能稳定拆成镜头、页节奏和视觉冲击点；
  - 作为解说旁白素材时，读出来不拗口、不冗余、有沉浸感。
- 兼容模式不是把正文改成解说提纲，而是把叙述句训练成“可朗读的画面句”。
- 旁白友好最低要求：
  - 单句优先只做一件事。
  - 长句必须能自然断气，避免连续修饰链。
  - 每个关键段至少包含一个可入镜名词和一个推动动作或状态变化。
  - 少用抽象总结句，多用“声场、光线、距离、动作、物件异常”承载情绪。
  - 同一信息不得以“叙述 + 解释 + 感受总结”重复三遍。
- 解说漫兼容时，优先保留以下朗读手感：
  - `短句压迫`
  - `停顿留白`
  - `危险逼近时的节奏收紧`
  - `真相半揭时的半句停笔`
- 若一段文字适合看但不适合念，优先删冗余解释，再调整句长与停顿，而不是牺牲画面。

## Hook Contract (Mandatory)

章末钩子是本技能默认硬门槛。最低要求：

- 每章至少命中一种钩子类型。
- 钩子优先作用在“真相缺口、危险逼近、关系逆转、代价升级”。
- 同一篇稿子不得连续多章使用完全同型钩子而不变化。

钩子类型与例句真源见：

- [references/hook-ending-playbook.md](references/hook-ending-playbook.md)

## Convergence Contract (Mandatory)

最终交付必须汇流成单一口径：

- 来源摘要只保留一份 `source_digest`
- 改编意图只保留一份 `adaptation_brief`
- 正文只保留一份 `漫画小说主稿`
- 视觉桥接只保留一份 `visual_bridge`
- 思行裁决摘要只保留一份精简结论，不外挂第二主稿

## One-Shot Output Contract (Mandatory)

### A. 漫画小说主稿（Mandatory）

当任务允许写盘且用户给出目标目录时，canonical 落点默认：

`<target_root>/漫画小说改编/漫画小说主稿.md`

若用户只要求当前回复交付，则按同样结构直接输出。最低内容要求：

1. 标题
2. 一句话卖点
3. 来源类型与事实边界说明
4. 角色卡
5. 章节正文
6. 每章章末钩子

### B. 漫画桥接包（Mandatory）

当 `output_mode=full_package` 或用户明确要求后续继续做漫画生成时，同时交付：

`<target_root>/漫画小说改编/漫画桥接包.md`

最低内容要求：

1. 章节 -> 场景 -> 视觉锚点索引
2. 角色外观与情绪关键词
3. 关键道具/场景清单
4. 每章推荐钩子类型
5. 高冲击画面候选与推荐大格/翻页点
6. 若启用解说漫兼容：可直接朗读的旁白候选段

### C. 思行裁决摘要（Mandatory, Non-sidecar）

- 必须交代本轮 `source_type`、`truth_boundary`、`target_genre` 与钩子策略。
- 只输出精简裁决摘要，不要求第二份完整推理草稿。

## Quality And Audit Contract

### 评分矩阵

| 维度 | 指标 | 分值 |
| --- | --- | --- |
| 维度0: 契约遵循 | 是否完成来源归一、事实边界、桥接包与钩子合同 | __/10 |
| 维度1 | 来源要点保真度 | __/10 |
| 维度2 | 类型卖点与冲突发动机强度 | __/10 |
| 维度3 | 章节节奏与追更欲 | __/10 |
| 维度4 | 章末钩子有效性 | __/10 |
| 维度5 | 场景可视化程度 | __/10 |
| 维度6 | 漫画下游可消费性 | __/10 |
| 维度7 | 氛围压力场与高冲击画面前置设计 | __/10 |
| 维度8 | 旁白沉浸感与朗读质感 | __/10 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-COMIC-01` | `source_digest` | 把原始素材归一为事实、画面、情绪、关系、未解点 | `S1-S2` | 来源要点保真度 | `FAIL-COMIC-01` |
| `FIELD-COMIC-02` | `boundary_note / adaptation_mode` | 明确事实边界与虚构许可范围 | `S3` | 契约遵循 | `FAIL-COMIC-02` |
| `FIELD-COMIC-03` | `adaptation_brief` | 锁定类型、卖点、主角、对手、欲望与代价 | `S4` | 类型卖点与冲突强度 | `FAIL-COMIC-03` |
| `FIELD-COMIC-04` | `chapter_plan / 漫画小说主稿.md` | 章节推进清晰，正文场景化，可连续追读 | `S5-S7` | 节奏与钩子有效性 | `FAIL-COMIC-04` |
| `FIELD-COMIC-05` | `impact_beats / impact_map` | 预锁高冲击画面候选、氛围母题与翻页停笔点 | `S4-S5` | 氛围与画面冲击力 | `FAIL-COMIC-05` |
| `FIELD-COMIC-06` | `voice_brief / narration_ready_passages` | 正文描述可转为沉浸式旁白，句长与停顿适合朗读 | `S4-S6` | 旁白沉浸感 | `FAIL-COMIC-06` |
| `FIELD-COMIC-07` | `visual_bridge / 漫画桥接包.md` | 角色、场景、动作、道具与大格建议可供后续漫画消费 | `S8` | 下游可消费性 | `FAIL-COMIC-07` |
| `FIELD-COMIC-08` | `final_delivery` | 最终交付结构完整，思行裁决摘要可追溯 | `S9` | 交付完整性 | `FAIL-COMIC-08` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-COMIC-01` | 本轮到底在改编什么 | 锁定目标与素材 | 连素材类型都不清楚就开写 |
| `S2` | `FIELD-COMIC-01` | 来源如何统一成可写基座 | 生成 `source_digest` | 只有形容词，没有事件与关系 |
| `S3` | `FIELD-COMIC-02` | 哪些能虚构，哪些不能 | 写 `boundary_note` | 现实事实与虚构混淆 |
| `S4` | `FIELD-COMIC-03` | 为什么这稿值得追更 | 生成 `adaptation_brief` | 卖点弱、冲突平 |
| `S5` | `FIELD-COMIC-05` | 哪几处必须先被设计成炸点画面 | 生成 `impact_map` | 全文读完没有大格候选 |
| `S6` | `FIELD-COMIC-06` | 正文是否同时具备场景感与朗读感 | 写正文场景并压实朗读节奏 | 画面有了但念出来拖沓 |
| `S7` | `FIELD-COMIC-04` | 结尾有没有把缺口留住 | 注入 `hook_pack` | 章节收得太满 |
| `S8` | `FIELD-COMIC-07` | 下游能否直接继续做漫画 | 生成 `visual_bridge` | 无法拆角色/场景/动作锚点 |
| `S9` | `FIELD-COMIC-08` | 当前交付是否达到闭环 | 验收并决定返工 | 只有文案，没有验收口径 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-COMIC-01` | `source_digest` 同时覆盖事实、画面、情绪、关系、未解点 | `FAIL-COMIC-01` | `S1-S2` |
| `FIELD-COMIC-02` | 事实边界明确，现实事实不被伪造 | `FAIL-COMIC-02` | `S3` |
| `FIELD-COMIC-03` | 改编摘要能说明类型、卖点、冲突与代价 | `FAIL-COMIC-03` | `S4` |
| `FIELD-COMIC-04` | 章节推进清楚、正文场景化、章末有钩子 | `FAIL-COMIC-04` | `S6-S7` |
| `FIELD-COMIC-05` | 预锁的冲击画面、氛围母题与翻页点足够明确 | `FAIL-COMIC-05` | `S4-S5` |
| `FIELD-COMIC-06` | 正文可抽出精炼旁白段，朗读时不啰嗦不泄气 | `FAIL-COMIC-06` | `S4-S6` |
| `FIELD-COMIC-07` | 桥接包足以支持角色/场景/分镜继续加工 | `FAIL-COMIC-07` | `S8` |
| `FIELD-COMIC-08` | 主稿、桥接层与思行裁决摘要口径一致 | `FAIL-COMIC-08` | `S9` |

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修源层合同，再决定是否只改局部文案：

- 文本改编仍像摘要，不像漫画小说。
- 图片/视频改编后没有形成冲突链。
- 新闻/热搜改编把虚构写成事实。
- 章节结尾把话说完，没有钩子。
- 正文能读但不能拆成后续漫画场景。
- 氛围层写得很满，但没有提前服务漫画页级冲击。
- 正文画面很强，但旁白念出来发虚、发绕、发满。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/comic/漫画小说改编/CONTEXT.md`
  - `.agents/skills/comic/漫画小说改编/references/source-intake-and-mode-selection.md`
  - `.agents/skills/comic/漫画小说改编/references/hook-ending-playbook.md`
  - `.agents/skills/comic/漫画小说改编/references/hotsearch-news-adaptation.md`
- `Meta Rule Source`
  - `/Volumes/AIGC/AIGC-DREAM- MAKER/AGENTS.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-知行合一/SKILL.md`

用户闭环输出固定三段：

1. 根因位置
2. 立即修复
3. 系统预防修复

## SKILL / CONTEXT 分工（Mandatory）

- `SKILL.md` 负责：触发条件、来源判型、思行网络、字段真源、输出合同与验收门。
- `CONTEXT.md` 负责：来源类型坑点、钩子强化经验、热门题材 heuristics、失败修复与成功抽象。

## Completion Criteria

满足以下条件才算完成：

- 已锁定来源类型与事实边界。
- 已把素材改造成章节化、场景化、强钩子化的漫画小说底稿。
- 已生成足够继续做漫画生成的视觉桥接层。
- 已给出思行裁决摘要与验收结论。
