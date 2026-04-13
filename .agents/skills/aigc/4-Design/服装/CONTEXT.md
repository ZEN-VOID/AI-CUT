# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/服装` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
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
