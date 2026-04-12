---
name: aigc-design-scenes
description: Use when the `4-Design` stage needs scene-side artifacts, especially routing scene catalog, scene design, and scene panel work under `projects/<项目名>/4-Design/1-场景/`.
governance_tier: lite
---

# 4-Design / 1-场景

## 概述

`1-场景` 是 `4-Design` 阶段里负责场景对象池、场景设计稿和后续场景展示面板的类目父级合同。

当前轮次已把：

- `1-清单` 固定为场景对象池入口
- `2-设计` 升级为由父 skill 统筹、场景设计组 subagents 分工的设计入口
- `3-面板` 升级为消费 `场景设计.json` 的场景面板 carrier 入口

## When to Use

- 需要把 `3-Detail` / `编导` 中的场景事实继续收束为场景设计源。
- 需要判断当前任务应先做场景清单、场景设计，还是等待后续场景面板。
- 需要说明场景设计与上游导演事实、下游画面/视频之间的消费边界。

## When Not to Use

- 任务其实是角色、服装或道具方向，应回到 `4-Design` 父级改路由。
- 当前诉求已经是图片生成、视频请求或镜头级 prompt，不在本类目执行。
- 上游 `3-Detail / 编导` 事实还未稳定，或 `1-清单` 尚未能建立对象池。

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
- `2-设计`：active，负责在父 skill 收束下调用场景设计组 subagents 生成场景设计稿与 episode 级 design carrier。
- `3-面板`：active，负责把 `2-设计` 的场景设计 carrier 收束为 `场景面板.json + <scene_key>-layout.json`。

## Execution Summary

- 默认顺序固定为 `1-清单 -> 2-设计 -> 3-面板`。
- `2-设计` 默认优先消费 `1-清单` 的 `第N集.json`，再按需回看 `2-Global`、`3-Detail` 与初始化预设。
- 当前类目产物统一写到 `projects/<项目名>/4-Design/1-场景/`。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本类目父级合同：

- 用户要“场景设计”，却没有任何场景清单可供消费。
- 场景链直接从导演 JSON 跳到设计稿，不经过对象池收敛。
- 叶子技能各自重新扫 `3-Detail`，没有复用同一份场景清单。
- 场景设计组 subagents 开始直接写最终产物，而不是回到父 skill 汇总。

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

## Context Preload (Mandatory)

- 先加载 `aigc` 根合同与 `4-Design` 父级合同。
- 再加载本类目 `SKILL.md + CONTEXT.md`。
- 进入 `1-清单`、`2-设计` 或 `3-面板` 时继续加载其本地合同、经验层，以及对应 references/templates/scripts。
