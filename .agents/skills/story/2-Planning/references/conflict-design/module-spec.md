# 冲突设计模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 4`，或故事推进有事件但对抗关系、压力源、解决窗口发虚
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、mission-design、holomap

## Scope

本模块只负责 `2-Planning` 的 Step 4：

- 把故事主干转成可持续升级的对抗网络
- 锁定外部冲突、内部冲突、理念冲突的 owner、压力来源与解决窗口
- 为 Step 5 与 Step 8 提供冲突状态流

本模块不负责：

- 代做任务系统或线索系统
- 把单章热闹误判为冲突升级链
- 越权重写 Step 3 的叙事脊柱

## Load Contract

- 加载条件：
  - 正常执行 Step 4
  - 大纲已有推进，但“谁在阻拦谁、为什么现在爆发”仍然发虚
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Planning/2-章节规划.json`
  - `Planning/3-故事大纲.json`
  - `Cards/**/*.json`
- 模板依赖：
  - `templates/conflict-design.json`
- 局部经验层：
  - 需要冲突梯度修法、owner 判定启发式时，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Cards/**/*.json`

## Output Contract

- 模板：`templates/conflict-design.json`
- 正式输出：`Planning/4-冲突设计.json`
- 必须产出：
  - 冲突分类
  - owner / pressure source
  - 升级链
  - 解决窗口
  - 与任务系统的接口

## Decision Focus

1. 当前项目有哪些外部冲突、内部冲突、理念冲突？
2. 冲突如何从轻度摩擦升级到无法回避的对抗？
3. 冲突的 owner、压力来源与解决方式分别是谁？
4. 哪些冲突必须被延迟解决，哪些冲突必须在当前卷爆发？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `对抗网络收束` | `conflict_system`、`conflict_owner`、`pressure_source` | 只有情绪词，没有对抗归属 | 主压迫源与辅增压源的驱动力 | 先锁谁在压迫谁，再谈冲突强度 |
| `成立轴` | `升级链成立` | `escalation_ladder`、`resolution_window`、`phase_pressure` | 强冲突过早耗尽或无升级链 | 冲突在多卷中的延续与爆发节奏 | 只有能持续升级的冲突才成立 |
| `优选轴` | `行动逼出收益` | `mission_trigger`、`clue_pressure`、`holomap_state_flow` | 冲突无法逼出任务和状态流 | 对任务、线索、holomap 的联动收益 | 在成立解中选最能驱动行动的冲突网络 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `conflict_system`、`conflict_owner`、`pressure_source` | 当前应采用哪类对抗网络 | 圈定主压迫源与冲突簇 | 先形成清晰冲突归属 |
| `细裁决 / Range Narrowing` | `escalation_ladder`、`resolution_window`、`phase_pressure` | 哪些冲突真的能持续升级 | 排除早耗尽或无梯度方案 | 保留升级链成立的对抗网络 |
| `离散裁决 / Final Selection` | `mission_trigger`、`clue_pressure`、`holomap_state_flow` | 哪套冲突最能驱动后续行动 | 比较对任务、线索、holomap 的联动收益 | 输出最能逼出角色行动的冲突系统 |

## Design Levers

- 冲突不是单章热闹，而是升级链
- 多线冲突可以共存，但必须知道谁是主压迫源，谁是辅增压源
- 解决窗口必须服务后续任务与线索推进，而不是打一架就结束

## High Risk Signals

- 冲突只剩情绪词，没有归属关系
- 强冲突过早耗尽，导致后续无梯度
- 冲突与任务、线索完全脱节

## Handoff Contract

- `mission-design` 必须读取本模块的冲突网络，决定角色为何必须行动
- `holomap` 必须在 chapter board 中挂载冲突 owner 与状态流

## Verification Checklist

1. `owner gate`
   - 每条主冲突都有明确 owner 与 pressure source
2. `gradient gate`
   - 冲突存在升级链，而不是只靠强度词
3. `boundary gate`
   - 本模块未代做任务、线索系统
4. `handoff gate`
   - Step 5 与 Step 8 可读取冲突状态流
