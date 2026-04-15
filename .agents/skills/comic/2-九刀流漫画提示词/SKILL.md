---
name: comic-nine-blade-prompts
description: Use when 上游漫画小说或用户指定小说需要被蒸馏为一次 Seedream 连续生成 9 张漫画页的结构化长提示词 JSON，尤其适合要固定角色、跨页叙事、漫画格布局、对白/旁白/独白/SFX 文本规范的场景。
governance_tier: full
---

# 九刀流漫画提示词

## 1. 定位

本技能把上游 `1-漫画小说改编` 的小说底稿、漫画桥接包，或用户直接提供的任意小说片段，转成可被下游 `3-漫画生成` 消费的 `nine_blade_comic_prompts.v1` JSON。

核心目标不是写 9 个互不相关的文生图 prompt，而是生成一份**单次 Seedream 连续多图请求**可理解的九页漫画提示词包：

- 一次固定 9 张图。
- 每张图是一页竖版 9:16 漫画页。
- 每页内部允许 1-5 个 panels，默认 3 panels。
- 九页之间是连续连环画画面，不是同一画面九个版本。
- 最终 JSON 必须足够让 `3-漫画生成` 合成一个单请求 master prompt。

## 2. 业务需求分析合同

| analysis_field | 必须锁定的问题 | 默认策略 |
| --- | --- | --- |
| `business_goal` | 输出服务什么动作 | 服务 Seedream 一次生成 9 张连续漫画页 |
| `business_object` | 输入是什么 | 上游漫画小说 / 用户小说 / 片段摘要 / 漫画桥接包 |
| `success_criteria` | 什么叫成功 | 9 页连续、角色一致、每页漫画感强、文本槽位清晰、可被下游脚本校验 |
| `constraint_profile` | 哪些约束不可破 | 禁止九宫格拼图；禁止同一图九变体；固定 9:16；固定 9 页 |
| `topology_fit` | 最佳思行结构 | 先抽剧情九刀，再并行锁角色/风格/文字系统，最后汇流为 JSON |
| `step_strategy` | 重点在哪 | 页级剧情切分、犀利全局漫画风格、经典漫画版式轮换、跨页一致性、Seedream 单请求兼容 |

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
- `style_profile`
  - 默认 `cinematic_comic_realism`，可指定国风连环画、美漫电影感、韩漫、暗黑写实等。
- `text_language`
  - 默认 `zh-CN`。
- `page_count`
  - 固定为 `9`，不得因内容少而减少。
- `page_aspect_ratio`
  - 固定为 `9:16`。
- `output_path`
  - 若用户未指定，默认写到 `projects/comic/[项目名]/2-九刀流漫画提示词/nine_blade_comic_prompts.json`。

## 5. 思行网络

本技能采用“串行剧情主干 + 三支路漫画语法并行 + 汇流校验”的思行网络。剧情切页先锁住 9 页叙事功能；角色连续性完成后，风格锐化、版式轮换、文字系统三条支路可并行设计，但必须在 `N4G-COMIC-GRAMMAR-MERGE` 汇流后才允许写 page prompts。

```mermaid
flowchart TD
    A["N1-INTAKE<br/>锁输入/目标/输出路径"] --> B["N2-STORY-BLADES<br/>切 9 个页级剧情刀口"]
    B --> C["N3-CONTINUITY<br/>锁角色/场景/道具连续性"]
    C --> D1["N4A-STYLE-SHARPEN<br/>全局漫画风格锐化词"]
    C --> D2["N4B-LAYOUT-DIVERSIFY<br/>经典版式轮换"]
    C --> D3["N4C-TEXT-SYSTEM<br/>对白/旁白/独白/SFX 槽"]
    D1 --> E["N4G-COMIC-GRAMMAR-MERGE<br/>漫画语法汇流门"]
    D2 --> E
    D3 --> E
    E --> F["N5-PAGE-PROMPTS<br/>逐页生成 prompt/panels/text_slots"]
    F --> G["N6-ASSEMBLY<br/>组装 nine_blade_comic_prompts.v1"]
    G --> H{"N7-VALIDATE<br/>schema + 风格 + 版式门禁"}
    H -->|"pass"| I["N8-HANDOFF<br/>交付 JSON + 思考过程"]
    H -->|"fail: story"| B
    H -->|"fail: style/layout/text"| E
    H -->|"fail: structure"| G
```

