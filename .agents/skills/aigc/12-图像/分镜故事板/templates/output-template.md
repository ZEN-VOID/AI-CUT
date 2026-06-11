# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、group index、reference manifest、imagegen plan/result、通过 `.agents/skills/cli/imagegen` 直接生成并持久化的 storyboard sheet 图片、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/12-图像/分镜故事板/第N集/` |
| Naming convention | `第N集-分镜故事板-prompts.md`、`第N集-group-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`第N集-imagegen-results.json`、`images/<分镜组ID>.png`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo` only after `.agents/skills/cli/imagegen` has been called and every target group has a persisted storyboard sheet image path; prompt-only / review-only / waiting-confirmation / imagegen-plan-only states cannot complete |

## Episode Directory Shape

```text
projects/aigc/<项目名>/12-图像/分镜故事板/第N集/
├── 第N集-分镜故事板-prompts.md
├── 第N集-group-index.json
├── 第N集-reference-manifest.json
├── 第N集-imagegen-plan.json
├── 第N集-imagegen-results.json
├── images/
│   └── <分镜组ID>.png
└── 执行报告.md
```

## Execution Report Template

```markdown
# 第N集 分镜故事板执行报告

## Input

- project_root:
- source_group_path:
- mode:
- scope:

## Summary

- total_groups:
- total_storyboard_frame_units:
- resolution_target: 4K
- visual_style: standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors
- style_lock_policy: complete_group_source_is_evidence_only_not_visual_style_directive
- panel_image_aspect_ratio_default: locked_16_9_image_box
- panel_text_position: below_each_panel_image
- layout_policy: use_layout_aspect_decision
- spatial_handoff_policy: optional_from_分镜平面图_not_completion_gate
- visual_prompt_atoms_policy: required_per_panel_before_imagegen
- annotation_color_system:
  - red_arrows: body_movement
  - blue_arrows: camera_movement
  - green_marks: framing_composition_notes
  - orange_marks: lighting_direction
  - purple_marks: emotion_sound_narrative_emphasis
  - black_text: character_name_labels_above_heads_short_shot_notes_and_panel_labels
- prompted:
- generated:
- generated_image_paths:
  - group_id:
    path:
- skipped:
- failed:
- missing_references:

## Frame Unit Mapping

- source_comprehension_status:
- source_comprehension_evidence:
  - narrative_function:
  - action_chain:
  - spatial_anchors:
  - character_state_anchors:
  - prop_state_anchors:
  - visual_turning_points:
  - must_preserve_source_facts:
  - forbidden_inventions:
- frame_unit_status:
- mapping_policy: visual_beat_based_not_one_to_one_with_source_shot_labels
- panel_description_status:
- panel_description_density: rich_brief
- character_name_label_status:
- annotation_plan_status:
- complete_group_source_status:
- partial_or_ambiguous_groups:

## Style Lock And Prompt Atoms

- style_lock_status:
- upstream_style_quarantine_status:
- visual_prompt_atoms_status:
- atom_fields_checked:
  - draw_subjects
  - subject_actions
  - spatial_positions
  - camera_framing
  - line_art_instruction
  - annotation_overlay
  - text_strip
  - negative_prompt_atoms
- prompt_atom_rework_groups:

## Layout Aspect Decision

- layout_aspect_status:
- panel_count_source: storyboard_frame_units.length
- target_panel_image_aspect_ratio:
- effective_panel_slot_ratio:
- panel_geometry_blueprint_status:
- max_panel_image_box_ratio_error:
- selected_grid:
- selected_sheet_aspect_ratio:
- selected_sheet_size:
- pagination_or_multi_sheet_decision:
- layout_risk_groups:

## Optional Spatial Handoff

- spatial_handoff_status: none | available | consumed | conflict | misused
- source: 分镜平面图
- consumed_groups:
- conflicts_or_misuse:
- handling: missing_handoff_does_not_block_storyboard_generation

## Reference Context

- reference_input_status:
- viewed_reference_images:
- missing_reference_images:
- subject_fidelity_anchor_status:
- global_style_usage: forbidden
- color_rendering_usage: forbidden_except_annotation_system

## Imagegen Execution

- dependency: .agents/skills/cli/imagegen/SKILL.md + .agents/skills/cli/imagegen/CONTEXT.md
- direct_call_required: true
- imagegen_called:
- plan_only_status: forbidden_as_completion_state
- persisted_storyboard_images:

## Review

```yaml
verdict:
checked_gates: []
todos: []
```

## Failed Or Skipped

| group_id | status | reason | rework_entry |
| --- | --- | --- | --- |
```
