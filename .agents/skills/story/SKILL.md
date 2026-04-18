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

它只统一回答三件事：

1. 当前诉求应该路由到哪个阶段 skill。
2. 哪一层才是这类问题的 canonical truth。
3. 根级 `references/`、`scripts/`、`templates/` 分别承担什么共享职责。

补充治理约束：

- repo 级复杂任务治理真源固定回指 `.codex/schemas/`、`.codex/runbooks/`、`.codex/registry/`。
- 书项目级 tracked run 的 shadow 工件固定落在 `<project_root>/.webnovel/tasks/<run_id>/`。
- 第一阶段不拿 shadow 工件替代 `.webnovel/workflow_state.json / execution_state.json / task_log.jsonl`，只把它们作为三省证据层增强。

硬边界：

- 根级 `story/SKILL.md` 负责跨阶段拓扑、共享载体边界、总路由和根因追溯总则。
- 各阶段目录下的 `SKILL.md` 负责本阶段的严格执行合同。
- 根级 `CONTEXT.md` 只沉淀跨阶段经验，不吞并阶段私有故障模式。

## When to Use

- 用户只说“用 story2026 做这件事”，但还没有明确该进哪一个阶段。
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
- `5-Loopback` 只在 `4-Validation = PASS` 后拥有 validated truth writeback 权。

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
  - 它不是主链 stage，也不是 tracked satellite workflow；若后续恢复正式技能，必须先回到 `references/command-naming-contract.md` 补登记。

## Root Truth Ownership Contract

| 层 | 拥有的真源 | 不拥有的真源 |
| --- | --- | --- |
| 根级 `story2026` | 跨阶段拓扑、总路由、共享载体边界、默认加载顺序 | 各阶段内部执行细则、局部 reference 专业判断 |
| `0-Init` | 立项合同、`north_star_contract`、初始 seeds | 对象真源、规划真源、validated actualization |
| `1-Cards` | 角色/场景/物品等对象真源 | 章节编排真源、章节审查判断 |
| `2-Planning` | `Planning/8-全息地图.json` 为核心的规划真源 | 对象当前态、validated actualization |
| `3-Drafting` | 章节草稿、润色闭环、章节级写作执行包 | 评估判断权、validated truth writeback |
| `4-Validation` | 隔离评估团队与 `validation_status` 判定 | 报告持久化、actualization 写回 |
| `review` | 审查报告、评分落库、状态持久化 | `validation_status` 判定、actualization 写回 |
| `5-Loopback` | validated actualization 与 truth writeback | 未通过验证的修改写回 |
| `query / resume` | 查询、恢复 | 主链 canonical truth 判定权 |

## Shared Carrier Contract

### 根级 `references/`

根级 `references/` 只承载跨阶段共享合同，不承载单一阶段私有技巧。

默认先读：

- `references/README.md`

仅在问题命中时，再按需读取：

- `command-naming-contract.md`
- `checker-output-schema.md`
- `context-contract-v2.md`
- `entity-management-spec.md`
- `loopback-actualization-spec.md`
- `project-memory-schema.md`
- `validation-fact-pack-spec.md`
- `shared/*`

### 根级 `scripts/`

根级 `scripts/` 是 story2026 的共享脚本入口层，负责：

- canonical path helper
- workflow / state / status 管理
- shared CLI entrypoint
- 多阶段共用的数据访问与校验
- shadow governance task artifact 写入与引用回填

规则：

- 若同类路径、状态或 truth 读取逻辑会被两个及以上阶段复用，应优先提升到根级 `scripts/` 统一维护。
- 阶段 skill 不应各自复制一套共享 helper。

## Governance Artifact Chain

repo 级 authoritative source：

- `.codex/schemas/`
- `.codex/runbooks/`
- `.codex/registry/`

书项目级 shadow artifact chain：

- `<project_root>/.webnovel/tasks/<run_id>/mandate.yaml`
- `<project_root>/.webnovel/tasks/<run_id>/mission_brief.yaml`
- `<project_root>/.webnovel/tasks/<run_id>/route_plan.yaml`
- `<project_root>/.webnovel/tasks/<run_id>/preflight_verdict.yaml`
- `<project_root>/.webnovel/tasks/<run_id>/artifact_manifest.json`
- `<project_root>/.webnovel/tasks/<run_id>/validation_report.md`
- `<project_root>/.webnovel/tasks/<run_id>/learning_record.md`

