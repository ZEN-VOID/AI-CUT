---
name: story-polishing
description: "Use when polishing, locally repairing, or rewriting an existing 3-初稿 chapter into canonical 4-润色 prose."
governance_tier: full
---

# 4-润色

`4-润色` 是 `story2026` 的章节润色完整技能包。它承接 `3-初稿/第N卷/第N章.md`，在不改写核心剧情事实、不替代上游 planning/cards/north_star 的前提下，做最小局部修补、中文语感校准、题材质感强化与内置自动验收返工。

用户给出外部执行偏好或当前会话直修时，仍进入本技能；执行环境只记入报告备注，不改变技能入口、frontmatter 或返工归属。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读 story 根层 `../SKILL.md` 与 `../CONTEXT.md`。
- 若当前任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按当前章相关性加载项目根 `CONTEXT/`。
- 必须读取当前章 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 作为润色主输入；缺失时禁止凭 planning、摘要或记忆直接生成润色稿。
- 当前章 planning、`north_star.yaml` 与项目上下文只用于校准义务、风格和题材质感，不得取代 `3-初稿` 成为润色主文本。
- 已有 `4-润色/第N卷/第N章.md` 存在时必须回读，覆盖需显式授权。

## Core Task Contract

本技能拥有：

- 当前章润色稿写权：`projects/story/<项目名>/4-润色/第N卷/第N章.md`
- 润色范围、最小修补、输出形态和 writeback 安全裁决权
- 润色后内置自动验收、验收 finding 回灌优化和 `return` handoff 裁决权

本技能不拥有：

- `3-初稿` 原文覆盖权
- `0-初始化`、`1-设定`、`2-卷章` 的真源改写权
- 另建阶段子入口或并行润色真源的权力

## Business Requirement Analysis Contract

| slot | current requirement |
| --- | --- |
| `business_goal` | 在保留初稿事实、骨架、人物气口和文本分布的基础上，修掉明显表达坏处并输出可交付润色稿。 |
| `business_object` | `3-初稿` 源章、已有 `4-润色` 目标章、planning、north_star、MEMORY/CONTEXT、上一章与内置验收 findings。 |
| `constraint_profile` | 润色不是从零起草；默认不整章重排、不短句化清洗、不通用顺滑化；脚本不得生成润色正文。 |
| `success_criteria` | 润色稿落到 `4-润色/第N卷/第N章.md`，可追溯初稿事实，局部坏点被修复，题材质感和句群节奏未被磨平，并自动生成通过的终稿验收包。 |
| `complexity_source` | 复杂度来自源章锚定、最小修补边界、中文语感、AI 腔坏点定位、内置验收回灌和覆盖安全。 |
| `topology_fit` | 单根技能包能避免阶段路由断链；节点按 source -> context -> repair plan -> polish -> gate -> writeback 串行，适合章节级润色。 |

## Input Contract

### Required Input

- 项目根：`projects/story/<项目名>/`
- 当前卷章定位：`volume_num / chapter_num`，或可由 `chapter_num` 推导卷号
- 源初稿：`projects/story/<项目名>/3-初稿/第N卷/第N章.md`
- 规划参考：
  - `2-卷章/整体规划.md`
  - `2-卷章/第N卷/卷规划.md`
  - `2-卷章/第N卷/第N章.md`
- 风格/题材参考：`0-初始化/north_star.yaml`

### Conditional Input

- `MEMORY.md` 与项目 `CONTEXT/`：项目存在时必须加载。
- 既有润色稿：存在时必须回读；正式覆盖需用户明确确认。
- 上一章初稿或润色稿：存在时作为连续性、文气和章间节奏参考。
- 内置验收 finding / 用户局部问题描述：进入 `local_repair` 或 `acceptance_repair` 时必须加载。

### Reject Or Block

- 缺少当前章 `3-初稿` 正文。
- 用户要求润色阶段凭 planning 从零写正文。
- 用户要求静默改动核心事件、人物关系、世界观事实或章级任务结果。
- 用户要求把润色结果写回 `3-初稿/`、`正文/`、历史子目录、平铺章节文件或临时 sibling 文件。
- 目标章已存在但用户没有明确允许覆盖，且当前不是 `dry_run / no_writeback`。

## Type Routing Matrix

