---
name: comic-nine-blade-prompts
description: Use when 上游漫画小说或用户指定小说需要被蒸馏为一次 Seedream 连续生成 9 张漫画页的结构化长提示词 JSON，尤其适合要固定角色、跨页叙事、漫画格布局、对白/旁白/独白/SFX 文本规范的场景。
governance_tier: full
---

# 九刀流漫画提示词

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 定位

本技能把上游 `1-漫画小说改编` 的小说底稿、漫画桥接包，或用户直接提供的任意小说片段，转成可被下游 `3-漫画生成` 消费的 `nine_blade_comic_prompts.v1` JSON。

核心目标不是写 9 个互不相关的文生图 prompt，而是生成一份**单次 Seedream 连续多图请求**可理解的九页漫画提示词包：

- 一次固定 9 张图。
- 每张图是一页竖版 9:16 漫画页。
- 每页内部必须是 2-5 个 panels，默认 3 panels。
- 禁止把某一页退化成单幅海报、单镜头插画或无分格整页图；即使使用 splash 主格，也必须保留至少一个辅助格形成“多格漫画页”。
- 九页之间是连续连环画画面，不是同一画面九个版本。
- 最终 JSON 必须足够让 `3-漫画生成` 合成一个单请求 master prompt。

## 2. 业务需求分析合同

| analysis_field | 必须锁定的问题 | 默认策略 |
| --- | --- | --- |
| `business_goal` | 输出服务什么动作 | 服务 Seedream 一次生成 9 张连续漫画页 |
| `business_object` | 输入是什么 | 上游漫画小说 / 用户小说 / 片段摘要 / 漫画桥接包 |
| `source_format_profile` | 原始小说源属于哪种叙事密度 | 先判定 `scene-led / explainer-led / compare`，再决定格式化路径 |
| `success_criteria` | 什么叫成功 | 9 页连续、群像角色可区分且一致、场景锚点稳定、每页漫画感强、右下角带纯数字页码、可被下游脚本校验 |
| `constraint_profile` | 哪些约束不可破 | 禁止九宫格拼图；禁止同一图九变体；固定 9:16；固定 9 页 |
| `topology_fit` | 最佳思行结构 | 先做小说来源格式化前奏，再切剧情九刀，再并行锁角色/风格/文字系统，最后汇流为 JSON |
| `step_strategy` | 重点在哪 | 原始小说整形、页级剧情切分、犀利全局漫画风格、经典漫画版式轮换、跨页一致性、Seedream 单请求兼容 |

## 3. Context Preload

- 每次使用先读取同目录 `CONTEXT.md`。
- 复杂提示词结构细则读取 [references/nine-blade-prompt-contract.md](references/nine-blade-prompt-contract.md)。
- 输出 JSON 必须遵守 [templates/nine-blade-comic-prompts.schema.json](templates/nine-blade-comic-prompts.schema.json)。
- 可从 [templates/nine-blade-template.json](templates/nine-blade-template.json) 复制骨架后填充。

## 4. 总输入合同

### 必需输入

- `source_novel`
  - 上游漫画小说正文、用户指定小说、或足够完整的情节片段。

### 可选输入

- `comic_bridge_pack`
  - 上游输出的角色、场景、道具、冲击画面候选、旁白密度等桥接信息。
- `formatted_source_novel`
  - 若上游已经提供格式化好的小说源包，可作为前奏跳过候选；但仍必须先通过本技能的来源格式化验证门，不能盲信。
- `style_profile`
  - 默认 `cinematic_comic_realism`，可指定国风连环画、美漫电影感、韩漫、暗黑写实等。
- `text_language`
  - 默认 `zh-CN`。
- `page_count`
  - 固定为 `9`，不得因内容少而减少。
- `page_aspect_ratio`
  - 固定为 `9:16`。
- `output_path`
  - 若用户未指定且当前任务是单集/单回项目，默认写到 `projects/comic/[项目名]/2-九刀流漫画提示词/nine_blade_comic_prompts.json`。
  - 若用户未指定且当前项目已明确进入多集执行（例如用户说“第2集 / 第3集”或阶段目录里已存在其他集产物），必须启用集级防覆盖命名，默认写到 `projects/comic/[项目名]/2-九刀流漫画提示词/第N集-nine_blade_comic_prompts.json`。
  - 同轮产出的 `formatted_source_novel` 与思考摘要也应使用同一集级前缀：`第N集-formatted_source_novel.json`、`第N集-思考过程摘要.md`。

