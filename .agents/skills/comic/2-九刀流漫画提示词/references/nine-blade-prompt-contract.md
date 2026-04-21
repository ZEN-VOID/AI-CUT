# 九刀流提示词合同

## 1. 九刀流定义

`九刀流` 是页级切分方法：把一段漫画剧本切成 9 个连续漫画页刀口。每一刀必须承担一个不同叙事功能：

| blade | 默认功能 | 常用页面动作 |
| --- | --- | --- |
| 1 | 开场钩子 | 异常初现 / 主角现身 / 危险倒计时 |
| 2 | 触发动作 | 递出警告 / 做出选择 / 踏入禁区 |
| 3 | 阻力上桌 | 嘲笑、反派、误会、规则压迫 |
| 4 | 代价宣告 | 放狠话、交易条件、命运提示 |
| 5 | 场景迁移 | 派对、战场、山门、异界入口 |
| 6 | 危机显形 | 吊灯、雷劫、怪物、阴谋证据 |
| 7 | 生死瞬间 | 坠落、爆炸、追杀、暴露 |
| 8 | 反击/救援 | 主角出手、觉醒、破局 |
| 9 | 余波钩子 | 危机未解、倒计时继续、真凶线索 |

可按故事类型替换功能，但不得让 9 页变成同一事件的 9 个角度。

## 1.0 剧本来源格式化前奏

`九刀流` 不再直接从任意原始剧本文本切页。当前口径固定为：

1. 先把 `source_script` 做“剧本来源格式化处理”。
2. 优先直接用 `1-漫画剧本改编/第N组.md` 作为九刀切页的起点。
3. 最终不再默认只交付一份整集 JSON；当前口径是“一个 `第N组.md` 对应一份 `nine_blade_comic_prompts.v1` JSON”。兼容切组只在用户直接给 raw source 且没有 stage-1 产物时发生。

若 `1-漫画剧本改编/第N组.md` 已存在，则它优先于自由 prose，默认视为唯一上游文本真源。

前奏处理机制参照 `.agents/skills/aigc/1-Planning/2-格式`，按以下顺序执行：

- `source intake`
- `business analyze`
- `source route`
- `variant format`
- `source normalize`
- `source validate`

### 1.0.1 来源判模

原始剧本源必须先判定为以下之一：

- `scene-led`
  - 适用于章节正文、动作/对白较充足的戏剧型文本。
- `explainer-led`
  - 适用于梗概、简介、摘要、解说密度高的概述型文本。
- `compare`
  - 仅在输入模糊时内部双路比较后择一，不允许保留双 canonical handoff。

### 1.0.2 格式化真源最低要求

`第N组.md` 推荐最少包含：

- 组标题
- 本组剧情跨度
- 可直接切页的场景化正文
- 组末钩子

若 `第N组.md` 使用包装区块，读取优先级固定为：

1. `【漫剧正文】`
2. `【组末钩子】`
3. `【本组跨度】`
4. frontmatter 中的 `估算原文字数 / 尾组决议 / adaptation_posture / type_stack_summary`

其中只有 `【漫剧正文】` 拥有业务正文真相权；其余区块只作为切页辅证，不得反向覆盖正文。

硬规则：

- 未完成前奏验证前，不得直接切 `story_beat_map`。
- `【漫剧正文】` 必须可拆成可顺序切刀的场景化段落，不能还是大段抽象 prose。
- 若关键角色、场景、转场、高潮或余波在从 `第N组.md` 提取 `group_source_extract` 时丢失，视为前奏失败而不是九刀失败。

### 1.0.3 Page-Group 划分硬规则

- `第N组.md` 存在时，必须直接按组执行九刀，不再额外挂出 `page_group_plan` 竞争真源。
- 默认节奏口径：约 `1000` 字原文 = 一个 9 pages 的组单元。
- 不满 `1000` 字的一组直出；长文切分后的尾组 `300` 字以内并入上一组，`700` 字以上可自成一组，`301-699` 字默认并入上一组，除非存在明确场景或钩子闭合边界。
- 分组优先尊重 `【边界判定】`、`【漫剧正文】` 和 `【组末钩子】` 所体现的自然边界。
- 每个 group 至少要有：`entry_hook`、中段推进/阻力、`exit_hook` 或余波；不能只收一段长解释。
- 每个 group 输出仍是标准 `nine_blade_comic_prompts.v1`，但建议额外包含 `page_group` 与 `continuity_context`，明确该组身份和 continuity 继承。
- 组间 continuity 必须继承同一套 `main_character_lock`、`style_bible`、`character_locks`、`scene_continuity_bible`。允许剧情功能变化，不允许作品风格和角色造型 DNA 断层切换。