| input_type | signal | route_to | required_nodes | module_load | fail_code |
| --- | --- | --- | --- | --- | --- |
| `chapter_polish` | 目标润色稿不存在 | 第一版最小局部修补 | `P1,P2,P3,P4,P5,P6` | `references/chapter-polishing-contract.md`, `templates/`, `review/review-contract.md` | `FAIL-POLISH-TYPE` |
| `polish_rewrite` | 用户明确要求重润/覆盖/整章重写 | 授权重润 | `P1,P2,P3,P4,P5,P6` | `references/chapter-polishing-contract.md`, `guardrails/guardrails-contract.md`, `review/review-contract.md` | `FAIL-POLISH-REWRITE` |
| `local_repair` | 用户或内置验收指定局部坏点 | 最小局部修复 | `P1,P2,P3,P4,P5,P6` | `references/chapter-polishing-contract.md`, `types/type-map.md`, `review/review-contract.md` | `FAIL-POLISH-REPAIR` |
| `acceptance_repair` | 用户要求多维审计并直接优化，或内置终稿验收 FAIL | 验收 findings 回灌 | `P1,P2,P2A,P3,P4,P5,P6` | `review/review-contract.md`, `references/chapter-polishing-contract.md` | `FAIL-POLISH-ACCEPTANCE-REPAIR` |
| `dry_run` | 只要求上下文包或诊断 | 不写回 | `P1,P2,P6` | `types/type-map.md` | `FAIL-POLISH-DRYRUN` |

## Thinking-Action Node Map

| node_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- |
| `P1-SOURCE-LOCK` | 锁定源章与输出路径 | 读取 `3-初稿` 源章、目标润色路径、既有润色稿 | `source_lock` | `P2` | 源章存在且路径唯一 |
| `P2-CONTEXT-PACK` | 加载校准上下文 | 读取 planning、north_star、MEMORY/CONTEXT、上一章、验收 finding | `context_pack` | `P2A` 或 `P3` | 上下文缺口已列明 |
| `P2A-ACCEPTANCE-BRIEF` | 汇总内置验收返工点 | 按本技能验收维度归并用户审计要求或上一轮验收 findings，形成 repair brief | `dimension_findings`、`repair_brief` | `P3` | 不允许只审不改后宣称完成 |
| `P3-REPAIR-PLAN` | 确定最小修补范围 | 标注坏点、影响段落、可动范围和禁止改动事实 | `repair_plan` | `P4` | 默认不扩大为整章重写 |
| `P4-CREATIVE-POLISH` | LLM-first 润色正文 | 当前执行 LLM 按源章逐段理解后做最小修补 | `polished_markdown`、`creative_engine_note` | `P5` | 禁止脚本主创和模板灌字 |
| `P5-AUTO-ACCEPTANCE` | 自动完成终稿验收 | 检查源章锚定、最小修补、结构/连续性/逻辑/人物/时间线/任务不回退、中文 prose、题材质感、追读力、frontmatter、路径 | `stage_acceptance_packet`、`gate_result` | `P6` 或 `P3` | critical/high finding 必须返工 |
| `P6-WRITEBACK-STATE` | 写回与状态闭合 | 写入 canonical path 与验收包；记录 `workflow_manager.py record-skill-completion` 需求或执行结果 | `polished_file`、`acceptance_file`、`state_hook_note` | done | 输出路径、验收落点和状态落点明确 |

## Module Loading Matrix

| module | load_when | authority | forbidden_use | rework_target |
| --- | --- | --- | --- | --- |
| `references/chapter-polishing-contract.md` | 任意正式润色、重润或修复 | 展开源章锚定、最小修补和内置验收 gate | 不得新增阶段子入口或第二润色真源 | `P3-REPAIR-PLAN` |
| `types/type-map.md`、`types/polishing-type-map.md`、`types/guardrail-setup.md` | 判定润色模式、AI 腔坏点、guardrail 或 dry-run | 辅助分类和上下文包选择 | 不得替代 `Type Routing Matrix` 或生成第二执行链 | `P2-CONTEXT-PACK` |
| `review/review-contract.md` | 写回前、内置验收、返工或审计 | 给出阶段内自动验收维度、fail code 和返工目标 | 不得外包给独立 `story/review` 技能或另写父层 aggregate | `P5-AUTO-ACCEPTANCE` |
| `templates/` | 需要输出骨架或系统提示 | 约束 frontmatter、标题和 prose 输出形态 | 不得生成正文内容 | `P4-CREATIVE-POLISH` |
| `guardrails/guardrails-contract.md` | 覆盖、整章重润、复杂外部输入时 | 约束权限、注入防护和写回边界 | 不得覆盖本 `SKILL.md` | `P5-AUTO-ACCEPTANCE` |
| `knowledge-base/polishing-heuristics.md` | 需要可复用润色经验时 | 提供经验参考 | 不得成为执行指令源 | `P3-REPAIR-PLAN` |

