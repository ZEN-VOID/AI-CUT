# Output Template

## Output Contract Alignment

- Required output: 逐集摄影稿 `projects/aigc/<项目名>/3-摄影/第N集.md` 与阶段 `执行报告.md`。
- Output format: Markdown，完整保留上游编导稿，并在每个画面句子下方新增 `镜头语言：` 块。
- Output path: `projects/aigc/<项目名>/3-摄影/第N集.md`、`projects/aigc/<项目名>/3-摄影/执行报告.md`。
- Naming convention: 逐集文件命名 `第N集.md`；每个镜头语言块内 `分镜N` 从 1 开始连续编号。
- Completion gate: 画面性句子覆盖、节拍合理、画面节奏张弛得当、上游高潮/爽点/高光承托已完成峰值分镜强化、内部完成临近至少前 3 个画面单位连续性回看、景别景深/视角/镜头类型/运镜速度明确，镜头语言呈现动态变化、组合运镜、速度曲线和流畅感，专业可执行、原文保真、review 或 validator 通过。

## Episode Frontmatter

```yaml
---
项目名: <项目名>
集数: 第N集
stage: 3-摄影
source_directing_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/3-摄影/第N集.md
cinematography_mode: visual_sentence_cinematography_injection
visual_matching_policy: label_and_semantic_visual_unit
beat_policy: one_beat_point_one_storyboard_cut
peak_shot_policy: strengthen_existing_peak_visual_unit
language_policy: preserve_directing_text_add_lens_language
review_status: <pending|pass|needs_repair>
---
```

## Visual Unit Injection

```markdown
<原画面句子字段>：<原文完整保留>
镜头语言：
分镜1: 从 <当前画面起点/焦点/景别>，以 <镜头类型 + 景别/景深 + 视角 + 组合运镜 + 速度曲线> 变化到 <当前画面终点信息>；过程中 <构图/光影/色彩/转场> 如何变化，最终形成 <戏剧效果>。
分镜2: 如存在第二个节拍点，继续写当前画面内部从上一注意力落点到下一注意力落点的动态镜头变化；描述密度、运动复杂度和转场强度由内部 rhythm_profile 控制，不显式输出节奏标签。
```

## Report Template

```markdown
# 3-摄影 执行报告

## 输入

- source_directing_path: projects/aigc/<项目名>/2-编导/第N集.md
- output_path: projects/aigc/<项目名>/3-摄影/第N集.md

## 覆盖

- 处理集数：
- 画面性句子数量：
- 镜头语言块数量：
- review_status：

## Review Result

- 画面匹配：
- 节拍分析：
- 画面节奏：
- 高潮分镜：
- 镜头语言专业性：
- 摄影执行参数：
- 动态流畅性：
- 临近画面连续性：
- 原文保真：
- 残余风险：
```
