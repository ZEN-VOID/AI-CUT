---
name: story-drafting
description: "Use when drafting, continuing, rewriting, or repairing story chapters from planning truth into canonical 3-初稿 prose."
governance_tier: full
---

# 3-初稿

`3-初稿` 是 `story2026` 的章节初稿完整技能包。根目录本身持有起草、续写、重写、局部修复、上下文装配、质量门禁和 canonical 写回合同。

用户给出外部执行偏好或当前会话直写时，仍进入本技能；执行环境只记入报告备注，不改变技能入口、frontmatter 或返工归属。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读 story 根层 `../SKILL.md` 与 `../CONTEXT.md`，先锁定 `story2026` 总线边界。
- 必须读取 `../_shared/context-loading-contract.md` 与 `../_shared/core-constraints.md`。
- 正式写作调用必须读取 `_shared/supervised-drafting-review-loop-contract.md`，并把项目 `team.yaml -> roles.production.members` 监制组、请教问题、回答摘要和可执行指导汇流为 `supervision_packet`；若真实 subagents 被阻断，必须记录降级报告。
- 若当前任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按当前卷/章相关性加载项目根 `CONTEXT/`。
- 必须读取三层 planning、`north_star.yaml` 的 `global_contract / style_contract / genre_contract`、对象卡和关系图谱；缺关键输入时不得凭记忆补写。
- 必须加载当前卷内所有已存在且早于目标章的前序正文。最近前章负责开章承接，其余前序章负责既成事实、线索、关系、道具、卷目标完成度、任务连续性、悬疑节奏和文气边界。
- 目标章已存在时必须先回读，再判定续写、重写或局部修复。

## Core Task Contract

本技能拥有：

- 当前章初稿写权：`projects/story/<项目名>/3-初稿/第N卷/第N章.md`
- 当前章初稿 frontmatter 与标题行格式裁决权
- 初稿上下文加载、监制包接入、正文作者性、内置自动验收与状态 hook 裁决权

本技能不拥有：

- `0-初始化`、`1-设定`、`2-卷章` 的真源改写权
- `return` 的 validated actualization 写回权
- 另建阶段子入口或并行正文真源的权力

## Business Requirement Analysis Contract

| slot | current requirement |
| --- | --- |
| `business_goal` | 将当前章 planning 与项目上下文转成可交付的中文小说候选正文。 |
| `business_object` | 当前章 planning、整体/卷级规划、north_star、对象卡、项目 MEMORY/CONTEXT、当前卷全部前序章、既有目标章。 |
| `constraint_profile` | planning 只能提供义务和约束，不得原样贴入正文；脚本不得生成创作正文。 |
| `success_criteria` | 初稿落到 `3-初稿/第N卷/第N章.md`，frontmatter 极简，正文具备现场发现、承接、推进、章末牵引，并自动生成通过的初稿验收包。 |
| `complexity_source` | 复杂度来自上游真源加载、同卷连续性、正文小说化转译、监制包吸收与写回安全。 |
| `topology_fit` | 单根技能包能避免阶段路由断链；节点按 source -> context -> supervision -> prose -> gate -> state 串行，适合章节级初稿。 |

## Input Contract

### Required Input

- 项目根：`projects/story/<项目名>/`
- 当前卷章定位：`volume_num / chapter_num`，或可由 `chapter_num` 推导卷号
- 三层 planning：
  - `2-卷章/整体规划.md`
  - `2-卷章/第N卷/卷规划.md`
  - `2-卷章/第N卷/第N章.md`
- 北极星：`0-初始化/north_star.yaml`，至少含 `global_contract / style_contract / genre_contract`
- 对象真源：角色、场景、物品、技能卡；存在 `1-设定/2-角色卡/角色关系图谱.md` 时必须加载

### Conditional Input

- `MEMORY.md` 与项目 `CONTEXT/`：项目存在时必须加载。
- 当前卷早于目标章的所有已存在初稿：存在时必须加载。
- 目标章既有正文：存在时必须回读，并要求用户意图能判定为 `chapter_continue / chapter_rewrite / local_repair`。
- 内置验收 finding、人工校阅意见或用户局部问题描述：进入 `local_repair` 时必须加载。

### Reject Or Block

- 缺少任一必需 planning、`north_star.yaml` 或关键对象真源。
- 用户要求脚本、模板、正则、规则拼接或启发式补写替代正文主创。
- 输出路径被要求写到平铺 `3-初稿/第N章.md`、`正文/`、临时 sibling 文件或历史子目录。
- 目标章已存在但用户没有授权续写、重写、覆盖或局部修复。

