# 全息地图模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 8`，或下游需要统一读取章节-时间线-节点关系
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、3-Drafting、query、resume、loopback

## Scope

本模块只负责 `2-Planning` 的 Step 8：

- 把前 1-7 份 planning 文件收束为唯一 canonical truth `Planning/8-全息地图.json`
- 维护时间轴、空间轴、集序轴与 chapter boards 的统一组织
- 为下游提供 holomap-first 的导航、编组与校验入口

本模块不负责：

- 越权重写前 1-7 的上游裁决
- 把 holomap 降格为摘要页
- 在写回 actualization 时静默覆盖 planned state

## Load Contract

- 加载条件：
  - 前 1-7 份 planning 文件已稳定，需要收束为唯一真源
  - drafting/query/resume/loopback 需要统一读取章节-时间线-节点关系
- 上游依赖：
  - `Planning/1-题材选型.json`
  - `Planning/2-章节规划.json`
  - `Planning/3-故事大纲.json`
  - `Planning/4-冲突设计.json`
  - `Planning/5-任务设计.json`
  - `Planning/6-线索设计.json`
  - `Planning/7-伏笔设计.json`
  - `Cards/**/*.json`
  - `.webnovel/state.json`（若存在）
- 模板依赖：
  - `templates/holomap.json`
- 局部经验层：
  - 需要读取三轴收束、chapter board 校验、actualization 写回避坑时，再加载同目录 `CONTEXT.md`

## Required Inputs

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Planning/4-冲突设计.json`
- `Planning/5-任务设计.json`
- `Planning/6-线索设计.json`
- `Planning/7-伏笔设计.json`
- `Cards/**/*.json`
- `.webnovel/state.json`（若存在）

## Output Contract

- 模板：`templates/holomap.json`
- 正式输出：`Planning/8-全息地图.json`
- 真源身份：下游默认规划入口
- 必须产出：
  - `timeline_axis`
  - `space_axis`
  - `episode_sequence_axis`
  - `chapter_boards`
  - `cross_thread_indexes`
  - `planned_* + actualization` 并存容器

## Decision Focus

1. 时间轴、空间轴、集序轴是否同时成立？
2. 每个 chapter board 是否能回答六问底盘？
3. 长线对象能否跨章追踪？
4. actualization 是否与 planned state 并存，而不是静默覆盖？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `真源收束对齐` | `timeline_axis`、`space_axis`、`episode_sequence_axis`、`chapter_boards` | 只有摘要，没有导航与编组 | 三轴与章节板对下游消费的支撑度 | 先锁 holomap 的真源组织骨架 |
| `成立轴` | `跨线程追踪成立` | `cross_thread_indexes`、`lifecycle_lexicon`、`chapter_linkage`、`state_transition` | 长线对象无法跨章反查 | 线程索引与状态流是否闭合 | 只有可追踪、可回查的 holomap 才成立 |
| `优选轴` | `下游消费收益` | `holomap_first_readability`、`actualization_container`、`chapter_board_density` | 下游仍需二次拼导航层 | drafting/query/resume/loopback 的默认消费效率 | 在成立解中选最利于下游直接消费的 holomap 形态 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `timeline_axis`、`space_axis`、`episode_sequence_axis`、`chapter_boards` | 先形成哪种真源骨架 | 圈定三轴与章节板编组 | 保证 holomap 不是摘要页 |
| `细裁决 / Range Narrowing` | `cross_thread_indexes`、`lifecycle_lexicon`、`chapter_linkage`、`state_transition` | 哪种骨架真的能承住长线追踪 | 排除不可回查、不可追踪的方案 | 保留线程索引与状态流闭合的结构 |
| `离散裁决 / Final Selection` | `holomap_first_readability`、`actualization_container`、`chapter_board_density` | 哪个成立解最利于下游直接消费 | 比较可读性、actualization 并存与节点密度 | 输出 holomap-first 的唯一 canonical truth |

## Design Levers

- holomap 的三大职责：
  - 导航职责
  - 编组职责
  - 校验职责
- 单章节点最小密度是“六问底盘”，不是摘要段落
- lifecycle 统一采用：
  - 出现
  - 激活
  - 转移
  - 解决
  - 兑现
  - 退场

## High Risk Signals

- 只有时间轴，没有空间轴或集序轴
- chapter board 看不到挂载关系，只能看摘要
- loopback 写回时覆盖 `planned_*` 而不是写入 actualization 容器

## Handoff Contract

- `3-Drafting / query / resume / loopback` 都默认 holomap-first
- 若 holomap 无法解释某章为何必须这样排，必须回溯前 1-7 的最早失稳文件

## Verification Checklist

1. `truth gate`
   - `Planning/8-全息地图.json` 已成为唯一 canonical truth
2. `three-axis gate`
   - 时间轴、空间轴、集序轴三轴同时成立
3. `chapter-board gate`
   - 每个 chapter board 可回答六问底盘
4. `actualization gate`
   - actualization 与 planned state 并存
5. `downstream gate`
   - drafting/query/resume/loopback 可默认 holomap-first
