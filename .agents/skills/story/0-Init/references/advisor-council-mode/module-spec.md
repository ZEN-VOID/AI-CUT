# 智能顾问团模式模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `init_mode == 智能顾问团模式`
- `entrypoint`: `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Advisor Council Contract`、`Step 0.5`、`Step 0.6`
- `primary_consumers`: 初始化协调助手、顾问 subagents、最终确认卡生成流程

## Scope

本模块只负责 `智能顾问团模式` 的执行细则：

- 如何校验顾问 agent 路径
- 如何处理 `策划 / 监制 / 评审` 三阶段顾问布阵
- 如何构造统一初始化 brief
- 如何并发发起顾问会诊
- 如何把会诊结果收束为初始化合稿

本模块不负责：

- 重复定义三种模式的总入口
- 把完整问卷链搬回顾问团模式
- 直接改写 `1-Cards` 或 `2-Planning` 的 canonical

## Load Contract

- 加载条件：`init_mode == 智能顾问团模式`
- 互斥规则：本模块成为主执行细则后，不得再加载 `references/fast-mode/module-spec.md` 或 `references/autonomous-mode/module-spec.md` 作为主路径
- 上下文规则：进入本模块后，如需局部经验与故障恢复策略，再加载同目录 `CONTEXT.md`
- 交互闸门：不得进入完整问卷链；仅允许最终确认卡，必要时加 1 张用户裁决卡

## Mode Goal

让指定顾问团围绕同一份初始化 brief 一次性完成会诊，输出可直接落盘的初始化合稿，而不是把顾问团变成“每轮都来发言的陪聊层”。

## Think-Think Design Snapshot

### 三轴

| 轴角色 | 本模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | 会诊合稿优先 | 当前任务是否应该收敛为“统一 brief -> 顾问会诊 -> 单次综合”，而不是回到问卷链 | `Execution Procedure`、`mode gate` |
| `成立轴` | 分歧可暴露成立 | 哪些顾问意见能进入共识、哪些必须以分歧或裁决卡形式暴露 | `One-Shot Internal Task Templates`、`council gate` |
| `优选轴` | 共识与来源兼得 | 在成立方案中，哪种综合方式最利于保留 provenance 并写回正式 handoff/state | `Output Contract`、`Output Landing Contract` |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 当前是否命中顾问团会诊，而不是快速补全或自主问卷 | `Load Contract`、`Required Inputs` |
| `细裁决 / Range Narrowing` | 哪些意见构成共识、哪些属于关键分歧、哪些需要用户裁决 | `协调汇总模板`、`Execution Procedure` |
| `离散裁决 / Final Selection` | 最终采用哪份可写回且 provenance 清晰的初始化合稿 | `Output Landing Contract`、`Verification Checklist` |

## Required Inputs

- 用户原始需求、风格偏好、禁飞区、目标平台
- `team_setup.team_mode`
- `team_setup.shared_agents`
- `team_setup.roles.planning.members`
- `team_setup.roles.production.members`
- `team_setup.roles.review.members`
- `advisor_agents`（legacy mirror，默认映射策划阶段）
- `research_policy`
- `decision_owner`
- 当前已知字段与明显缺口
- 已触发的题材/世界/创意参考

## Shared Dependency Contract

- 必读共享入口：
  - `templates/genres/README.md`
- 按需共享依赖：
  - `templates/genres/{genre}.md`
  - `templates/genres/details/{genre_slug}/`
  - `templates/worldbuilding/*.md`
  - `references/creative-seed-routing/module-spec.md`

加载原则：

1. 本模块是顾问会诊的主路径，但不替代共享题材/世界观/创意资产根目录。
2. 创意相关资料必须先经过 `creative-seed-routing` 的统一路由，再被压进 `initialization_brief`，而不是让每位顾问各自漫游 leaf references。
3. 若共享资料无法形成稳定共识，应保留分歧并暴露给协调汇总层，而不是假装顾问团天然一致。

## One-Shot Internal Task Templates

### 模板 A：顾问单线程任务模板