## Type Routing Matrix

| input_type | signal | route_to | required_nodes | module_load | fail_code |
| --- | --- | --- | --- | --- | --- |
| `chapter_draft` | 目标章不存在，用户要求起草/写正文 | 新章起草 | `N1,N2,N3,N4,N5,N6,N7` | `references/chapter-drafting-contract.md`, `templates/`, `review/review-contract.md` | `FAIL-DRAFT-TYPE` |
| `chapter_continue` | 目标章已存在，用户要求续写/补完 | 承接续写 | `N1,N2,N3,N4,N5,N6,N7` | `references/chapter-drafting-contract.md`, `types/type-map.md`, `review/review-contract.md` | `FAIL-DRAFT-CONTINUE` |
| `chapter_rewrite` | 目标章已存在，用户明确要求重写/覆盖 | 整章重写 | `N1,N2,N3,N4,N5,N6,N7` | `references/chapter-drafting-contract.md`, `guardrails/guardrails-contract.md`, `review/review-contract.md` | `FAIL-DRAFT-REWRITE` |
| `local_repair` | 用户或内置验收指出局部问题 | 局部修复 | `N1,N2,N3,N4,N5,N6,N7` | `references/chapter-drafting-contract.md`, `types/type-map.md`, `review/review-contract.md` | `FAIL-DRAFT-REPAIR` |
| `dry_run` | 只要求上下文包、检查或诊断 | 只装配不写回 | `N1,N2,N3,N7` | `types/type-map.md` | `FAIL-DRAFT-DRYRUN` |

## Thinking-Action Node Map

| node_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、卷章、任务模式和写回权限 | 解析用户意图、目标路径、既有章状态 | `task_profile`、`canonical_output_path` | `N2` | 项目根和卷章唯一 |
| `N2-SOURCE-LOCK` | 锁定上游真源 | 读取三层 planning、north_star、对象卡、关系图谱、MEMORY/CONTEXT | `source_manifest` | `N3` | 必需输入齐备 |
| `N3-CONTINUITY` | 建立同卷连续性桥 | 读取当前卷全部前序章，提炼事实、线索、关系、道具和章末压力 | `continuity_bridge` | `N4` | 前序章存在时必须列出实际路径 |
| `N4-SUPERVISION` | 汇流监制包 | 按项目 team roster 请教相关顾问，或记录降级 | `supervision_packet` / `degradation_note` | `N5` | 正式写作必须有其一 |
| `N5-CREATIVE-DRAFT` | LLM-first 创作正文 | 当前执行 LLM 按上下文逐条理解后写出完整小说 prose；脚本只可辅助读取/校验/落盘 | `draft_markdown`、`creative_engine_note` | `N6` | 禁止脚本主创和模板灌字 |
| `N6-AUTO-ACCEPTANCE` | 自动完成初稿验收 | 按内置九项验收检查 context、结构兑现、连续性、逻辑、人物、时间线、任务汇聚、文体读感/追读力、输出形态 | `stage_acceptance_packet`、`gate_result` | `N7` 或 `N5` | critical/high finding 必须返工 |
| `N7-WRITEBACK-STATE` | 写回与状态闭合 | 写入 canonical path 与验收包；记录 `workflow_manager.py record-skill-completion` 需求或执行结果 | `chapter_file`、`acceptance_file`、`state_hook_note` | done | 输出路径、验收落点和状态落点明确 |

## Module Loading Matrix

| module | load_when | authority | forbidden_use | rework_target |
| --- | --- | --- | --- | --- |
| `references/chapter-drafting-contract.md` | 任意正式起草、续写、重写或修复 | 展开章节正文硬规则和 review gate mapping | 不得新增阶段子入口或第二正文真源 | `N5-CREATIVE-DRAFT` |
| `types/type-map.md`、`types/网文/` | 判定任务模式、题材上下文或 dry-run | 辅助分型和上下文包选择 | 不得替代 `Type Routing Matrix`，不得生成平行草稿 | `N1-INTAKE` |
| `review/review-contract.md` | 写回前、内置验收、返工或审计 | 给出阶段内自动验收维度、fail code 和返工目标 | 不得外包给独立 `story/review` 技能或另写父层 aggregate | `N6-AUTO-ACCEPTANCE` |
| `templates/` | 需要输出骨架或系统提示 | 约束 frontmatter、标题和 prose 输出形态 | 不得生成正文内容 | `N5-CREATIVE-DRAFT` |
| `guardrails/guardrails-contract.md` | 覆盖、重写、修复、外部输入复杂时 | 约束权限、注入防护和写回边界 | 不得覆盖本 `SKILL.md` | `N6-AUTO-ACCEPTANCE` |
| `knowledge-base/drafting-heuristics.md` | 需要可复用写作经验时 | 提供经验参考 | 不得成为执行指令源 | `N5-CREATIVE-DRAFT` |

