# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | group index、组级多图 prompt 文档、reference manifest、GPT-IMAGE-2 multi-image plan/result、独立图片、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/12-图像/分镜画面`，逐集文件组织在 `第N集/` 子目录 |
| Naming convention | `第N集-分镜画面-prompts.md`、`第N集-group-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`第N集-imagegen-results.json`、`images/<shot_id>.png`、`执行报告.md` |
| Completion gate | 每组一个 `multi_image_task`；`n == shot_count`；默认 `aspect_ratio=16:9`，只有用户显式要求时才使用 override；返回图片数匹配；不是拼图；每张独立落盘；报告证据完整 |

## Episode Directory Shape

```text
projects/aigc/<项目名>/12-图像/分镜画面/
└── 第N集/
    ├── 第N集-分镜画面-prompts.md
    ├── 第N集-group-index.json
    ├── 第N集-reference-manifest.json
    ├── 第N集-imagegen-plan.json
    ├── 第N集-imagegen-results.json
    ├── images/
    │   └── <shot_id>.png
    └── 执行报告.md
```

## Execution Report Template

```markdown
# 第N集 分镜画面执行报告

## Input

- project_root:
- source_group_path:
- project_style_context:
- mode:
- scope:

## Summary

- total_groups:
- total_shot_points:
- prompted_groups:
- generated_groups:
- generated_images:
- skipped:
- failed:

## Group Source Lock

- group_full_content_status:
- processed_group_ids:
- skipped_connectors:
- unresolved_groups:

## Shot Count And Mapping

| group_id | shot_count | prompt_sections | plan_n | returned_count | verdict |
| --- | ---: | ---: | ---: | ---: | --- |

## Reference Context

- reference_input_status:
- viewed_reference_images:
- missing_reference_images:
- yaml_subject_binding_notes:

## Multi-Image Prompt Gate

- task_execution_prefix_status:
- non_collage_constraint:
- consistency_contract_status:
- prompts_path:
- covered_group_ids:

## GPT-IMAGE-2 Handoff

- call_mode: gpt_image_2_multi_image_group
- model: gpt-image-2
- aspect_ratio:
- aspect_ratio_override:
- provider_cap:
- provider_cap_override:
- blocked_over_cap_groups:
- plan_path:

## Result Mapping

| group_id | image_index | shot_id | output_image_path | status |
| --- | ---: | --- | --- | --- |

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |

## Rule Evidence Map

| rule | evidence | output_location | verdict |
| --- | --- | --- | --- |

## N/A Justification

| item | reason |
| --- | --- |

## Repair Log

| fail_code | rework_target | action | result |
| --- | --- | --- | --- |

## Review

```yaml
verdict:
checked_gates: []
todos: []
```

## Failed Or Skipped

| group_id | shot_id | status | reason | rework_entry |
| --- | --- | --- | --- | --- |
```
