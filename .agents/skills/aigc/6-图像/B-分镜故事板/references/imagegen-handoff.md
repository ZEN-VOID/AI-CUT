# Imagegen Handoff Contract

本文件定义 step3：根据完整分镜故事板信息、storyboard frame-unit plan 和主体参照，调用 `.agents/skills/cli/imagegen` 以分镜组为单位生成组级 storyboard 图片。

## Skill Dependency

执行前必须加载：

```text
.agents/skills/cli/imagegen/SKILL.md
.agents/skills/cli/imagegen/CONTEXT.md
```

默认遵循该技能的内置 `image_gen` 路由；CLI/API fallback 只有用户显式要求 CLI、API、模型参数、透明通道或等价能力时允许。

## Reference Input Semantics

- built-in `image_gen` 支持在对话上下文中使用可见图片作为参照；本地图片路径本身不等于视觉输入。
- `reference_images` 中的每个本地路径必须先通过 `view_image` 检视进入对话上下文，并在 prompt / manifest / plan 中标注图片角色，之后才可声明为参考图生图或参照图生成。
- 构造 `reference_images` 时必须消费 `references/reference-slot-binding.md` 的选择结果：同一主体多视图和主图都存在时，只写入多视图路径；只有无多视图时才写入主图路径。
- 绑定场景图时，场景图必须同时标注为 `scene_reference` 与 `style_lighting_atmosphere_reference`；imagegen prompt 和 plan 必须要求生成画面风格、光影、氛围与场景参照图保持一致。
- 若存在已绑定本地参照图但尚未 `view_image`，必须先补做检视；不能直接降级为“路径仅记录”并继续生成。
- 确无可绑定图片时，允许按纯文本 prompt 生成并持久化到项目目录；结果应记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: no_reference_images_bound`。
- 若用户明确要求 API 级 mask、透明通道、模型参数或其他内置工具不暴露的控制，必须在需要 CLI/API fallback 时先取得用户显式确认。

## Batch Semantics

- 一次可以处理一集或多个分镜组。
- 每个 `group_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 每个任务的 `resolution_target` 必须固定为 `4K`。分镜故事板包含多 panel，2K 容易导致单格细节不可读，不得使用通用 2K 默认。
- 默认不设置后台并行要求；执行者应按 `.agents/skills/cli/imagegen` 当前能力顺序执行或受控批量执行。只有工具能力和用户显式要求同时支持时，才可采用更高吞吐的执行方式。
- 无论采用何种执行节奏，同一 `group_id` 都不得被多个任务同时写入。
- 失败任务不得阻塞已成功任务落盘；最终报告必须列出 `generated / skipped / failed`。

## Task Payload

每个 imagegen 任务至少包含：

```yaml
group_id: "1-1-1"
mode: "built_in_generate_with_reference"
resolution_target: "4K"
prompt: "<fixed prefix + storyboard frame-unit plan + complete group body>"
storyboard_frame_units:
  - panel_no: 1
    source_shot_labels: []
    source_span: ""
    visual_beat: ""
    mapping_type: "one_to_one | split_from_shot | merged_from_shots"
reference_images:
  characters: []
  scene:
    visual_anchor: "style_lighting_atmosphere"
  props: []
reference_context:
  required: true
  tool: "view_image"
  status: "visible_in_conversation_context"
scene_visual_policy:
  match_style_lighting_atmosphere: true
layout_policy:
  panel_grid: "auto_adapt_to_total_storyboard_frame_units"
  panel_number_position: "bottom_left"
  other_text: "none"
output_image_path: "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png"
reference_input_status: "visible_in_conversation_context"
```

## Layout Integrity

- prompt 必须保留所有源分镜信息，并包含 `storyboard_frame_units`；生成时要求模型按 frame-unit 数量自动适配 panel grid。
- storyboard panel 数来自 `storyboard_frame_units`，不是机械来自 `shot_count` 或 `source_shot_labels` 数量。
- 生成规格固定为 4K，不能因默认 imagegen 路由或批量执行降级为 2K。
- 不强制固定行列数，除非用户明确指定。
- 若 `storyboard_frame_units` 过多，计划中必须记录 `layout_risk`，可建议分页，但不得擅自丢弃视觉节拍。

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `group_id` 可追溯；
- prompt 以固定英文开头起笔；
- prompt 包含 frame-unit plan 和完整组正文；
- imagegen plan / result 的 `resolution_target` 为 `4K`；
- reference paths 存在，且同一主体存在多视图时没有退回主图；
- 若绑定场景图，prompt / manifest / plan 均声明风格、光影、氛围与场景参照图一致；
- 已绑定本地 reference paths 均已通过 `view_image` 进入对话上下文，并在任务中标注角色；
- output path 不覆盖现有文件，除非用户要求 rerun / replace；
- mode 未越权使用 CLI/API fallback。
