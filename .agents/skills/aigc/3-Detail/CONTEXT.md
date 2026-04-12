# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-Detail` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/3-Detail/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-Detail` 还回指外置 `制作组` 合同 | 真源治理层 | 把 team / role / shared playbook 能力内收进 `SKILL.md + references/` | 在审计脚本中加入“禁止引用已删除制作组路径”检查 | `3-Detail` 文档与 audit 均不再引用旧路径 |
| 没有 `shot skeleton` 就直接补构图、表演、运镜 | 拓扑依赖层 | 强制 `shot_skeleton_engine` 先产出 `分镜ID / 时间段 / coverage` | 在 `IO_CONTRACT` 与 `execution-flow` 中固定 skeleton 先决门 | 其他能力链不再发明镜序 |
| 结构链、表演链、摄影链同时补同一字段导致冲突 | 字段 ownership 层 | 用 `_shared/IO_CONTRACT.md` 固定 owned fields 与 merge precedence | 将 ownership 与 precedence 提升为 shared I/O 真源 | 合并结果可稳定落到 schema |
| 炫技表达压过叙事清晰度 | 路由策略层 | 默认保守路由为 `叙事派 + 摄影总协调`，挑战方案只作条件对照 | 在 `type-strategies.md` 固定 default vs challenger 规则 | 运镜与摄影优先服务剧情任务 |
| 摄影链只写“电影感 / 冷暖对比 / 高级感”，缺少可执行光位与色彩判断 | 摄影维度合同层 | 在 `references/摄影美学.md` 中强制先回看项目级摄影底座，再拆成 `光位 / 组级光影推进 / 色彩心理 / 摄影总协调` 四段 | 在 `chain-of-thought.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md` 同步固定摄影链的串并结构与必答维度 | `摄影美学` 不再是抽象口号，且能解释组内光影如何推进 |
| 摄影知识库被当成“术语贴纸”，没有真正进入节点决策 | 知识库转译层 | 在 `摄影美学.md` 中增加显式 `命中摄影知识库` 节点，并要求产出 `cinematography_academy_hit_note` | 在 `SKILL.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md` 中把该 note 固定为摄影链前置证据 | 学院派知识会被转成当前镜组的布光/色彩决策，而不是标题堆砌 |
| 连续性复核与真源审计缺位，导致写回时放过漂移 | 汇流门层 | 把 `review -> audit -> writeback` 写成固定串行 gate | 在 `output-template.md` 与 audit 脚本中同步固化 | `validation-report.md` 与 `audit_report` 同步存在 |
| 旧制作组能力删除后，质量方法也被一起删没了 | 能力吸收层 | 将共享稳定性合同与创作方法整理进 `capability-playbook.md` | 用“内部能力链 + playbook 细则”的单技能结构替代 team/role docs | 细则仍可追溯，但不再依赖外置 agents |
| 角色表现写成泛情绪标签，镜头有人但人物不成立 | 角色表现规则层 | 先锁角色化表达通道，再把情绪落成习惯动作、下意识和可见微表情 | 在 `references/角色表现.md` 固定 `主轴 -> 个性/习惯/下意识 -> 可见信号 -> 叙事行为 -> 传神强化` 的串行链 | `角色表现` 字段能区分“这个角色怎么演”，而不只是“现在什么情绪” |

## Repair Playbook

1. 先判断问题出在输入/阶段门、scope/bootstrap、skeleton、并发 merge、还是 review/audit。
2. 若镜序不稳，先回到 `shot_skeleton_engine`，不要直接修后段字段。
3. 若字段打架，优先修 `_shared/IO_CONTRACT.md` 的 ownership 与 precedence，而不是手工裁判本轮 JSON。
4. 若 challenge 方案压过叙事，先回退到默认叙事路由，再决定是否保留对照 note。
5. 若输出又出现第二真源，优先修 `output-template.md` 与写回规则，只保留 `第N集.json`。
6. 若能力细则漂散，优先回收到 `references/capability-playbook.md`，不要重新长出平行角色文档。

