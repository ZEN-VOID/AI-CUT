# Imagegen Handoff Contract

本文件定义 step3：根据任务执行前缀、`8-分组` 对应分镜组完整内容、storyboard frame-unit plan、panel 描述、角色头顶名称标注、annotation plan、主体参照、style lock、layout aspect decision、visual prompt atoms 和可选 `spatial_handoff`，调用 `.agents/skills/cli/imagegen` 以分镜组为单位生成组级 storyboard sheet 图片。

## Skill Dependency

执行前必须加载：

```text
.agents/skills/cli/imagegen/SKILL.md
.agents/skills/cli/imagegen/CONTEXT.md
```

默认且唯一遵循该技能的内置 `image_gen` 路由；CLI/API/provider 专属控制不属于本技能默认或 fallback 路线。

`第N集-imagegen-plan.json` 只是执行载体，不是完成态。每个目标组必须进入实际 imagegen 调用并得到 `imagegen-results.json` 与项目内 `images/<分镜组ID>.png`；无生成图路径时 review verdict 不得为 `pass` 或 `pass_with_todo`。

## Reference Input Semantics

- built-in `image_gen` 支持在对话上下文中使用可见图片作为参照；本地图片路径本身不等于视觉输入。
- `reference_images` 中的每个本地路径必须先通过 `view_image` 检视进入对话上下文，并在 prompt / manifest / plan 中标注图片角色，之后才可声明为参考图生图或参照图生成。
- 绑定场景图时，场景图必须标注为 `scene_spatial_reference` 与 `subject_identity_reference`；imagegen prompt 和 plan 必须要求在黑白线稿中保留空间结构、主体身份和关键环境特征，不得要求生成画面风格、光影、氛围与场景参照图保持一致。
- 分镜故事板统一使用 `standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors`；不得把项目全局风格、north star 全局画风或场景图画风作为风格词传入 imagegen。
- 每个 imagegen task 必须携带 `style_lock_spec`、逐 panel `visual_prompt_atoms`、`layout_aspect_decision` 与 `panel_geometry_blueprint`。
- 彩色只允许用于标注系统：红色箭头=身体运动；蓝色箭头=摄影机运动；绿色标记=取景/构图笔记；橙色标记=灯光方向；紫色标记=情绪/声音/叙事强调；黑色文本=每个可见角色头顶的角色名、简短镜头笔记和面板标签。
- 可选 `spatial_handoff` 只用于补充角色站位、相对距离、运动路径或机位方向证据；不得作为 imagegen 前置门禁。缺失时记录 `spatial_handoff_status: none` 并继续。

## Batch Semantics

- 一次可以处理一集或多个分镜组。
- 每个 `group_id` 是一个独立 imagegen 任务，拥有独立 prompt、reference images、output path 和 review status。
- 每个目标 `group_id` 都必须实际调用 imagegen；计划存在但未执行时只能记录为 failed 或 needs_rework，不得视为 generated。
- 每个任务的 `resolution_target` 必须固定为 `4K`。
- 每个任务的 `panel_image_aspect_ratio` 默认必须为 `16:9`，且生成语义必须是锁定 16:9 image box，而不是把图片区拉伸填满 cell。
- 每个任务必须包含 `panel_description` 与 `panel_description_density: rich_brief`，并要求文字区位于对应 panel 图片下方，不遮挡图片。
- 每个任务必须包含 `character_name_labels`，要求每个可见角色头顶显示黑色文本角色名，且名称与分组稿/组底 YAML `角色` 字段完全一致。
- 每个任务必须包含 `annotation_plan` 与 `annotation_color_system`；标注应清晰但不遮挡主体画面或下方描述文字。
- 批量多任务默认按 `.agents/skills/cli/imagegen` 的 subagents 并发模式执行，最大并发数为 `10`；只有用户显式要求时才允许主线程逐一执行。
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
complete_group_source: "<8-分组中该分镜组完整内容，包含组正文和底部 YAML>"
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
  upstream_style_quarantine: []
storyboard_frame_units:
  - panel_no: 1
    panel_image_aspect_ratio: "16:9"
    source_shot_labels: []
    source_span: ""
    visual_beat: ""
    panel_description: ""
    panel_description_density: "rich_brief"
    character_name_labels: []
    annotation_plan: {}
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
spatial_handoff:
  status: "none | consumed"
  source_skill: "分镜平面图"
  accepted_floor_plan_sheet_path: ""
  usable_constraints: []
  usage_policy: "evidence_only_not_storyboard_completion_gate"
reference_images:
  characters: []
  scene:
    visual_anchor: "spatial_structure_and_subject_identity"
  props: []
reference_context:
  required: true
  tool: "view_image"
  status: "visible_in_conversation_context | no_reference_images_bound"
layout_policy:
  sheet_layout: "use_layout_aspect_decision"
  panel_image_aspect_ratio_default: "locked_16_9_image_box"
  panel_text_position: "below_each_panel_image"
  annotation_position: "inside_panel_image_area_without_obscuring_subjects_or_text"
  overflow_strategy: "paginate_or_multiple_sheets_when_needed"
layout_aspect_decision:
  panel_count: 1
  target_panel_image_aspect_ratio: "16:9"
  selected_grid:
    columns: 1
    rows: 1
  panel_geometry_blueprint:
    geometry_lock: "fixed_16_9_image_boxes"
    max_panel_image_box_ratio_error: 0.06
    panels: []
  selected_sheet_size: ""
  panel_image_box_ratio_error: 0
  pagination_or_multi_sheet_decision: "single_sheet | paginate | multiple_sheets"
