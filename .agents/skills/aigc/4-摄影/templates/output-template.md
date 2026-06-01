# Output Template

## Output Contract Alignment

- Required output: 逐集摄影稿 `projects/aigc/<项目名>/4-摄影/第N集.md` 与阶段 `执行报告.md`。
- Output format: Markdown，保留上游场景顺序、对白、非画面字段、画面性字段标题和剧情事实；将每个画面性字段正文改写为该字段标题下的连续 `[起始秒-结束秒]` 分镜时间段。
- Output path: `projects/aigc/<项目名>/4-摄影/第N集.md`、`projects/aigc/<项目名>/4-摄影/执行报告.md`。
- Naming convention: 逐集文件命名 `第N集.md`；每个画面性字段标题下的时间段从 `[0-...秒]` 起连续递增。
- Completion gate: 所有画面性字段标题均被原样保留，字段正文均被语义保真地改写为连续 `[起始秒-结束秒]` 时间段；每段都融合原画面事实和摄影·运镜语言，能反推节拍、时值、镜头运动、构图锚点、光线结果、连续性交接和下游 AIGC 可消费 payload；同字段时间段首尾相接，相邻字段块末段/首段互相承接；上游画面描述中的必须保留可见事实不得被摘要、删短、泛化或摄影术语替代。

## Episode Frontmatter

```yaml
---
项目名: <项目名>
集数: 第N集
stage: 4-摄影
source_motion_path: projects/aigc/<项目名>/3-运动/第N集.md
fallback_source_writing_directing_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/4-摄影/第N集.md
cinematography_mode: integrated_storyboard_picture
visual_matching_policy: label_and_semantic_visual_unit_to_storyboard_picture
duration_policy: short_drama_aigc_continuous_time_ranges_with_dialogue_budget
language_policy: preserve_dialogue_and_facts_upgrade_visual_fields_to_storyboard_picture
camera_design_scope: internal_camera_continuity_and_handoff_only
review_status: <pending|pass|needs_repair>
repair_status: <not_needed|repaired|blocked>
re_review_status: <not_needed|pass|needs_repair|blocked>
---
```

## Visual Unit Projection

```markdown
<非画面字段或对白字段>：<原文完整保留>

<原画面性字段标题>：
[0-2秒] <先保留当前秒点绑定的原画面可见事实，再自然融合镜头语言：镜头从哪里进入、如何包裹人物动作或可见信息、景别/焦点/构图/光线如何组织、动作或表演如何在画面内发生、最后落到哪里。>
[2-3秒] <仅当存在第二个有效触发点、观看结果或叙事节奏价值时追加；上一段落点必须成为本段入口或过渡锚点。>
[3-5秒] <关键揭示、动作分相、对白承托、群像扩散、高点承托或 set-piece 链条需要时追加；本段末尾必须留下下一字段可消费的姿态、视线、声音、光色、空间出口或注意力落点；不得作为固定模板。>
```

原 `动作画面`、`对白画面`、`环境描写`、`角色造型`、`场面调度`、`角色动作`、`心理反应`、`心理变化`、`思考反应`、`角色思考`、`认知变化`、`内心反应`、`道具特写`、`转场` 等画面性字段标题必须保留；这些字段标题下方直接写 `[起始秒-结束秒]` 的自然镜头文字。不要新增统一 `分镜画面：` 字段，也不要写成“原画面句子 + 附着分镜说明”。原字段中的人物、动作、姿态、服装/造型、道具、环境、文字、光线、身体距离、微表情、心理/思考反应外化和表演事实不能丢失；摄影语言是增量叠加：原事实或心理/思考变化先进入可见表演，镜头再决定如何看、何时停、交给谁。

每个时间段必须满足：

- 时间范围连续：同一块从 0 秒开始，后一段起点等于前一段终点。
- 时值使用明确时间范围：写 `[0-2秒]`，不写近似时长标签。
- 语言自然丝滑：读起来先是可见画面，再是摄影机如何看；技术判断藏在句子里。
- 原画面事实保真：不新增剧情结果、对白、人物关系或场景顺序。
- 非复述：去掉原画面事实后，仍能读出机位、运镜路径、速度、停点、焦点、光影结果或交出接口。
- 源事实不缩水：去掉摄影术语后，仍能看出上游画面句子的关键可见事实；若原句有多个事实，必须能回指它们分别落在哪个秒点或焦点变化中。
- 格式承载连续性：同字段内上一段落点成为下一段入口；相邻字段块之间，上一块末段留下的姿态、视线、动作方向、声音尾巴、光色或空间出口能被下一块首段消费。

## Example

```markdown
对白（苏红叶，低语/压迫）："你以为规则是写给你看的？"

对白画面：
[0-2秒] 长焦压缩后排课桌，镜头贴近苏红叶停在桌沿的手指，红指甲在冷白灯下压住木纹；她的低语从画外压进来，背景黑板字退成一片冷白。
[2-4秒] 焦点从她的手指滑到林寂的眼睛，他的视线缓慢上移到她嘴角，瞳孔里映出一抹红色倒影，嘴角微微收紧。
```

## Report Template

```markdown
# 4-摄影 执行报告

## 输入

- source_motion_path:
- fallback_source_writing_directing_path:
- output_path:

## 覆盖

- 处理集数：
- 画面性句子数量：
- 原画面性字段时间段组数量：
- 时间段数量分布：
- density_curve_summary：
- review_status：

## Review Result

- 画面匹配：
- 节拍分析：
- 镜头时值：
- 段落观看意图与逐点归属：
- 分镜画面融合质量：
- 源画面细节增量融合：
- 时间段连续性：
- 格式连续性承载：
- 功能性影视投影：
- 源句复述扣除测试：
- AI 视频执行稳定性：
- 自然成稿：
- 原文保真：
- 直接修复项：
- 复审结果：
- 下游许可：
- 残余风险：
```
