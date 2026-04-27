---
name: comic-nine-blade-prompts
description: Use when 上游 `第N组.md` 漫剧剧本或用户指定剧本需要按组进入九刀流，并分别蒸馏为可供 3 号 CLI imagegen 执行层生成 9 张漫画页的结构化长提示词 JSON，尤其适合要固定角色、跨页叙事、漫画格布局、对白/旁白/独白/SFX 文本规范的场景。
governance_tier: full
---

# 九刀流漫画提示词

技能包 ID: `comic-nine-blade-prompts`

本技能把 `1-漫画剧本改编` 产出的 `第N组.md`，或用户直接提供的剧本片段，蒸馏为 `nine_blade_comic_prompts.v1` 组级 JSON。每个 page-group 可被 `3-漫画生成` 投影为 9 个 CLI imagegen 单页 jobs，生成 9 张独立竖版漫画页，而不是九宫格拼图、同图九变体或单幅海报。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须识别来源/连续性/交接 mode，并按 `Reference Loading Guide` 加载 `steps/source-routing-and-handoff.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包；本技能语境下类型包仅指 `types/漫画/<题材>/` 题材包，来源/连续性/交接 mode 不再归入 `types/`。
- 若当前任务绑定具体 `projects/comic/<项目名>/`，先读取项目已存在的上游 `1-漫画剧本改编/第N组.md` 与前序 group JSON；若项目存在连续集产物，前序 JSON 视为 continuity 证据。
- 若同目录 `CONTEXT.md`、`steps/source-routing-and-handoff.md`、`types/type-map.md` 或命中题材类型包缺失，应先补齐最小骨架或报告阻塞，不得跳过预加载继续执行。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > `references/` / `steps/` / `review/` / `types/` / `templates/` > `agents/openai.yaml` > 项目上下文 > `CONTEXT.md`。

## Input Contract

### Required input

- `source_script`：上游 `第N组.md` 正文、用户指定剧本、或足够完整的情节片段。

### Optional input

- `grouped_script_files`：`projects/comic/<项目名>/1-漫画剧本改编/第*.组.md`；存在时默认视为唯一文本真源。
- `legacy_formatted_source_script`：仅作为旧项目兼容回退，不再是新口径 canonical output。
- `type_stack_ref` / `type_pack_context`：优先继承 1 号阶段已锁定的 active packs 与 `stage_projection.nine_blade_prompting`。
- `style_profile`：默认 `cinematic_comic_realism`，可切换国风连环画、美漫电影感、韩漫、暗黑写实等。
- `episode_index`：多集项目用于启用 `第N集-` 防覆盖命名。
- `output_path`：用户指定输出目录或 JSON 文件路径。

### Source priority

1. `projects/comic/[项目名]/1-漫画剧本改编/第*.组.md`
2. 用户直接提供的 `source_script`
3. legacy 项目的 `projects/comic/[项目名]/1-漫画剧本改编/formatted_source_script.json`

若第 1 项存在，不得忽略分组文件再从整篇 prose 二次自由猜结构。

### Reject or clarify when

- 没有可用剧情正文、分组文件为空、或 raw source 不足以形成 9 页连续漫画。
- 用户要求生成非 9 页、非 9:16、单幅海报、九宫格拼图或同画面九变体。
- 用户要求脚本自动生成核心创作正文；本技能的切页、角色锁、风格锁和页级 prompt 必须由 LLM 直接创作，脚本只做校验/投影/落盘辅助。

## Mode Selection

| mode | 触发信号 | 合同位置 |
| --- | --- | --- |
| `grouped-script` | 已存在 `第N组.md` 或用户提供明确 group | `steps/source-routing-and-handoff.md` |
| `raw-source-fallback` | 只有 raw source，没有 1 号阶段分组产物 | `steps/source-routing-and-handoff.md` |
| `multi-episode-continuity` | 用户点名第 2 集/第 3 集，或目录已有其他集 JSON | `steps/source-routing-and-handoff.md` |
| `poster-aware-handoff` | 下游需要 4 号剧集海报继续消费剧情高光、角色和风格锚点 | `steps/source-routing-and-handoff.md` |

mode 可叠加：多集 raw source 可同时命中 `raw-source-fallback` 与 `multi-episode-continuity`；需要强化海报交接时再叠加 `poster-aware-handoff`。漫画题材类型包另由 `types/type-map.md` 选择。

## Reference Loading Guide

按任务动态加载，不要把全部分区一次性灌入上下文。

| 场景 | 读取文件 |
| --- | --- |
| 九刀流字段、主角锚、场景锚、版式和文字硬规则 | `references/nine-blade-prompt-contract.md` |
| 来源前奏、切组、九刀节点、失败回路与 handoff | `steps/nine-blade-workflow.md` |
| 来源模式、连续性模式与 4 号海报 handoff | `steps/source-routing-and-handoff.md` |
| 漫画题材类型包选择、固定上下文加载与互斥/叠加规则 | `types/type-map.md` 与命中题材包 |
| 漫画风格、版式、提示词拼装经验与反模式 | `knowledge-base/comic-prompt-heuristics.md` |
| 输出质量、字段审计、review/provider 降级口径 | `review/review-contract.md` |
| JSON 模板与 schema | `templates/nine-blade-template.json`、`templates/nine-blade-comic-prompts.schema.json`、`templates/output-template.md` |
| 结构校验脚本 | `scripts/validate_nine_blade_prompt_json.py` |
| 产品侧入口元信息 | `agents/openai.yaml` |

## Execution Contract

1. 读取 `CONTEXT.md`、`steps/source-routing-and-handoff.md`、`types/type-map.md` 和命中题材类型包，锁定 mode、上游真源和输出命名。
2. 优先消费 `第N组.md`；若没有分组文件，先按 `raw-source-fallback` mode 做最小格式化和临时切组，不额外挂出第二份 canonical 组计划。
3. 以每个 group 为单位进入 `steps/nine-blade-workflow.md` 的 `P1 -> N8` 节点网络。
4. 由 LLM 直接完成 `story_beat_map[9]`、`main_character_lock`、`character_locks`、`scene_continuity_bible`、`style_bible`、`comic_text_system` 与 9 个 page prompt 的主创判断。
5. 组装 `nine_blade_comic_prompts.v1` JSON，并用 `scripts/validate_nine_blade_prompt_json.py` 进行机械校验。
6. 输出 group JSON 与同名前缀思考摘要；思考摘要只说明切组理由、切页理由、版式策略、continuity 继承和关键风险，不输出冗长推理草稿。

## Output Contract

### Required output

- 每个 page-group 一份 `nine_blade_comic_prompts.v1` JSON。
- 同轮可附一份思考过程摘要，说明切组/切页/版式/continuity 决策与风险。

### Output format

- JSON 根对象必须包含：`schema_version`、`page_group`、`continuity_context`、`generation_contract`、`type_stack_ref`、`type_pack_context`、`main_character_lock`、`scene_continuity_bible`、`style_bible`、`character_locks`、`comic_text_system`、`story_beat_map`、`pages`、`global_negative_prompt`。
- `pages` 必须恰好 9 个；每页必须是竖版 9:16 多格漫画页，包含 `active_character_ids`、`scene_id`、`layout`、`panels`、`page_number_overlay`、`positive_prompt`。

### Output path

- 单集默认：`projects/comic/[项目名]/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json`
- 多集默认：`projects/comic/[项目名]/2-九刀流漫画提示词/第N集-page-group-01-nine_blade_comic_prompts.json`
- 思考摘要与 JSON 使用同一前缀：`page-group-01-思考过程摘要.md` 或 `第N集-page-group-01-思考过程摘要.md`。

### Naming convention

- group 文件使用两位序号：`page-group-01-nine_blade_comic_prompts.json`。
- 多集文件必须加 `第N集-` 前缀，避免覆盖旧集 canonical truth。
- 任务 ID、字段 ID 和 schema version 保持 ASCII 安全；中文只用于用户可读标题、正文和路径前缀。

### Completion gate

- `python3 .agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py <json_path>` 通过。
- 人工 review 确认：不是九宫格、不是同图九变体、每页多格、角色/场景/风格跨页稳定、右下角页码为纯数字 1-9、四类文字槽至少各覆盖一次。
- 若下游需要 4 号剧集海报，确认 `pages[].panels[]` 足以提炼 3-5 个剧情高光候选。

## Field Mapping

| field_id | owner | output_or_rule | fail_code |
| --- | --- | --- | --- |
| `FIELD-NB-01` | `steps/` | 来源判模与前奏验证通过 | `FAIL-NB-SOURCE-ROUTE` |
| `FIELD-NB-02` | `steps/` | grouped / raw / multi-episode / poster-aware mode 路由正确 | `FAIL-NB-MODE-ROUTE` |
| `FIELD-NB-03` | `steps/` | 当前 group 的 9 个连续页级剧情刀口 | `FAIL-NB-BEATS` |
| `FIELD-NB-04` | `references/` | 主角锚、群像锚和场景锚完整 | `FAIL-NB-LOCKS` |
| `FIELD-NB-05` | `references/` | 漫画风格锁、版式多样性和文字系统完整 | `FAIL-NB-STYLE` |
| `FIELD-NB-06` | `templates/` | JSON 满足 schema 与输出模板 | `FAIL-NB-CONTRACT` |
| `FIELD-NB-07` | `review/` | schema + semantic review 双门通过 | `FAIL-NB-REVIEW` |
| `FIELD-NB-08` | `scripts/` | 校验脚本只做机械验证，不替代 LLM 主创 | `FAIL-NB-SCRIPT-OVERREACH` |
| `FIELD-NB-09` | `types/` | 漫画题材类型包加载正确，并透传 `type_stack_ref / type_pack_context` | `FAIL-NB-TYPE-PACK` |

## Quality Gates

- 顶层 `generation_contract.hard_constraints` 必须包含 9 separate pages、no nine-grid collage、no same-scene variants、multiple comic panels、character/scene consistency、bottom-right digits-only page number。
- `style_bible` 与每页 `positive_prompt` 都必须注入同一条全局视觉 DNA；禁止跨页切成儿童绘本、Q 版、影视概念图、3D render 或 live-action storyboard。
- 每页 prompt 推荐顺序：`vertical 9:16 comic page` -> layout grammar -> global style anchor -> main character anchor -> active character anchors -> scene anchor -> page number -> consistency rule -> panel actions -> readable Chinese lettering -> mood。
- 版式默认至少 5 个不同 `layout_id`，动态版式不少于 3 类。
- `comic_text_system` 必须覆盖 `dialogue / narration / inner_monologue / sfx` 四类，九页整体至少各出现一次。

## Root-Cause Execution Contract

若下游生成出九宫格拼图、九张近似变体、角色漂移、文本槽混乱或 JSON 无法被 3 号技能读取，必须按以下链路上溯：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

- 拼图/变体：先查 `generation_contract.hard_constraints`、`global_negative_prompt` 与 `references/nine-blade-prompt-contract.md`。
- 故事节奏失败：回 `steps/nine-blade-workflow.md` 的 `P1-G3/N2`。
- 角色/场景漂移：回 `references/` 的锁定规则与 `N3-CONTINUITY`。
- 风格断层或漫画感不足：回 `knowledge-base/comic-prompt-heuristics.md` 与 `N4A/N4B/N4G`。
- 文字槽或页码失败：回 `references/`、`templates/` 与 `scripts/validate_nine_blade_prompt_json.py`。
- mode 路由丢失：回 `steps/source-routing-and-handoff.md`。
- 题材类型包丢失：回 `types/type-map.md` 与命中包。
- 输出门禁缺失：回 `review/review-contract.md`。

Meta Rule Source：仓库 `AGENTS.md` 的 LLM-first creative authorship、Skill 2.0 分区 owner、脚本不得替代主创判断规则。
