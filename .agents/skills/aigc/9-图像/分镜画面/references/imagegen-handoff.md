# Imagegen Handoff Contract

本文件定义 `N8-MULTI-IMAGE-GENERATE` 与 `N9-PERSIST-MAP`：把已审查的组级多图 prompt package 交给 `.agents/skills/cli/imagegen`，由该技能的内置 `image_gen` 路由按每个 `shot_id` 的 task spec 生成独立图片，并按顺序映射回四段式 `shot_id`。

## Default Route

- 组级生成计划的执行依赖固定为 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`。
- `execution_route` 固定为 `built_in_image_gen_via_imagegen_skill`。
- 每个普通 `group_id` 对应一个 `group_imagegen_package`。
- 每个 `shot_id` 对应一个独立 `imagegen_task_spec`，`expected_image_count` 必须等于该组 `shot_count`。
- `aspect_ratio` 默认 `16:9`；只有用户显式要求时才写入 `aspect_ratio_override`，例如 `9:16` 或其他比例。
- 批量出图默认遵循 `.agents/skills/cli/imagegen` 的 subagents 并发 fan-out，最大并发 10；用户显式要求时才主线程逐一执行。
- 多组任务的 prompt/package 建立仍按源稿 `group_id` 顺序汇流，生成执行可由 imagegen 以受控并发完成，父级负责结果映射和项目目录持久化。

## Reference Input Semantics

- 本地图片路径本身不等于视觉输入；生成前必须用 `view_image` 检视进入对话上下文。
- 角色图职责：`character_identity_reference`。
- 场景图职责：`scene_reference` + `scene_visual_style_reference`，用于锁定场景设计、材质、光影、色调和氛围。
- 道具图职责：`prop_reference`。
- 同组中所有 Image sections 共享同一组必要参照，以增强角色和场景一致性；单张图可有自己的可见主体 subset，但不得切换主体身份图。

## Multi-Image Task Payload

`imagegen-plan.json` 中每个 group package 至少包含：

```yaml
task_id: "1-1-1.group_imagegen_package"
group_id: "1-1-1"
imagegen_skill: ".agents/skills/cli/imagegen"
execution_route: "built_in_image_gen"
batch_execution:
  mode: "subagents_parallel_default"
  max_concurrency: 10
expected_image_count: 3
aspect_ratio: "16:9"
aspect_ratio_override: null
prompt_source:
  prompts_path: "projects/aigc/<项目名>/9-图像/分镜画面/第1集/第1集-分镜画面-prompts.md"
  prompt_block_id: "Group 1-1-1 Multi-Image Task"
source_group:
  source_episode_path: "projects/aigc/<项目名>/8-分组/第1集.md"
  group_full_content_status: "included_or_auditable_reference"
shot_id_order:
  - "1-1-1-1"
  - "1-1-1-2"
  - "1-1-1-3"
source_shot_order:
  - "分镜1"
  - "分镜2"
  - "分镜3"
reference_images:
  characters: []
  scene: []
  props: []
reference_input_status: "visible_in_conversation_context"
imagegen_task_specs:
  - task_index: 1
    shot_id: "1-1-1-1"
    prompt_section: "Image 1 / Shot ID 1-1-1-1"
    output_image_path: "projects/aigc/<项目名>/9-图像/分镜画面/第1集/images/1-1-1-1.png"
  - task_index: 2
    shot_id: "1-1-1-2"
    prompt_section: "Image 2 / Shot ID 1-1-1-2"
    output_image_path: "projects/aigc/<项目名>/9-图像/分镜画面/第1集/images/1-1-1-2.png"
  - task_index: 3
    shot_id: "1-1-1-3"
    prompt_section: "Image 3 / Shot ID 1-1-1-3"
    output_image_path: "projects/aigc/<项目名>/9-图像/分镜画面/第1集/images/1-1-1-3.png"
output_mapping:
  - image_index: 1
    shot_id: "1-1-1-1"
    output_image_path: "projects/aigc/<项目名>/9-图像/分镜画面/第1集/images/1-1-1-1.png"
