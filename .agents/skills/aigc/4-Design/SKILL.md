---
name: aigc-design
description: Use when the `4-Design` stage needs to route the current design tranche under `projects/aigc/<项目名>/4-Design/`, with `1-清单/{场景,角色,道具}` and `2-设计/{场景,角色,道具}` already re-landed while the rest of the tranche tree remains in bootstrap-compatible migration.
governance_tier: full
---

# aigc 4-Design

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`4-Design` 是 `aigc` 技能树承接 `3-Detail`、连接 `5-Image / 6-Video` 的阶段父 skill。

当前阶段的 source-layer 处于 `bootstrap_compat` 迁移窗口。

本轮已稳定落地的链路是：

`3-Detail -> 1-清单/{场景,角色,道具} -> 2-设计/{场景,角色,道具} + 单主体自动图 -> 3-面板/{场景,角色,道具}`

更完整的阶段目标仍然是：

`3-Detail -> 1-清单 -> 2-设计 -> 3-面板 -> 5-Image`

`4-Design` 父层不生产新的跨类目超级主稿；它只负责：

- 阶段入口判定
- tranche 路由
- 类目路由
- runtime 根路径与 shared contract 对齐
- 阶段级验收摘要回接到 `projects/aigc/<项目名>/4-Design/validation-report.md`
- 在项目根 `team.yaml` 启用 `roles.supervision` 时，对本轮命中的 leaf canonical 触发一次阶段末端 `监制强化`

## Parent Positioning

`4-Design` 拥有：

- `1-清单 / 2-设计 / 3-面板` 的顺序门
- `场景 / 角色 / 服装 / 道具` 四类类目路由
- `projects/aigc/<项目名>/4-Design/` 的路径真源对齐
- `3-Detail` 下游 design-source 消费总合同回链
- `team.yaml -> roles.supervision -> stage-end refine` 的 shared runtime 裁决

`4-Design` 不拥有：

- 直接写某个类目的 canonical 内容产物
- 发明 stage-level 第二业务真源
- 越权改写 `3-Detail/第N集.json`

## Internal Capability Fusion Contract (Mandatory)

| 能力面 | 当前 owner | 说明 |
| --- | --- | --- |
| 阶段入口判定 | `4-Design/SKILL.md` | 决定本轮是否进入 design 阶段 |
| tranche 路由 | `4-Design/SKILL.md` | 决定进入 `1-清单 / 2-设计 / 3-面板` 哪一段 |
| list-stage 总线 | `4-Design/1-清单/SKILL.md` | 当前已落地，用来统一承接 `3-Detail` 输出，并稳定 `场景 / 角色 / 道具` 清单真源 |
| design-stage 总线 | `4-Design/2-设计/SKILL.md` | 当前已重建 tranche parent，`场景 / 角色 / 道具` leaf 已 active，并通过共享输出合同自动生成同目录同名单主体图；其余 sibling 仍待迁移 |
| panel-stage 总线 | `4-Design/3-面板/SKILL.md` | 当前已重建 tranche parent，`场景 / 角色 / 道具` leaf 已 active，可消费 `2-设计` prompt 与同 stem 单主体图；`服装` leaf 仍待迁移 |
| supervision runtime | `4-Design/SKILL.md` + shared `council-runtime` | 当前轮命中 leaf 的 canonical 首次落盘后，按 `team.yaml` 解析 `监制` reviewer、模式与 subagents/fallback，并把 findings 汇流到既有真源 |

硬规则：

1. `4-Design` 父层只路由真实存在的 tranche parent 与 leaf。
2. 默认 tranche 顺序固定为 `1-清单 -> 2-设计 -> 3-面板`。
3. 类目默认集合固定为 `场景 / 角色 / 服装 / 道具`。
4. 父层不得再生成 `4-Design` 阶段总稿。

## Stage Coverage Status

