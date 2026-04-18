---
name: story2026
description: Use when coordinating, routing, or repairing the overall story2026 workflow across stage skills, shared references, shared scripts, and runtime truth sources.
governance_tier: lite
allowed-tools: Read Grep Bash Write Edit Task
---

# story2026

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载跨阶段经验层，不得覆盖本 `SKILL.md` 的总线路由与真源边界。
- 若 `CONTEXT.md` 与当前目录结构不一致，先修根级真源，再继续下游阶段。

## Overview

`story2026` 根级 skill 是整个小说流水线的总入口与总线合同，不是“把各阶段再抄一遍”的大目录说明书。

它只统一回答四件事：

1. 当前诉求应该路由到哪个阶段 skill。
2. 哪一层才是这类问题的 canonical truth。
3. 根级 `_shared`、`scripts`、`templates`、`type-packs` 分别承担什么共享职责。
4. 当前项目应如何在“不改主链”的前提下启用 `type-pack` 类型化处理能力。

补充治理约束：

- 书项目 canonical runtime root 固定为 `projects/story/<项目名>/`。
- repo 级复杂任务治理真源固定回指 `.codex/schemas/`、`.codex/runbooks/`、`.codex/registry/`。
- 书项目级 tracked run 运行态固定内联到 `STATE.json.workflow_runtime`。
- `workflow_state / execution_state / task_log / governance_index` 均属于 `STATE.json.workflow_runtime` 的内联子层，不再拆成 `.webnovel/tasks/` 或旧独立状态文件。

硬边界：

- 根级 `story/SKILL.md` 负责跨阶段拓扑、共享载体边界、总路由和根因追溯总则。
- 根级 `story/SKILL.md` 负责 `type-pack` 总体机制、组合顺序、投影边界与 resolver 回指。
- 各阶段目录下的 `SKILL.md` 负责本阶段的严格执行合同。
- 根级 `CONTEXT.md` 只沉淀跨阶段经验，不吞并阶段私有故障模式。

## Type-Pack Mechanism

`story` 当前采用：

- 固定 `method kernel`
- 可增长 `type-pack`

二层架构。

### Method Kernel

固定主链不变：

1. `0-Init`
2. `1-Cards`
3. `2-Planning`
4. `3-Drafting`
5. `4-Validation`
6. `review`
7. `5-Loopback`

### Type-Pack

`type-pack` 不是新的 stage，而是对固定主链的类型化增强包，按项目当前 `type_stack` 注入：

- 读者承诺
- 叙事引擎
- 禁写模式
- 阶段 hook
- 类型兑现维度
- loopback 反馈槽

canonical root：

- `.agents/skills/story/type-packs/`

canonical contracts：

- `type-packs/网文/`
- `type-packs/扩维与调整指南.md`
- `_shared/type-pack-loading-contract.md`

### Active Type Stack

项目当前激活 stack 固定由 `0-Init/north_star.yaml` 锁定：

- `base`
- `primary`
- `secondary[]`
- `platform[]`
- `audience[]`

默认规则：

- 未显式声明时，只加载 `_base`
- `0-Init` 拥有 canonical `type_stack` 锁定权
- `5-Loopback` 只能沉淀 pack 反馈，不得改写 canonical `type_stack`

### Stage Projection

各阶段的默认投影职责固定为：

- `0-Init`
  - 锁定 `type_stack`
- `1-Cards`
  - 把 pack 规则翻译成角色/场景/物品卡的功能槽
- `2-Planning`
  - 把 pack 规则投影到 `story_promise / genre_corridor / navigation_rules`
- `3-Drafting`
  - 按 1-7 工序注入 step-specific hook
- `4-Validation`
  - 增加独立 `类型兑现` 维度与 hard fail signal
- `review`
  - 输出质量结论与类型兑现叙述
- `5-Loopback`
  - 只沉淀 validated feedback 到下一轮 projection 参考

硬规则：

- 通用基座必须能在没有任何显式 `type-pack` 的情况下独立运行
- 类型化知识默认属于增强层，不得反向变成基座硬依赖
- 若 pack 冲突，先报冲突，再裁决；不得静默吞并

## When to Use

- 用户只说“用 story2026 做这件事”，但还没有明确该进哪一个阶段。
- 需要设计、选择、组合或解释某个项目的 `type-pack` / `type_stack`。
- 需要判断某个问题应归 `0-Init / 1-Cards / 2-Planning / 3-Drafting / 4-Validation / review / 5-Loopback / query / resume` 中的哪一层，或是否只是辅助命令 `/story-learn`。
- 需要修复跨阶段路由、共享 reference、共享脚本、真源分工、运行态数据流的源层问题。
- 需要解释 `story2026` 的整条主链、卫星技能关系与默认加载顺序。

