---
name: aigc-design
description: Use when the `4-Design` stage needs to route `1-主体清单 -> 2-主体设计 -> 3-面板设计` across `场景 / 角色 / 服装 / 道具`, while keeping runtime truth inside `projects/aigc/<项目名>/4-Design/`.
governance_tier: full
---

# aigc 4-Design

## 概述

`4-Design` 是 `aigc` 技能树承接 `3-Detail`、连接 `5-Image / 6-Video` 的阶段父 skill。

当前阶段的稳定执行链固定为：

`3-Detail -> 1-主体清单 -> 2-主体设计 -> 3-面板设计 -> 5-Image`

`4-Design` 父层不生产新的跨类目超级主稿；它只负责：

- 阶段入口判定
- tranche 路由
- 类目路由
- runtime 根路径与 shared contract 对齐
- 阶段级验收摘要回接到项目级 `validation-report.md`

## Parent Positioning

`4-Design` 拥有：

- `1-主体清单 / 2-主体设计 / 3-面板设计` 的顺序门
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
| tranche 路由 | `4-Design/SKILL.md` | 决定进入 `1-主体清单 / 2-主体设计 / 3-面板设计` 哪一段 |
| list-stage 总线 | `4-Design/1-主体清单/SKILL.md` | 统一承接 `3-Detail` 输出，生成 design-source 对象池 |
| design-stage 总线 | `4-Design/2-主体设计/SKILL.md` | 统一承接对象池，生成 machine-first 设计真源 |
| panel-stage 总线 | `4-Design/3-面板设计/SKILL.md` | 统一承接设计真源，生成 layout carrier |

硬规则：

1. `4-Design` 父层只路由真实存在的 tranche parent 与 leaf。
2. 默认 tranche 顺序固定为 `1-主体清单 -> 2-主体设计 -> 3-面板设计`。
3. 类目默认集合固定为 `场景 / 角色 / 服装 / 道具`。
4. 父层不得再生成 `4-Design` 阶段总稿。

## Stage Coverage Status

| 单元 | 当前状态 | 说明 |
| --- | --- | --- |
| `1-主体清单` | active | 四类 list leaf 与 shared contracts 可执行 |
| `2-主体设计` | active | 四类 design leaf 与 design-stage 验收可执行 |
| `3-面板设计` | active | 四类 panel leaf 与 panel-stage 验收可执行 |

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/3-Detail/SKILL.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-主体清单/SKILL.md`
- 强制读取：`.agents/skills/aigc/4-Design/2-主体设计/SKILL.md`
- 强制读取：`.agents/skills/aigc/4-Design/3-面板设计/SKILL.md`

硬规则：

1. `projects/aigc/<项目名>/4-Design/` 是 design 阶段唯一 runtime 根。
2. `1-主体清单` 是 `2-主体设计` 的默认上游。
3. `2-主体设计` 是 `3-面板设计` 的默认上游。
4. leaf 只在各自 domain runtime 下写 canonical 业务产物。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/_shared/project-runtime-layout.md`
6. `.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
7. 命中 `1-主体清单` 时，加载 `4-Design/1-主体清单/SKILL.md + CONTEXT.md`
8. 命中 `2-主体设计` 时，加载 `4-Design/2-主体设计/SKILL.md + CONTEXT.md`
9. 命中 `3-面板设计` 时，加载 `4-Design/3-面板设计/SKILL.md + CONTEXT.md`
10. `projects/aigc/<项目名>/team.yaml`（若存在）

## Route And Topology Contract (Mandatory)

### 默认模式

1. `single-tranche-single-domain`
2. `single-tranche-multi-domain`
3. `cross-tranche-handoff`

### 路由规则

1. 只缺对象池时，进入 `1-主体清单`。
2. design-source 已稳定、需生成设计真源时，进入 `2-主体设计`。
3. 设计真源已稳定、需生成 layout carrier 时，进入 `3-面板设计`。
4. 若用户只命中单一类目，本轮只调度该类目。
5. 若用户只命中单一 tranche，本轮只调度该 tranche，不伪造全链完成。

## Canonical Output Governance (Mandatory)

1. `4-Design` 阶段没有父层第二业务真源。
2. 阶段级 summary 只允许沉到项目级 `projects/aigc/<项目名>/validation-report.md`。
3. canonical 业务内容始终由具体 tranche leaf 写回。
4. 父层只负责阶段边界、coverage 与下一入口说明。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-4D-01` | 阶段边界 | 明确 `4-Design` 只拥有路由与边界，不拥有第二业务真源 | `S1` | 边界清晰度 | `FAIL-4D-01` |
| `FIELD-4D-02` | tranche 顺序 | 明确 `1-主体清单 -> 2-主体设计 -> 3-面板设计` 顺序 | `S2` | 路由稳定性 | `FAIL-4D-02` |
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
  - `.agents/skills/aigc/4-Design/1-主体清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-主体设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-面板设计/SKILL.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/SKILL.md`
  - `AGENTS.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

## Completion Criteria

- 已建立真实存在的 `4-Design` 阶段父级合同
- 已把 design 阶段路由收束为三个 tranche parent
- 已把四类类目挂入统一 stage parent
- 已避免父级造出第二业务真源
