# 章节规划模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 2`，或故事大纲、holomap、drafting 出现挂章失败与密度失衡
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、故事大纲、holomap、drafting

## Scope

本模块只负责 `2-Planning` 的 Step 2：

- 锁定整书总章数、卷篇拆分、章节功能槽与节奏窗口
- 把篇幅体量翻译成角色、场景、物品、线索、伏笔的密度合同
- 为后续 Step 3-8 提供稳定章节容器

本模块不负责：

- 代写卷级剧情主干
- 越权决定冲突、任务、线索、伏笔的具体内容
- 用平均分章替代章节功能设计

## Load Contract

- 加载条件：
  - 正常执行 Step 2
  - 后续模块或 drafting 无法稳定挂章
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Cards/**/*.json`
  - `.webnovel/state.json`（若存在）
- 模板依赖：
  - `templates/chapter-planning.json`
- 局部经验层：
  - 如需读取挂章返工顺序、密度失衡修法，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Cards/**/*.json`
- 预估篇幅、卷数、章节节奏与对象规模

## Output Contract

- 模板：`templates/chapter-planning.json`
- 正式输出：`Planning/2-章节规划.json`
- 必须产出：
  - 卷篇结构
  - chapter / volume blocks
  - function slots
  - density contract
  - 节奏窗口与换挡区

## Decision Focus

1. 整书是短、中还是长篇？卷篇如何分布？
2. 每个章节板块承担什么功能，而不是只有数量？
3. 哪些高潮、换挡、喘息、桥接窗口必须显式存在？
4. 当前体量对应怎样的角色、场景、物品、线索、伏笔密度？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `章节容器对齐` | `series_scale`、`volume_blocks`、`function_slots` | 只有章节数量，没有容器功能 | 卷篇拆分对后续挂章的支持度 | 先锁章节容器，再谈剧情填充 |
| `成立轴` | `密度承载成立` | `density_contract`、`cast_load`、`thread_load` | 体量与对象密度失衡 | 容器对角色/线索/伏笔负荷的承载度 | 只有能承住负荷的章节结构才成立 |
| `优选轴` | `节奏弹性收益` | `pacing_windows`、`transition_buffers`、`climax_spacing` | 节奏窗口被平均主义抹平 | 可写性、换挡余量、后续 holomap 编组弹性 | 在成立解中选最利于长期编排的容器方案 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `series_scale`、`volume_blocks`、`function_slots` | 采用哪种章节容器形态 | 圈定体量与卷篇方案 | 先形成能承接后续模块的容器 |
| `细裁决 / Range Narrowing` | `density_contract`、`cast_load`、`thread_load` | 哪种容器真的承得住对象负荷 | 排除密度失衡方案 | 保留密度合同成立的章节结构 |
| `离散裁决 / Final Selection` | `pacing_windows`、`transition_buffers`、`climax_spacing` | 在成立解中哪套节奏更稳 | 比较节奏弹性与后续挂载收益 | 输出最可持续的章节板块与窗口设计 |

## Design Levers

- 先定章节容器，再谈剧情节点
- 密度合同必须采用区间带，而不是一个死数
- 长线越多，越需要稳定功能槽，而不是平均分章

## High Risk Signals

- 只有“第一卷 30 章”式平均分配
- 章节功能槽缺失，导致 3-8 步无稳定挂点
- 群像规模、线索密度与体量明显不匹配

## Handoff Contract

- `story-outline` 必须把叙事主干挂入本模块的 volume blocks 与 function slots
- `holomap` 必须能回指本模块的密度合同是否被承接
- 若后续模块无法稳定挂章，必须先回本模块，而不是各自局部补丁

## Verification Checklist

1. `container gate`
   - 已形成章节容器，而不是仅有数量分配
2. `density gate`
   - 角色/线索/伏笔密度与体量匹配
3. `boundary gate`
   - 本模块没有越权代做剧情与长线内容
4. `handoff gate`
   - Step 3-8 都有明确挂载位点可读
