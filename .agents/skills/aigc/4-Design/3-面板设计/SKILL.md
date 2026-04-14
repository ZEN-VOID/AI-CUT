---
name: aigc-design-object-panel
description: Use when the `4-Design/3-面板设计` stage needs to route `场景 / 角色 / 服装 / 道具` panel skills, inherit design carriers from `2-主体设计`, and aggregate panel-stage validation under `projects/aigc/<项目名>/4-Design/`.
governance_tier: full
---

# aigc 4-Design / 3-面板设计

## 概述

`3-面板设计` 是 `4-Design` 阶段承接 `2-主体设计`、连接 `5-Image` 与人工审阅的阶段父 skill。

当前 active 子技能固定为：

1. `场景`
2. `角色`
3. `服装`
4. `道具`

父层拥有：

- `design carrier -> panel packet` 的阶段入口判定
- 多域 panel build 的 selective dispatch
- 各域模板与输出根是否稳定的阶段级检查
- `projects/aigc/<项目名>/4-Design/validation-report.md` 的 panel-stage 验收摘要
- 指向 `5-Image / review` 的统一 handoff 说明

父层不拥有：

- 直接写某一域 layout packet 内容
- 改写 `2-主体设计` 的 design master 或 prompt sidecar
- 代替 leaf 重建模板结构
- 自动触发图片或视频生成

## Stage Coverage Status

| 单元 | 当前状态 | 第一输入根 | canonical 输出 |
| --- | --- | --- | --- |
| `场景` | active | `场景设计.json` | `场景面板.json + <scene_key>-layout.json` |
| `角色` | active | `character_design.json` | `<role_id>-...-CharacterPanel-layout.json` |
| `服装` | active | `服装设计.json` | `<costume_id>-...-CostumePanel-layout.json` |
| `道具` | active | `道具设计.json` | `<prop_id>-...-PropPanel-layout.json` |

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/4-Design/2-主体设计/SKILL.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`场景/SKILL.md`
- 强制读取：`角色/SKILL.md`
- 强制读取：`服装/SKILL.md`
- 强制读取：`道具/SKILL.md`

硬规则：

