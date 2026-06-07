# Imagegen Handoff Contract

本文件定义 step3：根据任务执行前缀、`10-分组` 对应分镜组完整内容、storyboard frame-unit plan、panel 描述、角色头顶名称标注、annotation plan、主体参照和已验收 `spatial_floor_plan`，调用 `.agents/skills/cli/imagegen` 以分镜组为单位生成组级 storyboard sheet 图片。

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
- 每个 imagegen task 必须携带 `style_lock_spec`，明确 `base_rendering: black_white_clean_line_art`、`allowed_color_layer: annotation_only`、`upstream_style_quarantine` 和 `forbidden_rendering_layers`；完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感、胶片颗粒等词只能保留在 source evidence 中，不得进入可执行绘制指令。
- 每个 imagegen task 必须携带逐 panel `visual_prompt_atoms`；最终绘制指令优先消费 atoms，而不是让模型直接从完整组稿长文本中自行抽象。atoms 缺失或只有泛化摘要时不得进入 imagegen。
- 彩色只允许用于标注系统：红色箭头=身体运动；蓝色箭头=摄影机运动；绿色标记=取景/构图笔记；橙色标记=灯光方向；紫色标记=情绪/声音/叙事强调；黑色文本=每个可见角色头顶的角色名、简短镜头笔记和面板标签。不得把颜色用于角色、服装、背景、光影、氛围或渲染。
- 若存在已绑定本地参照图但尚未 `view_image`，必须先补做检视；不能直接降级为“路径仅记录”并继续生成。
- 确无可绑定图片时，允许按纯文本 prompt 生成并持久化到项目目录；结果应记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: no_reference_images_bound`。
- 若用户明确要求 API 级 mask、透明通道、模型参数或其他内置工具不暴露的控制，必须在需要 CLI/API fallback 时先取得用户显式确认。
- storyboard sheet 生成必须同时消费 `accepted_spatial_floor_plan`；它承担空间站位、相对距离、摄影机方向和连续性锚定。平面图不得作为画风或透视构图参照，只作为顶视图空间关系约束。
- storyboard sheet 生成必须同时消费 `floor_plan_to_panel_mapping`；只传入 accepted floor plan 路径不够。每个 panel 必须明确使用哪个平面图区块、哪些角色站位/朝向、哪些道具位置、哪个摄影机位置/方向和哪些禁止空间漂移项。
- 若 `spatial_floor_plan.acceptance.verdict` 不是 `accepted`，或当前组缺少 floor plan，必须先回到 floor plan 节点自动返工；只有 accepted 后才能继续 storyboard sheet 生成，无法恢复时只可 failed 报告。

## Batch Semantics

- 一次可以处理一集或多个分镜组。
- 每个 `group_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 每个任务的 `resolution_target` 必须固定为 `4K`。分镜故事板包含多 panel 和 panel 下方描述文字，2K 容易导致单格细节与文字不可读，不得使用通用 2K 默认。
- 每个任务的 `panel_image_aspect_ratio` 默认必须为 `16:9`，且生成语义必须是锁定 16:9 image box，而不是把图片区拉伸填满 cell；只有用户显式要求时才可改为 `9:16` 或其他比例。
- 每个任务必须包含 `layout_aspect_decision` 和 `panel_geometry_blueprint`：先按实际 `panel_count` 和目标单格比例裁决行列与整图比例，再为每个 panel 计算固定 16:9 `image_box`、独立 `text_strip` 和归一化坐标，最后选择 `gpt-image-2` 合法 `selected_sheet_size`；不得把整张 sheet 固定为默认 16:9 后挤压 panel。
- built-in `image_gen` 不暴露硬尺寸参数时，`selected_sheet_size` 作为 prompt/delivery target 传入；只有用户显式授权 CLI/API/model 控制时，才把该值作为 `gpt-image-2 --size WIDTHxHEIGHT` 传给 fallback CLI。
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
source_comprehension:
  narrative_function: ""
  action_chain: []
  spatial_anchors: []
  character_state_anchors: []
  prop_state_anchors: []
  visual_turning_points: []
  must_preserve_source_facts: []
  forbidden_inventions: []
