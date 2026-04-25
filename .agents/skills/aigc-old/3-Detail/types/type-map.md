# 3-Detail Type Map

`types/` 是 `3-Detail` 的分型策略层。它先形成 `type_profile`，再让 `steps/detail-thinking-action-workflow.md` 选择最小执行入口。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `scope_type` | `episode_scope`, `group_scope`, `shot_scope`, `field_scope`, `closure_scope` | 本轮 patch 的最小范围 |
| `field_type` | `skeleton`, `performance`, `atmosphere`, `photo`, `motion_transition`, `report` | 当前主要写入对象 |
| `knowledge_domain` | `director`, `storyboard`, `cinematography`, `mixed`, `none` | 学院派知识主域 |
| `runtime_shape` | `canonical`, `legacy`, `template` | 目标 JSON 结构形态 |
| `review_type` | `stage-validator`, `creative-checklist`, `structural-only`, `blocked` | 验收方式 |

## Scope Routing Matrix

| scope_type | trigger | minimum_entry | required_review |
| --- | --- | --- | --- |
| `episode_scope` | 首次落盘或整集上游 seed 变化 | `N1` | full stage validator |
| `group_scope` | 只重写指定分镜组 | `N2` | 命中组字段 + 报告证据 |
| `shot_scope` | 只修指定分镜 | `N2` 或字段节点 | 命中镜头 + continuity |
| `field_scope` | 只修后序字段 | `N3/N4/N5/N6` | 字段边界 + 不反改骨架 |
| `closure_scope` | 只修报告或结案证据 | `N7/N8` | report sections only |

## Knowledge Domain Matrix

| knowledge_domain | primary bundle | target fields | risk |
| --- | --- | --- | --- |
| `director` | `knowledge-base/电影学院派/导演手册/` | 戏剧单元、角色目标、揭示顺序、空间组织 | 写成导演术语而非镜内动作 |
| `storyboard` | `knowledge-base/电影学院派/分镜脚本/` | 镜数、轴线、方向、机位路径、观看任务 | 过度规则化，压扁人物 |
| `cinematography` | `knowledge-base/电影学院派/电影摄影/` | 光影、色彩、质感、视觉重力 | 堆器材或参数 |
| `mixed` | 以上按问题最小组合 | 跨字段协同 | 误把全库通读当质量 |
| `none` | 不读取外部知识包 | 报告写 `unused_with_reason` | 挂名使用或证据缺失 |

## Field Routing Matrix

| field_type | route | forbidden overlap |
| --- | --- | --- |
| `skeleton` | `N2` | 后序节点不得顺手改 `分镜数 / 时间 / 剧本正文 / 主体锚定 / 分镜构图` |
| `performance` | `N3` | 不写机位、光影、镜头运动 |
| `atmosphere` | `N4` | 不用抽象 mood 替代空间条件 |
| `photo` | `N5` | 不抢构图骨架，不堆器材参数 |
| `motion_transition` | `N6` | 不倒逼结构重写；必要时回 `N2` |
| `report` | `N7/N8` | 不借 closure_scope 改业务 JSON |

## Fusion Rule

1. 先判 `scope_type`。
2. 再判 `field_type`。
3. 再按当前戏剧问题选择 `knowledge_domain`。
4. 将 `type_profile` 交给 steps 节点，禁止直接在 types 中写完整执行流程。
