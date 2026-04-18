# 故事大纲模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 3`，或后续长线系统缺少统一叙事骨架
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、冲突/任务/线索/伏笔四条长线、holomap

## Scope

本模块只负责 `2-Planning` 的 Step 3：

- 把题材走廊与章节容器转成整书叙事脊柱
- 锁定卷级推进、关键转折与主问题升级
- 为 Step 4-7 提供统一主干挂载骨架

本模块不负责：

- 代做冲突、任务、线索或伏笔的具体系统设计
- 把大纲写成事件流水账
- 越权覆盖 Step 1 的题材裁决或 Step 2 的章节容器

## Load Contract

- 加载条件：
  - 正常执行 Step 3
  - 后续长线系统失去统一主干或 holomap 只有板块没有“为什么这样排”
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Planning/2-章节规划.json`
  - `Cards/**/*.json`
- 模板依赖：
  - `templates/story-outline.json`
- 局部经验层：
  - 需要读取主干失焦修法、转折失效信号时，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Cards/**/*.json`

## Output Contract

- 模板：`templates/story-outline.json`
- 正式输出：`Planning/3-故事大纲.json`
- 必须产出：
  - 叙事脊柱
  - 卷级推进
  - 关键转折
  - 后续四条长线的挂载骨架

## Decision Focus

1. 整部书的叙事脊柱是什么？
2. 各卷如何推进主问题，而不是各自散开？
3. 关键转折怎样改变人物、局势和阅读预期？
4. 后续冲突链、任务链与证据链该挂在哪些主干节点上？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `主问题脊柱收束` | `core_question`、`outline_spine`、`volume_drive` | 只有卷摘要没有统一主问题 | 主问题对全书推进的牵引力 | 先锁叙事脊柱，不让卷摘要代替大纲 |
| `成立轴` | `转折改向成立` | `turning_points`、`state_shift`、`expectation_flip` | 转折不改变结构方向 | 转折对人物/局势/预期的真实改向强度 | 只有会改向的转折才进入主干 |
| `优选轴` | `长线挂载收益` | `conflict_hooks`、`mission_hooks`、`clue_hooks`、`foreshadow_hooks` | 后续四线挂不上去 | 主干节点对 4-7 步的挂载清晰度 | 在成立解中选最利于长线挂载的骨架 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `core_question`、`outline_spine`、`volume_drive` | 先进入哪种主干推进方案 | 圈定叙事脊柱候选 | 以主问题驱动卷级推进 |
| `细裁决 / Range Narrowing` | `turning_points`、`state_shift`、`expectation_flip` | 哪些转折真的能改写结构 | 排除只增事件不改向的方案 | 保留会改写结构方向的转折链 |
| `离散裁决 / Final Selection` | `conflict_hooks`、`mission_hooks`、`clue_hooks`、`foreshadow_hooks` | 哪套主干最利于后续四线挂载 | 比较挂载收益与可追溯性 | 输出可承接 4-7 步的故事脊柱 |

## Design Levers

- 先锁主问题，再写卷级推进
- 大纲不是细节堆叠，而是问题升级、视角推进与预期反转
- act / wave 只在服务当前项目时使用，不机械套模板

## High Risk Signals

- 只有卷摘要，没有脊柱
- 转折像事件清单，不改变结构方向
- 冲突、任务、线索、伏笔都像后来外挂

## Handoff Contract

- `conflict-design / mission-design / clue-design / foreshadow-design` 都必须以本模块的主干节点为挂载骨架
- `holomap` 若无法解释章节编组原因，应先回查本模块是否站稳

## Verification Checklist

1. `spine gate`
   - 已形成整书叙事脊柱，而非卷摘要堆叠
2. `turning-point gate`
   - 关键转折会改写结构方向，而不是只增加事件数
3. `boundary gate`
   - 本模块未越权代做四条长线的具体系统
4. `handoff gate`
   - Step 4-7 可从本模块读取明确挂载骨架