style_lock_spec:
  base_rendering: "black_white_clean_line_art"
  allowed_color_layer: "annotation_only"
  forbidden_rendering_layers:
    - "color_cinematic_still"
    - "photorealistic_rendering"
    - "global_style_keywords"
    - "scene_lighting_atmosphere"
    - "costume_background_lighting_color_rendering"
  upstream_style_quarantine:
    - source_phrase: ""
      treatment: "evidence_only_not_style_directive"
  reference_usage_policy: "identity_silhouette_spatial_structure_prop_shape_only"
  style_drift_stop_condition: "missing_style_lock_or_color_rendering_terms_in_visual_prompt_atoms"
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
visual_prompt_atoms:
  - panel_no: 1
    draw_subjects: []
    subject_actions: ""
    spatial_positions: ""
    camera_framing: ""
    line_art_instruction: "black-and-white clean storyboard line art, clear silhouettes, no color rendering"
    annotation_overlay: ""
    text_strip: ""
    negative_prompt_atoms:
      - "no color cinematic still"
      - "no photorealistic lighting"
      - "no rewritten character positions"
      - "no facts outside source_span"
reference_images:
  characters: []
  scene:
    visual_anchor: "spatial_structure_and_subject_identity"
  props: []
reference_context:
  required: true
  tool: "view_image"
  status: "visible_in_conversation_context"
accepted_spatial_floor_plan:
  floor_plan_id: "1-1-1"
  top_view_diagram_path: "projects/aigc/<项目名>/12-图像/分镜故事板/第1集/floor-plans/1-1-1.png"
  acceptance_verdict: "accepted"
  scene_boundary: ""
  character_positions: []
  prop_positions: []
  camera_plan: []
  continuity_from_previous:
    spatial_consistency_verdict: "initial | consistent"
  usage_policy: "spatial_positioning_reference_not_visual_style"
floor_plan_to_panel_mapping:
  - panel_no: 1
    floor_plan_zone: ""
    characters_position_and_facing: ""
    props_position: ""
    camera_position_and_direction: ""
    movement_path_used: ""
    unchanged_anchors_from_floor_plan: ""
    allowed_composition_variation: "framing_crop_perspective_only"
    forbidden_spatial_drift: ""
subject_fidelity_policy:
  preserve_character_identity: true
  preserve_scene_spatial_structure: true
  preserve_prop_shape: true
layout_policy:
  sheet_layout: "use_layout_aspect_decision"
  panel_image_aspect_ratio_default: "locked_16_9_image_box"
  panel_text_position: "below_each_panel_image"
  annotation_position: "inside_panel_image_area_without_obscuring_subjects_or_text"
  overflow_strategy: "paginate_or_multiple_sheets_when_needed"
layout_aspect_decision:
  panel_count: 1
  target_panel_image_aspect_ratio: "16:9"
  effective_panel_slot_ratio: ""
  selected_grid:
    columns: 1
    rows: 1
  panel_geometry_blueprint:
    geometry_lock: "fixed_16_9_image_boxes"
    max_panel_image_box_ratio_error: 0.06
    outer_margin_pct: 0.04
    gutter_pct: 0.02
    text_strip_factor: 0.2
    image_box_policy: "lock_16_9_inside_cell_leave_whitespace_if_needed"
    panels:
      - panel_no: 1
        cell_norm: { x: 0.0, y: 0.0, w: 1.0, h: 1.0 }
        image_box_norm: { x: 0.0, y: 0.0, w: 1.0, h: 0.5625 }
        image_box_aspect_ratio: "16:9"
        text_strip_norm: { x: 0.0, y: 0.58, w: 1.0, h: 0.2 }
        ratio_error: 0
  selected_sheet_aspect_ratio: ""
  selected_sheet_size: ""
  provider_size_constraints:
    model: "gpt-image-2"
    max_edge_px: 3840
    edge_multiple_px: 16
    max_long_short_ratio: "3:1"
    min_total_pixels: 655360
    max_total_pixels: 8294400
  panel_image_box_ratio_error: 0
  pagination_or_multi_sheet_decision: "single_sheet | paginate | multiple_sheets"
  execution_size_semantics: "built_in_prompt_target | cli_size_parameter"
