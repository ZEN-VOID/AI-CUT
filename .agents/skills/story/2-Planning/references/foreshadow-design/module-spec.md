# 伏笔设计模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 7`，或线索能求证但长期回照系统无力
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、holomap

## Scope

本模块只负责 `2-Planning` 的 Step 7：

- 把长期回收点设计成可铺设、可加深、可静默、可兑现的系统
- 锁定人物、关系、规则、物件或终局命题层面的回照链
- 为 Step 8 提供伏笔状态与兑现窗口

本模块不负责：

- 把当前可求证的线索重命名成伏笔
- 把一次性提醒伪装成长期回照系统
- 越权改写故事主干或任务链

## Load Contract

- 加载条件：
  - 正常执行 Step 7
  - 线索系统成立，但未来回照仍然无力
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Planning/2-章节规划.json`
  - `Planning/3-故事大纲.json`
  - `Planning/4-冲突设计.json`
  - `Planning/5-任务设计.json`
  - `Planning/6-线索设计.json`
  - `Cards/**/*.json`
- 模板依赖：
  - `templates/foreshadow-design.json`
- 局部经验层：
  - 需要读取铺设/加深/静默/兑现修法时，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Planning/4-冲突设计.json`
- `Planning/5-任务设计.json`
- `Planning/6-线索设计.json`
- `Cards/**/*.json`

## Output Contract

- 模板：`templates/foreshadow-design.json`
- 正式输出：`Planning/7-伏笔设计.json`
- 必须产出：
  - 伏笔对象
  - 铺设窗口
  - 加深节点
  - 静默区
  - 兑现窗口

## Decision Focus

1. 哪些内容值得被长期埋藏，并在未来改变读者理解？
2. 伏笔服务的是人物、关系、规则、物件还是终局命题？
3. 铺设、加深、静默、兑现窗口分别落在哪些章节板块？
4. 回收时如何回照前文，而不是临时解释？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `回照对象收束` | `foreshadow_object`、`service_domain`、`future_reinterpretation` | 埋设内容不会改变未来理解 | 不同伏笔对象对终局命题的牵引力 | 先锁值得长期埋的对象 |
| `成立轴` | `状态链成立` | `plant_window`、`reinforcement_node`、`silence_window`、`payoff_window` | 只有埋设，没有加深或兑现 | 伏笔状态在多阶段中的持续性 | 只有完整状态链成立的伏笔才保留 |
| `优选轴` | `回收反照收益` | `callback_strength`、`meaning_shift`、`thread_overlap_risk` | 回收不能重估前文意义 | 兑现后的语义反照强度与系统清晰度 | 在成立解中选最能改变读者理解的回照链 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `foreshadow_object`、`service_domain`、`future_reinterpretation` | 先埋哪类长期对象 | 圈定伏笔对象候选 | 只保留值得长期埋藏的内容 |
| `细裁决 / Range Narrowing` | `plant_window`、`reinforcement_node`、`silence_window`、`payoff_window` | 哪些伏笔链真的成立 | 排除一次性提醒或无兑现窗口的方案 | 保留状态链完整的伏笔系统 |
| `离散裁决 / Final Selection` | `callback_strength`、`meaning_shift`、`thread_overlap_risk` | 哪套回照最有价值 | 比较兑现后的反照强度与系统清晰度 | 输出最能重估前文意义的伏笔链 |

## Design Levers

- 主伏笔至少应覆盖两个阶段以上，而不是一次埋下后消失
- 静默区是必要资产，不是“忘记提了”
- 伏笔与线索分工：
  - 线索偏当前可求证
  - 伏笔偏未来再理解

## High Risk Signals

- 伏笔只有一次提醒，没有加深或回收
- 回收时不能重估前文意义
- 把线索换个名字继续写，导致系统混乱

## Handoff Contract

- `holomap` 必须能显示伏笔当前处于铺设、加深、静默还是兑现
- 若 Step 8 无法显示长期回照状态，优先回查本模块

## Verification Checklist

1. `lifecycle gate`
   - 已形成铺设/加深/静默/兑现的完整状态链
2. `boundary gate`
   - 本模块未把线索系统冒充为伏笔系统
3. `recall gate`
   - 兑现时能够重估前文意义，而非临时解释
4. `handoff gate`
   - Step 8 可读取伏笔状态与兑现窗口
