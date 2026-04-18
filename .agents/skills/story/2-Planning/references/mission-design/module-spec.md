# 任务设计模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 5`，或故事推进只有被迫应对、缺少明确目标链与行动链
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、clue-design、holomap

## Scope

本模块只负责 `2-Planning` 的 Step 5：

- 把冲突系统转成角色可执行的目标链与行动链
- 锁定主线任务、阶段任务、章内行动任务、隐藏任务的门槛、代价、收益与失败后果
- 为 Step 6 与 Step 8 提供任务状态与目标追踪位点

本模块不负责：

- 代做冲突 owner 判定或线索发现路径
- 把任务写成空泛的动作提示词
- 越权覆盖人物弧光与故事主干

## Load Contract

- 加载条件：
  - 正常执行 Step 5
  - 文本推进只有“被迫应对”，缺少明确推进路线
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Planning/2-章节规划.json`
  - `Planning/3-故事大纲.json`
  - `Planning/4-冲突设计.json`
  - `Cards/**/*.json`
- 模板依赖：
  - `templates/mission-design.json`
- 局部经验层：
  - 需要门槛设计、代价收益校准启发式时，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Planning/4-冲突设计.json`
- `Cards/**/*.json`

## Output Contract

- 模板：`templates/mission-design.json`
- 正式输出：`Planning/5-任务设计.json`
- 必须产出：
  - 主线任务
  - 阶段任务
  - 章内行动任务
  - 隐藏任务
  - 门槛 / 代价 / 收益 / 失败后果

## Decision Focus

1. 主线任务、阶段任务、章内行动任务、隐藏任务分别是什么？
2. 每条任务的门槛、代价、收益和失败后果是什么？
3. 任务如何推动角色弧光，而不是只推动剧情？
4. 哪些任务需要跨卷延续，哪些任务必须在当前阶段解决？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `目标链收束` | `main_mission`、`stage_mission`、`action_task`、`hidden_task` | 只有动作口号，没有目标链 | 任务层级对推进路线的清晰度 | 先形成可追踪的目标链，再谈行动细节 |
| `成立轴` | `门槛代价成立` | `entry_requirement`、`cost`、`reward`、`failure_consequence` | 没有门槛和代价，任务像旁白提示 | 任务风险与收益是否足以成立 | 只有代价收益闭环的任务才成立 |
| `优选轴` | `弧光推进收益` | `character_change`、`situation_shift`、`info_shift`、`rule_shift` | 任务只推剧情不推人物 | 对人物弧光与局势变化的推动力 | 在成立解中选最能显影主动性的任务链 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `main_mission`、`stage_mission`、`action_task`、`hidden_task` | 先形成哪种任务分层 | 圈定目标链结构 | 保证任务不是单层口号 |
| `细裁决 / Range Narrowing` | `entry_requirement`、`cost`、`reward`、`failure_consequence` | 哪些任务真的成立 | 排除没有代价与门槛的方案 | 保留风险收益闭环成立的任务 |
| `离散裁决 / Final Selection` | `character_change`、`situation_shift`、`info_shift`、`rule_shift` | 哪套任务链最能推动角色主动性 | 比较弧光与局势推进收益 | 输出最能驱动人物与剧情同步前进的任务系统 |

## Design Levers

- 任务是角色主动性的显影器
- 高价值任务必须改变局势、关系、规则或信息状态中的至少一项
- 奖励与代价必须具体，不得只写“成长了”“更危险了”

## High Risk Signals

- 目标链模糊，只剩“去查”“去打”“去救”
- 没有门槛与代价，任务像旁白提示
- 任务和人物弧光没有绑定

## Handoff Contract

- `clue-design` 读取任务链，决定角色如何接近真相
- `holomap` 必须在 chapter board 中说明“角色此章想达成什么”

## Verification Checklist

1. `goal gate`
   - 已形成清晰目标链，而不是动作口号
2. `cost gate`
   - 门槛、代价、收益、失败后果具体可追踪
3. `boundary gate`
   - 本模块未代做线索系统或重写冲突系统
4. `handoff gate`
   - Step 6 与 Step 8 可读取任务状态与目标位点
