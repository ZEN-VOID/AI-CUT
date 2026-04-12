---
name: aigc-planning
description: Use when the planning stage needs direct episode splitting plus staged patches coordinated through the 规划组 team for format arbitration, grouping, and rhythm handoff before `2-Global`.
governance_tier: full
---

# aigc 1-Planning

## 概述

`1-Planning` 是 `aigc` 技能树在 `0-Init` 之后、`2-Global` 之前的规划阶段父级真源。

本阶段负责把项目故事主源、初始化种子与 leaf/规划组判断收束成同一份规划主稿与规划 handoff，而不是让各子路径各写一套平行真相。

当前稳定链路是：

`Story/ -> 1-分集(逐集原文真源) -> 2-剧本(单技能包，路由 标准剧|解说剧 subagents) -> 3-分组 -> 2-Global`

当前阶段的唯一规范真源由父 `SKILL.md` 持有；`1-分集` 直接由 leaf skill 执行，`.codex/agents/aigc/规划组/` 只承接其余规划判断，默认只返回 `agents_plan + patch / note / report`。

## Skill Execution / Team Routing Rule (Mandatory)

在 `1-Planning` 中，分工固定为：

- `1-分集` 直接由 leaf skill 执行，不再经过规划组 `分集` agent
- 规划组其余 subagents 负责思考、`agents plan`、变体判断、局部证据整理与 `patch / note / report`
- 父 skill 负责总路由、上下文装配、执行收束、validator 调用、canonical 写回、阶段验收与下游 handoff

规划组 subagents 可以决定“怎么想、怎么拆、该走哪个局部方案”，但不能替代 skill 完成阶段执行闭环；`1-分集` 则直接以内生 leaf 合同执行。

## When to Use

- 需要先做分集、格式判模、分组或节奏蓝图，再进入 `2-Global`。
- 需要把 `north_star / init_handoff / story-source-manifest` 收束成逐集规划主稿。
- 需要把 `1-分集` 的逐集原文进一步整理成 `2-剧本` canonical 主稿。
- 需要通过 `.codex/agents/aigc/规划组/team.md` 做格式/分组/节奏选择性调度，并由父 skill 聚合写回。
- 需要给 `2-Global` 预留 `bootstrap_output` 与 `source_profile` handoff。

## When Not to Use

- 当前连 `projects/<项目名>/Story/` 的可用正文都不存在。
- 当前任务已经进入导演组、制作组、主体、画面或视频层。
- 当前只想查询状态、续跑或做验收，应进入 `query / resume / review`。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 分集真源 | `projects/<项目名>/1-Planning/1-分集/第N集.md` | `1-分集` 叶子技能的逐集原文真源 |
| 规划主稿 | `projects/<项目名>/1-Planning/2-剧本/第N集.md` | 规划阶段唯一逐集主稿，由父 skill 聚合写回 |
| 阶段验收 | `projects/<项目名>/1-Planning/validation-report.md` | 规划阶段验收、返工入口与 handoff 结论 |
| 分集执行报告 | `projects/<项目名>/1-Planning/1-分集/执行报告.md` | `1-分集` 叶子技能的全剧集证据侧车 |
| 分集机读索引 | `projects/<项目名>/1-Planning/episode-split-plan.json` | 分集边界、覆盖范围、`source_profile` 与 `bootstrap_output` 索引 |
| 分组主稿 | `projects/<项目名>/1-Planning/3-分组/第N集.md` | `3-分组` 叶子技能的本地 canonical 分组主稿 |
| 分组执行报告 | `projects/<项目名>/1-Planning/3-分组/执行报告.md` | 组边界、组序、量化门槛与 `2-Global` handoff 的总报告 |
| 故事输入根 | `projects/<项目名>/Story/` | 当前阶段默认故事正文输入根 |
| 共享 I/O | `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md` | 规划阶段输入/输出、命名与 handoff 单一真源 |
| 规划组 team | `.codex/agents/aigc/规划组/team.md` | 规划组执行投影与共享禁令 |

## 当前覆盖状态

