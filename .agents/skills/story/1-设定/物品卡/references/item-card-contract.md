# Item Card Contract

物品卡持有剧情杠杆、归属链、使用规则、代价与专属适配。物品必须吸收角色和场景上游接口，不能自说自话。

## Boundary

- 物品卡只拥有物品的剧情功能、归属链、使用规则、代价与专属适配。
- 角色成长归 `角色卡`，空间规则归 `场景卡`，能力机制归 `技能卡`，世界规则归 `0-初始化/north_star.yaml`。
- 物品外观必须服务功能和代价，不得用装饰性描写替代对象闭合。

## Required Closure

每张物品卡必须闭合：

1. 物品为什么能改变局面。
2. 物品属于谁、如何转手或被争夺。
3. 物品怎样启用，何时失效。
4. 使用代价或风险。
5. 专属物如何贴合角色与场景上游接口。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 物品是否有剧情杠杆，而不是命名设定？ | `function` | `FAIL-CD-ITEM-FUNC` | `steps/item-card-workflow.md` 的 `I2` | `narrative_functions`、`function_note` |
| 归属链、启用规则和代价是否闭合？ | `cost` | `FAIL-CD-ITEM-OWN` | `steps/item-card-workflow.md` 的 `I3` | `ownership_links`、`usage_rules`、`costs` |
| 专属适配是否吸收角色和场景上游接口？ | `fit` | `FAIL-CD-ITEM-EXCLUSIVE` | `steps/item-card-workflow.md` 的 `I4` | `exclusive_fit`、`upstream_trace` |
| 显式启用 subagents 时，顾问建议是否被转成可执行物品指导？ | `advisor_consultation` | `FAIL-CD-ITEM-ADVISOR` | `SKILL.md` 的 `I1A` | `advisor_consultation_packet.execution_brief` |
