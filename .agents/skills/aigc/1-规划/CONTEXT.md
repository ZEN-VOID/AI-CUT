# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划` 阶段的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/1-规划/SKILL.md` 时，应自动预加载本文件。
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
| `1-规划` 目录存在但父级 `SKILL.md` 为空 | 阶段合同层 | 先补父级阶段合同，锁定子路径路由与落点 | 让所有规划子路径都从父级显式可达 | 父级能明确说明进入哪个子路径 |
| 子技能已存在内容，但父级没有入口 | 父子路由层 | 回写父级路由矩阵与 Mermaid 总览 | 形成“父级总入口 + 子级实质合同”结构 | 从父级可定位唯一子入口 |
| 直接照抄参考仓路径，导致落点不适配当前 `projects/` 体系 | 真源继承层 | 将能力继承与路径合同拆开，只迁移能力，不复制旧路径 | 在子技能中明确当前仓的 canonical landing | 产物全部落到当前项目运行时指定目录 |
| 规划阶段越权替下游阶段做细节真源 | 阶段边界层 | 收回到结构规划、格式规划、分组规划的边界 | 在父级和子级合同都显式声明“不拥有”范围 | 规划产物可交给下游继续消费，而不是代替下游 |
| `2-格式` 已有变体目录，但缺少父级裁决与默认分支 | 变体路由层 | 先补 `2-格式` 父级合同，再写 `标准剧/解说剧` 子技能 | 固化“父级裁决变体，子级细写合同” | 不再出现空壳变体目录 |
| 项目已启用顾问团，但规划阶段未读取 `team.yaml` | 共享运行时层 | 执行前先读项目根 `team.yaml` 与 `_shared/council-runtime/module-spec.md` | 在 `1-规划` 根技能固化 `策划前置 + 评审闸门` 合同 | 规划任务进入前能判断是否要启用顾问团 |
| 分组后节奏治理仍挂在 `2-组间` | 阶段边界层 | 将其迁回 `1-规划/subtypes/4-节奏`，并让 `0-Init.original_adherence` 直接作为规划阶段执行门 | 固化 `1-规划` 的第 4 个串行子路径，避免 `3-分组 -> 2-组间` 之间出现错位真源 | 分组后的节奏产物统一落到 `projects/<项目名>/规划/4-节奏/` |
| `1-规划` 结束后没有为后续共享 episode 根文件留下稳定入口 | 运行时真源层 | 让 `1-分集` 先登记 `bootstrap_output` 与 `source_profile` handoff，再由 `2-组间` 首次进入时自动创建 `projects/<项目名>/编导/第N集.json` | 把 `_shared/project-runtime-layout.md` 与 bootstrap template 作为跨阶段 shared carrier，并让 `2-组间` 拥有缺文件自动建根责任 | `2-组间` 与 `3-明细` 都围绕同一根文件工作，但规划阶段不再过早落空壳 |
| 规划阶段默认假设“故事主源已经存在”，导致 `1-分集` 缺少显式阻塞门 | 共享输入真源层 | 在 `1-规划` 根技能增加 `Story Source Gate`，统一读取 `Init/story-source-manifest.yaml` | 把故事源缺失提示上收到 `_shared/story-source-contract.md`，由父级先挡住 `1-分集` | 进入 `1-分集` 前能先判断是否具备增量进入条件与整季完成条件 |
| 上游其实是分镜脚本，但 `1-规划` 仍按小说原文型处理 | 根级类型策略层 | 在根技能建立 `storyboard_script` 双来源矩阵，并把预设保护模式回写到 `source_profile` | 用根层 `references/type-strategies.md` + shared manifest/schema 固化“保留并扩写”链路 | `3-明细` 能读取并顺着预设扩写，而不是重写预设 |
| `1-规划` 跑完后只剩各子路径 sidecar，没有 `规划/第N集.md` 主稿 | 父级聚合合同层 | 在父技能建立 `规划/第N集.md` 作为唯一集级规划主稿，并让 `1-分集/2-格式/3-分组` 只提供聚合输入 | 用父级输出模板 + 聚合流程 + 子路径回指规则固化“父级汇总、子级 sidecar”机制 | `2-组间` 与 `3-明细` 能默认直接读取 `规划/第N集.md` |
| 混合源约束只写进 handoff，`规划/第N集.md` 看不出 mixed 属性，且镜号被误写成场景号 | 父级聚合 + 格式模板层 | 在父级主稿与 `2-格式` 结果稿顶部显式投影 `source_profile`，并把 `场景号` 改回连续时空编号、`镜号/锚点` 独立保留 | 用父级模板、执行流与检查清单固化“source profile 可见化 + scene/shot 去混淆” | `规划/第N集.md` 顶部能直接看见混合源画像，同一连续时空跨组时使用 `场景X（续）` 而不是新场景号 |
| 根技能同时保留 `references/output-template.md` 和 `templates/planned-episode.md` 两份主稿骨架 | 根级真源治理层 | 把 `planned-episode.md` 并回 `references/output-template.md`，删除平行模板文件 | 固化“父级主稿骨架只在根级 output-template 唯一化” | 根级 `1-规划` 不再存在第二份 `规划/第N集.md` 模板真源 |
| 父级 `规划/第N集.md` 几乎与 `2-格式/第N集.md` 同稿 | 父级聚合投影层 | 让 `2-格式` 回到 scene-first draft，并要求父级显式投影 `3-分组` 的 compact group summary | 固化“父级主稿 != 2-格式拷贝稿，必须体现组级消费价值” | 父级主稿至少多出每组的目标/锚点/约束投影 |
| 已执行子路径的 validator 未过，但父级 `规划/validation-report.md` 仍写成 `PASS` | 父级验收闸门层 | 先回查失败子路径并重跑本地 validator，再重写阶段报告 | 在父级 `1-规划/SKILL.md` 固化“所有已执行子路径 gate 先通过，阶段级结论才可写 PASS” | 任何一次父级结案前，都能用子路径 validator 结果复核 |

