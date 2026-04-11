---
name: aigc-video-generation
description: Use when the `aigc` video workflow already has stable request JSON and needs provider routing, submit-plan generation, and a model-ready handoff pack before actual provider execution.
governance_tier: full
---

# aigc 6-视频 / 3-视频生成

## 概述

`3-视频生成` 是 `6-视频` 阶段里承接“稳定请求对象 -> provider 选择 -> handoff 包”的 tranche-3 父技能。

它不直接替代外部 provider skill，也不回头改写 `编导/第N集.json` 或提示词蒸馏结果。它只负责把已经稳定的请求 JSON 收束成一个可复核、可续跑、可提交的生成入口。

它优先回答四件事：

1. 当前请求对象是否已经达到可提交状态
2. 本轮应路由到哪个 provider
3. 要把哪些信息写进 `submit-plan.json` 与 `submit-brief.md`
4. 后续应该 handoff 给哪个外部 provider skill 或人工执行入口

## When to Use

- 已经拥有来自 `1-提示词蒸馏/全能参照` 或 `1-提示词蒸馏/首帧参照` 的稳定请求 JSON。
- 当前任务目标是选择 provider、组织提交参数、写 handoff 包，而不是继续补 prompt。
- 需要把 `6-视频` 与具体 provider skill 的边界锁清楚。

## When Not to Use

- 还没有合法请求 JSON，或请求对象仍需回到 `1-提示词蒸馏` 补齐。
- 当前问题已经明确是 provider 运行时故障排查，而不是提交前组织。
- 仍在修改 `编导/第N集.json`、主体资产或画面资产本体。

## 父技能边界

### `3-视频生成` 拥有

- provider 路由裁决
- `submit-plan.json` 与 `submit-brief.md` 的 canonical 生成入口
- handoff 包与下一执行入口
- 对 `request_ready` 的提交前检查

### `3-视频生成` 不拥有

- 改写 `编导/第N集.json`
- 重新生成提示词蒸馏产物
- 直接代替 provider skill 执行提交、轮询与下载

## Provider Slot Contract

- `providers/` 目录只保留 provider 槽位，不默认视为本地 governed child skill。
- 当前槽位：`grok`、`kling`、`seedance`、`sora`、`veo`、`vidu`。
- 某 provider 若未来需要本地执行合同，必须显式升级为 `SKILL.md + CONTEXT.md`，不能继续以空目录充当能力声明。

## Reference Modules (Mandatory)

`3-视频生成/SKILL.md` 只保留父级主合同、边界、路由摘要与回链；专项细则以下列模块为真源：

- `references/chain-of-thought.md`
- `references/execution-flow.md`
- `references/type-strategies.md`
- `references/output-template.md`

硬规则：

1. 主 `SKILL.md` 是唯一父合同；`references/` 是模块化细则承载层，不是并行第二真源。
2. provider 路由、提交前检查、handoff 包与输出模板若需升级，优先回写对应 `references/*.md`。
3. `providers/` 只承载命名槽位，不承载执行合同。

## Canonical Landing

- tranche 根目录：`projects/<项目名>/视频/生成任务/`
- provider 计划目录：`projects/<项目名>/视频/生成任务/<provider>/第N集/`
- canonical 计划文件：`projects/<项目名>/视频/生成任务/<provider>/第N集/submit-plan.json`
- canonical 简报：`projects/<项目名>/视频/生成任务/<provider>/第N集/submit-brief.md`

## Route Summary

- 若用户已显式指定 provider 且请求对象可提交，直接进入对应 provider 计划目录。
- 若用户未指定 provider，但任务目标是“先把提交流程组织好”，父技能先输出 provider 候选与推荐，不越权假设已提交。
- 若 `request_ready` 不成立，停止并回到命中的 `1-提示词蒸馏` 子技能。
- 若问题已经是 provider 运行时故障，则停止在本层并 handoff 到对应 provider skill。

## Execution Summary

- 第一事实源仍是 `projects/<项目名>/编导/第N集.json` 与上游稳定请求 JSON。
- 本层只把“请求对象”转成“执行计划”，不在本层发明新的剧情事实、镜头事实或 prompt 主体。
- 详细执行链、provider 路由与 handoff 规则见 `references/execution-flow.md`。

## Output Summary

- 当前 tranche 的最低交付是：
  - `submit-plan.json`
  - `submit-brief.md`
  - provider 选择理由
  - 下一入口
- 若 provider 尚无本地执行 skill，也必须把 handoff 包写完整，而不是只留一句口头建议。

## Field System Summary

- 字段主表、thought pass 与 pass table 已下沉到 `references/chain-of-thought.md`。
- 主 `SKILL.md` 只保留父级合同摘要，不重复长表。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修 `3-视频生成` 的源层合同：

- 已有稳定请求 JSON，却还是直接跳到 provider 命令
- provider 名称只存在为空目录，却被误判为“本地已建 skill”
- `submit-plan.json` 缺字段、缺落点、缺下一入口
- 本层越权回写上游请求 JSON 或 `编导/第N集.json`

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/SKILL.md`
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/CONTEXT.md`
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/references/*`
- `Meta Rule Source`
  - `.agents/skills/aigc/6-视频/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 执行前先加载 `.agents/skills/aigc/SKILL.md + CONTEXT.md`。
- 再加载 `.agents/skills/aigc/6-视频/SKILL.md + CONTEXT.md`。
- 再加载本 `SKILL.md + CONTEXT.md`。
- 需要具体路由、执行流与输出模板时，继续加载 `references/*.md`。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/6-视频/SKILL.md` > 本 `SKILL.md` > 各级 `CONTEXT.md`。
