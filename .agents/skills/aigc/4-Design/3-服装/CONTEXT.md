# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-服装` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 服装链直接重做角色抽取 | canonical source 层 | 回退到 `2-角色/1-清单/角色清单.json` 作为第一输入根 | 在 `1-清单` 与父级合同中固定“先角色、再服装” | 不再出现角色 identity 漂移 |
| 服装设计只剩 prompt，没有稳定 design master | 输出治理层 | 区分 `服装设计.json` 与 `costume_design_prompt.json` | 将 canonical facts 与执行话术分层 | 下游能稳定复用设计真值 |
| subagents 直接写服装设计主稿 | team 边界层 | 收回 canonical writeback 到 `2-设计` 父 skill | 在 team 合同中固定 `patch / note / report` | agents 不再越权落盘 |
| 服装面板回头重扫导演 JSON | 下游承接层 | 把输入锁定为 `2-设计` 产物 | 在 `3-面板` runner 与合同中同时固化输入根 | panel 只读取 `2-设计/第N集/` |
| 父级 `3-服装` 只剩目录说明，无法在单轮任务中唯一裁路 | 父级编排层 | 把业务分析、阶段判定、路由节点、子路径 bundle 与汇流门收回同一 `SKILL.md` | 固化“父技能每轮只返回一个命中子路径”的知行合一合同 | 当前轮只会命中一个服装子技能 |

## Repair Playbook

1. 先看当前任务是服装对象池、设计 synthesis 还是展示面板。
2. 若还没有 `角色清单.json`，先回到 `2-角色/1-清单`。
3. 若已有角色清单但没有 `costume_design_bridge.json`，进入 `1-清单`。
4. 若 bridge 已有、目标是设计稿或 prompt sidecar，进入 `2-设计`。
5. 若已经有 design master，再考虑 `3-面板`。

## Reusable Heuristics

- 服装链最稳的第一输入根不是导演 JSON，而是已经 canonicalized 的 `角色清单.json`。
- 服装设计不应退化成“角色设计里的一个字段补丁”；一旦需要独立服装面板和设计侧车，就要升格为独立类目真源。
- 面板阶段最稳的输入不是重新回看角色清单，而是已经固化好的 `服装设计.json + costume_design_prompt.json`。
- 对服装类目父技能做知行合一改造时，最关键的不是把三个子技能都列出来，而是让父技能在每一轮只锁定一个命中子路径。

## Case Log

### Case-20260412-AIGC-COSTUME-CATEGORY-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/3-服装` 建立了类目父级合同，并一次性开放 `1-清单 / 2-设计 / 3-面板` 三段 active 路由。
- root_cause_or_design_decision: `4-Design` 父级此前只把 `3-服装` 留作 pending 空目录，导致服装事实既无法从角色清单继续沉淀，也没有独立 design / panel handoff。
- final_fix_or_heuristic: 将服装类目定义为“消费角色清单、沉淀服装真源、供下游面板与图像阶段消费”的独立链路，并明确其第一输入根来自 `2-角色/1-清单`。
- prevention_or_replication_checklist:
  - [x] `3-服装` 父级合同已存在
  - [x] `1-清单 -> 2-设计 -> 3-面板` 顺序已显式化
  - [x] `角色清单.json` 已固定为服装链第一输入根
- evidence_paths:
  - `.agents/skills/aigc/4-Design/3-服装/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `角色 / 场景 / 道具` 三套现有设计技能及其 subagents 配置，完整补齐 `.agents/skills/aigc/4-Design/3-服装`。

### Case-20260412-AIGC-COSTUME-CATEGORY-ZHI-XING-NETWORK

- milestone_type: source_contract_change
- outcome: 在不改变 `角色清单 -> 1-清单 -> 2-设计 -> 3-面板` 真源路径与 team/shared I/O 机制的前提下，将 `3-服装` 父技能重排为知行合一路由网络。
- root_cause_or_design_decision: 原父级合同更像类目说明书，能描述三个 active 子路径，但无法在单轮任务中给出唯一入口、思行节点、汇流门和一次性闭环。
- final_fix_or_heuristic: 将父级主合同升级为 `governance_tier: full`，补齐业务分析、总输入合同、条件路由、思行节点网络、子路径 bundle 细则和 one-shot output，并显式声明 `复杂链路的骨架 / 细则分层 = false`。
- prevention_or_replication_checklist:
  - [x] 父技能已能唯一裁路 `1-清单 / 2-设计 / 3-面板`
  - [x] 思考过程与 triad closure 已进入父级输出合同
  - [x] 未新增第二份服装总稿或平行父级 sidecar
- evidence_paths:
  - `.agents/skills/aigc/4-Design/3-服装/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“内容和机制上全量参照现有配置，但根据知行合一的规范进行编排”，并指定“复杂链路的骨架 / 细则分层：false”。
