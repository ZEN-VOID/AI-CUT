# Output Template

## Output Contract Alignment

- Required output: 逐集摄影稿 `projects/aigc/<项目名>/3-摄影/第N集.md` 与阶段 `执行报告.md`。
- Output format: Markdown，完整保留上游编导稿，并在每个画面句子下方新增 `镜头语言：` 块；该字段名为下游兼容保留，内容语义固定为“运镜摄影设计”。
- Output path: `projects/aigc/<项目名>/3-摄影/第N集.md`、`projects/aigc/<项目名>/3-摄影/执行报告.md`。
- Naming convention: 逐集文件命名 `第N集.md`；每个镜头语言块内 `分镜N` 从 1 开始连续编号。
- Completion gate: 画面性句子覆盖、节拍合理、画面节奏张弛得当、上游高潮/爽点/高光承托已完成峰值分镜强化、内部完成临近至少前 3 个画面单位连续性回看、`shot_design_plan` 已完成 references 汇流、景别景深/视角/镜头类型/运镜速度明确，镜头语言呈现动态变化、组合运镜、速度曲线和流畅感，专业可执行、原文保真；不得输出抽象主题、心理结论、世界观解释、导演阐释或不可执行的气氛口号；若 review 或 validator 发现阻断项，已在 `3-摄影` 阶段内直接最小修复并复审通过，或明确记录阻断来源且不得推进下游。

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
camera_design_scope: camera_movement_cinematography_aesthetics_motivated_transition_only
review_status: <pending|pass|needs_repair>
repair_status: <not_needed|repaired|blocked>
re_review_status: <not_needed|pass|needs_repair|blocked>
---
```

## Visual Unit Injection

```markdown
<原画面句子字段>：<原文完整保留>
镜头语言：
分镜1: 从 <承接上一镜或当前画面的入口/焦点/景别>，以 <镜头类型 + 景别/景深 + 视角 + 组合运镜 + 速度曲线> 变化到 <本节拍的终点信息>；过程中 <构图/机位/光影/色彩/有动机转场> 如何变化，最终把注意力交给 <下一分镜入口或下一画面接口>。
分镜2: 如存在第二个节拍点，必须承接分镜1的终点，从 <上一落点/反应/动作/声音/光色接口> 继续变化到 <新的注意力落点>；该分镜必须提供新的信息、动作相位、情绪压力、空间关系或转场接口，不能重复上一分镜。
```

`镜头语言：` 块内禁止写主题寓意、心理结论、世界观解释、导演阐释或不可执行的气氛口号；这些只能作为内部判断，最终必须转译为可见的运镜、摄影美学或有明确动机的转场特效。

每个 `分镜N` 必须能反推内部 `shot_design_plan`：为什么有这一镜、为什么在这个顺序、从哪里进入、如何运动、落在哪里、如何交给下一镜或下一画面。若只能写成“推进加强压迫感”之类短句，视为计划缺失，必须回到 `N6.5-SHOT-PLAN`。

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
- shot_design_plan 汇流：
- 分镜计划投影：
- 运镜摄影设计纯度：
- 镜头语言专业性：
- 摄影执行参数：
- 动态流畅性：
- 临近画面连续性：
- 原文保真：
- 直接修复项：
- 复审结果：
- 下游许可：
- 残余风险：
```