### 派生中间真源

- `formatted_source_novel`
  - 这是本技能的强制前奏产物，也是九刀主流程的唯一上游文本真源。
  - 若用户未显式提供，必须由本技能先从 `source_novel` 生成。
  - 若用户已提供，仍必须先校验其字段齐备和可切九刀性，才能进入主流程。

推荐至少包含：

- `source_format_variant`
- `canonical_story_summary`
- `ordered_story_units[]`
- `character_seed_roster[]`
- `scene_seed_roster[]`
- `continuity_alerts[]`
- `blade_ready_notes`

### 小说来源格式化前奏合同

硬规则：

1. 任意 `source_novel` 都不得直接进入 `N2-STORY-BLADES`。
2. 必须先经过“来源格式化前奏”，把原始文本归一为 `formatted_source_novel`。
3. 前奏处理机制参照 `.agents/skills/aigc/1-Planning/2-格式` 的思路：先 intake，再 business analyze，再 route，再整形，再 normalize，再 validate。
4. 前奏只服务“把原始小说变成可切九刀的标准化输入”，不输出第二份 canonical 成品，不与最终 JSON 竞争真源。
5. 若原始小说是章节正文、对话体、梗概、简介、剧情摘要或混合文本，必须先判定为：
   - `scene-led`：场景动作充足，优先保留戏剧性切块。
   - `explainer-led`：概述/解说密度高，优先压成可视化事件单元。
   - `compare`：无法稳定判断时，内部比较两种整形路径后只保留一份 canonical handoff。
6. 只有 `formatted_source_novel` 通过前奏验证后，当前九刀配置才允许开始。

## 5. 思行网络

本技能采用“来源格式化前奏 + 串行剧情主干 + 三支路漫画语法并行 + 汇流校验”的思行网络。原始小说先被格式化为 `formatted_source_novel`；只有前奏验证通过，才允许切 9 个页级刀口。角色连续性完成后，风格锐化、版式轮换、文字系统三条支路可并行设计，但必须在 `N4G-COMIC-GRAMMAR-MERGE` 汇流后才允许写 page prompts。

```mermaid
flowchart TD
    A["P1-SOURCE-INTAKE<br/>锁原始小说输入与边界"] --> B["P2-SOURCE-ANALYZE<br/>判密度/视角/可视化程度"]
    B --> C{"P3-SOURCE-ROUTE<br/>scene-led / explainer-led / compare"}
    C -->|"scene-led"| D1["P4S-SCENE-LED-FORMAT<br/>保留场景/动作/对白块"]
    C -->|"explainer-led"| D2["P4E-EXPLAINER-LED-FORMAT<br/>压缩概述为事件单元"]
    C -->|"compare"| D3["P4C-COMPARE-FORMAT<br/>双路比较后择一"]
    D1 --> E["P5-SOURCE-NORMALIZE<br/>统一为 formatted_source_novel"]
    D2 --> E
    D3 --> E
    E --> F{"P6-SOURCE-VALIDATE<br/>可切九刀? 连续性齐备?"}
    F -->|"pass"| G["N1-INTAKE<br/>锁目标/风格/输出路径"]
    F -->|"fail"| C
    G --> H["N2-STORY-BLADES<br/>基于 formatted_source_novel 切九刀"]
    H --> I["N3-CONTINUITY<br/>锁角色/场景/道具连续性"]
    I --> J1["N4A-STYLE-SHARPEN<br/>全局漫画风格锐化词"]
    I --> J2["N4B-LAYOUT-DIVERSIFY<br/>经典版式轮换"]
    I --> J3["N4C-TEXT-SYSTEM<br/>对白/旁白/独白/SFX 槽"]
    J1 --> K["N4G-COMIC-GRAMMAR-MERGE<br/>漫画语法汇流门"]
    J2 --> K
    J3 --> K
    K --> L["N5-PAGE-PROMPTS<br/>逐页生成 prompt/panels/text_slots"]
    L --> M["N6-ASSEMBLY<br/>组装 nine_blade_comic_prompts.v1"]
    M --> N{"N7-VALIDATE<br/>schema + 风格 + 版式门禁"}
    N -->|"pass"| O["N8-HANDOFF<br/>交付 JSON + 思考过程"]
    N -->|"fail: source"| C
    N -->|"fail: story"| H
    N -->|"fail: style/layout/text"| K
    N -->|"fail: structure"| M
```

