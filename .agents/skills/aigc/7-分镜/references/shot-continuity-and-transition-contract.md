# Shot Continuity And Transition Contract

本文件融合旧 `4-摄影/references/intra-shot-transition-contract.md` 与 `shot-continuity-contract.md`，改写为 `7-分镜` 的连贯性细则。它约束字段内相邻分镜和字段间相邻画面点的可剪辑连续性，不替代下游创意转场或 `7-图像` / `8-视频` 生成。

## Core Rule

每个画面点内的相邻分镜之间必须存在物理、注意力、声音或光色过渡锚点。相邻画面点之间必须保留可消费的姿态、轴线、动作方向、视线、声音尾巴、光色变化、空间出口或注意力落点。

连续性不等于段落吞并。当前画面点的分镜只服务当前字段；不得为了流畅提前写入后文主体动作、对白反应、记忆段或道具揭示。

## Continuity Profile

每个画面点内部形成：

| field | question |
| --- | --- |
| `previous_3_points` | 前 3 个画面点分别看什么、怎么动、落在哪里 |
| `current_entry_point` | 当前分镜从上一注意力落点、声音或动作接口进入哪里 |
| `axis_policy` | 继续同轴、反打换轴、建立镜头重置，还是主观视角合理跳轴 |
| `movement_policy` | 顺接上一运动方向、减速停住、反向但给动机，还是用静止切断 |
| `action_anchor` | 人物站/坐/蹲/跪/靠墙/牵手/搀扶等持续姿态是否继承 |
| `segment_link` | 当前画面点内相邻分镜如何连接 |
| `field_link_chain` | 当前画面点最后一条分镜如何交给下一画面点 |
| `unit_ownership` | 当前分镜没有吞入其他画面点的信息 |

## Transition Anchor Types

| anchor_type | requirement |
| --- | --- |
| `movement_continuity` | 同一运动体的位置、速度、方向变化可追踪 |
| `prop_state` | 同一道具的状态变化可追踪，且道具通过准入 |
| `sound_timeline` | 声音尾音、骤停、变形或来源变化有时序 |
| `light_color` | 光色明暗变化有来源，例如遮挡、显影、实用光变化 |
| `gaze_attention` | 视线、注意力或焦点从上一落点转到下一入口 |

字段内 N 条分镜需要 N-1 个过渡锚点。覆盖率低于 100% 时，必须重写、合并或标明合法叙事断裂。

## Axis And Action Rules

- 双人对峙、追逐、打斗、逼问、谈判或凝视必须先建立虚拟轴线。
- 若 screen left/right 影响理解，内部计划必须重复谁在画面左侧、谁在右侧，中间空间锚点是什么。
- 换轴必须通过中性镜头、主观视角、可见运动镜头或角色明确换位。
- 持续动作锚点必须继承：上一画面点结尾坐着、牵手、搀扶、靠墙，下一画面点不能凭空站到别处。
- 道具、反射、静物或环境声只有通过互动、证据、危险源、规则显影或必要空间交代时，才可成为连续性切点。

## Inline Projection

连续性不能只留在报告或内部计划。成稿应能在相邻分镜句子里读出连接：

```text
分镜1（0-2秒）：中景，深景深，走廊纵深构图，主角沿画面左侧墙根后退，右手仍扶着门框，后景冷白灯管一盏盏退远。
分镜2（2-4秒）：近景，浅景深，门框前景遮挡构图，承接他扶门的右手，指节在冷白灯下发白，背景走廊虚成一条压低的亮线。
```

不合法：

```text
分镜1（0-2秒）：主角后退。
分镜2（2-4秒）：切到手部特写。
```

## Legal Discontinuity

强断裂只有在以下情况可成立，并必须记录理由：

- 惊吓、规则打断、系统入侵、记忆闪回或主观感知异常。
- 声音骤停或光变本身就是叙事事件。
- 上游字段明确要求断裂式转场或突变。

即便合法断裂，也必须保留观众可理解的断裂动机，而不是用“突然”掩盖因果黑洞。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 字段内相邻分镜是否有过渡锚点，覆盖率 100%？ | `GATE-SB-12` | `FAIL-SB-TRANSITION` | `N7-CONTINUITY` | `transition_anchor_map` |
| 相邻画面点是否有可消费交出和进入接口？ | `GATE-SB-13` | `FAIL-SB-CONTINUITY` | `N7-CONTINUITY` | `field_link_chain` |
| 动作锚点和人物姿态是否被继承，没有凭空变化？ | `GATE-SB-13` | `FAIL-SB-CONTINUITY` | `N7-CONTINUITY` | action anchor samples |
| 轴线和 screen left/right 是否稳定，换轴是否有桥接？ | `GATE-SB-13` | `FAIL-SB-CONTINUITY` | `N7-CONTINUITY` | axis policy samples |
| 连续性是否没有吞入后文画面点？ | `GATE-SB-14` | `FAIL-SB-FIDELITY` | `N7/N8` | ownership boundary check |
