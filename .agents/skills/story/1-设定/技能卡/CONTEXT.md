# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 技能只有名字没有使用代价 | skill rule closure | 回补 `activation_rules + limits_and_costs` | 技能卡最小三元组固定为“启用 + 限制 + 代价” | 技能能回答如何使用、何时失效、付出什么 |
| 科技/法术/武功混成一个万能能力 | taxonomy drift | 按题材语义重分桶并补 `skill_taxonomy` | 每张卡只能有一个主桶，跨桶能力用 `hybrid_tags` 表达 | `group` 与 `skill_taxonomy.primary_domain` 一致 |
| 技能替角色卡决定成长命运 | owner boundary drift | 把人物命运回写到角色卡，只在技能卡保留 `progression_hooks` | 技能卡只给能力成长接口，不直接改写人物弧线 | 角色变化仍可追溯到角色卡 |
| 技能变成无敌外挂 | counterplay missing | 增补克制、失败模式、误用后果 | 每张强技能都必须有 `counterplay` | drafting 能写失败、训练和反制 |
| 生活/职业技能被忽略 | genre bias | 将厨艺、才艺、职业技能、社交能力纳入 `life_talents/professional_skills` | 技能卡的“技能”按广义能力理解，不只服务战斗题材 | 非战斗题材也能产出可写戏能力卡 |

## Repair Playbook

1. 先判定技能是否是可写戏能力，不是单纯设定名词。
2. 再判主桶：科技、法术异能、武功、作战技能、生活才艺、专业技能。
3. 然后闭合启用条件、限制、代价、成长、克制。
4. 若技能与角色命运、场景规则、物品媒介冲突，回上游真源修接口，不在技能卡硬改。
5. 修复后至少跑 writer / validator 的局部检查，确认 `skill_links` 与 `progression_hooks` 可追溯。

## Reusable Heuristics

- 技能卡的核心价值是“能力如何制造选择压力”，不是“能力听起来多酷”。
- 越强的能力越需要更清楚的限制、代价和反制，否则 drafting 会滑向无代价解决问题。
- 科技与法术的差别不在外观，而在解释体系、学习路径、资源消耗和社会约束。
- 武功、枪械、厨艺、谈判、修理、表演都可以是技能卡，只要它能反复影响剧情选择。
- 技能卡最好给 planning 提供成长钩子，给 drafting 提供使用场景、失败方式和反制压力。
