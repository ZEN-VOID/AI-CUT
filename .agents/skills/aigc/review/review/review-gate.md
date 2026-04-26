# Review Gate

## Default Provider

- 默认辅助 provider：`code-reviewer`
- provider 配置：`_shared/execution-provider.yaml`
- runner：`scripts/aigc_review_runner.py`

上层策略若阻断真实 subagent 或外部 reviewer 调度，允许降级为本地 checklist，但必须报告：

- 阻断来源层级
- 原计划 provider 路径
- 实际采用的降级路径
- 未真实启动的 reviewer

## Verdict Model

| review_status | meaning |
| --- | --- |
| `FAIL-COVENANT` | fact pack required slice 缺失，不能进入维度审计 |
| `FAIL-BLOCKING` | 存在 critical/high issue，阻断 handoff |
| `PASS-WITH-WARNINGS` | 可放行但需要携带非阻断修复项 |
| `PASS` | 可进入下一阶段、provider handoff 或 release |

## Routing Decision Contract

| routing_decision | 适用条件 |
| --- | --- |
| `back_to_stage_contract` | 问题主要落在当前阶段产物或节点 |
| `back_to_source_contract` | 问题来自上游真源、规划冲突或治理断链 |
| `block_provider_handoff` | provider pack、引用或 continuity 不可信 |
| `handoff_next_stage` | 当前 scope 可放行到唯一下一入口 |
| `hold_for_human_review` | 自动审计无法稳定裁决 |

## Covenant Early Exit

- `review_fact_pack.missing_required_refs` 非空时，runner 必须直接写 `FAIL-COVENANT`。
- 早停时不得调用 `code-reviewer`，不得生成维度 sidecar，避免把证据缺口误包装成维度审查结论。
- 早停仍必须写 aggregate packet、repair sidecar 与 review summary。
