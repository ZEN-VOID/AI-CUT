# Prompt Assembly Contract

本文件定义 step1 的 prompt 组装规则：直接使用现有分镜组内容作为生图提示词主体，先插入可追溯的 storyboard frame-unit plan，并添加固定开头明确多格 storyboard 属性。

## Fixed Prefix

每条组级 prompt 必须逐字以下列文本开头：

```text
Create a multi-panel storyboard based on the following grouped shot source. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Render the final storyboard at 4K resolution so each panel remains clear and readable. Add the storyboard panel sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of storyboard panels. Match the generated image style, lighting, and atmosphere to the bound scene reference image whenever a scene reference is provided.
```

固定开头之后先进入 `Storyboard Frame Units`，再进入 `6-分组` 的组正文主体；不插入解释性说明、provider 参数、执行日志或额外任务指令。

## Storyboard Frame Units

- `Storyboard Frame Units` 是 prompt 中的轻量 panel plan，用于告诉生图模型 storyboard 格数和每格视觉节拍。
- frame unit 必须来自 `references/group-source-extraction.md` 识别结果，可回指 `group_body`，不得补写上游没有的剧情事实。
- frame unit 的编号是 `panel_no`，不是原始 `分镜N`。原始 `分镜N` 只出现在 `source_shot_labels` 中，用于追溯。
- 允许 `panel_no` 与 `source_shot_labels` 一对多、多对一或一对一；不得把 `分镜标签数 = storyboard panel 数` 作为默认规则。
- 若 frame-unit 识别为 `partial`，必须在 prompt 包和报告中标记风险；没有人工确认前不得强行生成。

## Prompt Body

- `prompt_body` 直接采用 `group_body` 的现有内容。
- 保留组内风格句、类型元素、画面风格、对白、动作画面、分镜明细和 `分镜N:` 顺序；默认忽略相邻组间连接件，不把连接件写入 storyboard prompt。
- 不翻译、不摘要、不改写剧情事实。
- 可在结构化侧车中记录 `shot_count`、`group_id` 和 YAML 主体，但不要把报告字段插入 prompt 正文。
- 若绑定场景参照图，prompt 必须保留“生成画面风格、光影、氛围与场景参照图一致”的要求；全局风格文字锁定不能替代场景图视觉锚定。

## Layout Semantics

固定开头已声明：

- 多格 storyboard；
- frame unit 基于视觉节拍识别，不强制一一对应原始 `分镜N`；
- 最终成图按 4K 分辨率生成，保障小 panel 可读性；
- 每格左下角放 storyboard panel sequence number；
- 除镜头序号外无其他文字；
- 根据 storyboard panel 数自动适配 panel grid；
- 若提供场景参照图，生成风格、光影和氛围向该场景参照图对齐。

执行者不得再额外硬编码格数，除非用户明确要求某种布局。

## Prompt Package Shape

Markdown prompt 包推荐：

```markdown
## 1-1-1

Create a multi-panel storyboard based on the following grouped shot source. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Render the final storyboard at 4K resolution so each panel remains clear and readable. Add the storyboard panel sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of storyboard panels. Match the generated image style, lighting, and atmosphere to the bound scene reference image whenever a scene reference is provided.

### Storyboard Frame Units

1. source_shot_labels: 分镜1
   visual_beat: <从组正文中识别出的第一个 storyboard panel 视觉节拍>
   source_span: <可回指的源文本片段或摘要>

2. source_shot_labels: 分镜1, 分镜2
   visual_beat: <可合并或拆分后的 storyboard panel 视觉节拍>
   source_span: <可回指的源文本片段或摘要>

<6-分组中该组现有正文，不含底部 YAML>

### Reference Subjects

Characters:
- 林寂: projects/aigc/<项目名>/7-设计/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/7-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png
  visual_anchor: style_lighting_atmosphere

Props:
- 厚黑窗帘: missing
```

## Integrity Gate

通过 prompt 组装必须满足：

