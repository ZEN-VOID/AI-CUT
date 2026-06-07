# Storyboard Sheet Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个分镜组的 storyboard prompt block |
| Output format | Markdown section that can be copied into `第N集-分镜故事板-prompts.md` |
| Output path | Rendered inside `projects/aigc/<项目名>/12-图像/分镜故事板/第N集/第N集-分镜故事板-prompts.md` |
| Naming convention | Section heading uses `## <分镜组ID>` |
| Completion gate | 任务执行前缀完整并声明黑白线稿基底、受控彩色标注系统、每个可见角色头顶黑色角色名、4K、锁定 16:9 panel image box、panel 下方 `rich_brief` 描述文字、基于 panel 数反推的 layout aspect decision 与 panel geometry blueprint；`Style Lock Spec` 隔离上游风格词；`Visual Prompt Atoms` 逐 panel 给出生图可执行原子；`Floor Plan To Panel Mapping` 逐 panel 回指 accepted floor plan；source comprehension、frame-unit plan 与 accepted spatial floor plan 可追溯；完整分镜组内容保留但只作为源证据；主体参照来自 YAML manifest 并用于身份/空间/道具保真 |

```markdown
## <分镜组ID>

Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a locked 16:9 image box with a visible rectangular border, plus a separate storyboard description text strip directly below that image box. Use the supplied Layout Aspect Decision and Panel Geometry Blueprint: draw the sheet according to the selected grid, normalized cell coordinates, fixed 16:9 image_box coordinates, text_strip coordinates, margins, and gutters. Do not squeeze, stretch, crop, or distort any panel image box to fill a mismatched cell; leave clean whitespace inside the cell if needed. Use pagination or multiple sheets when one legal canvas cannot preserve locked 16:9 image boxes and readable text strips. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable. Treat the Complete Group Source as evidence and source text, not as a visual style directive; upstream color, lighting, atmosphere, cinematic, lens, grain, film, rendering, or global style phrases are quarantined and must not override this black-and-white line-art style lock. Before drawing, obey the supplied Style Lock Spec, Visual Prompt Atoms, and Floor Plan To Panel Mapping; if any of those blocks are missing, stop and rework the prompt instead of generating.

### Style Lock Spec

- base_rendering: black_white_clean_line_art
- allowed_color_layer: annotation_only
- forbidden_rendering_layers:
  - color_cinematic_still
  - photorealistic_rendering
  - global_style_keywords
  - scene_lighting_atmosphere
  - costume_background_lighting_color_rendering
- upstream_style_quarantine:
  - source_phrase: <源文本中的上游风格句>
    treatment: evidence_only_not_style_directive
- reference_usage_policy: identity_silhouette_spatial_structure_prop_shape_only
- style_drift_stop_condition: missing_style_lock_or_color_rendering_terms_in_visual_prompt_atoms

### Source Comprehension

- narrative_function: <本组叙事功能>
- action_chain: <连续动作链>
- spatial_anchors: <空间锚点>
- character_state_anchors: <角色状态锚点>
- prop_state_anchors: <道具状态锚点>
- visual_turning_points: <视觉转折>
- must_preserve_source_facts: <必须保留的源事实>
- forbidden_inventions: <禁止补写项>

### Storyboard Frame Units

1. panel_no: 1
   panel_image_aspect_ratio: 16:9
   visual_beat: <该 panel 要表现的视觉节拍>
   panel_description: <rich_brief；从 source_span 和分组稿分镜描述原文保真精简为 1-2 句>
   panel_description_density: rich_brief
   character_name_labels:
     - <角色名>: above_character_head
   annotation_plan:
     red_body_movement_arrows: <身体运动方向；不适用写 none>
     blue_camera_movement_arrows: <摄影机运动方向；不适用写 none>
     green_framing_composition_marks: <取景/构图笔记；不适用写 none>
     orange_lighting_direction_marks: <灯光方向；不适用写 none>
     purple_emotion_sound_narrative_marks: <情绪/声音/叙事强调；不适用写 none>
     black_text_notes_and_panel_label: <简短镜头笔记和面板标签>
   source_shot_labels: <分镜N 或多个源分镜标签>
   source_span: <可回指的组正文片段或摘要>

### Visual Prompt Atoms

1. panel_no: 1
   draw_subjects: <本 panel 可见主体，角色名与 YAML 一致>
   subject_actions: <源文本可回指的动作/状态>
   spatial_positions: <来自 Floor Plan To Panel Mapping 的站位、朝向、相对距离>
   camera_framing: <源文本已有景别/构图/运镜；无则 none>
   line_art_instruction: black-and-white clean storyboard line art, clear silhouettes, no color rendering
   annotation_overlay: <红/蓝/绿/橙/紫/黑标注落点；不适用写 none>
   text_strip: <等于 panel_description>
   negative_prompt_atoms:
     - no color cinematic still
     - no photorealistic lighting
     - no rewritten character positions
     - no facts outside source_span

### Layout Aspect Decision

- panel_count: <storyboard_frame_units 数量>
- target_panel_image_aspect_ratio: 16:9
- effective_panel_slot_ratio: <计入文字区和安全边距后的单格槽位比例>
- panel_geometry_blueprint:
  - geometry_lock: fixed_16_9_image_boxes
  - max_panel_image_box_ratio_error: 0.06
  - outer_margin_pct: <0.035-0.05>
  - gutter_pct: <0.018-0.03>
  - text_strip_factor: <0.18-0.26>
  - image_box_policy: lock_16_9_inside_cell_leave_whitespace_if_needed
  - panels:
    - panel_no: 1
      cell_norm: { x: <0-1>, y: <0-1>, w: <0-1>, h: <0-1> }
      image_box_norm: { x: <0-1>, y: <0-1>, w: <0-1>, h: <0-1> }
      image_box_aspect_ratio: 16:9
      text_strip_norm: { x: <0-1>, y: <0-1>, w: <0-1>, h: <0-1> }
      ratio_error: <必须 <= 0.06>
- candidate_grids:
  - columns: <候选列数>
    rows: <候选行数>
    predicted_sheet_aspect_ratio: <候选整图比例>
    nearest_gpt_image_2_size: <合法 WIDTHxHEIGHT>
    panel_image_box_ratio_error: <单格图片区比例误差>
    readability_risk: <none | low | medium | high>
- selected_grid: <columns>x<rows>
- selected_sheet_aspect_ratio: <整图比例>
- selected_sheet_size: <gpt-image-2 合法 WIDTHxHEIGHT>
- pagination_or_multi_sheet_decision: <single_sheet | paginate | multiple_sheets>
- panel_image_box_ratio_error: <最终误差；必须 <= 0.06，否则分页或多 sheet>
- rationale: <选择理由>

### Accepted Spatial Floor Plan

- floor_plan_id: <分镜组ID>
- top_view_diagram_path: projects/aigc/<项目名>/12-图像/分镜故事板/第N集/floor-plans/<分镜组ID>.png
- acceptance_verdict: accepted
- scene_boundary: <场景边界、出入口、主要空间锚点>
- character_positions: <角色站位、朝向、相互距离；角色名与 YAML 一致>
- prop_positions: <关键道具位置及与角色/场景关系>
- camera_plan: <每个 panel 或视觉节拍的摄影机位置、方向、视野锥和运动路径>
- continuity_from_previous: <与上一张 accepted floor plan 相比的不变锚点、变化项和移动逻辑>

### Floor Plan To Panel Mapping

1. panel_no: 1
   floor_plan_zone: <对应平面图区域/镜头锥>
   characters_position_and_facing: <角色站位、朝向、相互距离>
   props_position: <道具位置>
   camera_position_and_direction: <摄影机位置、方向和视野锥>
   movement_path_used: <使用哪条运动路径；无则 none>
   unchanged_anchors_from_floor_plan: <保持不变的空间锚点>
   allowed_composition_variation: <仅限景别、裁切、透视转换>
   forbidden_spatial_drift: <不得改变的左右/内外/前后/朝向关系>

### Complete Group Source From 10-分组

<直接粘贴 10-分组 中该分镜组完整内容，包含组正文和底部 fenced YAML>

### Reference Subjects

Characters:
- <角色名>: <图片路径或 missing>

Scene:
- <场景名>: <图片路径或 missing>
  visual_anchor: spatial_structure_and_subject_identity

Props:
- <道具名>: <图片路径或 missing>
```
