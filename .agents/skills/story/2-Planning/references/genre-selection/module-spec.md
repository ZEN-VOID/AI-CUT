# 题材选型模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `planning_step == 1`，或任一步出现题材漂移、平台承诺失焦、禁飞区失效
- `entrypoint`: `2-Planning/SKILL.md` 的 `单技能治理规则`、`任务流程`、`条件加载矩阵`，以及 `references/README.md` 的模块索引
- `primary_consumers`: planning 主协调链路、题材返工链路、后续 `chapter-planning / story-outline / holomap`

## Scope

本模块只负责 `2-Planning` 的 Step 1：

- 锁定主副题材组合、题材走廊、平台承诺与禁飞区
- 判断哪些副题材会真实改变后续章节、冲突、任务与线索结构
- 为后续 2-7 步提供题材边界，而不是代做章节、剧情或长线设计

本模块不负责：

- 直接决定章节容器或卷篇拆分
- 直接书写卷级主干与具体事件清单
- 在 `references/` 内复制私有题材套路库

## Load Contract

- 加载条件：
  - 初次进入整书 planning
  - `chapter-planning`、`story-outline`、`holomap` 任一步出现题材漂移
- 上游依赖：
  - `Init/north_star_contract.json`
  - `Init/初始化简报.json`
  - `Cards/**/*.json`
- 共享依赖：
  - `templates/genres/README.md`
  - `templates/genres/{genre}.md`
  - `templates/genres/details/{genre_slug}/`（仅在入口模板不足以支撑裁决时按需读取）
- 模板依赖：
  - `templates/genre-selection.json`
- 局部经验层：
  - 进入本模块后，如需局部避坑、返工顺序与题材漂移修法，再读取同目录 `CONTEXT.md`

## Required Inputs

- `Init/north_star_contract.json`
- `Init/初始化简报.json`
- `Cards/**/*.json`
- 平台语义、受众承诺、风格偏好、世界规则中的硬约束

## Output Contract

- 模板：`templates/genre-selection.json`
- 正式输出：`Planning/1-题材选型.json`
- 必须产出：
  - 题材承诺句
  - 主副题材组合与配比
  - 平台承诺
  - 禁飞区
  - 下游 hooks（供 Step 2-8 读取）

## Decision Focus

1. 这本书向读者承诺的核心阅读体验是什么？
2. 哪些副题材会真实改变后续结构，而不是只改变包装语义？
3. 哪些元素只能当热词包装，不能升格为有效辅题材？
4. 哪些套路、语气、世界规则越界必须提前封禁？

## Think-Think Embedded Contract

### 三轴

| 轴角色 | 当前模块轴名 | 驱动字段 | 判废字段 | 对比字段 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `题材承诺收束` | `reader_promise`、`primary_genre`、`platform_fit` | 题材标签不能改变后续结构 | 主副题材对后续 2-8 步的驱动强度 | 先锁真正驱动整书的题材方向盘 |
| `成立轴` | `结构影响成立` | `secondary_genre_effect`、`genre_corridor`、`forbidden_zone` | 副题材只改包装、不改结构 | 副题材对章节/冲突/任务的真实影响范围 | 只有会改结构的副题材才允许保留 |
| `优选轴` | `长期走廊收益` | `series_sustainability`、`tone_stability`、`downstream_hooks` | 题材组合后续无法持续供给 | 长期连载稳定性与下游 hooks 清晰度 | 在成立解中选最稳的题材走廊 |

### 三重

| 裁决层 | 本层关键向字段 | 本层问题 | 本层动作 | 本层结论 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `primary_genre`、`reader_promise`、`platform_fit` | 先进入哪类题材走廊 | 圈定主题材候选簇 | 先定主驱动，不让包装热词抢方向盘 |
| `细裁决 / Range Narrowing` | `secondary_genre_effect`、`genre_corridor`、`forbidden_zone` | 哪些副题材真的成立 | 排除只改包装不改结构的辅题材 | 保留会改变后续规划结构的副题材 |
| `离散裁决 / Final Selection` | `series_sustainability`、`tone_stability`、`downstream_hooks` | 在成立解中选哪个组合最稳 | 比较长期可写性与下游承接力 | 输出可持续的主副题材组合与禁飞区 |

## Design Levers

- 四层承诺：
  - 情绪承诺
  - 推进引擎
  - 世界语法
  - 边界与禁飞区
- 主副题材只允许 `主驱动 + 辅增压`，不允许双主题材互抢方向盘
- 题材知识归共享 `templates/genres/`，本模块只保留 Step 1 的裁决合同

## High Risk Signals

- 只剩标签列表，没有题材承诺句
- 副题材不会改变后续结构，却仍被当成有效辅题材
- 禁飞区缺失，导致后续 planning 无法回正

## Handoff Contract

- `chapter-planning` 必须读取本模块的题材走廊与题材配比
- `story-outline` 必须把主问题建立在本模块锁定的题材承诺之上
- 若 3-7 任一步出现题材漂移，优先回到本模块，不直接修 holomap

## Verification Checklist

1. `promise gate`
   - 已写出可执行的题材承诺，而非标签堆叠
2. `boundary gate`
   - 本模块没有代做章节、剧情或长线系统
3. `shared-asset gate`
   - 题材知识来自共享 `templates/genres/`，未在 `references/` 内复制
4. `handoff gate`
   - 输出已包含供 Step 2-8 读取的 hooks 与禁飞区
