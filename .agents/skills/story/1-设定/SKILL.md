---
name: story-cards
governance_tier: lite
skill_role: parent_guide
description: "Use when routing story card generation for characters, scenes, items, or skills."
tools: [Read, Write, Edit, Grep, Bash]
color: amber
---

# 1-设定

## Role

`1-设定` 是 `story2026` 的对象设定技能组导引层。

它负责判断本轮应该进入哪些对象子技能、以什么顺序执行、如何回读项目上下文、如何把子技能产物写回项目设定根并完成 gate。它不直接代替子技能做角色、场景或物品的创作判断。

`全局设定 / 整书风格 / 类型方向盘` 不再作为 `1-设定` 下的独立子技能或独立卡册存在；它们的正式真源统一融合进 `projects/story/<项目名>/0-初始化/north_star.yaml`：

- `global_contract`：世界观、规则体系、时代约束、文化艺术、势力拓扑、力量/科技、金手指。
- `style_contract`：整体风格身份、阅读体验、叙事/对白/画面/文体/场面写法与风格 gate。
- `genre_contract`：读者承诺、题材走廊、禁飞区、导航规则与 planning 投影。

一句话边界：

- 父层管路由、依赖、写回、验证与闭环。
- 子技能管各自对象的创作判断、字段成立条件与正式 card payload。
- 脚本只做读取、校验、落盘、统计等机械辅助，不得替代 LLM 主创。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按需读取项目根 `CONTEXT/` 中与本轮 cards 相关的材料。
- 若本阶段或命中子技能显式要求启用 subagents，必须读取项目根 `team.yaml` 与 `../_shared/team-advisor-consultation-contract.md`；优先调用 `roles.planning.members` 中已指定成员作为资深创作顾问，按对象域提出具体请教问题，并在子技能 LLM 创作前形成 `advisor_consultation_packet` 作为额外重要上下文。
- 进入任一子技能前，必须加载该子技能自己的 `SKILL.md + CONTEXT.md`。
- 根级 `CONTEXT.md` 只提供 cards 技能组经验与返工启发，不得覆盖本文件的路由、所有权与 gate。

## Skill Group Members

| 子技能 | 负责对象 | 正式输出根 |
| --- | --- | --- |
| `角色卡` | 角色对象真源、关系、成长、专属物接口、关系图谱 | `1-设定/2-角色卡/**/*.json` + `角色关系图谱.md` |
| `场景卡` | 场景功能、规则、危险、角色适配、复用策略 | `1-设定/3-场景卡/**/*.json` |
| `物品卡` | 武器、线索、遗物、重要叙事物、归属链、代价、专属适配 | `1-设定/4-物品卡/**/*.json` |
| `技能卡` | 科技、法术、武功、作战技能、生活才艺、职业技能等广义能力对象 | `1-设定/5-技能卡/**/*.json` |

硬边界：

1. 四个成员都是直连 child skills；父层不得把它们重新压回根层 `references/` 或根层 `templates/`。
2. 对象私有模板、字段映射、步骤和审查规则归子技能包本地所有。
3. 父层只聚合被实际调度的子技能产物，不为未调度子技能补空字段或占位稿。
4. 角色、场景、物品、技能存在强依赖：`角色卡 -> 场景卡 -> 物品卡 -> 技能卡`。
5. `north_star.yaml` 是 planning 默认题材方向盘与 drafting/validation 默认写法 gate；`1-设定` 只消费，不复制。

## Mode Selection

| request_shape | 父层动作 | 调度策略 |
| --- | --- | --- |
| 单一对象请求 | 只进入命中的一个子技能 | 可单独执行 |
| 多个独立对象修复 | 只进入命中的子技能 | 无真实依赖时可并行；同一写回目标要串行收束 |
| `mixed` 建卡 | 进入多个子技能并聚合 | `角色卡 -> 场景卡 -> 物品卡 -> 技能卡` |
| `full-build` | 全量建卡并完成 gate | 固定按 mixed 顺序串行推进 |
| coverage repair | 先读 validator finding，再进入相关子技能 | 只修 blocking finding 指向的对象 |
| source-contract-fix | 修父子合同、模板、writer、validator、tests 的一致性 | 先修真源层，再跑局部 gate |

## Routing Guide

