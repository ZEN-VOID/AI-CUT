# Review Gate

本文件定义 `4-Review` 的质量门禁、provider 接入与 verdict 汇流规则。

## Default Provider

- 默认 provider：`code-reviewer`
- 默认执行方式：后台独立窗口/进程。
- 当前 repo 的 canonical runner：`.agents/skills/story/scripts/review_runner.py`
- 上层策略若阻断真实 subagent 或外部 reviewer 调度，允许降级为本地 checklist，但必须报告阻断来源、原计划路径、实际路径和未启动 reviewer。

## Provider Aggregation

`code-reviewer` 输出不得停在 sidecar，必须映射回父层 aggregate：

| provider output | aggregate target |
| --- | --- |
| structured findings | `issues[]` |
| severity | `severity_counts`、`critical_issues` |
| suggested owner | `source_trace`、`source_layer_owner` |
| repair suggestion | `rework_targets` |
| report sidecar | `dimension_report_refs` 或 reviewer sidecar refs |

## Verdict Model

| validation_status | meaning | route |
| --- | --- | --- |
| `PASS` | 可以交给 `review/`，并在 handoff 授权时进入 `5-Loopback` | `handoff_to_review_and_loopback` 或 `handoff_to_review_only` |
| `FAIL-QUALITY` | 当前卷正文质量或执行链存在 blocking issue | `back_to_drafting_nodes` |
| `FAIL-COVENANT` | fact pack、写作日志或 required source slice 缺失 | `back_to_source_contract` |
| `FAIL-RUNTIME` | provider、runner、schema 或 aggregate 汇流失败 | 修运行时后重跑 |

## Gate Checklist

- mandatory 维度全部有 `dimension_packet`。
- 所有 packet 的 `volume_ref / chapter_refs / pack_ref` 指向同一轮事实包。
- issue 至少包含 `id / type / severity / chapter_ref / location / description / suggestion / source_layer_owner`。
- aggregate 包含 `validation_status / routing_decision / handoff_targets / rework_targets / validation_ref`。
- `critical_issues` 非空时不得 PASS。
- source conflict 未解决时不得打回 drafting 当作正文质量问题。

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: structure | continuity | logic | character | timeline | task_convergence | runtime
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```
