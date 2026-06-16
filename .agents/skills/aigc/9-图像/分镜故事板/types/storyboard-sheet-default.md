# Storyboard Sheet Default Type Package

默认类型包用于所有 `分镜故事板` 任务。

## Fixed Context

- `references/group-source-extraction.md`
- `references/prompt-assembly-contract.md`
- `references/reference-slot-binding.md`
- `SKILL.md` 的 `Thinking-Action Node Map`
- `review/review-contract.md`

## Gate

- 组源必须可追溯。
- 必须先建立 source comprehension，理解本组叙事功能、动作链、空间/主体/道具锚点、视觉转折、必须保留源事实和禁止补写项；不得用通用套句替代对现有内容的理解。
- 必须建立 `style_lock_spec`：完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感和胶片颗粒等词只能作为 source evidence，不得进入最终绘制指令；缺失时标记 `FAIL-SHEET-STYLE-LOCK`。
- storyboard panel / frame unit 必须从组正文视觉节拍识别。
- 每个 panel 必须具备来自源正文的 `rich_brief` 分镜描述文字，位于 panel 图片下方；描述由 LLM 从分组稿原文保真精简为 1-2 句，不得脚本拼接或新增事实。
- 每个 panel 必须具备 `visual_prompt_atoms`：draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip、negative_prompt_atoms；不得只靠摘要或完整组稿让 imagegen 自行理解。
- `spatial_positions` 优先来自源正文的空间锚点；若已有 `分镜平面图` accepted 侧车，可作为补充证据读取，但不得成为故事板生成前置条件。
- 每个可见角色头顶必须有黑色文本角色名，名称必须与 `8-分组` 分组稿或组底 YAML `角色` 字段一致，不得简写、改名、翻译或猜名。
- 每个 panel 图片区默认 locked 16:9 image box；用户显式要求时才可调整为 9:16 或其他比例。
- 整张 storyboard sheet 的画布比例不得固定继承 16:9；必须在 frame-unit 数量确定后生成 `layout_aspect_decision` 和 `panel_geometry_blueprint`，选择能让每个单格 `image_box` 锁定 16:9、且适配 imagegen 4K 目标的 sheet aspect / size 策略。
- `panel_geometry_blueprint` 必须记录每格 `cell_norm`、`image_box_norm`、`text_strip_norm`，并保证 `panel_image_box_ratio_error <= 0.06`；如果合法单张画布无法保持 panel 比例与文字可读性，必须分页或多 sheet，并在报告中说明。
- 角色、场景、道具参照只能来自组底 YAML 与真实资产。
- 画面基底统一为标准分镜手稿风格黑白线稿，不援引项目全局风格作为风格词。
- 彩色只允许用于标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。
- 即便是黑白线稿，也必须按绑定主体参照还原角色身份、场景空间结构和道具外形。
- 输出根必须位于项目 `9-图像/分镜故事板/`。