## Repair Playbook

1. 先检查父级 `1-规划/SKILL.md` 是否具备阶段定位、子路径路由与落点合同。
2. 再检查具体子路径是否已有可执行 `SKILL.md + CONTEXT.md`。
3. 若目标是 `2-格式`，继续检查父级是否已写清 `标准剧/解说剧` 的默认与进入条件。
4. 若参考仓可借鉴，只继承高价值能力和验证结构，不直接复制旧仓路径。
5. 先让父级能路由到子级，再细化子级内容。
6. 新经验优先沉淀在最窄作用域；跨子路径共性再向上晋升。

## Reusable Heuristics

- 对多子路径规划阶段来说，最常见的问题不是“子技能写得不够多”，而是父级没有入口，导致子技能变成孤岛。
- 从参考仓继承技能时，能力结构可以借，路径合同必须重写到当前仓的 canonical landing。
- `1-规划` 最稳的职责边界是“给结构，不替下游拍板表现细节”。
- 对 `2-格式` 来说，父级最重要的职责不是写某个变体的细节，而是先做唯一变体裁决。
- 只要某个能力的直接输入已经是 `3-分组` 产物，它就应优先归入 `1-规划`，而不是继续挂在 `2-组间` 假装自己是导演层真源。
- 如果用户没有显式给出“旁白主导/解说剧”信号，规划阶段默认先走 `标准剧`，通常更稳。
- 对 `1-规划` 来说，顾问团最稳的节奏是“策划先给结构建议，评审最后卡 validation gate”，不要三角色同时抢答。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 当后续多个阶段都要围绕同一集文件持续 patch 时，`1-规划` 最稳的做法不是只写报告，而是先把空的 runtime root file 创建出来。
- 若某个规划子路径的进入前提取决于共享输入真源，最稳的拦截层应在 `1-规划` 父级，而不是让叶子技能各自临时追问。
- 只要主故事源已经覆盖到至少一段连续正文，`1-规划` 就不应再把整个分集入口判死；更合理的做法是允许增量规划，并把“整季未完备”单独标红。
- 当项目把正文运行时目录改名为 `故事/` 时，父级 `1-规划` 应优先回写 shared contract 和 manifest，而不是只改单个项目路径。
- 若主故事源直接是分镜脚本，`1-规划` 最稳的职责不是“小说化清洗”，而是先把预设点变成下游可消费的受保护约束，再允许 `3-明细` 顺着这些点扩写。
- 多子路径父技能如果没有单集主稿，执行越完整，产物反而越分散；这类问题优先补父级聚合真源，不要继续给子路径加报告。
- 对混合源主稿来说，最容易丢的不是 `source_profile` 有没有写进 JSON，而是有没有显性投影到人能直接读到的 `规划/第N集.md`。
- 组号解决的是执行容器，场景号解决的是连续时空；两者不能互相顶替，尤其不能把镜号直接升格为场景号。
- 对父级根技能来说，`references/output-template.md` 已经承担主稿写位真源时，就不要再额外保留一个 `templates/*.md` 平行骨架；否则极容易形成“改了一边、忘了另一边”的双真源。
- 父级 `规划/第N集.md` 若和 `2-格式/第N集.md` 只差一层文件路径或一行节奏说明，通常说明聚合没有真正消费 `3-分组`，而只是把 scene draft 换壳。
- 父级 `规划/validation-report.md` 不能替代子路径 validator；只要某个已执行子路径仍是 FAIL，父级阶段结论就必须停在返工或阻塞。

