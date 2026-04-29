# Scope Package: Mechanism

## Selection Signals

- 物品、道具、技能、能力、规则、限制、代价、持有人、机制说明、武功、法则。

## When X Then Check X

| when | must check |
| --- | --- |
| 改物品属性或归属 | 物品卡、首次出现章、当前持有人、后续使用章 |
| 改技能或能力机制 | 技能卡、限制/代价、训练/来源、战斗或解谜使用点 |
| 改世界规则 | north_star、整体规划、相关对象卡、所有显式规则解释点 |
| 改机制 payoff | 前置说明、使用代价、后续兑现章、review 逻辑自洽维度 |

## Required Impact Additions

- `mechanism_source_refs`
- `first_explanation_refs`
- `holder_or_user_refs`
- `cost_limit_refs`
- `payoff_refs`

## Review Gate

- 机制的来源、限制、代价、持有人和可用范围一致。
- 机制没有被局部修改抬成主角外挂。
- 后续使用不回到旧规则。
