# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-组间` 阶段的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/2-组间/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-组间` 目录存在但父级 `SKILL.md` 为空 | 阶段合同层 | 先补父级阶段合同与子路径矩阵 | 让三个子技能都从父级显式可达 | 父级能说明唯一入口 |
| 项目级共享约束与分组动态设计混在一起 | 阶段边界层 | 先拆成“全组一致项”和“分组偏置项”再落子技能 | 在父级合同与类型协议里显式区分 shared vs group-biased | 全局风格保持全组一致，类型元素与导演意图不再混层 |
| 分组后节奏诉求仍混入 `2-组间` | 阶段边界层 | 将节奏蓝图回收到 `1-规划/4-节奏`，`2-组间` 只消费其 handoff | 在父级路由中移除旧第四入口，并要求节奏类诉求先查 `1-规划` | 规划层与组间层不再混淆 |
| `类型元素` 与 `全局风格` 先后不清 | tranche 合同层 | 在父级显式写 `全局风格 -> 类型元素` | 用 tranche precedence 取代隐式默认 | 路由不再摇摆 |
| `导演意图` 未依赖分组容器 | 上游依赖层 | 显式挂到 `1-规划/3-分组` | 在子技能合同写前置条件 | 不再凭空自建分组 |
| 项目已启用顾问团，但组间阶段未读取 `team.yaml` | 共享运行时层 | 执行前先读项目根 `team.yaml` 与 `_shared/council-runtime/module-spec.md` | 在 `2-组间` 根技能固化 `监制前置 + 评审闸门` 合同 | 组间任务进入前能判断是否要启用顾问团 |
| `导演意图` 与 `3-明细` 分别维护各自的组/镜 JSON 壳 | 真源治理层 | 把共享结构上收到 `.agents/skills/aigc/_shared/director_episode_output.schema.json` | 阶段与子技能只回写 Markdown 真稿和 shared schema 映射，不再各写一套字段名 | `2-组间` 与 `3-明细` 都引用同一个 shared schema |
| `2-组间` 仍把产物落到阶段私有目录，而不是统一编导根文件 | 运行时真源层 | 将父级合同与输出契约统一改写为 `projects/<项目名>/编导/第N集.json` | 把 `_shared/project-runtime-layout.md` 设为目录真源，并固定“执行前完整读取 episode JSON，再做组级 patch” | `2-组间` 父级、子级与 `3-明细` 对单一根文件口径一致 |
| 子技能既想直写统一根文件，又想把完整思维链塞进根文件，导致 episode JSON 臃肿 | 输出治理层 | 固定“根文件只放最终业务真相，完整思维链留在子技能 sidecar” | 在父级 `SKILL.md` 建立 `Unified Root File Output Governance`，要求子技能只交 `field patch`，父级统一聚合 | 根文件不再重复堆叠多份子技能三段式思维链 |
| 父级默认把所有子技能都纳入聚合，导致未命中能力也被补空字段 | 调度治理层 | 在父级 `SKILL.md` 建立 `Selective Dispatch And Aggregation Contract`，只聚合 `selected_subskills[]` | 固定“未调度子技能与总 json 无关，禁止为了结构完整补空聚合” | 本轮总 json 只受实际命中的子技能 patch 影响 |

## Repair Playbook

1. 先检查父级 `2-组间/SKILL.md` 是否明确“全组一致 / 分组动态 / 逐组设计”的边界。
2. 再检查三个子路径是否都具备 `SKILL.md + CONTEXT.md`。
3. 再检查 tranche precedence 与 `shared vs group-biased` 是否写清。
4. 最后检查是否形成到 `3-明细` 的唯一 handoff。

## Reusable Heuristics

- `2-组间` 最常见的问题不是子技能不够多，而是父级没有把“全组一致”和“分组动态”边界立起来。
- 三个子技能都叫 `unordered` 不等于可以无脑并行；只要存在稳定前置依赖，就应该在父级显式写 tranche。
- 若 `0-Init.original_adherence=false` 且已完成分组，节奏治理应先进入 `1-规划/4-节奏`；`2-组间` 只继承该 handoff 做导演层解释。
- 全局风格应只保留所有组都要继承的稳定底座；一旦开始替单个组加例外，就该下沉到 `类型元素` 或 `导演意图`。
- 类型元素最稳的写法不是“统一类型口号”，而是“共享类型约束 + 分组激活/偏置表”。
- 从参考仓继承时，最值得迁移的是能力分工，不是旧路径与旧载体。
- 对 `2-组间` 来说，顾问团最稳的节奏是“监制先校执行方向，评审最后卡 validation gate”，不要让评审过早参与发散。
- 对内容输出型技能族做结构升级时，优先把字段、流程、策略、模板拆进 `references/`，再收缩主 `SKILL.md`，比直接重写整份合同更稳。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 当 `导演意图` 与 `3-明细` 共享同一组级/镜级事实时，最稳的做法是让 `_shared/*.schema.json` 承担结构真源，阶段文档只维护语义和写位，不再各自发明 JSON 壳。
- 当规划阶段只留下 `bootstrap_output` 与 `source_profile` handoff 时，`2-组间` 最该守住的不是等待别人先建根，而是“缺文件就自动初始化，再只 patch 自己负责的组级字段”。
- 对复合型多子技能包来说，最稳的输出结构不是“每个子技能把完整三段式灌进根文件”，而是“根文件只收最终字段，三段式思维链留在 sidecar”。
- 对复合型多子技能包来说，最稳的聚合方式不是“每轮全量子技能都过一遍”，而是“只聚合本轮命中的子技能 patch”；未命中能力与总 json 无关。
- 当叶子层开始共享同一份 `projects/<项目名>/编导/第N集.json` 时，最容易长回来的旧习惯是“叶子自认拥有自己的阶段主稿”；最稳的修法是强制每个 leaf 在 `execution-flow.md` 中显式写出 `patch target / sidecar / selected_subskills only`。
- 当 `2-组间` 已切到统一根文件后，深层 references 与历史 case 不能继续把 `style-bible.md / type-playbook.md / 第N集.md` 说成当前主产物；更稳的写法是保留“曾经承载过什么能力”的背景，同时把现状明确改写为 `第N集.json` 中的字段区块真源。

## Case Log

### Case-20260409-AIGC-DIRECTING-STAGE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/2-组间` 建立了父级阶段合同，并补齐子技能体系的 `SKILL.md + CONTEXT.md`。
- root_cause_or_design_decision: 用户要求补齐 `2-组间` 子路径，但真正的源层缺口不是单个子目录，而是 `2-组间` 根级完全空白，导致无法给子路径提供统一路由、tranche 与路径合同。
- final_fix_or_heuristic: 先补父级 `2-组间/SKILL.md + CONTEXT.md`，再把子技能都收束为适配当前仓运行时的内容输出合同；当时先补齐阶段合同，当前最新运行时已进一步统一到 `projects/<项目名>/编导/第N集.json`；显式写出 `全局风格 -> 类型元素 -> 导演意图` 的 tranche precedence。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补齐
  - [x] 父级 `CONTEXT.md` 已建立
  - [x] 子路径合同已纳入父级统一路由
  - [x] tranche precedence 已显式声明
  - [x] 已形成到 `3-明细` 的 handoff 方向
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/1-风格基座/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/2-类型指导/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/4-导演意图/SKILL.md`
- user_feedback_or_constraint: 用户明确要求按内容输出型完善 `2-组间` 子路径，并在完成后补齐根级 `SKILL.md` 与 `CONTEXT.md`。

### Case-20260409-AIGC-DIRECTING-RHYTHM-SUBTYPE-REMOVAL

- milestone_type: source_contract_change
- outcome: 移除了原有的集级节奏子技能目录，并把集级节奏收束并入 `导演意图` 的父级路由与 handoff 合同。
- root_cause_or_design_decision: 用户明确要求删除 `节奏优化` 子技能；若只删目录而不回写父级路由、输出契约与上下游 handoff，仓内会残留失效入口与悬空路径。
- final_fix_or_heuristic: 先在 `2-组间` 根合同中把可执行子路径收束为 `全局风格 / 类型元素 / 导演意图`，再同步修改输出契约、上游继承与 `3-明细` handoff，最后删除目录本体。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已改为三个子路径
  - [x] `references/` 路由与输出契约已同步
  - [x] 下游 `3-明细` handoff 已去除失效入口
  - [x] 原子技能目录已删除
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/references/type-strategies.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户直接要求移除原有的集级节奏子技能目录。

### Case-20260409-AIGC-DIRECTING-RHYTHM-SUBTYPE-RETURN

- milestone_type: source_contract_change
- outcome: 将 `节奏优化` 重新引入为 `2-组间` 的条件式第四入口，并用 `0-Init.original_adherence` 作为执行门。
- root_cause_or_design_decision: 新需求不再是“删除节奏子技能”，而是“仅在未强调原作遵循时独立执行节奏蓝图”；若只恢复目录而不回写父级路由、输出契约和上游布尔门，仓内会同时存在新旧两套真相。
- final_fix_or_heuristic: 先在 `0-Init` 固化 `original_adherence` 与剧本节奏字段，再在 `2-组间` 根合同中恢复 `节奏优化` 子技能，并把 `导演意图` 收回到导演构思本位。
- prevention_or_replication_checklist:
  - [x] `0-Init` 已新增 `original_adherence` 布尔门
  - [x] 父级 `2-组间` 已恢复第四入口
  - [x] `导演意图` 与 `节奏优化` 边界已重新划清
  - [x] 已从旧仓提炼节奏治理精华而非整包照搬
- evidence_paths:
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/节奏优化/SKILL.md`
- user_feedback_or_constraint: 用户要求“在未强调原作遵循的情况下”恢复 `节奏优化`，并明确由相关 YAML 字段决定执行与否。

### Case-20260409-AIGC-DIRECTING-COUNCIL-RUNTIME

- milestone_type: source_contract_change
- outcome: 为 `2-组间` 根技能接入了基于项目根 `team.yaml` 的顾问团运行时，默认执行 `监制前置 -> 主代理草案 -> 评审闸门`。
- root_cause_or_design_decision: 用户要求 `2-组间` 根技能及其叶子技能进入时都先判断顾问团是否启用，并落实 `监制 / 评审` 职责；若只在初始化阶段保留团队配置，组间阶段将无法稳定消费。
- final_fix_or_heuristic: 组间阶段的顾问团运行时不应由各个子技能各自重写，而应由 `2-组间` 根技能读取项目根 `team.yaml` 并统一执行。
- prevention_or_replication_checklist:
  - [x] `2-组间/SKILL.md` 已新增 `Council Runtime Contract`
  - [x] 已固定 `监制前置 + 评审 validation gate`
  - [x] 子技能继续只承接内容合同
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- user_feedback_or_constraint: 用户明确要求 `2-组间` 及其叶子技能进入时都先读取 `projects/<项目名>/team.yaml`，并默认启用 `监制 / 评审` 职责。

### Case-20260409-AIGC-DIRECTING-REFERENCES-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `2-组间` 根技能重构为“主合同 + references 模块细则”结构，并为子技能建立统一的 `references` 承载层。
- root_cause_or_design_decision: 现有内容本体已经稳定，但大量 VSM、field map、workflow 与输出契约全部堆在单个 `SKILL.md` 中，不符合最新内容输出型规范要求的模块化真源承载，也增加后续同步漂移风险。
- final_fix_or_heuristic: 根技能保留阶段边界、路由门禁与 Root-Cause 合同；把思维链、执行流程、类型策略、输出契约拆到 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md`。
- prevention_or_replication_checklist:
  - [x] 根技能已建立 `references/` 四件套
  - [x] 根 `SKILL.md` 已回收到主合同层
  - [x] 子技能仍以原 canonical landing 为真源
  - [x] 未改变项目级/集级边界与既有语义
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/references/chain-of-thought.md`
  - `.agents/skills/aigc/2-组间/references/execution-flow.md`
  - `.agents/skills/aigc/2-组间/references/type-strategies.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“加载最新的规范，重构 `.agents/skills/aigc/2-组间`，不改变内容基础”。

### Case-20260410-AIGC-DIRECTING-RHYTHM-DEMOTION-TO-PLANNING

- milestone_type: source_contract_change
- outcome: 从 `2-组间` 根合同与 `references/` 中移除了 `节奏优化` 作为阶段内子路径的定义，并改为消费 `1-规划/4-节奏` 的上游 handoff。
- root_cause_or_design_decision: 用户要求将节奏治理迁到 `1-规划`；直接技术原因是该能力真正依赖 `3-分组` 的稳定容器，继续挂在组间阶段会让父级路由与真实输入链错位。
- final_fix_or_heuristic: 对 `2-组间` 来说，分组后的节奏蓝图应视为规划层上游输入，而不是阶段内独立叶子；组间层只保留风格、类型、导演意图三个可执行入口。
- prevention_or_replication_checklist:
  - [x] `2-组间` 根合同已移除旧第四入口
  - [x] `references/type-strategies.md` 与 `references/output-template.md` 已同步
  - [x] 子技能回退指向已改为 `1-规划/4-节奏`
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/SKILL.md`
- user_feedback_or_constraint: 用户明确要求把原 `节奏优化` 从 `2-组间` 挪到 `1-规划/subtypes/4-节奏`，并改成分组后规划层节奏能力。

