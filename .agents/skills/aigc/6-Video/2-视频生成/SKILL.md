---
name: aigc-video-generation
description: Use when the `aigc` video workflow already has stable request JSON and needs provider routing, submit-plan generation, and a model-ready handoff pack before actual provider execution.
governance_tier: full
---

# aigc 6-Video / 2-视频生成

## 概述

`2-视频生成` 是 `6-Video` 阶段里承接“稳定请求对象 -> provider 路由 -> submit-plan -> submit-brief -> 下一执行入口”的叶子父技能。

它不替代外部 provider skill，也不回头改写 `projects/<项目名>/3-Detail/第N集.json`、`1-提示词蒸馏/*` 请求 JSON 或上游设计资产。它只负责把已经稳定的请求对象收束成一个可复核、可续跑、可 handoff 的真实生成入口。

本技能优先回答四件事：

1. 当前请求对象是否已经达到可提交状态。
2. 本轮应该路由到哪个 provider，或是否只能给出推荐主案。
3. 哪些信息必须写进 `submit-plan.json` 与 `submit-brief.md`。
4. 下一入口到底是外部 provider skill、人工提交，还是回上游补请求对象。

## 单一真源声明

- 本 `SKILL.md` 是 `2-视频生成` 的唯一规范真源。
- `CONTEXT.md` 只承载经验层知识库，不再保存规范性路径、字段定义或输出合同。
- `providers/README.md` 仅保留目录说明与槽位列举，不再承载规则真源。
- 本轮升格已将原 `references/*.md` 的字段体系、执行流、类型策略与输出契约内联到本文件；`references/` 不再作为技能规范载体存在。

## When to Use

- 已经拥有来自 `1-提示词蒸馏/全能参照` 或 `1-提示词蒸馏/首帧参照` 的稳定请求 JSON。
- 当前任务目标是选择 provider、组织提交参数、写 `submit-plan.json + submit-brief.md`，而不是继续补 prompt。
- 需要把 `6-Video` 与具体 provider skill 的边界锁清楚。

## When Not to Use

- 还没有合法请求 JSON，或请求对象仍需回到 `1-提示词蒸馏/*` 补齐。
- 当前问题已经明确是 provider 运行时故障排查，而不是提交前组织。
- 仍在修改 `projects/<项目名>/3-Detail/第N集.json`、主体资产或画面资产本体。

## 父技能边界

### `2-视频生成` 拥有

- provider 路由裁决
- `submit-plan.json` 与 `submit-brief.md` 的 canonical 生成入口
- handoff 包与下一执行入口
- 对 `request_ready` 的提交前检查
- manual-only provider 的显式暂停与返工入口

### `2-视频生成` 不拥有

- 改写 `projects/<项目名>/3-Detail/第N集.json`
- 重新生成提示词蒸馏产物
- 直接代替 provider skill 执行提交、轮询与下载
- 把 provider 槽位目录误判为本地已实现执行能力

## Canonical Source Governance

- authoritative source: 本 `SKILL.md`
- derived projection: `CONTEXT.md`
- local note only: `providers/README.md`
- removed carrier: `references/*.md`

允许的本地变化：

- `providers/README.md` 只允许补充 provider 名称列表或非规范性目录注释。
- `CONTEXT.md` 只允许沉淀经验型 Type Map、Playbook、Heuristics 与里程碑 Case。

禁止的第二真源：

- 不再把字段表、执行流程、路由策略、输出模板写回 `references/`。
- 不再让 `providers/README.md` 承担 provider 选择规则、handoff schema 或失败闭环。
- 不再在 `CONTEXT.md` 中放置带强约束力的路径与字段定义。

## Topology Contract

- 当前叶子默认采用父 skill 单点收束，不自动补建本地 subagent team。
- 理由：本叶子以 deterministic 路由、提交前检查与 handoff 组织为主，当前 provider 目录仅为外部执行槽位，不构成值得长期沉淀为本地 governed subagents 的稳定 specialist roster。
- 若未来出现稳定复用的 `provider-router / submit-pack-reviewer / execution-auditor` 角色，并需要跨任务复用，则再按 `skill-subagents` 合同补建 `.codex/agents/...` team 与调用细则。

## Provider Slot Contract