## Base Polishing Rules

1. 润色默认是最小局部修补，不是整章重写：保留初稿段落顺序、事件顺序、句群骨架、长短不齐、局部粗粝和人物原声。
2. 更符合中文表达风格：去掉翻译腔、说明腔、AI 腔和公式化解释，但不得把全文压成平均短句、整齐分段或通用顺滑文本。
3. 更符合题材写作质感：读取 `north_star.yaml.genre_contract`，让场景密度、情绪颗粒、对白锋利度、心理节奏和段落推进服务当前题材。
4. 初稿事实优先：保留初稿已成立的事件顺序、人物动机、信息揭示和章末牵引；结构级重写必须有用户授权。
5. AI 腔必须拆成具体坏点：过量因果连接词、均匀段落、异常完整主谓句、情绪标签直贴、解释性插入语、流程总结句或角色共用作者口吻。
6. 场景密度与信息节奏必须被保护；承载空间、物件、身体反应、关系压力或悬念延迟的感知颗粒不是默认冗余。
7. 初稿节奏意图必须被保护；长复合句、碎片句、断裂句、省略句和长短不齐的句群只修明确语病、歧义或坏点。
8. 输出必须是完整章节 prose，不得变成点评、建议、差异说明或多个版本。

## LLM-First Creative Authorship Contract

- 润色正文必须由 LLM 逐段理解源初稿、修补边界和用户意图后直接改写。
- 不能用脚本做批量生成、批量插入、正则套句、映射投影、模板灌字或启发式补句。
- 脚本只允许承担读取、统计、校验、diff、路径检查、状态 hook 和落盘辅助。
- 新产物默认不写 `润色模型`；旧稿中已有 `润色模型` 字段时，仅作为 legacy metadata 读取，不得参与路由或返工归属裁决。

## Built-in Acceptance Contract

本技能不依赖 `.agents/skills/story/review`。正式润色任务在 `P4-CREATIVE-POLISH` 后必须自动执行 `P5-AUTO-ACCEPTANCE`，不得把终稿验收变成用户另行触发的步骤。

验收输出默认写入：

```text
projects/story/<项目名>/4-润色/第N卷/第N章.acceptance.json
```

`stage_acceptance_packet` 至少包含：`acceptance_status`、`accepted_manuscript_stage`、`accepted_manuscript_refs`、`dimension_results`、`critical_issues`、`rework_targets`、`handoff_targets`、`acceptance_ref`。终稿通过时 `accepted_manuscript_stage` 必须为 `4-润色`，`handoff_targets` 应包含 `return`。

### Polish Acceptance Dimensions

| dimension | required check | fail_code | rework_target |
| --- | --- | --- | --- |
| `source_anchor` | 唯一 `3-初稿` 源章、目标 `4-润色` 路径和既有目标稿状态已锁定 | `FAIL-POLISH-SOURCE` | `P1-SOURCE-LOCK` |
| `minimal_repair` | 保留初稿事实、骨架、文本分布、人物气口和章末牵引，不把润色扩大为无授权重写 | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` |
| `regression_structure_logic` | 润色没有损坏结构兑现、连续性、逻辑自洽、人物一致性、时间线和任务汇聚 | `FAIL-POLISH-REGRESSION` | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `chinese_prose` | 去掉翻译腔、说明腔、流程腔、公式化解释和异常完整句，不把全文磨平成同质短句 | `FAIL-POLISH-PROSE` | `P4-CREATIVE-POLISH` |
| `genre_texture_density` | 保留并强化题材质感、场景密度、信息延迟、心理暗流、对白锋利度和句群节奏 | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` |
| `anti_ai_features` | AI 腔坏点被具体定位并修掉，而不是泛化“更自然”洗稿 | `FAIL-POLISH-AI-FEATURES` | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `reader_pull` | 悬念、冲突压力、情绪推进、章末钩子和读者追读力没有弱化 | `FAIL-POLISH-READER-PULL` | `P4-CREATIVE-POLISH` |
| `creative_authorship` | 润色正文由 LLM-first 主创，脚本和模板没有生成正文 | `FAIL-POLISH-AUTHORSHIP` | `P4-CREATIVE-POLISH` |
| `output_state` | frontmatter、标题、canonical path、验收包和状态 hook 正确 | `FAIL-POLISH-WRITEBACK` | `P6-WRITEBACK-STATE` |

