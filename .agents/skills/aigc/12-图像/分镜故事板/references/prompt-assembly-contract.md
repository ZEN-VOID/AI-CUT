# Prompt Assembly Contract

本文件定义 step1 的 prompt 组装规则：直接引用 `10-分组` 对应分镜组的完整内容作为生图基础，先插入可追溯的 storyboard frame-unit plan、每格 panel 描述、角色头顶名称标注和 annotation plan，并添加任务执行前缀明确黑白线稿分镜手稿、受控彩色标注系统、panel 图片比例、文字区和自适应排版要求。

## Task Execution Prefix

每条组级 prompt 必须逐字以下列文本开头；这是启动生图任务的任务执行词，不得替换为项目全局风格词：

```text
Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a 16:9 image area by default, with a storyboard description text area directly below that panel image. Auto-adapt the sheet layout to the total number of storyboard panels, using pagination or multiple sheets when needed. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable.
```

任务执行前缀之后先进入 `Storyboard Frame Units`，再进入 `Complete Group Source From 10-分组`；不插入解释性说明、provider 参数、执行日志或额外任务指令。

## Storyboard Frame Units

- `Storyboard Frame Units` 是 prompt 中的轻量 panel plan，用于告诉生图模型 storyboard 格数、每格视觉节拍、每格下方文字描述、每个角色头顶名称标注和每格标注计划。
- frame unit 必须来自 `references/group-source-extraction.md` 识别结果，可回指 `group_body`，不得补写上游没有的剧情事实。
- frame unit 的编号是 `panel_no`，不是原始 `分镜N`。原始 `分镜N` 只出现在 `source_shot_labels` 中，用于追溯。
- 允许 `panel_no` 与 `source_shot_labels` 一对多、多对一或一对一；不得把 `分镜标签数 = storyboard panel 数` 作为默认规则。
- 每个 frame unit 必须包含 `panel_description`，作为该 panel 图片下方的文字内容；`panel_description` 只能由 LLM 从对应 `source_span` 和分组稿分镜描述原文保真精简整合，不得发明新动作、情绪结果或角色事实。
- `panel_description_density` 默认写 `rich_brief`：每格下方文字应是 1-2 句可读分镜说明，推荐 40-90 个中文字符，最多 120 个中文字符；同一 sheet panel 很多时可压缩到 25-60 个中文字符。内容优先级为：主体/动作/画面状态 > 景别/构图/运镜 > 情绪/声音/叙事强调 > 关键场景/道具。删除重复风格词、过长对白、执行说明和无关修饰。
- 每个 frame unit 必须记录 `panel_image_aspect_ratio`，默认值为 `16:9`；只有用户显式指定时才可改为 `9:16` 或其他比例。
- 每个 frame unit 必须记录 `character_name_labels`，用于在每个可见角色头顶放置黑色文本角色名；角色名必须与分组稿/组底 YAML `角色` 字段完全一致。
- 每个 frame unit 必须记录 `annotation_plan`。如果某类标注在该 panel 不适用，写 `none`；不得为了填满颜色系统而发明不存在的运动、机位、灯光、声音或叙事强调。
- 若 frame-unit 识别为 `partial`，必须在 prompt 包和报告中标记风险；没有人工确认前不得强行生成。

## Prompt Body

- `prompt_body` 必须直接引用对应分镜组的完整内容，包括组正文和组底 YAML；YAML 同时用于主体参照绑定。
- 保留组内风格句、类型元素、画面风格、对白、动作画面、分镜明细、`分镜N:` 顺序和底部 YAML；默认忽略相邻组间连接件，不把连接件写入 storyboard prompt。
- 不翻译、不摘要、不改写剧情事实。
- 可在结构化侧车中记录 `shot_count`、`group_id` 和 YAML 主体，但不要把报告字段插入 prompt 正文。
- prompt 的画风要求只允许使用任务执行前缀中的“标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统”；不得援引项目全局风格、north star 全局画风或场景图风格作为风格词。
- source block 中保留的上游风格句只作为完整分镜组内容证据，不得被解释为 imagegen style directive。
- 绑定的角色、场景、道具参照图只用于主体身份、轮廓、空间结构和关键道具外形保真，不用于继承彩色画风、光影或氛围。
- 角色头顶名称标注属于黑色文本标注层，名称来源必须回指完整分镜组内容或组底 YAML；不得从参照图文件名、外观、正文泛称或模型猜测中改写角色名。
- 彩色标注系统只用于信息标注，不得把颜色涂进角色、服装、背景、光影或氛围。

## Layout Semantics

任务执行前缀已声明：

