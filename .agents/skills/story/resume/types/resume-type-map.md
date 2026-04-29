# Resume Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


`types/` 是 `$story-resume` 的恢复分型真源。执行时先形成 `resume_type_profile`，再让 `steps/resume-workflow.md` 消费它。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `detect_state` | `tracked`, `artifact_fallback`, `none`, `conflict`, `unavailable` | workflow 检测和业务证据状态 |
| `tracked_command` | `story-init`, `story-cards`, `story-plan`, `story-write`, `story-validate`, `story-review`, `story-return`, `story-query`, `unknown` | tracked run 的命令归属 |
| `stage_owner` | `0-初始化`, `1-设定`, `2-卷章`, `3-初稿`, `review`, `return`, `query`, `manual` | 下一入口 owner |
| `recovery_mode` | `tracked_workflow_resume`, `artifact_fallback_resume`, `query_light_resume`, `write_cleanup_resume`, `review_decision_resume`, `manual_diagnosis`, `blocked_safety_stop` | 本轮恢复模式 |
| `risk_level` | `low`, `medium`, `high`, `blocked` | 执行或建议风险 |
| `confirmation_required` | `none`, `user_choice`, `cleanup_confirm`, `manual_decision` | 是否必须等待用户确认 |
| `output_type` | `chat_report`, `report_file`, `command_execution_summary`, `blocker` | 输出形态 |

## Command Mapping

| command signal | recovery mode | allowed action | forbidden action | review gate |
| --- | --- | --- | --- | --- |
| `story-init` | `tracked_workflow_resume` | generic continue / clear / rerun advice | 套用章节 cleanup | `generic_run_gate` |
| `story-cards` | `tracked_workflow_resume` | generic continue / clear / rerun advice | 直接补卡片真源 | `generic_run_gate` |
| `story-plan` | `tracked_workflow_resume` | generic continue / clear / rerun advice | 直接重写规划 | `generic_run_gate` |
| `story-write` Step 1 | `tracked_workflow_resume` | 重新做 Step 1 或继续当前工序 | 删除正文且无确认 | `write_resume_gate` |
| `story-write` Step 2-8 | `write_cleanup_resume` 或 `tracked_workflow_resume` | 继续当前工序；或 preview cleanup 后重跑 | 未 preview 直接 confirm cleanup | `cleanup_gate` |
| `story-validate` | `tracked_workflow_resume` | generic continue / clear / rerun advice | 直接改写 validation 结果 | `validation_resume_gate` |
| `story-review` Step 1-6 | `tracked_workflow_resume` | 核对输入未变后继续 | 跳过 validation 输入检查 | `review_resume_gate` |
| `story-review` Step 7 | `review_decision_resume` | 重新向用户确认关键问题处理策略 | 自动替用户裁决 | `human_decision_gate` |
| `story-review` Step 8 | `tracked_workflow_resume` | 收尾或重新完成任务 | 改写审查真源 | `review_resume_gate` |
| `story-return` | `tracked_workflow_resume` | generic continue / clear / rerun advice | 由 resume 直接 actualize | `context_return_boundary_gate` |
| `story-query` | `query_light_resume` | generic continue / rerun / diagnosis | 章节 cleanup | `query_light_gate` |
| `unknown` | `manual_diagnosis` | 保留现场并诊断 | 伪造 tracked workflow | `manual_gate` |

## Artifact Fallback Mapping

| fallback reason | evidence | next entry | risk | gate |
| --- | --- | --- | --- | --- |
| `上下文回流_completed_next_volume_ready` | `context-return/第V卷.context-return.json` | `story-write` 下一卷首章 | `low` | 列 carryover context |
| `validation_pass_review_pending` | `review/第V卷.validation.json` PASS，无 review 持久化 | `story-review` | `low` | 核对 validation packet |
| `validation_pass_review_persisted_上下文回流_pending` | validation PASS + `review/*章审查报告.md` / `STATE.json.review_checkpoints` | `story-return` | `low` | 不由 resume actualize |
| `validation_pass_context_return_gate_not_ready` | validation PASS 但缺 `handoff_to_review_and_context_return`、`return` handoff 或 accepted manuscript lock | `story-review` / `4-润色` 路由确认 | `medium` | 不把 PASS-only 当 actualization 权限 |
| `candidate_volume_draft_waiting_validation` | `3-初稿/第V卷.写作日志.yaml` 到 candidate draft | `story-review` | `medium` | 核对 draft batch |
| `validation_failed_back_to_drafting` | validation FAIL + drafting route | `3-初稿` rework target | `medium` | 按 rework targets |
| `validation_failed_back_to_source_contract` | validation FAIL + source trace | `0-初始化` / `1-设定` / `2-卷章` | `high` | 不发明 repair 内容 |

## Risk Matrix

| signal | risk_level | required confirmation | route impact |
| --- | --- | --- | --- |
| 只读取 detect / preflight | `low` | `none` | 可直接报告 |
| 继续当前非破坏性步骤 | `low` to `medium` | `user_choice` | 回对应 stage |
| cleanup preview | `medium` | `user_choice` | 只预览，不删除 |
| cleanup confirm | `high` | `cleanup_confirm` | 必须用户明确确认 |
| review Step 7 | `high` | `manual_decision` | 必须用户裁决 |
| Git hard reset / 未备份删除 | `blocked` | n/a | block |

## Fusion Rules

1. 先由 `detect_state` 决定 tracked / fallback / none / conflict。
2. tracked 状态再看 `tracked_command`，`story-query` 永远降到轻量恢复。
3. fallback 状态必须列 evidence files，并收敛到唯一 `stage_owner`。
4. 任何 cleanup confirm 都必须经过 `review/resume-review-gate.md`。
5. 若 `stage_owner` 多于一个，输出 blocker，不输出“任选其一”。