```mermaid
flowchart LR
    A["N7 failure"] --> B{{"失败类型"}}
    B -->|"FAIL-NB-SOURCE-ROUTE"| C["回 P3<br/>重做来源判模"]
    B -->|"FAIL-NB-SOURCE-FORMAT"| D["回 P4/P5<br/>重整 source units"]
    B -->|"FAIL-NB-SOURCE-COVERAGE"| E["回 P6<br/>补连续性/转场/视觉钩子"]
    B -->|"FAIL-NB-BEATS"| F["回 N2<br/>重切 story_beat_map"]
    B -->|"FAIL-NB-LOCKS"| G["回 N3<br/>补角色/场景/道具锁"]
    B -->|"FAIL-NB-STYLE"| H["回 N4A<br/>补 manga_style_keywords"]
    B -->|"FAIL-NB-LAYOUT-DIVERSITY"| I["回 N4B<br/>重排 layout_id/panel_ratios"]
    B -->|"FAIL-NB-TEXT"| J["回 N4C<br/>压短文字槽"]
    B -->|"FAIL-NB-PAGES"| K["回 N5<br/>补 panels/positive_prompt"]
    B -->|"FAIL-NB-CONTRACT/STRUCTURE"| L["回 N6<br/>修 JSON 合同"]
```

```mermaid
stateDiagram-v2
    [*] --> SourceIntake
    SourceIntake --> SourceAnalyzed
    SourceAnalyzed --> SourceRouted
    SourceRouted --> SourceFormatted
    SourceFormatted --> SourceValidated
    SourceValidated --> CoreIntake
    CoreIntake --> BladesReady: N2 pass
    BladesReady --> ContinuityReady: N3 pass
    ContinuityReady --> ComicGrammarFork: enter N4A/N4B/N4C
    ComicGrammarFork --> GrammarMerged: style + layout + text pass
    GrammarMerged --> PagePromptsReady: N5 pass
    PagePromptsReady --> JsonAssembled: N6 pass
    JsonAssembled --> Validated: N7 pass
    JsonAssembled --> Rework: N7 fail
    Rework --> SourceRouted: source fail
    Rework --> BladesReady: story fail
    Rework --> ComicGrammarFork: style/layout/text fail
    Rework --> JsonAssembled: structure fail
    Validated --> HandedOff
    HandedOff --> [*]
```

```mermaid
erDiagram
    SOURCE_NOVEL ||--|| FORMATTED_SOURCE_NOVEL : normalizes_to
    FORMATTED_SOURCE_NOVEL ||--o{ STORY_UNIT : contains
    FORMATTED_SOURCE_NOVEL ||--|| STORY_BEAT_MAP : distills
    COMIC_BRIDGE_PACK ||--o{ CHARACTER_LOCK : supplies
    COMIC_BRIDGE_PACK ||--o{ LOCATION_LOCK : supplies
    STORY_BEAT_MAP ||--o{ PAGE_PROMPT : drives
    MANGA_STYLE_BIBLE ||--o{ PAGE_PROMPT : sharpens
    LAYOUT_PLAN ||--o{ PAGE_PROMPT : structures
    CHARACTER_LOCK ||--o{ PANEL_PROMPT : constrains
    COMIC_TEXT_SYSTEM ||--o{ TEXT_SLOT : labels
    PAGE_PROMPT ||--o{ PANEL_PROMPT : contains
    PANEL_PROMPT ||--o{ TEXT_SLOT : contains
    PAGE_PROMPT }o--|| NINE_BLADE_JSON : assembles
```

```mermaid
flowchart TD
    A0["前奏验证门 P6"] --> B0{{"formatted_source_novel 是否齐备?"}}
    B0 -->|"chronology / story_units / scene seeds 缺失"| C0["阻断 N2<br/>回 P3-P5"]
    B0 -->|"visual hooks / transition coverage 不足"| D0["阻断 N2<br/>补来源格式化"]
    B0 -->|"全部通过"| E0["允许进入 N2"]
```