| 用户诉求关键词 | 目标子技能 | 路由说明 |
| --- | --- | --- |
| 世界、规则、年代、文化、势力、武功、科技、金手指 | `0-初始化/north_star.yaml` | 不进入 `1-设定` 子技能；修 `global_contract` |
| 题材、类型、读者承诺、平台感、禁飞区、爽点/虐点边界 | `0-初始化/north_star.yaml` | 不进入 `1-设定` 子技能；修 `genre_contract` |
| 气质、文风、对白、镜头感、叙事口吻、语言节奏 | `0-初始化/north_star.yaml` | 不进入 `1-设定` 子技能；修 `style_contract` |
| 人物、关系、成长、伤口、欲望、专属物接口 | `角色卡` | 人物对象真源和关系网络 |
| 地点、空间、危险、规矩、常驻场、返场价值 | `场景卡` | 可写戏空间与规则压力 |
| 武器、道具、线索、遗物、钥匙、代价、归属 | `物品卡` | 剧情杠杆和使用成本 |
| 技能、能力、科技、法术、武功、枪械、格斗、战术、厨艺、才艺、职业技能 | `技能卡` | 可成长、可使用、可失败、可克制的能力对象 |

若请求同时命中多个对象，优先用依赖链判断顺序，而不是按技能目录名称判断。

## Input Contract

- Accepted input: 角色卡、场景卡、物品卡、技能卡生成/修复/覆盖率修复，或父子 card 合同、writer、validator、模板一致性修复。
- Required input: 项目根 `projects/story/<项目名>/`，本轮对象范围，或能定位到具体 child skill 的卡片修复 finding。
- Optional input: `0-初始化/north_star.yaml`、`MEMORY.md`、项目 `CONTEXT/`、既有 `1-设定/**/*.json`、coverage 报告。
- Reject or reroute when: 全局设定、整书风格、题材方向盘请求应回到 `0-初始化/north_star.yaml`；章节规划和正文写作不得由本阶段直接产出。

## Shared Runtime Contract

正式写回和验证默认经由共享脚本辅助完成：

- `.agents/skills/story/scripts/cards_writer.py`
- `.agents/skills/story/scripts/cards_coverage_validator.py`
- `.agents/skills/story/scripts/story.py`

脚本职责仅限机械流程：

- 读取项目输入与既有 cards
- 投影子技能产出的结构化 payload
- 原子写入 JSON / Markdown side output
- 校验 schema、trace、数量、密度与 route parity
- 生成 gate 报告

脚本不得生成核心创作正文、审美判断、故事判断或对象成立理由。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 父层路由与依赖 | 本文件 `Mode Selection`、`Shared Runtime Contract` 与 `CONTEXT.md` |
| 角色对象 | `角色卡/SKILL.md`、`角色卡/CONTEXT.md`、`角色卡/references/`、`角色卡/templates/` |
| 场景对象 | `场景卡/SKILL.md`、`场景卡/CONTEXT.md`、`场景卡/references/`、`场景卡/templates/` |
| 物品对象 | `物品卡/SKILL.md`、`物品卡/CONTEXT.md`、`物品卡/references/`、`物品卡/templates/` |
| 技能对象 | `技能卡/SKILL.md`、`技能卡/CONTEXT.md`、`技能卡/references/`、`技能卡/templates/` |
| 父层判型 | 本文件 `Mode Selection` 与 `CONTEXT.md` Type Map |
| 显式启用 subagents / team advisor consultation | `../_shared/team-advisor-consultation-contract.md`，由命中子技能实际消费 |
| 父层门禁 | `cards_coverage_validator.py` 与子技能 `review/` |
| 经验层 | `CONTEXT.md` |
| 输出摘要 | 对话或用户指定 `reports/` 路径 |
| 机械写回/校验 | 共享 `.agents/skills/story/scripts/cards_writer.py` 与 `cards_coverage_validator.py` |
| 产品侧入口 | `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml` |
| 父级导引最小结构 | 本父级导引 skill 只要求同目录 `SKILL.md + CONTEXT.md`；对象模板、类型包、局部 review 和字段细则归 `角色卡/`、`场景卡/`、`物品卡/` 子技能 |

## Canonical Output Root

正式业务输出只允许落在：

```text
projects/story/<项目名>/1-设定/
├── 2-角色卡/
├── 3-场景卡/
├── 4-物品卡/
└── 5-技能卡/
```

禁止把技能目录、临时 sidecar、报告目录或 repo 根层模板当成项目 card 真源。
禁止再新建 `0-全局卡 / 1-风格卡 / 5-类型卡` 作为正式设定输出；旧项目遗留目录只可兼容回读或一次性迁移到 `north_star.yaml`。

## Operating Flow