- `providers/` 目录只保留 provider 槽位，不默认视为本地 governed child skill。
- 当前槽位：`grok`、`kling`、`seedance`、`sora`、`veo`、`vidu`。
- 某 provider 只有在补齐 `SKILL.md + CONTEXT.md` 后，才可被视为本地可执行子技能。
- 在此之前，本技能只把 provider 当作 handoff 目标名，不把它们当作“已实现能力”。

## Canonical Inputs

- 命中的 `6-Video` 稳定请求 JSON
- `projects/<项目名>/3-Detail/第N集.json`
- `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`
- 可选：`projects/<项目名>/5-Image/` 与 `projects/<项目名>/4-Design/` 中的引用资产

## Canonical Landing

- tranche 根目录：`projects/<项目名>/6-Video/生成任务/`
- provider 计划目录：`projects/<项目名>/6-Video/生成任务/<provider>/第N集/`
- canonical 计划文件：`projects/<项目名>/6-Video/生成任务/<provider>/第N集/submit-plan.json`
- canonical 简报：`projects/<项目名>/6-Video/生成任务/<provider>/第N集/submit-brief.md`

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VIDGEN-01 | 输入 | 是否已有稳定请求 JSON | `ready/missing` | 检查上游产物存在与完整度 | P0 |
| V-VIDGEN-02 | 路由 | 是否已明确 provider | `explicit/recommend_only` | 读取用户要求与现有计划 | P1 |
| V-VIDGEN-03 | 执行面 | provider 是否已有外部 skill | `skill_available/manual_only` | 结合仓内技能与任务要求 | P1 |

## Route And Type System

| case_id | 触发谓词 | 主策略 | 通过标准 | fallback |
| --- | --- | --- | --- | --- |
| C-VIDGEN-01 | `V-VIDGEN-01=missing` | 停止并回上游补请求对象 | 不伪造提交计划 | 回 `1-提示词蒸馏/*` |
| C-VIDGEN-02 | `V-VIDGEN-01=ready and V-VIDGEN-02=explicit` | 直写对应 provider 的 handoff 包 | `submit-plan.json` 可直接交接 | 无 |
| C-VIDGEN-03 | `V-VIDGEN-01=ready and V-VIDGEN-02=recommend_only` | 写推荐主案 + 备选理由 | 下一入口清楚 | 等用户裁决 |
| C-VIDGEN-04 | `V-VIDGEN-03=manual_only` | 保留完整 handoff 包，不伪造本地执行 skill | 人工可直接接手 | 暂停 |

## Workflow

1. 读取上游稳定请求对象，确认 `request_ready`。
2. 若不满足提交前条件，立即停止并回上游补请求对象。
3. 锁定唯一 provider 或推荐主案。
4. 写 `submit-plan.json`，包括 source request、目标 provider、输出目录、执行说明与返工入口。
5. 写 `submit-brief.md`，包括本轮边界、理由、风险、provider 语义与下一入口。
6. handoff 到外部 provider skill、人工执行入口，或显式暂停等待用户裁决。

## Handoff Contract

推荐最小输入输出命名：

- `source_request`: 当前稳定请求对象与版本
- `provider_selection`: 唯一 provider 或推荐主案
- `submit-plan.json`: 提交参数、目标目录、执行说明、返工入口
- `submit-brief.md`: 边界、理由、风险、下一入口

强制要求：

- 本层结束时默认只给一个下一入口。
- 若 provider 已有外部执行 skill，可直接 handoff。
- 若 provider 当前无本地执行 skill，也必须保留完整 handoff 包，禁止只留一句“手动提交”。
- 最终 canonical artifact 只能由父 skill 写回，provider 槽位目录不拥有 writeback 权。

## Output Contract

阶段级最低交付：

1. `submit-plan.json`
2. `submit-brief.md`
3. provider 路由结论
4. 唯一下一入口

最低要求：

