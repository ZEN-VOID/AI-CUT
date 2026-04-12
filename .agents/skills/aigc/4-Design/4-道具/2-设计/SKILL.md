---
name: aigc-design-prop-design
description: Use when the `4-Design/4-道具/2-设计` stage needs to turn prop bridges plus global presets into a canonical prop design master and prompt sidecar under `projects/<项目名>/4-Design/4-道具/2-设计/`.
governance_tier: full
---

# 4-Design / 4-道具 / 2-设计

## 概述

`2-设计` 是 `4-Design/4-道具` 类目下的 subagent-governed 设计 synthesis 叶子技能。

它不再重复生成研究层，也不把长 prompt 当成唯一真源。它的职责是把上游 `1-清单` 已经稳定写出的 `prop_design_bridge.json`、`道具研究.json`、`道具清单.json`，连同 `2-Global` 和初始化预设，一次收束成：

1. `道具设计.json`
   canonical design master，只保存稳定设计事实、设计决策和 render contract
2. `prop_design_prompt.json`
   prompt sidecar，只保存执行话术、长 prompt 和布局指令
3. `_manifest.json`
   lineage、输入输出与审计侧车

当前子技能采用 `skill-subagents` 的父子治理结构：

- 父 skill 负责触发、路由、上下文装配、patch 聚合、质量门禁与最终写回
- `.codex/agents/aigc/设计组/道具设计/` 下的 subagents 负责结构、材质、痕迹、prompt 和审计的专门化思考
- subagents 默认返回 `agents_plan + patch / note / report`，不直接写 canonical JSON

## Skill / Subagent Execution Rule (Mandatory)

在 `4-道具/2-设计` 中，分工固定为：

- subagents 负责思考、`agents plan`、局部证据整理、字段候选与 `patch / note / report`
- skill 本身负责命中对象裁决、上下文装配、patch 收束、canonical 写回、prompt/audit 闭环与下游 handoff

subagents 可以决定“本轮怎么想、先补哪块、哪些冲突该上抛”，但不能替代 skill 完成阶段执行闭环。

## When to Use

- 已有 `prop_design_bridge.json`，需要把 bridge 收束成单一设计真源。
- 需要生成可直接喂给 `nano-banana/multiview-prop` 或后续 `5-Image` 的道具设计包。
- 需要用 subagents 分工方式分别完善结构、材质、痕迹与 prompt sidecar。

## When Not to Use

- 还没有 `1-清单` 产物，应先回到 `4-道具/1-清单`。
- 当前任务只是继续补 `3-Detail` 道具事实，应回到上游。
- 当前任务是直接执行生图或视频请求，而不是先锁定 design master。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 上游 bridge | `projects/<项目名>/4-Design/4-道具/1-清单/第N集/prop_design_bridge.json` | `2-设计` 的第一输入根 |
| 上游研究 | `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具研究.json` | 研究层补证与 evidence ledger |
| 上游清单 | `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具清单.json` | 原始 shot/group 回链 |
| episode 根文件 | `projects/<项目名>/3-Detail/第N集.json` | 镜头级事实与最新状态 |
| 全局风格 | `projects/<项目名>/2-Global/全局风格.md` | 项目级风格锚点 |
| 类型指导 | `projects/<项目名>/2-Global/类型指导.md` | 项目级类型与导演打法约束 |
| 初始化 handoff | `projects/<项目名>/0-Init/init_handoff.yaml` | 项目级硬边界与世界观基线 |
| north star | `projects/<项目名>/0-Init/north_star.yaml` | 总目标与风格北极星 |
| shared I/O | `.agents/skills/aigc/4-Design/4-道具/2-设计/_shared/IO_CONTRACT.md` | 输入、输出与命名真源 |
| 道具设计组 team | `.codex/agents/aigc/设计组/道具设计/team.md` | subagent 拓扑、后台执行与越权禁令 |

## Prop Design Team Contract (Mandatory)

