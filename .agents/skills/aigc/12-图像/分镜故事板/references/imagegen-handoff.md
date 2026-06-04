# Imagegen Handoff Contract

本文件定义 step3：根据任务执行前缀、`10-分组` 对应分镜组完整内容、storyboard frame-unit plan、panel 描述、角色头顶名称标注、annotation plan 和主体参照，调用 `.agents/skills/cli/imagegen` 以分镜组为单位生成组级 storyboard sheet 图片。

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
- 绑定场景图时，场景图必须标注为 `scene_spatial_reference` 与 `subject_identity_reference`；imagegen prompt 和 plan 必须要求在黑白线稿中保留空间结构、主体身份和关键环境特征，不得要求生成画面风格、光影、氛围与场景参照图保持一致。
- 分镜故事板统一使用 `standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors`；不得把项目全局风格、north star 全局画风或场景图画风作为风格词传入 imagegen。
- 彩色只允许用于标注系统：红色箭头=身体运动；蓝色箭头=摄影机运动；绿色标记=取景/构图笔记；橙色标记=灯光方向；紫色标记=情绪/声音/叙事强调；黑色文本=每个可见角色头顶的角色名、简短镜头笔记和面板标签。不得把颜色用于角色、服装、背景、光影、氛围或渲染。
- 若存在已绑定本地参照图但尚未 `view_image`，必须先补做检视；不能直接降级为“路径仅记录”并继续生成。
- 确无可绑定图片时，允许按纯文本 prompt 生成并持久化到项目目录；结果应记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: no_reference_images_bound`。
- 若用户明确要求 API 级 mask、透明通道、模型参数或其他内置工具不暴露的控制，必须在需要 CLI/API fallback 时先取得用户显式确认。

## Batch Semantics

- 一次可以处理一集或多个分镜组。
- 每个 `group_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 每个任务的 `resolution_target` 必须固定为 `4K`。分镜故事板包含多 panel 和 panel 下方描述文字，2K 容易导致单格细节与文字不可读，不得使用通用 2K 默认。
- 每个任务的 `panel_image_aspect_ratio` 默认必须为 `16:9`；只有用户显式要求时才可改为 `9:16` 或其他比例。
- 每个任务必须包含 `panel_description` 与 `panel_description_density: rich_brief`，并要求文字区位于对应 panel 图片下方，不遮挡图片；描述必须由分组稿原文保真精简，不能新增事实。
- 每个任务必须包含 `character_name_labels`，要求每个可见角色头顶显示黑色文本角色名，且名称与分组稿/组底 YAML `角色` 字段完全一致。
- 每个任务必须包含 `annotation_plan` 与 `annotation_color_system`；标注应清晰但不遮挡主体画面或下方描述文字。
- 默认不设置后台并行要求；执行者应按 `.agents/skills/cli/imagegen` 当前能力顺序执行或受控批量执行。只有工具能力和用户显式要求同时支持时，才可采用更高吞吐的执行方式。
- 无论采用何种执行节奏，同一 `group_id` 都不得被多个任务同时写入。
- 失败任务不得阻塞已成功任务落盘；最终报告必须列出 `generated / skipped / failed`。

## Task Payload

每个 imagegen 任务至少包含：

