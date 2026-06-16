# Action Destruction FX Types Index

本目录是 `6-氛围` 的动作破坏点类型模块。`SKILL.md` 是唯一主入口和规则真源；本目录只在 `SKILL.md` 建立 `destruction_type_route` 后，提供对应类型的力量来源、受击材质、材料响应、节奏质感和专属边界。

## Type Route Schema

```yaml
destruction_type_route:
  type: wuxia_hk_cold_weapons | fantasy_xuanhuan | war_ruins | thriller_chase | naval_water | interior_court | realism_street | sci_fi_cyber | generic_material_response
  module: types/action-destruction-fx/<type>.md
  evidence:
    user_signal:
    aesthetic_signal:
    source_scene_signal:
    source_action_signal:
    material_signal:
    memory_signal:
  confidence: high | medium | low
  boundary_profile:
  fallback_reason:
```

## Module Map

| type | module | load_when |
| --- | --- | --- |
| `wuxia_hk_cold_weapons` | `types/action-destruction-fx/wuxia-hk-cold-weapons.md` | 港风武侠、冷兵器、白刃剑风、枪风、链镰、飞剑、断链余劲、兵器碰撞。 |
| `fantasy_xuanhuan` | `types/action-destruction-fx/fantasy-xuanhuan.md` | 玄幻、奇幻、仙侠、仪式、法阵、灵光、超自然力量被上游和 `2-美学` 授权。 |
| `war_ruins` | `types/action-destruction-fx/war-ruins.md` | 战争、废墟、灾后、爆破余波、墙体坍塌、瓦砾震落。 |
| `thriller_chase` | `types/action-destruction-fx/thriller-chase.md` | 惊悚、追逐、逃亡、躲藏、门窗玻璃和杂物短促破坏。 |
| `naval_water` | `types/action-destruction-fx/naval-water.md` | 海战、水域、船上、码头、风浪、船板、缆绳、水汽和湿木。 |
| `interior_court` | `types/action-destruction-fx/interior-court.md` | 宫廷、室内、文戏动作、屏风、瓷器、桌案、烛火、纸墨。 |
| `realism_street` | `types/action-destruction-fx/realism-street.md` | 现实主义、街巷、巷战、日常空间、路面、铁门、雨棚、积水。 |
| `sci_fi_cyber` | `types/action-destruction-fx/sci-fi-cyber.md` | 科幻、赛博、金属墙、管线、屏幕、车体、蒸汽、电子故障。 |
| `generic_material_response` | `types/action-destruction-fx/generic-material-response.md` | 类型证据不足、混合类型无法安全裁决，或只需要保守材质响应。 |

## Routing Rules

- 类型裁决优先级：用户显式信号 > `2-美学` > `5-表演` 场景/动作/材质证据 > 项目 `MEMORY.md` > 物理氛围知识库。
- 不能只靠单词判型：`爆点`、`水汽`、`火星`、`武器名`、`玻璃屑` 都不是类型结论。
- 若证据混合，按主场景和主动作服务的叙事功能裁决；若 `confidence=low`，使用 `generic_material_response` 或不触发。
- 同一画面点通常只加载一个类型模块；只有明确跨类型场景，例如“玄幻海战”或“科幻废墟追逐”，才允许加载两个模块，并在报告说明主次。

## Boundary Rules

- 本目录没有统一禁词。`灵光`、`法阵`、`能量波`、`护盾`、`粒子`、`科技光效` 等是否允许，由 `destruction_type_route.type`、上游 source、`2-美学` 和项目 `MEMORY.md` 共同裁决。
- 对不支持法术/科技光效的类型，相关表达属于类型越界。
- 对玄幻、奇幻、仙侠、科幻或赛博类型，只要上游和 `2-美学` 已授权，对应光效/能量/法阵/科技故障可以作为力量来源，但仍必须落到受击材质和剧情保真边界。

## Report Evidence

触发动作破坏点时，执行报告至少记录：

- `Destruction Type Route`
- `Action Destruction FX Map`
- loaded type module path
- source anchor
- force source
- target material
- effect material
- rhythm profile
- boundary check