```text
你现在参与 story2026 的“智能顾问团模式”初始化会诊。

你的身份来源：
- 先严格遵守你自己的 agent 文档
- 本次任务边界以 0-Init 初始化合同为准

你的任务：
基于同一份初始化 brief，一次性给出你对本书立项的专业建议，目标是帮助协调助手生成可直接落盘的初始化合稿，而不是继续向用户发散提问。

硬约束：
1. 不得改写用户已确认字段。
2. 不得越权把对象 canonical 或规划 canonical 提前拍死。
3. 只在 truly blocking 的冲突上提出“需要用户裁决”。
4. 输出必须显式区分：`council_advised`、`user_confirmed`、`unknowns`。

请按以下结构返回：
1. `advisor_position`
2. `project_contract`
3. `cards_seed`
4. `planning_seed`
5. `unknowns`
6. `risk_flags`
7. `need_user_decision`
```

### 模板 B：协调汇总模板

```text
你现在是 story2026 初始化协调助手，正在处理“智能顾问团模式”。

输入：
- 用户原始 brief
- 多位顾问的结构化会诊结果
- 当前已确认字段

你的任务：
一次性综合顾问团意见，形成可落盘初始化包。

必须输出：
1. `共识`
2. `关键分歧`
3. `建议采用方案`
4. `少数派高价值提醒`
5. `project_contract`
6. `cards_seed`
7. `planning_seed`
8. `unknowns`
9. `sources_breakdown`

裁决规则：
- 用户已确认 > 顾问共识 > 高质量少数派提醒 > 协调助手保守推断
- 只有当关键分歧会直接改变题材承诺、规模、核心冲突或主角结构时，才允许生成 1 张用户裁决卡
```

## Execution Procedure

1. 先确定顾问团布阵方式：`同一套班底三阶段通用` 或 `三阶段分别指定`。
2. 校验每个阶段涉及的 agent 路径真实存在且是可读的 agent 规则文档。
3. 构造统一 `initialization_brief`，包括用户输入、已知字段、缺口、参考触发结果、三阶段布阵，以及不可越权边界。
4. 并行启动顾问线程，逐个发送“顾问单线程任务模板”。
5. 收集全部顾问输出后，执行“协调汇总模板”。
6. 若存在高后果分歧，向用户发送 1 张裁决卡；否则直接生成初始化摘要草案。
7. 在确认卡通过后，调用初始化落盘脚本，并把三阶段布阵落到 `TEAM.toml`。

## Output Contract

- 必须产出完整的 `project_contract + cards_seed + planning_seed + unknowns`
- 必须附带 `sources_breakdown`
- 必须显式记录：
  - 哪些字段是 `user_confirmed`
  - 哪些字段是 `council_advised`
  - 哪些字段是 `assistant_inferred`

## Output Landing Contract

顾问团模式的会诊结果必须能直接回填到 `0-Init` 的正式写回链路：

- `Init/north_star_contract.json`
  - 承接用户确认与顾问共识中的长期约束，不直接照抄所有顾问原话
- `Init/初始化简报.json`
  - 必须写入 `project_contract / cards_seed / planning_seed / unknowns / sources_breakdown`
- `.webnovel/state.json`
  - 必须记录 `init_mode / team_setup / advisor_agents(legacy) / research_policy / decision_owner / mode_source`
- `TEAM.toml`
  - 必须记录 `策划 / 监制 / 评审` 三阶段的 `智能顾问团 / 成员 / 管辖`
- `.webnovel/task_log.jsonl`
  - 必须能回溯顾问建议、用户确认与助手综合推断的来源分层

若顾问会诊只留下自然语言纪要，却不能稳定映射到上述位点，视为本模块输出未闭环。

## Fallback

- 若无法并发 subagents：顺序读取顾问 agent 文档并模拟顾问纪要，但必须标注为降级执行。
- 若顾问路径失效：中止顾问团模式，要求用户修正路径或切换模式。

## Verification Checklist

1. `mode gate`
   - 顾问团模式执行中不得回流到 Step 1-4 问卷链。
2. `dependency gate`
   - 共享依赖被压进统一 brief，而不是让顾问各自读取出不同入口真源。
3. `council gate`
   - 输出同时保留 `共识 / 关键分歧 / 少数派高价值提醒`。
4. `provenance gate`
   - `user_confirmed / council_advised / assistant_inferred` 三层来源都能追溯。
5. `landing gate`
   - 会诊结果可直接映射到 `north_star_contract.json`、`初始化简报.json` 与 `.webnovel/state.json`。
