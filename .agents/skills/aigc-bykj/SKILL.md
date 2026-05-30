---
name: aigc-bykj
description: Use when routing BYKJ AIGC workflow tasks across script processing, optimization, episode splitting, global presets, asset extraction, and storyboard stages.
governance_tier: router
metadata:
  short-description: BYKJ AIGC workflow router
---

# aigc-bykj

`aigc-bykj` 是 BYKJ AIGC 工作流的父级导引 skill。它只负责阶段路由、真源边界和输出回接，不直接替代各阶段子技能执行。

## Context Loading Contract

- 每次调用 `$aigc-bykj` 或本目录 `SKILL.md` 时，必须同时加载同目录 `CONTEXT.md`。
- 进入任一阶段目录时，必须继续加载该阶段的 `SKILL.md + CONTEXT.md`。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > 本 `SKILL.md` > 阶段 `SKILL.md` > 阶段 `references/` / `review/` / `types/` / `templates/` > 本 `CONTEXT.md`。

## Stage Routing

| trigger | route | canonical output |
| --- | --- | --- |
| 用户指定任意小说或剧本，要求剧本处理、编剧、导演、表演整合 | `02-剧本处理/` | `output/[项目名]/02-剧本处理/` |
| 用户要求修复或增强既有 `02-剧本处理` 输出 | `02R-剧本优化/` | `output/[项目名]/02R-剧本优化/` |
| 用户要求智能分集、章节/集拆分 | `03-智能分集/` | `output/[项目名]/03-智能分集/` |
| 用户要求全局预设、世界观、角色/风格总设定 | `04-全局预设/` | `output/[项目名]/04-全局预设/` |
| 用户要求优化全局预设 | `04R-全局优化/` | `output/[项目名]/04R-全局优化/` |
| 用户要求资产提取、角色/场景/道具清单 | `05-资产提取/` | `output/[项目名]/05-资产提取/` |
| 用户要求优化资产结果 | `05R-资产优化/` | `output/[项目名]/05R-资产优化/` |
| 用户要求分镜、镜头或 storyboard | `06-智能分镜/` | `output/[项目名]/06-智能分镜/` |
| 用户要求优化分镜 | `06R-分镜优化/` | `output/[项目名]/06R-分镜优化/` |

## Boundary

- 本父级 skill 不直接生成创作正文。
- 阶段输出真源归阶段目录所有。
- `02-剧本处理` 已整合原 `aigc/2-编剧`、`3-导演`、`4-表演` 的核心能力；父级不得把它再拆回三个 canonical 阶段。
- 若阶段目录尚未初始化完整 `SKILL.md + CONTEXT.md`，调用前必须报告缺口或先补齐。

## Output / Handoff Contract

- 父级路由结果必须包含：命中阶段、项目名、输入来源、预期输出目录、下一步应加载的阶段 `SKILL.md`。
- 进入阶段后，以阶段 `SKILL.md` 的输入、输出和 review gate 为准。
