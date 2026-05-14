# Changelog

## 2026-05-08

- 调整 storyboard panel 落点规则：新增 `storyboard_frame_units`，要求基于 `6-分组` 当前组正文中的视觉节拍识别 panel，而不是把原始 `分镜1`、`分镜2` 机械映射为 storyboard 格子；允许 split/merge，但每个 panel 必须能回指源正文。
- 强化场景参照图职责：场景图除空间参照外，必须同步作为生成画面的风格、光影和氛围锚点；prompt、reference manifest、imagegen plan 和 review gate 均需记录该约束。
- 固化分镜故事板 4K 出图要求：因多 panel 单格面积较小，本技能不再沿用 imagegen 通用 2K 默认，prompt、imagegen plan、result 与 review gate 均需记录 `resolution_target: 4K`。

## 2026-05-01

- 收紧图片参照选择规则：同一主体如有多视图可选，prompt slot、reference manifest 与 imagegen plan 均优先使用多视图；只有缺少多视图时才退到主图。
- 强化 built-in `image_gen` 本地参照图语义：已绑定本地图片必须先 `view_image` 进入对话上下文，再执行参照图生成；结果记录 `reference_input_status: visible_in_conversation_context`，确无绑定图片时才使用 `no_reference_images_bound`。

## 2026-04-25

- 初始化 `B-分镜故事板` Skill 2.0 配置。
- 将主信息源固定为 `projects/aigc/<项目名>/6-分组`。
- 固化用户指定的 multi-panel storyboard 固定英文开头。
- 固化组底 YAML 主体参照绑定规则：角色、场景、道具，多视图优先，主图次之，缺图移除槽位。
- 接入 `.agents/skills/cli/imagegen` 作为默认生图执行技能，并声明按分镜组批量计划、顺序或受控批量生成与项目内持久化门禁。
- 明确 built-in `image_gen` 曾可按 `text_prompt_only` 生成并持久化；该口径已由 2026-05-01 的 `view_image` 前置门禁收紧。
