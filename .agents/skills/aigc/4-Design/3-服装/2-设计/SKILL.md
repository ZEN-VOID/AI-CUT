---
name: aigc-design-costume-design
description: Use when the `4-Design/3-服装/2-设计` stage needs to turn costume bridges plus global presets into a canonical costume design master, prompt sidecar, and costume design cards under `projects/<项目名>/4-Design/3-服装/2-设计/`.
governance_tier: full
---

# 4-Design / 3-服装 / 2-设计

## 概述

`2-设计` 是 `4-Design/3-服装` 类目下的 subagent-governed 设计 synthesis 叶子技能。

它不再重复生成服装研究层，也不把角色设计中的 `wardrobe_profile` 直接冒充服装设计主稿。它的职责是把上游 `1-清单` 已经稳定写出的 `costume_design_bridge.json`、`服装研究.json`、`服装清单.json`，连同 `2-Global`、初始化预设和可选 `character_design.json`，一次收束成：

1. `服装设计.json`
   canonical design master，只保存稳定服装事实、设计决策和 render contract
2. `costume_design_prompt.json`
   prompt sidecar，只保存执行话术、长 prompt 和 panel / image handoff
3. `第N集/<costume_id>-<canonical_label>.md`
   与 JSON 同源的人读稿
4. `_manifest.json`
   lineage、输入输出与审计侧车

## Skill / Subagent Execution Rule (Mandatory)

在 `3-服装/2-设计` 中，分工固定为：

- subagents 负责思考、`agents plan`、局部证据整理、字段候选与 `patch / note / report`
- skill 本身负责命中服装裁决、上下文装配、patch 收束、canonical 写回、prompt/audit 闭环与下游 handoff

subagents 可以决定“本轮怎么想、先补哪块、哪些冲突该上抛”，但不能替代 skill 完成阶段执行闭环。

## When to Use

- 已有 `costume_design_bridge.json`，需要把 bridge 收束成单一服装设计真源。
- 需要生成可直接供 `3-面板`、`5-Image` 或 `nano-banana/costume-swap` 继续消费的服装设计包。
- 需要用服装设计组 subagents 分工方式分别完善廓形层次、材质纹样、配饰连续性与 prompt sidecar。

## When Not to Use

- 还没有 `1-清单` 产物，应先回到 `4-Design/3-服装/1-清单`。
- 当前任务只是继续补角色设计或导演分镜事实，应回到上游。
- 当前任务是直接执行生图或视频请求，而不是先锁定 design master。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 上游 bridge | `projects/<项目名>/4-Design/3-服装/1-清单/第N集/costume_design_bridge.json` | 本阶段第一输入根 |
| 上游研究 | `projects/<项目名>/4-Design/3-服装/1-清单/第N集/服装研究.json` | 研究层补证与 evidence ledger |
| 上游清单 | `projects/<项目名>/4-Design/3-服装/1-清单/第N集/服装清单.json` | 原始 shot/group 回链 |
| 角色设计可选输入 | `projects/<项目名>/4-Design/2-角色/2-设计/第N集/character_design.json` | 锚点对齐与避免重复定义角色主体 |
| episode 根文件 | `projects/<项目名>/3-Detail/第N集.json` | 镜头级穿搭、动作与 continuity 证据 |
| 全局风格 | `projects/<项目名>/2-Global/全局风格.md` | 项目级风格锚点 |
| 类型指导 | `projects/<项目名>/2-Global/类型指导.md` | 项目级类型与时代约束 |
| 初始化 handoff | `projects/<项目名>/0-Init/init_handoff.yaml` | 项目级硬边界 |
| north star | `projects/<项目名>/0-Init/north_star.yaml` | 总目标与风格北极星 |
| shared I/O | `.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md` | 输入、输出与命名真源 |
| 服装设计组 team | `.codex/agents/aigc/设计组/服装设计/team.md` | subagent 拓扑、后台执行与越权禁令 |

## Costume Design Team Contract (Mandatory)