### Case-20260410-AIGC-INTER-GROUP-REPOSITION

- milestone_type: source_contract_change
- outcome: 将阶段 `2-组间` 从传统编导语义重新定位为“分镜组间统一或动态设计”阶段，并同步收束根合同、子技能职责与入口元数据。
- root_cause_or_design_decision: 用户明确要求把该阶段调整为“全局风格全组一致、类型元素半一致半动态、导演意图逐组考虑”；若只改目录名而不改合同，阶段会继续以旧的项目级/集级编导逻辑运行，形成新路径承载旧规则。
- final_fix_or_heuristic: 先在父级合同中锁定三层关系：`全局风格 = 所有分镜组一致`、`类型元素 = 全组共享约束 + 分组偏置`、`导演意图 = 按集承载、逐组设计`，再把这套关系回写到 references、子技能与入口元数据。
- prevention_or_replication_checklist:
  - [x] `2-组间/SKILL.md` 已改为组间设计主合同
  - [x] `2-组间/CONTEXT.md` 已补共享/动态边界 heuristic
  - [x] `全局风格 / 类型元素 / 导演意图` 三个子技能职责已同步
  - [x] `aigc/SKILL.md` 已把阶段 2 描述更新为组间
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/references/type-strategies.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
- user_feedback_or_constraint: 用户明确要求把原阶段目录重命名为 `组间`，并把阶段定位调整为“全局统一 + 类型半动态 + 导演逐组设计”。

### Case-20260410-AIGC-DIRECTING-SHARED-DIRECTOR-SCHEMA

- milestone_type: source_contract_change
- outcome: 将 `导演意图 -> 3-明细` 的共享 JSON 结构上收为 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，并让阶段/子技能输出契约统一回指该 schema。
- root_cause_or_design_decision: 用户要求为后续 harness 工程化预先建立导演集级结构真源；若仍让 `2-组间` 与 `3-明细` 分别维护自己的 group/shot JSON 壳，后续接入验证器、中间件和下游消费器时会出现平行字段合同。
- final_fix_or_heuristic: 顶层固定沿用 `skill-内容输出型` 的 `metadata / thinking_chain / final_output` 三段式 JSON 投影，组级固定壳统一为 `final_output.main_content.分镜组列表[]`，镜级固定壳统一为 `分镜明细[]`。
- prevention_or_replication_checklist:
  - [x] shared schema 已落到 `_shared/`
  - [x] `2-组间/references/output-template.md` 已回指 shared schema
  - [x] 子技能输出模板引用已统一回收到 `2-组间/references/output-template.md`
  - [x] 后续 `3-明细` 可沿同一壳继续 patch-in-place
- evidence_paths:
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“考虑后续 harness 工程化演化方向”，并指定三段式 JSON 布局与组级/镜级固定字段层级。

### Case-20260410-AIGC-DIRECTING-UNIFIED-DIRECTOR-ROOT

- milestone_type: source_contract_change
- outcome: 将 `2-组间` 的父级运行时从阶段私有目录收敛为统一根文件 `projects/<项目名>/编导/第N集.json`，并把本阶段职责重写为组级字段 patch。
- root_cause_or_design_decision: 用户明确要求后续 `2-组间` 与 `3-明细` 都围绕一个统一 JSON 根文件做定向输出；若 `2-组间` 继续声明自己的阶段主文件，就会形成 shared schema 之外的第二真相。
- final_fix_or_heuristic: 由 `_shared/project-runtime-layout.md` 统一声明目录真源，`2-组间` 父级合同与输出模板只保留字段责任、sidecar 与阶段验收，不再保留独立 episode 主产物。
- prevention_or_replication_checklist:
  - [x] `2-组间/SKILL.md` 已回指 shared runtime layout
  - [x] `2-组间/references/output-template.md` 已改为字段责任表
  - [x] 阶段验收路径已改为 `projects/<项目名>/编导/validation-report.md`
  - [x] 已显式声明执行前加载完整 `第N集.json`
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“2组和3组都将围绕一个统一根文件（确定为 json）进行不同字段分属下的定向输出”。