| 单元 | 当前状态 | 说明 |
| --- | --- | --- |
| `1-分集` | active | 本轮已补齐 leaf skill 合同、经验层与模板 |
| `2-剧本` | active | 已补齐单技能包合同，并在包内路由 `标准剧 / 解说剧` subagents |
| `3-分组` | active | 已重构为 stage-local parent skill：共享规划组只做调度与 specialist patch，量化/写回/校验收回到本地父合同 |
| `4-节奏` | agent-projection | 当前仅以规划组 `节奏` agent 承接 |

## Planning Team Contract (Mandatory)

规划阶段唯一执行投影：

- team：`.codex/agents/aigc/规划组/team.md`
- roles：
  - `.codex/agents/aigc/规划组/格式判模.md`
  - `.codex/agents/aigc/规划组/标准剧.md`
  - `.codex/agents/aigc/规划组/解说剧.md`
  - `.codex/agents/aigc/规划组/分组.md`
  - `.codex/agents/aigc/规划组/节奏.md`

### 父 skill 拥有

- 阶段入口判定
- `1-分集` 直达执行裁决
- `selected_agents[]` 决策
- 上下文裁剪
- `projects/<项目名>/1-Planning/2-剧本/第N集.md` 的唯一写回权
- `validation-report.md` 与下一入口收束
- `2-剧本` 单技能包的最终收束权

### 规划组 agents 拥有

- 局部规划判断
- `agents_plan + patch / note / report`
- 角色侧局部证据与阻塞报告
- `agents plan` 与局部判断产出

### 规划组 agents 不拥有

- `projects/<项目名>/1-Planning/2-剧本/第N集.md` 最终写回
- 第二份规划主稿
- 未命中角色的占位输出
- 将 `标准剧 / 解说剧` 升格为本地 sibling 技能包
- 阶段执行闭环与最终验收

### Stage-Local Ownership Rule

- `规划组/team.md` 是 `1-Planning` 的 shared dispatch plane，不是 `3-分组` 的局部父合同。
- `3-分组` 的 stage-local topology、场景顺序与时长策略投影、quantizer、validator 与 grouped-script writeback 全部只由 `.agents/skills/aigc/1-Planning/3-分组/SKILL.md` 持有。
- `规划组/分组.md` 只返回边界建议与 `patch / note / report`，authoritative 数值字段由 `3-分组` 父 skill 计算。

## Route And Topology Contract (Mandatory)

### 默认 tranche

`1-分集(直达 leaf) -> 格式判模 -> 2-剧本(标准剧 | 解说剧) -> 分组 -> 节奏`

### 路由规则

1. 父 skill 先锁定本轮是只执行 `1-分集`、进入规划组 team，还是走全链规划。
2. 全链规划时，先直达执行 `1-分集`，再做 `格式判模`，随后进入 `2-剧本` 单技能包并路由到互斥的 `标准剧 / 解说剧` subagent，再进入 `分组`。
3. `2-剧本` 默认只接受一个主变体；只有用户显式要求双案对照时，才允许同轮并行调度 `标准剧 + 解说剧`。
4. `节奏` 仅在以下条件至少满足一项时进入：
   - 用户显式要求节奏蓝图、重排或峰值规划
   - `original_adherence == false`
   - 分组已稳定且需要为 `2-Global` 提前登记节奏 handoff
5. 单点直达时，只执行命中的 leaf 或调度命中的 team 角色，不补空路径。
6. 未命中的角色不得伪装成“理论已完成”。

### 后台执行规则

