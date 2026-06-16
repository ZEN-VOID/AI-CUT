# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | group index、组级多图 prompt 文档、reference manifest、imagegen plan/result、独立图片、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/<项目名>/9-图像/分镜画面`，逐集文件组织在 `第N集/` 子目录 |
| Naming convention | `第N集-分镜画面-prompts.md`、`第N集-group-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`第N集-imagegen-results.json`、`images/<shot_id>.png`、`执行报告.md` |
| Completion gate | 每组一个 group imagegen package；`expected_image_count == shot_count`；默认 `aspect_ratio=16:9`，只有用户显式要求时才使用 override；生成图片数匹配；不是拼图；每张独立落盘到项目目录；报告证据完整 |

## Episode Directory Shape

```text
projects/aigc/<项目名>/9-图像/分镜画面/
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

| group_id | shot_count | prompt_sections | expected_image_count | returned_count | verdict |
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

## Image Upstream Visual Direction Matrix

| upstream_context | direction_role | used_as | stage_decision | prompt_or_output_anchor | boundary_check | evidence_map |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Imagegen Handoff

- imagegen_skill: .agents/skills/cli/imagegen
- execution_route: built_in_image_gen
- batch_execution:
- aspect_ratio:
- aspect_ratio_override:
- max_concurrency: 10
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