### Case-20260411-AIGC-PLANNING-PARENT-VS-FORMAT-DRAFT

- milestone_type: source_contract_change
- symptom_or_outcome: 当前项目的 `规划/第1集.md` 与 `规划/2-格式/第1集.md` 几乎完全相同，父级主稿没有体现 `3-分组` 的额外价值。
- root_cause_or_design_decision: 直接技术原因不是 `3-分组` 不存在，而是 `2-格式` 子稿越权长成半聚合稿，父级聚合合同又只要求“写入 G 边界”，没有要求 compact group projection。
- final_fix_or_heuristic: 把 `2-格式` 锁回 scene-first draft，并把父级主稿的 group projection 明确提升为 `组目标 / 结构锚点 / 交接约束` 三项 compact summary。
- prevention_or_replication_checklist:
  - [x] `2-格式` 已补“不写 G 组容器”硬规则
  - [x] 根级 `output-template.md` 已补 compact group summary 骨架
  - [x] 根级 `execution-flow.md` 已补父级聚合判定
- evidence_paths:
  - `.agents/skills/aigc/1-规划/references/output-template.md`
  - `.agents/skills/aigc/1-规划/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `projects/嫡母重生：过继局/规划/第1集.md`
  - `projects/嫡母重生：过继局/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确指出父级主稿“几乎与 2 阶段的完全一样”。

### Case-20260411-AIGC-PLANNING-ROOT-OUTPUT-TEMPLATE-CANONICALIZATION

- milestone_type: source_contract_change
- symptom_or_outcome: 根 `1-规划` 同时保留 `references/output-template.md` 和 `templates/planned-episode.md` 两份 `规划/第N集.md` 主稿骨架，破坏唯一真源。
- root_cause_or_design_decision: 直接技术原因不是主稿结构设计错误，而是父级在已经拥有 `references/output-template.md` 的前提下，又额外挂了一个平行模板文件，导致根级输出合同出现重复载体。
- final_fix_or_heuristic: 将 `planned-episode.md` 的骨架并回 `references/output-template.md` 的 `Planning Master Template` 段落，并删除根级平行模板文件，锁定“根主稿骨架只在 output-template 唯一化”。
- prevention_or_replication_checklist:
  - [x] `references/output-template.md` 已内联 canonical skeleton
  - [x] 根级 `templates/planned-episode.md` 已删除
  - [x] 所有根级回指已切回 `references/output-template.md`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/references/output-template.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“`.agents/skills/aigc/1-规划/templates` 也不需要重复定义，直接在 `references/output-template.md` 中唯一化”。

### Case-20260411-AIGC-PLANNING-SCENE-ID-AND-HYBRID-VISIBILITY