## 1.1 主角锚定硬规则

- 九页连续漫画默认必须先锁一个 `main_character_lock`，它是整组 prompt 的第一视觉锚点，不得省略。
- 即使当前页主角未正面出镜，也要保留该锚定句，以防模型在跨页时漂移主角的脸、毛色、服装或轮廓。
- 群像戏不等于取消主角锚。群像只意味着 `character_locks` 中还有其他角色；`main_character_lock` 仍必须唯一。
- 推荐字段最少包含：`character_id`、`name`、`anchor_prompt`。

## 1.2 群像角色协同硬规则

- `character_locks` 中的 recurring characters 必须是具名锁，而不是一句泛化备注。推荐字段最少包含：`character_id`、`name`、`anchor_prompt`。
- 每页必须显式声明 `active_character_ids`；多人页禁止只写“others nearby”之类泛化表述。
- 若某页 `active_character_ids` 数量 >= 2，页级 prompt 必须点名这些角色，并加入 `visually consistent and clearly distinguishable`、`stable height order / face / costume / silhouette` 一类协同语义，防止多人页出现“主角清楚、其他人漂移成路人”的问题。

## 1.3 场景连续性硬规则

- 顶层必须存在 `scene_continuity_bible`，至少包含 `default_rule` 与 `scene_locks[]`。
- 每个 `scene_lock` 推荐最少包含：`scene_id`、`name`、`anchor_prompt`。`anchor_prompt` 应锁住建筑/地标/道具/光线/时段/空间朝向，而不是只写“同一地点”。
- 每页必须通过 `scene_id` 回指一个已定义场景；页级 prompt 需要显式带入该场景名和连续性语义。

## 2. 页面 prompt 最佳骨架

每页 `positive_prompt` 推荐顺序：

1. `Page Style`
   - `cinematic comic page, vertical 9:16 aspect ratio`
   - 先指定犀利漫画风格、边框、gutter、印刷质感；不要只写泛影视感。
2. `Layout`
   - `irregular classic manga page layout`
   - 明确 panel 比例、跨格、斜切、inset、splash、破框 SFX、黑 gutter 等。
3. `Global Style Lock`
   - 在每页 prompt 前段重复注入同一条 `global style anchor`，而不是只把风格放在顶层 `style_bible`。
   - 这条 style anchor 至少锁住：同一渲染媒介、同一线条体系、同一明暗方法、同一上色策略、同一 lettering 质感、同一 panel border 质感、同一角色年龄比例。
   - 必须补一句 `forbidden style shifts`，明确禁止页面之间断层切换成 `chibi / SD / children picture-book / painterly concept art / 3D render / live-action storyboard / random full-color realism`。
   - 允许变化的是布局、镜头、情绪强弱；不允许变化的是整组 9 页的视觉 DNA。
   - 若当前 episode 被切成多个 `page-group`，这条 `global style anchor` 也必须跨组继承；不允许上一组重墨低饱和、下一组突然儿童彩图或影视概念图。
4. `Continuity Locks`
   - 先注入 `main_character_lock.anchor_prompt`。
   - 再写当前页 `active_character_ids` 对应角色的名字与其他角色锁。
   - 推荐直接采用 `Character locked across all panels: [name], [species/body/face/costume/material/color], consistent face, costume, silhouette and color palette in every panel and every page.` 这种高密度锚定句。
   - 若是多人页，补 `all listed recurring characters remain visually consistent and clearly distinguishable` 一类协同语义。
   - 再注入 `scene_continuity_bible.scene_locks[scene_id].anchor_prompt`。
   - 再写 `place page number "N" in the bottom-right corner, digits only`。
   - 每页必须显式写入“保持角色和场景一致性”的等价语义；英文推荐短语：`keep character and scene consistency across all pages`。
4. `Panel Blocks`
   - 每格镜头、动作、情绪、环境、光线、漫画技法。
5. `Text Slots`
   - speech bubble / caption box / thought bubble / SFX。
6. `Overall`
   - 氛围、质感、光影、质量词。

### 2.1 风格稳定性硬规则

- 9 页连续漫画不允许“每页像不同作品”。最常见失控形态是：第一页黑白重墨，第二页儿童彩图，第三页影视概念图，第四页又回到简笔漫画。这样的结果即使剧情对了，也属于失败。
- `style_bible` 不只负责“漫画感”，还负责“同一部作品感”。它必须让模型知道 9 页是一个稳定世界，而不是 9 次独立试风格。
- 若用户没有明确指定风格，仍必须先选一套稳定基线，例如：
  - `heavy ink contour + screentone + limited color accents`
  - `clean brush contour + airy negative space + low-saturation wash`
  - `sharp black-white action comic + restrained palette`