```yaml
group_id: "1-1-1"
mode: "built_in_generate_with_reference"
resolution_target: "4K"
style_policy:
  visual_style: "standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors"
  forbidden_style_sources:
    - "global_style_keywords"
    - "scene_lighting_atmosphere"
  annotation_color_system:
    red_arrows: "body_movement"
    blue_arrows: "camera_movement"
    green_marks: "framing_composition_notes"
    orange_marks: "lighting_direction"
    purple_marks: "emotion_sound_narrative_emphasis"
    black_text: "character_name_labels_above_heads_short_shot_notes_and_panel_labels"
prompt: "<task execution prefix + storyboard frame-unit plan + panel descriptions + complete group source>"
complete_group_source: "<10-分组中该分镜组完整内容，包含组正文和底部 YAML>"
storyboard_frame_units:
  - panel_no: 1
    panel_image_aspect_ratio: "16:9"
    source_shot_labels: []
    source_span: ""
    visual_beat: ""
    panel_description: ""
    panel_description_density: "rich_brief"
    character_name_labels:
      - name: ""
        source: "group_yaml.角色"
        placement: "above_character_head"
    annotation_plan:
      red_body_movement_arrows: ""
      blue_camera_movement_arrows: ""
      green_framing_composition_marks: ""
      orange_lighting_direction_marks: ""
      purple_emotion_sound_narrative_marks: ""
      black_text_notes_and_panel_label: ""
    mapping_type: "one_to_one | split_from_shot | merged_from_shots"
reference_images:
  characters: []
  scene:
    visual_anchor: "spatial_structure_and_subject_identity"
  props: []
reference_context:
  required: true
  tool: "view_image"
  status: "visible_in_conversation_context"
subject_fidelity_policy:
  preserve_character_identity: true
  preserve_scene_spatial_structure: true
  preserve_prop_shape: true
layout_policy:
  sheet_layout: "auto_adapt_to_total_storyboard_frame_units"
  panel_image_aspect_ratio_default: "16:9"
  panel_text_position: "below_each_panel_image"
  annotation_position: "inside_panel_image_area_without_obscuring_subjects_or_text"
  overflow_strategy: "paginate_or_multiple_sheets_when_needed"
output_image_path: "projects/aigc/<项目名>/12-图像/B-分镜故事板/第1集/images/1-1-1.png"
reference_input_status: "visible_in_conversation_context"
```

## Layout Integrity