唯一执行投影：

- team：`.codex/agents/aigc/设计组/道具设计/team.md`
- roles：
  - `.codex/agents/aigc/设计组/道具设计/模型师.md`
  - `.codex/agents/aigc/设计组/道具设计/材质工艺师.md`
  - `.codex/agents/aigc/设计组/道具设计/痕迹叙事师.md`
  - `.codex/agents/aigc/设计组/道具设计/提示词架构师.md`
  - `.codex/agents/aigc/设计组/道具设计/设计审计.md`

### 父 skill 拥有

- `selected_agents[]` 与 tranche 决策
- 上下文裁剪、context packet 装配与 canonical path 归一
- `道具设计.json`、`prop_design_prompt.json`、`_manifest.json` 的最终写回权
- canonical facts 与 prompt sidecar 的分层裁决
- triad closure、阻塞报告与下游 `5-Image` 回接口径

### 道具设计组 agents 拥有

- `agents_plan + patch / note / report`
- 结构、材质、痕迹、prompt 与审计的局部 patch
- 当前角色范围内的 evidence note 与 blocking report

### 道具设计组 agents 不拥有

- 直接写回 `projects/<项目名>/4-Design/4-道具/2-设计/第N集/*.json`
- 把自己的 patch 升格成最终真源
- 重写上游 `3-Detail` 或 `1-清单` 事实
- 用 prompt 文案反向污染 canonical design facts

## Route And Topology Contract (Mandatory)

### 默认 tranche

1. `模型师 + 材质工艺师 + 痕迹叙事师`
   同一批 bridge 输入下并行返回 design section patch
2. `提示词架构师`
   读取父 skill 收束后的 canonical design facts，生成 prompt sidecar patch
3. `设计审计`
   复核事实来源、字段覆盖率、prompt 漂移与下游可执行性

### 路由规则

1. 若 `prop_design_bridge.json` 不存在，停止进入本技能，并返回“先做 `1-清单`”。
2. 若桥接层已存在但 `道具设计.json` 缺失，默认命中：
   - `模型师`
   - `材质工艺师`
   - `痕迹叙事师`
   - `提示词架构师`
   - `设计审计`
3. 若 `道具设计.json` 已存在但只需刷新 prompt sidecar，默认只命中：
   - `提示词架构师`
   - `设计审计`
4. 若用户显式只要求补结构、材质或痕迹，允许单点命中对应角色，但最终仍由父 skill 聚合写回。
5. 若用户给出的输出路径是 `projects/<项目名>/4-Design/2-角色/4-道具` 一类错位路径，父 skill 必须规范化为 `projects/<项目名>/4-Design/4-道具/2-设计/第N集/`，不能跟错路径跑偏。

### 后台执行规则

- 无论当前是 tranche 1 并行、tranche 2 单点 prompt 架构，还是只命中局部角色，道具设计组 subagents 默认都走后台派发，由父 skill 汇总 patch 后统一写回三份 JSON 真源/侧车。
- 只有用户显式要求逐轮共创某个道具设计，或 evidence 缺口必须人工补料时，父 skill 才前台阻塞。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/4-Design/4-道具/2-设计/_shared/IO_CONTRACT.md`
- 强制读取：`.codex/agents/aigc/设计组/道具设计/team.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`

硬规则：

1. 本阶段的第一输入根固定为 `prop_design_bridge.json`，不是重新扫描 `3-Detail` 全量字段。
2. canonical truth 固定写到 `道具设计.json`，prompt 文案与布局话术固定写到 `prop_design_prompt.json`。
3. `_manifest.json` 只承担 lineage、coverage 与审计追踪，不与 canonical truth 争权。
4. 若上游给的是角色目录中的错位路径，必须在本阶段做 path normalization 并写入 manifest。

## Context Contract (Mandatory)

### 加载顺序

1. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
2. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/4-道具/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/4-Design/4-道具/2-设计/_shared/IO_CONTRACT.md`
6. `.codex/agents/aigc/设计组/道具设计/team.md`
7. `projects/<项目名>/0-Init/north_star.yaml`
8. `projects/<项目名>/0-Init/init_handoff.yaml`
9. `projects/<项目名>/2-Global/全局风格.md`
10. `projects/<项目名>/2-Global/类型指导.md`
11. `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具清单.json`
12. `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具研究.json`
13. `projects/<项目名>/4-Design/4-道具/1-清单/第N集/prop_design_bridge.json`
14. `projects/<项目名>/3-Detail/第N集.json`
15. 仅加载命中的 agent docs