## Reusable Heuristics

- `3-Detail` 的关键不在“多写镜头文字”，而在“先锁 skeleton，再让并发字段补全可被同一 schema 吃下”。
- 对这个阶段来说，最危险的不是内容贫乏，而是并发链失去 merge precedence。
- 结构链与表演链负责让镜头成立，运镜/摄影/转场链只负责在此基础上做 finish，而不是反向定义镜头主任务。
- `叙事派` 最稳的角色已经不是一个外置 agent，而是一条默认路由策略；挑战方案永远只能是条件对照。
- 运镜维度里“更酷”不是另起炉灶，而是先固定同一表现目标，再比较 2-3 个不偷换任务的镜头变体；只有额外收益明确时，才把其中一个升格为挑战案。
- 单技能知行合一最适合这种“最终只有一份 JSON，但中间有多条并发能力链”的阶段。
- 高质量方法不能跟着被删除的外置 agents 一起消失，必须在父 skill 的 reference 层重建为可追溯的能力手册。
- 当维度数已经达到 `分镜表现 / 角色表现 / 场景氛围 / 运镜手法 / 摄影美学 / 转场特效` 这种密度时，单一总手册只应保留共享规则，逐维度思行节点必须独立成文。
- `摄影美学` 最稳的写法不是直接堆“光影 + 色彩”形容词，而是先回看 `全局风格 / 类型指导 / 导演意图`，再把 `主光源 / 辅助光 / 逆光 / 照明类型 / 光影流动 / 色相 / 明度 / 饱和度 / 色温 / 色彩心理` 压成单一摄影判断。
- 若 `knowledge-base/电影学院派/电影摄影` 有高命中条目，最稳的用法不是“引用它”，而是先生成一份 `cinematography_academy_hit_note`，明确“命中哪条规则、转成了什么布光/色彩判断、放弃了什么不适用规则”。
- `分镜表现` 维度最稳的起手式不是先写构图，而是先锁组级节奏、关键节拍和镜头密度，再为每拍配景别、为每镜配焦点。
- 当 `分镜表现` 进入 shot-level 结构链时，`景别` 后面不要直接跳到 `焦点/空间轴线`；更稳的顺序是先锁 `主体/陪体/背景关系 -> 构图布局 -> 构图方式`，再收束到焦点、观看路径、空间与几何写回。
- 若用户或下游需要结构化镜头标签，最稳的落点不是新开平行字段族，而是把 `景别 / 镜头属性 / 镜头框架 / 镜头类型 / 镜头视角` 作为 `FIELD-DETAIL-05` 的 shot-level 描述子槽，由 `分镜表现` 统一统筹。
- 当 reference 模块内部已经存在明确的串行、并行、条件分支或回退链时，除了表格合同，还应补一段 Mermaid，把上游输入、节点拓扑、失败回跳和下游消费关系显式画出来。
- `角色表现` 如果只写“愤怒、悲伤、紧张”这类抽象词，几乎一定会丢掉人物辨识度；更稳的写法是先锁角色会怎样露馅、怎样硬撑、怎样下意识反应。
- 想让观众共情，不应先加大情绪词，而应优先增加“想压住却露出来”“想维持却失手”的可见身体细节，尤其是眉眼、呼吸、嘴角、肩颈与手部的小失控。

## Case Log

### Case-20260412-AIGC-DETAIL-ZXY-FUSION