- 多格 storyboard；
- frame unit 基于视觉节拍识别，不强制一一对应原始 `分镜N`；
- 最终成图按 4K 分辨率生成，保障小 panel 可读性；
- 每个 panel 的图片区默认 16:9；
- 每个 panel 的图片下方必须有分镜描述文字区；
- 根据 storyboard panel 数自动适配 sheet layout；
- frame units 过多时允许分页或多 sheet 计划，并在 plan/report 中记录；
- 画面基底统一为标准黑白线稿分镜手稿，不使用全局风格词；
- 彩色只用于标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。

执行者不得再额外硬编码格数，除非用户明确要求某种布局。

## Prompt Package Shape

Markdown prompt 包推荐：

```markdown
## 1-1-1

Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a 16:9 image area by default, with a storyboard description text area directly below that panel image. Auto-adapt the sheet layout to the total number of storyboard panels, using pagination or multiple sheets when needed. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable.

### Storyboard Frame Units

1. panel_no: 1
   panel_image_aspect_ratio: 16:9
   visual_beat: <从组正文中识别出的第一个 storyboard panel 视觉节拍>
   panel_description: <rich_brief；从 source_span 和分组稿分镜描述原文保真精简为 1-2 句>
   panel_description_density: rich_brief
   character_name_labels:
     - <角色名>: above_character_head
   annotation_plan:
     red_body_movement_arrows: <身体运动方向；不适用写 none>
     blue_camera_movement_arrows: <摄影机运动方向；不适用写 none>
     green_framing_composition_marks: <取景/构图笔记；不适用写 none>
     orange_lighting_direction_marks: <灯光方向；不适用写 none>
     purple_emotion_sound_narrative_marks: <情绪/声音/叙事强调；不适用写 none>
     black_text_notes_and_panel_label: <简短镜头笔记和面板标签>
   source_shot_labels: 分镜1
   source_span: <可回指的源文本片段或摘要>

2. panel_no: 2
   panel_image_aspect_ratio: 16:9
   visual_beat: <可合并或拆分后的 storyboard panel 视觉节拍>
   panel_description: <rich_brief；从 source_span 和分组稿分镜描述原文保真精简为 1-2 句>
   panel_description_density: rich_brief
   character_name_labels:
     - <角色名>: above_character_head
   annotation_plan:
     red_body_movement_arrows: <身体运动方向；不适用写 none>
     blue_camera_movement_arrows: <摄影机运动方向；不适用写 none>
     green_framing_composition_marks: <取景/构图笔记；不适用写 none>
     orange_lighting_direction_marks: <灯光方向；不适用写 none>
     purple_emotion_sound_narrative_marks: <情绪/声音/叙事强调；不适用写 none>
     black_text_notes_and_panel_label: <简短镜头笔记和面板标签>
   source_shot_labels: 分镜1, 分镜2
   source_span: <可回指的源文本片段或摘要>

### Complete Group Source From 10-分组

<直接粘贴 10-分组 中该分镜组完整内容，包含组正文和底部 fenced YAML>

### Reference Subjects

Characters:
- 林寂: projects/aigc/<项目名>/11-主体/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/11-主体/场景/3-生成/永夜私立中学二年级A班教室-多视图.png
  visual_anchor: spatial_structure_and_subject_identity

Props:
- 厚黑窗帘: missing
```

## Integrity Gate

通过 prompt 组装必须满足：

