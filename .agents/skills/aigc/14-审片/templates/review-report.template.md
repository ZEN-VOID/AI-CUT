# <group_id><variant_suffix> 审片报告

## Input

- input_origin:
- video_path:
- project_root:
- group_id:
- variant:
- source_group_path:
- reviewed_at:

## LibTV Intake

- input_shape:
- canvas_url:
- canvas_name:
- projectUuid:
- video_node_name:
- video_node_key:
- remote_result_url:
- remote_task_id:
- remote_query_path:
- download_output_path:
- canonical_video_path:
- prompt_source:

## Evidence

- source_origin:
- duration:
- resolution:
- fps:
- audio_note:
- keyframe_summary:

## Observed Content

<实际视频内容概述>

## Method Selection

- selected_methods:
- skipped_methods:
- selection_reason:
- user_focus_coverage:
- advisor_focus_coverage:

## Expected From Group

<来自 10-分组的目标意图摘要>

## Prompt Alignment

- prompt_source:
- match_verdict:
- mismatch_owner:
- prompt_problem_evidence:
- model_problem_evidence:
- attribution_confidence:

## Creative Quality

- intrinsic_video_verdict:
- anti_banal_verdict:
- art_direction_note:
- aesthetic_integrity_note:
- rhythm_note:
- quality_verdict:

## Example Calibration

- example_inputs:
- good_example_signals:
- bad_example_signals:
- target_video_distance:
- reusable_learning_candidate:

## Review Advisor Packet

- 顾问与复核流程_mode:
- roster_source:
- consulted_members:
- node_pass_gate_refs:
- must_check:
- must_not_accept:
- quality_bar:
- rerun_or_repair_guidance:
- execution_brief:
- local_checklist:

## Findings

| id | method_id | dimension | severity | expected | actual | root_cause_guess | evidence | confidence | landing | chosen_operation |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |

## Operation Design

- candidate_operations:
- chosen_operations:
- rejected_operations_reason:
- authorization_required:
- closure_evidence:
- next_action:

## Landing Decision

- verdict:
- changed_files:
- rerun_recommendation:
- source_escalation:
- quality_learning:

## Thinking Process

- 为什么选择当前审片路径：
- 为什么选择这些审片方法，为什么跳过其他方法：
- 视频本身、prompt 匹配和创作质量三层如何综合：
- 顾问与复核流程的顾问参谋如何影响或没有影响本次判断：
- 如果不一致，为什么归因为 prompt / 模型 / 混合原因 / 证据缺口：
- 好/坏示例如何影响本次判断：
- 为什么这些 finding 应该这样落点：
- 为什么选择这些操作，为什么没有选择其他操作：
- 为什么没有/已经上升源层：

## Verification

- checks:
- libtv_checks:
  - project_resolved:
  - node_resolved:
  - remote_query_saved:
  - real_video_downloaded:
  - prompt_hygiene_checked:
  - rerun_closed:
- residual_risk:
