---
name: story-cards
governance_tier: router
skill_role: parent_guide
description: "Use when routing story card generation, repair, coverage, writeback, and validation across character, scene, item, and skill card child skills."
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

## Context Processing Contract

| processing_slot | required_action | evidence | fail_code |
| --- | --- | --- | --- |
| `context_snapshot` | 记录父层、项目层和命中子技能上下文是否加载 | `loaded_context_manifest` | `FAIL-CARDS-CONTEXT` |
| `missing_context_policy` | 项目 `MEMORY.md` 或必要 card 输入缺失时先报告缺口，不伪造设定 | `missing_context_report` | `FAIL-CARDS-CONTEXT` |
| `context_conflict_map` | 用户请求、项目记忆、north_star 与既有 cards 冲突时标注 owner | `conflict_owner_map` | `FAIL-CARDS-ROUTE` |
| `context_application` | 只把上下文转成子技能输入、顾问问题或 validator finding，不直接替子技能创作 | `child_input_packet` | `FAIL-CARDS-CREATIVE-AUTHORSHIP` |
| `context_writeback_decision` | 新长期偏好写项目 `MEMORY.md`，跨项目经验写本 `CONTEXT.md` | `writeback_decision` | `FAIL-CARDS-WRITEBACK` |

## Business Requirement Analysis Contract

| field | requirement | evidence | fail_code |
| --- | --- | --- | --- |
| `business_goal` | 把 story 设定对象路由到角色、场景、物品、技能四个 child owner，并完成写回与 gate 闭环 | 用户请求、项目 `1-设定/` 目录、child skill 合同 | `FAIL-CARDS-BUSINESS-GOAL` |
| `business_object` | `projects/story/<项目名>/1-设定/2-角色卡/`、`3-场景卡/`、`4-物品卡/`、`5-技能卡/` 及关系图谱 side output | Canonical Output Root、child Output Contract | `FAIL-CARDS-BUSINESS-OBJECT` |
| `constraint_profile` | 父层不创作对象正文，不复制 `north_star.yaml`，不为未调度子技能补空 payload | Skill Group Members、Shared Runtime Contract | `FAIL-CARDS-BUSINESS-CONSTRAINT` |
| `success_criteria` | 路由正确、上下文加载完整、实际调度 child 完成写回、coverage/review 无 blocking finding、状态回写成功 | Quality Gates、Completion Contract | `FAIL-CARDS-BUSINESS-SUCCESS` |
| `complexity_source` | 复杂度来自多对象依赖链、项目上下文、顾问请教、writer/validator parity 和选择性聚合 | Mode Selection、Operating Flow | `FAIL-CARDS-BUSINESS-COMPLEXITY` |
| `topology_fit` | router 拓扑适配：父层保 owner 裁决；child 保创作判断；writer/validator 保机械一致；依赖链阻止物品/技能绕过上游接口 | Skill Group Members、Visual Maps、Quality Gates | `FAIL-CARDS-TOPOLOGY-FIT` |

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

## Type Routing Matrix

| input_type | signal | route_to | required_nodes | module_load | fail_code |
| --- | --- | --- | --- | --- | --- |
| `single` | 只命中角色、场景、物品或技能之一 | `Single Child Path` | `N1,N2,N3,N5,N6` | `CONTEXT.md` | `FAIL-CARDS-TYPE-SINGLE` |
| `mixed` | 同时命中多个对象或用户要求成套建卡 | `Dependency Chain Path` | `N1,N2,N3,N4,N5,N6` | `CONTEXT.md` | `FAIL-CARDS-TYPE-MIXED` |
| `full-build` | 用户要求全量设定卡闭环 | `Full Build Path` | `N1,N2,N3,N4,N5,N6` | `CONTEXT.md` | `FAIL-CARDS-TYPE-FULL` |
| `coverage-repair` | validator finding 指向 cards 覆盖率、route parity 或 schema | `Finding Repair Path` | `N1,N2,N3,N5,N6` | `CONTEXT.md` | `FAIL-CARDS-TYPE-REPAIR` |
| `source-contract-fix` | 父子合同、writer、validator、模板或测试漂移 | `Source Contract Path` | `N1,R1,R2,N5,N6` | `CONTEXT.md` | `FAIL-CARDS-TYPE-SOURCE` |

