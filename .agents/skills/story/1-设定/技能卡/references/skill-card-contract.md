# Skill Card Contract

技能卡持有广义能力的规则、限制、代价、成长和克制关系。它可以覆盖科技、法术、武功、作战技能、生活才艺、职业技能和其他能力体系。

## Boundary

- 世界规则归 `0-初始化/north_star.yaml`，技能卡只消费并投影到具体能力对象。
- 角色命运归角色卡，技能卡只提供训练、使用、失败、升级和反制接口。
- 物品媒介归物品卡，技能卡只说明能力如何依赖媒介或资源。

## Required Closure

每张技能卡必须闭合：

1. 主桶与题材语义。
2. 谁能学习或使用。
3. 如何启用。
4. 何时失效。
5. 使用代价。
6. 成长路径。
7. 克制与反制。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 技能主桶和题材语义是否一致？ | `taxonomy` | `FAIL-CD-SKILL-TYPE` | `steps/skill-card-workflow.md` 的类型判定节点 | `skill_taxonomy`、`group` |
| 启用条件、限制和代价是否具体？ | `rules` | `FAIL-CD-SKILL-RULES` | `steps/skill-card-workflow.md` 的规则闭合节点 | `activation_rules`、`limits_and_costs` |
| 成长路径能否被 planning 消费？ | `progression` | `FAIL-CD-SKILL-PROGRESSION` | `steps/skill-card-workflow.md` 的成长/克制节点 | `progression_model`、`progression_hooks` |
| 强技能是否有失败方式或反制关系？ | `counterplay` | `FAIL-SKILL-COUNTERPLAY` | `steps/skill-card-workflow.md` 的成长/克制节点 | `counterplay` |
| 技能卡是否越权改写世界、角色、场景或物品真源？ | `owner` | `FAIL-SKILL-OWNER` | `SKILL.md` 的 Root-Cause Execution Contract | `upstream_consistency_note` |
| 显式启用 subagents 时，顾问建议是否被转成可执行技能指导？ | `advisor_consultation` | `FAIL-CD-SKILL-ADVISOR` | `SKILL.md` 的 `S1A` | `advisor_consultation_packet.execution_brief` |
