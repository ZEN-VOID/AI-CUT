# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、shot index、reference manifest、imagegen plan/result、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/7-图像/A-分镜画面`，逐集文件组织在其下的 `第N集/` 子目录 |
| Naming convention | `第N集-分镜画面-prompts.md`、`第N集-shot-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`images/<分镜ID>.png`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo`; scene reference visual style lock is visible or explicitly missing; same-scene previous generated frames have been reviewed or have explicit missing/not-applicable reasons; 3D spatial continuity plan is present; complete prompts document is persisted before imagegen; batch execution is strictly serial by `shot_id` |

## Episode Directory Shape

```text
projects/aigc/<项目名>/7-图像/A-分镜画面/
└── 第N集/
    ├── 第N集-分镜画面-prompts.md
    ├── 第N集-shot-index.json
    ├── 第N集-reference-manifest.json
    ├── 第N集-imagegen-plan.json
    ├── 第N集-imagegen-results.json
    ├── images/
    │   └── <分镜ID>.png
    └── 执行报告.md
```

## Execution Report Template

```markdown
# 第N集 A-分镜画面执行报告

## Input

- project_root:
- source_group_path:
- north_star_path:
- mode:
- scope:

## Summary

- total_shots:
- prompted:
- generated:
- skipped:
- failed:

## Reference Context

- reference_input_status:
- viewed_reference_images:
- missing_reference_images:

## Prompt Package Gate

- prompt_package_status:
- prompts_path:
- manifest_path:
- plan_path:
- covered_shot_ids:
- package_completed_before_imagegen:

## Scene Visual Style Lock

- scene_visual_style_lock_status:
- viewed_scene_reference_images:
- fixed_prompt: `画面风格，光影，色调和氛围与场景参照图保持一致。`
- lighting_notes:
- color_palette_notes:
- atmosphere_notes:
- material_notes:

## Previous Frame Continuity

- previous_frame_context_status:
- viewed_previous_frame_images:
- missing_or_not_applicable_previous_frames:
- continuity_notes:

## 3D Spatial Continuity

- scene_space_model_status:
- shot_anchor_projection_status:
- source_frame_anchor_evidence:
- fixed_anchors:
- character_position_notes:
- movement_path_notes:
- camera_axis_notes:
- shot_reverse_shot_notes:

## Serial Batch Execution

- execution_mode: serial_by_shot_id
- execution_order:
- completed_serial_indices:
- blocked_serial_indices:
- previous_shot_status_notes:
- runtime_previous_frame_context_notes:

## Review

```yaml
verdict:
checked_gates: []
todos: []
```

## Failed Or Skipped

| shot_id | status | reason | rework_entry |
| --- | --- | --- | --- |
```
