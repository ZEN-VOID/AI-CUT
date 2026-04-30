---
name: story-cards-scene
governance_tier: lite
description: "Use when creating, rebuilding, or repairing story scene cards."
---

# 场景卡

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 当父层、项目 `team.yaml` 或本轮任务显式要求启用 subagents / reviewer -> subagent / parallel-council 时，必须加载项目 `team.yaml` 与 `../../_shared/team-advisor-consultation-contract.md`，优先把 `roles.planning.members` 作为资深创作顾问 roster；在正式场景卡 LLM 创作前，按场景功能、规则代价、危险、返场价值与角色适配提出具体请教问题，并把结论汇流为 `advisor_consultation_packet`。
- 本技能只负责场景对象判断与正式场景卡 payload，不替父层承担总线路由与最终 gate。

## Overview

`场景卡` 负责把地点、空间、规则与危险收束为可写戏场景卡。

它必须直接产出：

- `narrative_functions`
- `rule_and_risk`
- `compatible_roles`
- `scene_links`
- `repeat_use_strategy`

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把“可看场景”收束成“可写戏空间”。 |
| `business_object` | `1-设定/3-场景卡/**/*.json`、`scene_links`、场景索引。 |
| `constraint_profile` | 规则先于奇观，复用先于一次性布景。 |
| `success_criteria` | 场景能回答谁来、做什么、代价是什么、为什么值得返场。 |

## Visual Maps

```mermaid
flowchart TD
    A["场景诉求"] --> B["确认进入场景卡 child skill"]
    B --> C["锁 narrative_functions 和场景桶"]
    C --> D["闭合 rule_and_risk 与 compatible_roles"]
    D --> E["建立 scene_links / repeat_use_strategy"]
    E --> F["映射 scene-card.json"]
```

```mermaid
stateDiagram-v2
    [*] --> Routed
    Routed --> Functional
    Functional --> RuleClosed
    RuleClosed --> Reusable
    Reusable --> ReadyForWriteback
```

```mermaid
flowchart LR
    A["narrative_functions"] --> B["rule_and_risk"]
    B --> C["compatible_roles"]
    C --> D["scene_links"]
    D --> E["repeat_use_strategy"]
```

## Total Input Contract

- `0-初始化/north_star.yaml`
- `0-初始化/init_handoff.yaml`
- 既有 `1-设定/3-场景卡/**/*.json`（若存在）
- mixed/full-build 时来自角色卡的进入者与关系压力

## Thinking-Action Network

| step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `S1` | 确认当前真的是场景问题 | `module_route=story-cards > 场景卡/SKILL.md` | `FAIL-CD-SCENE-ROUTE` | 回父技能 |
| `S1A` | 显式启用 subagents 时请教项目监制/规划顾问 | `advisor_consultation_packet.scene_questions + execution_brief` | `FAIL-CD-SCENE-ADVISOR` | 回 `team.yaml` roster 与顾问问题包 |
| `S2` | 锁场景功能与桶位 | `narrative_functions + group` | `FAIL-CD-SCENE-FUNC` | 回场景功能 |
| `S3` | 闭合规则与危险 | `rule_and_risk + compatible_roles` | `FAIL-CD-SCENE-RULE` | 回规则闭合 |
| `S4` | 建立返场能力 | `scene_links + repeat_use_strategy` | `FAIL-CD-SCENE-REUSE` | 回复用策略 |
| `S5` | 映射模板 | `scene-card payload` | `FAIL-CD-SCENE-TEMPLATE` | 回模板映射 |

## One-Shot Output Contract

本技能只交付：

- 正式场景卡 payload
- 可进入索引的 `scene_links`
- 可验证的 `repeat_use_strategy`

## Root-Cause Execution Contract

场景问题优先检查：

1. 场景功能是否成立
2. 显式启用 subagents 时，项目顾问请教是否已转成可执行场景指导
3. 规则/危险/代价是否成立
4. 返场策略是否成立
5. 模板映射是否完整

## Lite Field Mapping

| field_id | step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `FIELD-CD-SCENE-01` | `S1` | 场景路由正确 | `content.module_route` | `FAIL-CD-SCENE-ROUTE` | 回父技能 |
| `FIELD-CD-SCENE-02` | `S1A` | 顾问请教已转为场景指导 | `advisor_consultation_packet.execution_brief` | `FAIL-CD-SCENE-ADVISOR` | 回顾问问题包 |
| `FIELD-CD-SCENE-03` | `S2-S3` | 场景成立 | `narrative_functions + rule_and_risk + compatible_roles` | `FAIL-CD-SCENE-RULE` | 回规则闭合 |
| `FIELD-CD-SCENE-04` | `S4` | 返场能力成立 | `scene_links + repeat_use_strategy` | `FAIL-CD-SCENE-REUSE` | 回复用策略 |
| `FIELD-CD-SCENE-05` | `S5` | 正式模板可写回 | `scene-card payload` | `FAIL-CD-SCENE-TEMPLATE` | 回模板映射 |

## Completion Gate

- 场景不是布景板，而是可写戏空间。
- 显式启用 subagents 时，已生成 `advisor_consultation_packet`，并能说明项目顾问建议如何落实为场景功能、规则代价或返场策略。
- `rule_and_risk` 与 `compatible_roles` 成立。
- `scene_links` 与 `repeat_use_strategy` 可支撑长篇返场。

## Dispatch Note

- 本技能包名称不承载串行语义。
- 当请求只命中场景对象，或与兄弟子技能不存在共享 writeback 依赖时，允许与兄弟子技能并发执行。
- 只有在父技能判定 mixed/full-build 需要先吸收角色接口或为物品提供规则前置时，才进入串行链。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 场景规则、危险、复用策略和角色接口消费细则 | `references/scene-card-contract.md` |
| 显式启用 subagents 时的项目顾问请教、汇流与降级报告 | `../../_shared/team-advisor-consultation-contract.md`、项目 `team.yaml` |
| 执行场景卡生成、修复与回写节点 | `steps/scene-card-workflow.md` |
| 判定场景字段、复用策略和 trace 变量 | `types/field-map.md` |
| 交付前质量门禁 | `review/review-contract.md` |
| 复用场景卡经验 | `knowledge-base/heuristics.md` |
| 正式 JSON skeleton 与交付报告模板 | `templates/scene-card.json`、`templates/output-template.md` |
| 机械辅助说明 | `scripts/README.md` |
| 产品侧入口元数据 | `agents/openai.yaml` |

## Output Contract

- Required output: `projects/story/<项目名>/1-设定/3-场景卡/**/*.json` 中的正式场景卡 payload。
- Output format: 使用 `templates/scene-card.json` 对齐的 JSON；过程摘要可使用 `templates/output-template.md`。
- Output path: 正式业务输出只写入项目根 `1-设定/3-场景卡/`。
- Naming convention: 场景卡文件名应使用 ASCII 安全 id 或项目既有命名规则，不得写入技能目录。
- Completion gate: 父层 `cards_writer.py` 写回成功；显式启用 subagents 时已完成项目顾问请教或按合同报告降级；场景规则可被物品卡和 planning 消费，coverage / review gate 无 blocking finding。