```mermaid
flowchart TD
    A["字段汇流门 N4G"] --> B{{"三支路是否齐备?"}}
    B -->|"style_bible 缺漫画锐化词"| C["阻断 N5<br/>补 N4A"]
    B -->|"style_bible 缺全局风格锁 / 易跨页漂移"| C
    B -->|"layout_plan 少于 5 种布局"| D["阻断 N5<br/>补 N4B"]
    B -->|"动态布局少于 3 类"| D
    B -->|"text_slots 未分型或过长"| E["阻断 N5<br/>补 N4C"]
    B -->|"全部通过"| F["允许 N5 写 9 页 prompt"]
    F --> G["N7 validator<br/>脚本复核同一门禁"]
```

## 6. 思行节点表

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `P1-SOURCE-INTAKE` | 锁定原始小说输入与边界 | `source_novel`、`formatted_source_novel`、`comic_bridge_pack`、用户要求 | 读取原始小说或已格式化源；识别来源类型、长度、章节边界、可复用桥接信息 | 输入摘要、来源类型、原始边界说明 | pass -> `P2`；输入不足 -> 要求补源 | 原始输入可被归类 |
| `P2-SOURCE-ANALYZE` | 完成来源格式化前的业务分析 | `P1` 输出 | 提炼叙事密度、对白占比、概述占比、视角稳定性、时间线清晰度、可视化程度 | source brief、风险卡 | pass -> `P3` | 已明确该用哪种格式化路径 |
| `P3-SOURCE-ROUTE` | 做来源格式化判模 | `P2` 输出 | 裁决 `scene-led / explainer-led / compare`，默认优先 `scene-led`，信息过密或摘要化文本才切 `explainer-led` | `source_format_variant`、route evidence | `scene-led -> P4S`；`explainer-led -> P4E`；`compare -> P4C` | 只允许一个 canonical handoff |
| `P4S-SCENE-LED-FORMAT` | 整形场景驱动小说源 | 原始章节、对白、动作、桥接包 | 保留场景动作与对白块，压缩赘述，抽出可切页的事件单元与视觉钩子 | scene-led source units | pass -> `P5` | 场景/动作可被九刀复用 |
| `P4E-EXPLAINER-LED-FORMAT` | 整形概述驱动小说源 | 梗概、简介、摘要、旁白化文本 | 将摘要压成顺时序事件单元，补齐人物、场景、转场与视觉化动作，不把长段概述直接丢进九刀 | explainer-led source units | pass -> `P5` | 事件单元足够 sceneable |
| `P4C-COMPARE-FORMAT` | 在歧义输入上内部比较双路格式化 | 原始文本、bridge pack | 同时试跑两路整形，比较哪一路更利于九刀切页与连续性；只保留一份 canonical handoff | compare verdict、selected packet | pass -> `P5` | 不产生双 canonical 真源 |
| `P5-SOURCE-NORMALIZE` | 统一归一为 `formatted_source_novel` | `P4S/P4E/P4C` 输出 | 组装 `canonical_story_summary`、`ordered_story_units[]`、`character_seed_roster[]`、`scene_seed_roster[]`、`continuity_alerts[]`、`blade_ready_notes` | `formatted_source_novel` | pass -> `P6` | 字段齐备且顺序稳定 |
| `P6-SOURCE-VALIDATE` | 验证格式化源是否可切九刀 | `formatted_source_novel` | 检查时间线、角色出场链、场景回指、视觉钩子、转场覆盖、高潮可切性；必要时回退补齐 | source validation verdict | pass -> `N1`；fail -> `P3/P4/P5` | 只有通过后才允许进入九刀主流程 |
| `N1-INTAKE` | 锁定目标、风格、输出路径 | `formatted_source_novel`、`comic_bridge_pack`、用户风格要求 | 读取格式化小说源与桥接包；锁项目名、输出路径、风格边界 | intake 摘要、项目名、输出路径、风格约束 | pass -> `N2` | 进入主流程时不再读取 raw source 作为主真源 |
| `N2-STORY-BLADES` | 切出 9 个页级剧情刀口 | `formatted_source_novel.ordered_story_units[]`、视觉锚点、章节钩子 | 生成 `story_beat_map[9]`，每页有动作、情绪、悬念和不同叙事功能 | `story_beat_map`、每页 `page_role` | pass -> `N3`；情节不足 -> 扩写过渡页；过密 -> 合并解释保留动作 | 9 页不重复、不跳戏 |
| `N3-CONTINUITY` | 锁角色、场景、道具和世界观一致性 | `story_beat_map`、桥接包角色/场景/道具 | 先确定唯一 `main_character_lock`，再写具名 `character_locks`、`scene_continuity_bible.scene_locks` 与每页 `active_character_ids / scene_id`，提炼跨页复用短语 | 主角锚定锁、群像角色锁、场景锁、道具锁 | pass -> `N4A/N4B/N4C`；漂移风险高 -> 回桥接包补锁 | 主角外观、配角识别物与场景地标都可逐页复用 |
| `N4A-STYLE-SHARPEN` | 锁全局犀利漫画风格 | 题材、目标画风、连续性锁 | 写 `style_bible.manga_style_keywords / layout_directive / genre_style_keywords`，并额外锁定同一轮 9 页共享的 `global style anchor`：同一渲染媒介、线条体系、明暗体系、上色策略、lettering 质感、panel border 质感与角色年龄比例；同时写明 `forbidden style shifts`，避免只有泛影视词 | `style_bible` 中的漫画语法词 + 风格锁定语句 + 禁止漂移清单 | pass -> `N4G`；风格泛化或存在页间漂移风险 -> 补 reference 风格词库与风格锁 | 至少命中漫画页、ink/line、gutter/panel/SFX 等风格语法，且能明确阻止跨页切换成儿童绘本、Q 版、影视概念图或不同渲染媒介 |
| `N4B-LAYOUT-DIVERSIFY` | 锁 9 页经典漫画版式轮换 | `story_beat_map`、冲击页、解释页、过渡页 | 为每页分配 `layout_id / panel_count / panel_ratios`，轮换 splash、inset、diagonal、split、border-breaking、zigzag 等 | `layout_plan`、每页 layout | pass -> `N4G`；平整化 -> 重排高冲击页和过渡页 | 至少 5 个 layout_id，动态布局不少于 3 类 |
| `N4C-TEXT-SYSTEM` | 锁文字槽位与漫画文字表现 | 剧情信息量、对白/旁白/SFX 需求 | 把解释压进 caption，把动作声压进 SFX，把对白压短并绑定气泡类型 | `comic_text_system`、每页 text slot 策略 | pass -> `N4G`；文字过长 -> 压缩/转旁白 | 每个文字槽类型明确，中文短句可读 |
| `N4G-COMIC-GRAMMAR-MERGE` | 汇流漫画语法三支路 | `style_bible`、`layout_plan`、`comic_text_system` | 检查三支路是否齐备，阻断缺失支路，形成 page prompt 写作策略；额外做一次“页间风格漂移预判”：确认 9 页只允许布局和情绪变化，不允许渲染媒介、线稿密度、角色年龄比例、色彩系统发生断层式切换 | 汇流摘要、风险清单、style drift 预判结论 | pass -> `N5`；fail -> 对应回 `N4A/N4B/N4C` | 风格、版式、文字三个门禁同时通过，且页间风格锁稳定 |
| `N5-PAGE-PROMPTS` | 写 9 个完整页 prompt | `story_beat_map`、主角锚定锁、群像角色锁、场景锁、风格词、layout plan、文字系统、页码覆盖层 | 为每页写 `positive_prompt / panels / text_slots`，prompt 固定顺序必须为：`版式 -> 全局 style anchor -> 主角锚定 -> 群像锚定 -> 场景锚定 -> 页码 -> 一致性语义 -> panel 动作 -> 文字可读性/字型规则 -> overall mood`。每页都必须重复同一套全局 style anchor，禁止把风格锁只放在顶层 `style_bible` 里隐含表达 | 9 个 page objects | pass -> `N6`；缺页、缺 panel 或风格锁未逐页注入 -> 回本节点 | 每页含 9:16、独立页、非拼图约束、漫画版式、全局风格锁、主角锚定语句、群像可区分语句、场景锚定语句、右下角数字页码 |
| `N6-ASSEMBLY` | 汇流为 `nine_blade_comic_prompts.v1` JSON | 9 个 page objects、schema、模板 | 按 schema 填充顶层合同、style、locks、pages、negative prompt | JSON 文件 | pass -> `N7`；结构缺失 -> 本节点修复 | JSON 可解析且字段齐 |
| `N7-VALIDATE` | 脚本与人工双门验收 | JSON 文件、validator、reference 门禁 | 运行 validator；检查 9 页、风格词、layout 多样性、文字系统、负向提示词 | validator 输出、人工风险摘要 | pass -> `N8`；fail -> 按失败码回对应节点 | 可被 3 号技能消费 |
| `N8-HANDOFF` | 交付下游生成所需真源 | 已验证 JSON、思考过程摘要、输出路径 | 单集项目写入 `projects/comic/[项目名]/2-九刀流漫画提示词/nine_blade_comic_prompts.json`；多集项目默认写入 `projects/comic/[项目名]/2-九刀流漫画提示词/第N集-nine_blade_comic_prompts.json`，并同步落盘 `第N集-formatted_source_novel.json` 与 `第N集-思考过程摘要.md` | 最终 JSON、思考过程 | 完成或交给 3 号技能 | 当前集 canonical JSON 唯一且不覆盖其他集 |