non_collage_constraint: true
consistency_contract_status: "present"
overwrite_policy: "fail_unless_rerun_or_replace_authorized"
```

## Execution Rules

- 生成前必须通过 review；`prompt_only` 不进入本节点。
- `expected_image_count < 1` 或 `expected_image_count != shot_count` 阻断。
- 未显式指定比例时，`aspect_ratio` 必须为 `16:9`；显式指定 `9:16` 或其他比例时必须记录 override 来源。
- 批量出图最大并发为 10；并发数超过 10 阻断或拆批，除非由 imagegen 父任务分批调度并记录。
- 一个组的 imagegen task specs 必须生成 `shot_count` 张独立图片。
- 若返回 1 张拼图、故事板、多 panel 图，即使包含所有画面，也判定 `FAIL-FRAME-RESULT-MAP`。
- 若返回图片数少于或多于 `shot_count`，不得猜测补齐或丢弃；进入 repair。
- 不得静默覆盖已有 `images/<shot_id>.png`；`rerun/replace` 必须有用户授权记录。

## Output Persistence

- 结果必须持久化到 `projects/aigc/<项目名>/9-图像/分镜画面/第N集/images/`。
- 文件名固定为 `<shot_id>.png`，例如 `1-1-1-2.png`。
- `imagegen-results.json` 必须记录：
  - `group_id`
  - `task_id`
  - `expected_count`
  - `returned_count`
  - `batch_execution`
  - `image_index_to_shot_id`
  - `output_image_path`
  - `status`
  - `review_verdict`

## Review Before Execution

必须检查：

- `group_full_content` 已进入 prompt 或可审计引用。
- `shot_count == prompt Image section count == expected_image_count`。
- `aspect_ratio` 未显式指定时为 `16:9`，且 prompt 前缀与 plan 一致。
- `Task Execution Prefix` 明确禁止 storyboard sheet / collage / grid / multi-panel / variants。
- 所有已绑定本地 reference paths 均已 `view_image`。
- `reference_images` 与 `reference-manifest.json` 一致。
- `output_mapping` 覆盖每个 `shot_id` 且不覆盖现有文件，除非授权。
- batch execution mode、max_concurrency 和项目目录持久化策略已记录。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个普通分镜组是否只有一个 group imagegen package，并按 `shot_id` 建立 task specs？ | `G6-PLAN` | `FAIL-FRAME-IMAGEGEN` | `N7-PREVIEW-REVIEW` | plan 中 `task_id=<group_id>.group_imagegen_package`，`imagegen_task_specs[]` 覆盖全部 `shot_id`。 |
| `imagegen_skill`、`execution_route`、`expected_image_count`、`aspect_ratio`、`shot_id_order`、`imagegen_task_specs` 和 `output_mapping` 是否完整且一致？ | `G6-PLAN` | `FAIL-FRAME-IMAGEGEN` | `N7-PREVIEW-REVIEW` | plan 字段、`shot_count` 对照与 `aspect_ratio_override`。 |
| imagegen 批量并发是否已检查，max_concurrency 是否不超过 10，主线程串行是否有用户显式要求？ | `G7-HANDOFF` | `FAIL-FRAME-IMAGEGEN` | `N8-MULTI-IMAGE-GENERATE` | report 记录 `batch_execution`、`max_concurrency`、serial opt-in 或 blocked reason。 |
| 返回是否为 `shot_count` 张单独图片，未生成拼图/故事板？ | `G8-RESULT-MAP` | `FAIL-FRAME-RESULT-MAP` | `N9-PERSIST-MAP` | results 记录 `expected_count`、`returned_count`、单图审查结论。 |
| 每张图是否按返回顺序保存到对应 `<shot_id>.png`？ | `G8-RESULT-MAP` | `FAIL-FRAME-RESULT-MAP` | `N9-PERSIST-MAP` | `image_index_to_shot_id` 与项目内文件存在性。 |
