---
name: comic-episode-poster
description: Use when 漫画项目需要为当前剧集输出一个以实际出场主角、代表性剧情画面、居中文字系统和钩子标题为核心的剧集海报设计 JSON，并可把通过校验的海报 prompt 交接给 .agents/skills/cli/imagegen。
governance_tier: full
---

# 剧集海报

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包。
- 若当前任务绑定 `projects/comic/<项目名>/`，必须优先回读项目上游 artifact，再进入海报创作。
- 若用户要求把海报设计继续生图，必须在本 JSON 通过门禁后，再加载 `.agents/skills/cli/imagegen/SKILL.md` 及其同目录 `CONTEXT.md`，并按该技能合同执行生图/落盘。
- 冲突优先级：用户显式请求 > 仓库 `AGENTS.md` > 本 `SKILL.md` > `references/`、`steps/`、`types/`、`review/`、`templates/` > `agents/openai.yaml` > 同目录 `CONTEXT.md` > `knowledge-base/`。

## Scope

本技能是 `.agents/skills/comic/` 系列当前第 4 段，也是漫画主链的收束阶段。它把当前剧集的剧情钩子、实际出场主角、代表性画面、前景/背景/文字/氛围/配色与生图交接信息汇流为 `comic_episode_poster_design.v1` JSON。

本技能默认只交付海报设计 JSON，不直接生成图片。若用户显式要求“生成海报图 / 生图 / 渲染海报”，本技能先产出并校验 JSON，再把 `prompt_package.positive_prompt` 与 `imagegen_handoff` 交给 `.agents/skills/cli/imagegen`。

## Input Contract

- Accepted input: `project_name`、`episode_number`、当前剧集上游文件、用户标题、目标比例、已有漫画页目录、或要求继续生图的明确指令。
- Required input: `project_name`，以及至少能定位当前集事实的上游 artifact。优先读取 `projects/comic/<项目名>/1-漫画剧本改编/第*.组.md` 与 `projects/comic/<项目名>/2-九刀流漫画提示词/page-group-*.json`；多集项目优先读取 `第N集-page-group-*.json`。
- Optional input: `poster_aspect_ratio`，默认 `3:4`；`title_language`，默认 `zh-CN`；`user_title_text`；`generated_pages_dir`；`render_image` 或等价生图意图。
- Ask before proceeding when: 项目名无法推断、目标 episode 无法定位、缺少分组剧本与九刀流 JSON 两类真源、或用户要求覆盖已有海报 JSON/图片但未明确允许替换。
- Reject or reroute when: 用户只要求生成漫画页，应转 `3-漫画生成`；用户只要求改写上游剧本或九刀流 JSON，应转 1/2 号；用户要求直接生图但没有可用海报设计事实，应先执行本技能 JSON 设计与校验。

## Reference Loading Guide

| need | load |
| --- | --- |
| 字段细则、上游回读、主体/高光/文字规则 | `references/episode-poster-design-contract.md` |
| 思行节点、分支、回退与落盘顺序 | `steps/poster-design-workflow.md` |
| 海报任务分型、类型包加载与默认包规则 | `types/type-map.md` |
| 质量门禁、语义审查、imagegen 交接审查 | `review/review-contract.md` |
| 可复用标题、构图与失败模式 | `knowledge-base/episode-poster-heuristics.md` 与 `CONTEXT.md` |
| JSON schema 与起草骨架 | `templates/episode-poster-design.schema.json`、`templates/episode-poster-design.template.json` |
| Output Contract 对齐说明 | `templates/output-template.md` |
| 结构与内容校验脚本 | `scripts/validate_episode_poster_json.py` |
| 产品侧入口元信息 | `agents/openai.yaml` |
| 后续海报生图工具 | `.agents/skills/cli/imagegen/SKILL.md`、`.agents/skills/cli/imagegen/CONTEXT.md` |

## Mode Selection

| mode | trigger | route |
| --- | --- | --- |
| `design_json` | 默认；用户要求剧集海报设计、海报 JSON、标题/画面/配色合同 | 产出并校验 `comic_episode_poster_design.v1` JSON |
| `design_json_with_user_title` | 用户显式提供标题文字 | 标题直接进入 `text_system.hook_title.text`，只允许最小排版化处理 |
| `design_json_and_render` | 用户明确要求继续生成海报图 | 先完成 JSON，再把 prompt 与 handoff 交给 `.agents/skills/cli/imagegen` |
| `repair_existing_json` | 已有海报 JSON 不合格或需要修复 | 读取 JSON、上游 artifact 与 review gate，定点修复后复验 |
| `batch_episode_posters` | 多集批量海报 | 每集独立执行本技能；可额外生成索引，但单集 JSON 仍是唯一真源 |

## Execution Contract

