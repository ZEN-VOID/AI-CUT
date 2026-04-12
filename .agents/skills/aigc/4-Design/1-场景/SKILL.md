---
name: aigc-design-scenes
description: Use when the `4-Design` stage needs scene-side artifacts, especially routing scene catalog, scene design, and scene panel work under `projects/<项目名>/4-Design/1-场景/`.
governance_tier: lite
---

# 4-Design / 1-场景

## 概述

`1-场景` 是 `4-Design` 阶段里负责场景对象池、场景设计稿和场景展示面板的类目父级合同。

当前口径已经统一为：

- `1-清单`：知行合一单合同，负责锁定 scene catalog
- `2-设计`：知行合一单合同，负责将场景对象池收束为场景设计卡与 `场景设计.json`
- `3-面板`：消费 `场景设计.json` 的场景面板入口

场景链当前不再依赖 `.codex/agents/aigc/设计组/场景设计` 作为外挂真源；相关判断面已经被吸收进 `2-设计/SKILL.md`。

## When To Use

- 需要判断当前任务应先做场景清单、场景设计，还是进入后续场景面板。
- 需要说明场景对象池、场景设计与场景面板之间的消费边界。
- 需要修复场景链的阶段顺序、真源边界或 handoff 口径。

## When Not To Use

- 任务其实是角色、服装或道具方向，应回到 `4-Design` 父级改路由。
- 当前诉求已经是图片生成、视频请求或镜头级 prompt，不在本类目执行。
- 上游 `3-Detail` 事实还未稳定，或 `1-清单` 尚未能建立对象池。

## 类目边界

### `1-场景` 拥有

- 场景类设计源的父级路由。
- `projects/<项目名>/4-Design/1-场景/` 下的目录约定。
- `清单 -> 设计 -> 面板` 的默认消费顺序。

### `1-场景` 不拥有

- 越权改写上游导演 JSON。
- 直接替代 `5-Image / 6-Video` 生成最终请求。
- 跳过清单层就凭空发明场景设定定稿。

## 当前路由状态

- `1-清单`：active，负责把镜级场景事实收束为 scene catalog。
- `2-设计`：active，负责以内收能力镜面的单技能方式生成场景设计稿与 episode 级 design carrier。
- `3-面板`：active，负责把 `场景设计.json` 收束为 `场景面板.json + <scene_key>-layout.json`。

## Execution Summary

- 默认顺序固定为 `1-清单 -> 2-设计 -> 3-面板`。
- `2-设计` 默认优先消费 `1-清单` 的 `第N集.json`，再按顺序吸收 `2-Global`、`3-Detail` 与 `0-Init`。
- 当前类目产物统一写到 `projects/<项目名>/4-Design/1-场景/`。

## Lite Field Map

| field_id | 覆盖范围 | 内容要求 | 验证点 | 失败信号 |
| --- | --- | --- | --- | --- |
| FIELD-SCN-PARENT-01 | 路由顺序 | 明确 `1-清单 -> 2-设计 -> 3-面板` 为默认消费链 | 下游都以同一 scene source 为输入 | 叶子技能各自重扫上游真源 |
| FIELD-SCN-PARENT-02 | 真源边界 | 明确 `1-清单` 拥有对象池、`2-设计` 拥有设计真源、`3-面板` 拥有展示真源 | 无叶子技能越权改写兄弟阶段产物 | 对象池与设计稿相互覆盖 |
| FIELD-SCN-PARENT-03 | 能力归属 | 明确原 scene-design agents 能力已内收至 `2-设计/SKILL.md` | 不再存在活动中的外挂 scene-design agent 真源依赖 | 路由仍回指外部 agent 合同 |

## Root-Cause Execution Contract

当出现以下症状时，必须先修本类目父级合同：

- 用户要“场景设计”，却没有任何场景清单可供消费。
- 场景链直接从导演 JSON 跳到设计稿，不经过对象池收敛。
- `2-设计` 仍回指外挂 scene-design agents，而不是使用内收后的单技能合同。
- 叶子技能各自重新扫 `3-Detail`，没有复用同一份场景清单。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/1-场景/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/`
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/`
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload

- 先加载 `aigc` 根合同与 `4-Design` 父级合同。
- 再加载本类目 `SKILL.md + CONTEXT.md`。
- 进入 `1-清单`、`2-设计` 或 `3-面板` 时继续加载其本地合同、经验层，以及对应 templates/scripts。