- milestone_type: source_contract_change
- outcome: 将 `3-Detail` 从“父 skill + 制作组 subagents”重构为“单一知行合一 skill + references 细则分层”的复杂并发链。
- root_cause_or_design_decision: 旧结构虽然有完整能力面，但真源分裂在 `SKILL.md + team.md + 16 个角色 agent + 两份 shared 手册` 中；对当前阶段来说，主要复杂度来自并发补字段与汇流审计，而不是长期独立角色治理。
- final_fix_or_heuristic: 保留全部既有能力面，但把它们内收为 `shot_skeleton / structural_staging / performance / atmosphere / camera_movement / cinematography / transition_fx / continuity_review / source_audit` 九条内部能力链，并用 `SKILL.md` 承担骨架、`references/` 承担细则。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已改为单技能思行网络
  - [x] `references/` 已承接链路细则与能力手册
  - [x] `_shared/IO_CONTRACT.md` 已移除外置 agent 依赖
  - [x] 审计脚本已增加禁止旧制作组路径的检查
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/3-Detail/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求“根据知行合一规范编排，走复杂链路的骨架 / 细则分层；不再需要 `.codex/agents/aigc/制作组`；每一步从哪些方面着手要足够细致”。

### Case-20260412-AIGC-DETAIL-CAPABILITY-PRESERVATION

- milestone_type: new_success_class
- outcome: 删除外置制作组真源的同时，保留了分镜规划、构图、角色表现、运镜、氛围、摄影、转场、复核、审计的全部方法密度。
- root_cause_or_design_decision: 直接删 team/role docs 容易导致“机制统一了，但能力细则被削平”；真正需要保留的是方法和 merge logic，而不是角色文件本身。
- final_fix_or_heuristic: 最稳的做法是“主文档只保留网络骨架 + references/capability-playbook.md 承接逐能力步骤、门禁和回退”，这样既不回退到多智能体，也不损失高质量细则。
- prevention_or_replication_checklist:
  - [x] 能力矩阵已写入 `SKILL.md`
  - [x] 逐能力步骤已写入 `capability-playbook.md`
  - [x] 路由判型已写入 `type-strategies.md`
  - [x] 输出与审计闭环已写入 `output-template.md`
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/references/type-strategies.md`
  - `.agents/skills/aigc/3-Detail/references/output-template.md`
- user_feedback_or_constraint: 用户要求“内容和机制上全量参照现有配置，但根据知行合一的规范进行编排”。

### Case-20260412-AIGC-DETAIL-DIMENSION-SPLIT

- milestone_type: source_contract_change
- outcome: 将 `3-Detail` 的六个高复杂子领域进一步拆为独立 references，形成真正的“骨架 / 维度细则”双层结构。
- root_cause_or_design_decision: 单一 `capability-playbook.md` 已能承接共享规则，但六个维度各自都存在丰富子类型、节点门禁和回退逻辑；继续塞在一份文档里，会重新形成第二个“大而全真源”。
- final_fix_or_heuristic: 保留 `capability-playbook.md` 作为共享总则与跨维度协调器，并把 `分镜表现 / 角色表现 / 场景氛围 / 运镜手法 / 摄影美学 / 转场特效` 各自拆成独立 reference 文档，分别承载思维执行节点设计。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已回链六个维度模块
  - [x] `capability-playbook.md` 已降为共享总则与协调层
  - [x] 六个维度细则已各自独立落盘
  - [x] 审计脚本已将这些 references 纳入声明式引用检查
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/references/分镜表现.md`
  - `.agents/skills/aigc/3-Detail/references/角色表现.md`
  - `.agents/skills/aigc/3-Detail/references/场景氛围.md`
  - `.agents/skills/aigc/3-Detail/references/运镜手法.md`
  - `.agents/skills/aigc/3-Detail/references/摄影美学.md`
  - `.agents/skills/aigc/3-Detail/references/转场特效.md`
- user_feedback_or_constraint: 用户明确要求在 `references/` 中以六个专属维度展开思维·执行节点细节设计。

### Case-20260412-AIGC-DETAIL-CINEMATOGRAPHY-LIGHTING

