# Storyboard Sheet Default Type Package

默认类型包用于所有 `B-分镜故事板` 任务。

## Fixed Context

- `references/group-source-extraction.md`
- `references/prompt-assembly-contract.md`
- `references/reference-slot-binding.md`
- `steps/storyboard-sheet-workflow.md`
- `review/review-contract.md`

## Gate

- 组源必须可追溯。
- storyboard panel / frame unit 必须从组正文视觉节拍识别。
- 每个 panel 必须具备来自源正文的 `rich_brief` 分镜描述文字，位于 panel 图片下方；描述由 LLM 从分组稿原文保真精简为 1-2 句，不得脚本拼接或新增事实。
- 每个可见角色头顶必须有黑色文本角色名，名称必须与 `10-分组` 分组稿或组底 YAML `角色` 字段一致，不得简写、改名、翻译或猜名。
- 每个 panel 图片区默认 16:9；用户显式要求时才可调整为 9:16 或其他比例。
- 角色、场景、道具参照只能来自组底 YAML 与真实资产。
- 画面基底统一为标准分镜手稿风格黑白线稿，不援引项目全局风格作为风格词。
- 彩色只允许用于标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。
- 即便是黑白线稿，也必须按绑定主体参照还原角色身份、场景空间结构和道具外形。
- 输出根必须位于项目 `12-图像/B-分镜故事板/`。
