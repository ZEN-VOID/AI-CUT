# Resume Review Contract

本文件是 `$aigc-resume` 的 canonical review wrapper，用于兼容 Skill 2.0 smoke test 默认读取的 `review/review-contract.md`。详细 gate 仍由同目录 `resume-review-gate.md` 展开；本文件不新增第二审查真源。

## Output Contract Alignment

| Output Contract field | Review alignment |
| --- | --- |
| Required output | 恢复裁决包必须包含项目根、证据摘要、恢复模式、风险等级、治理缺口、唯一下一入口、安全边界和最小修复项 |
| Output format | Markdown 用户-facing 恢复报告；必要时附 YAML/JSON patch 建议 |
| Output path | 默认不落盘；用户要求时写入 `projects/aigc/<项目名>/resume/resume-report-YYYYMMDD.md` |
| Naming convention | `resume-report-YYYYMMDD.md`；恢复模式使用 ASCII-safe mode id |
| Completion gate | 项目根已锁定、证据链可复核、风险已标注、禁止动作已过滤、唯一下一入口已给出 |

## Verdict

| verdict | condition |
| --- | --- |
| `pass` | 项目根、证据链、风险、禁止动作和唯一下一入口全部满足 |
| `pass_with_followups` | 唯一入口安全，但存在非阻断治理补齐项 |
| `blocked` | 项目根不唯一、证据不足、高风险 gate 缺失或下一入口无法唯一裁决 |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否锁定真实项目根？ | `GATE-RESUME-ROOT` | `FAIL-RESUME-ROOT` | `S1-INTAKE` | project_root_lock、candidate_count |
| 是否有可复核状态证据和工件证据？ | `GATE-RESUME-EVIDENCE` | `FAIL-RESUME-EVIDENCE` | `S2-TRUTH` | state_truth、artifact_truth、gate_truth |
| 是否只输出一个安全下一入口？ | `GATE-RESUME-ENTRY` | `FAIL-RESUME-ENTRY` | `S4-PLAN` | one_next_entry、required_repairs |
| 是否过滤 destructive 动作？ | `GATE-RESUME-SAFETY` | `FAIL-RESUME-SAFETY` | `S5-GATE` | safety_verdict、forbidden_actions_filtered |