- milestone_type: source_contract_change
- outcome: 将 `摄影美学` 从“光影 / 色彩”两段抽象子补丁，增强为“摄影底座回看 -> 光位与照明类型 -> 组级光影流动 -> 色彩心理 -> 摄影总协调”的可执行链。
- root_cause_or_design_decision: 旧摄影链能表达 final look，但还没有把 `全局风格 / 类型指导 / 导演意图` 的摄影承诺显式回收到节点前置，也没有把组级照明推进与色彩心理拆成稳定必答位，容易滑回抽象审美词。
- final_fix_or_heuristic: 先在 `references/摄影美学.md` 固定摄影链的串并结构，再同步修改 `chain-of-thought.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md`，让摄影维度既有局部细则，又有共享门禁承接。
- prevention_or_replication_checklist:
  - [x] `摄影美学.md` 已显式要求回看项目级摄影底座
  - [x] 光位、组级光影推进与色彩心理已成为摄影链必答维度
  - [x] 共享思维链、执行流与 I/O 合同已同步摄影链串并关系
  - [x] 最终写回仍收束到单一 `摄影美学` 字段，没有越权扩 schema
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/摄影美学.md`
  - `.agents/skills/aigc/3-Detail/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
- user_feedback_or_constraint: 用户要求把摄影美学中的灯光与色彩考量细化到可执行节点，并优先落在 `references` 专属模块中。

### Case-20260412-AIGC-DETAIL-CINEMATOGRAPHY-KB-HIT

- milestone_type: source_contract_change
- outcome: 将 `knowledge-base/电影学院派/电影摄影` 从可选背景材料提升为 `摄影美学` 链的显式前置命中节点。
- root_cause_or_design_decision: 仅在总合同里提“可命中学院派知识库”还不够，摄影链如果没有单独的知识命中与转译节点，最终容易退化为只读了知识库但没有改变布光和色彩决策。
- final_fix_or_heuristic: 在 `references/摄影美学.md` 中加入 `CP-3 命中摄影知识库`，并把 `cinematography_academy_hit_note` 接入 execution flow、shared I/O 与主技能骨架，使摄影知识直接参与后续光位与色彩分支。
- prevention_or_replication_checklist:
  - [x] `摄影美学.md` 已显式列出摄影知识库文件
  - [x] 已增加知识命中与转译节点
  - [x] `cinematography_academy_hit_note` 已进入执行流与 I/O 合同
  - [x] 质量门禁已禁止直接照抄学院派术语
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/摄影美学.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
- user_feedback_or_constraint: 用户明确说明他的意思是“把 `knowledge-base/电影学院派/电影摄影` 作为摄影美学思维·执行节点里的直接高命中参考来源”。 

### Case-20260412-AIGC-DETAIL-PERFORMANCE-EXPRESSIVITY

- milestone_type: source_contract_change
- outcome: 将 `角色表现` 维度从“情绪/动作/关系可见化”进一步增强为“角色化表达 + 行为推动叙事 + 微表情传神”的串行支链。
- root_cause_or_design_decision: 仅要求“可见表演”仍容易落成通用情绪模板，导致镜头有人物却缺少人物辨识度，也难把共情与叙事推进写进同一字段。
- final_fix_or_heuristic: 在 `references/角色表现.md` 中固定 `主轴 -> 个性/习惯/下意识 -> 可见信号 -> 叙事性行为 -> 传神强化 -> 越权清理` 的内部顺序，并把其对运镜/摄影的协同关系写入 `execution-flow.md` 与 `capability-playbook.md`。
- prevention_or_replication_checklist:
  - [x] `角色表现` 专属 reference 已加入角色化表达、动作叙事、共情强化与眉眼微表情节点
  - [x] `chain-of-thought.md` 已提升 `FIELD-DETAIL-07` 的判定口径
  - [x] `execution-flow.md` 已明确该支链“外并行、内串行”的执行方式
  - [x] `capability-playbook.md` 已明确与运镜/摄影的 side input 交接边界
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/角色表现.md`
  - `.agents/skills/aigc/3-Detail/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
- user_feedback_or_constraint: 用户要求在 `3-Detail` 的思维·执行节点中补入“个性化表现、习惯动作、下意识、动作推动叙事、形象生动与共情、强情绪与眉眼传神”等考虑，并优先落在 references 专属模块。