## 7. 输出合同

最终输出为一个 JSON 对象，禁止只输出散文式 prompt。推荐文件名：

```text
nine_blade_comic_prompts.json
```

若项目已进入多集模式，推荐文件名自动升级为：

```text
第N集-nine_blade_comic_prompts.json
```

最小结构：

```json
{
  "schema_version": "nine_blade_comic_prompts.v1",
  "generation_contract": {
    "provider": "seedream",
    "call_mode": "single_request_sequential",
    "image_count": 9,
    "page_aspect_ratio": "9:16"
  },
  "main_character_lock": {},
  "scene_continuity_bible": {},
  "style_bible": {},
  "character_locks": [],
  "comic_text_system": {},
  "pages": [],
  "global_negative_prompt": ""
}
```

输出同时附 `思考过程`，只说明切页理由、版式策略和关键风险，不输出冗长推理草稿。

## 8. 版式与文字硬规则

- 页面级：每个 `page.positive_prompt` 必须写明 `vertical 9:16 comic page`。
- 分格级：每一页必须明确要求 `multiple comic panels`，且 `layout.panel_count >= 2`；禁止任何单格整页输出。
- 主角锚定级：顶层必须存在唯一 `main_character_lock`。它不是普通角色表，而是九页连续生成的第一视觉锚点。即使是群像戏，也必须先选一个当前段落的主要角色作为锚点，其余角色继续放入 `character_locks`。
- `main_character_lock.anchor_prompt` 推荐直接采用高密度英文锚定句，参考格式：