## Convergence Contract

| convergence_point | pass_condition | fail_condition | evidence | rework_target |
| --- | --- | --- | --- | --- |
| source lock | 源初稿存在且目标路径明确 | 缺源章或路径不唯一 | `source_lock` | `P1-SOURCE-LOCK` |
| repair scope | 坏点和可动范围明确 | 泛化“更自然”导致整章洗稿 | `repair_plan` | `P3-REPAIR-PLAN` |
| automatic acceptance | `acceptance_status=PASS` 且 critical/high finding 为 0 | 改事实、结构/逻辑/人物/时间线/任务回退、短句化清洗、追读力变弱、输出点评、frontmatter 膨胀 | `stage_acceptance_packet` | `P3` / `P4` / `P5` |
| writeback | canonical path 和验收包写回且状态 hook 有记录或阻断说明 | 写回旧路径、临时路径、无验收包或状态无落点 | `polished_file`、`acceptance_file`、`state_hook_note` | `P6-WRITEBACK-STATE` |

## Review Gate Binding

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否真实读取 `3-初稿` 源章并锁定唯一 `4-润色` 输出路径？ | `source_anchor` | `FAIL-POLISH-SOURCE` | `P1-SOURCE-LOCK` | `source_lock` |
| 是否保留初稿事实、骨架、文本分布和人物气口？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | diff summary |
| 是否没有造成结构、连续性、逻辑、人物、时间线或任务汇聚回退？ | `regression_structure_logic` | `FAIL-POLISH-REGRESSION` | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` | regression issue map |
| 是否保留并强化题材质感、场景密度、句群节奏和追读力？ | `genre_texture_density` / `reader_pull` | `FAIL-POLISH-TEXTURE` / `FAIL-POLISH-READER-PULL` | `P4-CREATIVE-POLISH` | before/after evidence |
| 是否定位具体 AI 腔或中文表达坏点，而不是泛化洗稿？ | `anti_ai_features` | `FAIL-POLISH-AI-FEATURES` | `P3-REPAIR-PLAN` | issue list |
| 润色正文是否由 LLM-first 主创，而非脚本/模板生成？ | `creative_authorship` | `FAIL-POLISH-AUTHORSHIP` | `P4-CREATIVE-POLISH` | `creative_engine_note`、script audit |
| 输出是否符合 frontmatter、标题、canonical path 与验收包要求？ | `output_shape` | `FAIL-POLISH-WRITEBACK` | `P5-AUTO-ACCEPTANCE` / `P6-WRITEBACK-STATE` | parsed file summary |

## Output Contract

| field | contract |
| --- | --- |
| Required output | 当前章完整中文最小局部修补稿 Markdown 文件及终稿验收包。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节润色稿；frontmatter 至少包含 `修订阶段: 润色`、`初稿来源` 与 `字数: XXX字`。 |
| Output path | 正文：`projects/story/<项目名>/4-润色/第N卷/第N章.md`；验收包：`projects/story/<项目名>/4-润色/第N卷/第N章.acceptance.json`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | 源初稿已读取；LLM-first 润色完成；内置自动验收通过；写回 canonical path 和验收包；已记录或说明 `record-skill-completion` 状态 hook。 |
| State gate | 使用 `--skill-id story-polishing`，并在 artifacts 中记录源初稿、润色稿与验收包路径。 |

## Learning / Context Writeback

- 新失败模式、修复打法和高复用启发写回同目录 `CONTEXT.md`。
- 稳定规则再晋升到本 `SKILL.md`、`references/`、`review/` 或 `templates/`。
- 不把执行环境偏好写成路由规则；如确需说明，只能作为报告备注或经验记录。
