---
name: aigc-design
description: Use when the `4-Design` stage needs to route the current design tranche under `projects/aigc/<项目名>/4-Design/`, with `1-清单/{场景,角色,道具}` and `2-设计/{场景,角色,道具}` already re-landed while the rest of the tranche tree remains in bootstrap-compatible migration.
governance_tier: full
---

# aigc 4-Design

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

## Parent Positioning

`4-Design` 拥有：

- `1-清单 / 2-设计 / 3-面板` 的顺序门
- `场景 / 角色 / 服装 / 道具` 四类类目路由
- `projects/aigc/<项目名>/4-Design/` 的路径真源对齐
- `3-Detail` 下游 design-source 消费总合同回链

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

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/_shared/project-runtime-layout.md`
6. `.agents/skills/aigc/4-Design/1-清单/_shared/detail-output-consumption-contract.md`
7. 命中 `1-清单` 时，加载 `4-Design/1-清单/SKILL.md + CONTEXT.md`
8. 命中 `2-设计` 时，加载 `4-Design/2-设计/SKILL.md + CONTEXT.md`
9. 命中 `2-设计` 或 `3-面板` 时，加载 `4-Design/2-设计/_shared/design-output-contract.md`
10. 命中 `3-面板` 时，加载 `4-Design/3-面板/SKILL.md + CONTEXT.md`；当前仅 `场景 / 角色 / 道具` leaf 可继续下钻
11. `projects/aigc/<项目名>/team.yaml`（若存在）

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
4. 父层只负责阶段边界、coverage 与下一入口说明。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界 | 明确 `4-Design` 只拥有路由与边界，不拥有第二业务真源 | `S1` | 边界清晰度 | `FAIL-4D-01` |
| `FIELD-4D-02` | tranche 顺序 | 明确 `1-清单 -> 2-设计 -> 3-面板` 顺序 | `S2` | 路由稳定性 | `FAIL-4D-02` |
| `FIELD-4D-03` | 类目调度 | 明确四类类目的 selective dispatch | `S3` | 调度准确性 | `FAIL-4D-03` |
| `FIELD-4D-04` | runtime 对齐 | 明确 `projects/aigc/<项目名>/4-Design/` 是唯一 stage runtime 根 | `S4` | 真源一致性 | `FAIL-4D-04` |
| `FIELD-4D-05` | handoff | 明确 `5-Image / 6-Video / review` 的下一入口口径 | `S5` | 闭环完整性 | `FAIL-4D-05` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-4D-01` | 当前是不是 design 阶段父层问题 | 锁定阶段边界 | 父层越权写业务主稿 |
| `S2` | `FIELD-4D-02` | 当前该进哪个 tranche | 写 tranche route | 顺序漂移 |
| `S3` | `FIELD-4D-03` | 当前命中哪些类目 | 写 domain route | 未命中类目被补空 |
| `S4` | `FIELD-4D-04` | 路径是否回到 design runtime 根 | 回指 shared runtime layout | 叶子私造路径 |
| `S5` | `FIELD-4D-05` | 下游入口是什么 | 写 handoff | 只能停在阶段中间态 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界明确，不造第二真源 | `FAIL-4D-01` | `S1` |
| `FIELD-4D-02` | tranche 顺序与命中规则明确 | `FAIL-4D-02` | `S2` |
| `FIELD-4D-03` | 类目 selective dispatch 明确 | `FAIL-4D-03` | `S3` |
| `FIELD-4D-04` | runtime 根与 shared contract 对齐 | `FAIL-4D-04` | `S4` |
| `FIELD-4D-05` | handoff 与阶段闭环明确 | `FAIL-4D-05` | `S5` |

## Root-Cause Execution Contract (Mandatory)

当 `4-Design` 出现以下问题时，必须先修源层而不是补某个 leaf：

- 根技能声称 `4-Design` 已建合同，但仓内没有阶段父级
- leaf preload 指向不存在的 stage/substage parent
- tranche 名称、runtime 名称与路由口径再次漂移
- 父层开始发明 stage-level 第二业务真源

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/SKILL.md`
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
