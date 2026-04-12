---
name: aigc-design-props
description: Use when the `4-Design` stage needs prop-side design artifacts, especially routing prop list outputs into design masters, prompt sidecars, or later prop panels under `projects/<项目名>/4-Design/4-道具/`.
governance_tier: lite
---

# 4-Design / 4-道具

## 概述

`4-道具` 是 `4-Design` 阶段里负责道具对象池、道具设计稿与后续面板承接的类目父级合同。

当前类目已经具备三段可执行链：

1. `1-清单`
   把 `3-Detail/第N集.json` 收束为 `道具清单.json + 道具研究.json + prop_design_bridge.json`
2. `2-设计`
   把 `prop_design_bridge.json` 继续收束为 `道具设计.json + prop_design_prompt.json`
3. `3-面板`
   把 `道具设计.json + prop_design_prompt.json` 继续收束为逐道具 `PropPanel-layout.json`

## When to Use

- 需要从导演事实进入道具 design-source、design master 或 panel layout。
- 需要判断当前应先做道具清单、道具设计 synthesis，还是进入 panel handoff。
- 需要把道具类目产物稳定落到 `projects/<项目名>/4-Design/4-道具/`。

## When Not to Use

- 当前任务是角色、场景或服装方向，应回到对应 sibling 类目。
- 当前任务已经进入图片生成或视频请求，而不是先固化道具设计真源。
- 上游 `3-Detail` 尚未稳定，道具对象池都还不存在。

## 类目边界

### `4-道具` 拥有

- 道具类目父级路由。
- `projects/<项目名>/4-Design/4-道具/` 下的目录约定。
- `清单 -> 设计 -> 面板` 的默认收敛顺序。

### `4-道具` 不拥有

- 越权重写 `projects/<项目名>/3-Detail/第N集.json`。
- 直接替代 `5-Image` 生成道具图。
- 跳过清单层直接凭空发明道具设定。

## 当前路由状态

- `1-清单`：active，负责 canonical prop roster、研究层与 design bridge。
- `2-设计`：active，负责 canonical design master、prompt sidecar 与 subagent synthesis。
- `3-面板`：active，负责基于 design master 产出逐道具 panel layout JSON 与 manifest。

## Execution Summary

- 默认先进入 `1-清单`，把道具对象池与 bridge 稳定落盘。
- 当 `prop_design_bridge.json` 已存在且用户目标是“设计稿 / 设计图输入 / 多视图设计页真源”时，进入 `2-设计`。
- 当 `道具设计.json` 已存在且用户目标是“展示面板 / 审阅面板 / panel layout handoff”时，进入 `3-面板`。
- 当前类目产物统一写到 `projects/<项目名>/4-Design/4-道具/`。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本类目父级合同：

- 任务明明是道具设计，却还停留在 `1-清单` 的研究层。
- 道具链直接从 `3-Detail` 跳到 prompt，没有经过 bridge 或 design master。
- `2-设计` 已有输出，但下游仍各自重新扫 `3-Detail`。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/4-道具/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/4-道具/1-清单/`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/`
  - `.agents/skills/aigc/4-Design/4-道具/3-面板/`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 先加载 `aigc` 根合同与 `4-Design` 父级合同。
- 再加载本类目 `SKILL.md + CONTEXT.md`。
- 进入 `1-清单`、`2-设计` 或 `3-面板` 时继续加载对应本地合同与所需模板/脚本。
