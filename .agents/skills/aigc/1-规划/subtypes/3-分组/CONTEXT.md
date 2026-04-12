---
skill: aigc-planning-grouping
context_type: knowledge-base
last_updated: 2026-04-11
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
| 只写组名清单，没有边界裁决摘要与边界理由 | 裁决合同层 | 先补不可动约束、候选边界与终裁理由，再重写分组计划 | 把“先抽取约束，再做多维量化裁决”固化为硬规则 | `执行报告.md` 可解释为何这样分组 |
| 直接照抄旧仓路径，产物漂移到 `output/影片/...` | 路径合同层 | 重写到 `projects/<项目名>/规划/3-分组/` | 将当前仓 canonical landing 固化到主合同 | 所有产物落在当前项目工作区 |
| 把集内分组误写成 `第N组.md` 独立文件 | 输出粒度层 | 收回到对应 `第N集.md` 中写组级容器 | 固化“集粒度由 `1-分集` 决定，`3-分组` 只做集内分组” | 不再出现 `第N组.md`，且对应 `第N集.md` 内含分组表与组条目 |
| 分组只是平均切块，未考虑依赖与并行性 | 结构设计层 | 重跑边界评估与依赖分析 | 在 `FIELD-GRP-DEP-06` 固化串并行检查 | 可明确判断哪些组能并行、哪些需串行 |
| 只有 `SKILL.md + CONTEXT.md`，没有统一裁决 reference / template / validator 载体 | 真源机制层 | 补齐 `references/`、`templates/`、`scripts/validate_grouping.py` | 将裁决细则、模板骨架、校验入口都提升为单一真源 | `3-分组` 不再只是可读合同，而具备可执行机制骨架 |
| 组容器只有目标与范围，没有结构锚点、依赖说明和并行性判断 | 输出锚点层 | 在表格与组章节中补 `structure_anchor / dependency_note / parallelism` | 把这些字段纳入模板和 validator 的强制校验 | 下游无需重新猜“为什么这样分”和“先做哪组” |
| 量化合同是当前技能自己抽象的一套简化分数，而未继承参照源的场景顺序与字窗机制 | 量化真源层 | 把参照源的“场景顺序 + 时长策略 + 字窗公式 + 有效字数”投影为本技能 shared reference | 将 `scene-duration-projection.md` 设为量化真源，并让 `SKILL.md / references / templates / validator` 全部回指它 | `group_load_score` 降为二级摘要，量化硬门槛以投影 reference 为准 |
| 非均匀组时长只写在说明文字里，未显式落到 episode meta，导致下游把整集时长误当每组时长 | 时间基线层 | 在 `第N集.md` frontmatter 补 `默认组时长 / 分镜组时长映射`，并让 `estimated_duration_seconds` 与解析结果对齐 | 把组总时长基线固化进模板、reference 与 validator；帧级切分只作为下游交接合同，不在本阶段伪造 | 任一偏离默认值的组都能在 frontmatter 显式追溯到时长来源 |
| 外部分镜锚点没有进入分组层，导致 hard lock 被切断或 soft lock 无法解释 | 跨阶段预设继承层 | 在 `3-分组` 模板、reference 与 validator 中加入 `外部分镜锚点登记 + preset_anchor_policy` | 将 `preset_registry` 视为组边界前置真源，而不是只留给 `3-明细` 事后补救 | 每个组都能回答“继承了哪些外部锚点、为什么能拆/不能拆” |
| 量化字段已写出，但 `effective_text_chars / window_status` 与字窗公式不一致 | 量化校验层 | 先按 `scene-duration-projection.md` 重算状态，再修正当前组表 | 在 validator 中增加“按 `estimated_duration_seconds + pace_tier` 回推窗口并核对 `window_status`”的强校验 | `validate_grouping.py` 能直接拦下 `20秒 + 260字 + warn-high` 这类自相矛盾组合 |
| `warn` 状态仍被当作可落盘结果，或无证据写入非默认时长 | 严格 gate 层 | 收回到统一 `15秒`，并把非 `ok` 一律视作返工信号 | 将 “`window_status != ok` 不得落盘” 与 “无 `时长偏离证据` 不得写 `分镜组时长映射`” 固化进 reference、SKILL、template 与 validator | validator 会直接拒绝 `warn-*` 成稿与无证据时长 override |
| `effective_text_chars` 只是手填数字，未从混合源 / 分镜源正文真实回算 | 主源量化证据层 | 先按 `story-source-manifest.yaml -> primary_story_source.path` 和 `source_span` 镜号范围重算，再重写分组结果 | 将“命中 `storyboard_script / hybrid_story_text` 时强制主源回算”固化进 `scene-duration-projection.md`、执行流、模板与 validator | validator 会直接拒绝与主源回算不一致的 `effective_text_chars` |
| `3-分组` 明明应直接消费 `2-格式`，执行流/模板却仍把父级输入写成模糊 `规划/第N集.md`，并且 validator 不能读取 `.docx` 主源 | 输入链与校验入口层 | 将直接输入链显式收口为 `Init/episode-split-plan.json + 规划/2-格式/第N集.md`，并为 validator 补 `.docx + plain 镜号` 解析 | 把“`2-格式` 为直接业务输入、主故事源只作证据回算”固化进 `SKILL.md / execution-flow / template / validator` | 执行 `3-分组` 时不再误判为要重绕原始故事文件分组，且 validator 可在 `.docx` 项目上正常通过 |
| 把 `hard_lock` 误执行成“一锚一组”，导致同一锚点内已经形成独立 handoff 的连续子段被过度并组 | 锚点解释层 | 在保持锚点顺序和 owned axes 不变的前提下，允许同锚点内连续切分，并让各子组继续继承同一锚点 | 将 `hard_lock` 收口为“保护顺序与 owned axes”，而不是机械禁止一切组内连续切分 | 分组结果可以在不破坏锚点的情况下更细地匹配结构 handoff |