1. 不得只说“去用某 provider”，却没有计划文件。
2. `submit-plan.json` 必须回链上游请求对象。
3. `submit-brief.md` 必须写清边界、风险、返工入口与下一入口。
4. 若 provider 仅存在于 `providers/`，必须明确说明其是槽位，不是本地已建执行 skill。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-VIDGEN-ROOT-01 | `submit-brief.md / tranche 判定` | 说明当前任务为何属于提交前组织层 | S1 | 边界清晰度 | FAIL-VIDGEN-ROOT-01 |
| FIELD-VIDGEN-INPUT-02 | `submit-plan.json / source_request` | 记录稳定请求对象来源与版本 | S2 | 输入可追溯性 | FAIL-VIDGEN-INPUT-02 |
| FIELD-VIDGEN-PROVIDER-03 | `submit-plan.json / provider` | 给出唯一 provider 或明确推荐主案 | S3 | 路由准确性 | FAIL-VIDGEN-PROVIDER-03 |
| FIELD-VIDGEN-PACK-04 | `submit-plan.json / handoff` | 形成提交参数、目标目录与执行说明 | S4 | 提交计划完整性 | FAIL-VIDGEN-PACK-04 |
| FIELD-VIDGEN-HANDOFF-05 | `submit-brief.md / next_entry` | 给出唯一下一入口与返工入口 | S5 | 交接可执行性 | FAIL-VIDGEN-HANDOFF-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-VIDGEN-ROOT-01 | 当前任务是不是提交前组织层 | 锁定叶子边界与排除项 | 本层开始重写 prompt 或剧情 |
| S2 | FIELD-VIDGEN-INPUT-02 | 当前请求对象是否可提交 | 记录 source request 与 readiness verdict | 没有稳定请求对象却继续向下 |
| S3 | FIELD-VIDGEN-PROVIDER-03 | 应该交给哪个 provider | 给唯一 provider 或推荐主案 | 同时给多个无序 provider |
| S4 | FIELD-VIDGEN-PACK-04 | handoff 包要包含什么 | 输出 `submit-plan.json` 主体 | 只留口头说明 |
| S5 | FIELD-VIDGEN-HANDOFF-05 | 下一步到底去哪 | 给唯一下一入口与返工入口 | 执行者仍需自己猜下一步 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-VIDGEN-ROOT-01 | 叶子边界与排除项清楚 | FAIL-VIDGEN-ROOT-01 | S1 |
| FIELD-VIDGEN-INPUT-02 | source request 可追溯且状态明确 | FAIL-VIDGEN-INPUT-02 | S2 |
| FIELD-VIDGEN-PROVIDER-03 | provider 唯一或推荐主案明确 | FAIL-VIDGEN-PROVIDER-03 | S3 |
| FIELD-VIDGEN-PACK-04 | `submit-plan.json` 可供下游直接消费 | FAIL-VIDGEN-PACK-04 | S4 |
| FIELD-VIDGEN-HANDOFF-05 | 下一入口与返工入口明确 | FAIL-VIDGEN-HANDOFF-05 | S5 |

## Audit Contract

质量评估至少覆盖：

- `contract_compliance`: 是否遵守本叶子的触发、边界、输出与 handoff 规则
- `request_readiness`: 上游请求对象是否真的达到可提交状态
- `provider_accuracy`: provider 是否唯一或推荐主案是否写清理由
- `handoff_integrity`: `submit-plan.json + submit-brief.md` 是否足以支撑下一入口
- `auditability`: 是否保留返工入口、路径、risk note 与 provider 槽位语义

审计最小要求：

- provider 槽位目录不得被误当作本地已建执行 skill
- manual-only 情况必须显式停住，不得伪造后续自动执行链
- 失败闭环必须返回 `root cause location + immediate fix + systemic prevention fix`

## Migration And Compatibility

- 旧写法 `3-视频生成` 与 `subtypes/3-视频生成` 已退出当前 canonical path。
- 当前唯一磁盘路径为 `.agents/skills/aigc/6-Video/2-视频生成/`。
- 若文档中仍出现 `tranche-3`，只能作为历史语义背景，不得被解释为当前 filesystem path。
- 本轮升格已把 `references/*.md` 规范内容收束回本 `SKILL.md`；旧 `references/` 文件将在同轮任务中移除。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修 `2-视频生成` 的源层合同：

- 已有稳定请求 JSON，却还是直接跳到 provider 命令
- provider 名称只存在为空目录，却被误判为“本地已建 skill”
- `submit-plan.json` 缺字段、缺落点、缺下一入口
- 本层越权回写上游请求 JSON 或 `projects/<项目名>/3-Detail/第N集.json`
- 规则仍散落在 `references/` 或 `providers/README.md`，导致主合同不是唯一真源

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/providers/README.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 执行前先加载 `.agents/skills/aigc/SKILL.md + CONTEXT.md`。
- 再加载 `.agents/skills/aigc/6-Video/SKILL.md + CONTEXT.md`。
- 再加载本 `SKILL.md + CONTEXT.md`。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/6-Video/SKILL.md` > 本 `SKILL.md` > 各级 `CONTEXT.md`。
