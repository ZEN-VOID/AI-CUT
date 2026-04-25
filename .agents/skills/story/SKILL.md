---
name: story2026
description: Use when coordinating, routing, initializing, or repairing the overall story2026 小说/novel/book workflow across stage skills, shared references, shared scripts, and runtime truth sources; for 影片/电影/影视/video project initialization use `aigc-init`.
governance_tier: lite
allowed-tools: Read Grep Bash Write Edit Task
---

# story2026

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载跨阶段经验层，不得覆盖本 `SKILL.md` 的总线路由与真源边界。
- 若 `CONTEXT.md` 与当前目录结构不一致，先修根级真源，再继续下游阶段。

## Overview

`story2026` 根级 skill 是整条小说流水线的总入口与总线合同。

它只统一回答四件事：

1. 当前诉求应该路由到哪个阶段 skill。
2. 哪一层才是这类问题的 canonical truth。
3. 根级 `_shared`、`scripts`、`templates` 分别承担什么共享职责。
4. 题材方向盘如何通过 `1-Cards/5-类型卡` 进入 planning / drafting / validation。

硬边界：

- 根级 `story/SKILL.md` 只负责跨阶段拓扑、共享载体边界、总路由和根因追溯总则。
- 各阶段目录下的 `SKILL.md` 负责本阶段的严格执行合同。
- 根级 `CONTEXT.md` 只沉淀跨阶段经验，不吞并阶段私有故障模式。

## 类型机制

`story` 现在采用：

- 固定主链
- 人工维护的 `类型卡`

二层架构。

### 固定主链

主链固定不变：

1. `0-Init`
2. `1-Cards`
3. `2-Planning`
4. `3-Drafting`
5. `4-Review`
6. `review`
7. `5-Loopback`

### 人工类型卡

题材机制不再依赖旧的“系统自动题材装配”机制。

当前规则固定为：

- `0-Init` 只提供题材 seed 与初始设定，不自动锁定题材系统。
- `1-Cards/5-类型卡/**/*.json` 是唯一题材方向盘真源。
- `2-Planning` 只导入 `story_promise / genre_corridor / navigation_rules`，不再二次猜题材。
- `3-Drafting` 只消费人工题材承诺与 planning handoff，不再消费自动 step hook。
- `4-Review` 继续做结构/连续性/逻辑/人物/时间线/任务汇聚校验，不再保留独立自动类型兑现维度；默认后台启用 `code-reviewer` 做独立审计，再把 findings 回流为修复分流。
- `5-Loopback` 可以沉淀反馈，但不得自动改写 `类型卡`。

硬规则：

- 通用基座必须能在没有任何题材包目录的情况下独立运行。
- 题材判断默认属于人工创作层，不得再被系统隐式反向硬绑。
- 若题材方向发生变化，优先修改 `类型卡`，不要在 downstream 阶段静默偷改。

## When to Use

- 用户只说“用 story2026 做这件事”，但还没有明确该进哪一个阶段。
- 需要设计、选择或解释某个项目的 `类型卡` / 题材方向盘。
- 需要判断某个问题应归 `0-Init / 1-Cards / 2-Planning / 3-Drafting / 4-Review / review / 5-Loopback / query / resume` 中的哪一层。
- 需要修复跨阶段路由、共享 reference、共享脚本、真源分工、运行态数据流的源层问题。

## System Topology

### Mainline Stages

主链固定为：

1. `0-Init`
2. `1-Cards`
3. `2-Planning`
4. `3-Drafting`
5. `4-Review`
6. `review`
7. `5-Loopback`

执行原则：

- 主链默认按阶段顺序串行，不得跳过上游真源直接伪造下游结论。
- `review` 是 `4-Review` 的承接层，不拥有评估判断权。
- `5-Loopback` 只在 `4-Review = PASS` 且 handoff 明确授予 `5-Loopback` 后拥有 validated truth writeback 权。

### Satellite Skills

卫星技能固定挂在主链侧，不单独冒充新的 stage：

- `query`
- `resume`
- `doubao`

## Root Truth Ownership Contract