1. 锁定项目、集数、输出路径与 mode。
2. 加载 `types/type-map.md` 并选择类型包；若用户没有指定，默认 `story-bound-poster`，若要求生图则同时加载 `render-ready-handoff`。
3. 回读上游真源：分组剧本、九刀流 JSON、可选 3 号生成图/报告；记录到 `upstream_context.loaded_artifacts`。
4. 执行 `steps/poster-design-workflow.md`：先列 3-5 个剧情高光候选，再锁定最终高光点、主体、创意标题、三层构图、文字系统与氛围配色。
5. 组装 `comic_episode_poster_design.v1` JSON，并写入 `imagegen_handoff.tool_skill_path = ".agents/skills/cli/imagegen"`。
6. 运行 `scripts/validate_episode_poster_json.py <json_path>`；失败按 `review/review-contract.md` 回退到对应 owner。
7. 若 mode 是 `design_json_and_render`，加载 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`，以已校验 JSON 为唯一设计合同执行生图；不得绕过本 JSON 临时重写画面。

## Root-Cause Execution Contract

若海报设计出现主角不对、像通用角色海报、标题无钩子、文字层级乱、只剩情绪没有剧情绑定、脱离上游风格、抓错剧情高光点、或生图交接绕过 `.agents/skills/cli/imagegen`，按以下链路上溯：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

| symptom | likely owner | repair route |
| --- | --- | --- |
| 输出仍落到 `5-剧集海报` | `SKILL.md` / parent route | 改回 `projects/comic/<项目名>/4-剧集海报/` 并同步 registry |
| 海报脱离本集事实 | `steps/poster-design-workflow.md` | 回到上游回读与高光候选筛选 |
| 主体用了未出场角色 | `references/episode-poster-design-contract.md` | 重做 `subject_lock` 和 presence evidence |
| 标题不采用用户给定文本 | `types/user-title-locked.md` / review gate | 恢复用户标题优先级 |
| prompt 可读但无法生图 | `types/render-ready-handoff.md` / `imagegen_handoff` | 补完整画面、文字、比例、风格与落盘策略 |
| 直接调用旧生图工具或 API | `.agents/skills/cli/imagegen` handoff | 先校验 JSON，再加载 imagegen 技能执行 |

## Field Mapping

| field_id | owner | must contain | fail code |
| --- | --- | --- | --- |
| `FIELD-CEP-01` | `SKILL.md` | Input Contract、Reference Loading Guide、Mode Selection、Output Contract | `FAIL-CEP-ENTRY` |
| `FIELD-CEP-02` | `CONTEXT.md` | Type Map、Repair Playbook、Reusable Heuristics | `FAIL-CEP-CONTEXT` |
| `FIELD-CEP-03` | `references/` | 上游回读、主体、高光、文字、prompt 细则 | `FAIL-CEP-REFERENCE` |
| `FIELD-CEP-04` | `steps/` | 思行节点、分支、回退、落盘顺序 | `FAIL-CEP-STEPS` |
| `FIELD-CEP-05` | `types/` | 分型包、选择信号、固定加载规则 | `FAIL-CEP-TYPES` |
| `FIELD-CEP-06` | `review/` | 结构、语义、imagegen 交接门禁 | `FAIL-CEP-REVIEW` |
| `FIELD-CEP-07` | `templates/` | schema、JSON 模板、Output Contract Alignment | `FAIL-CEP-TEMPLATE` |
| `FIELD-CEP-08` | `scripts/` | JSON validator 等机械校验工具 | `FAIL-CEP-SCRIPT` |
| `FIELD-CEP-09` | `knowledge-base/` | 标题/构图/风格经验与失败模式 | `FAIL-CEP-KB` |
| `FIELD-CEP-10` | `agents/` | OpenAI/Codex 入口元信息 | `FAIL-CEP-AGENT` |

## Output Contract

- Required output: 一个通过校验的 `comic_episode_poster_design.v1` JSON；若用户要求生图，再追加 `.agents/skills/cli/imagegen` 生成结果和落盘记录。
- Output format: JSON 文件。JSON 必须包含 `schema_version`、`project_name`、`type_stack_ref`、`type_pack_context`、`episode`、`upstream_context`、`thinking_process`、`creative_direction`、`subject_lock`、`composition`、`text_system`、`atmosphere_color`、`prompt_package`、`imagegen_handoff`。
- Output path: 默认 `projects/comic/<项目名>/4-剧集海报/第N集-剧集海报.json`；生图结果默认交给 `.agents/skills/cli/imagegen` 按项目绑定资产规则落到同阶段 `imagegen/` 或用户指定目录。
- Naming convention: 单集 JSON 使用 `第N集-剧集海报.json`；批量执行仍保持一集一个 JSON；生图资产使用稳定描述名或 `第N集-剧集海报-vNN.png`，不得无提示覆盖旧文件。
- Completion gate: JSON 通过 `scripts/validate_episode_poster_json.py`；上游加载、风格继承、高光候选、主体边界、双轴居中文字、三层构图、可生图 prompt 与 `imagegen_handoff.tool_skill_path` 全部通过 review gate；若执行生图，最终资产必须由 `.agents/skills/cli/imagegen` 交付并持久化到项目目录。