```text
Character locked across all panels: Sun Wukong, a muscular monkey demon, covered in golden fur, a pronounced thunder-god mouth, sunken eyes with bright golden pupils, no eyebrows, sharp fangs visible, wearing a tattered grey-brown Daoist novice robe, realistic fur and muscle anatomy, consistent face, costume, silhouette and color palette in every panel and every page.
```

- `main_character_lock.anchor_prompt` 必须同时包含：角色名、物种/身份、体型或轮廓、脸部识别特征、服装、关键材质/色彩、以及 `consistent face / costume / silhouette / color palette` 一类稳定语义。不得只写“主角保持一致”这种空泛话。
- 群像协同级：`character_locks` 不能再只是松散角色表。每个 recurring character 必须具备 `character_id / name / anchor_prompt`，并在对应页通过 `pages[].active_character_ids` 显式声明出场。若某页出现两名及以上 recurring characters，`page.positive_prompt` 必须点名这些角色，并要求他们 `visually consistent and clearly distinguishable`，避免模型把多人页压成主角 + 模糊路人。
- 场景锚定级：顶层必须存在 `scene_continuity_bible`，其中 `scene_locks[]` 至少包含 `scene_id / name / anchor_prompt`。每页必须通过 `pages[].scene_id` 绑定一个场景锁，并在 `page.positive_prompt` 中显式注入该场景名与稳定语义，例如 `consistent architecture / landmark props / lighting / spatial geography`。不得只写抽象的“保持场景一致”。
- 连续性级：每个 `page.positive_prompt` 必须在版式说明之后、具体动作之前，固定写入“保持角色和场景一致性”的等价语义。英文推荐短语为 `keep character and scene consistency across all pages`，可按语境改写为 `consistent character appearance and consistent scene/location continuity across all pages`，但不得只依赖 `character_locks` 或 `location_locks` 字段隐含表达。
- 页码级：每页必须存在 `page_number_overlay`，且 `text` 必须等于该页页码的纯数字字符串，取值严格为 `"1"` 到 `"9"`。位置固定 `bottom-right`，并在 `page.positive_prompt` 中显式写入 `place page number "N" in the bottom-right corner, digits only` 或等价语义。页码不得写中文、不得加 `Page` 前缀、不得放在其他角落。
- 注入顺序级：每个 `page.positive_prompt` 的推荐固定顺序为：`vertical 9:16 comic page` -> `layout grammar` -> `global style anchor / forbidden style shifts` -> `main_character_lock.anchor_prompt` -> `active character anchors / clearly distinguishable ensemble rule` -> `scene lock anchor` -> `page_number_overlay rule` -> `keep character and scene consistency across all pages` -> `panel actions / text slots / overall mood`。全局风格锁与主角锚定句都不得被挪到 prompt 末尾。
- 全局风格级：`style_bible` 必须包含能显著推动漫画感的锐化词组，优先写入 `manga_style_keywords` 或等价字段，例如：`dynamic manga paneling`、`dramatic inked line art`、`screentone shadows`、`high contrast black gutters`、`oversized SFX`、`cinematic page composition`。
- 全局风格锁定级：除 `manga_style_keywords` 外，`style_bible` 还应明确写出一条不可跨页漂移的 `style anchor`，至少锁住：
  - 同一套渲染媒介与完成度，例如“重墨线稿 + screentone + 有限上色”或“轻水墨线描 + 低饱和铺色”，而不是有时黑白港漫、有时儿童彩图、有时影视概念图。
  - 同一套线条粗细与明暗方法，例如 `heavy ink contour + black shadow masses` 或 `clean brush contour + airy negative space`。
  - 同一套角色年龄比例和造型语法，避免一页少年写实、一页 Q 版、一页卡通幼态。
  - 同一套 lettering 和 panel border 质感，避免页面之间像不同作品拼盘。
  - 一条 `forbidden style shifts` 语句，明确禁止 `chibi / SD / children picture-book / painterly concept art / 3D render / live-action storyboard / random full-color realism` 这类断层切换。
