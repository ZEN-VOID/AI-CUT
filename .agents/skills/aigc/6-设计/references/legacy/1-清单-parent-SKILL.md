---
name: aigc-design-object-list
description: Use when the `6-设计/1-清单` tranche needs to hold the shared `3-Detail` consumption contract and route the currently landed scene/prop list leaves under `projects/aigc/<项目名>/6-设计/`.
governance_tier: full
---

# aigc 6-设计 / 1-清单

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`1-清单` 是 `6-设计` 阶段承接 `3-Detail`、连接 `2-设计` 的阶段父 skill。

当前 source-layer 已落地的子技能为：

1. `场景`
2. `角色`
3. `道具`

保留中的 sibling 目录：

- `服装`

`服装` 当前只保留路径位，不宣称本轮可执行。

父层拥有：

- list-stage 入口判定与 selective dispatch
- `3-Detail -> 1-清单` 的共享输入口径裁决
- `角色 -> 服装` 的依赖门
- 各 leaf canonical 输出的覆盖率检查
- `projects/aigc/<项目名>/6-设计/validation-report.md` 的阶段级验收摘要

父层不拥有：

- 重写 `3-Detail/第N集.json`
- 生成任何第二份对象池主稿
- 让某个 leaf 越权改写兄弟 leaf 的 canonical 输出
- 把 `_manifest.json` 升格为业务真源

## Stage Coverage Status

| 单元 | 当前状态 | 第一输入根 | 默认输出根 |
| --- | --- | --- | --- |
| `场景` | active | `3-Detail/第N集.json` | `6-设计/场景/1-清单/第N集/` |
| `角色` | active | `3-Detail/第N集.json` | `6-设计/角色/1-清单/第N集/` |
| `服装` | pending-migration | `6-设计/角色/1-清单/第N集/角色清单.json` | 暂不声明 active runtime；不得在初始化时预建 `6-设计/服装/*` |
| `道具` | active | `3-Detail/第N集.json` | `6-设计/道具/1-清单/第N集/` |

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/3-Detail/SKILL.md`
- 强制读取：`.agents/skills/aigc/3-Detail/_shared/episode_detail.json`
- 强制读取：`.agents/skills/aigc/_shared/detail_root_adapter.py`
- 兼容读取：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/6-设计/1-清单/_shared/detail-output-consumption-contract.md`
- 强制读取：`.agents/skills/aigc/6-设计/1-清单/_shared/object-normalization-contract.md`
- 强制读取：`.agents/skills/aigc/6-设计/1-清单/_shared/list-output-contract.md`
- 强制读取：`道具/SKILL.md`
- 条件读取：`场景/SKILL.md`
- 条件读取：`角色/SKILL.md`
- 条件读取：`服装/SKILL.md`

硬规则：

