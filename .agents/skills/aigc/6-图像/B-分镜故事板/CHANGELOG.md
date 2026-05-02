# Changelog

## 2026-05-01

- 收紧图片参照选择规则：同一主体如有多视图可选，prompt slot、reference manifest 与 imagegen plan 均优先使用多视图；只有缺少多视图时才退到主图。
- 强化 built-in `image_gen` 本地参照图语义：已绑定本地图片必须先 `view_image` 进入对话上下文，再执行参照图生成；结果记录 `reference_input_status: visible_in_conversation_context`，确无绑定图片时才使用 `no_reference_images_bound`。

## 2026-04-25

- 初始化 `B-分镜故事板` Skill 2.0 配置。
- 将主信息源固定为 `projects/aigc/<项目名>/4-分组`。
- 固化用户指定的 multi-panel storyboard 固定英文开头。
- 固化组底 YAML 主体参照绑定规则：角色、场景、道具，多视图优先，主图次之，缺图移除槽位。
- 接入 `.agents/skills/cli/imagegen` 作为默认生图执行技能，并声明按分镜组批量计划、顺序或受控批量生成与项目内持久化门禁。
- 明确 built-in `image_gen` 曾可按 `text_prompt_only` 生成并持久化；该口径已由 2026-05-01 的 `view_image` 前置门禁收紧。
