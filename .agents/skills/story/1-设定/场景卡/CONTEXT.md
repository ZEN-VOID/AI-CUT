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
| 启用 subagents 后只收泛泛审美意见，没有请教空间功能问题 | advisor consultation gap | 按 `team.yaml` 顾问专长追问场景功能、规则代价、危险、返场价值和角色适配 | 显式启用 subagents 时先生成 `advisor_consultation_packet`，再进入场景卡创作 | 场景卡能说明顾问建议如何落到 `narrative_functions / rule_and_risk / repeat_use_strategy` |

## Repair Playbook

1. 先判功能，再判规则，再判复用。
2. 若不清楚为何是场景问题，先回父技能。
3. 先修可写性，再补视觉表达。
4. 如果显式启用 subagents，顾问问题要聚焦“这个空间强迫角色做什么选择”和“返场时能变出什么不同功能”，不要停在氛围、视觉或喜好词。

## Reusable Heuristics

- 场景卡的第一问永远是“允许什么戏发生”。
- 没有代价和限制的超现实场景会把世界规则冲穿。
- 返场策略要写“同一空间在不同卷段承担什么不同功能”，不要只写成抽象的“可复用”。
- 顾问请教对场景卡的价值在于提前识别“漂亮但不可写”的空间；能转成规则、风险、角色行动压力或返场策略的建议才进入正式卡。