1. `场景 / 角色 / 道具` 的第一输入根固定为 `projects/aigc/<项目名>/3-Detail/第N集.json`。
2. `服装` 的第一输入根固定为 `projects/aigc/<项目名>/6-设计/角色/1-清单/第N集/角色清单.json`。
3. legacy `projects/aigc/<项目名>/编导/第N集.json` 只允许作为兼容 fallback，不得与 canonical 路径并列成双真源。
4. 父层只调度与验收，不创建 stage-level 第二对象池。
5. 全量构建时，`服装` 不得早于 `角色`。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/6-设计/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
5. 本 `SKILL.md + CONTEXT.md`
6. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
7. `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`
8. `.agents/skills/aigc/_shared/detail_root_adapter.py`
9. `.agents/skills/aigc/_shared/project-runtime-layout.md`
10. `.agents/skills/aigc/6-设计/1-清单/_shared/detail-output-consumption-contract.md`
11. `.agents/skills/aigc/6-设计/1-清单/_shared/object-normalization-contract.md`
12. `.agents/skills/aigc/6-设计/1-清单/_shared/list-output-contract.md`
13. 命中 `场景` 时，加载 `场景/SKILL.md + CONTEXT.md`
14. 命中 `角色` 时，加载 `角色/SKILL.md + CONTEXT.md`
15. 命中 `道具` 时，加载 `道具/SKILL.md + CONTEXT.md`
16. 其余 sibling 迁回后，再按命中域追加加载
17. `projects/aigc/<项目名>/3-Detail/第N集.json`
18. `projects/aigc/<项目名>/6-设计/角色/1-清单/第N集/角色清单.json`（若存在）
19. 各 leaf 已存在的 `1-清单` 输出物（若存在）

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`

### 条件必需输入

- `projects/aigc/<项目名>/6-设计/角色/1-清单/第N集/角色清单.json`
  - 当 `服装` leaf 迁回并被命中时必须存在

### 可选输入

- `projects/aigc/<项目名>/编导/第N集.json`
- 用户显式指定的 `selected_domains[] / selected_groups[] / selected_shots[]`
- 已存在的 `6-设计/<领域>/1-清单/第N集/*`

### 硬规则

1. 父层先判定命中域，再读取对应 leaf 所需最小输入。
2. canonical detail root 统一按 `meta + groups[].global/detail.分镜列表` 理解；若 leaf 运行时仍读取 `分镜组列表[] / 分镜明细[]`，必须先经过 `detail_root_adapter.py` 的兼容投影。
3. 若用户只命中单域，本轮不得补跑其余三域。
4. 当前轮若未显式重建其余 sibling，父层允许调度 `场景 / 角色 / 道具`。
5. 任一 leaf 输入缺失时，父层必须阻塞该域，而不是伪造空输出。

## Route And Topology Contract (Mandatory)

### 默认模式

1. `single-domain`
   - 只命中一个 leaf
2. `tri-domain-full-build`
   - 当前可覆盖 `场景 / 角色 / 道具`
3. `future-four-domain-full-build`
   - `服装` 迁回后再启用完整四域
4. `incremental-repair`
   - 只修指定域或指定文件

### 路由规则

1. 需要对象池、research、bridge 的入口，统一先进入 `1-清单`。
2. 只需要场景对象池、research 折叠或 scene bridge 直参，命中 `场景`。
3. 需要 role catalog / research / bridge，命中 `角色`。
4. 需要 prop catalog / research / bridge，命中 `道具`。
5. 需要 costume catalog / research / bridge，但 `服装` 叶子尚未迁回时，父层只报告前置依赖和缺口。
6. 当前全量构建只覆盖 `场景 / 角色 / 道具`；四域全量构建只在 `服装` leaf 回迁后启用。

## Canonical Output Governance (Mandatory)

| 领域 | catalog truth | research / bridge truth | audit sidecar |
| --- | --- | --- | --- |
| `场景` | `场景清单.json` | `场景研究.json`、`scene_design_bridge.json` | `_manifest.json` |
| `角色` | `角色清单.json` | `角色研究.json`、`role_design_bridge.json` | `_manifest.json` |
| `服装` | `服装清单.json` | `服装研究.json`、`costume_design_bridge.json` | `_manifest.json` |
| `道具` | `道具清单.json` | `道具研究.json`、`prop_design_bridge.json` | `_manifest.json` |

父层补充规则：

1. 各 leaf 只在自己的 domain runtime 下写 canonical 输出。
2. 父层只在 `projects/aigc/<项目名>/6-设计/validation-report.md` 汇总当前轮 dispatch、缺口与 handoff。
3. 父层不得生成 `1-清单.json` 一类并列总稿。
4. `2-设计` 只能消费 leaf 已稳定写出的 design-source outputs；对 `场景/角色/道具` 来说，默认同时读取三真源，分别用于对象池、研究证据与设计桥接。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DESIGN-LIST-01` | 阶段定位 | 明确父层只负责路由、依赖门与验收 | `S1` | 边界清晰度 | `FAIL-DESIGN-LIST-01` |
| `FIELD-DESIGN-LIST-02` | 调度裁决 | 明确命中域、全量顺序与 selective dispatch | `S2` | 路由正确性 | `FAIL-DESIGN-LIST-02` |
| `FIELD-DESIGN-LIST-03` | 共享输入 | 固定 `3-Detail` 与 `角色清单.json` 的输入口径 | `S3` | 真源一致性 | `FAIL-DESIGN-LIST-03` |
| `FIELD-DESIGN-LIST-04` | 输出治理 | 锁定各域三真源与 manifest 边界 | `S4` | 输出治理 | `FAIL-DESIGN-LIST-04` |
| `FIELD-DESIGN-LIST-05` | 验收回接 | 写清 validation 摘要与 `2-设计` handoff | `S5` | 闭环完整性 | `FAIL-DESIGN-LIST-05` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-DESIGN-LIST-01` | 当前是不是清单阶段父级问题 | 锁父子边界与不拥有项 | 父层越权改 leaf 输出 |
| `S2` | `FIELD-DESIGN-LIST-02` | 本轮命中哪些域、顺序如何 | 写路由与依赖门 | 全量模式没有顺序或 selective dispatch |
| `S3` | `FIELD-DESIGN-LIST-03` | 输入真源是否被统一锁定 | 回指 shared consumption contracts | 各域各读各的 detail 口径 |
| `S4` | `FIELD-DESIGN-LIST-04` | 各域三真源职责是否清楚 | 写 catalog / research / bridge 治理表 | manifest 被误升格，或三份业务 JSON 互相复制 |
| `S5` | `FIELD-DESIGN-LIST-05` | 如何证明本轮完成并交给下游 | 写 validation 摘要与 handoff | 没有返工口或下游入口 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-DESIGN-LIST-01` | 父层只做路由、依赖门、验收 | `FAIL-DESIGN-LIST-01` | `S1` |
| `FIELD-DESIGN-LIST-02` | 命中域、顺序与 selective dispatch 明确 | `FAIL-DESIGN-LIST-02` | `S2` |
| `FIELD-DESIGN-LIST-03` | `3-Detail` 与 `角色清单.json` 输入口径统一 | `FAIL-DESIGN-LIST-03` | `S3` |
| `FIELD-DESIGN-LIST-04` | 各域三真源与 manifest 边界稳定 | `FAIL-DESIGN-LIST-04` | `S4` |
| `FIELD-DESIGN-LIST-05` | `validation-report` 与 `2-设计` handoff 明确 | `FAIL-DESIGN-LIST-05` | `S5` |

## Review Gate Mapping

No independent gate: 本文件是旧 `1-清单` tranche parent 的 legacy archive，不再作为 active skill 入口、独立阻断真源或当前清单执行合同；所有可复用规则必须回接 `6-设计` 父级 active gate，并由 `场景 / 角色 / 道具` 域级 leaf 复核后才能执行。

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否仍把旧 `.agents/skills/aigc/6-设计/1-清单` 当作当前 active 清单入口，而不是路由到 `场景 / 角色 / 道具` 域级包？ | `GATE-DESIGN-LEGACY-01` | `FAIL-DESIGN-LEGACY-ACTIVE-ENTRY` | `D-N2-DOMAIN`；`references/阶段路由矩阵.md` | 旧 tranche 触发词、改路由后的 active domain package、被移除或保留为 legacy 的引用 |
| 旧合同中的 `3-Detail` 共享输入、角色到服装依赖、leaf coverage 是否未经当前域级 `1-清单` 合同复核就被直接执行？ | `GATE-DESIGN-LEGACY-02` | `FAIL-DESIGN-LEGACY-UNVALIDATED-RULE` | `D-N4-DISPATCH`；对应域级 `1-清单` leaf `SKILL.md + CONTEXT.md` | 被复用的 legacy rule、active leaf 合同位置、采用/废弃理由 |
| 父层是否生成 `1-清单.json` 并列总稿、补空对象池，或把 `_manifest.json` 升格为清单业务真源？ | `GATE-DESIGN-CLOSEOUT-01` | `FAIL-DESIGN-CLOSEOUT-DOMAIN-GATE` | `D-N5-DOMAIN-GATE`；对应域级 `1-清单` Output Contract | canonical `<域>/1-清单/<域>清单.md` 路径、manifest sidecar 边界、根目录平铺文件检查 |
| 旧合同里的 `服装` pending-migration 规则是否被误读为当前可执行 leaf，导致初始化或全量构建预建 `6-设计/服装/*`？ | `GATE-DESIGN-ROUTE-02` | `FAIL-DESIGN-ROUTE-DOMAIN` | `D-N2-DOMAIN`；`references/阶段路由矩阵.md` | active/pending domain table、服装依赖状态、未调度说明 |
| 旧 `FIELD-DESIGN-LIST-* / FAIL-DESIGN-LIST-*` 是否被当作当前 review fail code 使用，而不是作为归档索引回接父级 review contract？ | `GATE-DESIGN-LEGACY-02` | `FAIL-DESIGN-LEGACY-UNVALIDATED-RULE` | `D-N4-DISPATCH`；`review/review-contract.md` | legacy field/fail code 对照、当前 gate/fail code 替换说明 |

## Root-Cause Execution Contract (Mandatory)

当 `1-清单` 出现以下问题时，必须先修源层而不是补单次输出：

- 四个 leaf 对 `3-Detail` 输入口径解释不一致
- `服装` 跳过 `角色清单.json`
- 父层开始生成并列总稿或补空模板
- 下游 `2-设计` 需要重新猜对象池主键

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/6-设计/1-清单/SKILL.md`
  - `.agents/skills/aigc/6-设计/1-清单/_shared/detail-output-consumption-contract.md`
  - `.agents/skills/aigc/6-设计/1-清单/_shared/object-normalization-contract.md`
  - `.agents/skills/aigc/6-设计/1-清单/_shared/list-output-contract.md`
  - 四个 leaf `SKILL.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/3-Detail/SKILL.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `1-清单` 父级阶段合同
- 已锁定 `场景 / 角色 / 道具` 的输入与输出边界，并为 future siblings 保留共享消费真源
- 已明确 `角色 -> 服装` 依赖门只在对应 leaf 回迁后生效
- 已给出 `projects/aigc/<项目名>/6-设计/validation-report.md` 的阶段级验收回接