## Playbook

1. 先确认父级 `1-规划` 已把当前任务路由到 `3-分组`。
2. 先锁定 `Init/episode-split-plan.json` 已给出的集边界，再优先读取父级 `规划/2-格式/第N集.md` 的现有主稿，而不是重切分集。
3. 先锁定待分组材料与主目标，而不是直接平分组数。
4. 先抽取不可动约束，再生成候选边界。
5. 先做依赖与并行性检查，再把组级容器写回对应 `第N集.md`。
6. 若参考仓结构有用，只迁移“容器优先 + 可追溯闭环”，不迁移导演层专属字段和旧路径。
7. 若发现 `3-分组` 只有合同没有机制载体，优先补 `references/`、`templates/`、`scripts/validate_grouping.py`，再继续扩写内容。

## Reusable Heuristics

- `3-分组` 最容易出错的地方不是不会分，而是把“组”误写成松散目录建议，没有形成下游可消费的结构容器。
- `3-分组` 的真源粒度不是“组文件”，而是“集文件里的组容器”；只要长出 `第N组.md`，通常就说明越过了 `1-分集` 的边界合同。
- 从 `3-拍摄段落` 继承能力时，最该继承的是“先定容器、再写细节”的工程思路，而不是它的导演字段体系。
- 从 `3-拍摄段落` 继承量化机制时，不能只拿一个简化负载分；优先继承“场景顺序先行 + 时长策略优先级 + 节奏字窗 + 有效字数 + 尾组规则”这条主链。
- 对规划阶段来说，分组的价值不在“均匀”，而在“可交接、可并行、依赖清晰”。
- `3-分组` 一旦需要跨执行者稳定复现，就不能只靠 `SKILL.md` 大段正文；至少要把统一裁决 reference、模板和 validator 各落一个真源载体。
- 若一个组不能回答“它锚定哪段结构、依赖谁、能否并行”，那它通常还不算可交接的组容器。
- 规划阶段可以不落导演阶段全部字段，但量化规则层必须与参照源同源，再在当前阶段做字段投影，而不是重新发明另一套口径。
- 当主 `SKILL.md` 已经开始变成“厚合同”时，优先把流程、思维链、类型化策略、输出模板说明拆到标准 `references` 模块层，而不是继续在主文档里横向加章节。
- 当 `G1/G2/G3` 三个 sibling reference 长期同步修改时，应把它们并入单一 `type-strategies.md` 真源；路由差异适合做章节，而不适合继续做并列文件。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 对 reasoning 模型的思维链模块，不要把 `S1-S7` 写成“必须逐字外显”的流程剧本；应先用启发式工作链决定删什么、比什么、落到哪个字段，再把 `S1-S7` 作为可见支架。
- `3-分组` 的可见思维快照至少要暴露 `边界裁决摘要 + 候选边界 + 组容器落点 + Gate Summary`；如果只剩流程标题或完整内部推理全文，都会降低可审计性。
- “组总时长元数据”与“帧内时间切分规则”不是同一层：前者属于 `3-分组` 的 episode meta 真源，后者属于下游 `5-分镜构图` 的消费合同，适合沉在量化 reference 做交接。
- 外部分镜脚本若已有粗锚点，`3-分组` 的职责不是忽略它，而是先裁决“这根锚点是 hard lock、soft lock 还是 reference only”。
- `soft_lock + single_anchor_multi_shot` 最稳的处理，不是在本阶段强行细化成镜头，而是在组层明确登记“允许下游一锚多镜展开”。
- `3-分组` 的最小稳定输入链是 `Init/episode-split-plan.json + 规划/2-格式/第N集.md`；只有 `2-格式` 尚未执行时，才应临时回退到 `1-分集/第N集.md` 或其他已声明待分组材料。
- `3-分组` 的主稿输入与量化证据要分层：前者优先消费 `2-格式` 聚合稿，后者再从 `story-source-manifest.yaml -> primary_story_source` 回算 `effective_text_chars`。
- 当主故事源是 `.docx` 时，validator 不能假设它已经是 markdown bullet 稿；至少要同时兼容 `.docx` 段落提取与 plain `镜号 X` 分镜格式。
- `hard_lock` 保护的是顺序、边界主意图和 owned axes，不等于必须“一锚一组”；如果锚点内部已经出现更清晰的连续 handoff，可以在不破坏顺序的前提下拆成多个连续组。
- “写了 `effective_text_chars` 和 `window_status`”不等于量化已落实；至少还要检查它们是否能被 `estimated_duration_seconds + pace_tier` 的窗口公式反推一致。
- 在严格 gate 模式下，`warn-low / warn-high / error` 都不再是“可解释偏差”，而是“必须返工”的失败信号。
- 对 `storyboard_script / hybrid_story_text`，只要求“写了 `effective_text_chars`”还不够；如果 `source_span` 已经能指向镜号范围，就必须让 validator 从主源回算并复核。