```mermaid
flowchart LR
    A["N7 failure"] --> B{{"失败类型"}}
    B -->|"FAIL-NB-BEATS"| C["回 N2<br/>重切 story_beat_map"]
    B -->|"FAIL-NB-LOCKS"| D["回 N3<br/>补角色/场景/道具锁"]
    B -->|"FAIL-NB-STYLE"| E["回 N4A<br/>补 manga_style_keywords"]
    B -->|"FAIL-NB-LAYOUT-DIVERSITY"| F["回 N4B<br/>重排 layout_id/panel_ratios"]
    B -->|"FAIL-NB-TEXT"| G["回 N4C<br/>压短文字槽"]
    B -->|"FAIL-NB-PAGES"| H["回 N5<br/>补 panels/positive_prompt"]
    B -->|"FAIL-NB-CONTRACT/STRUCTURE"| I["回 N6<br/>修 JSON 合同"]
```

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> BladesReady: N2 pass
    BladesReady --> ContinuityReady: N3 pass
    ContinuityReady --> ComicGrammarFork: enter N4A/N4B/N4C
    ComicGrammarFork --> GrammarMerged: style + layout + text pass
    GrammarMerged --> PagePromptsReady: N5 pass
    PagePromptsReady --> JsonAssembled: N6 pass
    JsonAssembled --> Validated: N7 pass
    JsonAssembled --> Rework: N7 fail
    Rework --> BladesReady: story fail
    Rework --> ComicGrammarFork: style/layout/text fail
    Rework --> JsonAssembled: structure fail
    Validated --> HandedOff
    HandedOff --> [*]
```

```mermaid
erDiagram
    SOURCE_NOVEL ||--|| STORY_BEAT_MAP : distills
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
    A["字段汇流门 N4G"] --> B{{"三支路是否齐备?"}}
    B -->|"style_bible 缺漫画锐化词"| C["阻断 N5<br/>补 N4A"]
    B -->|"layout_plan 少于 5 种布局"| D["阻断 N5<br/>补 N4B"]
    B -->|"动态布局少于 3 类"| D
    B -->|"text_slots 未分型或过长"| E["阻断 N5<br/>补 N4C"]
    B -->|"全部通过"| F["允许 N5 写 9 页 prompt"]
    F --> G["N7 validator<br/>脚本复核同一门禁"]
```

## 6. 思行节点表

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定输入、目标、风格、输出路径 | `source_novel`、`comic_bridge_pack`、用户风格要求 | 读取小说与桥接包；标记主角、主冲突、高潮点、输出路径 | 输入摘要、项目名、输出路径、风格约束 | pass -> `N2`；输入不足 -> 要求补源或进入改编段 | 输入足够形成 9 页 |
| `N2-STORY-BLADES` | 切出 9 个页级剧情刀口 | 小说段落、视觉锚点、章节钩子 | 生成 `story_beat_map[9]`，每页有动作、情绪、悬念和不同叙事功能 | `story_beat_map`、每页 `page_role` | pass -> `N3`；情节不足 -> 扩写过渡页；过密 -> 合并解释保留动作 | 9 页不重复、不跳戏 |
| `N3-CONTINUITY` | 锁角色、场景、道具和世界观一致性 | `story_beat_map`、桥接包角色/场景/道具 | 写 `character_locks / location_locks / prop_locks`，提炼跨页复用短语 | 角色锁、场景锁、道具锁 | pass -> `N4A/N4B/N4C`；漂移风险高 -> 回桥接包补锁 | 主角外观每页可复用 |
| `N4A-STYLE-SHARPEN` | 锁全局犀利漫画风格 | 题材、目标画风、连续性锁 | 写 `style_bible.manga_style_keywords / layout_directive / genre_style_keywords`，避免只有泛影视词 | `style_bible` 中的漫画语法词 | pass -> `N4G`；风格泛化 -> 补 reference 风格词库 | 至少命中漫画页、ink/line、gutter/panel/SFX 等风格语法 |
| `N4B-LAYOUT-DIVERSIFY` | 锁 9 页经典漫画版式轮换 | `story_beat_map`、冲击页、解释页、过渡页 | 为每页分配 `layout_id / panel_count / panel_ratios`，轮换 splash、inset、diagonal、split、border-breaking、zigzag 等 | `layout_plan`、每页 layout | pass -> `N4G`；平整化 -> 重排高冲击页和过渡页 | 至少 5 个 layout_id，动态布局不少于 3 类 |
| `N4C-TEXT-SYSTEM` | 锁文字槽位与漫画文字表现 | 剧情信息量、对白/旁白/SFX 需求 | 把解释压进 caption，把动作声压进 SFX，把对白压短并绑定气泡类型 | `comic_text_system`、每页 text slot 策略 | pass -> `N4G`；文字过长 -> 压缩/转旁白 | 每个文字槽类型明确，中文短句可读 |
| `N4G-COMIC-GRAMMAR-MERGE` | 汇流漫画语法三支路 | `style_bible`、`layout_plan`、`comic_text_system` | 检查三支路是否齐备，阻断缺失支路，形成 page prompt 写作策略 | 汇流摘要、风险清单 | pass -> `N5`；fail -> 对应回 `N4A/N4B/N4C` | 风格、版式、文字三个门禁同时通过 |
| `N5-PAGE-PROMPTS` | 写 9 个完整页 prompt | `story_beat_map`、角色锁、风格词、layout plan、文字系统 | 为每页写 `positive_prompt / panels / text_slots`，prompt 先写版式再写角色动作 | 9 个 page objects | pass -> `N6`；缺页或缺 panel -> 回本节点 | 每页含 9:16、独立页、非拼图约束、漫画版式 |
| `N6-ASSEMBLY` | 汇流为 `nine_blade_comic_prompts.v1` JSON | 9 个 page objects、schema、模板 | 按 schema 填充顶层合同、style、locks、pages、negative prompt | JSON 文件 | pass -> `N7`；结构缺失 -> 本节点修复 | JSON 可解析且字段齐 |
| `N7-VALIDATE` | 脚本与人工双门验收 | JSON 文件、validator、reference 门禁 | 运行 validator；检查 9 页、风格词、layout 多样性、文字系统、负向提示词 | validator 输出、人工风险摘要 | pass -> `N8`；fail -> 按失败码回对应节点 | 可被 3 号技能消费 |
| `N8-HANDOFF` | 交付下游生成所需真源 | 已验证 JSON、思考过程摘要、输出路径 | 写入 `projects/comic/[项目名]/2-九刀流漫画提示词/nine_blade_comic_prompts.json`，附切页/版式/风险摘要 | 最终 JSON、思考过程 | 完成或交给 3 号技能 | 只有一个 canonical JSON |

## 7. 输出合同

最终输出为一个 JSON 对象，禁止只输出散文式 prompt。推荐文件名：

```text
nine_blade_comic_prompts.json
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
- 全局风格级：`style_bible` 必须包含能显著推动漫画感的锐化词组，优先写入 `manga_style_keywords` 或等价字段，例如：`dynamic manga paneling`、`dramatic inked line art`、`screentone shadows`、`high contrast black gutters`、`oversized SFX`、`cinematic page composition`。
- 版式级：9 页必须轮换经典漫画布局，不得全部采用从上到下的平整条带；默认至少 5 个不同 `layout_id`，并至少包含 3 类动态布局：`splash-with-insets`、`diagonal-cut-action`、`split-diopter-page`、`border-breaking-cliffhanger`、`vertical-cascade`、`impact-sfx-page` 等。
- 每页 `positive_prompt` 必须先说明页面版式，再写角色/动作；禁止只写“cinematic shot”而缺少 panel grammar。
- 单次生成级：顶层 `generation_contract.hard_constraints` 必须包含：
  - `Generate exactly 9 separate images/pages.`
  - `Do not create a nine-grid collage.`
  - `Do not create nine variations of the same scene.`