### 四层上下文

1. `global charter context`
   - 根 `AGENTS.md`
   - `.agents/skills/aigc/SKILL.md`
2. `task context`
   - 用户目标、项目名、当前集数、显式约束
3. `role context`
   - 结构 / 材质 / 痕迹 / prompt / 审计 各自所需的最小事实切片
4. `evidence context`
   - `bridge / research / catalog / 3-Detail / 全局风格 / 类型指导 / north_star / init_handoff`

## Execution Workflow

1. 读取 bridge、research、catalog 和当前集 detail，锁定输入完整性。
2. 生成父 skill 的 `mission_brief_prop_design`，并装配命中角色的 `subagent_brief_<role>` 与 `context_packet_<role>`。
3. 并行收集 `模型师 / 材质工艺师 / 痕迹叙事师` 的 design section patch。
4. 父 skill 聚合结构、材质、痕迹 patch，先写出 canonical `道具设计.json`。
5. `提示词架构师` 读取 canonical design facts，生成 `prop_design_prompt.json` patch。
6. `设计审计` 复核 canonical truth、prompt sidecar 与 manifest，返回 `review_note_设计审计 + audit_report_设计审计`。
7. 父 skill 写回 `_manifest.json`，并确认下一默认回接口径为 `5-Image` 或 `nano-banana/multiview-prop`。

## Canonical Output Governance (Mandatory)