1. prompt 以固定开头起笔。
2. `Storyboard Frame Units` 存在，且每个 panel 可回指源正文；不得默认把原始 `分镜N` 机械映射为 panel。
3. 固定开头明确要求 4K 出图，避免多 panel 被压缩到不可读。
4. `group_body` 直接来自 `6-分组`，没有上游剧情改写。
5. 所有 `分镜N:` 标签按原顺序保留。
6. YAML 不被混入 prompt 正文主体，但其主体列表进入 reference manifest。
7. 若绑定场景图，prompt 和 manifest 均声明场景图作为风格、光影、氛围锚点。
8. 若由于 provider 限制必须压缩，必须先记录风险并得到用户确认；默认不压缩。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 固定开头分行、漏句或被翻译 | 重写 prompt header |
| 组正文被摘要 | 回到 `group-source-extraction.md` 重新提取 |
| 插入了说明文字或 provider 参数 | 删除非 prompt 内容，移到 plan/report |
| 分镜顺序乱序 | 按源正文顺序恢复 |
| panel 与 `分镜N` 被默认一一对应 | 重建 `Storyboard Frame Units`，按视觉节拍识别 |
| 有场景图但没有风格/光影/氛围对齐要求 | 恢复固定开头与 Scene `visual_anchor` |
| prompt 未声明 4K | 恢复固定开头中的 4K 分辨率句 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条组级 prompt 是否逐字以固定英文开头起笔，没有漏句、翻译、分行破坏或前置说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT` / `references/prompt-assembly-contract.md#fixed-prefix` | prompt markdown 中每个 `## group_id` 后首段可逐字比对固定前缀 |
| 固定开头之后是否先写 `Storyboard Frame Units`，再进入 `6-分组` 组正文主体，没有插入 provider 参数、执行日志或解释性说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT` / `references/prompt-assembly-contract.md#fixed-prefix` | prompt package 结构顺序为 fixed prefix -> frame units -> group body -> reference subjects |
| `Storyboard Frame Units` 是否来自 group extraction 结果，panel 编号使用 `panel_no`，没有把原始 `分镜N` 直接当 storyboard panel 编号？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT` | prompt 的 frame-unit plan 含 `panel_no`、`source_shot_labels`、`source_span`，并可回指 `group-index.json` |
| panel 与原始 `分镜N` 是否允许一对一、一对多、多对一，并通过 `mapping_type` 解释，而非默认一一对应？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT` | prompt 与 `group-index.json` 同步记录 `mapping_type`，review note 抽查 split/merge 合理性 |
| `prompt_body` 是否直接采用 `group_body`，保留风格句、对白、动作画面、分镜明细和 `分镜N:` 顺序，没有翻译、摘要或改写剧情事实？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N4-PROMPT` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体与 `group-index.json.group_body` diff 或抽查记录显示无剧情改写、无顺序漂移 |
| 相邻组间连接件是否没有进入 storyboard prompt 主体？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N3-GROUP-INDEX` / `N4-PROMPT` | prompt markdown 不含 `## x-y-z~x-y-z` 连接件正文，报告记录 connector ignored |
| YAML 是否没有混入 prompt 正文主体，而是只通过 reference manifest / Reference Subjects 进入参照槽位？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体不含 fenced YAML；`reference-manifest.json` 和 `Reference Subjects` 记录 YAML 主体 |
| 绑定场景图时，prompt、manifest 与 plan 是否都声明场景参照图承担风格、光影、氛围锚定，而不是只依赖全局风格文字？ | `G7-SCENE-VISUAL` | `FAIL-SHEET-REF` | `N4-PROMPT` / `N5-REF-BIND` | prompt 固定开头、Scene slot、manifest 和 imagegen plan 均出现 `style_lighting_atmosphere` |
| prompt 是否保留 4K、左下角 panel 序号、无其他文字、自动适配 grid 等 layout semantics，且没有额外硬编码格数？ | `G8-RESOLUTION` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT` / `references/prompt-assembly-contract.md#layout-semantics` | prompt 固定前缀包含 4K 与 layout 约束；除用户明确要求外无固定行列数 |
| 若 provider 限制迫使压缩，是否先记录风险并取得用户确认，而不是默认压缩组正文或删减 frame units？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N4-PROMPT` / `N10-CLOSE` | 执行报告记录 compression risk、用户确认状态、受影响 `group_id` 和保真影响 |