## Case Log

### Case-20260411-AIGC-PLAN-GROUPING-UNIFIED-DECISION

- milestone_type: source_contract_change
- symptom_or_outcome: 用户明确指出 `3-分组` 把 `projected_group_ids` 与 `G1/G2/G3` 路由制绑得过紧，导致执行时固执地把 manifest 投影直接当最终分组真相。
- root_cause_or_design_decision: 直接技术原因不是量化字段不足，而是 `3-分组` 的方法论仍然要求先判 `G1/G2/G3`，把“上游预设、结构证据、依赖闭环、量化硬门槛、下游 handoff”拆成互斥主路由，进而放大了 `projected_group_ids` 的权重。
- final_fix_or_extracted_heuristic: 将 `3-分组` 从“路由制”收敛为“统一多维量化裁决”单一方法：先抽取不可动约束，再生成候选边界，再按结构、依赖、量化和 handoff 同时终裁；`projected_group_ids` 只保留为约束输入或追踪索引，不再直接等同正式组数。
- prevention_or_replication_checklist:
  - [x] `type-strategies.md` 已改为统一多维量化裁决真源
  - [x] `execution-flow.md` 已删除 `G1/G2/G3` 主裁决流程
  - [x] `chain-of-thought.md` 已改为暴露边界裁决摘要而非路由决议
  - [x] 模板与 validator 已改用 `grouping_method: multidimensional_quantized`
  - [x] 当前项目 `规划/3-分组/` 已按新合同回写
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/group-plan.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/grouped-episode.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/validation-report.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
  - `projects/嫡母重生：过继局/规划/3-分组/`