1. `道具设计.json` 是道具设计事实与 render contract 的唯一真源。
2. `prop_design_prompt.json` 是 prompt sidecar，只承载执行话术、布局说明与模型消费友好的长描述。
3. `_manifest.json` 是 lineage 与审计侧车，不写设计事实。
4. 上游 `道具研究.json`、`prop_design_bridge.json` 仍保留为输入真源，不被本技能覆盖。
5. 任何 subagent 都只能返回 `agents_plan + patch / note / report`，最终 JSON 一律由父 skill 聚合写回。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-PROP-DESIGN-01 | 阶段定位 | 明确 `2-设计` 是 bridge 下游的 design synthesis，而不是研究复写或直接生图 | S1 | 边界清晰度 | FAIL-PROP-DESIGN-01 |
| FIELD-PROP-DESIGN-02 | 角色路由 | 明确 `selected_agents[]`、parallel tranche、prompt tranche 与 audit gate | S2 | 路由完整性 | FAIL-PROP-DESIGN-02 |
| FIELD-PROP-DESIGN-03 | shared I/O | 锁定 bridge 输入根、三份输出与 patch 命名 | S3 | 交接清晰度 | FAIL-PROP-DESIGN-03 |
| FIELD-PROP-DESIGN-04 | canonical design master | `道具设计.json` 必须只保留稳定设计事实、style refs 与 render contract | S4 | 真源稳定性 | FAIL-PROP-DESIGN-04 |
| FIELD-PROP-DESIGN-05 | prompt sidecar | `prop_design_prompt.json` 必须承载长 prompt、布局与模型话术，不回写业务事实 | S5 | 分层正确性 | FAIL-PROP-DESIGN-05 |
| FIELD-PROP-DESIGN-06 | synthesis writeback | 父 skill 聚合 patch，规范化路径并统一落盘 | S6 | 聚合可执行性 | FAIL-PROP-DESIGN-06 |
| FIELD-PROP-DESIGN-07 | audit and trace | 返回 coverage、drift flags、blocking note 与 triad closure | S7 | 审计完整性 | FAIL-PROP-DESIGN-07 |
| FIELD-PROP-DESIGN-08 | downstream handoff | 明确对 `5-Image` / `nano-banana/multiview-prop` 的默认回接 | S8 | 下游可消费性 | FAIL-PROP-DESIGN-08 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-PROP-DESIGN-01 | 当前是不是 bridge 下游的 design synthesis 问题 | 锁定阶段边界与上下游职责 | 把本阶段写成研究层或直接生图 |
| S2 | FIELD-PROP-DESIGN-02 | 本轮该调度哪些角色 | 写出 `selected_agents[]` 与 tranche | 多角色并列但没有进入条件 |
| S3 | FIELD-PROP-DESIGN-03 | 输入输出真源是什么 | 回指 shared I/O 与 team | 输入输出说不清，仍重扫上游 |
| S4 | FIELD-PROP-DESIGN-04 | canonical design master 是否只承载稳定设计事实 | 聚合结构/材质/痕迹 patch 到 `道具设计.json` | prompt 话术污染 canonical truth |
| S5 | FIELD-PROP-DESIGN-05 | prompt sidecar 是否独立且可执行 | 生成 `prop_design_prompt.json` | 把长 prompt 塞回 design master |
| S6 | FIELD-PROP-DESIGN-06 | 父 skill 如何安全写回 | 规范化路径，写回三份 JSON | 路径错位或多真源并存 |
| S7 | FIELD-PROP-DESIGN-07 | 如何证明本轮完成或阻塞 | 输出 review/audit 报告与 manifest | 没有 coverage 或 drift 结论 |
| S8 | FIELD-PROP-DESIGN-08 | 下游如何继续消费 | 返回 `5-Image / multiview-prop` 默认入口 | 结果无法继续进入图像阶段 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-PROP-DESIGN-01 | 阶段边界、父子职责与上下游口径明确 | FAIL-PROP-DESIGN-01 | S1 |
| FIELD-PROP-DESIGN-02 | 角色路由、顺序与后台执行规则明确 | FAIL-PROP-DESIGN-02 | S2 |
| FIELD-PROP-DESIGN-03 | bridge 输入、三份输出与 patch 命名统一 | FAIL-PROP-DESIGN-03 | S3 |
| FIELD-PROP-DESIGN-04 | `道具设计.json` 只保存稳定设计事实与 render contract | FAIL-PROP-DESIGN-04 | S4 |
| FIELD-PROP-DESIGN-05 | `prop_design_prompt.json` 只保存 prompt sidecar 内容 | FAIL-PROP-DESIGN-05 | S5 |
| FIELD-PROP-DESIGN-06 | 父 skill 独占写回，并能规范化错位路径 | FAIL-PROP-DESIGN-06 | S6 |
| FIELD-PROP-DESIGN-07 | triad closure、coverage 与 drift flags 完整 | FAIL-PROP-DESIGN-07 | S7 |
| FIELD-PROP-DESIGN-08 | 结果能被 `5-Image` 或 `nano-banana/multiview-prop` 稳定消费 | FAIL-PROP-DESIGN-08 | S8 |

## Root-Cause Execution Contract (Mandatory)

当 `2-设计` 出现以下问题时，必须先修源层而不是补单次 prompt：

- 只有 `prop_design_bridge.json`，没有 `道具设计.json`
- 把长 prompt 当成唯一道具设计真源
- 路由仍写成 `4-Design/2-角色/4-道具` 之类错位路径
- subagents 直接争夺最终 JSON 的写回权
- prompt sidecar 脱离 canonical design facts，开始自说自话

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/道具设计/team.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-subagents/SKILL.md`

## References

- 输出模板：`references/output-template.md`
- 执行流程：`references/execution-flow.md`
