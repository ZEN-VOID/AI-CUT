---
name: aigc-design-roles
description: Use when the `4-Design` stage needs character-side design artifacts, especially routing director episode JSON into role list, role design, or role panel outputs under `projects/<项目名>/4-Design/2-角色/`.
governance_tier: lite
---

# 4-Design / 2-角色

## 概述

`2-角色` 是 `4-Design` 阶段里负责角色对象池、角色设计稿和角色展示面板的类目父级合同。

当前轮次已把 `1-清单`、`2-设计` 与 `3-面板` 做成 active 入口：前者先把导演 JSON 中的镜级角色事实收敛为角色清单，中段把角色对象池收束成结构化设计稿，末段继续生成可下游消费的角色面板 packet。

## When to Use

- 需要从 `projects/<项目名>/3-Detail/第N集.json` 或兼容输入中抽取角色对象池。
- 需要判断角色链当前应先做清单、后做设计，还是进入面板呈现。
- 需要说明角色设计和上游导演事实之间的消费边界。

## When Not to Use

- 任务其实是场景、服装或道具方向，应回到 `4-Design` 父级改路由。
- 当前诉求已经是具体图像生成或视频请求，不在本类目执行。

## 类目边界

### `2-角色` 拥有

- 角色类设计源的父级路由。
- `projects/<项目名>/4-Design/2-角色/` 下的目录约定。
- 从导演事实到角色 design-source 的收敛顺序。

### `2-角色` 不拥有

- 越权重写上游导演 JSON。
- 直接替代 `5-Image` 生成角色图。
- 跳过清单层就发明角色设计定稿。

## 当前路由状态

- `1-清单`：active，本轮已落地。
- `2-设计`：active，承接角色形象、变体与结构化设计稿。
- `3-面板`：active，承接角色展示、layout packet 与面板审阅输入。

## Execution Summary

- 默认顺序固定为 `1-清单 -> 2-设计 -> 3-面板`。
- `1-清单` 负责锁角色 canonical identity、出现证据和穿搭线索。
- 已有 `角色清单.json` 时，默认继续进入 `2-设计`，由 `.codex/agents/aigc/设计组/角色设计/team.md` 承担专门化思考，父 skill 统一写回 `2-设计` canonical 产物。
- 已有 `character_design.json + [角色名].md` 时，默认继续进入 `3-面板`，由 packet runner 把 `prompt整合` 与模板布局收束为角色面板 packet。
- 当前类目产物统一写到 `projects/<项目名>/4-Design/2-角色/`。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本类目父级合同：

- 用户要“角色设计”，却没有任何角色清单可供消费。
- 角色链直接从导演 JSON 跳到面板，不经过对象池收敛。
- `1-清单` 已有输出，但下游仍各自重新扫导演 JSON。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/2-角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/2-角色/1-清单/`
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/`
  - `.agents/skills/aigc/4-Design/2-角色/3-面板/`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 先加载 `aigc` 根合同与 `4-Design` 父级合同。
- 再加载本类目 `SKILL.md + CONTEXT.md`。
- 进入 `1-清单` 时继续加载其 references 与脚本说明。
- 进入 `2-设计` 时继续加载其 `_shared/IO_CONTRACT.md`、references、templates 与角色设计组 team 合同。
- 进入 `3-面板` 时继续加载其 `_shared/IO_CONTRACT.md`、references、template 与 packet runner。