| 单元 | 当前状态 | 说明 |
| --- | --- | --- |
| `1-清单` | partial-active | 父层与 `场景 / 角色 / 道具` leaf 已迁回新路径；其余 sibling 仍待迁移 |
| `2-设计` | partial-active | tranche parent 与 `场景 / 角色 / 道具` leaf 已迁回；其余 sibling 仍待迁移 |
| `3-面板` | partial-active | tranche parent 已重建，`场景 / 角色 / 道具` leaf 已迁回并默认桥接 nano-banana/general；其余 sibling 仍待迁移 |

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- 强制读取：`.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- 强制读取：`.agents/skills/aigc/3-Detail/SKILL.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-清单/_shared/detail-output-consumption-contract.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-清单/SKILL.md`
- 强制读取：`.agents/skills/aigc/4-Design/2-设计/SKILL.md`
- 条件读取：`.agents/skills/aigc/4-Design/2-设计/_shared/design-output-contract.md`（命中 design 或 panel tranche 时）
- 条件读取：`.agents/skills/aigc/4-Design/3-面板/SKILL.md`（命中 panel tranche 时）
- 条件读取：`.codex/commands/master-check-team.md`（命中阶段末 `监制强化` 时）
- 条件读取：`.codex/commands/master-check.md`（命中阶段末 `监制强化` 时）

硬规则：

1. `projects/aigc/<项目名>/4-Design/` 是 design 阶段唯一 runtime 根。
2. `1-清单` 是 `2-设计` 的默认上游。
3. `2-设计` 当前已具备 tranche parent 与 `场景 / 角色 / 道具` leaf；未迁回的 sibling 仍不得伪装为 active。
4. `2-设计` 的正式完成必须包含 `full_generation_prompt` 与同目录同 stem 单主体图片。
5. `3-面板` 当前已具备 tranche parent 与 `场景 / 角色 / 道具` leaf；未迁回的 sibling 仍不得伪装为 active。
6. leaf 只在各自 domain runtime 下写 canonical 业务产物。
7. 若 `team.yaml` 启用 `roles.supervision`，阶段末会审只能围绕本轮命中的 leaf canonical 与 `validation-report.md` 做最小必要 patch；不得生成新的“监制稿”“评审稿”或跨类目总稿。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/_shared/project-runtime-layout.md`
6. `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
7. `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
8. `.agents/skills/aigc/4-Design/1-清单/_shared/detail-output-consumption-contract.md`
9. 命中 `1-清单` 时，加载 `4-Design/1-清单/SKILL.md + CONTEXT.md`
10. 命中 `2-设计` 时，加载 `4-Design/2-设计/SKILL.md + CONTEXT.md`
11. 命中 `2-设计` 或 `3-面板` 时，加载 `4-Design/2-设计/_shared/design-output-contract.md`
12. 命中 `3-面板` 时，加载 `4-Design/3-面板/SKILL.md + CONTEXT.md`；当前仅 `场景 / 角色 / 道具` leaf 可继续下钻
13. `.codex/commands/master-check-team.md`（命中阶段末 `监制强化` 时）
14. `.codex/commands/master-check.md`（命中阶段末 `监制强化` 时）
15. `projects/aigc/<项目名>/team.yaml`（若存在）

## Route And Topology Contract (Mandatory)

### 默认模式

1. `single-tranche-single-domain`
2. `single-tranche-multi-domain`
3. `cross-tranche-handoff`

### 路由规则

1. 只缺对象池时，进入 `1-清单`。
2. design-source 已稳定且命中 `场景 / 角色 / 道具` 域时，进入 `2-设计/<域>`。
3. 设计真源、`full_generation_prompt` 与同 stem 单主体图已稳定且命中 `场景 / 角色 / 道具` 面板时，进入对应 `3-面板/<域>`；命中其他未迁回 sibling 时报告 pending-migration。
4. 若用户只命中单一类目，本轮只调度该类目。
5. 若用户只命中单一 tranche，本轮只调度该 tranche，不伪造全链完成。

## Canonical Output Governance (Mandatory)

