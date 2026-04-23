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
- 若项目根 `team.yaml` 启用 `roles.supervision`，只允许把它用于本阶段前置 advisory；本轮 leaf canonical 首次落盘后的收尾不再由 `监制` 执行

## Parent Positioning

`4-Design` 拥有：

- `1-清单 / 2-设计 / 3-面板` 的顺序门
- `场景 / 角色 / 服装 / 道具` 四类类目路由
- `projects/aigc/<项目名>/4-Design/` 的路径真源对齐
- `3-Detail` 下游 design-source 消费总合同回链
- `team.yaml -> roles.supervision` 的前置 advisory 裁决

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
| advisory runtime | `4-Design/SKILL.md` + shared `council-runtime` | 当前轮如需前置顾问，只在落盘前读取 `team.yaml` 的 `roles.supervision`，把 advisory 作为路由与创作约束输入 |

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

硬规则：

1. `projects/aigc/<项目名>/4-Design/` 是 design 阶段唯一 runtime 根。
2. `1-清单` 是 `2-设计` 的默认上游。
3. `2-设计` 当前已具备 tranche parent 与 `场景 / 角色 / 道具` leaf；未迁回的 sibling 仍不得伪装为 active。
4. `2-设计` 的正式完成必须包含 `full_generation_prompt` 与同目录同 stem 单主体图片。
5. `3-面板` 当前已具备 tranche parent 与 `场景 / 角色 / 道具` leaf；未迁回的 sibling 仍不得伪装为 active。
6. leaf 只在各自 domain runtime 下写 canonical 业务产物。
7. 若 `team.yaml` 启用 `roles.supervision`，它在 `4-Design` 中只拥有前置 advisory 权；首次落盘后的收尾 patch 必须回到审计/验收层，不再由 `监制` 执行。

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
4. 父层只负责阶段边界、coverage、前置 advisory 边界与下一入口说明。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界 | 明确 `4-Design` 只拥有路由与边界，不拥有第二业务真源 | `S1` | 边界清晰度 | `FAIL-4D-01` |
| `FIELD-4D-02` | tranche 顺序 | 明确 `1-清单 -> 2-设计 -> 3-面板` 顺序 | `S2` | 路由稳定性 | `FAIL-4D-02` |
| `FIELD-4D-03` | 类目调度 | 明确四类类目的 selective dispatch | `S3` | 调度准确性 | `FAIL-4D-03` |
| `FIELD-4D-04` | runtime 对齐 | 明确 `projects/aigc/<项目名>/4-Design/` 是唯一 stage runtime 根 | `S4` | 真源一致性 | `FAIL-4D-04` |
| `FIELD-4D-05` | handoff | 明确 `5-Image / 6-Video / review` 的下一入口口径 | `S5` | 闭环完整性 | `FAIL-4D-05` |
| `FIELD-4D-06` | advisory boundary | `team.yaml` 的 `roles.supervision` 在本阶段只作为前置 advisory，可追踪且不越权到落盘后 refine | `S6` | 角色边界正确性 | `FAIL-4D-06` |
| `FIELD-4D-07` | final closure | `validation-report.md` 已汇流当前轮 leaf canonical 的阶段 summary、审计占位说明与下一入口 | `S7` | 阶段闭环完整性 | `FAIL-4D-07` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-4D-01` | 当前是不是 design 阶段父层问题 | 锁定阶段边界 | 父层越权写业务主稿 |
| `S2` | `FIELD-4D-02` | 当前该进哪个 tranche | 写 tranche route | 顺序漂移 |
| `S3` | `FIELD-4D-03` | 当前命中哪些类目 | 写 domain route | 未命中类目被补空 |
| `S4` | `FIELD-4D-04` | 路径是否回到 design runtime 根 | 回指 shared runtime layout | 叶子私造路径 |
| `S5` | `FIELD-4D-05` | 下游入口是什么 | 写 handoff | 只能停在阶段中间态 |
| `S6` | `FIELD-4D-06` | 本轮若命中 `team.yaml.roles.supervision`，是否只把它用于前置 advisory，而没有越权到落盘后 refine | 记录 advisory 来源、是否读取、是否采纳，以及 post-write 收尾不归 `监制` | 把 `roles.supervision` 扩写成 closeout owner，或把派生 PNG 当成监制补丁对象 |
| `S7` | `FIELD-4D-07` | 当前轮是否已完成阶段 summary、审计占位说明与下一入口 | 写 `validation-report.md` 的 closure、audit note 与下一入口 | handoff 不唯一，或仍要求汇流 `监制强化` 结果 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界明确，不造第二真源 | `FAIL-4D-01` | `S1` |
| `FIELD-4D-02` | tranche 顺序与命中规则明确 | `FAIL-4D-02` | `S2` |
| `FIELD-4D-03` | 类目 selective dispatch 明确 | `FAIL-4D-03` | `S3` |
| `FIELD-4D-04` | runtime 根与 shared contract 对齐 | `FAIL-4D-04` | `S4` |
| `FIELD-4D-05` | handoff 与阶段闭环明确 | `FAIL-4D-05` | `S5` |
| `FIELD-4D-06` | `roles.supervision` 只作为前置 advisory，未越权到落盘后收尾 | `FAIL-4D-06` | `S6` |
| `FIELD-4D-07` | `validation-report` 已汇流阶段 summary、审计占位说明与最终下一入口 | `FAIL-4D-07` | `S7` |

## Root-Cause Execution Contract (Mandatory)

当 `4-Design` 出现以下问题时，必须先修源层而不是补某个 leaf：

- 根技能声称 `4-Design` 已建合同，但仓内没有阶段父级
- leaf preload 指向不存在的 stage/substage parent
- tranche 名称、runtime 名称与路由口径再次漂移
- 父层开始发明 stage-level 第二业务真源
- 项目根 `team.yaml` 已启用 `roles.supervision`，但父层没有在落盘前读取其 advisory 约束
- 把 `roles.supervision` 继续写成落盘后收尾 owner，导致顾问机制与审计机制混层
- 首次落盘后的审计收尾继续把派生 PNG、request sidecar 或 `_manifest.json` 当成“监制补丁”目标，导致阶段边界失真

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
- 若 `projects/aigc/<项目名>/team.yaml` 启用 `roles.supervision` 且命中 `4-Design`，已在本轮真正写稿前消费其 advisory 约束；首次落盘后的收尾改写已从 `监制` 名下收回，并在 `validation-report.md` 中写明该边界

## 输出后审计边界（Mandatory）

1. `4-Design` 首次落盘后的收尾不再由 `roles.supervision` 执行，也不再在本阶段父层内触发 `监制强化`。
2. 若当前轮需要记录收尾问题，只能写入 `projects/aigc/<项目名>/4-Design/validation-report.md` 的阶段 summary / audit note，不得借 `监制` 名义对既有 canonical 做额外 closeout patch。
3. `roles.supervision.source_skill_refs` 继续只作领域提示，不得被重新升级为 post-write reviewer 或 runtime 授权字段。
4. `5-Image / 6-Video` 的 `review gate` 仍保留现状，但它的后续改造不在本轮 `4-Design` 父层合同内展开。
