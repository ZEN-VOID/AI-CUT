---
name: aigc-planning
description: Use when the planning stage needs to execute `1-分集 -> 2-剧本 -> 3-分组` under one parent skill, with routing, variant control, grouping gates, and handoff governance internalized into stage-local SKILL contracts instead of external planning agent docs.
governance_tier: full
---

# aigc 1-Planning

## 概述

`1-Planning` 是 `aigc` 技能树在 `0-Init` 之后、`2-Global` 之前的规划阶段父级真源。

当前阶段的稳定链路固定为：

`Story/ -> 1-分集 -> 2-剧本 -> 3-分组 -> 2-Global`

本次口径进一步收紧为：

- `1-分集` 继续作为 direct leaf skill
- `2-剧本` 继续作为单技能包，但其内部已内化 `格式判模 + 标准剧 + 解说剧 + 编排边界`
- `3-分组` 继续作为 stage-local parent skill，但其内部已内化分组 specialist / 节奏复核规则
- `1-Planning` 父 skill 只回链真实存在的阶段技能，不再依赖已废弃的旧规划组文档

## Internal Capability Fusion Contract (Mandatory)

`1-Planning` 不再通过外部 planning team 文档持有阶段总线；阶段能力面统一分布在父 skill 与各子阶段 skill：

| 能力面 | 当前 owner | 说明 |
| --- | --- | --- |
| 阶段入口判定 | `1-Planning/SKILL.md` | 决定本轮是单点直达还是全链规划 |
| 分集执行 | `1-分集/SKILL.md` | 直接生成逐集原文真源与机读索引 |
| 剧本判模与变体执行 | `2-剧本/SKILL.md` | 在单技能内化 `标准剧 / 解说剧` 与主稿落盘 |
| 分组与节奏复核 | `3-分组/SKILL.md` | 在 stage-local parent 内化组边界、量化门与节奏复核接口 |
| 阶段验收与 handoff | `1-Planning/SKILL.md` | 聚合 leaf/stage 产物并写 `validation-report.md` |

硬规则：

1. `1-Planning` 不得引用不存在的 planning agent 文档。
2. 父 skill 只依赖已声明的 stage-local `SKILL.md + CONTEXT.md + agents/openai.yaml`。
3. 任一子阶段若出现高频分叉，也必须先证明单技能内化已不足，再考虑重新升格 team/agent。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 分集真源 | `projects/<项目名>/1-Planning/1-分集/第N集.md` | `1-分集` 的逐集原文真源 |
| 规划主稿 | `projects/<项目名>/1-Planning/2-剧本/第N集.md` | 规划阶段唯一逐集主稿 |
| 分组主稿 | `projects/<项目名>/1-Planning/3-分组/第N集.md` | `3-分组` 的 grouped script |
| 阶段验收 | `projects/<项目名>/1-Planning/validation-report.md` | 规划阶段验收、返工与 handoff 结论 |
| 分集执行报告 | `projects/<项目名>/1-Planning/1-分集/执行报告.md` | `1-分集` 全剧集证据侧车 |
| 分组执行报告 | `projects/<项目名>/1-Planning/3-分组/执行报告.md` | 分组量化、边界与 handoff 证据 |
| 分集机读索引 | `projects/<项目名>/1-Planning/episode-split-plan.json` | coverage、`source_profile`、`bootstrap_output` |
| 共享 I/O | `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md` | 阶段输入/输出、命名与 handoff 真源 |

## Stage Coverage Status

| 单元 | 当前状态 | 说明 |
| --- | --- | --- |
| `1-分集` | active | direct leaf 执行，已按知行合一重排 |
| `2-剧本` | active | 单技能内化判模、标准剧、解说剧与执行闭环 |
| `3-分组` | active | stage-local parent 内化分组与节奏复核规则 |
| `4-节奏` | folded-into-grouping | 当前不再作为独立 external agent 载体；节奏复核只作为 `3-分组` 内部 reviewer 规则或父级额外 gate |

## Route And Topology Contract (Mandatory)

### 默认 tranche

`1-分集 -> 2-剧本 -> 3-分组 -> 2-Global`

### 路由规则

1. 父 skill 先锁定本轮是单点直达还是全链规划。
2. 只需切分逐集原文时，直达 `1-分集`。
3. 需要规划阶段 canonical 主稿时，进入 `2-剧本`。
4. 需要组边界、量化与分组 handoff 时，进入 `3-分组`。
5. 节奏复核只在以下条件满足至少一项时进入：
   - 用户显式要求节奏预演或重排判断
   - `3-分组` 的 `group_load_score` 与量化门长期冲突
   - `2-Global` 需要额外的节奏影响说明