1. `4-Design` 阶段没有父层第二业务真源。
2. 阶段级 summary 只允许沉到 `projects/aigc/<项目名>/4-Design/validation-report.md`。
3. canonical 业务内容始终由具体 tranche leaf 写回。
4. 父层只负责阶段边界、coverage、阶段末监制强化与下一入口说明。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界 | 明确 `4-Design` 只拥有路由与边界，不拥有第二业务真源 | `S1` | 边界清晰度 | `FAIL-4D-01` |
| `FIELD-4D-02` | tranche 顺序 | 明确 `1-清单 -> 2-设计 -> 3-面板` 顺序 | `S2` | 路由稳定性 | `FAIL-4D-02` |
| `FIELD-4D-03` | 类目调度 | 明确四类类目的 selective dispatch | `S3` | 调度准确性 | `FAIL-4D-03` |
| `FIELD-4D-04` | runtime 对齐 | 明确 `projects/aigc/<项目名>/4-Design/` 是唯一 stage runtime 根 | `S4` | 真源一致性 | `FAIL-4D-04` |
| `FIELD-4D-05` | handoff | 明确 `5-Image / 6-Video / review` 的下一入口口径 | `S5` | 闭环完整性 | `FAIL-4D-05` |
| `FIELD-4D-06` | supervision runtime | `team.yaml` 的 `roles.supervision`、reviewer 来源、模式与是否真实启用 subagents 可追踪 | `S6` | stage-end refine 正确性 | `FAIL-4D-06` |
| `FIELD-4D-07` | final closure | `validation-report.md` 已汇流当前轮 leaf canonical + 监制强化结果 + 下一入口 | `S7` | 阶段闭环完整性 | `FAIL-4D-07` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-4D-01` | 当前是不是 design 阶段父层问题 | 锁定阶段边界 | 父层越权写业务主稿 |
| `S2` | `FIELD-4D-02` | 当前该进哪个 tranche | 写 tranche route | 顺序漂移 |
| `S3` | `FIELD-4D-03` | 当前命中哪些类目 | 写 domain route | 未命中类目被补空 |
| `S4` | `FIELD-4D-04` | 路径是否回到 design runtime 根 | 回指 shared runtime layout | 叶子私造路径 |
| `S5` | `FIELD-4D-05` | 下游入口是什么 | 写 handoff | 只能停在阶段中间态 |
| `S6` | `FIELD-4D-06` | 本轮是否要按 `team.yaml` 启用监制 subagents，以及评审哪些 leaf canonical | 解析 `roles.supervision`、review target bundle、mode、subagents/fallback，并做最小必要 refine | `team.yaml` 已启用却静默跳过，或把派生 PNG 当主评审对象 |
| `S7` | `FIELD-4D-07` | 当前轮是否已完成阶段 summary 与监制强化汇流 | 写 `validation-report.md` 的 closure、patched targets 与下一入口 | 监制强化结果未汇流，或 handoff 不唯一 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界明确，不造第二真源 | `FAIL-4D-01` | `S1` |
| `FIELD-4D-02` | tranche 顺序与命中规则明确 | `FAIL-4D-02` | `S2` |
| `FIELD-4D-03` | 类目 selective dispatch 明确 | `FAIL-4D-03` | `S3` |
| `FIELD-4D-04` | runtime 根与 shared contract 对齐 | `FAIL-4D-04` | `S4` |
| `FIELD-4D-05` | handoff 与阶段闭环明确 | `FAIL-4D-05` | `S5` |
| `FIELD-4D-06` | supervision runtime / reviewer / mode / used_subagents 可追踪 | `FAIL-4D-06` | `S6` |
| `FIELD-4D-07` | validation-report 已汇流监制强化结果与最终下一入口 | `FAIL-4D-07` | `S7` |

## Root-Cause Execution Contract (Mandatory)

当 `4-Design` 出现以下问题时，必须先修源层而不是补某个 leaf：

- 根技能声称 `4-Design` 已建合同，但仓内没有阶段父级
- leaf preload 指向不存在的 stage/substage parent
- tranche 名称、runtime 名称与路由口径再次漂移
- 父层开始发明 stage-level 第二业务真源
- 项目根 `team.yaml` 已启用 `roles.supervision`，但阶段输出后没有读取其配置、没有解析 reviewer、或没有按规则触发监制强化
- stage-end 会审直接把派生 PNG、request sidecar 或 `_manifest.json` 当业务主评审对象，导致 reviewer 越过 canonical 文本/JSON 真源
- `runtime_policy.use_subagents_by_default == true` 且 reviewer 已稳定命中，但父层仍静默跳过真实 subagents

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
  - `.agents/skills/aigc/4-Design/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-面板/角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-面板/道具/SKILL.md`
  - `.codex/commands/master-check-team.md`
  - `.codex/commands/master-check.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/SKILL.md`
  - `AGENTS.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

## Completion Criteria

- 已建立真实存在的 `4-Design` 阶段父级合同
- 已把 `1-清单/{场景,角色,道具}` 迁回新路径并与 `3-Detail` 对齐
- 已把 `2-设计/{场景,角色,道具}` 接回 source-layer 总线，并要求每个主体产出含全局风格前缀的 `full_generation_prompt` 与同目录同名图片；其余 sibling 仍显式标记待迁移
- 已把 `3-面板/{场景,角色,道具}` 接回 source-layer 总线并默认桥接 `nano-banana/general`，可消费 `2-设计` 同 stem 单主体图作为批量 SMART 参照；其余 sibling 仍显式标记待迁移
- 已避免父级造出第二业务真源
- 若 `projects/aigc/<项目名>/team.yaml` 启用 `roles.supervision` 且命中 `4-Design`，已在本轮命中的 leaf canonical 首次落盘后完成一次阶段末 `监制强化`，并在 `validation-report.md` 中写明 reviewer 来源、模式、是否启用真实 subagents、patched targets 或 skip/fallback 原因

## Subagents 监制强化（Mandatory）

`4-Design` 的监制强化不是围绕一个阶段总稿，而是围绕“本轮命中的 leaf canonical + 阶段级 summary”。

### 触发门

只有同时满足以下条件，才进入真实 `监制强化`：