- user_feedback_or_constraint: 用户明确要求“分组根本不需要 `G1/G2/G3`，按照统一的多维度复合计算量化标准来执行就好了”。 

### Case-20260411-AIGC-PLAN-GROUPING-SOURCE-BACKED-EFFECTIVE-CHARS

- milestone_type: source_contract_change
- symptom_or_outcome: 用户质疑当前项目 `3-分组` 的 `effective_text_chars` 是“为了通过而作弊”的手填数字；复核发现 validator 只校验字段自洽，没有从故事主源回算。
- root_cause_or_design_decision: 直接技术原因不是 `effective_text_chars` 没写进合同，而是当前执行链只要求“有这个字段”，却没有把 `storyboard_script / hybrid_story_text` 下的主源回算变成强制 gate。
- final_fix_or_extracted_heuristic: 当主故事源是 `storyboard_script / hybrid_story_text` 且 `source_span` 可解析为镜号范围时，validator 必须从 `story-source-manifest.yaml -> primary_story_source.path` 读取主源，按镜号范围回算 `effective_text_chars`，不再允许纯手填。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已补“主源回算优先于手填”的硬规则
  - [x] `scene-duration-projection.md` 已补主源回算合同
  - [x] `execution-flow.md` 已补回算步骤
  - [x] `output-template.md` 与 `grouped-episode.md` 已补可机读 `source_span` 说明
  - [x] `validate_grouping.py` 已补主源回算校验
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/scene-duration-projection.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/grouped-episode.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
- user_feedback_or_constraint: 用户明确指出“怀疑是为了通过而作弊”，要求把这条缺口补成可执行 gate。

### Case-20260411-AIGC-PLAN-GROUPING-HARDLOCK-NOT-ONE-GROUP

- milestone_type: source_contract_change
- symptom_or_outcome: 用户指出当前项目里 `G01` 不应继续吞入场景2，且原 `G02` 的“重生选子与反向改局”再拆成两个分组更合适。
- root_cause_or_design_decision: 直接技术原因不是量化不成立，而是当前执行结果把 `hard_lock` 近似执行成“一锚一组”，过度放大了 `A01/A02` 的整锚点保留，压过了同锚点内部已经形成的连续结构 handoff。
- final_fix_or_extracted_heuristic: 将 `hard_lock` 的解释收口为“保护顺序与 owned axes，不等于禁止同锚点内连续切分”；当用户显式要求、且切分后 handoff 更清晰时，允许多个连续组共同继承同一锚点。
- prevention_or_replication_checklist:
  - [x] `type-strategies.md` 已更新 `hard_lock` 解释
  - [x] 当前项目 `3-分组/第1集.md` 已按 `镜1-4 / 镜5 / 镜6-7 / 镜8-10 / 镜11-13` 重裁
  - [x] `CONTEXT.md` 已补“hard_lock != 一锚一组”的经验
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `projects/嫡母重生/规划/3-分组/第1集.md`
- user_feedback_or_constraint: 用户明确指出“场景2开始就要进入到新的分组”“G02 重生选子与反向改局 拆成两个分组比较合适”。

### Case-20260409-AIGC-PLAN-GROUPING

