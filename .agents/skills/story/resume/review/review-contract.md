# Story Resume Review Contract

本文件是 `$story-resume` 的 canonical review 合同。`review/resume-review-gate.md` 保留更细的 checklist 和 provider 降级说明；本文件只承接 Skill 2.0 validator / smoke test 对 `review/review-contract.md` 的默认入口要求。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 恢复裁决可交付，且项目根、证据、风险、确认、唯一下一入口和 truth boundary 全部通过。 |
| `pass_with_followups` | 可交付，但存在非阻断后续补件；不得包含危险动作、证据缺失或多入口。 |
| `needs_rework` | 证据链、风险标注、用户确认或唯一下一入口存在阻断缺陷。 |
| `blocked` | 项目根、权限、证据冲突、用户意图或安全规则阻断恢复裁决。 |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否已唯一锁定项目根或输出最小追问？ | 缺 `STATE.json` project root 不得继续 | `FAIL-RESUME-ROOT` | `SKILL.md#N2-PREFLIGHT` | project_root、preflight 摘要 |
| 是否已执行或消费 detect，并在无 tracked 中断时检查 fallback？ | 无证据判断断点即失败 | `FAIL-RESUME-EVIDENCE` | `SKILL.md#N3-DETECT` | detect payload、fallback files |
| 是否过滤危险动作并按风险等待确认？ | cleanup confirm 无 preview 或用户确认即失败 | `FAIL-RESUME-SAFETY` | `SKILL.md#N5-NORMALIZE` | risk_level、confirmation_required |
| 是否输出唯一 handoff 或 blocker？ | 多个 next entry 即失败 | `FAIL-RESUME-OUTPUT` | `SKILL.md#N8-CLOSURE` | next_stage_handoff、blockers |