- 风格稳定性级：9 页允许变化的是剧情功能、构图、镜头远近、情绪强弱与版式；不允许变化的是全局视觉 DNA。本规则优先级高于“某页看起来更华丽”。
- 版式级：9 页必须轮换经典漫画布局，不得全部采用从上到下的平整条带；默认至少 5 个不同 `layout_id`，并至少包含 3 类动态布局：`splash-with-insets`、`diagonal-cut-action`、`split-diopter-page`、`border-breaking-cliffhanger`、`vertical-cascade`、`impact-sfx-page` 等。
- 每页 `positive_prompt` 必须先说明页面版式，再写角色/动作；禁止只写“cinematic shot”而缺少 panel grammar。
- 单次生成级：顶层 `generation_contract.hard_constraints` 必须包含：
  - `Generate exactly 9 separate images/pages.`
  - `Do not create a nine-grid collage.`
  - `Do not create nine variations of the same scene.`
  - `Every page must contain multiple comic panels, never a single full-page illustration.`
  - `Keep character and scene consistency across all pages.`
  - `Place a small page number in the bottom-right corner of every page, using digits 1-9 only.`
- 文字系统：
  - 顶层 `comic_text_system` 必须完整声明 `dialogue / narration / inner_monologue / sfx` 四类文字系统。
  - 每个文字系统对象至少包含：`visual_form / placement_rule / legibility_rule / max_chars`。
  - 推荐固定上限：`dialogue.max_chars = 18`、`narration.max_chars = 24`、`inner_monologue.max_chars = 20`、`sfx.max_chars = 6`。
  - 九页整体默认必须覆盖四类文字槽至少各一次，不得退化成只有旁白、没有对白/独白/SFX 的说明文式输出。
  - 每个 `text_slot` 至少包含：`type / text / placement / bubble_style / inside_panel`。
  - `dialogue` 与 `inner_monologue` 额外必须包含 `speaker_id`，且 `speaker_id` 必须属于当前页 `active_character_ids`。
  - 对白：`speech bubble`，短句，放角色附近。
  - 旁白：`rectangular caption box`，放页边或 panel 边缘。
  - 内心独白：`thought bubble` 或 `inner monologue caption`，与对白区分。
  - 音效：`large hand-lettered SFX`，作为画面元素，不替代对白。
- 中文文字必须使用 `clear legible Chinese text`，每个气泡不宜超过 18 个汉字。
- 每页 `positive_prompt` 必须显式注入文字可读性与文字形态语义；当该页含 `dialogue / narration / inner_monologue / sfx` 时，prompt 中必须能读到对应的 `speech bubble / caption box / thought bubble or inner caption / integrated hand-lettered SFX` 约束，而不是只把这些信息留在结构字段里。