## Thinking-Action Node Map

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、请求类型和非目标 | 用户请求、项目路径、north_star 信号 | 判定是否属于 `1-设定`，全局/风格/题材请求转回 `0-初始化/north_star.yaml` | `task_profile`、`reroute_decision` | `N2-LOAD` / `R1-ROOT-CAUSE` | 项目根或 child finding 不可定位时停止 |
| `N2-LOAD` | 加载上下文并形成 child 输入包 | 本 `SKILL.md + CONTEXT.md`、项目 `MEMORY.md`、项目 `CONTEXT/` | 形成 `loaded_context_manifest`、冲突 owner 和缺失上下文报告 | `loaded_context_manifest`、`context_conflict_map` | `N3-ROUTE` | 上下文缺失不得伪造对象事实 |
| `N3-ROUTE` | 选择实际调度的 child skills | Type Routing、Routing Guide、validator finding | 生成命中 child 列表和执行顺序；未调度 child 不补占位 | `child_dispatch_plan` | `N4-ADVISOR` / `N5-WRITEBACK` | route 必须与对象 owner 一致 |
| `N4-ADVISOR` | 显式启用 subagents 时形成顾问请教包 | 项目 `team.yaml`、共享顾问合同、child 输入 | 面向角色/场景/物品/技能提出具体问题并收束为 `advisor_consultation_packet` | `advisor_consultation_packet` 或降级报告 | `N5-WRITEBACK` | 未启用 subagents 时记录 N/A；启用但阻断时必须说明降级 |
| `N5-WRITEBACK` | 聚合实际 child 产物并执行机械写回/校验 | child payload、shared writer、coverage validator | 调用 writer/validator；记录 route parity、schema、coverage 与状态回写 | `writeback_report`、`validation_report`、`state_update_report` | `N6-CLOSE` / `R1-ROOT-CAUSE` | blocking finding 必须回源层或 child owner 修复 |
| `N6-CLOSE` | 收束唯一交付口径 | validation 结果、未处理对象边界 | 输出调度摘要、写回路径、验证状态、未处理边界、源层同步结果 | `final_cards_report` | `done` | 最终只交付实际调度对象和 gate 结论 |
| `R1-ROOT-CAUSE` | 非平凡失败追因 | validator finding、路径漂移、合同冲突 | 上溯父层路由、child 合同、模板、writer、validator 或 card 内容 | `root_cause_trace` | `R2-SYNC` | 不得只修单张 card 掩盖源层漂移 |
| `R2-SYNC` | 修复源层并回归验证 | `root_cause_trace` | 同步父子合同、模板、writer/validator/test 引用和上下文经验 | `sync_patch`、`reference_scan` | `N5-WRITEBACK` | 受影响引用必须扫描或说明残留 |

## Multi-Subskill Continuous Workflow

- 主技能包被整体调用时，在满足必要输入、显式选择和安全门后，不再为“是否继续下一步”额外确认。
- 无序号同级子技能包默认由父级根据用户请求选择性调度；只有 `mixed/full-build` 或依赖门需要时才进入依赖链。
- 数字序号阶段按 `角色卡 -> 场景卡 -> 物品卡 -> 技能卡` 串行执行，前一对象接口自动作为后一对象输入。
- 英文序号路线按用户意图、父级路由或输入类型单选分流；只有用户明确要求对比或并跑时才多选。
- 卫星技能、query/resume/review 旁路入口不默认纳入本技能主链；只有 gate、用户请求或父级合同显式需要时才回接。
- 每个被调度的技能仍必须加载自身 `SKILL.md + CONTEXT.md`，并由子技能完成 LLM 主创判断。

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

## Module Loading Matrix

| module | load_when | authority | forbidden_use | rework_target |
| --- | --- | --- | --- | --- |
| `CONTEXT.md` | 每次调用本 router | cards 技能组经验、失败模式、路由启发 | 重定义父层路由、child owner 或输出根 | `Context Processing Contract` |
| `子技能/SKILL.md + CONTEXT.md` | `N3-ROUTE` 命中对应对象时 | child 创作合同、字段 owner、局部 gate | 未命中时补空 payload；覆盖父层依赖链 | `N3-ROUTE` / 命中子技能 |
| `../_shared/team-advisor-consultation-contract.md` | 显式启用 subagents / team advisor 时 | 顾问请教、汇流、降级报告格式 | 替代 child LLM 主创或 reviewer gate | `N4-ADVISOR` |
| `.agents/skills/story/scripts/cards_writer.py` | child payload 已通过局部门禁后 | 机械投影、原子写回 | 生成创作正文、补字段、裁决对象质量 | `N5-WRITEBACK` |
| `.agents/skills/story/scripts/cards_coverage_validator.py` | 写回后或 coverage repair 时 | schema、route parity、数量/密度/依赖检查 | 替代 child 语义审查 | `N5-WRITEBACK` / `R1-ROOT-CAUSE` |

## Module Trigger Matrix

| trigger_signal | required_modules | load_phase | return_gate | rework_target | mechanical_check |
| --- | --- | --- | --- | --- | --- |
| `single / FAIL-CARDS-TYPE-SINGLE / FAIL-CARDS-ROUTE` | `CONTEXT.md`, `子技能/SKILL.md + CONTEXT.md` | `N1-INTAKE -> N3-ROUTE` | `N3-ROUTE` | `N3-ROUTE` | child route list has exactly the matched owner |
| `mixed / full-build / FAIL-CARDS-TYPE-MIXED / FAIL-CARDS-TYPE-FULL` | `CONTEXT.md`, `子技能/SKILL.md + CONTEXT.md` | `N1-INTAKE -> N3-ROUTE` | `N5-WRITEBACK` | `N3-ROUTE` | dependency order is character, scene, item, skill |
| `coverage-repair / FAIL-CARDS-TYPE-REPAIR / FAIL-CARDS-GATE` | `CONTEXT.md`, `.agents/skills/story/scripts/cards_coverage_validator.py` | `N1-INTAKE -> R1-ROOT-CAUSE` | `N5-WRITEBACK` | `R1-ROOT-CAUSE` | finding maps to one child owner or parent parity |
| `source-contract-fix / FAIL-CARDS-TYPE-SOURCE / FAIL-CARDS-WRITEBACK` | `CONTEXT.md`, `.agents/skills/story/scripts/cards_writer.py`, `.agents/skills/story/scripts/cards_coverage_validator.py` | `R1-ROOT-CAUSE -> R2-SYNC` | `N5-WRITEBACK` | `R2-SYNC` | `rg` scan shows no stale child route references |
| `subagents / FAIL-CARDS-ADVISOR` | `../_shared/team-advisor-consultation-contract.md` | `N4-ADVISOR` | `N4-ADVISOR` | `N4-ADVISOR` | packet or downgrade report is present |

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
4. 对每个命中子技能加载其 `SKILL.md + CONTEXT.md`，再按其合同读取本地模板、references、review、types 或 guardrails。
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