1. 各域 panel 第一输入根必须来自对应的 `2-主体设计` canonical carrier。
2. panel packet 只承载 layout / prompt / display handoff，不反写设计事实。
3. 模板缺失时应阻塞对应域，不得在父层或脚本里另造第二模板。
4. 若用户请求全量 panel build，四域默认可以并行候选；只有用户显式要求共享审阅包时才等全部域汇流后统一说明。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/4-Design/2-主体设计/SKILL.md + CONTEXT.md`
5. 本 `SKILL.md + CONTEXT.md`
6. `.agents/skills/aigc/_shared/project-runtime-layout.md`
7. `场景/SKILL.md + CONTEXT.md`
8. `角色/SKILL.md + CONTEXT.md`
9. `服装/SKILL.md + CONTEXT.md`
10. `道具/SKILL.md + CONTEXT.md`
11. 各域 `2-主体设计` 输出与已存在 `3-面板设计` 产物（若存在）

## Total Input Contract (Mandatory)

### 条件必需输入

- `场景`：`4-Design/场景/2-设计/第N集/场景设计.json`
- `角色`：`4-Design/角色/2-设计/第N集/character_design.json`
- `服装`：`4-Design/服装/2-设计/第N集/服装设计.json`
- `道具`：`4-Design/道具/2-设计/第N集/道具设计.json`

### 关键模板输入

- 各域 `templates/*` 或 `_shared/IO_CONTRACT.md` 中声明的 layout template

### 可选输入

- 各域 prompt sidecar
- 各域逐项 Markdown / 设计卡
- 用户显式指定的 `selected_domains[] / selected_items[]`
- 已存在的各域 `3-面板设计` 输出

### 硬规则

1. 父层先判域，再装配该域的 design carrier 与 template。
2. 若 design carrier 缺失，必须回退到 `2-主体设计`，不得从 `1-主体清单` 或 `3-Detail` 补猜 panel。
3. 若模板缺失，必须阻塞对应域并写明缺口。
4. 同轮多域执行时，未命中的域不得补空 packet。

## Route And Topology Contract (Mandatory)

### 默认模式

1. `single-domain`
2. `multi-domain`
3. `full-build`
4. `incremental-repair`

### 路由规则

1. 需要展示布局包、review-ready packet 或 image handoff JSON 时，统一先进入 `3-面板设计`。
2. 四个 panel leaf 默认相互独立，不以名字序号推断串行。
3. 用户只指定单域时，本轮只命中该域。
4. 全量 panel build 时，四域可并行候选；父层只汇总 coverage 与 handoff readiness。
5. 若某域仅需修补 manifest 或单个 packet，本轮不得重跑整集其余域。

## Canonical Output Governance (Mandatory)

| 领域 | canonical packet | stage-local aggregate | audit sidecar |
| --- | --- | --- | --- |
| `场景` | `<scene_key>-layout.json` | `场景面板.json` | `_manifest.json` |
| `角色` | `<role_id>-...-CharacterPanel-layout.json` | 无额外总稿 | `_manifest.json` |
| `服装` | `<costume_id>-...-CostumePanel-layout.json` | 无额外总稿 | `_manifest.json` |
| `道具` | `<prop_id>-...-PropPanel-layout.json` | 无额外总稿 | `_manifest.json` |

父层补充规则：

1. 父层不生成跨域 `panel_master.json`。
2. 父层只在 `projects/aigc/<项目名>/4-Design/validation-report.md` 记录命中域、blocked templates、下游 handoff。
3. `5-Image` 只能消费已稳定写出的 packet，不应要求 panel 阶段重造设计事实。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-PANEL-STAGE-01` | 阶段定位 | 锁父层只做路由、模板门和验收 | `S1` | 边界清晰度 | `FAIL-PANEL-STAGE-01` |
| `FIELD-PANEL-STAGE-02` | 调度裁决 | 明确命中域、并行候选和 selective dispatch | `S2` | 路由完整性 | `FAIL-PANEL-STAGE-02` |
| `FIELD-PANEL-STAGE-03` | 输入 carrier | 固定各域从 `2-主体设计` carrier 起步 | `S3` | 真源一致性 | `FAIL-PANEL-STAGE-03` |
| `FIELD-PANEL-STAGE-04` | 模板与输出治理 | 固定 packet、aggregate 与 manifest 边界 | `S4` | 输出治理 | `FAIL-PANEL-STAGE-04` |
| `FIELD-PANEL-STAGE-05` | 验收回接 | 锁 `5-Image / review` handoff | `S5` | 闭环完整性 | `FAIL-PANEL-STAGE-05` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-PANEL-STAGE-01` | 当前是不是面板阶段父级问题 | 锁父子边界与不拥有项 | 父层越权写 packet 内容 |
| `S2` | `FIELD-PANEL-STAGE-02` | 本轮命中哪些域、是否需要并行 | 写 route 与 selective dispatch | 多域执行没有任何调度规则 |
| `S3` | `FIELD-PANEL-STAGE-03` | 输入 carrier 是否从 `2-主体设计` 正确继承 | 回指 design carrier 输入根 | 回头从 detail 或 list 直接造 panel |
| `S4` | `FIELD-PANEL-STAGE-04` | 模板与 packet 输出是否稳定 | 写模板门和输出治理表 | manifest 或 aggregate 越权承载事实 |
| `S5` | `FIELD-PANEL-STAGE-05` | 如何证明本轮已可下游消费 | 写 validation 摘要与 handoff | 没有 `5-Image` 或 review 入口 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-PANEL-STAGE-01` | 父层职责与不拥有项明确 | `FAIL-PANEL-STAGE-01` | `S1` |
| `FIELD-PANEL-STAGE-02` | 多域调度与 selective dispatch 明确 | `FAIL-PANEL-STAGE-02` | `S2` |
| `FIELD-PANEL-STAGE-03` | 各域统一从 `2-主体设计` carrier 起步 | `FAIL-PANEL-STAGE-03` | `S3` |
| `FIELD-PANEL-STAGE-04` | 模板、packet、aggregate、manifest 边界稳定 | `FAIL-PANEL-STAGE-04` | `S4` |
| `FIELD-PANEL-STAGE-05` | `validation-report` 与 `5-Image / review` handoff 明确 | `FAIL-PANEL-STAGE-05` | `S5` |

## Root-Cause Execution Contract (Mandatory)

当 `3-面板设计` 出现以下问题时，必须先修源层而不是补单次 layout：

- 某一域从 `1-主体清单` 或 `3-Detail` 直接造 panel
- 模板缺失却在脚本里临时拼结构
- packet 开始回写设计事实
- `5-Image` 仍需重猜 packet 路径或 prompt 来源

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/3-面板设计/SKILL.md`
  - 四个子技能 `SKILL.md`
  - `.agents/skills/aigc/4-Design/2-主体设计/SKILL.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `3-面板设计` 父级阶段合同
- 已锁定四域从 `2-主体设计` carrier 起步的输入边界
- 已明确多域 panel build 的并行候选与 selective dispatch
- 已给出 `projects/aigc/<项目名>/4-Design/validation-report.md` 的 panel-stage 验收回接