## 9. 字段映射

| field_id | 输出位置/字段 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `FIELD-NB-01` | `formatted_source_novel.source_format_variant` | 原始小说已被裁决为 `scene-led / explainer-led / compare -> selected` 之一 | `FAIL-NB-SOURCE-ROUTE` |
| `FIELD-NB-02` | `formatted_source_novel` | 含 `canonical_story_summary / ordered_story_units[] / character_seed_roster[] / scene_seed_roster[] / continuity_alerts[] / blade_ready_notes`，可直接服务九刀切页 | `FAIL-NB-SOURCE-FORMAT` |
| `FIELD-NB-03` | `formatted_source_novel.ordered_story_units[]` | 时间线、转场、视觉钩子、高潮与余波覆盖充分 | `FAIL-NB-SOURCE-COVERAGE` |
| `FIELD-NB-04` | `generation_contract` | 固定 9 张、9:16、single_request_sequential | `FAIL-NB-CONTRACT` |
| `FIELD-NB-05` | `story_beat_map` | 9 个连续页级剧情刀口 | `FAIL-NB-BEATS` |
| `FIELD-NB-06` | `main_character_lock` | 唯一主要角色锚定对象，含 `name` 与高密度 `anchor_prompt` | `FAIL-NB-MAIN-LOCK` |
| `FIELD-NB-07` | `scene_continuity_bible` | 具名场景锁完整，含 `scene_locks[]` 与稳定地标/光线/空间语义 | `FAIL-NB-SCENE-LOCK` |
| `FIELD-NB-08` | `character_locks` | 其他跨页角色外观、服装、关键识别物稳定，且具名可回指 | `FAIL-NB-LOCKS` |
| `FIELD-NB-09` | `comic_text_system` | 四类文字系统齐备；每类含 `visual_form / placement_rule / legibility_rule / max_chars`；九页整体至少覆盖一次 | `FAIL-NB-TEXT` |
| `FIELD-NB-10` | `pages[]` | 恰好 9 页；每页含 panel 布局、prompt、文本槽、`active_character_ids`、`scene_id`、`page_number_overlay`，且 `positive_prompt` 显式包含主角锚定语句、群像区分语义、场景锚定语义与右下角数字页码语义 | `FAIL-NB-PAGES` |
| `FIELD-NB-11` | `global_negative_prompt` | 禁止拼图、变体、文字错误、错手、logo、水印 | `FAIL-NB-NEGATIVE` |
| `FIELD-NB-12` | `style_bible` | 全局漫画风格锐化词明确，不能只有泛影视词 | `FAIL-NB-STYLE` |
| `FIELD-NB-13` | `pages[].layout` | 9 页 layout_id 足够多样，动态版式不少于 3 类 | `FAIL-NB-LAYOUT-DIVERSITY` |
| `FIELD-NB-14` | `style_bible + pages[].positive_prompt` | 9 页共享同一套全局视觉 DNA；每页都显式重复 style anchor，禁止跨页切换成儿童绘本、Q 版、影视概念图或不同渲染媒介 | `FAIL-NB-STYLE-DRIFT` |

## 10. 验证

```bash
python3 .agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py \
  path/to/nine_blade_comic_prompts.json
```

提交前还必须做前奏侧人工验证：

- `formatted_source_novel` 是否已覆盖开场、触发、阻力、代价、迁移、危机、生死瞬间、反击、余波等可切页节点。
- `ordered_story_units[]` 是否存在明确转场和视觉钩子，而不是连续抽象概述。
- 是否仍有关键角色、关键场景或高潮因原始文本松散而在前奏中丢失。

## 11. Root-Cause 合同

若下游生成出九宫格拼图、九张近似变体、角色漂移、文本槽混乱或 JSON 无法被 3 号技能读取，必须按以下链路上溯：

`Symptom -> Direct Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

- `Rule Source`：本 `SKILL.md`、`references/nine-blade-prompt-contract.md`、来源格式化前奏合同、schema、验证脚本。
- `Meta Rule Source`：仓库 `AGENTS.md` 与 `skill-知行合一` 的单技能思行网络 / skeleton-first 合同。
- 优先修来源格式化前奏、模板、schema 或验证脚本，再修单次内容。
