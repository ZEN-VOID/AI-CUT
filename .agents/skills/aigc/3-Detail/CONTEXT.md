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
- last_checked_at: 2026-04-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-Detail` 还回指外置 `制作组` 合同 | 真源治理层 | 把 team / role / shared playbook 能力内收进 `SKILL.md + references/` | 在审计脚本中加入“禁止引用已删除制作组路径”检查 | `3-Detail` 文档与 audit 均不再引用旧路径 |
| shared episode root 仍把 `thinking_chain` 当标准输出 | 输出合同层 | 从 shared schema、bootstrap template、示例与 writeback 文档中移除必填要求，并删除当前项目 root 中该字段 | 固定 canonical 输出为 `metadata + final_output` 双槽；`thinking_chain` 只保留兼容旧 root 的可选定义 | rerun 后的新 root 默认不再生成 `thinking_chain` |
| 没有 `shot skeleton` 就直接补构图、表演、运镜 | 拓扑依赖层 | 强制 `shot_skeleton_engine` 先产出 `分镜ID / 时间段 / coverage` | 在 `IO_CONTRACT` 与 `execution-flow` 中固定 skeleton 先决门 | 其他能力链不再发明镜序 |
| 分镜组镜数异常整齐，几乎都落成 `2 镜` | 密度裁决层 | 先检查是否把 `tail-hook` 预映误算成本组 beat，及是否沿用了共享样例的双镜粒度 | 在 `分镜表现.md`、`execution-flow.md` 与 `capability-playbook.md` 固定 `hook preview != canonical beat`，并增加 `密度同质化` 返工门 | 同一集多数分镜组同镜数时会触发复核，而不是直接通过 |
| 分镜密度只靠经验判断，缺少可量化基准 | 密度合同层 | 将镜数裁决改写为 `候选节拍 -> 推荐镜数基准 -> 最终分镜数` 的联合公式，并加入时长窗口 | 在 `分镜表现.md`、`execution-flow.md`、`chain-of-thought.md` 与 `capability-playbook.md` 固定动作阶段点/气口点/焦点切换点/结构转折点，以及格式档位抬升 | `shot_count_decision` 能回溯到量化字段，而不是停留在主观描述 |
| 结构链、表演链、摄影链同时补同一字段导致冲突 | 字段 ownership 层 | 用 `_shared/IO_CONTRACT.md` 固定 owned fields 与 merge precedence | 将 ownership 与 precedence 提升为 shared I/O 真源 | 合并结果可稳定落到 schema |
| 炫技表达压过叙事清晰度 | 路由策略层 | 默认保守路由为 `叙事派 + 摄影总协调`，挑战方案只作条件对照 | 在 `type-strategies.md` 固定 default vs challenger 规则 | 运镜与摄影优先服务剧情任务 |
| 摄影链只写“电影感 / 冷暖对比 / 高级感”，缺少可执行光位与色彩判断 | 摄影维度合同层 | 在 `references/摄影美学.md` 中强制先回看项目级摄影底座，再拆成 `光位 / 组级光影推进 / 色彩心理 / 摄影总协调` 四段 | 在 `chain-of-thought.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md` 同步固定摄影链的串并结构与必答维度 | `摄影美学` 不再是抽象口号，且能解释组内光影如何推进 |
| 摄影知识库被当成“术语贴纸”，没有真正进入节点决策 | 知识库转译层 | 在 `摄影美学.md` 中增加显式 `命中摄影知识库` 节点，并要求产出 `cinematography_academy_hit_note` | 在 `SKILL.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md` 中把该 note 固定为摄影链前置证据 | 学院派知识会被转成当前镜组的布光/色彩决策，而不是标题堆砌 |
| 连续性复核与真源审计缺位，导致写回时放过漂移 | 汇流门层 | 把 `review -> audit -> writeback` 写成固定串行 gate | 在 `output-template.md` 与 audit 脚本中同步固化 | `validation-report.md` 与 `audit_report` 同步存在 |
| 旧制作组能力删除后，质量方法也被一起删没了 | 能力吸收层 | 将共享稳定性合同与创作方法整理进 `capability-playbook.md` | 用“内部能力链 + playbook 细则”的单技能结构替代 team/role docs | 细则仍可追溯，但不再依赖外置 agents |
| 角色表现写成泛情绪标签，镜头有人但人物不成立 | 角色表现规则层 | 先锁角色化表达通道，再把情绪落成习惯动作、下意识和可见微表情 | 在 `references/角色表现.md` 固定 `主轴 -> 个性/习惯/下意识 -> 可见信号 -> 叙事行为 -> 传神强化` 的串行链 | `角色表现` 字段能区分“这个角色怎么演”，而不只是“现在什么情绪” |
| 对手戏引用电影学院派知识时只停在“像某种经典场面” | 对手戏参考转译层 | 先做高命中检测，再把母型压成攻守、距离、障碍、逼近/退让等表演策略 | 在 `角色表现.md` 固定 `对手戏高命中检测` 条件节点，只允许输出 `dialogue_scene_reference_note` | 对手戏参考能被消费为行为策略，而不是空泛致敬或越权摄影描述 |
| 运镜层直接复用学院派分镜知识时，容易和 `分镜表现` 抢夺镜头设计权 | 运镜-结构边界层 | 把学院派分镜脚本命中检测放到 `camera_movement_engine` 的“默认路线与动机”之后，只允许输出 `camera_academy_hit_note`，再由默认 patch 吸收 | 在 `运镜手法.md`、`execution-flow.md`、`chain-of-thought.md`、`IO_CONTRACT.md` 与主 `SKILL.md` 中同步固定其为条件串行节点，并声明只处理运动语法 | 学院派分镜知识会增强运动策略，而不会变成第二次构图/空间裁决 |

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
- `摄影美学` 最稳的写法不是直接堆“光影 + 色彩”形容词，而是先回看上游 `组间设计.全局风格 / 类型元素 / 导演意图`，再把 `主光源 / 辅助光 / 逆光 / 照明类型 / 光影流动 / 色相 / 明度 / 饱和度 / 色温 / 色彩心理` 压成单一摄影判断。
- 若 `knowledge-base/电影学院派/电影摄影` 有高命中条目，最稳的用法不是“引用它”，而是先生成一份 `cinematography_academy_hit_note`，明确“命中哪条规则、转成了什么布光/色彩判断、放弃了什么不适用规则”。
- 若 `knowledge-base/电影学院派/分镜脚本` 在运镜层有高命中条目，最稳的用法不是重做一次镜头设计，而是先锁默认路线与动机，再生成 `camera_academy_hit_note`，只提炼“怎么动、为什么这样动、哪些条目不适用”。
- 对 `3-Detail` 来说，最稳的第一结构化输入不再是 `2-Global/*.md`，而是 `2-Global` 已 seed 的 shared episode root；长文本 Markdown 只应作为兼容回退或审计证据。
- 若 shared episode root 已经能用 `metadata + final_output` 表达 business truth，就不要再为“可见收束说明”强挂一个 `thinking_chain` 槽；这类说明最多保留在兼容层，而不应继续占据 canonical 输出合同。
- `分镜表现` 维度最稳的起手式不是先写构图，而是先锁组级节奏、关键节拍和镜头密度，再为每拍配景别、为每镜配焦点。
- 当 grouped script 带有 `tail-hook` 借入段时，最稳的做法是先把它记成 `hook preview`，而不是直接当作本组新增节拍；只有当前组确实需要“余波 / 预感 / 将收未收”的单独落点时，才给它分镜配额。
- 共享 phase 示例只可复用字段组织和 patch 粒度，不可复用镜头数量；如果一集里大多数组都被写成同一镜数，优先怀疑隐性模板污染，而不是先假设“这就是成熟节奏”。
- 分镜密度最稳的口径不是“一拍一镜”，而是先把 `动作阶段点 / 台词气口点 / 焦点切换点 / 结构转折点` 汇成 `候选节拍`，再经过 `节奏系数 + 格式档位 + 拆镜加权 - 合镜折减 + 组时长窗口` 联合裁决。
- 当项目目标明确偏向短剧、漫剧或强节奏笑点内容时，节奏系数可以比常规电影化短片更激进；但这种上调应写成公开档位，而不是执行时临场偷加速。
- `standard_film / short_drama / comic_page` 应作为公开格式档位；当前默认档已提升为 `short_drama = 1.2`。若项目被写成 `概念短片 + 观察式生活喜剧`，且没有额外稀疏镜数说明，也应继续归到 `short_drama`。
- 当 `分镜表现` 进入 shot-level 结构链时，`景别` 后面不要直接跳到 `焦点/空间轴线`；更稳的顺序是先锁 `主体/陪体/背景关系 -> 构图布局 -> 构图方式`，再收束到焦点、观看路径、空间与几何写回。
- 若用户或下游需要结构化镜头标签，最稳的落点不是新开平行字段族，而是把 `景别 / 镜头属性 / 镜头框架 / 镜头类型 / 镜头视角` 作为 `FIELD-DETAIL-05` 的 shot-level 描述子槽，由 `分镜表现` 统一统筹。
- 当 reference 模块内部已经存在明确的串行、并行、条件分支或回退链时，除了表格合同，还应补一段 Mermaid，把上游输入、节点拓扑、失败回跳和下游消费关系显式画出来。
- `角色表现` 如果只写“愤怒、悲伤、紧张”这类抽象词，几乎一定会丢掉人物辨识度；更稳的写法是先锁角色会怎样露馅、怎样硬撑、怎样下意识反应。
- 想让观众共情，不应先加大情绪词，而应优先增加“想压住却露出来”“想维持却失手”的可见身体细节，尤其是眉眼、呼吸、嘴角、肩颈与手部的小失控。
- 对手戏调用知识库时，最有价值的不是“复现经典调度”，而是识别当前戏是否高命中某种权力/距离/隔阂母型，再把它翻译成演员层的让压、逼近、回避、断开和位置交换。

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
- root_cause_or_design_decision: 旧摄影链能表达 final look，但还没有把上游 `组间设计.全局风格 / 类型元素 / 导演意图` 的摄影承诺显式回收到节点前置，也没有把组级照明推进与色彩心理拆成稳定必答位，容易滑回抽象审美词。
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

### Case-20260412-AIGC-DETAIL-DIALOGUE-SCENE-MATCH

- milestone_type: source_contract_change
- outcome: 在 `角色表现` 的 `对手戏模式` 中加入电影学院派一流对话场景知识的高命中检测节点。
- root_cause_or_design_decision: 对手戏确实会受经典对话场景母型启发，但若没有命中检测与转译边界，知识库很容易被错误使用成抽象致敬或直接越权写成摄影/运镜指令。
- final_fix_or_heuristic: 将知识库读取限制为 `对手戏模式` 下的条件路径，并要求先判定是否与权力对比、障碍隔离、位置交换、距离压缩、排挤关系等母型高度同构；命中后只能沉成 `dialogue_scene_reference_note` 服务表演策略。
- prevention_or_replication_checklist:
  - [x] `角色表现.md` 已加入 `PF-2A 对手戏高命中检测`
  - [x] `execution-flow.md` 已声明该节点为 `performance_engine` 的条件串行节点
  - [x] `chain-of-thought.md` 已把“对手戏高命中”加入 `FIELD-DETAIL-07` 判题口径
  - [x] `capability-playbook.md` 已补强知识库转译边界
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/角色表现.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `knowledge-base/电影学院派/导演手册/一流对话场景.md`
- user_feedback_or_constraint: 用户要求在 `3-Detail` 的思维·执行节点里补入“对手戏时，关联 `knowledge-base/电影学院派/导演手册/一流对话场景.md` 是否有高度命中的”这一考虑，并优先落在 `references` 专属模块。

### Case-20260412-AIGC-DETAIL-CAMERA-KB-HIT

- milestone_type: source_contract_change
- outcome: 在 `运镜手法` 的思维·执行链里加入 `knowledge-base/电影学院派/分镜脚本` 的高命中检测节点，并明确其只负责运动语法转译。
- root_cause_or_design_decision: `分镜表现` 已有学院派分镜知识的结构层命中，但运镜层此前没有独立判断“当前运动意图是否高度命中某种调度/语法母型”，导致要么完全漏用知识库，要么错误地在运镜层重做一次镜头设计。
- final_fix_or_heuristic: 将知识库检测插入 `camera_movement_engine` 的内部串行链，顺序固定为 `默认路线 -> 运动动机 -> 高命中检测 -> 默认 patch -> 变体比较 -> 挑战案`；命中后只允许沉成 `camera_academy_hit_note` 服务运动策略，不得反向改写构图、景别、空间与表演主任务。
- prevention_or_replication_checklist:
  - [x] `运镜手法.md` 已增加高命中检测节点与知识库边界
  - [x] `execution-flow.md` 已声明其为 `camera_movement_engine` 的条件串行步骤
  - [x] `chain-of-thought.md` 与 `_shared/IO_CONTRACT.md` 已纳入该证据与命名合同
  - [x] 主 `SKILL.md` 已认领该节点，不再只停留在专属 reference
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/运镜手法.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `knowledge-base/电影学院派/分镜脚本/电影镜头调度.md`
  - `knowledge-base/电影学院派/分镜脚本/电影镜头技术.md`
- user_feedback_or_constraint: 用户要求在 `.agents/skills/aigc/3-Detail` 的“思维·执行”节点中，为运镜手法部分补入“关联 `knowledge-base/电影学院派/分镜脚本` 是否有高度命中的”考虑，并优先落在 `references` 专属模块。

### Case-20260412-AIGC-DETAIL-INHERIT-GROUP-DESIGN

- milestone_type: source_contract_change
- outcome: 将 `3-Detail` 的第一结构化输入改为继承 `2-Global` 已 seed 的 shared episode root，不再默认从三份 Markdown 长文二次抽取 `组间设计`。
- root_cause_or_design_decision: 旧合同虽然把 `2-Global/*.md` 设为必需输入，但 schema 真正需要的是每组的 `组间设计.全局风格 / 类型元素 / 导演意图`；继续以长文本为第一输入，会让 `3-Detail` 反复执行同一层蒸馏，导致 handoff 漂移。
- final_fix_or_heuristic: 把 `projects/<项目名>/3-Detail/第N集.json` 提升为 `3-Detail` 的第一结构化输入，并要求 `scope_bootstrap_engine` 先校验与继承上游 `组间设计`；`2-Global/*.md` 只保留为兼容回退或审计证据。
- prevention_or_replication_checklist:
  - [x] `3-Detail/SKILL.md` 已将 shared root 升为必需输入
  - [x] `_shared/IO_CONTRACT.md` 已固定 `组间设计` 继承校验
  - [x] `references/execution-flow.md` 已改为默认从 shared root 取组级上下文
  - [x] `CONTEXT.md` 已沉淀“长文本只作回退/审计”的启发式
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/CONTEXT.md`
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
- user_feedback_or_constraint: 用户明确要求“来到 3-Detail 时，对于 2-Global 上游层的上下文加载不必再去读取三份 MD 文档，而是直接继承 JSON（本身为同一模版，只是 2-Global 填了部分字段，其余留空等着 3-Detail 完成）。”

### Case-20260412-AIGC-DETAIL-REMOVE-THINKING-CHAIN

- milestone_type: source_contract_change
- outcome: shared episode root 不再把 `thinking_chain` 作为 canonical 输出必填槽；当前项目 `第1集.json` 已去掉该字段。
- root_cause_or_design_decision: schema、bootstrap template、transition 示例和 `3-Detail` 写回文档此前仍把 `thinking_chain` 当成标准输出，导致即使业务真相已完整落在 `metadata + final_output`，新 root 仍会被重复写入一段对下游无消费价值的可见摘要。
- final_fix_or_heuristic: 将 shared schema 改为 `thinking_chain` 仅兼容旧 root 的可选字段，删除 bootstrap template、示例 JSON 与当前项目 root 中的该字段，并把 `3-Detail` 的 writeback 合同改成只维护 `metadata + final_output`。
- prevention_or_replication_checklist:
  - [x] shared schema 已取消 `thinking_chain` 必填
  - [x] bootstrap template 与 transition 示例已去掉 `thinking_chain`
  - [x] `3-Detail` 输出合同与执行流已改为只写 `metadata + final_output`
  - [x] `projects/2049退休老头的快乐生活/3-Detail/第1集.json` 已删除 `thinking_chain`
- evidence_paths:
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/references/output-template.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `projects/2049退休老头的快乐生活/3-Detail/第1集.json`
- user_feedback_or_constraint: 用户明确要求 `projects/2049退休老头的快乐生活/3-Detail/第1集.json` 与 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 中不再要求思维链 `thinking_chain` 输出。

### Case-20260413-AIGC-DETAIL-DENSITY-HOMOGENIZATION

- milestone_type: source_contract_change
- outcome: 为 `3-Detail` 增加了分镜密度反同质化合同，明确 `tail-hook` 预映默认不是本组独立 beat，也明确共享示例不可被复用为“默认 2 镜模板”。
- root_cause_or_design_decision: 最新一轮执行里，同一集 9 个分镜组无论正文负载差异如何都落成 2 镜；上溯后发现根因不是显式硬编码，而是三层组合偏置叠加：`1-Planning/3-分组` 默认 15 秒均匀组长、非末组正文普遍带 `tail-hook` 借入首拍、`3-Detail` 又缺少“hook preview 不自动算 beat”与“镜数高度一致需返工”的明文 gate，同时共享 phase 示例恰好全是双镜粒度。
- final_fix_or_heuristic: 在 `references/execution-flow.md` 中要求 skeleton / 分镜表现先区分 `canonical beat` 与 `hook preview`；在 `references/分镜表现.md` 中增加 `shot_count_decision / why_not_fewer / why_not_more` 与 `密度同质化` 返工门；在 `capability-playbook.md` 与共享示例 README 中固定“样例只复用结构、不复用镜数”的边界。
- prevention_or_replication_checklist:
  - [x] `execution-flow.md` 已要求先标记 `hook_preview_span`
  - [x] `分镜表现.md` 已加入分镜密度裁决规则与同质化返工门
  - [x] `capability-playbook.md` 已固定 tail-hook 与样例模板的防误用规则
  - [x] 已移除共享 phase 示例，避免继续形成双镜模板污染
  - [x] `CONTEXT.md` 已沉淀本次失败类型与复用启发式
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/分镜表现.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/CONTEXT.md`
  - `projects/2049退休老头的快乐生活/1-Planning/3-分组/第1集.md`
  - `projects/2049退休老头的快乐生活/3-Detail/第1集.json`
- user_feedback_or_constraint: 用户明确追问“分镜密度几乎都均匀设定为 2 个，是不是规则中某个不合理设置导致的”，并进一步要求移除共享双镜示例及相关引用，避免继续干扰执行。

### Case-20260413-AIGC-DETAIL-QUANTIZED-DENSITY-RULE

- milestone_type: source_contract_change
- outcome: 将 `3-Detail` 的分镜密度裁决从经验判断升级为可量化机制，并把 `短剧 / 漫剧` 的高密度倾向收束为受控的格式档位。
- root_cause_or_design_decision: 仅靠“节拍感”描述镜数，执行时很容易重新滑回主观裁量，既难解释“为什么不是更少/更多”，也难像 `3-分组` 的字窗机制那样形成 warn / hard gate；同时，短剧与漫画页导向确实需要更高镜数基准，但若不给出显式档位，就会变成隐性默认加速。
- final_fix_or_heuristic: 在 `references/分镜表现.md` 中固定 `候选节拍 = 动作阶段点 + 台词气口点 + 焦点切换点 + 结构转折点`，并定义 `推荐镜数基准 = 候选节拍 * 节奏系数 * 格式基准系数`、`最终分镜数 = 推荐镜数基准 + 拆镜加权 - 合镜折减`，再受组时长与场景类型窗口校正；同时在 `execution-flow.md`、`chain-of-thought.md` 与 `capability-playbook.md` 固定 `format_density_profile` 与量化输出项。
- prevention_or_replication_checklist:
  - [x] `分镜表现.md` 已加入候选节拍、节奏系数、格式档位、拆镜加权、合镜折减、组时长窗口与强制输出项
  - [x] `execution-flow.md` 已把 `format_density_profile` 加入 bootstrap 与 staging 输入
  - [x] `chain-of-thought.md` 已把量化密度机制纳入 `FIELD-DETAIL-05`
  - [x] `capability-playbook.md` 已明确 `节拍 != 机械一拍一镜`
  - [x] `north-star.template.yaml` 已补充 `format` 示例注释，降低未来格式档位歧义
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/分镜表现.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/3-Detail/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求参照 `scene-order-duration-strategy.md` 的字窗设计机制，为分镜密度建立量化标准，并进一步要求评估“短剧/漫剧的目标属性是否可以调高一些基准”。

### Case-20260413-AIGC-DETAIL-PACE-COEFFICIENT-RETUNE

- milestone_type: source_contract_change
- outcome: 将量化密度机制的节奏系数上调为更敏感的五档：`1.5 / 1.3 / 1.0 / 0.8 / 0.6`。
- root_cause_or_design_decision: 前一版 `1.3 / 1.15 / 1.0 / 0.85 / 0.7` 更偏保守，适合电影化短片，但对短剧、漫剧或强节奏笑点内容的镜数拉升还不够敏感。
- final_fix_or_heuristic: 在 `references/分镜表现.md` 中直接将 `超快 / 快 / 正常 / 慢 / 超慢` 调整为 `1.5 / 1.3 / 1.0 / 0.8 / 0.6`，保持快档可明显增密、慢档可明显降密。
- prevention_or_replication_checklist:
  - [x] `分镜表现.md` 已更新五档节奏系数
  - [x] `CONTEXT.md` 已记录“高节奏项目可采用更激进系数，但必须公开成档位”
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/分镜表现.md`
  - `.agents/skills/aigc/3-Detail/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求将节奏系数调整为 `超快 1.5 / 快 1.3 / 正常 1.0 / 慢 0.8 / 超慢 0.6`。

### Case-20260413-AIGC-DETAIL-FORMAT-BASELINE-RETUNE

- milestone_type: source_contract_change
- outcome: 将格式基准档位调整为 `standard_film = 1.0 / short_drama = 1.2 / comic_page = 1.3`，并把默认档切到 `short_drama`。
- root_cause_or_design_decision: 旧版 `standard_visual / short_drama / comic_page = 1.0 / 1.1 / 1.2` 仍偏保守，也没有把“标准电影表达”和“默认快节奏表达”明确拆开；这会让短内容项目在未显式指定格式时继续落回偏电影化密度。
- final_fix_or_heuristic: 在 `references/分镜表现.md` 中把 `standard_visual` 重命名为 `standard_film`，并将三档系数改为 `1.0 / 1.2 / 1.3`，同时把默认格式档改为 `short_drama`；在 `execution-flow.md` 与 `capability-playbook.md` 同步档位命名与默认口径。
- prevention_or_replication_checklist:
  - [x] `分镜表现.md` 已更新档位名与系数
  - [x] `execution-flow.md` 已同步新的档位名
  - [x] `capability-playbook.md` 已同步新的默认口径
  - [x] `CONTEXT.md` 已记录这次格式基准重调
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/分镜表现.md`
  - `.agents/skills/aigc/3-Detail/references/execution-flow.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“默认取 `short_drama = 1.2`”，并将 `standard_visual = 1.0` 改为标准电影英文命名，`comic_page` 上调到 `1.3`。

### Case-20260413-AIGC-DETAIL-CONCEPT-SHORT-INTERPRETATION

- milestone_type: source_contract_change
- outcome: 明确规定 `概念短片 + 观察式生活喜剧` 在没有特殊表述时默认解释为 `short_drama = 1.2`。
- root_cause_or_design_decision: 仅把默认档改成 `short_drama` 还不够，因为执行者仍可能看到 `format: 概念短片` 就保守回退到 `standard_film`；这会让同类项目再次出现口径漂移。
- final_fix_or_heuristic: 在 `references/分镜表现.md` 与 `capability-playbook.md` 中补入显式解释：若项目是 `概念短片 + 观察式 / 生活流 / 轻喜剧`，且没有额外“标准电影稀疏镜数”说明，则默认继续使用 `short_drama = 1.2`。
- prevention_or_replication_checklist:
  - [x] `分镜表现.md` 已写入该解释
  - [x] `capability-playbook.md` 已写入该解释
  - [x] `CONTEXT.md` 已记录该解释为稳定口径
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/references/分镜表现.md`
  - `.agents/skills/aigc/3-Detail/references/capability-playbook.md`
  - `.agents/skills/aigc/3-Detail/CONTEXT.md`
- user_feedback_or_constraint: 用户明确说明“概念短片 + 观察式生活喜剧 在没有特殊表述时应理解为 `short_drama = 1.2`”。
