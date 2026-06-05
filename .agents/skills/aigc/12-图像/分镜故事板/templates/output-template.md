# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、group index、reference manifest、imagegen plan/result、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/12-图像/分镜故事板/第N集/` |
| Naming convention | `第N集-分镜故事板-prompts.md`、`第N集-group-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`images/<分镜组ID>.png`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo` |

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
- panel_image_aspect_ratio_default: 16:9
- panel_text_position: below_each_panel_image
- layout_policy: auto_adapt_to_total_storyboard_frame_units
- annotation_color_system:
  - red_arrows: body_movement
  - blue_arrows: camera_movement
  - green_marks: framing_composition_notes
  - orange_marks: lighting_direction
  - purple_marks: emotion_sound_narrative_emphasis
  - black_text: character_name_labels_above_heads_short_shot_notes_and_panel_labels
- character_name_label_status:
- prompted:
- generated:
- skipped:
- failed:
- missing_references:

## Frame Unit Mapping

- frame_unit_status:
- mapping_policy: visual_beat_based_not_one_to_one_with_source_shot_labels
- panel_description_status:
- panel_description_density: rich_brief
- character_name_label_status:
- annotation_plan_status:
- complete_group_source_status:
- partial_or_ambiguous_groups:

## Reference Context

- reference_input_status:
- viewed_reference_images:
- missing_reference_images:
- subject_fidelity_anchor_status:
- global_style_usage: forbidden
- color_rendering_usage: forbidden_except_annotation_system

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
