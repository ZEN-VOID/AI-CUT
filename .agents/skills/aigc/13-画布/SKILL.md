---
name: aigc-video-stage
description: "Use when routing AIGC 13-canvas video work from grouped storyboard prompts to LibTV canvas control, generation handoff, query, repair, or review."
governance_tier: router
---

# AIGC 13-画布

`13-画布` 是 AIGC 项目的视频生成阶段父入口。本级只负责路由、边界和回接；具体 LibTV 画布项目创建、素材上传、YAML 回刷、视频节点创建和连线由叶子技能持有。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按需加载项目根 `CONTEXT/` 中与视频阶段、LibTV、主体资产相关的文件。
- 进入叶子技能后，必须继续加载叶子 `SKILL.md + CONTEXT.md`，并按叶子 `Reference Loading Guide` 加载必要分区。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 叶子 `SKILL.md` > 叶子分区 > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Input Contract

Accepted input:

- 从 `projects/aigc/<项目名>/10-分组/第N集.md` 生成 LibTV 画布视频节点。
- 创建或选择 LibTV 画布项目，上传角色、场景、道具参照图，回刷 YAML 图片 UUID。
- 修复 LibTV 视频节点主体错绑、图片顺序错乱、画幅或 prompt 证据漂移。

Required input:

- 可定位的 `projects/aigc/<项目名>/` 项目根。
- 可定位的分组稿：通常是 `projects/aigc/<项目名>/10-分组/第N集.md`。
- 真实执行 LibTV 操作前必须能通过 `.agents/skills/cli/libTV` 使用官方 `libtv` CLI。

Reject or clarify when:

- 用户要求本父入口直接改写分镜组剧情、镜头内容或上游创作事实。
- 缺少项目名、集数和分组稿路径，且自动推断会覆盖错误项目。
- 需要删除已有远端视频节点但用户未明确授权。

## Mode Selection

| mode | trigger | route |
| --- | --- | --- |
| `canvas_flow` | 创建画布项目、上传主体参照、回刷 YAML、生成/连线视频节点 | `.agents/skills/aigc/13-画布/libTV画布流/SKILL.md` |

## Output Contract

- Required output: 唯一路由、项目根、分组稿路径、目标叶子技能或阻断原因。
- Output format: 简短路由说明；具体证据文件由叶子技能生成。
- Output path: 本父入口不写业务证据；叶子默认写 `projects/aigc/<项目名>/13-画布/libTV画布流/第N集/`。
- Naming convention: 阶段父入口不命名远端节点；叶子使用分镜组 ID 作为视频节点名。
- Completion gate: route 唯一、项目 runtime 不漂移、未越权改写上游分组稿正文。

## Root-Cause Execution Contract (Mandatory)

失败链路：

`Symptom -> Direct Cause -> 13-画布 route owner -> selected video leaf SKILL.md -> AGENTS.md`

优先修复：

1. 默认视频路线断链：回到本文件 `Mode Selection` 和 `.codex/registry/routes.yaml`。
2. `libTV画布流` 主体错绑：路由到 `libTV画布流/references/image-order-contract.md`。