解释：

- tracked workflow 当前通过根级 `scripts/workflow_manager.py + task_artifacts.py` 旁路写入这些工件。
- 阶段技能必须承认这些工件是 review / trace / closure 的共享证据层。
- 在 cutover 前，`.webnovel/workflow_state.json / execution_state.json / task_log.jsonl` 仍是运行态主链。

### 根级 `templates/`

根级 `templates/` 只放跨阶段或跨模块共享模板、共享题材资产与统一 schema 载体。

规则：

- 阶段私有模板留在对应阶段目录。
- 一旦模板被多个阶段共享消费，应优先评估是否提升为根级 canonical carrier。

## Routing Contract

| 用户诉求 / 问题形状 | 默认入口 |
| --- | --- |
| 新建项目、确定创作立项、初始化问卷/顾问团 | `0-Init` |
| 角色卡/场景卡/物品卡生成、回写、覆盖率修复 | `1-Cards` |
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
3. 若问题涉及共享合同，先读根级 `references/README.md`；若问题命中命令、skill id、workflow 命名漂移，再优先补读 `command-naming-contract.md`。
4. 路由到目标阶段的 `SKILL.md`。
5. 读取目标阶段 `CONTEXT.md`。
6. 若阶段采用 governed `references/`，固定顺序为：
   - `module-spec.md`
   - 同目录 `CONTEXT.md`
   - 对应模板 / 脚本

## Root-Cause Execution Contract (Mandatory)

当 `story2026` 出现跨阶段路由错误、真源分工混乱、共享 reference 漂移、共享脚本路径失配、根入口缺失或总线合同断裂时，必须按以下链路上溯：

1. `Symptom / Failure`
   - 明确是发现失败、路由错误、共享层漂移、还是阶段真源混淆。
2. `Direct Technical Cause`
   - 确认是根入口缺文件、总路由未声明、共享 carrier 边界不清、脚本 helper 缺统一入口，还是下游误把共享文档当私有文档。
3. `Rule Source`
   - 优先检查当前根级 `SKILL.md`、根级 `CONTEXT.md`、根级 `references/README.md` 与相关共享脚本入口。
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
  - 总路由、主链拓扑、卫星关系、共享 carrier 边界、默认加载顺序、跨阶段 root-cause 合同。
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
| FIELD-SYS-CARRIER-02 | Step 2 | 判断应读取哪些根级共享 carrier | `shared_refs_to_load`、`shared_scripts_needed` | FAIL-SYS-CARRIER-02 | 回到根级 `references/README.md` 与共享层边界合同 |
| FIELD-SYS-OWNER-03 | Step 3 | 锁定该问题的 canonical owner | `canonical_owner`、`non_owner_layers_to_avoid` | FAIL-SYS-OWNER-03 | 回到真源分工表，禁止让下游冒充上游 |
| FIELD-SYS-TRACE-04 | Step 4 | 完成跨阶段 root-cause trace | `symptom`、`direct_cause`、`rule_source`、`meta_rule_source` | FAIL-SYS-TRACE-04 | 重新补全分层 trace，不能停在局部症状 |
| FIELD-SYS-CLOSURE-05 | Step 5 | 产出修复闭环与防回归结果 | `root_cause_location`、`immediate_fix`、`systemic_prevention_fix` | FAIL-SYS-CLOSURE-05 | 回到修复落点，优先改根级真源 |

## Completion Gate

- 已能明确把任一泛化 `story2026` 请求路由到唯一默认入口。
- 已能说明该请求应读的 canonical truth 与不该误读的非真源层。
- 已区分根级 `references/`、`scripts/`、`templates/` 的共享职责。
- 已能指出 repo 级 `.codex/` 真源与项目级 `.webnovel/tasks/<run_id>/` shadow 工件链的分工。
- 出现跨阶段问题时，已给出完整 layered trace。
- 没有把根级入口写成“阶段细则大杂烩”。
