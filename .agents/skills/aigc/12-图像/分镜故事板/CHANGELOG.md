# Changelog

## 2026-06-04

- 将分镜故事板默认画风收束为标准分镜手稿风格黑白线稿；不再援引项目全局风格、north star 全局画风或场景光影氛围作为风格词。
- 在黑白线稿基底上新增受控彩色标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签；颜色不得用于角色、背景、光影或氛围渲染。
- 新增角色头顶名称规则：每个可见角色头顶必须显示与分组稿/组底 YAML `角色` 字段一致的黑色角色名，不得简写、改名、翻译或按外观猜名。
- 调整 prompt / imagegen 逻辑：以 `10-分组` 对应分镜组完整内容为生图基础，添加本技能任务执行前缀，并按组底 YAML 绑定角色、场景、道具参照图。
- 新增 panel 结构约束：每格包含默认 16:9 图片区和位于图片下方的分镜描述文字；用户显式要求时可调整为 9:16 或其他比例。
- 新增 `rich_brief` panel 描述规则：每格文字由 LLM 从分组稿分镜描述原文保真精简为 1-2 句，信息比短标签更完整，但必须控制长度、来源和新增事实风险。
- 调整排版合同：layout 根据 `storyboard_frame_units` 数量自适应，frame units 过多时记录分页或多 sheet 策略。
- 调整主体参照职责：即便输出黑白线稿，也必须还原已有角色身份、场景空间结构和道具外形；场景图不再作为风格/光影/氛围锚点。

## 2026-05-08

- 调整 storyboard panel 落点规则：新增 `storyboard_frame_units`，要求基于 `10-分组` 当前组正文中的视觉节拍识别 panel，而不是把原始 `分镜1`、`分镜2` 机械映射为 storyboard 格子；允许 split/merge，但每个 panel 必须能回指源正文。
- 强化场景参照图职责：场景图除空间参照外，必须同步作为生成画面的风格、光影和氛围锚点；prompt、reference manifest、imagegen plan 和 review gate 均需记录该约束。
- 固化分镜故事板 4K 出图要求：因多 panel 单格面积较小，本技能不再沿用 imagegen 通用 2K 默认，prompt、imagegen plan、result 与 review gate 均需记录 `resolution_target: 4K`。

## 2026-05-01

- 收紧图片参照选择规则：同一主体如有多视图可选，prompt slot、reference manifest 与 imagegen plan 均优先使用多视图；只有缺少多视图时才退到主图。
- 强化 built-in `image_gen` 本地参照图语义：已绑定本地图片必须先 `view_image` 进入对话上下文，再执行参照图生成；结果记录 `reference_input_status: visible_in_conversation_context`，确无绑定图片时才使用 `no_reference_images_bound`。

## 2026-04-25

- 初始化 `B-分镜故事板` Skill 2.0 配置。
- 将主信息源固定为 `projects/aigc/<项目名>/10-分组`。
- 固化用户指定的 multi-panel storyboard 固定英文开头。
- 固化组底 YAML 主体参照绑定规则：角色、场景、道具，多视图优先，主图次之，缺图移除槽位。
- 接入 `.agents/skills/cli/imagegen` 作为默认生图执行技能，并声明按分镜组批量计划、顺序或受控批量生成与项目内持久化门禁。
- 明确 built-in `image_gen` 曾可按 `text_prompt_only` 生成并持久化；该口径已由 2026-05-01 的 `view_image` 前置门禁收紧。