- prompt 必须保留完整分镜组内容，并包含 `storyboard_frame_units`；生成时要求模型按 frame-unit 数量自动适配 sheet layout。
- storyboard panel 数来自 `storyboard_frame_units`，不是机械来自 `shot_count` 或 `source_shot_labels` 数量。
- 生成规格固定为 4K，不能因默认 imagegen 路由或批量执行降级为 2K。
- 每个 panel 图片区默认 16:9，rich_brief panel 描述文字位于图片下方；用户显式指定时才允许改变图片区比例。
- panel 描述默认 `rich_brief`：1-2 句，来自分组稿原文，能读出主体动作、画面状态和必要的构图/运镜/情绪/场景道具信息；不得长到挤占图片区或不可读。
- 每个可见角色头顶必须有黑色文本角色名，且不得遮挡脸部、关键表情或动作。
- 每个 panel 可在图片区内叠加受控彩色标注，但标注不得遮挡主体、关键动作或下方描述文字。
- 不强制固定行列数，除非用户明确指定。
- 若 `storyboard_frame_units` 过多，计划中必须记录 `layout_risk`，可建议分页或多 sheet，但不得擅自丢弃视觉节拍。

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/<项目名>/12-图像/B-分镜故事板/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `group_id` 可追溯；
- prompt 以任务执行前缀起笔；
- prompt 包含任务执行前缀、frame-unit plan、rich_brief panel 描述、character name labels、annotation plan、默认 16:9 panel 图片区和完整分镜组内容；
- imagegen plan / result 的 `resolution_target` 为 `4K`；
- reference paths 存在，且同一主体存在多视图时没有退回主图；
- prompt / manifest / plan 均声明统一画风为标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统，不援引全局风格词；
- prompt / manifest / plan 均声明标注颜色语义，且颜色不得用于渲染；
- prompt / manifest / plan 均声明每个可见角色头顶黑色文本角色名，且名称来自分组稿/组底 YAML；
- 若绑定场景图，prompt / manifest / plan 均声明场景图用于空间结构和主体身份保真，不用于风格、光影、氛围锚定；
- 已绑定本地 reference paths 均已通过 `view_image` 进入对话上下文，并在任务中标注角色；
- output path 不覆盖现有文件，除非用户要求 rerun / replace；
- mode 未越权使用 CLI/API fallback。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 执行前是否加载 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`，并默认遵循 built-in `image_gen` 路由？ | `G9-HANDOFF` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `references/imagegen-handoff.md#skill-dependency` | imagegen plan 记录 dependency loaded、`mode` 和未启用 CLI/API fallback 的原因 |
| 若存在本地 reference images，是否先逐张 `view_image` 进入对话上下文，再声明为视觉参照，而不是只写路径？ | `G11-REF-INPUT` | `FAIL-SHEET-IMAGEGEN` | `N6-REVIEW` / `N7-IMAGEGEN` | manifest / plan / report 记录 `reference_input_status: visible_in_conversation_context` 和每张图的角色标注 |
| imagegen `reference_images` 是否消费 reference-slot-binding 的选择结果，同一主体多视图存在时不退回主图？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `N7-IMAGEGEN` | plan 中 reference paths 与 manifest `bound[]` 一致，`selected_variant` 无 priority drift |
| 绑定场景图时，prompt 和 plan 是否同时把场景图标注为 `scene_spatial_reference` 与 `subject_identity_reference`，且没有把场景图当作风格/光影/氛围锚点？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `N7-IMAGEGEN` | plan `subject_fidelity_policy.preserve_scene_spatial_structure: true`，scene reference entry 含空间结构与主体身份角色 |
| imagegen 任务是否统一采用标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统，且没有传入项目全局风格词或场景光影氛围作为风格约束？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT` / `N7-IMAGEGEN` | plan `style_policy.visual_style: standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors`，report 记录未使用 global style |
| annotation color system 是否完整且语义正确：红=身体运动、蓝=摄影机运动、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑=角色名、简短镜头笔记和面板标签？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT` / `N7-IMAGEGEN` | plan `style_policy.annotation_color_system`、frame-unit `annotation_plan` 与 report 一致 |
| 每个可见角色头顶是否有黑色文本角色名，且名称与分组稿/组底 YAML `角色` 字段一致？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N7-IMAGEGEN` | plan `storyboard_frame_units[].character_name_labels` 与 manifest `characters` 一致 |
| 确无可绑定图片时，是否走纯文本 prompt 生成并记录 `no_reference_images_bound`，没有伪造参照或把缺图写成已绑定？ | `G11-REF-INPUT` | `FAIL-SHEET-IMAGEGEN` | `N5-REF-BIND` / `N7-IMAGEGEN` | plan / result 记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: no_reference_images_bound` |
| CLI/API fallback 是否只在用户明确要求 API mask、透明通道、模型参数等内置工具不暴露能力时启用，并有确认记录？ | `G9-HANDOFF` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `references/imagegen-handoff.md#reference-input-semantics` | 执行报告记录 fallback request、user confirmation、fallback reason；无确认则 mode 仍为 built-in |
| 批量执行是否保持一组一任务、一组一输出路径，默认按工具能力顺序或受控批量执行，没有后台并行写同一 `group_id`？ | `G9-HANDOFF` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `references/imagegen-handoff.md#batch-semantics` | imagegen plan 记录 task list、`group_id` 写锁、执行节奏和无并发写冲突 |
| 每个任务的 `resolution_target` 是否固定为 `4K`，prompt、plan、result 没有继承通用 2K 默认？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT` / `N7-IMAGEGEN` | prompt、plan、result/report 均记录 `resolution_target: 4K` |
| 任务 payload 是否包含完整 prompt、完整分镜组内容、`storyboard_frame_units`、`panel_description`、`panel_description_density: rich_brief`、`character_name_labels`、`annotation_plan`、默认 `panel_image_aspect_ratio: 16:9`、layout policy，并明确 panel 数来自 frame units 而不是 `shot_count`？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N7-IMAGEGEN` | plan 中每个 task 含 `complete_group_source`、`storyboard_frame_units`、`panel_description_density`、`character_name_labels`、`annotation_plan`、`layout_policy` 与源 frame-unit 追溯 |
| frame units 过多时，是否记录 `layout_risk`、分页或多 sheet 建议，没有丢弃视觉节拍来适配单图？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N7-IMAGEGEN` / `N10-CLOSE` | imagegen plan / report 记录 layout risk、受影响 `group_id`、分页/多 sheet 或人工确认建议 |
| 生成结果是否持久化到 `projects/aigc/<项目名>/12-图像/B-分镜故事板/第N集/images/`，且不把 `$CODEX_HOME/generated_images` 当最终路径？ | `G10-PERSIST` | `FAIL-SHEET-IMAGEGEN` | `N8-PERSIST` / `.agents/skills/cli/imagegen/references/output-persistence.md` | `imagegen-results.json` 记录项目内 `output_image_path`、源路径、复制状态和存在性检查 |
| 输出路径若已存在，是否有用户 rerun / replace 授权或版本化策略，避免静默覆盖已有 storyboard？ | `G10-PERSIST` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `N8-PERSIST` | plan / report 记录 existing-file check、replace authorization 或 versioned output path |
| 执行结束是否列出 `generated / skipped / failed`，失败任务不阻塞已成功任务落盘，并提供返工入口？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N10-CLOSE` / `templates/output-template.md` | `执行报告.md` 记录每组 status、failure reason、skipped reason、rework target 和 review verdict |