- milestone_type: source_contract_change
- outcome: 参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/3-拍摄段落` 的结构容器思路，为当前 `aigc/1-规划/subtypes/3-分组` 建立了可执行子技能合同与经验层。
- root_cause_or_design_decision: 用户要求完善 `3-分组`，但当前仓的直接技术缺口不是“内容待补”，而是该子路径完全空白，且父级 `1-规划` 仍将其标记为“预留中”，导致无法成为正式路由入口。
- final_fix_or_heuristic: 把参考仓中高价值的“容器优先、主路由优先、证据闭环”迁入规划阶段，重写为 `G1/G2/G3` 分组主路由、`group-plan + 第N集 + 执行报告` 输出合同，并同步接回父级 `1-规划` 路由矩阵。
- prevention_or_replication_checklist:
  - [x] `3-分组/SKILL.md` 已建立完整子技能合同
  - [x] `3-分组/CONTEXT.md` 已建立经验层
  - [x] 路径合同已切换到 `projects/<项目名>/规划/3-分组/`
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
- final_fix_or_extracted_heuristic: 将 `3-分组` 的 canonical output 收回为 `projects/<项目名>/规划/3-分组/第N集.md`，在单集文件内部落盘分组表和组条目；`group-plan.md` 仅保留总览，不再承担组级真源。
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

### Case-20260411-AIGC-PLAN-GROUPING-PRESET-REGISTRY

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求当上游是外部分镜脚本时，`3-分组` 也要能回答“哪些锚点不能拆、哪些锚点可作为连续子组拆开”，而不是把全部压力留给 `3-明细` 事后修补。
- root_cause_or_design_decision: 直接技术缺口不是 `3-分组` 不会继承上游，而是此前 shared handoff 里没有 `preset_registry`，模板和 validator 也没有写位，导致外部分镜锚点只能停在口头约束。
- final_fix_or_extracted_heuristic: 将 `preset_registry` 接入 shared contract，并在 `3-分组` 的 `type-strategies / grouped-episode template / output-template / validate_grouping.py` 中正式增加 `外部分镜预设模式 + 外部分镜锚点登记 + preset_anchor_policy` 合同。
- prevention_or_replication_checklist:
  - [x] `3-分组/references/type-strategies.md` 已补锚点继承规则
  - [x] `templates/grouped-episode.md` 已补外部分镜锚点槽位
  - [x] `references/output-template.md` 已声明字段落点
  - [x] `scripts/validate_grouping.py` 已校验相关 frontmatter 与表格字段
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/grouped-episode.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户明确要求“把外部分镜脚本原有分镜设计的保留，以及我们 3-明细 的拆解拓展，做成真正的可执行合同”。

### Case-20260411-AIGC-PLAN-GROUPING-INPUT-CHAIN

- milestone_type: source_contract_change
- symptom_or_outcome: 父级 `1-规划` 已把 `1-分集` 的 child output 收口到 `Init/episode-split-plan.json`，但 `3-分组` 执行流和验证模板仍读取 `规划/1-分集/第N集.md`。
- root_cause_or_design_decision: 直接技术原因不是分组逻辑错误，而是 `3-分组` 的输入链仍停留在旧运行时路径，导致子技能间 handoff 失真。
- final_fix_or_extracted_heuristic: 将 `3-分组` 的固定输入链改为 `Init/episode-split-plan.json + 规划/第N集.md`，前者负责集边界真源，后者负责父级已聚合的当前集主稿。
- prevention_or_replication_checklist:
  - [x] `references/execution-flow.md` 已改为新输入链
  - [x] `templates/validation-report.md` 已移除旧 `规划/1-分集/` 路径
  - [x] `CONTEXT.md` 已补输入链 heuristic
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/validation-report.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求 `1-规划` 子技能顺序执行后，再统一汇总到 `projects/<项目名>/规划/第N集.md`。

### Case-20260411-AIGC-PLAN-GROUPING-QUANT-ENFORCEMENT

- milestone_type: source_contract_change
- symptom_or_outcome: 用户追问“分组规则是否真的按 `3-分组` 的详细量化细则落实”，复核发现当前项目 `第1集` 的 `G01` 写成 `20秒 / effective_text_chars=260 / window_status=warn-high`，与量化公式不一致。
- root_cause_or_design_decision: 直接技术原因不是没有量化字段，而是 validator 过去只校验字段存在、枚举值和时长映射，没有校验 `effective_text_chars -> window_status` 是否真能由 `estimated_duration_seconds + pace_tier` 反推出相同结论，导致“假量化”能静默通过。
- final_fix_or_extracted_heuristic: 在 `validate_grouping.py` 中增加窗口公式校验与组表/组章节一致性校验，按 `scene-duration-projection.md` 的字窗公式反推 `expected_window_status`，不再允许量化字段只写表面。
- prevention_or_replication_checklist:
  - [x] validator 已校验 `effective_text_chars` 为非负整数
  - [x] validator 已按 `estimated_duration_seconds + pace_tier` 反推 `window_status`
  - [x] validator 已校验组章节与分组计划表的量化字段一致
  - [x] `CONTEXT.md` 已记录“字段存在 != 量化落实”的失败类型
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/scene-duration-projection.md`
  - `projects/嫡母重生：过继局/规划/3-分组/第1集.md`
  - `projects/嫡母重生：过继局/规划/第1集.md`