output_image_path: "projects/aigc/<项目名>/12-图像/分镜故事板/第1集/images/1-1-1.png"
reference_input_status: "visible_in_conversation_context"
```

## Layout Integrity

- prompt 必须保留完整分镜组内容，并包含 `storyboard_frame_units`；生成时要求模型按 frame-unit 数量自动适配 sheet layout。
- storyboard panel 数来自 `storyboard_frame_units`，不是机械来自 `shot_count` 或 `source_shot_labels` 数量。
- imagegen 可执行绘制语义来自 `visual_prompt_atoms`，不是直接来自完整组稿长文本；完整组稿只承担事实边界和审计证据。
- `style_lock_spec` 是进入 imagegen 前的硬门槛；若 atoms 或 prompt 中出现彩色电影 still、写实光影、项目全局画风、场景氛围渲染、服装/背景/灯光上色等漂移词，任务必须返工。
- imagegen 任务必须携带 `accepted_spatial_floor_plan`，并要求每个 panel 的角色站位、朝向、相对距离、道具位置、摄影机方向与顶视图平面图一致。
- `accepted_spatial_floor_plan` 只约束空间站位，不提供全局画风、光影或氛围。
- imagegen 任务必须携带 `floor_plan_to_panel_mapping`，逐 panel 把 accepted floor plan 转译为可画的站位、朝向、道具、摄影机和运动路径约束；只携带平面图路径或 `accepted` 状态不得通过。
- 生成规格固定为 4K，不能因默认 imagegen 路由或批量执行降级为 2K。
- 每个 panel 图片区默认锁定为 16:9 image box，rich_brief panel 描述文字位于该图片框下方独立 text strip；用户显式指定时才允许改变图片区比例。
- 整张 sheet 的比例和尺寸来自 `layout_aspect_decision`，必须由 `panel_count`、目标 panel 图片比例、文字区和标注安全边距反推，并携带 `panel_geometry_blueprint`。若 `selected_sheet_size` 不满足 `gpt-image-2` 约束、`panel_geometry_blueprint` 缺失、`panel_image_box_ratio_error > 0.06`，或候选布局会压扁 panel，任务不得进入生成。
- `gpt-image-2` 合法尺寸约束：最大边 `<=3840px`，宽高均为 `16px` 的倍数，长短边比例 `<=3:1`，总像素 `655360..8294400`。
- panel 描述默认 `rich_brief`：1-2 句，来自分组稿原文，能读出主体动作、画面状态和必要的构图/运镜/情绪/场景道具信息；不得长到挤占图片区或不可读。
- 每个可见角色头顶必须有黑色文本角色名，且不得遮挡脸部、关键表情或动作。
- 每个 panel 可在图片区内叠加受控彩色标注，但标注不得遮挡主体、关键动作或下方描述文字。
- 不强制固定行列数，除非用户明确指定；但一旦选定行列，必须按 `panel_geometry_blueprint` 先画可见 16:9 panel image box 边框，再填画面内容和下方文字条。
- 若 `storyboard_frame_units` 过多，计划中必须记录 `layout_risk`，并自动采用分页或多 sheet 继续生成；不得丢弃视觉节拍或等待用户确认。

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/<项目名>/12-图像/分镜故事板/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `group_id` 可追溯；
- prompt 以任务执行前缀起笔；
- prompt 包含任务执行前缀、frame-unit plan、rich_brief panel 描述、character name labels、annotation plan、锁定 16:9 panel image box、panel geometry blueprint 和完整分镜组内容；
- prompt / plan 包含 source comprehension 和 layout aspect decision；
- prompt / plan 包含 `style_lock_spec`，并在 `upstream_style_quarantine` 中隔离完整组稿里的上游风格句；
- prompt / plan 包含逐 panel `visual_prompt_atoms`，每个 atom 包含 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip 和 negative_prompt_atoms；
- imagegen plan / result 的 `resolution_target` 为 `4K`；
- `layout_aspect_decision.selected_sheet_size` 满足 `gpt-image-2` 尺寸约束，`panel_geometry_blueprint` 完整，`panel_image_box_ratio_error <= 0.06`，且 built-in / CLI 的尺寸语义记录清楚；
- reference paths 存在，且同一主体存在多视图时没有退回主图；
- prompt / manifest / plan 均声明统一画风为标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统，不援引全局风格词；
- prompt / manifest / plan 均声明标注颜色语义，且颜色不得用于渲染；
- prompt / manifest / plan 均声明每个可见角色头顶黑色文本角色名，且名称来自分组稿/组底 YAML；
- floor-plan manifest 中当前组 `spatial_floor_plan.acceptance.verdict` 为 `accepted`；
- imagegen task 中包含 `accepted_spatial_floor_plan` 的 id、path、scene boundary、character positions、prop positions、camera plan 和 continuity verdict；
- imagegen task 中包含 `floor_plan_to_panel_mapping`，逐 panel 记录 floor_plan_zone、characters_position_and_facing、props_position、camera_position_and_direction、movement_path_used 和 forbidden_spatial_drift；
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
| imagegen 任务是否统一采用标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统，且没有传入项目全局风格词或场景光影氛围作为风格约束？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT-DRAFT` / `N7-IMAGEGEN` | plan `style_policy.visual_style: standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors`，report 记录未使用 global style |
| imagegen 任务是否携带 `style_lock_spec`，并隔离完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感、胶片颗粒等词？ | `G2A-STYLE-LOCK` | `FAIL-SHEET-STYLE-LOCK` | `N5B-FINAL-PAYLOAD` / `N7-IMAGEGEN` | plan `style_lock_spec.upstream_style_quarantine` 与 `forbidden_rendering_layers` 可审计，`visual_prompt_atoms` 不含漂移词 |
| annotation color system 是否完整且语义正确：红=身体运动、蓝=摄影机运动、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑=角色名、简短镜头笔记和面板标签？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT-DRAFT` / `N7-IMAGEGEN` | plan `style_policy.annotation_color_system`、frame-unit `annotation_plan` 与 report 一致 |
| 每个可见角色头顶是否有黑色文本角色名，且名称与分组稿/组底 YAML `角色` 字段一致？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N7-IMAGEGEN` | plan `storyboard_frame_units[].character_name_labels` 与 manifest `characters` 一致 |
| 当前组是否携带 `accepted_spatial_floor_plan`，且 `acceptance_verdict` 为 accepted？ | `G8D-FLOOR-PLAN-ACCEPTANCE` | `FAIL-SHEET-FLOOR-PLAN-GATE` | `N5A-FLOOR-PLAN` / `N7-IMAGEGEN` | plan task 记录 `accepted_spatial_floor_plan.floor_plan_id/path/verdict` |
| storyboard sheet 生成是否使用平面图约束角色站位、道具位置、摄影机方向和空间连续性，而不是只按画面美观重摆？ | `G8B-FLOOR-PLAN` | `FAIL-SHEET-FLOOR-PLAN` | `N5A-FLOOR-PLAN` / `N7-IMAGEGEN` | plan task 记录 spatial positioning policy，result review 抽查 panel 与 floor plan 一致 |
| storyboard sheet 生成是否携带逐 panel `floor_plan_to_panel_mapping`，而不是只携带 floor plan 路径或 accepted verdict？ | `G8E-FLOOR-PLAN-MAPPING` | `FAIL-SHEET-FLOOR-PLAN-MAPPING` | `N5A-FLOOR-PLAN` / `N5B-FINAL-PAYLOAD` / `N7-IMAGEGEN` | plan task 逐 panel 记录 floor_plan_zone、characters_position_and_facing、camera_position_and_direction、forbidden_spatial_drift |
| 确无可绑定图片时，是否走纯文本 prompt 生成并记录 `no_reference_images_bound`，没有伪造参照或把缺图写成已绑定？ | `G11-REF-INPUT` | `FAIL-SHEET-IMAGEGEN` | `N5-REF-BIND` / `N7-IMAGEGEN` | plan / result 记录 `mode_used: built_in_image_gen_text_prompt_only` 与 `reference_input_status: no_reference_images_bound` |
| CLI/API fallback 是否只在用户明确要求 API mask、透明通道、模型参数等内置工具不暴露能力时启用，并有确认记录？ | `G9-HANDOFF` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `references/imagegen-handoff.md#reference-input-semantics` | 执行报告记录 fallback request、user confirmation、fallback reason；无确认则 mode 仍为 built-in |
| 批量执行是否保持一组一任务、一组一输出路径，默认按工具能力顺序或受控批量执行，没有后台并行写同一 `group_id`？ | `G9-HANDOFF` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `references/imagegen-handoff.md#batch-semantics` | imagegen plan 记录 task list、`group_id` 写锁、执行节奏和无并发写冲突 |
| 每个任务的 `resolution_target` 是否固定为 `4K`，prompt、plan、result 没有继承通用 2K 默认？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT-DRAFT` / `N7-IMAGEGEN` | prompt、plan、result/report 均记录 `resolution_target: 4K` |
| 任务 payload 是否包含完整 prompt、完整分镜组内容、`source_comprehension`、`style_lock_spec`、`storyboard_frame_units`、`visual_prompt_atoms`、`panel_description`、`panel_description_density: rich_brief`、`character_name_labels`、`annotation_plan`、默认 locked `panel_image_aspect_ratio: 16:9`、layout policy，并明确 panel 数来自 frame units 而不是 `shot_count`？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` / `FAIL-SHEET-PROMPT-ATOMS` | `N3A-FRAME-UNITS` / `N7-IMAGEGEN` | plan 中每个 task 含 `complete_group_source`、`source_comprehension`、`style_lock_spec`、`storyboard_frame_units`、`visual_prompt_atoms`、`panel_description_density`、`character_name_labels`、`annotation_plan`、`layout_policy` 与源 frame-unit 追溯 |
| `layout_aspect_decision` 是否先按 `panel_count` 反推整图比例，再生成 `panel_geometry_blueprint` 并选择 `gpt-image-2` 合法 `selected_sheet_size`，且没有固定 16:9 sheet 后压缩 panel？ | `G8A-LAYOUT-ASPECT` | `FAIL-SHEET-LAYOUT-ASPECT` | `N3B-LAYOUT-ASPECT` / `N7-IMAGEGEN` | plan 记录 candidate grids、selected_grid、selected_sheet_aspect_ratio、selected_sheet_size、provider constraints、panel_geometry_blueprint、panel_image_box_ratio_error、execution_size_semantics |
| frame units 过多时，是否记录 `layout_risk` 并自动采用分页或多 sheet 继续生成，没有丢弃视觉节拍或等待确认来适配单图？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N7-IMAGEGEN` / `N10-CLOSE` | imagegen plan / report 记录 layout risk、受影响 `group_id`、分页/多 sheet 决策与生成图片路径 |
| 生成结果是否持久化到 `projects/aigc/<项目名>/12-图像/分镜故事板/第N集/images/`，且不把 `$CODEX_HOME/generated_images` 当最终路径？ | `G10-PERSIST` | `FAIL-SHEET-IMAGEGEN` | `N8-PERSIST` / `.agents/skills/cli/imagegen/references/output-persistence.md` | `imagegen-results.json` 记录项目内 `output_image_path`、源路径、复制状态和存在性检查 |
| 输出路径若已存在，是否有用户 rerun / replace 授权或版本化策略，避免静默覆盖已有 storyboard？ | `G10-PERSIST` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `N8-PERSIST` | plan / report 记录 existing-file check、replace authorization 或 versioned output path |
| 执行结束是否列出 `generated / skipped / failed`，失败任务不阻塞已成功任务落盘，并提供返工入口？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N10-CLOSE` / `templates/output-template.md` | `执行报告.md` 记录每组 status、failure reason、skipped reason、rework target 和 review verdict |