- milestone_type: source_contract_change
- symptom_or_outcome: `projects/嫡母重生：过继局/规划/第1集.md` 中，同一连续时空被按镜号错误拆成多个场景号，同时混合源约束只存在于 `manifest` / `第1集.json`，主稿本身看不出 mixed 属性。
- root_cause_or_design_decision: 直接技术原因是 `1-规划` 父级聚合模板与 `2-格式` 模板只有 `### 场景X` 骨架，没有把 `source_profile` 显性投影到主稿，也没有把“场景号绑定连续时空、镜号单独保留”写成硬规则。
- final_fix_or_heuristic: 在 `1-规划` 与 `2-格式` 的主模板、执行流和检查清单中，新增 `来源画像`、`镜号范围`、`锚点继承`，并规定混合源/分镜源下 `场景号` 只按连续时空编号；同一场景跨组续写时使用 `场景X（续）`。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已补“source_profile 可见化 + 场景号绑定连续时空”硬规则
  - [x] `1-规划/references/output-template.md` 已补 `来源画像` 与 `场景X（续）` 模板
  - [x] `1-规划/references/execution-flow.md` 已补聚合检查
  - [x] `2-格式` 父级与 `标准剧` 模板已补 `镜号范围 / 锚点继承`
  - [x] 当前项目 `规划/2-格式/第1集.md` 与 `规划/第1集.md` 已回写为混合源显性版本
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/references/output-template.md`
  - `.agents/skills/aigc/1-规划/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
  - `projects/嫡母重生：过继局/规划/2-格式/第1集.md`
  - `projects/嫡母重生：过继局/规划/第1集.md`
- user_feedback_or_constraint: 用户明确指出“相关空间场景和时间状态被错误分到不同场景号下”，并要求当前已选的混合模式必须在最终规划结果中留下可见痕迹。

### Case-20260411-AIGC-PLANNING-PARENT-MASTER-AGGREGATION

- milestone_type: source_contract_change
- outcome: 将 `1-规划` 从“子路径各自落盘 + 父级只写 validation-report”升级为“父级全链串行后汇总写回 `projects/<项目名>/规划/第N集.md` 的单集规划主稿”。
- root_cause_or_design_decision: 用户反馈 `1-规划` 执行后只产生一堆计划/规则 sidecar，缺少可直接给下游消费的核心文档；直接技术原因是父级合同只有子路径落点，没有父级集级聚合真源，且解释性报告默认全部保留。
- final_fix_or_heuristic: 父级 `1-规划` 默认全链执行应严格按 `1-分集 -> 2-格式 -> 3-分组`，并只在用户显式要求时追加 `4-节奏`；所有已执行子路径结果必须汇总为 `projects/<项目名>/规划/第N集.md`，同时将子路径报告降为非默认 sidecar。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已新增父级主稿与默认串行链合同
  - [x] `references/output-template.md` 已新增 `规划/第N集.md` 聚合模板说明
  - [x] `references/execution-flow.md` 已新增父级全链聚合流程
  - [x] `1-分集/2-格式/3-分组` 输出模板已补父级回指
  - [x] 当前项目已补 `projects/嫡母重生：过继局/规划/第1集.md`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/references/output-template.md`
  - `.agents/skills/aigc/1-规划/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `projects/嫡母重生：过继局/规划/第1集.md`
- user_feedback_or_constraint: 用户明确要求 `1-规划` 按子技能顺序执行，并在 `projects/<项目名>/规划/` 下输出经过分集与分组处理后的 `第N集.md` 核心文档；`4-节奏` 默认不选，只有显式强调时才执行。

### Case-20260410-AIGC-PLANNING-PARTIAL-STORY-SOURCE-ENTRY

- milestone_type: source_contract_change
- outcome: 修正了 `1-规划` 对故事源 gate 的过严解释，允许“至少一集原文”驱动覆盖范围内的增量分集，而不是把整个规划入口一起阻塞。
- root_cause_or_design_decision: 先前 `Story Source Gate` 只用了一个 `can_enter_episode_split` 布尔值承载全部语义，导致 manifest 在部分原文已就位时仍只能返回“未放行”。
- final_fix_or_heuristic: 父级 `1-规划` 应区分“允许进入增量分集”和“允许宣称整季正式分集完成”；前者只要求当前覆盖范围可证实，后者才要求整季边界可判定。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已新增增量 vs 整季的 gate 解释
  - [x] 项目 manifest 已要求写清 `split_scope`
  - [x] 项目摘要不再把“整季未齐”误写成“不能进入规划”
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/_shared/story-source-contract.md`
- user_feedback_or_constraint: 用户明确要求“原文至少有一集应就允许进入规划了”。

### Case-20260410-AIGC-PLANNING-STORY-DIR-RENAME

- milestone_type: source_contract_change
- outcome: 将 `1-规划` 依赖的项目级故事目录 canonical landing 同步到 `故事/`。
- root_cause_or_design_decision: 目录重命名若只改项目文件，不改父级规划合同，会导致 `1-规划` 继续把旧路径当作输入真源。
- final_fix_or_heuristic: 目录名变更时，先改 shared runtime layout 和 story-source contract，再改 `1-规划` 父级与项目 manifest，最后做物理重命名。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已同步新路径
  - [x] `1-规划/CONTEXT.md` 已记录重命名顺序
  - [x] 项目清单与摘要已改写到 `故事/`
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/_shared/story-source-contract.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“`projects/晴深不渝/故事源` 重命名为 `故事`（源层同步）”。

### Case-20260410-AIGC-PLANNING-RUNTIME-DIR-DERIVE

- milestone_type: source_contract_change
- outcome: 将 `1-规划` 阶段的 project runtime root 从带号目录收敛为无序号目录 `projects/<项目名>/规划/`。
- root_cause_or_design_decision: 先前阶段合同把技能名 `1-规划` 直接当成项目目录名，导致用户即使要求 runtime 去序号，规划阶段仍持续写回旧路径。
- final_fix_or_heuristic: 对项目路径，优先使用 `_shared/project-runtime-layout.md` 的“技能阶段 -> runtime 目录”映射，而不是从技能目录名直接推导项目路径。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已切到 `projects/<项目名>/规划/`
  - [x] team gate artifact 已同步到 `projects/晴深不渝/规划/validation-report.md`
  - [x] 物理目录已完成重命名
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `projects/晴深不渝/team.yaml`
- user_feedback_or_constraint: 用户明确要求 `projects/晴深不渝/1-规划` 不要序号。

## Case Log

### Case-20260411-AIGC-PLANNING-CHILD-GATE-BEFORE-STAGE-PASS

- milestone_type: source_contract_change
- symptom_or_outcome: 当前项目 `projects/嫡母重生：过继局/规划/validation-report.md` 曾写成 `PASS`，但 `规划/3-分组/第1集.md` 仍含 `error / warn-low`，且 `validate_grouping.py` 实跑失败。
- root_cause_or_design_decision: 直接技术原因不是 `3-分组` 缺少 validator，而是父级 `1-规划` 没把“已执行子路径 gate 先通过，阶段报告才可 PASS”写成显式验收闸门，导致执行层可能跳过子路径机检，直接写父级结论。
- final_fix_or_heuristic: 在父级 `1-规划/SKILL.md` 明确新增阶段 gate：所有已执行子路径的 validator / strict gate 必须先通过，父级才允许聚合并写 `规划/validation-report.md` 为 `PASS`；命中 `3-分组` 时明确运行 `validate_grouping.py`。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已补“子路径 gate 先于阶段 PASS”的硬规则
  - [x] `1-规划/SKILL.md` 已补命中 `3-分组` 时的 validator 命令
  - [x] `1-规划/CONTEXT.md` 已记录该失配模式与预防策略
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/scripts/validate_grouping.py`
  - `projects/嫡母重生：过继局/规划/validation-report.md`
  - `projects/嫡母重生：过继局/规划/3-分组/第1集.md`
- user_feedback_or_constraint: 用户要求“移除 `projects/嫡母重生：过继局/规划` 目录下全部内容并重新执行 `.agents/skills/aigc/1-规划`”，因此本轮先修父级 gate，再重跑规划产物。

