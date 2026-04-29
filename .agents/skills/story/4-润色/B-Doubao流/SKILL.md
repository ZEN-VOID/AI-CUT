---
name: story-polishing-doubao
description: Use when story2026 needs AnyFast Doubao Seed 2.0 Pro to polish an existing `3-初稿` chapter into `projects/story/<项目名>/4-润色/第N卷/第N章.md`.
governance_tier: full
---

# 4-润色 / B-Doubao流

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 必须回读 story 根层 `../../SKILL.md` 与 `../../CONTEXT.md`，再读取 `../SKILL.md` 与 `../CONTEXT.md` 作为 `4-润色` 阶段路由层。
- 若当前任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按当前章相关性加载项目根 `CONTEXT/`。
- 必须读取当前章 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 作为润色主输入；缺失则硬失败。

## Purpose

`B-Doubao流` 是 `4-润色` 阶段的显式 Doubao provider 路径。它通过 AnyFast `doubao-seed-2.0-pro` 对 `3-初稿` 正文做中文表达局部修补或用户显式要求的 Doubao 重润，并写回 `4-润色` canonical path；未点名 provider 的润色默认不走本 lane。

## Mode Selection

| mode | 触发信号 | 主路径 |
| --- | --- | --- |
| `chapter_polish` | `4-润色` 目标章不存在 | 读取 `3-初稿` 后生成第一版最小局部修补稿 |
| `polish_rewrite` | `4-润色` 目标章已存在，用户明确要求 Doubao 重润/覆盖/整章重写 | 回读初稿与既有润色稿后重润；正式覆盖需 `--force` |
| `local_repair` | 用户或审查指出局部语言/质感/AI 检测规整化问题 | 只修复指定问题，不扩大改写 |
| `subagent_review_optimize` | 用户显式要求启用 subagents、按审计点并行审查并直接优化 | 按 `../SKILL.md` 的 `Subagent Review-Optimize Contract` 调度 `story/review` 维度子技能，形成 repair brief 后仍由 Doubao provider 执行最小优化 |
| `dry_run` | 只需要上下文包 | 生成 Doubao messages，不调用 provider、不写正文真源 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 润色输入、frontmatter、provider 与输出细则 | `references/chapter-polishing-contract.md` |
| 执行拓扑、分支、汇流、失败回路 | `steps/chapter-polishing-workflow.md` |
| 判定 chapter_polish / polish_rewrite / local_repair | `types/polishing-type-map.md` |
| 质量门禁与 provider evidence gate | `review/review-contract.md` |
| 显式 subagents 分维度审计并直接优化 | `../SKILL.md` 的 `Subagent Review-Optimize Contract`、`.agents/skills/story/review/SKILL.md + CONTEXT.md`、命中的 review 子技能 `SKILL.md + CONTEXT.md` |
| 可复用润色经验 | `CONTEXT.md` 与 `knowledge-base/polishing-heuristics.md` |
| 输出骨架与系统提示 | `templates/chapter-root.template.md`、`templates/doubao-system-prompt.md`、`templates/output-template.md` |
| 执行机械辅助 | `scripts/polish_chapter_via_doubao.py` |

## Base Polishing Rules

- 默认最小局部修补：保留初稿段落顺序、句群骨架、长短不齐和人物原声，只处理明确坏点。
- 更符合中文表达风格：去翻译腔、说明腔、AI 腔和公式化解释，但不得把全文短句化、整齐分段或通用顺滑化。
- 更符合题材写作质感：读取 `north_star.yaml.genre_contract`，只在必要处把题材压力落实到场景、情绪、对白、心理和段落节奏。
- 初稿事实优先：不新增大情节，不改变核心事件、人物动机、信息揭示和章末牵引。
- 输出必须是完整润色章节 Markdown，不得输出点评、建议稿、差异说明或多个版本。

## Output Contract

| field | contract |
| --- | --- |
| Required output | 基于当前章 `3-初稿` 最小局部修补后的完整中文小说 Markdown 文件。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节润色稿；frontmatter 至少包含 `润色模型: Doubao`、`初稿来源` 与 `字数`。 |
| Output path | `projects/story/<项目名>/4-润色/第N卷/第N章.md`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | `3-初稿` 源章已读取；Doubao provider 真实命中；显式 subagents 模式下已按 `story/review` 维度子技能完成审计并把 findings 注入 Doubao repair brief 直接优化正文；输出通过 frontmatter、heading、最小修补、中文表达与题材质感门禁；正式正文已写回 canonical path。 |
