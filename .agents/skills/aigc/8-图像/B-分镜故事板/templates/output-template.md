# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、group index、reference manifest、imagegen plan/result、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/8-图像/B-分镜故事板/第N集/` |
| Naming convention | `第N集-分镜故事板-prompts.md`、`第N集-group-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`images/<分镜组ID>.png`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo` |

## Episode Directory Shape

```text
projects/aigc/<项目名>/8-图像/B-分镜故事板/第N集/
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
# 第N集 B-分镜故事板执行报告

## Input

- project_root:
- source_group_path:
- mode:
- scope:

## Summary

- total_groups:
- total_storyboard_frame_units:
- resolution_target: 4K
- prompted:
- generated:
- skipped:
- failed:
- missing_references:

## Frame Unit Mapping

- frame_unit_status:
- mapping_policy: visual_beat_based_not_one_to_one_with_source_shot_labels
- partial_or_ambiguous_groups:

## Reference Context

- reference_input_status:
- viewed_reference_images:
- missing_reference_images:
- scene_visual_anchor_status:

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