唯一执行投影：

- team：`.codex/agents/aigc/设计组/服装设计/team.md`
- roles：
  - `.codex/agents/aigc/设计组/服装设计/服装统筹.md`
  - `.codex/agents/aigc/设计组/服装设计/廓形层次设计师.md`
  - `.codex/agents/aigc/设计组/服装设计/材质纹样设计师.md`
  - `.codex/agents/aigc/设计组/服装设计/配饰连续性设计师.md`
  - `.codex/agents/aigc/设计组/服装设计/提示词架构师.md`
  - `.codex/agents/aigc/设计组/服装设计/服装一致性复核.md`
  - `.codex/agents/aigc/设计组/服装设计/真源审计.md`

### 父 skill 拥有

- `selected_costumes[]` 与 tranche 决策
- 上下文裁剪、context packet 装配与 canonical path 归一
- `服装设计.json`、逐服装 Markdown、`costume_design_prompt.json`、`_manifest.json` 的最终写回权
- canonical facts 与 prompt sidecar 的分层裁决
- triad closure、阻塞报告与下游 `3-面板 / 5-Image` 回接口径

### 服装设计组 agents 拥有

- `agents_plan + patch / note / report`
- 廓形层次、材质纹样、配饰连续性、prompt 与审计的局部 patch
- 当前服装范围内的 evidence note 与 blocking report

### 服装设计组 agents 不拥有

- 直接写回 `projects/<项目名>/4-Design/3-服装/2-设计/第N集/*`
- 把自己的 patch 升格成最终真源
- 重写上游 `1-清单`、`2-角色/2-设计` 或 `编导` 真源
- 把 prompt 文案反向污染 canonical design facts

## Route And Topology Contract (Mandatory)

### 默认 tranche

1. `服装统筹`
   先锁本轮命中服装、批次、缺口与返工入口
2. `廓形层次设计师 + 材质纹样设计师 + 配饰连续性设计师`
   在同一批 bridge 输入下并行返回 design section patch
3. `服装一致性复核`
   检查三类 patch 是否在同一 costume identity 上收束
4. `提示词架构师`
   读取父 skill 收束后的 canonical design facts，生成 prompt sidecar patch
5. `真源审计`
   复核事实来源、字段覆盖率、prompt 漂移与路径

### 路由规则

1. 若 `costume_design_bridge.json` 不存在，停止进入本技能，并返回“先做 `1-清单`”。
2. 若桥接层已存在但 `服装设计.json` 缺失，默认命中：
   - `服装统筹`
   - `廓形层次设计师`
   - `材质纹样设计师`
   - `配饰连续性设计师`
   - `服装一致性复核`
   - `提示词架构师`
   - `真源审计`
3. 若 `服装设计.json` 已存在但只需刷新 prompt sidecar，默认只命中：
   - `提示词架构师`
   - `真源审计`
4. 若用户显式只要求补某一套 costume、某一类材质或 continuity，允许单点命中对应角色，但最终仍由父 skill 聚合写回。

### 后台执行规则

