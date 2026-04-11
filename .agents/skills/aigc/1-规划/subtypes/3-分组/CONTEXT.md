---
skill: aigc-planning-grouping
context_type: knowledge-base
last_updated: 2026-04-09
---

# aigc-planning-grouping · 经验层文档

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划/subtypes/3-分组` 的经验层知识库，不是过程日志。
- 进入 `3-分组` 时，应在父级 `1-规划/CONTEXT.md` 之后预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 父级 `SKILL.md` > 本 `SKILL.md` > 父级 `CONTEXT.md` > 本 `CONTEXT.md`。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
current_chars: 9939
soft_limit_chars: 40000
hard_limit_chars: 80000
current_cases: 6
soft_limit_cases: 80
hard_limit_cases: 140
status: ok
last_compaction: null
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 直接沿用参考仓导演阶段字段，导致规划阶段越权 | 阶段边界层 | 收回到组级结构容器、边界理由与交接约束 | 在 `SKILL.md` 显式声明“继承结构，不继承导演字段” | 对应 `第N集.md` 不出现导演/镜头专属字段 |
| 只写组名清单，没有主路由与边界理由 | 路由合同层 | 先补 `G1/G2/G3` 裁决，再重写分组计划 | 把“先判路由再分组”固化为硬规则 | `执行报告.md` 可解释为何这样分组 |
| 直接照抄旧仓路径，产物漂移到 `output/影片/...` | 路径合同层 | 重写到 `projects/<项目名>/1-规划/3-分组/` | 将当前仓 canonical landing 固化到主合同 | 所有产物落在当前项目工作区 |
| 把集内分组误写成 `第N组.md` 独立文件 | 输出粒度层 | 收回到对应 `第N集.md` 中写组级容器 | 固化“集粒度由 `1-分集` 决定，`3-分组` 只做集内分组” | 不再出现 `第N组.md`，且对应 `第N集.md` 内含分组表与组条目 |
| 分组只是平均切块，未考虑依赖与并行性 | 结构设计层 | 重跑边界评估与依赖分析 | 在 `FIELD-GRP-DEP-06` 固化串并行检查 | 可明确判断哪些组能并行、哪些需串行 |
| 只有 `SKILL.md + CONTEXT.md`，没有 route reference / template / validator 载体 | 真源机制层 | 补齐 `references/`、`templates/`、`scripts/validate_grouping.py` | 将分路细则、模板骨架、校验入口都提升为单一真源 | `3-分组` 不再只是可读合同，而具备可执行机制骨架 |
| 组容器只有目标与范围，没有结构锚点、依赖说明和并行性判断 | 输出锚点层 | 在表格与组章节中补 `structure_anchor / dependency_note / parallelism` | 把这些字段纳入模板和 validator 的强制校验 | 下游无需重新猜“为什么这样分”和“先做哪组” |
| 量化合同是当前技能自己抽象的一套简化分数，而未继承参照源的场景顺序与字窗机制 | 量化真源层 | 把参照源的“场景顺序 + 时长策略 + 字窗公式 + 有效字数”投影为本技能 shared reference | 将 `scene-duration-projection.md` 设为量化真源，并让 `SKILL.md / references / templates / validator` 全部回指它 | `group_load_score` 降为二级摘要，量化硬门槛以投影 reference 为准 |
| 非均匀组时长只写在说明文字里，未显式落到 episode meta，导致下游把整集时长误当每组时长 | 时间基线层 | 在 `第N集.md` frontmatter 补 `默认组时长 / 分镜组时长映射`，并让 `estimated_duration_seconds` 与解析结果对齐 | 把组总时长基线固化进模板、reference 与 validator；帧级切分只作为下游交接合同，不在本阶段伪造 | 任一偏离默认值的组都能在 frontmatter 显式追溯到时长来源 |

## Playbook

1. 先确认父级 `1-规划` 已把当前任务路由到 `3-分组`。
2. 先锁定 `1-分集` 已给出的集边界与对应 `第N集.md`，而不是重切分集。
3. 先锁定待分组材料与主目标，而不是直接平分组数。
4. 先判 `G1/G2/G3`，再生成候选边界。
5. 先做依赖与并行性检查，再把组级容器写回对应 `第N集.md`。
6. 若参考仓结构有用，只迁移“容器优先 + 可追溯闭环”，不迁移导演层专属字段和旧路径。
7. 若发现 `3-分组` 只有合同没有机制载体，优先补 `references/`、`templates/`、`scripts/validate_grouping.py`，再继续扩写内容。

## Reusable Heuristics

- `3-分组` 最容易出错的地方不是不会分，而是把“组”误写成松散目录建议，没有形成下游可消费的结构容器。
- `3-分组` 的真源粒度不是“组文件”，而是“集文件里的组容器”；只要长出 `第N组.md`，通常就说明越过了 `1-分集` 的边界合同。
- 从 `3-拍摄段落` 继承能力时，最该继承的是“先定容器、再写细节”的工程思路，而不是它的导演字段体系。
- 从 `3-拍摄段落` 继承量化机制时，不能只拿一个简化负载分；优先继承“场景顺序先行 + 时长策略优先级 + 节奏字窗 + 有效字数 + 尾组规则”这条主链。
- 对规划阶段来说，分组的价值不在“均匀”，而在“可交接、可并行、依赖清晰”。
- `3-分组` 一旦需要跨执行者稳定复现，就不能只靠 `SKILL.md` 大段正文；至少要把 route reference、模板和 validator 各落一个真源载体。
- 若一个组不能回答“它锚定哪段结构、依赖谁、能否并行”，那它通常还不算可交接的组容器。
- 规划阶段可以不落导演阶段全部字段，但量化规则层必须与参照源同源，再在当前阶段做字段投影，而不是重新发明另一套口径。
- 当主 `SKILL.md` 已经开始变成“厚合同”时，优先把流程、思维链、类型化策略、输出模板说明拆到标准 `references` 模块层，而不是继续在主文档里横向加章节。
- 当 `G1/G2/G3` 三个 sibling reference 长期同步修改时，应把它们并入单一 `type-strategies.md` 真源；路由差异适合做章节，而不适合继续做并列文件。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 对 reasoning 模型的思维链模块，不要把 `S1-S7` 写成“必须逐字外显”的流程剧本；应先用启发式工作链决定删什么、比什么、落到哪个字段，再把 `S1-S7` 作为可见支架。
- `3-分组` 的可见思维快照至少要暴露 `路由决议 + 候选边界 + 组容器落点 + Gate Summary`；如果只剩流程标题或完整内部推理全文，都会降低可审计性。
- “组总时长元数据”与“帧内时间切分规则”不是同一层：前者属于 `3-分组` 的 episode meta 真源，后者属于下游 `5-分镜构图` 的消费合同，适合沉在量化 reference 做交接。

## Case Log

### Case-20260409-AIGC-PLAN-GROUPING

- milestone_type: source_contract_change
- outcome: 参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/3-拍摄段落` 的结构容器思路，为当前 `aigc/1-规划/subtypes/3-分组` 建立了可执行子技能合同与经验层。
- root_cause_or_design_decision: 用户要求完善 `3-分组`，但当前仓的直接技术缺口不是“内容待补”，而是该子路径完全空白，且父级 `1-规划` 仍将其标记为“预留中”，导致无法成为正式路由入口。
- final_fix_or_heuristic: 把参考仓中高价值的“容器优先、主路由优先、证据闭环”迁入规划阶段，重写为 `G1/G2/G3` 分组主路由、`group-plan + 第N集 + 执行报告` 输出合同，并同步接回父级 `1-规划` 路由矩阵。
- prevention_or_replication_checklist:
  - [x] `3-分组/SKILL.md` 已建立完整子技能合同
  - [x] `3-分组/CONTEXT.md` 已建立经验层
  - [x] 路径合同已切换到 `projects/<项目名>/1-规划/3-分组/`
  - [x] 父级 `1-规划` 已能把当前子路径视为正式入口
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/3-拍摄段落/SKILL.md`
- user_feedback_or_constraint: 用户要求同时使用 `skill-通用创建` 与 `skill-编排优化`，并明确指定以 `AIGC-ZEN-VOID` 的 `3-拍摄段落` 作为参考源，但当前仓默认以中文合同和 `projects/<项目名>/` 路径体系落地。

### Case-20260409-AIGC-PLAN-GROUPING-GRANULARITY

- milestone_type: source_contract_change
- symptom_or_outcome: 用户明确要求 `3-分组` 不应再按 `第N组.md` 输出，而应继续按 `1-分集` 已确定的 `第N集.md` 输出，分组仅在集内部执行。
- root_cause_or_design_decision: 直接技术原因不是不会分组，而是早先合同把“组级容器”误外化成了独立组文件，导致 `3-分组` 和 `1-分集` 在输出粒度上出现并行真相。
- final_fix_or_extracted_heuristic: 将 `3-分组` 的 canonical output 收回为 `projects/<项目名>/1-规划/3-分组/第N集.md`，在单集文件内部落盘分组表和组条目；`group-plan.md` 仅保留总览，不再承担组级真源。
- prevention_or_replication_checklist:
  - [x] `3-分组/SKILL.md` 已声明 `1-分集` 是集边界真源
  - [x] `3-分组/SKILL.md` 已禁止新增 `第N组.md`
  - [x] 对应 `第N集.md` 已成为分组结果真源
  - [x] 下游依赖文档已改为读取对应集文件中的组容器
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“仍然是按集，第N集.md（由 `.agents/skills/aigc/1-规划/subtypes/1-分集` 决定），分组仅在已经分好的集内部执行划分”。

### Case-20260409-AIGC-PLAN-GROUPING-ENGINE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求不要再停在“方向正确、机制半继承”，而是把 `3-分组` 继续补成接近成熟版 grouping engine 的形态。
- root_cause_or_design_decision: 直接技术原因不是主合同缺失，而是 `3-分组` 先前只有 `SKILL.md + CONTEXT.md` 两层，缺少分路细则、模板骨架和校验入口，导致规则可读但执行不可稳定复现。
- final_fix_or_extracted_heuristic: 为 `3-分组` 补齐路由细则、模板骨架与校验入口，并让 `SKILL.md` 回指这些真源；再用临时样例目录实跑校验，确认 engine 骨架可执行。
- prevention_or_replication_checklist:
  - [x] `3-分组/SKILL.md` 已声明 route references 为单一真源
  - [x] `3-分组/SKILL.md` 已声明 templates 为单一真源
  - [x] `3-分组/SKILL.md` 已声明 `validate_grouping.py` 为校验入口
  - [x] `references/` 已具备完整路由细则真源
  - [x] `templates/` 已补齐三类标准产物模板
  - [x] `scripts/validate_grouping.py` 已通过 `py_compile`
  - [x] 临时样例目录已实跑校验通过
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/group-plan.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/grouped-episode.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/validation-report.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
- user_feedback_or_constraint: 用户明确要求“继续全量完成为止”，且已将“默认按成熟版 engine 推进，不总停在最小补丁”上升到当前仓和跨项目 `AGENTS.md`。

### Case-20260409-AIGC-PLAN-GROUPING-QUANT-SOURCE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户明确指出 `3-分组` 的量化指标看起来是当前技能自己设计的简化版，没有直接继承参照源 `3-拍摄段落` 已沉淀的“场景顺序与时长策略规则”。
- root_cause_or_design_decision: 直接技术原因不是没有量化字段，而是把 `episode_load_score / group_load_score` 当成主量化机制，导致参照源中真正成熟的场景顺序、时长策略、节奏字窗、有效字数与尾组规则没有成为当前技能的量化真源。
- final_fix_or_extracted_heuristic: 新建 `references/scene-duration-projection.md` 作为规划阶段量化投影真源，并让 `SKILL.md`、`type-strategies.md`、模板和 validator 全部回指这条主链；原有 `group_load_score` 保留，但降级为二级摘要，不再充当主量化依据。
- prevention_or_replication_checklist:
  - [x] 已建立 `scene-duration-projection.md`
  - [x] `SKILL.md` 已声明量化真源继承合同
  - [x] `G2/G3` 已强制回指该量化真源
  - [x] 模板已增加 `duration_policy / pace_tier / base_text_window / hard_text_window / effective_text_chars / window_status`
  - [x] validator 已校验新量化字段与表头
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/scene-duration-projection.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/grouped-episode.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
- user_feedback_or_constraint: 用户明确要求“为什么不直接采纳原已沉淀好的宝贵经验”，并允许把较重内容落在 `/references` 承接，但要求规则层与之对齐。

### Case-20260409-AIGC-PLAN-GROUPING-LATEST-NORM

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求“加载最新的规范，重构 `.agents/skills/aigc/1-规划/subtypes/3-分组`，但不改变内容基础”。
- root_cause_or_design_decision: 当前 `3-分组` 已有成熟的领域合同与真源载体，但仍偏向旧版“厚主文档”结构，缺少最新 `skill-内容输出型` 规范要求的四个标准 `references` 模块，导致流程、思维链、类型化策略和模板说明的承载层不够稳定。
- final_fix_or_extracted_heuristic: 保留 `G1/G2/G3`、量化投影、模板与 validator 作为领域真源，同时补齐 `chain-of-thought / execution-flow / type-strategies / output-template` 四个标准模块，并让主 `SKILL.md` 改为“主合同 + 模块回指 + 领域真源”的三层结构。
- prevention_or_replication_checklist:
  - [x] 已补齐四个标准 `references` 模块
  - [x] `SKILL.md` 已声明标准模块与领域真源的分工边界
  - [x] `Root-Cause Execution Contract` 已把新增标准模块纳入优先排查链
  - [x] `CONTEXT.md` 已记录本轮 source-contract change
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“重构，不改变内容基础”；因此本轮只做规范层与承载层升级，不改动既有分组逻辑、量化口径与输出职责。

### Case-20260409-AIGC-PLAN-GROUPING-CANONICAL-ROUTE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求将 `g1-preset.md / g2-structure.md / g3-load.md` 整合到 `references/type-strategies.md` 后移除。
- root_cause_or_design_decision: 直接技术原因不是路由内容缺失，而是三条 sibling route references 已长期共同演化，形成“同一主题拆成三份并列真源”的漂移风险；这属于典型的 canonical source 缺失问题。
- final_fix_or_extracted_heuristic: 将三条路由的适用条件、证据、执行细则、量化门槛、回退条件、示例与误判统一并入 `references/type-strategies.md`，并把 `SKILL.md / CONTEXT.md` 的所有回指改为新的单一真源，然后删除旧文件。
- prevention_or_replication_checklist:
  - [x] `type-strategies.md` 已吸收 `G1/G2/G3` 全量路由细则
  - [x] `SKILL.md` 已回指新的单一路由真源
  - [x] `CONTEXT.md` 已同步更新历史证据路径与表述
  - [x] 旧 `g1/g2/g3` 文件已删除，避免再成为隐藏第二真相
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“应整合到 `type-strategies.md` 后移除”。

### Case-20260409-AIGC-PLAN-GROUPING-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求“按照最新的思维链设计规范，优化 `references/chain-of-thought.md`”。
- root_cause_or_design_decision: 直接技术原因不是 `3-分组` 缺少思维链模块，而是现有 `chain-of-thought.md` 仍偏旧版“裁决轴 + 步骤主链”快照，缺少最新 `think-think` 要求的运行模式、启发式工作链、可见快照/隐藏推理分层、工具后反思与 `Gate Summary`；同时相邻 `SKILL.md`、`execution-flow.md` 还残留了对已删除 `g1/g2/g3` 并列文件的旧回指。
- final_fix_or_extracted_heuristic: 将 `chain-of-thought.md` 升级为 `运行模式 + 启发式工作链 + 三向三重 + 可见快照 + Gate Summary` 合同，并把主合同与执行流中的旧路由回指统一收口到 `references/type-strategies.md`，避免思维链、执行流和主合同再次形成多套路由真源。
- prevention_or_replication_checklist:
  - [x] `references/chain-of-thought.md` 已升级为最新 `think-think` 结构
  - [x] 已显式声明“只暴露可见快照，不外显完整 CoT”
  - [x] `SKILL.md` 已改为回指 `references/type-strategies.md`
  - [x] `references/execution-flow.md` 已改为回指 `references/type-strategies.md` 对应章节
  - [x] `CONTEXT.md` 已记录本轮思维链升级 heuristic
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
- user_feedback_or_constraint: 用户明确指定使用最新 `think-think` 规范优化目标文件，并要求在当前 `3-分组` 内容基础上升级，而不是改写分组逻辑本身。

### Case-20260409-AIGC-PLAN-GROUPING-TIME-HANDOFF

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求把“分组时间切分机制”消化吸收后，按正确层级补到 `3-分组`，并明确区分类型与属性，不接受把原文大段粗暴粘进单一文件。
- root_cause_or_design_decision: 直接技术缺口不是 `3-分组` 缺少组时长概念，而是当前合同只有 `estimated_duration_seconds` 这类组级结果字段，缺少 episode frontmatter 对“默认组时长 / 非均匀组时长映射”的显式真源；同时帧级时间切分规则若直接塞进组模板，会造成阶段边界混淆。
- final_fix_or_extracted_heuristic: 将“默认组时长 + 分镜组时长映射”上升为 `第N集.md` 的 episode meta 合同，并让模板、主合同与 validator 校验其与 `estimated_duration_seconds` 一致；把 `X-Y秒`、场景类型化时长、节奏联动和 `FAIL-TIME-*` 失败码沉到 `scene-duration-projection.md`，作为下游 `5-分镜构图` 的时间切分交接协议。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已声明组总时长基线合同
  - [x] `references/type-strategies.md` 已声明全路由的组时长显式化规则
  - [x] `references/scene-duration-projection.md` 已接住帧级切分交接协议
  - [x] `references/output-template.md` 已补齐时间基线落点说明
  - [x] `templates/grouped-episode.md` 与 `templates/validation-report.md` 已补 timing 基线槽位
  - [x] `validate_grouping.py` 已校验 frontmatter 基线与组时长一致性
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/scene-duration-projection.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/grouped-episode.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/validation-report.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
- user_feedback_or_constraint: 用户明确要求“如已有相关内容不必赘述，仅作缺失补全”，并要求补全部分必须是真正消化吸收后的融合与分配，而不是直接大段插入。
