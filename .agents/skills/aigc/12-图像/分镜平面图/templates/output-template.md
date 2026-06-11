# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、floor-plan index、reference manifest、spatial continuity manifest、imagegen plan/result、通过 `.agents/skills/cli/imagegen` 直接生成并持久化的 floor plan sheet 图片、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/12-图像/分镜平面图/第N集/` |
| Naming convention | `第N集-分镜平面图-prompts.md`、`第N集-floor-plan-index.json`、`第N集-reference-manifest.json`、`第N集-spatial-continuity-manifest.json`、`第N集-imagegen-plan.json`、`第N集-imagegen-results.json`、`floor-plan-sheets/<分镜组ID>.png`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo` only after `.agents/skills/cli/imagegen` has been called and every target group has a persisted floor plan sheet image path or explicit failed status; imagegen-plan-only cannot complete |

## Episode Directory Shape

```text
projects/aigc/<项目名>/12-图像/分镜平面图/第N集/
├── 第N集-分镜平面图-prompts.md
├── 第N集-floor-plan-index.json
├── 第N集-reference-manifest.json
├── 第N集-spatial-continuity-manifest.json
├── 第N集-imagegen-plan.json
├── 第N集-imagegen-results.json
├── floor-plan-sheets/
│   └── <分镜组ID>.png
└── 执行报告.md
```

## Execution Report Template

```markdown
# 第N集 分镜平面图执行报告

## Input

- project_root:
- source_group_path:
- mode:
- scope:

## Summary

- total_groups:
- generated:
- skipped:
- failed:
- generated_image_paths:
  - group_id:
    path:
- visual_contract: top_down_black_white_architectural_floor_plan_sheet
- character_icon_policy: colored_geometric_icons_with_black_name_labels
- annotation_color_system:
  - red_arrows: body_movement
  - blue_arrows: camera_movement_camera_direction_field_of_view
  - green_marks: framing_composition
  - orange_marks: lighting_direction
  - purple_marks: emotion_sound_narrative_emphasis
  - black_text: character_names_anchor_labels_panel_labels

## Source And Panels

- source_trace_status:
- source_spatial_comprehension_status:
- floor_plan_panels_status:
- panel_count_by_group:
- scripted_projection_check:

## Diagram Contract

- diagram_standard_status:
- character_icon_legend_status:
- annotation_color_status:
- negative_prompt_atoms_status:
- perspective_or_storyboard_drift:

## Continuity

- continuity_manifest:
- initial_groups:
- consistent_groups:
- needs_rework_groups:
- failed_groups:

## Imagegen

- dependency: .agents/skills/cli/imagegen/SKILL.md + .agents/skills/cli/imagegen/CONTEXT.md
- direct_call_required: true
- imagegen_called:
- imagegen_mode:
- resolution_target: 4K
- output_root:
- reference_input_status:
- persisted_results:

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