- 无论当前是 tranche 2 并行 specialists、tranche 4 prompt 架构，还是只命中局部角色，服装设计组 subagents 默认都走后台派发，由父 skill 汇总 patch 后统一写回 canonical 产物。
- 只有用户显式要求逐轮共创某套服装，或 evidence 缺口必须人工补料时，父 skill 才前台阻塞。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md`
- 强制读取：`.codex/agents/aigc/设计组/服装设计/team.md`

硬规则：

1. 本阶段的第一输入根固定为 `costume_design_bridge.json`，不是重新扫描 `角色清单` 或 `编导` 全量字段。
2. canonical truth 固定写到 `服装设计.json`，prompt 文案与布局话术固定写到 `costume_design_prompt.json`。
3. `_manifest.json` 只承担 lineage、coverage 与审计追踪，不与 canonical truth 争权。
4. 逐服装 Markdown 必须与 `服装设计.json.costumes[]` 同源，而不是平行真相。

## Context Contract (Mandatory)

### 加载顺序

1. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
2. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/3-服装/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md`
6. `.codex/agents/aigc/设计组/服装设计/team.md`
7. `projects/<项目名>/0-Init/north_star.yaml`
8. `projects/<项目名>/0-Init/init_handoff.yaml`
9. `projects/<项目名>/2-Global/全局风格.md`
10. `projects/<项目名>/2-Global/类型指导.md`
11. `projects/<项目名>/4-Design/3-服装/1-清单/第N集/服装清单.json`
12. `projects/<项目名>/4-Design/3-服装/1-清单/第N集/服装研究.json`
13. `projects/<项目名>/4-Design/3-服装/1-清单/第N集/costume_design_bridge.json`
14. `projects/<项目名>/4-Design/2-角色/2-设计/第N集/character_design.json`
15. 仅加载命中的 agent docs

## Execution Workflow

1. 读取 bridge、research、catalog 与当前集 director evidence，锁定输入完整性。
2. 生成父 skill 的 `mission_brief_costume_design`，并装配命中角色的 `subagent_brief_<role>` 与 `context_packet_<role>`。
3. 调度 `服装统筹` 生成批次、优先级与返工入口。
4. 并行收集 `廓形层次设计师 / 材质纹样设计师 / 配饰连续性设计师` 的 design section patch。
5. `服装一致性复核` 复核 candidate 是否仍是同一套 costume identity。
6. 父 skill 聚合三类 patch，先写出 canonical `服装设计.json` 与逐服装 Markdown。
7. `提示词架构师` 读取 canonical design facts，生成 `costume_design_prompt.json` patch。
8. `真源审计` 复核 canonical truth、prompt sidecar 与 manifest，返回 `review_note_服装一致性 + audit_report_真源审计`。
9. 父 skill 写回 `_manifest.json`，并确认下一默认回接口径为 `3-面板` 或 `5-Image`。

## Canonical Output Governance (Mandatory)