- user_feedback_or_constraint: 用户强调关注点不是多余输出产物，而是“内容有没有真正落实量化细则”，并明确指出不能把看起来完整的表格误判成规则已执行。

### Case-20260411-AIGC-PLAN-GROUPING-STRICT-GATE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求把 `3-分组` 改成更严格的 gate：`warn` 不得继续落盘，非默认组时长必须有证据，且上浮空间从 `1.5x` 收紧到 `1.1x`。
- root_cause_or_design_decision: 直接技术原因不是量化公式缺失，而是旧合同默认允许“带理由的 warn 落盘”与“执行者推断式时长 override”，这会让结果看起来有规则，实则 gate 不够硬。
- final_fix_or_extracted_heuristic: 将 `hard_text_window` 上浮收紧到 `1.1x`，并把 `window_status != ok` 一律视作返工信号；同时新增 `时长偏离证据`，要求任何 `分镜组时长映射` 偏离都必须可追溯到上游证据。
- prevention_or_replication_checklist:
  - [x] `scene-duration-projection.md` 已收紧窗口上限到 `1.1x`
  - [x] `SKILL.md / type-strategies.md` 已声明 `warn` 不得正式落盘
  - [x] `templates/grouped-episode.md` 已加入 `时长偏离证据`
  - [x] validator 已拒绝非 `ok` 成稿与无证据时长偏离
  - [x] 当前项目 `第1集` 已收回到统一 `15秒` 基线
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/scene-duration-projection.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
  - `projects/嫡母重生：过继局/规划/3-分组/第1集.md`
- user_feedback_or_constraint: 用户明确要求“warn 不应继续落盘”“无证据不得偏离默认 15 秒”“1.5x 收缩为 1.1x”。

### Case-20260411-AIGC-PLAN-GROUPING-FORMAT-FIRST-DOCX-VALIDATOR

- milestone_type: source_contract_change
- symptom_or_outcome: 用户指出 `3-分组` 已经完成 `1-分集` 和 `2-格式`，因此本阶段应直接围绕 `规划/2-格式/第1集.md` 处理，而不是看起来又回到原始故事源重跑一遍。
- root_cause_or_design_decision: 直接技术原因不是业务链路错误，而是 `3-分组` 的执行流、模板和经验层仍把父级输入写成模糊 `规划/第N集.md`，同时 validator 在主源回算时默认把 `primary_story_source.path` 当 UTF-8 纯文本，未兼容当前项目实际使用的 `.docx + plain 镜号` 主源格式。
- final_fix_or_extracted_heuristic: 将 `3-分组` 的直接业务输入链显式收口为 `Init/episode-split-plan.json + 规划/2-格式/第N集.md`，把主故事源降为量化证据层；同时为 validator 增加 `.docx` 提取和 plain `镜号 X` 分镜解析能力，避免 source-backed 校验把证据层误表现为第二条主执行链。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已声明 `2-格式` 为默认直接输入
  - [x] `references/execution-flow.md` 已改为优先读取 `规划/2-格式/第N集.md`
  - [x] `templates/validation-report.md` 已改正输入清单示例
  - [x] `validate_grouping.py` 已兼容 `.docx` 主源与 plain `镜号` 格式
  - [x] `CONTEXT.md` 已补“主稿输入 / 量化证据分层”经验
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/templates/validation-report.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
- user_feedback_or_constraint: 用户明确指出“已经进行了分集和格式处理，那 3-分组 直接围绕 2-格式 的结果处理不就行了”。 
