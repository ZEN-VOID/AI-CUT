# 九刀流提示词合同

## 1. 九刀流定义

`九刀流` 是页级切分方法：把一段小说切成 9 个连续漫画页刀口。每一刀必须承担一个不同叙事功能：

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

## 2. 页面 prompt 最佳骨架

每页 `positive_prompt` 推荐顺序：

1. `Page Style`
   - `cinematic comic page, vertical 9:16 aspect ratio`
   - 先指定犀利漫画风格、边框、gutter、印刷质感；不要只写泛影视感。
2. `Layout`
   - `irregular classic manga page layout`
   - 明确 panel 比例、跨格、斜切、inset、splash、破框 SFX、黑 gutter 等。
3. `Continuity Locks`
   - 主角固定短语、服装、关键识别物。
4. `Panel Blocks`
   - 每格镜头、动作、情绪、环境、光线、漫画技法。
5. `Text Slots`
   - speech bubble / caption box / thought bubble / SFX。
6. `Overall`
   - 氛围、质感、光影、质量词。

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

## 7. 负向提示词基线

全局负向提示词至少覆盖：

```text
nine-grid collage, single image collage, contact sheet, nine variations of the same scene, duplicated composition, inconsistent character face, mismatched costume, unreadable Chinese text, wrong Chinese characters, speech bubble outside panel, caption outside panel, deformed hands, extra fingers, missing fingers, distorted face, low resolution, blurry, watermark, signature, logo
```