## When Not to Use

- 已经明确要执行某个阶段内的细节工作，此时应直接进入对应阶段 skill。
- 只是阅读某个单一模块 reference 的局部细则，不涉及跨阶段路由或共享层判断。
- 只是操作某个具体书项目的数据文件，而不是维护 `story2026` 技能体系本身。

## System Topology

### Mainline Stages

主链固定为：

1. `0-Init`
2. `1-Cards`
3. `2-Planning`
4. `3-Drafting`
5. `4-Validation`
6. `review`
7. `5-Loopback`

执行原则：

- 主链默认按阶段顺序串行，不得跳过上游真源直接伪造下游结论。
- `review` 是 `4-Validation` 的承接层，不拥有评估判断权。
- `5-Loopback` 只在 `4-Validation = PASS` 且 handoff 明确授予 `5-Loopback` 后拥有 validated truth writeback 权。

### Satellite Skills

卫星技能固定挂在主链侧，不单独冒充新的 stage：

- `query`
  - 运行时事实查询。
- `resume`
  - 中断恢复与断点续跑。

默认关系：

- `query / resume` 与 `5-Loopback` 语义关联最强，但各自只处理自己的卫星职责。
- 卫星技能不改写 `Cards` / `Planning` / `validation_status` 的 canonical truth。

### Auxiliary Command

- `/story-learn`
  - 当前只保留为用户命令层的辅助入口，用于把经验沉淀进 `.webnovel/project_memory.json`。
  - 它不是主链 stage，也不是 tracked satellite workflow；若后续恢复正式技能，必须先补根级路由合同与 `scripts/workflow_manager.py` 的 command alias。

## Root Truth Ownership Contract

| 层 | 拥有的真源 | 不拥有的真源 |
| --- | --- | --- |
| 根级 `story2026` | 跨阶段拓扑、总路由、共享载体边界、默认加载顺序 | 各阶段内部执行细则、局部 reference 专业判断 |
| 根级 `type-packs/` | 类型包 schema、resolver、composition 规则、pack canonical source | 章节正文、validation gate、loopback writeback |
| `0-Init` | 立项合同、`0-Init/*.yaml`、初始 seeds | 对象真源、规划真源、validated actualization |
| `1-Cards` | 角色/场景/物品等对象真源 | 章节编排真源、章节审查判断 |
| `2-Planning` | `Planning/全息地图.json` 为核心的规划真源 | 对象当前态、validated actualization |
| `3-Drafting` | `projects/story/<项目名>/3-Drafting/第N集.md + 写作日志.yaml` 为核心的章节正文真源与工序账本 | 评估判断权、validated truth writeback |
| `4-Validation` | 隔离评估团队与 `validation_status` 判定 | 报告持久化、actualization 写回 |
| `review` | 审查报告、评分落库、状态持久化 | `validation_status` 判定、actualization 写回 |
| `5-Loopback` | validated actualization 与 truth writeback | 未通过验证或未被 handoff 授权的修改写回 |
| `query / resume` | 查询、恢复 | 主链 canonical truth 判定权 |

## Canonical Runtime Root

- 书项目正式业务根目录：`projects/story/<项目名>/`
- 根层项目入口文件固定写在：
  - `projects/story/<项目名>/STATE.json`
  - `projects/story/<项目名>/team.yaml`
  - `projects/story/<项目名>/CHANGELOG.md`
- 阶段业务产物固定落在：
  - `projects/story/<项目名>/0-Init/`
  - `projects/story/<项目名>/Cards/`
  - `projects/story/<项目名>/Planning/`
  - `projects/story/<项目名>/3-Drafting/`
  - `projects/story/<项目名>/Validation/`
  - `projects/story/<项目名>/Loopback/`

## Shared Carrier Contract

### 根级 `_shared/`

根级 `_shared/` 是当前 `story` 技能树的跨阶段共享真源层；历史根级 `references/` 不再是 canonical carrier。

默认先读：

- `_shared/context-loading-contract.md`
- `_shared/core-constraints.md`

按需读取：

- `_shared/story_map.schema.json`
- `_shared/story_map_bootstrap.template.json`
- `_shared/entity-management-spec.md`
- `_shared/strand-weave-pattern.md`
- `_shared/type-pack-loading-contract.md`

可选增强材料（不属于通用基座必读）：

- `_shared/genre-profiles.md`
- `_shared/reading-power-taxonomy.md`
- `_shared/cool-points-guide.md`

阶段专属共享合同继续留在 owning stage：

- `2-Planning/_shared/*`
- `3-Drafting/_shared/*`
- `4-Validation/_shared/*`
- `5-Loopback/_shared/*`

