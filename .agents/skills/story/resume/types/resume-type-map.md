# Resume Type Map

## 类型包加载边界

- 本文件只在 `SKILL.md` 的 `Type Routing Matrix` 或 `Module Trigger Matrix` 命中 `types/resume-type-map.md` 时加载。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


`SKILL.md` 的 `Type Routing Matrix` 是 `$story-resume` 的恢复分型真源。本文件只展开命令映射、fallback 映射和风险矩阵；执行时先形成 `resume_type_profile`，再回到 `SKILL.md` 的 `Thinking-Action Node Map` 消费它。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `detect_state` | `tracked`, `artifact_fallback`, `none`, `conflict`, `unavailable` | workflow 检测和业务证据状态 |
| `tracked_command` | `story-init`, `story-cards`, `story-plan`, `story-write`, `story-polishing`, `story-return`, `story-query`, `unknown` | tracked run 的命令归属 |
| `stage_owner` | `0-初始化`, `1-设定`, `2-卷章`, `3-初稿`, `4-润色`, `return`, `query`, `manual` | 下一入口 owner |
| `recovery_mode` | `tracked_workflow_resume`, `artifact_fallback_resume`, `query_light_resume`, `write_cleanup_resume`, `acceptance_decision_resume`, `manual_diagnosis`, `blocked_safety_stop` | 本轮恢复模式 |
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
| `story-polishing` | `tracked_workflow_resume` 或 `acceptance_decision_resume` | 继续润色主创、P5 内置验收或回到 owning stage 修复 | 直接改写验收结果 | `acceptance_resume_gate` |
| `story-return` | `tracked_workflow_resume` | generic continue / clear / rerun advice | 由 resume 直接 actualize | `context_return_boundary_gate` |
| `story-query` | `query_light_resume` | generic continue / rerun / diagnosis | 章节 cleanup | `query_light_gate` |
| `unknown` | `manual_diagnosis` | 保留现场并诊断 | 伪造 tracked workflow | `manual_gate` |

## Artifact Fallback Mapping

| fallback reason | evidence | next entry | risk | gate |
| --- | --- | --- | --- | --- |
| `上下文回流_completed_next_volume_ready` | `context-return/第V卷.context-return.json` | `story-write` 下一卷首章 | `low` | 列 carryover context |
| `draft_acceptance_pass_polish_pending` | `3-初稿/第N卷/第N章.acceptance.json` PASS 且 handoff `4-润色` | `4-润色` | `low` | 核对 draft acceptance packet |
| `polish_acceptance_pass_return_pending` | `4-润色/第N卷/第N章.acceptance.json` PASS 且 handoff `return` | `story-return` | `low` | 不由 resume actualize |
| `acceptance_pass_return_gate_not_ready` | acceptance PASS 但缺 `return` handoff 或 accepted manuscript lock | `4-润色` 路由确认 | `medium` | 不把 PASS-only 当 actualization 权限 |
| `candidate_volume_draft_waiting_acceptance` | `3-初稿/第V卷.写作日志.yaml` 到 candidate draft | `3-初稿` 内置验收 | `medium` | 核对 draft batch |
| `acceptance_failed_back_to_drafting` | acceptance FAIL + drafting route | `3-初稿` rework target | `medium` | 按 rework targets |
| `acceptance_failed_back_to_source_contract` | acceptance FAIL + source trace | `0-初始化` / `1-设定` / `2-卷章` | `high` | 不发明 repair 内容 |

## Risk Matrix

| signal | risk_level | required confirmation | route impact |
| --- | --- | --- | --- |
| 只读取 detect / preflight | `low` | `none` | 可直接报告 |
| 继续当前非破坏性步骤 | `low` to `medium` | `user_choice` | 回对应 stage |
| cleanup preview | `medium` | `user_choice` | 只预览，不删除 |
| cleanup confirm | `high` | `cleanup_confirm` | 必须用户明确确认 |
| acceptance decision | `high` | `manual_decision` | 必须用户裁决 |
| Git hard reset / 未备份删除 | `blocked` | n/a | block |

## Fusion Rules

1. 先由 `detect_state` 决定 tracked / fallback / none / conflict。
2. tracked 状态再看 `tracked_command`，`story-query` 永远降到轻量恢复。
3. fallback 状态必须列 evidence files，并收敛到唯一 `stage_owner`。
4. 任何 cleanup confirm 都必须经过 `review/resume-review-gate.md`。
5. 若 `stage_owner` 多于一个，输出 blocker，不输出“任选其一”。