1. 锁定项目根、任务模式与输入范围。
2. 加载本 `SKILL.md + CONTEXT.md`、项目 `MEMORY.md` 与相关项目 `CONTEXT/`。
3. 根据请求路由到一个或多个子技能。
4. 对每个命中子技能加载其 `SKILL.md + CONTEXT.md`，再按其合同读取本地模板、references、steps、review 或 types。
5. 当启用 subagents 时，按共享团队顾问合同解析 `team.yaml` planning roster，针对命中对象域请教顾问并形成 `advisor_consultation_packet`；若真实 dispatch 被上层阻断，记录阻断层级、原计划路径、实际降级路径和未启动成员。
6. 由 LLM 完成对象判断与 payload 创作，并消费已裁决的 `advisor_consultation_packet`；脚本只负责投影、落盘或校验。
7. 经 shared writer 写回正式输出根。
8. 经 coverage validator / cards-check 完成 gate。
9. gate 通过或失败结论明确后，调用 `workflow_manager.py record-skill-completion` 同步项目状态；子技能单独执行时也必须记录对应 `skill-id`。
10. 若失败，按 finding 指向回到父层路由、子技能合同、模板、writer、validator 或 card 内容中最窄的真实根因。

## Quality Gates

| gate | 通过条件 |
| --- | --- |
| 路由 gate | 请求命中对象与子技能 owner 一致；全局/风格/类型请求转回 `north_star.yaml` |
| 上下文 gate | 父层、项目记忆、相关项目上下文、命中子技能上下文已加载 |
| 创作权 gate | 核心 card 判断来自 LLM，不来自脚本拼接 |
| 顾问请教 gate | 显式启用 subagents 时已按 `team.yaml` 请教 planning 顾问并形成可执行 `advisor_consultation_packet`；阻断时有降级报告 |
| trace gate | payload 标记的 `source_skill_id / module_route / loaded_references` 与实际调度一致 |
| schema gate | 输出 JSON 符合对应子技能本地模板 |
| dependency gate | 物品卡没有绕过角色接口与场景规则；技能卡没有绕过世界规则、角色成长、场景限制与物品媒介 |
| coverage gate | 数量、结构、密度、规则刚性和 route parity 通过验证 |

## Root-Cause Execution Contract

非平凡问题必须沿链路上溯：

`Symptom -> Direct Cause -> Source Layer -> Rule Source -> Fix Landing Point`

修复落点优先级：

1. 父层路由、依赖和写回 gate。
2. 子技能 `SKILL.md + CONTEXT.md` 合同。
3. 子技能本地模板、steps、review、types。
4. writer / validator / tests 的运行时一致性。
5. 单张 card 内容。

最终反馈应收束为：

- 根因位置
- 已修复内容
- 验证结果
- 仍需用户裁决的创作选择

## Field Mapping

| field_id | owner | required_output | fail_code |
| --- | --- | --- | --- |
| `FIELD-CARDS-ROUTE` | 父层路由 | 命中的 child skill 列表与执行顺序 | `FAIL-CARDS-ROUTE` |
| `FIELD-CARDS-CONTEXT` | 父层加载 | 父层、项目和 child `CONTEXT.md` 加载证据 | `FAIL-CARDS-CONTEXT` |
| `FIELD-CARDS-ADVISOR` | 共享顾问合同 | 显式启用 subagents 时的 team roster、请教问题、可执行指导或降级说明 | `FAIL-CARDS-ADVISOR` |
| `FIELD-CARDS-WRITEBACK` | writer | `1-设定/` 下正式 JSON/Markdown refs | `FAIL-CARDS-WRITEBACK` |
| `FIELD-CARDS-GATE` | review/validator | coverage 与 route parity 结论 | `FAIL-CARDS-GATE` |

## Completion Contract

一次 `1-设定` 任务完成时，父层只交付一套收束结果：

- 命中的角色/场景/物品/技能正式 cards 或相关合同修复。
- gate / validation 结论。
- 显式启用 subagents 时的 `advisor_consultation_packet` 状态或降级说明。
- 对未处理对象的明确边界说明。
- 若发生降级或跳过子技能，说明原因和影响。
- 必须已调用 `.agents/skills/story/scripts/workflow_manager.py record-skill-completion`，把本轮父技能或子技能完成态写入项目 `STATE.json#workflow_runtime.execution_state.stage_progress`；不得只交付 cards 而不落状态。

## Output Contract

- Required output: 命中的角色/场景/物品/技能 cards、相关合同修复摘要，或 coverage repair 结果。
- Output format: JSON card payload、Markdown 图谱/报告，或 `templates/output-template.md` 对齐的父层摘要。
- Output path: 正式业务输出只写入 `projects/story/<项目名>/1-设定/` 下的对应 child root。
- Naming convention: 文件名遵循 child skill 命名合同；父层报告使用 kebab-case 日期后缀。
- Completion gate: 已实际调度的 child skill 完成写回，未调度对象不补占位，writer 与 coverage/review gate 无 blocking finding。
- State gate: 父技能使用 `--skill-id story-cards`；子技能单独调用时分别使用 `story-cards-character / story-cards-scene / story-cards-item / story-cards-skill`，并在 `--artifacts` 中列出写回的 card/index/report 相对路径。