### 根级 `type-packs/`

`type-packs/` 是 `story` 的类型化处理真源层。

它只承载：

- 题材入口目录
- family craft 目录
- 类型化知识引用规则
- 扩维与目录治理说明

它不承载：

- 项目业务真源
- 章节正文
- validation gate packet
- actualization writeback

### 根级 `scripts/`

根级 `scripts/` 是 story2026 的共享脚本入口层，负责：

- canonical path helper
- workflow / state / status 管理
- shared CLI entrypoint
- 多阶段共用的数据访问与校验
- 内联 governance bundle 写入与引用回填

规则：

- 若同类路径、状态或 truth 读取逻辑会被两个及以上阶段复用，应优先提升到根级 `scripts/` 统一维护。
- 阶段 skill 不应各自复制一套共享 helper。

## Governance Artifact Chain

repo 级 authoritative source：

- `.codex/schemas/`
- `.codex/runbooks/`
- `.codex/registry/`

书项目级 runtime artifact chain：

- `STATE.json.workflow_runtime.workflow_state`
- `STATE.json.workflow_runtime.execution_state`
- `STATE.json.workflow_runtime.task_log`
- `STATE.json.workflow_runtime.governance_index.<run_id>.mandate`
- `STATE.json.workflow_runtime.governance_index.<run_id>.mission_brief`
- `STATE.json.workflow_runtime.governance_index.<run_id>.route_plan`
- `STATE.json.workflow_runtime.governance_index.<run_id>.preflight_verdict`
- `STATE.json.workflow_runtime.governance_index.<run_id>.artifact_manifest`
- `STATE.json.workflow_runtime.governance_index.<run_id>.validation_report`
- `STATE.json.workflow_runtime.governance_index.<run_id>.learning_record`

解释：

- tracked workflow 当前通过根级 `scripts/workflow_manager.py` 直接把这些工件内联写入 `STATE.json`。
- 阶段技能必须承认这些对象是 review / trace / closure 的共享证据层。
- `.webnovel/` 继续只保留 `index.db`、`vectors.db`、`summaries/`、`archive/` 与 `observability/` 这类辅助 runtime 载体。

### 根级 `templates/`

根级 `templates/` 只放跨阶段或跨模块共享模板、共享题材资产与统一 schema 载体。

规则：

- 阶段私有模板留在对应阶段目录。
- 一旦模板被多个阶段共享消费，应优先评估是否提升为根级 canonical carrier。

## Routing Contract

| 用户诉求 / 问题形状 | 默认入口 |
| --- | --- |
| 设计/选择/组合 `type-pack`、解释当前 `type_stack` | 根级 `story2026`，必要时再路由到 `0-Init` |
| 新建项目、确定创作立项、初始化问卷/顾问团 | `0-Init` |
| 全局卡/风格卡/角色卡/场景卡/物品卡生成、回写、覆盖率修复 | `1-Cards` |
| 长篇规划、MAP、章节编排、冲突/任务/线索/伏笔设计 | `2-Planning` |
| 写章节、润色、章节级执行包、正文产出 | `3-Drafting` |
| 隔离评估、checker 团队、`validation_status` | `4-Validation` |
| 审查报告、评分落库、审查结果持久化 | `review` |
| PASS 后的 actualization、truth writeback、projection refresh | `5-Loopback` |
| 查询当前态、规划态、实绩态、质量态 | `query` |
| 查看断点、续跑、清理或重启任务 | `resume` |
| 提炼成功模式或闭环修复后的负向 heuristic | `/story-learn`（辅助命令，非 tracked workflow） |

裁决原则：

- 先判诉求的 truth role，再判阶段。
- 若同一句话同时命中多个阶段，优先进入“最早拥有该真源的阶段”。
- 若问题涉及跨阶段漂移，先回到根级 `story2026` 入口做总线路由与源层诊断。

## Default Loading Order

1. 先读取根级 `SKILL.md`，锁定跨阶段拓扑与共享层边界。
2. 再读取根级 `CONTEXT.md`，避免重复踩跨阶段老坑。
3. 若问题涉及共享合同，先读根级 `_shared/context-loading-contract.md`、`_shared/type-pack-loading-contract.md` 与对应阶段的 `_shared/*`；若问题命中 workflow/命名漂移，再直接核对 `scripts/workflow_manager.py` 的 canonical command alias。
4. 若当前项目已锁定 `type_stack`，优先读取 `type-packs/网文/` 下与题材名同名的入口目录；除非特别说明，否则默认走该目录，再按设定补读必要的 family craft。
5. 路由到目标阶段的 `SKILL.md`。
6. 读取目标阶段 `CONTEXT.md`。
7. 若阶段采用 governed child skills 或 governed `references/`，固定顺序为：
   - 当前命中的子技能 `SKILL.md` 或 `module-spec.md`
   - 同目录 `CONTEXT.md`
   - 对应模板 / 脚本

