# Volume Planning Contract

## Purpose

给 `2-章节规划` 用的卷级规划合同。

它要解决的问题不是“每卷叫什么、覆盖哪十集”，而是让 Step 2 产出的 `volume_boards` 真正成为 downstream 可消费的卷级 planning truth：

- 这一卷负责什么 `wave duty`
- 这一卷如何交付卖点
- 这一卷在表现上如何区别于前后卷
- 这一卷哪些写法必须被禁止

如果 Step 2 只留下卷名、集数和一句 `core_function`，那后续 child 只能继承剧情功能，继承不到卷与卷之间的表现差异。

## Core Rule

`volume_boards` 在 Step 2 中一律视为“卷级 planning contract”，不是轻目录。

最小合格的卷级规划，必须同时覆盖三层：

1. 结构层：
   - `core_function`
   - `wave_duty`
   - `entry_promise`
   - `exit_hook`
2. 表现层：
   - `visual_climate`
   - `action_grammar`
   - `mystery_mode`
   - `emotional_temperature`
3. 护栏层：
   - `scene_materials`
   - `performance_axis`
   - `taboo_writeups`

## Required Fields

| field | question it must answer |
| --- | --- |
| `core_function` | 这卷在整书里负责推进什么，不负责什么 |
| `volume_promise` | 这卷向读者交付的核心期待是什么 |
| `wave_duty` | 这一卷在整书波形里承担 `promise / expansion / reversal / squeeze / payoff` 的哪种职责 |
| `entry_promise` | 卷头前 1-2 集必须先给读者什么感觉或承诺 |
| `exit_hook` | 卷尾必须把什么压力、问题或欲望送到下一卷 |
| `visual_climate` | 这一卷的场景气候、光色、材质和空间感怎么写 |
| `action_grammar` | 这一卷的动作戏靠什么推进，不能只写成 generic fight |
| `mystery_mode` | 这一卷的悬疑/信息控制属于哪种密度与玩法 |
| `emotional_temperature` | 这一卷整体情绪温度是什么 |
| `scene_materials` | 哪几类场域材料反复出现，构成卷内身体感 |
| `performance_axis` | 演员/人物关系在这一卷该怎么“演” |
| `taboo_writeups` | 这一卷最不能退化成什么写法 |

## Slice Mirror Rule

- 当前项目采用 `total-index-plus-deciles` 时，Step 2 还必须把卷级合同镜像到对应 slice 的 `slice_style_contract`。
- `slice_style_contract` 不是第二份卷级真源，只是把当前十集必须 obey 的卷级规则送到 episode-local 层。
- 若一卷正好对应一个十集 slice，`slice_style_contract` 应与该卷 `volume_board` 同步。
- 若一卷横跨多个 slice，多个 slice 允许共享同一卷合同，但必须保证字段一致，不得各自漂移。

## Anti-Drift Checks

- 若 `volume_boards` 只有 `title / episode_range / core_function`，视为卷级规划不足。
- 若总风格只存在 `0-Init`，而 `volume_boards` 无法回答每卷怎么表现，视为 Step 2 未完成。
- 若 slice 有 `chapter_boards` 但没有 `slice_style_contract`，说明卷级合同没有真正下沉到 episode-local 层。
- 若 `taboo_writeups` 缺失，downstream 很容易把卷级差异写平。

## Recommended Heuristic

- 卷与卷之间最稳的差异化，不是单纯换地点和换 Boss，而是同时换：
  - 压力类型
  - 信息控制方式
  - 动作推进语法
  - 情感温度
  - 场景材料
- 先写“这一卷绝不能变成什么”，再写“这一卷最该像什么”，通常更容易稳住卷级识别度。
