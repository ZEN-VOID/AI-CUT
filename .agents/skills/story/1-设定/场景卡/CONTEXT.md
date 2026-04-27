# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 场景像布景板 | scene function | 先补 `narrative_functions` 与 `compatible_roles` | “谁来做什么”先于氛围词 | 场景能回答进入者、目的与代价 |
| 超现实场景失控 | rule contract | 回补 `rule_and_risk` | 强规则项目先读 world rules 再写美学 | 场景不再只剩氛围词 |
| 场景只会新增不会复用 | reuse strategy | 回补 `scene_links + repeat_use_strategy` | 常驻场景优先级写死为 child heuristic | 返场场景能解释不同阶段用法 |
| `repeat_use_strategy` 只写在索引，不落到单场景卡 | writeback closure | 把每张场景卡的 `current_focus.repeat_use_strategy` 补成 2-3 条可验证用法 | 场景 repair 完成前必须逐卡跑覆盖校验，不能只看索引汇总 | `cards_coverage_validator.py` 的 scenes 维度转为 PASS |

## Repair Playbook

1. 先判功能，再判规则，再判复用。
2. 若不清楚为何是场景问题，先回父技能。
3. 先修可写性，再补视觉表达。

## Reusable Heuristics

- 场景卡的第一问永远是“允许什么戏发生”。
- 没有代价和限制的超现实场景会把世界规则冲穿。
- 返场策略要写“同一空间在不同卷段承担什么不同功能”，不要只写成抽象的“可复用”。
