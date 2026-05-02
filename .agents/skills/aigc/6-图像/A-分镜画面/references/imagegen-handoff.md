# Imagegen Handoff Contract

本文件定义 step4：根据已落盘的完整 prompt package 调用 `.agents/skills/cli/imagegen` 完成包含完整分镜构图与主体参照的图像生成。

## Default Route

- 默认遵循 `.agents/skills/cli/imagegen/SKILL.md`：普通图像生成使用内置 `image_gen` 路由。
- 默认目标为 2K 质量。
- CLI/API fallback 只有用户显式要求 CLI、API、模型参数、透明通道等能力时允许。

## Reference Input Semantics

- built-in `image_gen` 支持在对话上下文中使用可见图片作为参照；本地图片路径本身不等于视觉输入。
- `reference_images` 中的每个本地路径必须先通过 `view_image` 检视进入对话上下文，并在 prompt / manifest / plan 中标注图片角色，之后才可声明为参考图生图或参照图生成。
- 当前分镜若存在场景参照图，该图必须承担 `scene_visual_style_reference` 角色：不仅用于场景结构，还用于锁定画面风格、光影、色调和氛围。imagegen prompt 必须包含固定约束 `Match the scene reference image's visual style, lighting, color palette, and atmosphere.`，并在计划/结果中记录 `scene_visual_style_lock_status`。
- 同场景上一分镜生成图属于 `previous_frame_context` / `continuity_reference`：它用于理解空间站位、走位、朝向、遮挡、关键道具相对位置和镜头轴线，不替代角色、场景、道具槽位；若当前镜头动作或机位变化明确，必须保持逻辑延续而不是复制上一张构图。
- 两阶段批量生成中，prompt package 阶段只记录当时已存在的上一生成图或缺失原因；imagegen 串行阶段若上一分镜刚在本轮生成完成，当前镜执行前仍必须 `view_image` 该新图作为 runtime `previous_frame_context`，并把状态写入 plan/result/report。该 runtime 回看不得用来现场重写后续 prompt 正文，除非进入显式 repair。
- 构造 `reference_images` 时必须消费 `references/reference-slot-binding.md` 的选择结果：同一主体多视图和主图都存在时，只写入多视图路径；只有无多视图时才写入主图路径。
- 若存在已绑定本地参照图但尚未 `view_image`，必须先补做检视；不能直接降级为“路径仅记录”并继续生成。
- 确无可绑定图片时，允许按纯文本 prompt 生成并持久化到项目目录；结果应记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: no_reference_images_bound`。
- 若用户明确要求 API 级 mask、透明通道、模型参数或其他内置工具不暴露的控制，必须在需要 CLI/API fallback 时先取得用户显式确认。

## Batch Semantics

- 一次可以处理一集或多个 `分镜ID`。
- `episode_batch_generate` 与 `shot_batch_generate` 必须先完成指定范围的 `第N集-分镜画面-prompts.md`、`第N集-reference-manifest.json` 与 `第N集-imagegen-plan.json`；这些工件必须覆盖全部目标 `shot_id`，并在任何 imagegen 调用前通过生成前审查。
- 批量 imagegen 阶段只能消费已落盘 prompt block、reference manifest 和 plan，不得在执行某一镜时临时生成或补写后续分镜 prompt。
- 批量执行时，每个 `shot_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 批量执行是严格串行任务：必须按 `shot_id` 顺序逐镜执行，当前镜完成生成、持久化、`imagegen-results.json` 记录和必要报告更新后，才允许进入下一镜。
- 不允许后台并行、并发调用、分片并跑、多个 worker 同时生成不同分镜，或使用更高吞吐执行方式绕过顺序；即使工具能力支持并行，也必须保持串行。
- 无论采用何种执行节奏，同一 `shot_id` 都不得被多个任务同时写入。
- 失败任务不得阻塞已成功任务落盘；最终报告必须列出 failed / skipped / generated。
- 若某一镜失败，后续镜头是否继续必须遵守连续性依赖：同场景后续镜依赖该失败镜的生成图时，应记录 `previous_shot_status: failed` 并停在返工入口；不同场景或不依赖上一图的后续镜可继续串行执行，但仍不得并发。

## Task Payload

每个 imagegen 任务至少包含：

```yaml
shot_id: "1-1-1-2"
execution_order: 2
serial_index: 2
previous_shot_status: "generated"
prompt_package_status: "complete_before_imagegen"
prompt_source:
  prompts_path: "projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/第1集-分镜画面-prompts.md"
  prompt_block_id: "1-1-1-2"
mode: "built_in_generate_with_reference"
resolution_target: "2K"
prompt: "<Integrated AIGC image prompt>"
reference_images:
  characters: []
  scene: []
  props: []
reference_context:
  required: true
  tool: "view_image"
  status: "visible_in_conversation_context"
scene_visual_style_lock:
  status: "visible_in_conversation_context"
  fixed_prompt: "画面风格，光影，色调和氛围与场景参照图保持一致。"
  prompt_constraint: "Match the scene reference image's visual style, lighting, color palette, and atmosphere."
  scene_reference_path: "projects/aigc/<项目名>/5-设计/场景/3-生成/<场景名>.png"
previous_frame_context:
  status: "visible_in_conversation_context"
  previous_shot_id: "1-1-1-1"
  previous_image_path: "projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png"
  continuity_role: "spatial_blocking_reference"
output_image_path: "projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-2.png"
reference_input_status: "visible_in_conversation_context"
```

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/<项目名>/6-图像/A-分镜画面` 根路径下；逐集图片默认放入 `projects/aigc/<项目名>/6-图像/A-分镜画面/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `shot_id` 可追溯；
- `第N集-分镜画面-prompts.md` 已覆盖本轮指定范围的全部目标 `shot_id`，且先于任何 imagegen 调用落盘；
- `imagegen-plan.json` 中每个任务均引用已落盘 prompt block，并记录 `prompt_package_status: complete_before_imagegen`；
- prompt <= 1300 English words；
- prompt 包含场景参照图固定风格约束；若场景参照图存在，`scene_visual_style_lock_status` 必须是 `visible_in_conversation_context`；
- reference paths 存在，且同一主体存在多视图时没有退回主图；
- 已绑定本地 reference paths 均已通过 `view_image` 进入对话上下文，并在任务中标注角色；
- 同场景上一分镜已有本地生成图时，上一图已通过 `view_image` 进入对话上下文，并在任务中标注为 `previous_frame_context`；
- `imagegen-plan.json` 中包含 `execution_order` / `serial_index`，且执行结果按该顺序逐镜完成；
- 没有并发、后台并行、分片并跑或跳过前镜结果的执行痕迹；
- 没有边生成图片边补写后续 prompt 的执行痕迹；
- output path 不覆盖现有文件，除非用户要求 rerun / replace；
- mode 未越权使用 CLI/API fallback。
