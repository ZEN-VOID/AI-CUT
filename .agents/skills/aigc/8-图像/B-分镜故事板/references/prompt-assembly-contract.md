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