### Case-20260409-AIGC-PLANNING-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划` 建立了父级阶段合同与经验层，并把 `1-分集` 接回到可路由的父级入口。
- root_cause_or_design_decision: 用户要求完善 `subtypes/1-分集`，但实际直接技术阻塞是父级 `1-规划/SKILL.md` 与 `CONTEXT.md` 均为空，导致子技能即使补齐也仍无上层入口。
- final_fix_or_heuristic: 先补父级 `1-规划` 的阶段定位、子路径矩阵、落点与闭环，再建设 `1-分集` 子技能；将 `2-格式`、`3-分组` 显式标为待补合同。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补齐阶段边界与路由
  - [x] 父级 `CONTEXT.md` 已建立
  - [x] `1-分集` 已成为父级可达入口
  - [x] 未完成子路径已显式标记为待补
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参照 `AIGC-ZEN-VOID` 的分集技能完善当前 `1-分集`，默认交互语言为中文。

### Case-20260409-AIGC-PLANNING-GROUPING-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划/subtypes/3-分组` 建立了正式子技能合同，并将父级 `1-规划` 的路由矩阵从“预留中”提升为可执行入口。
- root_cause_or_design_decision: 用户要求完善 `3-分组`，但直接技术阻塞是该子路径完全空白，同时父级 `1-规划/SKILL.md` 仍明确把它标为“目录已建，合同待补”，导致下游无法把它视为真实路由。
- final_fix_or_heuristic: 参照 `AIGC-ZEN-VOID` 中 `3-拍摄段落` 的“结构容器优先”思路，补出当前仓的 `3-分组/SKILL.md + CONTEXT.md`，并同步修正父级 `1-规划` 的子路径状态与硬规则；当前集粒度继续由 `1-分集` 决定。
- prevention_or_replication_checklist:
  - [x] `3-分组` 已补齐 `SKILL.md + CONTEXT.md`
  - [x] 父级 `1-规划` 已把 `3-分组` 标记为已建合同
  - [x] 当前仓仍坚持 `projects/<项目名>/规划/3-分组/` 作为子路径 landing，且主产物按 `第N集.md` 落盘
  - [x] 导演阶段专属字段未被误迁入规划阶段
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/3-拍摄段落/SKILL.md`
- user_feedback_or_constraint: 用户要求同时参考 `skill-通用创建`、`skill-编排优化`，并以 `AIGC-ZEN-VOID` 的 `3-拍摄段落` 作为参照源，但落地必须适配当前仓的规划阶段和中文合同。

### Case-20260409-AIGC-PLANNING-FORMAT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划/subtypes/2-格式` 建立了父级格式规划合同，并补齐 `标准剧 / 解说剧` 两个可执行变体子技能。
- root_cause_or_design_decision: 用户要求完善 `标准剧`、`解说剧`，但真正的源层缺口不是两个子目录本身，而是 `1-规划 -> 2-格式 -> 变体` 整条父子路由链尚未闭环。
- final_fix_or_heuristic: 先补 `2-格式` 父级 `SKILL.md + CONTEXT.md`，再分别补 `标准剧 / 解说剧` 的规划层合同与经验层，最后回写 `1-规划` 根级路由矩阵、落点与默认分支规则。
- prevention_or_replication_checklist:
  - [x] `1-规划` 根级已声明 `2-格式` 可执行
  - [x] `2-格式` 父级已建立唯一变体裁决合同
  - [x] `标准剧 / 解说剧` 已具备 `SKILL.md + CONTEXT.md`
  - [x] 默认分支与进入条件已写清
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/标准剧/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md`
- user_feedback_or_constraint: 用户明确要求以 `AIGC-ZEN-VOID` 的双变体结构为参照，但当前仓必须落到 `1-规划/2-格式` 的规划语境中。

### Case-20260409-AIGC-PLANNING-COUNCIL-RUNTIME

- milestone_type: source_contract_change
- outcome: 为 `1-规划` 根技能接入了基于项目根 `team.yaml` 的顾问团运行时，默认执行 `策划前置 -> 主代理草案 -> 评审闸门`。
- root_cause_or_design_decision: 用户要求进入 `1-规划` 根技能或其叶子技能时都先判断顾问团是否启用，并落实 `策划 / 评审` 职责；若只在 `0-Init` 记团队配置，规划阶段将无法稳定消费。
- final_fix_or_heuristic: 规划阶段的顾问团运行时不应各子技能自定义，而应由 `1-规划` 根技能读取项目根 `team.yaml` 并统一执行，子技能只继承。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已新增 `Council Runtime Contract`
  - [x] `2-格式` 已声明继承上层顾问团运行时
  - [x] 已固定 `策划前置 + 评审 validation gate`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `1-规划` 及其叶子技能进入时都先读取 `projects/<项目名>/team.yaml`，并默认启用 `策划 / 评审` 职责。

### Case-20260410-AIGC-PLANNING-RHYTHM-PROMOTION

- milestone_type: source_contract_change
- outcome: 将原 `2-组间/subtypes/节奏优化` 迁移为 `.agents/skills/aigc/1-规划/subtypes/4-节奏`，并把 `1-规划` 父级路由扩展为四个串行子路径。
- root_cause_or_design_decision: 用户要求“分组之后的产物，同样根据是否进行原作节奏保留执行与否”，直接技术原因是节奏治理实际依赖 `3-分组` 结果，却仍被放在 `2-组间`，导致阶段边界与执行门都错位。
- final_fix_or_heuristic: 把节奏治理上收为 `1-规划` 的第 4 个串行子路径，并沿用 `0-Init.original_adherence` 作为“是否保留原作节奏”的布尔门；同时从 `2-组间` 移除旧入口，避免双真源。
- prevention_or_replication_checklist:
  - [x] `1-规划` 根级路由已新增 `4-节奏`
  - [x] `4-节奏` 已具备 `SKILL.md + CONTEXT.md + references + agents/openai.yaml`
  - [x] `0-Init` 的节奏执行门已改为指向规划阶段
  - [x] `2-组间` 已移除旧入口并改为消费规划 handoff
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
- user_feedback_or_constraint: 用户明确要求把 `.agents/skills/aigc/2-组间/subtypes/节奏优化` 调整到 `.agents/skills/aigc/1-规划/subtypes/4-节奏`，并统一 `1-规划/subtypes` 的输出内容格式为 `.md`。

### Case-20260410-AIGC-PLANNING-BOOTSTRAP-DIRECTOR-ROOT

- milestone_type: source_contract_change
- outcome: 将 `1-规划` 的项目级运行时升级为“以 `projects/<项目名>/规划/` 承接父级阶段产物与验收，同时允许 `1-分集` 在 `Init/` 写 bootstrap 产物，并在分集确定后立即创建 `projects/<项目名>/编导/第N集.json` 根文件”。
- root_cause_or_design_decision: 用户明确要求后续 `2-组间` 与 `3-明细` 都围绕一个统一 JSON 根文件工作；若 `1-规划/1-分集` 不先创建这个文件，后续阶段只能继续各自生成自己的 episode 真相。
- final_fix_or_heuristic: 将目录真源上收至 `.agents/skills/aigc/_shared/project-runtime-layout.md`，并把 `1-规划` 的阶段根目录固定为 `projects/<项目名>/规划/`；其中仅 `1-分集` 在落 `Init/episode-split-*` 的同时，按 bootstrap template 批量创建 `projects/<项目名>/编导/第N集.json`。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已改写到 `1-规划/`
  - [x] `1-分集/SKILL.md` 已声明 bootstrap `编导/第N集.json`
  - [x] shared runtime layout 已建立
  - [x] 后续阶段已回指同一根文件
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“`1-规划/subtypes/1-分集` 阶段随着分集的确定，索性就把这个 json 的空内容文件落了”。

### Case-20260411-AIGC-PLANNING-DUAL-SOURCE-TYPING

- milestone_type: source_contract_change
- outcome: 为 `1-规划` 根技能补齐了 `references/` 四件套，并把故事主源从“默认小说原文型”升级为“叙事原文型 / 分镜脚本型 / 混合型”的正式类型矩阵。
- root_cause_or_design_decision: 直接技术阻塞不在 `1-分集` 局部，而在 `1-规划` 根层缺少 `references/type-strategies.md` 与 shared handoff，导致 storyboard source 的预设点只能停留在经验判断，无法稳定交给 `3-明细` 顺承。
- final_fix_or_heuristic: 先在根技能建立双来源类型矩阵，再把 `source_type / preset_retention_mode / detail_expansion_mode / locked_preset_axes` 接到 `story-source-manifest.yaml` 与 bootstrap `第N集.json.metadata.source_profile`，让 `3-明细` 默认执行“preserve and extend”。
- prevention_or_replication_checklist:
  - [x] `1-规划` 根层已补 `references/chain-of-thought.md`
  - [x] `1-规划` 根层已补 `references/execution-flow.md`
  - [x] `1-规划` 根层已补 `references/type-strategies.md`
  - [x] `1-规划` 根层已补 `references/output-template.md`
  - [x] shared story-source contract 与 bootstrap handoff 已加入 storyboard source 保护链
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/references/type-strategies.md`
  - `.agents/skills/aigc/_shared/story-source-contract.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户明确要求“把 `1-规划` 从默认小说原文上游，升级为同时支持小说原文型和分镜脚本型的类型化处理，并保证后续 `3-明细` 顺着预设点继续扩写”。

### Case-20260411-AIGC-PLANNING-EPISODE-SPLIT-SIDECAR-DEFAULT

- milestone_type: source_contract_change
- outcome: 将 `1-分集` 的本地可读 sidecar 从“手动补件”上收为父级 `1-规划` 默认保留集的一部分，保证直达子路径与父级全链都默认生成 `projects/<项目名>/规划/1-分集/第N集.md`。
- root_cause_or_design_decision: 直接技术原因不是 sidecar 模板不存在，而是父级 `1-规划` 的默认最小输出集、保留策略与 `1-分集` 执行流没有一起改写，导致合同层仍把 sidecar 视作按需补件。
- final_fix_or_heuristic: 只要某个子路径 sidecar 既承担人工核读价值、又不与父级主稿竞争真源，就应同时写进父级保留集、父级输出清单与子路径执行流；缺一项都会回漂成“存在模板但默认不产出”。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已把 `规划/1-分集/第N集.md` 纳入默认保留集
  - [x] `1-规划/references/output-template.md` 已把该 sidecar 纳入 minimal output checklist
  - [x] `1-分集` 执行流已把 sidecar 改成默认落盘结果，而不是手工补件
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/references/execution-flow.md`
- user_feedback_or_constraint: 用户明确指出 `规划/第N集.md` 与 `规划/1-分集/第N集.md` 并不冲突，后者应作为 `1-分集` 的默认可读落点存在。

