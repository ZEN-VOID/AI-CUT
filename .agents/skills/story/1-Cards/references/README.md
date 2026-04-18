# Cards References

`references/` 只承担一件事：为单一 skill [`1-Cards/SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md) 提供按需加载的 governed reference 模块。

它们不是子技能，不单独拥有路由权，不单独拥有 skill id。父技能负责判定“何时进入哪个模块”，子模块负责各自对象类型的局部规范合同和经验层。

## Load Contract

固定读取顺序：

1. 根 [`SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md)
2. 根 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)
3. 当前 [`README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/README.md)
4. 命中的 `references/<module>/module-spec.md`
5. 命中的 `references/<module>/CONTEXT.md`
6. 命中的 `templates/*.json`
7. 当前项目对应的 `Cards/**/*.json` 切片

冲突优先级：用户显式请求 > `AGENTS.md` / 根 `SKILL.md` > 模块 `module-spec.md` > 模块 `CONTEXT.md`

## Reference Loading Guide

- 默认判定顺序：先判任务模式，再判对象类型；对象类型命中后，按 `角色 -> 场景 -> 物品` 作为默认串行顺序。
- 默认入口：单对象请求只进入一个命中模块；mixed 请求与全量建卡按 `角色 -> 场景 -> 物品` 串行。
- 互斥规则：`character / scene / item` 在单对象请求下互斥，不能同时把一个问题硬判成两个主模块。
- 串行规则：mixed 请求、全量建卡、跨模块 coverage repair 必须显式串行，并由父技能保留统一视图。
- 按需加载规则：coverage repair 只加载命中模块；若本模块无法解释当前问题，必须退回父技能重做路由。

| 模块 | 触发条件 | 进入信号 | 与其他模块关系 | 必读文件 | 模板 |
| --- | --- | --- | --- | --- | --- |
| `character-card-module` | 当前问题落在人物、关系、弧光、声口、专属物接口 | 人物、关系、成长、服装、专属物、角色桶 coverage | 单对象场景下与其他模块互斥；mixed / 全量建卡时是串行起点 | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/module-spec.md)、[`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/CONTEXT.md) | [`character-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/character-card.json) |
| `scene-card-module` | 当前问题落在地点、空间、规则、危险、复用策略 | 地点、环境、世界规则、氛围、危险、常驻场景、场景桶 coverage | 单对象场景下与其他模块互斥；mixed / 全量建卡时位于角色之后、物品之前 | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/module-spec.md)、[`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/CONTEXT.md) | [`scene-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/scene-card.json) |
| `item-card-module` | 当前问题落在武器、线索、道具、代价、归属、专属适配 | 武器、线索、遗物、专属物、使用规则、代价、物品桶 coverage | 单对象场景下与其他模块互斥；mixed / 全量建卡时位于串行收尾 | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/module-spec.md)、[`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/CONTEXT.md) | [`item-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/item-card.json) |

## 模块索引

| 模块 | 类型 | 规范合同 | 局部经验层 | 正式输出路径 |
| --- | --- | --- | --- | --- |
| `character-card-module` | `governed-reference` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/CONTEXT.md) | `Cards/2-角色卡/**/*.json` |
| `scene-card-module` | `governed-reference` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/CONTEXT.md) | `Cards/3-场景卡/**/*.json` |
| `item-card-module` | `governed-reference` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/CONTEXT.md) | `Cards/4-物品卡/**/*.json` |

## 设计与证据

- 当前三类 cards 子模块的显式思维链快照已内嵌在各自 `module-spec.md` 中；根 `references/` 不再维持第二份独立报告真源。

## 统一原则

- 共同长期约束来自 `Init/north_star_contract.json.cards`。
- 共同 companion 输入来自 `Init/初始化简报.json`。
- 共享 worldbuilding 工法来自 `templates/worldbuilding/` 根目录；`references/` 只保留 cards module 细则。
- 子模块局部经验沉淀到各自 `CONTEXT.md`；跨模块经验继续回到 `1-Cards/CONTEXT.md`。
- 三类卡的正式输出仍分别落到 `Cards/2-角色卡`、`Cards/3-场景卡`、`Cards/4-物品卡`。
- 全量建卡固定顺序仍是 `角色 -> 场景 -> 物品`。