- 一旦选定，9 页都不得改成另一种基线。
- 若故事包含回忆、梦境、神谕或异象，默认也只允许在同一基线内做“局部语气变化”，不得切换整套媒介或人物年龄画法。

## 3. 全局漫画风格锐化词库

`style_bible` 必须先写能强制模型进入漫画页语法的全局词，不要只写 `cinematic realism`。推荐字段：

```json
{
  "manga_style_keywords": [
    "dynamic manga paneling",
    "dramatic inked line art",
    "high contrast black gutters",
    "bold contour lines",
    "screentone shadows",
    "speed lines and impact bursts",
    "oversized hand-lettered SFX",
    "cinematic page composition",
    "asymmetric panel rhythm",
    "printed comic page texture"
  ],
  "layout_directive": "Use classic manga page grammar: splash panels, inset reaction panels, diagonal cuts, border-breaking SFX, silent beat panels, close-up strips, and irregular gutters. Avoid nine pages of flat top-to-bottom strips."
}
```

建议在 `style_bible` 里额外加入：

```json
{
  "style_anchor_prompt": "Use one immutable visual DNA across all 9 pages: the same rendering medium, line weight system, shadow system, color policy, lettering feeling, panel border feeling, and character age ratio. Do not switch into chibi, children picture-book, painterly concept art, 3D render, live-action storyboard, or random full-color realism on any page.",
  "style_continuity_rule": "Pages may change in layout and emotional pressure, but not in core rendering language.",
  "forbidden_style_shifts": [
    "chibi or SD deformation",
    "children picture-book softness",
    "painterly concept art rendering",
    "3D render gloss",
    "live-action storyboard realism",
    "random color-script reset between pages"
  ]
}
```

若当前是多组输出，建议在每个组级 JSON 中增加：

```json
{
  "page_group": {
    "group_id": "page-group-01",
    "group_index": 1,
    "total_groups": 3,
    "estimated_source_chars": 480,
    "target_source_chars": 500,
    "source_span_summary": "山门异象 -> 入殿前夜",
    "rhythm_rationale": "完整覆盖异常初现、进入行动与页末钩子，不把入殿动作截断。"
  },
  "continuity_context": {
    "inherit_global_locks": true,
    "same_visual_dna_rule": "Reuse the same rendering medium, line system, shadow method, lettering feeling, and character age ratio across all groups.",
    "previous_group_hook": "",
    "next_group_hook": "祭火大殿首次亮相"
  }
}
```

按题材补充：

| genre | 推荐锐化词 |
| --- | --- |
| 悬疑恐怖 | `black gutter suspense`, `negative space dread`, `screentone fog`, `single red accent`, `claustrophobic panel crop` |
| 热血动作 | `diagonal action cuts`, `motion trails crossing gutters`, `impact burst`, `border-breaking pose`, `oversized SFX` |
| 甜宠言情 | `soft shoujo screentone`, `floating inset reactions`, `sparkle texture`, `close-up emotion strip`, `gentle panel flow` |
| 玄幻奇观 | `epic splash panel`, `ornate ink details`, `mythic scale contrast`, `aura trails`, `vertical cascade composition` |
| 都市罪案 | `procedural evidence close-up`, `cold noir gutters`, `documentary realism`, `harsh fluorescent contrast`, `silent reaction beat` |

## 4. 漫画版式库

优先轮换以下版式，避免 9 页全是三等分：

| layout_id | 用途 | 描述 |
| --- | --- | --- |
| `three-tier-dramatic` | 稳定叙事 | top 25-35%, middle 35-50%, bottom 20-35% |
| `splash-with-insets` | 高冲击页 | one dominant splash panel with 2-3 inset panels |
| `diagonal-cut-action` | 动作推进 | diagonal panel borders, speed lines crossing gutters |
| `vertical-cascade` | 追逐/坠落 | tall cascading panels, motion trail across panel borders |
| `split-diopter-page` | 顿悟/双焦点 | foreground face + background action separated by panel depth |
| `silent-reaction-grid` | 情绪停顿 | small silent reaction panels + one caption |
| `impact-sfx-page` | 爆炸/坠落 | oversized hand-lettered SFX partially breaking panel border |
| `cliffhanger-closeup` | 结尾钩子 | extreme close-up + negative space + final caption |
| `asymmetric-investigation-page` | 悬疑取证 | one evidence close-up, one narrow reaction strip, one large negative-space room panel |
| `border-breaking-cliffhanger` | 页末钩子 | character gaze or SFX breaks panel border into black gutter |
| `full-bleed-splash-with-caption` | 震撼揭示 | full-page splash with small caption and one inset reaction |
| `zigzag-tension-ladder` | 压迫升级 | zigzag panel flow guiding eye downward into final reveal |
| `overlapping-inset-reaction` | 情绪打断 | large scene panel with overlapping circular/rectangular reaction insets |
| `noir-evidence-strip` | 都市罪案 | horizontal evidence strip + vertical face close-up + bottom procedural action |