- 文字系统：
  - 对白：`speech bubble`，短句，放角色附近。
  - 旁白：`rectangular caption box`，放页边或 panel 边缘。
  - 内心独白：`thought bubble` 或 `inner monologue caption`，与对白区分。
  - 音效：`large hand-lettered SFX`，作为画面元素，不替代对白。
- 中文文字必须使用 `clear legible Chinese text`，每个气泡不宜超过 18 个汉字。

## 9. 字段映射

| field_id | 输出位置/字段 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `FIELD-NB-01` | `generation_contract` | 固定 9 张、9:16、single_request_sequential | `FAIL-NB-CONTRACT` |
| `FIELD-NB-02` | `story_beat_map` | 9 个连续页级剧情刀口 | `FAIL-NB-BEATS` |
| `FIELD-NB-03` | `character_locks` | 跨页角色外观、服装、关键识别物稳定 | `FAIL-NB-LOCKS` |
| `FIELD-NB-04` | `comic_text_system` | 对白/旁白/独白/SFX 表现形式固定 | `FAIL-NB-TEXT` |
| `FIELD-NB-05` | `pages[]` | 恰好 9 页；每页含 panel 布局、prompt、文本槽 | `FAIL-NB-PAGES` |
| `FIELD-NB-06` | `global_negative_prompt` | 禁止拼图、变体、文字错误、错手、logo、水印 | `FAIL-NB-NEGATIVE` |
| `FIELD-NB-07` | `style_bible` | 全局漫画风格锐化词明确，不能只有泛影视词 | `FAIL-NB-STYLE` |
| `FIELD-NB-08` | `pages[].layout` | 9 页 layout_id 足够多样，动态版式不少于 3 类 | `FAIL-NB-LAYOUT-DIVERSITY` |

## 10. 验证

```bash
python3 .agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py \
  path/to/nine_blade_comic_prompts.json
```

## 11. Root-Cause 合同

若下游生成出九宫格拼图、九张近似变体、角色漂移、文本槽混乱或 JSON 无法被 3 号技能读取，必须按以下链路上溯：

`Symptom -> Direct Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

- `Rule Source`：本 `SKILL.md`、`references/nine-blade-prompt-contract.md`、schema、验证脚本。
- `Meta Rule Source`：仓库 `AGENTS.md` 与 `skill-知行合一` 的单技能思行网络 / skeleton-first 合同。
- 优先修模板、schema 或验证脚本，再修单次内容。