1. prompt 以任务执行前缀起笔。
2. `Storyboard Frame Units` 存在，且每个 panel 可回指源正文；不得默认把原始 `分镜N` 机械映射为 panel。
3. 每个 frame unit 具备 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 和默认 `panel_image_aspect_ratio: 16:9`，并声明描述文字位于该 panel 图片下方。
4. 任务执行前缀明确要求 4K 出图，避免多 panel 被压缩到不可读。
5. `Complete Group Source From 10-分组` 直接来自对应分镜组完整内容，没有上游剧情改写。
6. 所有 `分镜N:` 标签按原顺序保留。
7. YAML 不得被丢弃；其主体列表进入 reference manifest，并作为完整分镜组内容的一部分保留在 source block 中。
8. prompt 不得援引全局风格作为风格词；黑白线稿也必须通过绑定参照图还原角色、场景、道具主体形象。
9. 每个可见角色头顶必须有黑色文本角色名；角色名必须与分组稿/组底 YAML `角色` 字段一致。
10. 彩色只允许用于指定标注语义，不得用于画面渲染；每个颜色语义必须与用户声明的标注系统一致。
11. 若由于 provider 限制必须压缩，必须先记录风险并得到用户确认；默认不压缩。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 任务执行前缀分行、漏句或被翻译 | 重写 prompt header |
| 组正文被摘要 | 回到 `group-source-extraction.md` 重新提取 |
| 插入了说明文字或 provider 参数 | 删除非 prompt 内容，移到 plan/report |
| 分镜顺序乱序 | 按源正文顺序恢复 |
| panel 与 `分镜N` 被默认一一对应 | 重建 `Storyboard Frame Units`，按视觉节拍识别 |
| panel 缺少描述文字、过度简略、过度冗长或默认图片比例 | 按 `rich_brief` 精简规则补齐 `panel_description` 与 `panel_image_aspect_ratio: 16:9` |
| 角色头顶名称缺失或名称不一致 | 从组底 YAML `角色` 字段重建 `character_name_labels` |
| annotation plan 缺失或颜色语义错误 | 按标注系统补齐/修正 red/blue/green/orange/purple/black 字段 |
| prompt 援引全局风格或场景风格词 | 恢复任务执行前缀中的黑白线稿分镜手稿约束，并删除全局风格词 |
| prompt 未声明 4K | 恢复任务执行前缀中的 4K 分辨率句 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条组级 prompt 是否逐字以任务执行前缀起笔，没有漏句、翻译、分行破坏或前置说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT` / `references/prompt-assembly-contract.md#task-execution-prefix` | prompt markdown 中每个 `## group_id` 后首段可逐字比对任务执行前缀 |
| 任务执行前缀之后是否先写 `Storyboard Frame Units`，再进入 `Complete Group Source From 10-分组`，没有插入 provider 参数、执行日志或解释性说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT` / `references/prompt-assembly-contract.md#task-execution-prefix` | prompt package 结构顺序为 task prefix -> frame units -> complete group source -> reference subjects |
| `Storyboard Frame Units` 是否来自 group extraction 结果，panel 编号使用 `panel_no`，没有把原始 `分镜N` 直接当 storyboard panel 编号？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT` | prompt 的 frame-unit plan 含 `panel_no`、`source_shot_labels`、`source_span`，并可回指 `group-index.json` |
| panel 与原始 `分镜N` 是否允许一对一、一对多、多对一，并通过 `mapping_type` 解释，而非默认一一对应？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT` | prompt 与 `group-index.json` 同步记录 `mapping_type`，review note 抽查 split/merge 合理性 |
| 每个 frame unit 是否包含 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 和 `panel_image_aspect_ratio: 16:9` 默认值，且描述文字位于 panel 图片下方？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N4-PROMPT` | prompt 的 frame-unit plan、imagegen plan 和 report 同步记录 panel 描述、描述密度、角色名、标注计划与比例 |
| `prompt_body` 是否直接采用完整分镜组内容，保留风格句、对白、动作画面、分镜明细、`分镜N:` 顺序和底部 YAML，没有翻译、摘要或改写剧情事实？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N4-PROMPT` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体与 `group-index.json.group_full_source` diff 或抽查记录显示无剧情改写、无顺序漂移 |
| 相邻组间连接件是否没有进入 storyboard prompt 主体？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N3-GROUP-INDEX` / `N4-PROMPT` | prompt markdown 不含 `## x-y-z~x-y-z` 连接件正文，报告记录 connector ignored |
| YAML 是否作为完整分镜组内容保留，并只通过 YAML 主体列表驱动 reference manifest / Reference Subjects？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体含 fenced YAML；`reference-manifest.json` 和 `Reference Subjects` 记录 YAML 主体 |
| prompt、manifest 与 plan 是否都声明参照图用于主体身份、空间结构和道具外形保真，而不是作为全局风格或场景风格锚点？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-REF` | `N4-PROMPT` / `N5-REF-BIND` | prompt 任务执行前缀、Scene slot、manifest 和 imagegen plan 均出现主体保真策略，且不出现全局风格词 |
| prompt 是否声明并正确使用彩色标注系统：红=身体运动、蓝=摄影机运动、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑=角色名、简短镜头笔记和面板标签？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT` / `references/prompt-assembly-contract.md#layout-semantics` | prompt 任务执行前缀、frame-unit `annotation_plan`、plan/report 均记录颜色语义，且没有把颜色用于渲染 |
| 每个可见角色头顶是否使用黑色文本显示角色名，且角色名与分组稿/组底 YAML `角色` 字段一致？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N4-PROMPT` | prompt、frame-unit `character_name_labels`、plan/report 记录角色名来源与位置 |
| prompt 是否保留 4K、默认 16:9 panel 图片区、图片下方描述文字、自适应 layout 等语义，且没有额外硬编码格数？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT` / `references/prompt-assembly-contract.md#layout-semantics` | prompt 任务执行前缀包含 4K、16:9、description under image、annotation readability 与 layout 约束；除用户明确要求外无固定行列数 |
| 若 provider 限制迫使压缩，是否先记录风险并取得用户确认，而不是默认压缩组正文或删减 frame units？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N4-PROMPT` / `N10-CLOSE` | 执行报告记录 compression risk、用户确认状态、受影响 `group_id` 和保真影响 |