### 版式多样性门禁

- 9 页默认至少使用 5 个不同 `layout_id`。
- 至少 3 页必须不是常规上中下条带，而应使用 splash、inset、diagonal、split、border-breaking、zigzag、full-bleed 等动态版式。
- 高冲击页优先给 `splash-with-insets`、`full-bleed-splash-with-caption`、`impact-sfx-page` 或 `border-breaking-cliffhanger`。
- 解释页和过渡页也要有漫画页设计，例如证据条、反应小格、静默格，不应退化成普通电影分镜。

## 5. 经典漫画表现手法

可按页选择 1-3 个：

- `speed lines`
- `impact burst`
- `screen tone shadows`
- `black gutter suspense`
- `Dutch angle panel`
- `overlapping inset panel`
- `border-breaking character pose`
- `SFX breaking panel border`
- `silent beat panel`
- `reaction close-up strip`
- `motion trail across panels`
- `caption box as narration anchor`
- `full-bleed splash panel`
- `irregular gutter rhythm`
- `zigzag reading path`
- `evidence close-up strip`
- `single-color accent panel`

## 6. 文本槽规范

| text_type | 视觉形式 | 用途 | 长度建议 |
| --- | --- | --- | --- |
| `dialogue` | speech bubble | 角色说出口的话 | <= 18 汉字 |
| `narration` | rectangular caption box | 叙事压缩、时间地点、旁白 | <= 24 汉字 |
| `inner_monologue` | thought bubble / inner caption | 主角内心判断 | <= 20 汉字 |
| `sfx` | large hand-lettered SFX | 动作声音 | 1-6 字 |

长解释优先转成旁白 caption，不要塞进对白气泡。

### 6.1 结构化文字合同

- 顶层 `comic_text_system` 必须完整声明 `dialogue / narration / inner_monologue / sfx` 四类文字系统。
- 每类至少包含：
  - `visual_form`
  - `placement_rule`
  - `legibility_rule`
  - `max_chars`
- `text_slots[]` 不是纯文本数组，而是漫画文字执行槽。每个槽位至少包含：
  - `type`
  - `text`
  - `placement`
  - `bubble_style`
  - `inside_panel`
- `dialogue` 与 `inner_monologue` 槽位必须额外包含 `speaker_id`，并且必须回指当前页 `active_character_ids` 中的角色。
- 九页成品默认必须覆盖四类文字槽至少各一次，避免退化成“只有旁白说明文”的假漫画页。

推荐槽位形态：

```json
{
  "type": "dialogue",
  "speaker_id": "protagonist",
  "text": "别回头！",
  "placement": "near_speaker_inside_panel",
  "bubble_style": "speech_bubble",
  "inside_panel": true
}
```

```json
{
  "type": "narration",
  "text": "雷门第三次震动。",
  "placement": "panel_edge_caption",
  "bubble_style": "caption_box",
  "inside_panel": true
}
```

## 7. 负向提示词基线

全局负向提示词至少覆盖：

```text
nine-grid collage, single image collage, contact sheet, nine variations of the same scene, duplicated composition, inconsistent character face, mismatched costume, unreadable Chinese text, wrong Chinese characters, speech bubble outside panel, caption outside panel, deformed hands, extra fingers, missing fingers, distorted face, low resolution, blurry, watermark, signature, logo
```

顶层 `generation_contract.hard_constraints` 至少还必须包含角色与场景一致性约束，例如：

```text
Keep character and scene consistency across all pages.
```

以及页码约束：

```text
Place a small page number in the bottom-right corner of every page, using digits 1-9 only.
```

页级 `positive_prompt` 推荐固定骨架：

```text
vertical 9:16 comic page, [layout grammar], [global style anchor + forbidden style shifts], Character locked across all panels: [main character anchor prompt], [all active recurring characters with stable and distinguishable appearance], Scene locked across relevant pages: [scene anchor prompt], place page number "[N]" in the bottom-right corner, digits only, keep character and scene consistency across all pages, [panel actions], [text slots], [overall mood]
```

若当前页存在文字槽，`[text slots]` 片段至少要显式包含：

- `clear legible Chinese text`
- `speech bubbles near speakers`（有对白时）
- `rectangular caption boxes`（有旁白时）
- `thought bubbles or inner captions clearly different from dialogue`（有独白时）
- `hand-lettered SFX integrated inside the action panel`（有 SFX 时）