| 层 | 拥有的真源 | 不拥有的真源 |
| --- | --- | --- |
| 根级 `story2026` | 跨阶段拓扑、总路由、共享载体边界、默认加载顺序 | 各阶段内部执行细则、局部 reference 专业判断 |
| `0-Init` | 立项合同、`0-Init/*.yaml`、初始 seeds | 对象真源、规划真源、validated actualization |
| `1-Cards` | 类型/角色/场景/物品等对象真源 | 章节编排真源、章节审查判断 |
| `2-Planning` | 以 `1-部级 -> 2-卷级 -> 3-章级` 的三层分形结构持有 `2-Planning/整体规划.md`、`2-Planning/第N卷/卷规划.md`、`2-Planning/第N卷/第N章.md` 这组规划真源；`全息地图.json / 卷分片/*.json` 仅作兼容投影 | 对象当前态、validated actualization |
| `3-Drafting` | 以 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md` 作为章节正文唯一业务真源，由根级 `3-Drafting` 主技能直接执行 chapter-native 豆包创作；卷级写作日志等运行时工件仅作兼容 carrier，不再定义主创拓扑 | 评估判断权、validated truth writeback |
| `4-Review` | `validation_fact_pack` covenant、卷级隔离评估、父层 `4-Review/第V卷.validation.json` 聚合 gate | 审查报告持久化、actualization 写回 |
| `review` | 审查报告、评分落库、状态持久化 | `validation_status` 判定、actualization 写回 |
| `5-Loopback` | validated actualization、projection refresh、`5-Loopback/第V卷.loopback.json` | 未通过验证或未被 handoff 授权的修改写回 |
| `query / resume` | 查询、恢复 | 主链 canonical truth 判定权 |
| `doubao` | 风格分析、中文表达强化、候选润色正文与用户显式授权下的单点覆写 | `Cards / Planning / validation_status / actualization` 判定权 |

## Canonical Runtime Root

- 书项目正式业务根目录：`projects/story/<项目名>/`
- legacy `projects/aigc/<项目名>/` 仅允许作为兼容 fallback，不再是 canonical runtime。
- 根层项目入口文件固定写在：
  - `projects/story/<项目名>/STATE.json`
  - `projects/story/<项目名>/team.yaml`
  - `projects/story/<项目名>/MEMORY.md`
  - `projects/story/<项目名>/CHANGELOG.md`
  - `projects/story/<项目名>/CONTEXT/`

## Shared Carrier Contract

### 根级 `_shared/`

根级 `_shared/` 是当前 `story` 技能树的跨阶段共享真源层。

默认先读：

- `_shared/context-loading-contract.md`
- `_shared/core-constraints.md`

按需读取：

- `_shared/story_map.schema.json`
- `_shared/story_map_bootstrap.template.json`
- `_shared/entity-management-spec.md`
- `_shared/strand-weave-pattern.md`

可选增强材料：

- `_shared/genre-profiles.md`
- `_shared/reading-power-taxonomy.md`
- `_shared/cool-points-guide.md`

### 根级 `scripts/`

根级 `scripts/` 是 story2026 的共享脚本入口层，负责：

- canonical path helper
- workflow / state / status 管理
- shared CLI entrypoint
- 多阶段共用的数据访问与校验

### 根级 `templates/`

根级 `templates/` 只放跨阶段或跨模块共享模板、共享 schema 载体。

## Routing Contract

| 用户诉求 / 问题形状 | 默认入口 |
| --- | --- |
| 设计/选择/解释题材方向盘或 `类型卡` | 根级 `story2026`，必要时再路由到 `1-Cards/类型卡` |
| 初始化小说、初始化网文、新建书、新建长篇故事、小说项目起盘 | `0-Init` |
| 初始化影片、初始化电影、初始化影视、初始化视频项目 | 不进入 story；route to `.agents/skills/aigc/0-初始化/SKILL.md` |
| 新建项目、确定创作立项、初始化问卷/顾问团 | `0-Init` |
| 全局卡/类型卡/风格卡/角色卡/场景卡/物品卡生成、回写、覆盖率修复 | `1-Cards` |
| 长篇规划、MAP、章节编排、冲突/任务/线索/伏笔设计 | `2-Planning` |
| 写章节、润色、章节级执行包、正文产出 | `3-Drafting` |
| 明确要求“按章写正文”、输出到 `3-Drafting/第N卷/第N章.md`、或要求 YAML 头携带 global/style/`north_star` 摘要 | `3-Drafting` |
| 隔离评估、checker 团队、`validation_status` | `4-Review` |
| 审查报告、评分落库、审查结果持久化 | `review` |
| PASS 后的 actualization、truth writeback、projection refresh | `5-Loopback` |
| 查询当前态、规划态、实绩态、质量态 | `query` |
| 查看断点、续跑、清理或重启任务 | `resume` |
| 中文小说润色、文风拆解、整稿统修、去 AI 味与中文表达强化 | `doubao` |

## Default Loading Order

1. 先读取根级 `SKILL.md`，锁定跨阶段拓扑与共享层边界。
2. 再读取根级 `CONTEXT.md`，避免重复踩跨阶段老坑。
3. 若当前任务已绑定 `projects/story/<项目名>/`，必须先读取 `projects/story/<项目名>/MEMORY.md`，再读取 `projects/story/<项目名>/CONTEXT/` 下与本轮相关的项目级上下文文件。
4. 若问题涉及共享合同，先读根级 `_shared/context-loading-contract.md` 与对应阶段的 `_shared/*`。
5. 若当前项目已锁定题材方向盘，优先读取 `1-Cards/5-类型卡/**/*.json` 与 `2-Planning/整体规划.md`；如项目仍在兼容态，再回退到 `全息地图.json`。
6. 若当前诉求涉及终验或 actualization，继续读取：
   - `4-Review/_shared/validation-fact-pack-spec.md`
   - `5-Loopback/_shared/loopback-actualization-spec.md`
7. 路由到目标阶段的 `SKILL.md`。
8. 读取目标阶段 `CONTEXT.md`。

## Root-Cause Execution Contract (Mandatory)

当 `story2026` 出现跨阶段路由错误、真源分工混乱、共享 reference 漂移、共享脚本路径失配、根入口缺失或总线合同断裂时，必须按以下链路上溯：

1. `Symptom / Failure`
2. `Direct Technical Cause`
3. `Rule Source`
4. `Meta Rule Source`
5. `Fix Landing Points`

执行顺序硬约束：

- 先修总线真源，再修阶段投影。
- 若同一条规则需要在两个以上阶段重复改写，必须先判断是否缺少根级 canonical source。

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| FIELD-SYS-ROUTING-01 | Step 1 | 判定当前诉求属于哪个阶段与 truth role | `target_stage`、`truth_role` | FAIL-SYS-ROUTING-01 | 回到路由表，先判真源再判阶段 |
| FIELD-SYS-CARRIER-02 | Step 2 | 判断应读取哪些根级共享 carrier | `shared_refs_to_load`、`shared_scripts_needed` | FAIL-SYS-CARRIER-02 | 回到根级 `_shared/*.md` 与共享层边界合同 |
| FIELD-SYS-TYPECARD-03 | Step 3 | 判断当前项目的题材方向盘是否已被 `类型卡` 正式承接 | `type_card_refs`、`story_promise_summary`、`genre_corridor_summary` | FAIL-SYS-TYPECARD-03 | 回到 `1-Cards/类型卡` 与 `2-Planning` 导入链 |
| FIELD-SYS-OWNER-04 | Step 4 | 锁定该问题的 canonical owner | `canonical_owner`、`non_owner_layers_to_avoid` | FAIL-SYS-OWNER-04 | 回到真源分工表，禁止让下游冒充上游 |
| FIELD-SYS-TRACE-05 | Step 5 | 完成跨阶段 root-cause trace | `symptom`、`direct_cause`、`rule_source`、`meta_rule_source` | FAIL-SYS-TRACE-05 | 重新补全分层 trace，不能停在局部症状 |
| FIELD-SYS-CLOSURE-06 | Step 6 | 产出修复闭环与防回归结果 | `root_cause_location`、`immediate_fix`、`systemic_prevention_fix` | FAIL-SYS-CLOSURE-06 | 回到修复落点，优先改根级真源 |

## Completion Gate

- 已能明确把任一泛化 `story2026` 请求路由到唯一默认入口。
- 已能说明该请求应读的 canonical truth 与不该误读的非真源层。
- 已区分根级 `_shared`、`scripts/`、`templates/` 的共享职责。
- 已能说明当前项目的题材方向盘如何从 `类型卡` 进入 planning / drafting / validation。
- 已能指出 repo 级 `.codex/` 真源与项目级 `STATE.json.workflow_runtime` 内联工件链的分工。
- 已能说明 planning root/slice 的分工、`validation_fact_pack` 的 covenant，以及 loopback 的 PASS+handoff gate。
