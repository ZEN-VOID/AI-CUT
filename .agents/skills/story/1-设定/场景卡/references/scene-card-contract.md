# Scene Card Contract

场景卡持有场景功能、规则、危险、可复用策略与角色接口消费关系。场景不是布景板，而是可写戏空间。

## Boundary

- 场景卡只拥有空间功能、规则风险、角色适配与返场策略。
- 角色动机归 `角色卡`，物品代价归 `物品卡`，世界规则归 `0-初始化/north_star.yaml`。
- 场景视觉表达必须服务可写戏行动，不得替代 `narrative_functions` 或 `rule_and_risk`。

## Required Closure

每张场景卡必须闭合：

1. 场景承担的叙事功能。
2. 哪些角色适合进入，进入后被迫面对什么选择。
3. 场景规则、危险、代价或限制。
4. 与其他场景、角色或线索的连接关系。
5. 返场时能变化出的不同功能。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 场景是否有明确叙事功能，而不是布景板？ | `function` | `FAIL-CD-SCENE-FUNC` | `steps/scene-card-workflow.md` 的 `SC2` | `narrative_functions`、`function_note` |
| 场景规则、危险、代价与适配角色是否闭合？ | `rules` | `FAIL-CD-SCENE-RULE` | `steps/scene-card-workflow.md` 的 `SC3` | `rule_and_risk`、`compatible_roles` |
| 场景是否能支撑长篇返场？ | `reuse` | `FAIL-CD-SCENE-REUSE` | `steps/scene-card-workflow.md` 的 `SC4` | `scene_links`、`repeat_use_strategy` |
| 显式启用 subagents 时，顾问建议是否被转成可执行场景指导？ | `advisor_consultation` | `FAIL-CD-SCENE-ADVISOR` | `SKILL.md` 的 `S1A` | `advisor_consultation_packet.execution_brief` |