### Case-20260411-AIGC-PLANNING-DEFER-DIRECTOR-ROOT-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 将 `编导/第N集.json` 的首次创建责任从 `1-规划/1-分集` 后移到 `2-组间` 首次进入时，规划阶段只保留 `bootstrap_output` 目标路径与 `source_profile` handoff。
- root_cause_or_design_decision: 用户指出 `编导/第N集.json` 真正稳定的最小骨架应建立在“分组已完成”的前提上；直接技术原因是旧合同为了尽早统一根文件，把规划阶段也拉进了建根责任，导致规划期出现“空壳先落、后面再补”的过早落盘。
- final_fix_or_heuristic: 若某共享根文件的最小稳定结构依赖更后阶段已经成立的容器信息，就不应在更早阶段提前落盘；更稳的做法是让上游只登记目标路径与 handoff，由真正首次消费该根文件的下游阶段自动创建。
- prevention_or_replication_checklist:
  - [x] `_shared/project-runtime-layout.md` 已将建根责任改到 `2-组间`
  - [x] `1-规划/SKILL.md` 与 `references/*` 已去除规划阶段默认建根
  - [x] `2-组间` 已接管“缺文件即自动 bootstrap”的责任
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/references/execution-flow.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
- user_feedback_or_constraint: 用户明确提出“`编导/第N集.json` 应该在分组之后确定，或无必要的话就不在规划阶段落盘，等到 2-编导阶段再自动落盘”。