1. `服装设计.json` 是服装设计事实与 render contract 的唯一真源。
2. `costume_design_prompt.json` 是 prompt sidecar，只承载执行话术、布局说明与模型消费友好的长描述。
3. `第N集/<costume_id>-<canonical_label>.md` 是与 JSON 同源的人读稿，不是第二真源。
4. `_manifest.json` 是 lineage 与审计侧车，不写设计事实。
5. 上游 `服装研究.json`、`costume_design_bridge.json` 仍保留为输入真源，不被本技能覆盖。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-COSTUME-DESIGN-01 | 阶段定位 | 明确 `2-设计` 是 bridge 下游的 design synthesis，而不是研究复写或直接生图 | S1 | 边界清晰度 | FAIL-COSTUME-DESIGN-01 |
| FIELD-COSTUME-DESIGN-02 | 角色路由 | 明确 `selected_costumes[]`、parallel tranche、prompt tranche 与 audit gate | S2 | 路由完整性 | FAIL-COSTUME-DESIGN-02 |
| FIELD-COSTUME-DESIGN-03 | shared I/O | 锁定 bridge 输入根、三类输出与 patch 命名 | S3 | 交接清晰度 | FAIL-COSTUME-DESIGN-03 |
| FIELD-COSTUME-DESIGN-04 | canonical design master | `服装设计.json` 只保留稳定服装事实、layer system 与 continuity contract | S4 | 真源稳定性 | FAIL-COSTUME-DESIGN-04 |
| FIELD-COSTUME-DESIGN-05 | prompt sidecar | `costume_design_prompt.json` 只承载长 prompt、布局与模型话术 | S5 | 分层正确性 | FAIL-COSTUME-DESIGN-05 |
| FIELD-COSTUME-DESIGN-06 | markdown card | 逐服装 Markdown 必须与 JSON 同源并可审阅 | S6 | 人读一致性 | FAIL-COSTUME-DESIGN-06 |
| FIELD-COSTUME-DESIGN-07 | synthesis writeback | 父 skill 聚合 patch 并统一落盘 | S7 | 聚合可执行性 | FAIL-COSTUME-DESIGN-07 |
| FIELD-COSTUME-DESIGN-08 | audit and trace | 返回 coverage、drift flags、blocking note 与 triad closure | S8 | 审计完整性 | FAIL-COSTUME-DESIGN-08 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-COSTUME-DESIGN-01 | 当前是不是 bridge 下游的 design synthesis 问题 | 锁定阶段边界与上下游职责 | 把本阶段写成研究层或直接生图 |
| S2 | FIELD-COSTUME-DESIGN-02 | 本轮该调度哪些角色 | 写出 `selected_costumes[]` 与 tranche | 多角色并列但没有进入条件 |
| S3 | FIELD-COSTUME-DESIGN-03 | 输入输出真源是什么 | 回指 shared I/O 与 team | 输入输出说不清，仍重扫上游 |
| S4 | FIELD-COSTUME-DESIGN-04 | canonical design master 是否只承载稳定服装事实 | 聚合廓形/材质/连续性 patch 到 `服装设计.json` | prompt 话术污染 canonical truth |
| S5 | FIELD-COSTUME-DESIGN-05 | prompt sidecar 是否独立且可执行 | 生成 `costume_design_prompt.json` | 把长 prompt 塞回 design master |
| S6 | FIELD-COSTUME-DESIGN-06 | 人读稿是否与 JSON 同源 | 写逐服装 Markdown | Markdown 与 JSON 断链 |
| S7 | FIELD-COSTUME-DESIGN-07 | 父 skill 如何安全写回 | 规范化路径，写回 JSON + Markdown + manifest | 路径错位或多真源并存 |
| S8 | FIELD-COSTUME-DESIGN-08 | 如何证明本轮完成或阻塞 | 输出 review/audit 报告与 manifest | 没有 coverage 或 drift 结论 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-COSTUME-DESIGN-01 | 阶段边界、父子职责与上下游口径明确 | FAIL-COSTUME-DESIGN-01 | S1 |
| FIELD-COSTUME-DESIGN-02 | 角色路由、顺序与后台执行规则明确 | FAIL-COSTUME-DESIGN-02 | S2 |
| FIELD-COSTUME-DESIGN-03 | bridge 输入、输出与 patch 命名统一 | FAIL-COSTUME-DESIGN-03 | S3 |
| FIELD-COSTUME-DESIGN-04 | `服装设计.json` 只保存稳定服装事实与 render contract | FAIL-COSTUME-DESIGN-04 | S4 |
| FIELD-COSTUME-DESIGN-05 | `costume_design_prompt.json` 只保存 prompt sidecar 内容 | FAIL-COSTUME-DESIGN-05 | S5 |
| FIELD-COSTUME-DESIGN-06 | 逐服装 Markdown 与 JSON 同源 | FAIL-COSTUME-DESIGN-06 | S6 |
| FIELD-COSTUME-DESIGN-07 | 父 skill 独占写回并能统一落盘 | FAIL-COSTUME-DESIGN-07 | S7 |
| FIELD-COSTUME-DESIGN-08 | triad closure、coverage 与 drift flags 完整 | FAIL-COSTUME-DESIGN-08 | S8 |

## Root-Cause Execution Contract (Mandatory)

当 `2-设计` 出现以下问题时，必须先修源层而不是补单次 prompt：

- 只有 `costume_design_bridge.json`，没有 `服装设计.json`
- 把角色设计里的 `wardrobe_profile` 当成唯一服装设计真源
- subagents 直接争夺最终 JSON 的写回权
- prompt sidecar 脱离 canonical design facts，开始自说自话

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/服装设计/team.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-subagents/SKILL.md`

## References

- 输出模板：`references/output-template.md`
- 执行流程：`references/execution-flow.md`
- 类型策略：`references/type-strategies.md`
