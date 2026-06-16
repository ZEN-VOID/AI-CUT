# Storyboard Sheet Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个分镜组的 storyboard prompt block |
| Output format | Markdown section that can be copied into `第N集-分镜故事板-prompts.md` |
| Output path | Rendered inside `projects/aigc/<项目名>/9-图像/分镜故事板/第N集/第N集-分镜故事板-prompts.md` |
| Naming convention | Section heading uses `## <分镜组ID>` |
| Completion gate | 任务执行前缀完整并声明黑白线稿基底、受控彩色标注系统、每个可见角色头顶黑色角色名、4K、锁定 16:9 panel image box、panel 下方 `rich_brief` 描述文字、基于 panel 数反推的 layout aspect decision 与 panel geometry blueprint；`Style Lock Spec` 隔离上游风格词；`Visual Prompt Atoms` 逐 panel 给出生图可执行原子；source comprehension、frame-unit plan 与完整分镜组内容可追溯；可选 `Spatial Handoff` 仅来自 `分镜平面图` accepted 侧车且缺失不阻断 |

```markdown
## <分镜组ID>

Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a locked 16:9 image box with a visible rectangular border, plus a separate storyboard description text strip directly below that image box. Use the supplied Layout Aspect Decision and Panel Geometry Blueprint: draw the sheet according to the selected grid, normalized cell coordinates, fixed 16:9 image_box coordinates, text_strip coordinates, margins, and gutters. Do not squeeze, stretch, crop, or distort any panel image box to fill a mismatched cell; leave clean whitespace inside the cell if needed. Use pagination or multiple sheets when one legal canvas cannot preserve locked 16:9 image boxes and readable text strips. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable. Treat the Complete Group Source as evidence and source text, not as a visual style directive; upstream color, lighting, atmosphere, cinematic, lens, grain, film, rendering, or global style phrases are quarantined and must not override this black-and-white line-art style lock. Before drawing, obey the supplied Style Lock Spec, Source Comprehension, Storyboard Frame Units, Layout Aspect Decision, Visual Prompt Atoms, and Reference Subjects; if any required block is missing, stop and rework the prompt instead of generating.

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
- spatial_anchors: <源正文里的空间锚点、进出场、相对方位>
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
- selected_grid: <columns>x<rows>
- selected_sheet_aspect_ratio: <整图比例>
- selected_sheet_size: <适配 imagegen 4K 目标的 WIDTHxHEIGHT 或 N/A>
- pagination_or_multi_sheet_decision: <single_sheet | paginate | multiple_sheets>
- rationale: <选择理由>

### Visual Prompt Atoms

1. panel_no: 1
   draw_subjects: <本 panel 可见主体，角色名与 YAML 一致>
   subject_actions: <源文本可回指的动作/状态>
   spatial_positions: <来自源空间锚点；如有可选 Spatial Handoff，可补充但不得替代源理解>
   camera_framing: <源文本已有景别/构图/运镜；无则 none>
   line_art_instruction: black-and-white clean storyboard line art, clear silhouettes, no color rendering
   annotation_overlay: <红/蓝/绿/橙/紫/黑标注落点；不适用写 none>
   text_strip: <等于 panel_description>
   negative_prompt_atoms:
     - no color cinematic still
     - no photorealistic lighting
     - no rewritten character positions
     - no facts outside source_span

### Spatial Handoff

- status: none | consumed
- source_skill: 分镜平面图
- accepted_floor_plan_sheet_path: <仅当已存在且已验收时填写；缺失写 none>
- usable_constraints: <可消费的角色站位、动线、机位、空间连续性约束；缺失写 none>
- usage_policy: evidence_only_not_storyboard_completion_gate

### Complete Group Source From 8-分组

<直接粘贴 8-分组 中该分镜组完整内容，包含组正文和底部 fenced YAML>

### Reference Subjects

Characters:
- <角色名>: <图片路径或 missing>

Scene:
- <场景名>: <图片路径或 missing>
  visual_anchor: spatial_structure_and_subject_identity

Props:
- <道具名>: <图片路径或 missing>
```
