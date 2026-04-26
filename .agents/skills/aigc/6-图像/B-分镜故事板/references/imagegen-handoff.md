# Imagegen Handoff Contract

本文件定义 step3：根据完整分镜故事板信息和主体参照，调用 `.agents/skills/cli/imagegen` 以分镜组为单位生成组级 storyboard 图片。

## Skill Dependency

执行前必须加载：

```text
.agents/skills/cli/imagegen/SKILL.md
.agents/skills/cli/imagegen/CONTEXT.md
```

默认遵循该技能的内置 `image_gen` 路由；CLI/API fallback 只有用户显式要求 CLI、API、模型参数、透明通道或等价能力时允许。

## Reference Input Semantics

- built-in `image_gen` 默认允许 `text_prompt_only` 生成并持久化到项目目录。
- `reference_images` 中的本地路径默认只是 prompt package、manifest 和 plan 的记录项；除非执行工具明确接收这些图片作为输入，否则不得把它们描述为视觉参照已传入模型。
- `text_prompt_only` 不是失败状态，也不应导致任务被 `skipped`；结果应记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: not_passed_to_generation_tool`。
- 若用户明确要求真实参考图生图、编辑、identity lock 或视觉输入一致性，必须改走可接收参考图的工作流，并在需要 CLI/API fallback 时先取得用户显式确认。

## Batch Semantics

- 一次可以处理一集或多个分镜组。
- 每个 `group_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 默认不设置后台并行要求；执行者应按 `.agents/skills/cli/imagegen` 当前能力顺序执行或受控批量执行。只有工具能力和用户显式要求同时支持时，才可采用更高吞吐的执行方式。
- 无论采用何种执行节奏，同一 `group_id` 都不得被多个任务同时写入。
- 失败任务不得阻塞已成功任务落盘；最终报告必须列出 `generated / skipped / failed`。

## Task Payload

每个 imagegen 任务至少包含：

```yaml
group_id: "1-1-1"
mode: "built_in_generate_with_reference"
resolution_target: "2K"
prompt: "<fixed prefix + complete group body>"
reference_images:
  characters: []
  scene: []
  props: []
layout_policy:
  panel_grid: "auto_adapt_to_total_shots"
  shot_number_position: "bottom_left"
  other_text: "none"
output_image_path: "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png"
reference_input_status: "not_passed_to_generation_tool"
```

## Layout Integrity

- prompt 必须保留所有分镜，生成时要求模型自动适配 panel grid。
- 不强制固定行列数，除非用户明确指定。
- 若 `shot_count` 过大，计划中必须记录 `layout_risk`，可建议分页，但不得擅自丢镜头。

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `group_id` 可追溯；
- prompt 以固定英文开头起笔；
- prompt 包含完整组正文；
- reference paths 存在；
- output path 不覆盖现有文件，除非用户要求 rerun / replace；
- mode 未越权使用 CLI/API fallback。