output_image_path: "projects/aigc/<项目名>/9-图像/分镜故事板/第1集/images/1-1-1.png"
```

## Layout Integrity

- prompt 必须保留完整分镜组内容，并包含 `storyboard_frame_units`。
- storyboard panel 数来自 `storyboard_frame_units`，不是机械来自 `shot_count` 或 `source_shot_labels` 数量。
- imagegen 可执行绘制语义来自 `visual_prompt_atoms`，不是直接来自完整组稿长文本；完整组稿只承担事实边界和审计证据。
- `style_lock_spec` 是进入 imagegen 前的硬门槛；若 atoms 或 prompt 中出现彩色电影 still、写实光影、项目全局画风、场景氛围渲染等漂移词，任务必须返工。
- `spatial_handoff` 缺失不阻断。若存在，它只约束相对方位、站位、动线或机位证据，不提供全局画风、光影或氛围。
- 生成规格固定为 4K，不能因默认 imagegen 路由或批量执行降级为 2K。
- 每个 panel 图片区默认锁定为 16:9 image box，rich_brief panel 描述文字位于该图片框下方独立 text strip。

## Output Persistence

- 生成结果必须复制或持久化到 `projects/aigc/<项目名>/9-图像/分镜故事板/第N集/images/`。
- 不得把 `$CODEX_HOME/generated_images/...` 作为项目内最终路径。
- `imagegen-plan.json` 记录预期输出；`imagegen-results.json` 记录实际生成路径、源路径、状态与审查结论。

## Review Before Execution

批量生成前必须通过：

- `group_id` 可追溯；
- prompt 以任务执行前缀起笔；
- prompt / plan 包含 source comprehension、frame-unit plan、rich_brief panel 描述、character name labels、annotation plan、锁定 16:9 panel image box、panel geometry blueprint 和完整分镜组内容；
- prompt / plan 包含 `style_lock_spec` 与逐 panel `visual_prompt_atoms`；
- imagegen plan / result 的 `resolution_target` 为 `4K`；
- reference paths 存在，且同一主体存在多视图时没有退回主图；
- prompt / manifest / plan 均声明统一画风为标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统，不援引全局风格词；
- 可选 `spatial_handoff` 若存在，记录 source path/verdict/usable constraints，且未作为完成门禁或画风来源；
- 若绑定本地 reference paths，均已通过 `view_image` 进入对话上下文；
- output path 不覆盖现有文件，除非用户要求 rerun / replace；
- mode 未越权使用 CLI/API/provider 专属控制，且批量执行形态符合 imagegen 最大并发 `10` 的合同。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 执行前是否加载 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`，默认遵循 built-in `image_gen` 路由，并实际完成 imagegen 调用？ | `G9-HANDOFF` | `FAIL-SHEET-IMAGEGEN` | `N7-IMAGEGEN` / `references/imagegen-handoff.md#skill-dependency` | imagegen plan 记录 dependency loaded、`mode`、`batch_execution` 和无 CLI/API/provider 越权；results/report 记录 `imagegen_called` 与生成图路径 |
| 若存在本地 reference images，是否先逐张 `view_image` 进入对话上下文，再声明为视觉参照，而不是只写路径？ | `G11-REF-INPUT` | `FAIL-SHEET-IMAGEGEN` | `N6-REVIEW` / `N7-IMAGEGEN` | manifest / plan / report 记录 `reference_input_status: visible_in_conversation_context` 和每张图的角色标注 |
| imagegen 任务是否统一采用标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统，且没有传入项目全局风格词或场景光影氛围作为风格约束？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT-DRAFT` / `N7-IMAGEGEN` | plan `style_policy.visual_style` 正确，report 记录未使用 global style |
| imagegen 任务是否携带 `style_lock_spec`，并隔离完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感、胶片颗粒等词？ | `G2A-STYLE-LOCK` | `FAIL-SHEET-STYLE-LOCK` | `N5B-FINAL-PAYLOAD` / `N7-IMAGEGEN` | plan `style_lock_spec.upstream_style_quarantine` 与 `forbidden_rendering_layers` 可审计 |
| 每个任务是否包含完整 prompt、完整分镜组内容、`source_comprehension`、`style_lock_spec`、`storyboard_frame_units`、`visual_prompt_atoms`、`panel_description`、`character_name_labels`、`annotation_plan` 和 layout policy？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` / `FAIL-SHEET-PROMPT-ATOMS` | `N3A-FRAME-UNITS` / `N7-IMAGEGEN` | plan 中每个 task 含必需字段与源 frame-unit 追溯 |
| 可选 `spatial_handoff` 是否只作为空间证据使用，缺失时没有阻断 imagegen？ | `G8B-SPATIAL-HANDOFF` | `FAIL-SHEET-SPATIAL-HANDOFF` | `N5B-FINAL-PAYLOAD` / `N7-IMAGEGEN` | plan/report 记录 `spatial_handoff.status` 与 usage_policy |
| 生成结果是否持久化到 `projects/aigc/<项目名>/9-图像/分镜故事板/第N集/images/`，且不把 `$CODEX_HOME/generated_images` 当最终路径？ | `G10-PERSIST` | `FAIL-SHEET-IMAGEGEN` | `N8-PERSIST` / `.agents/skills/cli/imagegen/references/output-persistence.md` | `imagegen-results.json` 记录项目内 `output_image_path`、源路径、复制状态和存在性检查 |
