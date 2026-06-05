# Imagegen Handoff Contract

本文件定义 `N8-MULTI-IMAGE-GENERATE` 与 `N9-PERSIST-MAP`：把已审查的组级多图 prompt 交给 GPT-IMAGE-2，一次生成该分镜组的多张独立图片，并按顺序映射回四段式 `shot_id`。

## Default Route

- 组级生成计划的默认模型字段为 `gpt-image-2`。
- `call_mode` 固定为 `gpt_image_2_multi_image_group`。
- 每个普通 `group_id` 对应一个 `multi_image_task`。
- `n` 必须等于该组 `shot_count`。
- `aspect_ratio` 默认 `16:9`；只有用户显式要求时才写入 `aspect_ratio_override`，例如 `9:16` 或其他比例。
- 多组任务按源稿 `group_id` 顺序执行；每组内部不得拆成逐镜调用，除非 provider 上限阻断且用户显式授权拆组。

## Reference Input Semantics

- 本地图片路径本身不等于视觉输入；生成前必须用 `view_image` 检视进入对话上下文。
- 角色图职责：`character_identity_reference`。
- 场景图职责：`scene_reference` + `scene_visual_style_reference`，用于锁定场景设计、材质、光影、色调和氛围。
- 道具图职责：`prop_reference`。
- 同组中所有 Image sections 共享同一组必要参照，以增强角色和场景一致性；单张图可有自己的可见主体 subset，但不得切换主体身份图。

## Multi-Image Task Payload

`imagegen-plan.json` 中每个任务至少包含：

```yaml
task_id: "1-1-1.multi_image"
group_id: "1-1-1"
call_mode: "gpt_image_2_multi_image_group"
model: "gpt-image-2"
n: 3
aspect_ratio: "16:9"
aspect_ratio_override: null
provider_cap: 10
prompt_source:
  prompts_path: "projects/aigc/<项目名>/12-图像/分镜画面/第1集/第1集-分镜画面-prompts.md"
  prompt_block_id: "Group 1-1-1 Multi-Image Task"
source_group:
  source_episode_path: "projects/aigc/<项目名>/10-分组/第1集.md"
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
output_mapping:
  - image_index: 1
    shot_id: "1-1-1-1"
    output_image_path: "projects/aigc/<项目名>/12-图像/分镜画面/第1集/images/1-1-1-1.png"
  - image_index: 2
    shot_id: "1-1-1-2"
    output_image_path: "projects/aigc/<项目名>/12-图像/分镜画面/第1集/images/1-1-1-2.png"
  - image_index: 3
    shot_id: "1-1-1-3"
    output_image_path: "projects/aigc/<项目名>/12-图像/分镜画面/第1集/images/1-1-1-3.png"
non_collage_constraint: true
consistency_contract_status: "present"
overwrite_policy: "fail_unless_rerun_or_replace_authorized"
```

## Execution Rules

- 生成前必须通过 review；`prompt_only` 不进入本节点。
- `n < 1` 或 `n != shot_count` 阻断。
- 未显式指定比例时，`aspect_ratio` 必须为 `16:9`；显式指定 `9:16` 或其他比例时必须记录 override 来源。
- 默认 provider cap 为 `10`；`shot_count > provider_cap` 阻断，除非用户明确授权拆组/重组。
- 一个组的调用必须返回 `n` 张独立图片。
- 若返回 1 张拼图、故事板、多 panel 图，即使包含所有画面，也判定 `FAIL-FRAME-RESULT-MAP`。
- 若返回图片数少于或多于 `shot_count`，不得猜测补齐或丢弃；进入 repair。
- 不得静默覆盖已有 `images/<shot_id>.png`；`rerun/replace` 必须有用户授权记录。

## Output Persistence

- 结果必须持久化到 `projects/aigc/<项目名>/12-图像/分镜画面/第N集/images/`。
- 文件名固定为 `<shot_id>.png`，例如 `1-1-1-2.png`。
- `imagegen-results.json` 必须记录：
  - `group_id`
  - `task_id`
  - `expected_count`
  - `returned_count`
  - `image_index_to_shot_id`
  - `output_image_path`
  - `status`
  - `review_verdict`

## Review Before Execution

必须检查：

- `group_full_content` 已进入 prompt 或可审计引用。
- `shot_count == prompt Image section count == plan.n`。
- `aspect_ratio` 未显式指定时为 `16:9`，且 prompt 前缀与 plan 一致。
- `Task Execution Prefix` 明确禁止 storyboard sheet / collage / grid / multi-panel / variants。
- 所有已绑定本地 reference paths 均已 `view_image`。
- `reference_images` 与 `reference-manifest.json` 一致。
- `output_mapping` 覆盖每个 `shot_id` 且不覆盖现有文件，除非授权。
- provider cap 已记录。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个普通分镜组是否只有一个 `multi_image_task`，而不是逐镜独立任务？ | `G6-PLAN` | `FAIL-FRAME-IMAGEGEN` | `N7-PREVIEW-REVIEW` | plan 中 `task_id=<group_id>.multi_image`，同组无多个单镜 task。 |
| `model`、`call_mode`、`n`、`aspect_ratio`、`shot_id_order` 和 `output_mapping` 是否完整且一致？ | `G6-PLAN` | `FAIL-FRAME-IMAGEGEN` | `N7-PREVIEW-REVIEW` | plan 字段、`shot_count` 对照与 `aspect_ratio_override`。 |
| provider 上限是否已检查，超限时是否阻断或有用户授权拆组？ | `G7-HANDOFF` | `FAIL-FRAME-IMAGEGEN` | `N8-MULTI-IMAGE-GENERATE` | report 记录 `provider_cap`、`shot_count`、授权或 blocked reason。 |
| 返回是否为 `shot_count` 张单独图片，未生成拼图/故事板？ | `G8-RESULT-MAP` | `FAIL-FRAME-RESULT-MAP` | `N9-PERSIST-MAP` | results 记录 `expected_count`、`returned_count`、单图审查结论。 |
| 每张图是否按返回顺序保存到对应 `<shot_id>.png`？ | `G8-RESULT-MAP` | `FAIL-FRAME-RESULT-MAP` | `N9-PERSIST-MAP` | `image_index_to_shot_id` 与项目内文件存在性。 |