- `1-分集` 默认由 leaf skill 直接执行；规划组 subagents 则在全链串行、`标准剧 + 解说剧` 对照并行或单点直达时默认走后台派发，由父 skill 汇总 patch 后再写回 canonical 产物。
- 只有用户显式要求逐轮共创、某叶子步骤必须前台补充故事事实，或 validator/验收需要人工即时裁决时，父 skill 才转前台阻塞。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/story-source-contract.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`

硬规则：

1. `projects/<项目名>/Story/` 是 `1-分集` 的默认输入根。
2. `story-source-manifest.yaml` 若存在，只作为输入索引、coverage 与 `source_profile` 证据，不替代故事正文本体。
3. `1-分集` 的逐集原文真源固定落在 `projects/<项目名>/1-Planning/1-分集/第N集.md`。
4. 父 skill 的逐集主稿固定落在 `projects/<项目名>/1-Planning/2-剧本/第N集.md`。
5. `1-Planning` 只登记 `bootstrap_output` 与 `source_profile` handoff，不在本阶段创建 `projects/<项目名>/2-Global/导演意图.md` 或 `projects/<项目名>/3-Detail/第N集.json`。

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
10. `projects/<项目名>/1-Planning/1-分集/第N集.md` 与 `projects/<项目名>/1-Planning/1-分集/执行报告.md`（命中 `2-剧本` 时强制）
11. `projects/<项目名>/1-Planning/episode-split-plan.json`（若存在）
12. `projects/<项目名>/team.yaml` 与 `_shared/council-runtime/module-spec.md`（按需）
13. `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md + CONTEXT.md`（命中 `2-剧本` 时强制）
14. 仅加载命中的规划组 agent docs；`1-分集` 不再额外加载 team agent 文档

### 四层上下文

1. `global charter context`
   - 根 `AGENTS.md`
   - `.agents/skills/aigc/SKILL.md`
2. `task context`
   - 用户目标、项目名、当前集数、约束、偏好
3. `role context`
   - 仅命中角色需要的规划上下文
4. `evidence context`
   - `projects/<项目名>/Story/`
   - `story-source-manifest.yaml`（若存在）
   - `episode-split-plan.json`
   - `validation-report.md`

## Execution Workflow

1. 读取 `projects/<项目名>/Story/` 相关内容，并按需结合 `story-source-manifest.yaml` 判断是否允许进入 `1-分集`。
2. 若 `team.yaml.enabled == true`，先按共享 `council-runtime` 判定是否需要 `策划` / `评审` 顾问介入。
3. 锁定本轮是只执行 `1-分集`、只调度局部 team 角色，还是走全链规划；涉及 team 时再明确 `selected_agents[]`，不得模糊下放到多个角色。
4. 若命中 `1-分集`，先确保 `projects/<项目名>/1-Planning/1-分集/` 与 `projects/<项目名>/1-Planning/episode-split-plan.json` 合同可用，并由 leaf skill 直接完成分集。
5. 若命中 `格式判模`，根据项目定位在 `标准剧 / 解说剧` 之间做唯一主案裁决；除非用户显式要求，否则不做双案。
6. 若命中 `2-剧本`，必须先读取 `1-分集` 输出物，再由单技能包内部路由 `标准剧 / 解说剧` subagent，写回 `projects/<项目名>/1-Planning/2-剧本/第N集.md`。
7. 若命中 `分组`，只基于已稳定的分集/格式/剧本结果生成组级结构 patch。
8. 若命中 `节奏`，先校验 `original_adherence` 与分组稳定性。
9. 聚合有效结果：
   - `1-分集` 由 leaf skill 直接写回 `projects/<项目名>/1-Planning/1-分集/第N集.md`
   - 规划组命中角色返回 `agents_plan + patch / note / report`
   - `2-剧本` 写回 `projects/<项目名>/1-Planning/2-剧本/第N集.md`
   - `3-分组` 若命中 shared `分组` specialist，则先后台收集 `agents_plan + patch / note / report`，再由 stage-local parent skill 运行 quantizer/validator，写回 `projects/<项目名>/1-Planning/3-分组/第N集.md` 与 `执行报告.md`
   - 父 skill 负责把这些叶子结果收束进 `validation-report.md` 与下游 handoff，不把上游真源或分组本地稿伪装成第二份剧本主稿
10. 在 `projects/<项目名>/1-Planning/validation-report.md` 记录通过、返工入口与下一阶段 handoff。
11. 返回唯一默认下一入口：`2-Global`。

## Canonical Output Governance (Mandatory)

1. `projects/<项目名>/1-Planning/2-剧本/第N集.md` 是规划阶段唯一逐集主稿。
2. `projects/<项目名>/1-Planning/1-分集/第N集.md` 是 `1-分集` leaf 的上游原文真源，不与主稿竞争。
3. `projects/<项目名>/1-Planning/3-分组/第N集.md` 是 `3-分组` leaf 的本地真源；`执行报告.md` 只承载组级量化与 handoff 证据，不替代主稿。
4. `1-分集` 的执行报告与 `episode-split-plan.json` 只是证据侧车，不与主稿竞争。
5. `2-Global` 只读取规划 handoff 与有效 leaf 产物，不反向把规划信息写回 `1-Planning/1-分集/` 或 `1-Planning/3-分组/`。
6. `1-分集` 作为 direct leaf 只保留一份本地真源，不再旁挂单独 agent 合同。
7. 规划组 agents 只返回局部增量，不能先各写一份平行规划总稿。
8. `2-剧本` 是单技能包；`标准剧 / 解说剧` 只作为其内部变体 subagents，不得在本地重新落成第二套技能真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-PLAN-01 | 阶段定位 | 明确 `1-Planning` 是规划阶段唯一父级真源 | S1 | 边界清晰度 | FAIL-PLAN-01 |
| FIELD-PLAN-02 | 角色路由 | 明确 `selected_agents[]` 与 tranche 规则 | S2 | 路由完整性 | FAIL-PLAN-02 |
| FIELD-PLAN-03 | 共享 I/O | 明确 `1-分集` 真源、`2-剧本` 主稿与 handoff 的单一真源 | S3 | 真源一致性 | FAIL-PLAN-03 |
| FIELD-PLAN-04 | 聚合写回 | 明确父 skill 如何聚合角色 patch 并写回 `1-Planning/2-剧本/第N集.md` | S4 | 聚合可执行性 | FAIL-PLAN-04 |
| FIELD-PLAN-05 | 验收闭环 | 明确 `validation-report`、返工入口与下一阶段 handoff | S5 | 闭环完整性 | FAIL-PLAN-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-PLAN-01 | 当前是不是规划阶段问题 | 锁定阶段边界与父子职责 | 把规划写成导演或明细阶段 |
| S2 | FIELD-PLAN-02 | 本轮该调度哪些角色 | 写出 `selected_agents[]` 与 tranche | 多角色并列但没有路由依据 |
| S3 | FIELD-PLAN-03 | 输入/输出真源是什么 | 回指 shared I/O、story source、runtime layout | `0-Init/` 与 `1-Planning/` 口径混乱 |
| S4 | FIELD-PLAN-04 | 角色结果如何写回 | 只聚合命中 patch 到 `1-Planning/2-剧本/第N集.md` | 角色直接争夺主稿 |
| S5 | FIELD-PLAN-05 | 如何证明本轮完成或阻塞 | 写 `validation-report` 与 triad closure | 没有返工入口或下游 handoff |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-PLAN-01 | 规划阶段边界、父子职责与执行投影关系明确 | FAIL-PLAN-01 | S1 |
| FIELD-PLAN-02 | 角色路由、tranche 与单点直达规则明确 | FAIL-PLAN-02 | S2 |
| FIELD-PLAN-03 | `Story/`、`1-分集/第N集.md`、`episode-split-plan.json`、`1-Planning/2-剧本/第N集.md` 的真源关系明确 | FAIL-PLAN-03 | S3 |
| FIELD-PLAN-04 | 父 skill 独占写回权，agents 只返 `agents_plan + patch / note / report` | FAIL-PLAN-04 | S4 |
| FIELD-PLAN-05 | `validation-report`、返工入口与 `2-Global` handoff 明确 | FAIL-PLAN-05 | S5 |

## Root-Cause Execution Contract (Mandatory)

当规划阶段出现以下问题时，必须先修源层而不是补临时说明：

- 规划组指向不存在的父 skill
- `Story/` 输入根与 `1-Planning/2-剧本/第N集.md` 输出主稿口径冲突
- `projects/<项目名>/Story/` 被绕过，执行期临时猜输入范围
- 规划组角色直接争夺最终写回
- `2-剧本` 被重新拆成两个本地子技能包

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/_shared/story-source-contract.md`
  - `.codex/agents/aigc/规划组/team.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `1-Planning` 阶段父级真源。
- 已锁定规划主稿、分集真源与共享 I/O 的单一口径。
- 已锁定 `2-剧本` 为单技能包，`标准剧 / 解说剧` 只作为 subagents 路由。
- 已明确 `1-分集` 的 direct-leaf 边界与规划组的执行投影边界。
- 已给出 `validation-report` 与 `2-Global` handoff 闭环。