### Case-20260410-AIGC-DIRECTING-OUTPUT-GOVERNANCE-PROMOTION

- milestone_type: source_contract_change
- outcome: 将“统一根文件只承载最终业务真相、子技能完整思维链留在 sidecar、父技能负责 field patch 聚合”的输出治理决议正式晋升到 `2-组间/SKILL.md`。
- root_cause_or_design_decision: 用户在统一根文件方案下进一步提出输出机制选择问题；若不先把“根文件放什么、sidecar 放什么、父技能负责什么”写成父级规范，后续 leaf 重构会再次在“直写根文件”与“先各写完整主稿再汇总”之间摇摆。
- final_fix_or_heuristic: 在父级主合同新增 `Unified Root File Output Governance`，明确根文件只承载最终组级字段，子技能只交 `field patch`，完整三段式思维链只允许落在 sidecar，shared schema 顶层 `thinking_chain` 仅保留父级精简摘要或 provenance 用途。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已新增统一输出治理章节
  - [x] `CONTEXT.md` 已记录“根文件不堆叠子技能思维链”的经验
  - [x] 子技能输出模板已统一继承父级真源
  - [x] 后续整树重构可直接以该规范为准绳
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“先将以上决议升格为标准化规范，落盘到 `2组/3组` 的主 `SKILL.md`，再以其为指导执行完整重构”。

### Case-20260410-AIGC-DIRECTING-LEAF-LEGACY-NARRATIVE-FLATTENING

- milestone_type: source_contract_change
- outcome: 将 `2-组间` 深层 references 与 leaf 历史 case 中仍把 `style-bible.md / type-playbook.md / 第N集.md` 叙述为当前主产物的口径统一收平为字段区块真源叙述。
- root_cause_or_design_decision: 父级与运行时真源已经迁到 `projects/<项目名>/编导/第N集.json`，但 leaf 的 `CONTEXT.md` 历史案例和少量深层 references 仍在暗示旧主稿；如果不清这层叙述残留，后续协作者会把旧载体误当当前 canonical source。
- final_fix_or_heuristic: 保留历史案例的能力背景与当时的设计意图，但统一把现状真源改写为统一根文件中的 `全局风格 / 类型元素 / 导演意图` 字段区块；旧文件名只允许作为“曾经的载体”或负向禁令出现。
- prevention_or_replication_checklist:
  - [x] `全局风格/CONTEXT.md` 已改写为字段区块真源叙述
  - [x] `类型元素/CONTEXT.md` 已改写为字段区块真源叙述
  - [x] `导演意图/CONTEXT.md` 已改写为字段区块真源叙述
  - [x] `导演意图 / 类型元素` 深层思维链已改成 `全局风格 / 类型元素` 字段区块依赖口径
- evidence_paths:
  - `.agents/skills/aigc/2-组间/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/references/chain-of-thought.md`
- user_feedback_or_constraint: 用户明确要求“扫 `2-组间` 更深层 references 与历史 case/example 文本，把还残留的旧主稿叙述口径再清一轮”。

### Case-20260411-AIGC-INTER-GROUP-FIRST-BOOTSTRAP-OWNERSHIP

- milestone_type: source_contract_change
- outcome: 将 `projects/<项目名>/编导/第N集.json` 的首次初始化责任正式上收为 `2-组间`，并把规则固定为“首次进入且根文件缺失时自动 bootstrap，再继续 patch 组级字段”。
- root_cause_or_design_decision: 用户指出 `编导/第N集.json` 的稳定最小骨架应建立在分组容器已成立之后；直接技术原因是旧合同把建根责任放在 `1-规划/1-分集`，导致 `2-组间` 虽是第一次真正消费方，却无法对初始化时机负责。
- final_fix_or_heuristic: 如果某阶段是共享根文件的第一次真实消费方，就应同时拥有“缺文件则自动初始化”的责任；否则上游会被迫提前落一个语义不完整的空壳。
- prevention_or_replication_checklist:
  - [x] `2-组间/SKILL.md` 已声明缺文件自动 bootstrap
  - [x] `2-组间/references/output-template.md` 已改写父级真源责任
  - [x] `2-组间/references/execution-flow.md` 已把初始化插入正式工作流
- evidence_paths:
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/2-组间/references/execution-flow.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
- user_feedback_or_constraint: 用户明确提出“`编导/第N集.json` 应该在分组之后确定，或等到 2-编导阶段再根据规则自动落盘”。
