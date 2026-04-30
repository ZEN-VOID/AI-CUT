# Review Contract

## Default Provider

- 默认辅助 provider：`code-reviewer`。
- 用途：对 repair 方案与结果执行结构、跨层一致性、源层优先、provider authorship 和验收门禁审查。
- 若上层策略阻断真实 subagent 或外部 reviewer 调度，允许降级为本地 code-reviewer checklist，但必须报告阻断来源、原计划 provider 路径、实际降级路径和未真实启动的 reviewer。

## Review Dimensions

| dimension | required checks |
| --- | --- |
| impact_scope | 是否覆盖 upstream truth、same-layer predecessor、current locality、downstream existing、future constraints、review/return/state |
| type_matrix | 是否按 `Universal Type Matrix` 对修改对象判型，并加载对应 `types/scope/*` 包 |
| source_priority | 是否先修 canonical owner，再修投影和正文 |
| continuity | 修改后同层前列、当前章、后续章和卷末兑现是否连续 |
| cards_planning_alignment | 对象卡、整体规划、卷规划、章规划是否同向 |
| authorship | 创作性改写是否回到 owning stage 和原 provider lane；指定文档头部含 `写作模型` 时，实际 creative engine 是否默认遵循该字段 |
| accepted_truth | PASS 终稿、return actualization、STATE 是否被正确失效、重验或保留 |
| residual_risk | 是否说明未改文件、未知消费者和后续生成 guardrail |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 修复闭环可接受 |
| `pass_with_followups` | 当前修复可用，但存在非阻断后续项 |
| `needs_rework` | 影响范围、源层或审计存在阻断缺口 |
| `blocked` | 缺关键输入、权限、provider 或破坏性写回授权 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: impact_scope | type_matrix | source_priority | continuity | cards_planning_alignment | authorship | accepted_truth | residual_risk
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Gate Rule

不得宣布完成：

- 没有 `impact_map`。
- 命中通用类型矩阵但没有加载对应 typed scope 包。
- 没有 `canonical_owner` 和 `writeback_order`。
- 旧口径在上游真源仍正向命中，但报告声称已完成。
- B/C lane 正文创作性改写缺 provider evidence。
- 指定文档头部存在 `写作模型`，但内容调整未按该模型执行，且没有用户显式切换模型的证据。
- 已 PASS/return 的事实被改变但 review/return 未处理。