## Root-Cause Execution Contract (Mandatory)

当 `story2026` 出现跨阶段路由错误、真源分工混乱、共享 reference 漂移、共享脚本路径失配、根入口缺失或总线合同断裂时，必须按以下链路上溯：

1. `Symptom / Failure`
   - 明确是发现失败、路由错误、共享层漂移、还是阶段真源混淆。
2. `Direct Technical Cause`
   - 确认是根入口缺文件、总路由未声明、共享 carrier 边界不清、脚本 helper 缺统一入口，还是下游误把共享文档当私有文档。
3. `Rule Source`
   - 优先检查当前根级 `SKILL.md`、根级 `CONTEXT.md`、根级 `_shared/*.md`、`type-packs/` 真源与相关共享脚本入口。
4. `Meta Rule Source`
   - 继续上溯到仓库 `AGENTS.md` 的 rollout、root-cause、context 治理与 canonical source governance 合同。
5. `Fix Landing Points`
   - 优先修复根级合同、共享 reference inventory、共享 helper，再决定是否需要修具体阶段 skill。

执行顺序硬约束：

- 先修总线真源，再修阶段投影。
- 若同一条规则需要在两个以上阶段重复改写，必须先判断是否缺少根级 canonical source。
- 收尾必须返回：`root cause location + immediate fix + systemic prevention fix`。

## SKILL vs CONTEXT Placement Matrix

- 放在根级 `SKILL.md`
  - 总路由、主链拓扑、卫星关系、共享 carrier 边界、默认加载顺序、`type-pack` 机制、跨阶段 root-cause 合同。
- 放在根级 `CONTEXT.md`
  - 跨阶段路由漂移、共享层误放置、总入口缺失、共享 helper 失配的经验与启发式。
- 放在阶段 `SKILL.md`
  - 阶段级执行合同、输入输出、门禁、模块路由、阶段专属根因修复顺序。
- 放在阶段 `CONTEXT.md`
  - 阶段专属故障模式、返工顺序、局部可复用 heuristic。

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| FIELD-SYS-ROUTING-01 | Step 1 | 判定当前诉求属于哪个阶段与 truth role | `target_stage`、`truth_role` | FAIL-SYS-ROUTING-01 | 回到路由表，先判真源再判阶段 |
| FIELD-SYS-CARRIER-02 | Step 2 | 判断应读取哪些根级共享 carrier | `shared_refs_to_load`、`shared_scripts_needed` | FAIL-SYS-CARRIER-02 | 回到根级 `_shared/*.md` 与共享层边界合同 |
| FIELD-SYS-TYPEPACK-03 | Step 3 | 判断当前项目应激活哪些 `type-pack` | `type_stack`、`active_packs`、`source_refs` | FAIL-SYS-TYPEPACK-03 | 回到 `north_star.yaml`、`_shared/type-pack-loading-contract.md` 与 `type-packs/网文/` |
| FIELD-SYS-OWNER-04 | Step 4 | 锁定该问题的 canonical owner | `canonical_owner`、`non_owner_layers_to_avoid` | FAIL-SYS-OWNER-04 | 回到真源分工表，禁止让下游冒充上游 |
| FIELD-SYS-TRACE-05 | Step 5 | 完成跨阶段 root-cause trace | `symptom`、`direct_cause`、`rule_source`、`meta_rule_source` | FAIL-SYS-TRACE-05 | 重新补全分层 trace，不能停在局部症状 |
| FIELD-SYS-CLOSURE-06 | Step 6 | 产出修复闭环与防回归结果 | `root_cause_location`、`immediate_fix`、`systemic_prevention_fix` | FAIL-SYS-CLOSURE-06 | 回到修复落点，优先改根级真源 |

## Completion Gate

- 已能明确把任一泛化 `story2026` 请求路由到唯一默认入口。
- 已能说明该请求应读的 canonical truth 与不该误读的非真源层。
- 已区分根级 `_shared`、`scripts/`、`templates/`、`type-packs/` 的共享职责。
- 已能说明当前项目的 `type_stack`、默认题材入口目录与 family craft 补读顺序。
- 已能指出 repo 级 `.codex/` 真源与项目级 `STATE.json.workflow_runtime` 内联工件链的分工。
- 出现跨阶段问题时，已给出完整 layered trace。
- 没有把根级入口写成“阶段细则大杂烩”。
