---
name: story-polishing-deepseek
description: Use when story2026 needs DeepSeek `deepseek-v4-pro` to polish an existing `3-初稿` chapter into `projects/story/<项目名>/4-润色/第N卷/第N章.md`.
governance_tier: full
---

# 4-润色 / C-Deepseek流

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 必须回读 story 根层 `../../SKILL.md` 与 `../../CONTEXT.md`，再读取 `../SKILL.md` 与 `../CONTEXT.md` 作为 `4-润色` 阶段路由层。
- 必须同时读取 `.agents/skills/api/deepseek/SKILL.md` 与 `.agents/skills/api/deepseek/CONTEXT.md`，确认 DeepSeek provider 固定 `deepseek-v4-pro`、默认 `thinking=enabled`、`reasoning_effort=high`。
- 若当前任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按当前章相关性加载项目根 `CONTEXT/`。
- 必须读取当前章 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 作为润色主输入；缺失则硬失败。

## Purpose

`C-Deepseek流` 是 `4-润色` 阶段的 DeepSeek provider 路径。它通过 `.agents/skills/api/deepseek` 固定调用 `deepseek-v4-pro`，对 `3-初稿` 正文做高推理二次改写润色，并写回 `4-润色` canonical path。

## Mode Selection

| mode | 触发信号 | 主路径 |
| --- | --- | --- |
| `chapter_polish` | `4-润色` 目标章不存在 | 读取 `3-初稿` 后生成第一版润色稿 |
| `polish_rewrite` | `4-润色` 目标章已存在，用户要求重润/覆盖 | 回读初稿与既有润色稿后重润；正式覆盖需 `--force` |
| `local_repair` | 用户或审查指出局部语言/质感问题 | 只修复指定问题，不扩大改写 |
| `dry_run` | 只需要上下文包 | 生成 DeepSeek messages，不调用 provider、不写正文真源 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 润色输入、frontmatter、provider 与输出细则 | `references/chapter-polishing-contract.md` |
| 执行拓扑、分支、汇流、失败回路 | `steps/chapter-polishing-workflow.md` |
| 判定 chapter_polish / polish_rewrite / local_repair | `types/polishing-type-map.md` |
| 质量门禁与 provider evidence gate | `review/review-contract.md` |
| 可复用润色经验 | `CONTEXT.md` 与 `knowledge-base/polishing-heuristics.md` |
| 输出骨架与系统提示 | `templates/chapter-root.template.md`、`templates/deepseek-system-prompt.md`、`templates/output-template.md` |
| 执行机械辅助 | `scripts/polish_chapter_via_deepseek.py` |

## Base Polishing Rules

- 更符合中文表达风格：去翻译腔、说明腔、AI 腔、过度工整句式，让句群有自然呼吸和停顿。
- 更符合题材写作质感：读取 `north_star.yaml.genre_contract`，把题材压力落实到场景、情绪、对白、心理和段落节奏。
- 初稿事实优先：不新增大情节，不改变核心事件、人物动机、信息揭示和章末牵引。
- 输出必须是完整润色章节 Markdown，不得输出点评、建议稿、差异说明或多个版本。

## Output Contract

| field | contract |
| --- | --- |
| Required output | 基于当前章 `3-初稿` 二次改写后的完整中文小说 Markdown 文件。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节润色稿；frontmatter 至少包含 `润色模型: Deepseek` 与 `初稿来源`。 |
| Output path | `projects/story/<项目名>/4-润色/第N卷/第N章.md`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | `3-初稿` 源章已读取；DeepSeek provider 真实命中；输出通过 frontmatter、heading、正文完整度、中文表达与题材质感门禁；正式正文已写回 canonical path。 |
