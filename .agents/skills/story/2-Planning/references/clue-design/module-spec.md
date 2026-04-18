# 线索设计模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 6`，或推进中只有答案、没有公平发现过程
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、foreshadow-design、holomap

## Scope

本模块只负责 `2-Planning` 的 Step 6：

- 把任务链转成证据链、发现链和误导链
- 锁定证据源、承载物、发现路径、误导结构、揭晓窗口
- 为 Step 7 与 Step 8 提供信息状态变更位点

本模块不负责：

- 把已求证信息伪装成伏笔系统
- 用遮蔽信息替代公平误导
- 越权重做任务链与冲突链

## Load Contract

- 加载条件：
  - 正常执行 Step 6
  - 当前推进只有“知道答案”，没有公平发现过程
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Planning/2-章节规划.json`
  - `Planning/3-故事大纲.json`
  - `Planning/4-冲突设计.json`
  - `Planning/5-任务设计.json`
  - `Cards/**/*.json`
- 模板依赖：
  - `templates/clue-design.json`
- 局部经验层：
  - 需要读取公平误导、发现链修法时，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Planning/4-冲突设计.json`
- `Planning/5-任务设计.json`
- `Cards/**/*.json`

## Output Contract

- 模板：`templates/clue-design.json`
- 正式输出：`Planning/6-线索设计.json`
- 必须产出：
  - 证据源
  - 承载物
  - 发现路径
  - 误导结构
  - 揭晓窗口

## Decision Focus

1. 证据从哪里来，由什么承载，被谁发现？
2. 误导是否服从证据，而不是作者硬骗？
3. 发现路径中有哪些阻碍、纠偏与行动反馈？
4. 哪些线索节点必须在何处揭晓，才能推动下一阶段任务？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `证据链收束` | `evidence_source`、`carrier`、`discoverer`、`reveal_window` | 只有答案，没有证据来源与承载物 | 证据链对任务推进的支持度 | 先锁证据链，再谈解释与揭晓 |
| `成立轴` | `公平发现成立` | `discovery_route`、`obstacle`、`correction_point`、`action_feedback` | 发现过程断裂或不可追踪 | 角色是否真的能公平接近真相 | 只有可发现、可纠偏的线索链才成立 |
| `优选轴` | `误导行动收益` | `false_lead`、`evidence_compliance`、`next_action_push` | 误导只在遮蔽，不推动行动 | 误导对行动推进与读者公平性的收益 | 在成立解中选最公平且最能推动行动的误导结构 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `evidence_source`、`carrier`、`discoverer`、`reveal_window` | 先形成哪类证据链 | 圈定证据源与发现对象 | 保证线索不是答案摘要 |
| `细裁决 / Range Narrowing` | `discovery_route`、`obstacle`、`correction_point`、`action_feedback` | 哪些发现链真的成立 | 排除跳步获知与硬塞真相的方案 | 保留公平发现成立的路径 |
| `离散裁决 / Final Selection` | `false_lead`、`evidence_compliance`、`next_action_push` | 哪套误导最公平也最有推进力 | 比较误导对行动与公平的双重收益 | 输出服从证据且推动行动的线索网络 |

## Design Levers

- 线索链建议显式覆盖：
  - 证据源
  - 承载物
  - 解释层
  - 行动层
  - 回收层
- 公平误导必须同时满足：
  - 服从证据
  - 可纠偏
  - 推动行动

## High Risk Signals

- 线索只有结论，没有发现路径
- 误导只是遮蔽信息，不服务行动
- 线索与伏笔混写，导致既不能求证也不能回照

## Handoff Contract

- `foreshadow-design` 读取线索边界，避免把已求证信息误写成伏笔
- `holomap` 必须能显示“此章获得了什么信息”

## Verification Checklist

1. `discovery gate`
   - 已形成证据链与发现链，而不只是答案摘要
2. `fairness gate`
   - 误导服从证据，且存在纠偏机制
3. `boundary gate`
   - 本模块未把线索与伏笔混写
4. `handoff gate`
   - Step 7 与 Step 8 可读取信息状态变更
