# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `step-3-review-gate`，记录隔离审查路由与落库闸门的局部经验。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 若经验跨到 `4-Validation` 或根技能的流程合同，应回写更高层文档。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 主流程直接自审 | routing contract | 强制回到 `4-Validation` 建新团队 | 把隔离团队写成本模块第一闸门 | selected_agents 来自新团队 |
| `review_metrics` 字段不齐 | output contract | 以模块字段清单补齐后重新落库 | 保持本模块对落库字段的单一真源 | Step 4 能直接消费 |
| 时间线高风险仍被放行 | gate contract | 执行 timeline gate 并阻断 | 固定 timeline gate 为验收门禁 | 高严重度 `TIMELINE_ISSUE` 必阻断 |

## Repair Playbook

1. 先查是否真的经过 `4-Validation`。
2. 再查 selected_agents 与 routing_decision 是否匹配 mode。
3. 再查落库字段与 `notes` 形态。
4. 最后查 timeline gate 是否正确生效。

## Reusable Heuristics

- Step 3 最危险的假阳性是“看起来有分数”，但分数并不来自新的隔离团队。
- 路由是否正确，通常比“启用了多少 checker”更重要。
- 如果 Step 4 读不到稳定的问题包，根因大多在 Step 3 的字段落库，而不是润色器本身。