## LLM-First Creative Authorship Contract

- 核心正文必须由 LLM 逐条理解目标对象、上下文和用户意图后直接创作。
- 不能用脚本做批量生成、批量插入、正则套句、映射投影、模板灌字或启发式补写。
- 脚本只允许承担读取、统计、校验、diff、路径检查、状态 hook 和落盘辅助。
- 新产物默认不写 `写作模型`；旧稿中已有 `写作模型` 字段时，仅作为 legacy metadata 读取，不得参与路由或返工归属裁决。
- 若用户提出执行环境偏好，仍由本技能执行；最终报告只记录执行备注，不新建分支入口。

## Core Gates

- frontmatter 新格式只保留 `创作阶段: 初稿` 与 `字数: XXX字`；不得把 planning、cards、项目上下文、执行环境或 sidecar 路径灌入 YAML。
- 标题格式为 `# 第N章｜章标题`。
- 正文主体必须是中文小说 prose，不得把 planning 标题、任务线、规避条目或执行术语贴成正文。
- 每章至少出现一个“现场发现”：由物件、声音、气味、身体动作、空间阻隔、误触、沉默或环境反作用自然生成，并推动人物反应、信息揭示、关系压力或章末牵引。
- 正文必须保持叙事内视角，不得出现 `上一章`、`本章`、`planning`、`frontmatter`、`sidecar`、`supervision_packet` 等执行层标签。
- 情绪不得默认落到脸色颜色变化；避免“脸红/脸白/脸色惨白/脸色大变”等模板化捷径，改用动作、呼吸、手部细节、视线、物件误触、话语断裂或空间退让。
- 输出路径固定为 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`。
- 单章完成必须同步生成初稿 `stage_acceptance_packet`；该验收通过后才可进入 `4-润色`，但仍不代表可被 `return` actualize。

## Built-in Acceptance Contract

本技能不依赖 `.agents/skills/story/review`。正式写作任务在 `N5-CREATIVE-DRAFT` 后必须自动执行 `N6-AUTO-ACCEPTANCE`，不得把验收变成用户另行触发的步骤。

验收输出默认写入：

```text
projects/story/<项目名>/3-初稿/第N卷/第N章.acceptance.json
```

`stage_acceptance_packet` 至少包含：`acceptance_status`、`accepted_manuscript_stage`、`accepted_manuscript_refs`、`dimension_results`、`critical_issues`、`rework_targets`、`handoff_targets`、`acceptance_ref`。初稿通过时 `handoff_targets` 应包含 `4-润色`；不得包含 `return`。

### Draft Acceptance Dimensions

| dimension | required check | fail_code | rework_target |
| --- | --- | --- | --- |
| `source_context` | story 根、项目 MEMORY/CONTEXT、三层 planning、north_star、对象真源和监制包已加载 | `FAIL-DRAFT-CONTEXT` | `N2-SOURCE-LOCK` / `N4-SUPERVISION` |
| `structure_realization` | 本章 planning 的事件、冲突、任务、线索和伏笔义务被写成戏，而不是摘要式提到 | `FAIL-DRAFT-STRUCTURE` | `N5-CREATIVE-DRAFT` |
| `continuity` | 同卷前文的事实、关系、道具、压力线和章末余波被承接，关键转场有自然牵引 | `FAIL-DRAFT-CONTINUITY` | `N3-CONTINUITY` / `N5-CREATIVE-DRAFT` |
| `logic_self_consistency` | 因果链、能力边界、世界规则、例外代价和 source truth 不冲突 | `FAIL-DRAFT-LOGIC` | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` |
| `character_consistency` | 人物行为、动机、关系压力、成长承接、对白声口和社会身份语言成立 | `FAIL-DRAFT-CHARACTER` | `N5-CREATIVE-DRAFT` |
| `timeline` | 时间锚、事件顺序、持续时长和伏笔静默窗口不越线 | `FAIL-DRAFT-TIMELINE` | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` |
| `task_convergence` | 章级任务从属于卷级任务，支流任务有汇聚、转挂或显式开放 | `FAIL-DRAFT-TASK` | `N5-CREATIVE-DRAFT` |
| `prose_reader_pull` | 中文小说 prose 有现场感、句群起伏、对白潜台词、心理暗流、读者牵引和章末钩子；无明显 AI 腔、模板脸色和执行标签 | `FAIL-DRAFT-PROSE-PULL` | `N5-CREATIVE-DRAFT` |
| `output_state` | frontmatter、标题、canonical path、验收包和状态 hook 正确 | `FAIL-DRAFT-WRITEBACK` | `N7-WRITEBACK-STATE` |

## Convergence Contract

| convergence_point | pass_condition | fail_condition | evidence | rework_target |
| --- | --- | --- | --- | --- |
| source lock | 必需 truth 齐备且路径明确 | 缺 planning/north_star/对象真源 | `source_manifest` | `N2-SOURCE-LOCK` |
| prose draft | 输出为完整章节 prose | 摘要、提纲、过程说明、模板占位 | `draft_markdown` | `N5-CREATIVE-DRAFT` |
| automatic acceptance | `acceptance_status=PASS` 且 critical/high finding 为 0 | 结构未兑现、连续性断带、逻辑冲突、人物失真、时间错位、任务悬空、读感弱或输出形态错误 | `stage_acceptance_packet` | `N5` / `N6` |
| writeback | canonical path 和验收包写回且状态 hook 有记录或阻断说明 | 写到旧路径、临时路径、无验收包或状态无落点 | `chapter_file`、`acceptance_file`、`state_hook_note` | `N7-WRITEBACK-STATE` |

## Review Gate Binding

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否加载 story 根、项目 MEMORY/CONTEXT、三层 planning、north_star 与对象真源？ | `context_loading` | `FAIL-DRAFT-CONTEXT` | `N2-SOURCE-LOCK` | `source_manifest` |
| 是否把 planning 义务写成戏剧事件而非摘要提到？ | `structure_realization` | `FAIL-DRAFT-STRUCTURE` | `N5-CREATIVE-DRAFT` | obligation evidence |
| 同卷前文存在时是否完整加载并形成连续性桥？ | `continuity` | `FAIL-DRAFT-CONTINUITY` | `N3-CONTINUITY` | `previous_chapter_refs` |
| 因果、规则、能力、时间和任务是否成立？ | `logic_timeline_task` | `FAIL-DRAFT-LOGIC` / `FAIL-DRAFT-TIMELINE` / `FAIL-DRAFT-TASK` | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` | issue map |
| 人物行为、动机、关系和声口是否一致？ | `character_consistency` | `FAIL-DRAFT-CHARACTER` | `N5-CREATIVE-DRAFT` | character evidence |
| 正文是否由 LLM-first 主创，而非脚本/模板生成？ | `creative_authorship` | `FAIL-DRAFT-AUTHORSHIP` | `N5-CREATIVE-DRAFT` | `creative_engine_note`、script audit |
| 正文是否是有现场感、读者牵引和章末钩子的小说 prose，且没有 execution labels？ | `prose_reader_pull` | `FAIL-DRAFT-PROSE-PULL` | `N5-CREATIVE-DRAFT` | offending excerpt |
| 输出是否符合 frontmatter、标题、canonical path 与验收包要求？ | `output_shape` | `FAIL-DRAFT-WRITEBACK` | `N6-AUTO-ACCEPTANCE` / `N7-WRITEBACK-STATE` | parsed file summary |

## Output Contract

| field | contract |
| --- | --- |
| Required output | 当前章完整中文小说初稿 Markdown 文件。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节正文；frontmatter 至少包含 `创作阶段: 初稿` 与 `字数: XXX字`。 |
| Output path | 正文：`projects/story/<项目名>/3-初稿/第N卷/第N章.md`；验收包：`projects/story/<项目名>/3-初稿/第N卷/第N章.acceptance.json`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | 输入真源齐备；LLM-first 主创完成；内置自动验收通过；写回 canonical path 和验收包；已记录或说明 `record-skill-completion` 状态 hook。 |
| State gate | 使用 `--skill-id story-drafting`，并在 artifacts 中记录当前章正文路径与验收包路径。 |

## Learning / Context Writeback

- 新失败模式、修复打法和高复用启发写回同目录 `CONTEXT.md`。
- 稳定规则再晋升到本 `SKILL.md`、`references/`、`review/` 或 `templates/`。
- 不把执行环境偏好写成路由规则；如确需说明，只能作为报告备注或经验记录。
