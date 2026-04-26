# Imagegen Handoff Contract

本文件定义 step4：根据已有信息调用 `.agents/skills/cli/imagegen` 完成包含完整分镜构图与主体参照的图像生成。

## Default Route

- 默认遵循 `.agents/skills/cli/imagegen/SKILL.md`：普通图像生成使用内置 `image_gen` 路由。
- 默认目标为 2K 质量。
- CLI/API fallback 只有用户显式要求 CLI、API、模型参数、透明通道等能力时允许。

## Reference Input Semantics

- built-in `image_gen` 默认允许 `text_prompt_only` 生成并持久化到项目目录。
- `reference_images` 中的本地路径默认只是 prompt package、manifest 和 plan 的记录项；除非执行工具明确接收这些图片作为输入，否则不得把它们描述为视觉参照已传入模型。
- `text_prompt_only` 不是失败状态，也不应导致任务被 `skipped`；结果应记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: not_passed_to_generation_tool`。
- 若用户明确要求真实参考图生图、编辑、identity lock 或视觉输入一致性，必须改走可接收参考图的工作流，并在需要 CLI/API fallback 时先取得用户显式确认。

## Batch Semantics

- 一次可以处理一集或多个 `分镜ID`。
- 批量执行时，每个 `shot_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 默认不设置后台并行要求；执行者应按 `.agents/skills/cli/imagegen` 当前能力顺序执行或受控批量执行。只有工具能力和用户显式要求同时支持时，才可采用更高吞吐的执行方式。
- 无论采用何种执行节奏，同一 `shot_id` 都不得被多个任务同时写入。
- 失败任务不得阻塞已成功任务落盘；最终报告必须列出 failed / skipped / generated。

## Task Payload

每个 imagegen 任务至少包含：

```yaml
shot_id: "1-1-1-1"
mode: "built_in_generate_with_reference"
resolution_target: "2K"
prompt: "<Integrated AIGC image prompt>"
reference_images:
  characters: []
  scene: []
  props: []
output_image_path: "projects/aigc/[项目名]/6-图像/A-分镜画面/第1集/images/1-1-1-1.png"
reference_input_status: "not_passed_to_generation_tool"
```

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/[项目名]/6-图像/A-分镜画面` 根路径下；逐集图片默认放入 `projects/aigc/[项目名]/6-图像/A-分镜画面/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `shot_id` 可追溯；
- prompt <= 2000 字符；
- reference paths 存在；
- output path 不覆盖现有文件，除非用户要求 rerun / replace；
- mode 未越权使用 CLI/API fallback。