1. `projects/aigc/<项目名>/team.yaml` 存在。
2. `team.yaml.enabled == true`，或用户显式要求对当前轮执行 `subagents` 监制强化。
3. 本轮至少已有一个命中的 leaf canonical 首次落盘。
4. `4-Design` 的 stage-end refine 允许进入：要么项目显式让 `roles.supervision` 覆盖 `4-Design`，要么共享 `team.template.yaml` 把 `4-Design` 归于 `supervision`，要么当前轮为人工 override。

若任一条件不满足：

- 在 `projects/aigc/<项目名>/4-Design/validation-report.md` 写明 `skip_reason`
- 直接结束到 `S7`

### Review Target Bundle

`4-Design` 的 stage-end review target bundle 固定为：

1. 主目标：本轮命中的 leaf canonical truth
   - `1-清单`：各域的 catalog / research / bridge JSON
   - `2-设计`：`scene_design.json`、`character_design.json`、逐道具 canonical Markdown
   - `3-面板`：`*-Panel-layout.json`
2. 次目标：`projects/aigc/<项目名>/4-Design/validation-report.md`
3. 证据目标：当前轮 `_manifest.json`、同 stem 单主体图、request sidecar、派生 PNG

硬规则：

1. `_manifest.json`、request sidecar、派生 PNG 只作证据，不作为默认 patch 目标。
2. 监制强化默认只改文字/JSON canonical 与阶段级 `validation-report.md`。
3. 不得因为本轮涉及多个 leaf，就发明新的 `4-Design` 阶段总稿。

### Reviewer 解析顺序

按以下顺序抽取 reviewer，规则对齐 `master-check-team`：

1. `roles.supervision.members`
2. 若 `roles.review.operates_on_final_stage_of` 显式包含 `4-Design`，并入 `roles.review.members`
3. `team_setup.shared_agents`
4. `roles.supervision.source_skill_refs`
5. 基于 `roles.supervision.focus + target_type` 的安全补选

处理规则：

- 最终 reviewer 真源必须落在 `.agents/skills/team/**/SKILL.md`。
- `roles.review.operates_on_final_stage_of` 若显式覆盖 `4-Design`，只表示最终验收 gate 的 reviewer 来源可并入当前 roster，不取代 stage-end refine 的进入裁定。
- `roles.supervision.source_skill_refs` 若指向 `.agents/skills/aigc/**/SKILL.md`，只可作为领域提示，不得直接充当 reviewer，也不得充当 runtime 授权字段。
- 当显式 reviewer 不足时，才允许补选 `1-2` 个 reviewer。
- `4-Design` 的默认补选优先级：
  - 设计组 1 位
  - 若目标偏叙事/角色可拍性，补导演组或编剧组 1 位
  - 若目标偏画面组织与布局，补摄影组 1 位

### 模式裁决

1. reviewer 为 1 个 -> `single-reviewer`
2. reviewer 为 `2-4` 个且判断相对独立 -> `parallel-council`
3. 需要先修 design-source 再看 layout 的链式问题 -> `serial-refine`
4. `independent-only` 仅在用户明确要求“只看法不改稿”时启用

### Subagent Dispatch Gate

当满足以下条件时，必须真实启用 subagents：

1. `runtime_policy.use_subagents_by_default == true`
2. 已稳定解析出 `1-4` 个 reviewer
3. 当前环境未被更高优先级策略阻断
4. 用户未显式禁止 subagents

降级条件：

- 当前环境无法真实使用 subagents
- 更高优先级策略明确阻断
- 用户显式要求不要启用 subagents

降级时必须在 `validation-report.md` 中写明：

- `reviewer_source`
- `mode`
- `used_subagents: false`
- `fallback_reason`

### Optimization Boundary

`4-Design` 父层的监制强化不得越权：

1. 若 findings 命中 `1-清单` 的 catalog / research / bridge 结构
   - 回流对应 `1-清单/<域>` leaf
2. 若 findings 命中 `2-设计` 的 canonical design truth / prompt 结构
   - 回流对应 `2-设计/<域>` leaf
3. 若 findings 命中 `3-面板` 的 layout JSON
   - 回流对应 `3-面板/<域>` leaf
4. 若 findings 只涉及阶段级 dispatch、coverage、patched targets、reviewer provenance 或 handoff
   - 允许父层直接 patch `validation-report.md`
5. 普通监制收尾不得借机 patch `SKILL.md`、`CONTEXT.md`、commands、runbook 或 team 真源；源层治理问题必须单列为后续 task

### `validation-report.md` 最低记录槽位

命中 `监制强化` 时，`projects/aigc/<项目名>/4-Design/validation-report.md` 至少应包含：

- `## 监制强化`
- `team_yaml`
- `reviewer_source`
- `reviewers`
- `mode`
- `used_subagents`
- `patched_targets`
- `key_findings`
- `synthesis`
- `fallback_or_skip_reason`（若存在）