6. 未命中的阶段不得补空路径、补占位输出或伪造全链完成。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/story-source-contract.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`

硬规则：

1. `projects/<项目名>/Story/` 是 `1-分集` 的默认输入根。
2. `story-source-manifest.yaml` 只作为输入索引与 `source_profile` 证据，不替代故事正文。
3. `1-分集/第N集.md` 是上游逐集原文真源。
4. `2-剧本/第N集.md` 是规划阶段唯一逐集主稿。
5. `3-分组/第N集.md` 是 grouped script，不与 `2-剧本` 竞争。
6. `1-Planning` 只登记 `bootstrap_output` 与 `source_profile` handoff，不在本阶段生成 `2-Global/*.md` 或 `3-Detail/*.json`。

## Context Contract (Mandatory)

### 加载顺序

1. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
2. 本 `SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/_shared/project-runtime-layout.md`
4. `.agents/skills/aigc/_shared/story-source-contract.md`
5. `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
6. `projects/<项目名>/0-Init/north_star.yaml`
7. `projects/<项目名>/0-Init/init_handoff.yaml`
8. `projects/<项目名>/Story/` 相关内容
9. `projects/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
10. `projects/<项目名>/1-Planning/episode-split-plan.json`（若存在）
11. 命中 `1-分集` 时，加载 `1-分集/SKILL.md + CONTEXT.md`
12. 命中 `2-剧本` 时，加载 `2-剧本/SKILL.md + CONTEXT.md`
13. 命中 `3-分组` 时，加载 `3-分组/SKILL.md + CONTEXT.md`

### 四层上下文

1. `global charter context`
2. `task context`
3. `stage context`
4. `evidence context`

## Execution Workflow

1. 读取 `Story/` 与 `0-Init` 相关内容，锁定项目范围。
2. 判定本轮是单点直达还是全链规划。
3. 命中 `1-分集` 时，确保 `1-分集/` 与 `episode-split-plan.json` 合同可用，并由 leaf skill 完成切分。
4. 命中 `2-剧本` 时，必须先读取 `1-分集` 输出物，再由其内部完成变体裁决、主稿写回与 validator。
5. 命中 `3-分组` 时，必须先读取 `2-剧本` 输出物，再由其内部完成组边界、量化与节奏复核 gate。
6. 聚合有效结果并写入 `validation-report.md`。
7. 返回默认下一入口：`2-Global`。

## Canonical Output Governance (Mandatory)

1. `2-剧本/第N集.md` 是规划阶段唯一逐集主稿。
2. `1-分集/第N集.md` 是上游原文真源，不与主稿竞争。
3. `3-分组/第N集.md` 是 grouped script，不是第二份逐集主稿。
4. `1-分集` 与 `3-分组` 的执行报告只承载证据与 handoff，不替代 canonical 正文。
5. 阶段技能各自拥有本地写回权，父 skill 只负责阶段级聚合与验收。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-PLAN-01` | 阶段定位 | 明确 `1-Planning` 是规划阶段唯一父级真源 | `S1` | 边界清晰度 | `FAIL-PLAN-01` |
| `FIELD-PLAN-02` | 阶段路由 | 明确本轮命中的 stage 与 tranche | `S2` | 路由完整性 | `FAIL-PLAN-02` |
| `FIELD-PLAN-03` | 共享 I/O | 明确 `Story/ -> 1-分集 -> 2-剧本 -> 3-分组` 真源关系 | `S3` | 真源一致性 | `FAIL-PLAN-03` |
| `FIELD-PLAN-04` | 聚合写回 | 明确父 skill 如何汇总 stage 产物与验证报告 | `S4` | 聚合可执行性 | `FAIL-PLAN-04` |
| `FIELD-PLAN-05` | 验收闭环 | 明确 `validation-report`、返工入口与下游 handoff | `S5` | 闭环完整性 | `FAIL-PLAN-05` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-PLAN-01` | 当前是不是规划阶段问题 | 锁定阶段边界与父子职责 | 把规划写成导演或明细阶段 |
| `S2` | `FIELD-PLAN-02` | 本轮该走哪个阶段 skill | 写出命中阶段与 route reason | 多阶段并列但没有路由依据 |
| `S3` | `FIELD-PLAN-03` | 真源路径是否锁死 | 回指 shared I/O 与 runtime layout | 输入/输出口径混乱 |
| `S4` | `FIELD-PLAN-04` | 阶段产物如何聚合 | 写 `validation-report` 聚合规则 | 阶段互相争夺写回权 |
| `S5` | `FIELD-PLAN-05` | 如何证明本轮完成或阻塞 | 写返工入口与 `2-Global` handoff | 没有返工入口或下一步 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-PLAN-01` | 阶段边界、父子职责与 stage-local ownership 明确 | `FAIL-PLAN-01` | `S1` |
| `FIELD-PLAN-02` | 路由、单点直达与全链规则明确 | `FAIL-PLAN-02` | `S2` |
| `FIELD-PLAN-03` | `Story/`、`1-分集`、`2-剧本`、`3-分组` 的真源关系明确 | `FAIL-PLAN-03` | `S3` |
| `FIELD-PLAN-04` | 父 skill 只聚合 stage 产物，不替代子阶段写回 | `FAIL-PLAN-04` | `S4` |
| `FIELD-PLAN-05` | `validation-report`、返工入口与 `2-Global` handoff 明确 | `FAIL-PLAN-05` | `S5` |

## Root-Cause Execution Contract (Mandatory)

当规划阶段出现以下问题时，必须先修源层而不是补临时说明：

- 父 skill 仍引用已删除的 planning agent 文档
- `1-分集`、`2-剧本`、`3-分组` 真源关系再次混写
- 子阶段把非 owned truth 写进本阶段 canonical 文件
- `validation-report` 与真实阶段产物脱节

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `1-Planning` 阶段父级真源
- 已锁定 `Story/ -> 1-分集 -> 2-剧本 -> 3-分组` 单一口径
- 已去除对已废弃旧规划组文档的运行依赖
- 已给出 `validation-report` 与 `2-Global` handoff 闭环
