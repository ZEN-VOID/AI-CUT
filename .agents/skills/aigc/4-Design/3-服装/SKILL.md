---
name: aigc-design-costumes
description: Use when the `4-Design` stage needs costume-side artifacts, especially routing role-list costume facts into wardrobe list, costume design, or costume panel outputs under `projects/<项目名>/4-Design/3-服装/`.
governance_tier: lite
---

# 4-Design / 3-服装

## 概述

`3-服装` 是 `4-Design` 阶段里负责服装对象池、服装设计稿与服装展示面板的类目父级合同。

它不直接与 `2-角色` 争抢角色 identity 真源，而是把角色清单里已经锁住的 `costume_profile / costume_state / evidence` 继续收束为可复用的服装真源。

当前轮次开放三段 active 链路：

- `1-清单`
  - 把 `角色清单.json + 3-Detail/第N集.json` 收束为 `服装清单.json + 服装研究.json + costume_design_bridge.json`
- `2-设计`
  - 把 `costume_design_bridge.json` 继续收束为 `服装设计.json + costume_design_prompt.json + 逐服装设计卡`
- `3-面板`
  - 把 `服装设计.json + costume_design_prompt.json` 继续收束为逐服装 `CostumePanel-layout.json`

## When to Use

- 需要把角色侧已经识别出的穿搭事实升级为独立服装设计真源。
- 需要判断当前任务应先做服装清单、服装设计 synthesis，还是继续进入服装面板。
- 需要把服装类目产物稳定落到 `projects/<项目名>/4-Design/3-服装/`。

## When Not to Use

- 当前任务仍在抽角色 canonical identity，应先回到 `2-角色/1-清单`。
- 当前任务是场景或道具方向，应回到对应 sibling 类目。
- 当前任务已经进入图片生成、视频请求或素材发布，而不是先固化服装设计真源。

## 类目边界

### `3-服装` 拥有

- 服装类 design-source 的父级路由。
- `projects/<项目名>/4-Design/3-服装/` 下的目录约定。
- `角色清单 -> 服装清单 -> 服装设计 -> 服装面板` 的默认收敛顺序。

### `3-服装` 不拥有

- 越权重写 `2-角色/1-清单/角色清单.json` 的角色 identity。
- 越权改写 `3-Detail/第N集.json` 或 `3-Detail/第N集.json`。
- 直接替代 `5-Image` 生成服装图。

## 当前路由状态

- `1-清单`：active，负责 canonical costume roster、研究层与 design bridge。
- `2-设计`：active，负责 canonical design master、prompt sidecar 与服装设计组 subagent synthesis。
- `3-面板`：active，负责基于 design master 产出逐服装 panel layout JSON 与 manifest。

## Execution Summary

- 默认先进入 `1-清单`，把服装对象池、研究层和 bridge 稳定落盘。
- 当 `costume_design_bridge.json` 已存在且目标是“服装设计稿 / prompt sidecar / 可供生图消费的服装真源”时，进入 `2-设计`。
- 当 `服装设计.json` 已存在且目标是“展示面板 / 审阅面板 / layout dossier”时，进入 `3-面板`。
- 当前类目产物统一写到 `projects/<项目名>/4-Design/3-服装/`。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本类目父级合同：

- 服装链重新从导演 JSON 全量扫角色，绕开了 `角色清单.json`。
- 服装链直接从 `角色清单.json` 跳到图片 prompt，没有经过 bridge 或 design master。
- `2-设计` 已有输出，但下游仍各自重新扫角色清单或导演 JSON。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/3-服装/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/3-服装/1-清单/`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/`
  - `.agents/skills/aigc/4-Design/3-服装/3-面板/`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 先加载 `aigc` 根合同与 `4-Design` 父级合同。
- 再加载本类目 `SKILL.md + CONTEXT.md`。
- 进入 `1-清单`、`2-设计` 或 `3-面板` 时继续加载对应本地合同与所需模板/脚本。
