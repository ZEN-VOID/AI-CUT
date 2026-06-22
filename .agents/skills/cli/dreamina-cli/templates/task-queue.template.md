# Dreamina Queue Ledger

## Use Rules

- One row should represent one submitted Dreamina job or one user-approved grouped batch.
- Update this file manually after every `dreamina query_result`, `dreamina list_task`, or download action.
- Do not delete historical rows just because they are complete; move them to the history table or mark them closed.
- `submit_id` is mandatory for any row that should be follow-up runnable.
- Standalone default ledger root is `output/dreamina/<项目名>/`; standalone download root is `output/dreamina/<项目名>/<模型名称>/`.
- If this ledger belongs to an `aigc2026` downstream call, keep the caller's stage path and only use this template as the record shape.

## Active Queue

| queue_id | asset_kind | task_type | submit_id | local_status | remote_status | created_at | last_checked_at | next_action | output_path | prompt_summary | inputs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-001 | video | text2video | submit_xxx | submitted | queued | 2026-04-01 19:30 PDT | 2026-04-01 19:31 PDT | 20 minutes later run `dreamina query_result --submit_id=submit_xxx` | output/dreamina/示例项目/seedance2.0fast/demo-01.mp4 | 镜头推进，角色从门口走入庭院 | none | first batch |

## Update Log

| time | queue_id | command | summary | next_action | operator_notes |
| --- | --- | --- | --- | --- | --- |
| 2026-04-01 19:31 PDT | Q-001 | `dreamina text2video --poll=30 ...` | poll timed out, kept `submit_id` | 20 minutes later query again | initial submit |

## History

| queue_id | final_status | closed_at | result_path | closure_note |
| --- | --- | --- | --- | --- |
| Q-000 | downloaded | 2026-04-01 18:20 PDT | output/dreamina/示例项目/seedance2.0fast/archive-demo.mp4 | verified and archived |

## Suggested Status Vocabulary

- `submitted`: CLI accepted the task, first remote state not fully confirmed yet
- `queued`: accepted remotely and waiting for execution
- `running`: actively generating
- `querying`: poll timed out, waiting for manual follow-up query
- `success`: remote result is ready
- `downloaded`: result already fetched locally
- `failed`: remote task ended in failure
- `manual_hold`: intentionally paused by operator
- `abandoned`: no further follow-up planned
