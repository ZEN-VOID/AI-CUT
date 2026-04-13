# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-Detail` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/3-Detail/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-Detail` 还回指外置 `制作组` 合同 | 真源治理层 | 把 team / role / shared playbook 能力内收进 `SKILL.md + references/` | 在审计脚本中加入“禁止引用已删除制作组路径”检查 | `3-Detail` 文档与 audit 均不再引用旧路径 |
| shared episode root 仍把 `thinking_chain` 当标准输出 | 输出合同层 | 从 shared schema、bootstrap template、示例与 writeback 文档中移除必填要求，并删除当前项目 root 中该字段 | 固定 canonical 输出为 `metadata + final_output` 双槽；`thinking_chain` 只保留兼容旧 root 的可选定义 | rerun 后的新 root 默认不再生成 `thinking_chain` |
| `project_state.yaml` 声称 `3-Detail` 已完成，但实际缺 `第N集.json` 或 `validation-report.md` | 项目运行时同步层 | 先按 `3-Detail` bootstrap fallback 重建 shared root 并补阶段验收；若项目已推进到更后阶段，只恢复 artifact 一致性，不回退 `current_stage` | 阶段结案前强制交叉检查 `episode root + validation-report + project_state` 三件套一致性，并在 recovery rerun 合同中禁止晚阶段项目被 detail 补跑降级 | 出现“已完成”状态时，不再允许 root 或 validation 缺失 |
| 没有 `shot skeleton` 就直接补构图、表演、运镜 | 拓扑依赖层 | 强制 `shot_skeleton_engine` 先产出 `分镜ID / 时间段 / coverage` | 在 `IO_CONTRACT` 与 `execution-flow` 中固定 skeleton 先决门 | 其他能力链不再发明镜序 |
| 分镜组镜数异常整齐，几乎都落成 `2 镜` | 密度裁决层 | 先检查是否把 `tail-hook` 预映误算成本组 beat，及是否沿用了共享样例的双镜粒度 | 在 `分镜表现.md`、`execution-flow.md` 与 `capability-playbook.md` 固定 `hook preview != canonical beat`，并增加 `密度同质化` 返工门 | 同一集多数分镜组同镜数时会触发复核，而不是直接通过 |
| 分镜密度只靠经验判断，缺少结构化预算真源 | 密度合同层 | 补 `detail_density_quantizer.py + validate_detail_output.py`，把镜数裁决改成脚本生成的 `preferred_shot_count + shot_budget_floor/ceiling` | 在 `分镜表现.md`、`execution-flow.md`、`chain-of-thought.md` 与 `capability-playbook.md` 明确回指脚本；人工解释不再替代预算生成 | 预算可由脚本稳定复算，episode JSON 会被 validator 按预算区间判定 |
| 结构链、表演链、摄影链同时补同一字段导致冲突 | 字段 ownership 层 | 用 `_shared/IO_CONTRACT.md` 固定 owned fields 与 merge precedence | 将 ownership 与 precedence 提升为 shared I/O 真源 | 合并结果可稳定落到 schema |
| 炫技表达压过叙事清晰度 | 路由策略层 | 默认保守路由为 `叙事派 + 摄影总协调`，挑战方案只作条件对照 | 在 `type-strategies.md` 固定 default vs challenger 规则 | 运镜与摄影优先服务剧情任务 |
| 摄影链只写“电影感 / 冷暖对比 / 高级感”，缺少可执行光位与色彩判断 | 摄影维度合同层 | 在 `references/摄影美学.md` 中强制先回看项目级摄影底座，再拆成 `光位 / 组级光影推进 / 色彩心理 / 摄影总协调` 四段 | 在 `chain-of-thought.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md` 同步固定摄影链的串并结构与必答维度 | `摄影美学` 不再是抽象口号，且能解释组内光影如何推进 |
| 摄影知识库被当成“术语贴纸”，没有真正进入节点决策 | 知识库转译层 | 在 `摄影美学.md` 中增加显式 `命中摄影知识库` 节点，并要求产出 `cinematography_academy_hit_note` | 在 `SKILL.md`、`execution-flow.md` 与 `_shared/IO_CONTRACT.md` 中把该 note 固定为摄影链前置证据 | 学院派知识会被转成当前镜组的布光/色彩决策，而不是标题堆砌 |
| `3-Detail` 后段链重复读取外置知识库导致技能过重 | 后段能力合同层 | 暂时移除 `角色表现 / 运镜手法 / 摄影美学` 的二次知识库读取，只保留前置参考锚点与结构链已转译提示 | 在 `SKILL.md`、`execution-flow.md`、`运镜手法.md`、`摄影美学.md` 与 `_shared/IO_CONTRACT.md` 中固定“后段链只消费项目真源和上游已转译证据，不再额外命中 knowledge-base” | 后段链文档不再要求额外读取外置知识库，且核心 finish 能力仍能闭环 |
| 首选镜数与预算区间已锁定，但下游维度只能稳定给出 2-3 套局部方案 | 串并拓扑合同层 | 把 `shot-local envelope` 提升为结构链输出，并要求并行链只能填充 envelope；不匹配时回退到 `节拍/密度/景别` | 在 `IO_CONTRACT.md`、`execution-flow.md` 与 `capability-playbook.md` 固定“并行 = 受约束填充，不是再次定义粒度” | 后段链不再以复制组级文本的方式填满镜头数量 |
| 同一组内 shot-level 业务字段出现成片原句复制 | review/audit 门禁层 | 把 `组级统一 != 逐镜复读` 写进 `continuity_review_engine`，并让 validator 对高比例 exact duplication 直接报错 | 在 `capability-playbook.md`、维度细则与 `validate_detail_output.py` 中同步固定“`>= 75%` 原句复制即返工”的硬门槛 | validator 会直接报出重复字段与命中组，不再把成片复制输出判成 `PASS` |
| 服装信息继续混写在镜级站位句，导致走位与角色背景关系难以读清 | shared schema / field ownership 层 | 将镜级字段拆成 `角色背景面 / 角色站位走位`，并要求 `3-Detail` 父级聚合回填组级 `出场角色及穿搭` | 在 shared schema、`3-Detail` I/O 合同、execution flow 与 validator 中同步固定“镜级走位 / 组级穿搭摘要”分层 | 命中组已有分镜时，validator 不再放过空的 `组间设计.出场角色及穿搭` |
| 连续性复核与真源审计缺位，导致写回时放过漂移 | 汇流门层 | 把 `review -> audit -> writeback` 写成固定串行 gate | 在 `output-template.md` 与 audit 脚本中同步固化 | `validation-report.md` 与 `audit_report` 同步存在 |
| 旧制作组能力删除后，质量方法也被一起删没了 | 能力吸收层 | 将共享稳定性合同与创作方法整理进 `capability-playbook.md` | 用“内部能力链 + playbook 细则”的单技能结构替代 team/role docs | 细则仍可追溯，但不再依赖外置 agents |
| 角色表现写成泛情绪标签，镜头有人但人物不成立 | 角色表现规则层 | 先锁角色化表达通道，再把情绪落成习惯动作、下意识和可见微表情 | 在 `references/角色表现.md` 固定 `主轴 -> 个性/习惯/下意识 -> 可见信号 -> 叙事行为 -> 传神强化` 的串行链 | `角色表现` 字段能区分“这个角色怎么演”，而不只是“现在什么情绪” |
| 对手戏引用电影学院派知识时只停在“像某种经典场面” | 对手戏参考转译层 | 先做高命中检测，再把母型压成攻守、距离、障碍、逼近/退让等表演策略 | 在 `角色表现.md` 固定 `对手戏高命中检测` 条件节点，只允许输出 `dialogue_scene_reference_note` | 对手戏参考能被消费为行为策略，而不是空泛致敬或越权摄影描述 |
| 运镜层直接复用学院派分镜知识时，容易和 `分镜表现` 抢夺镜头设计权 | 运镜-结构边界层 | 把学院派分镜脚本命中检测放到 `camera_movement_engine` 的“默认路线与动机”之后，只允许输出 `camera_academy_hit_note`，再由默认 patch 吸收 | 在 `运镜手法.md`、`execution-flow.md`、`chain-of-thought.md`、`IO_CONTRACT.md` 与主 `SKILL.md` 中同步固定其为条件串行节点，并声明只处理运动语法 | 学院派分镜知识会增强运动策略，而不会变成第二次构图/空间裁决 |
| 结构链只锁信息与空间，没有把情感节奏、视点立场和心理距离写进节点 | 叙事-视觉桥接层 | 在 `S2/S4` 与 `分镜表现.md` 中补 `叙事内核 / 情节记忆 / 情绪引导 / 景别节奏模板 / POV 策略 / 心理距离` 槽位 | 将这些判断固定进 `chain-of-thought.md`、`execution-flow.md`、`capability-playbook.md` 与 `分镜表现.md` 的节点合同 | 结构链会同时回答“拍什么”与“让观众怎么感受”，而不是只交代空间信息 |
| 表演链能写情绪，但没有强制回答角色在掩饰什么、互动技巧如何落地、身体哪里会露馅 | 表演深描合同层 | 在 `角色表现.md` 中补 `Character Arc / Dialogue & Interaction / Subtext Visualization` 三个强制槽位 | 在 `chain-of-thought.md` 与 `execution-flow.md` 固定 `S6` 必答这些问题，并要求落成可拍微动作 | `角色表现` 不再停在情绪标签或抽象潜台词，而会落成具体互动打法与露馅点 |

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
- 当 `3-Detail` 变得过重时，优先保留 `S2` 的参考锚点和结构链已经完成的转译，收缩表演 / 运镜 / 摄影后段的二次知识库读取；后段链只消费项目真源与上游已转译提示。
- 结构链最稳的增强方向，不是继续追加镜头术语，而是把 `叙事内核 / Previous End / Current Mission / Next Start / 情绪引导` 先锁成视觉判断的上游约束。
- 景别设计若只回答“信息是否看清”，往往会失掉情感目标；更稳的做法是同时锁 `景别节奏模板 + POV 策略 + 心理距离`，并在命中镜头窗口内做反直觉复核。
- 表演深描若只写“他很紧张/很愤怒”，大概率还是浅；更稳的做法是同时回答 `角色在掩饰什么 / 采用什么互动技巧 / 身体哪处会露馅`。
- 并行链最危险的误用，不是“都做得不够细”，而是各自偷偷重判镜头粒度；一旦下游链发现自己需要的变化数和 `preferred_shot_count / shot_budget_floor / shot_budget_ceiling` 对不上，正确动作是上溯重判，不是复制模板补齐。
- `组级一致` 最稳的落地方式不是把同一句业务字段逐镜复制，而是先保留同一语法，再给每个 shot 写清自己的局部压力点、站位变化、光位变化或体感差异。
- 当镜级需要同时表达“角色怎么动”和“人物背后是哪一面空间”时，最稳的写法是把它拆成 `角色站位走位` 与 `角色背景面`；服装信息则回收到组级 `出场角色及穿搭`，由父级聚合统一维护。
- 对 `3-Detail` 来说，最稳的第一结构化输入不再是 `2-Global/*.md`，而是 `2-Global` 已 seed 的 shared episode root；长文本 Markdown 只应作为兼容回退或审计证据。
- 若 `project_state.yaml` 声称 `3-Detail` 已完成，最稳的起手式不是直接相信推荐入口，而是先核对 `3-Detail/第N集.json` 与 `3-Detail/validation-report.md` 是否同时存在。
- 若某项目的 `project_state.yaml` 与 `CONTEXT.md` 里都曾记录“已重建完成”，但磁盘再次缺失 `第N集.json` 或 `validation-report.md`，优先视为 runtime drift recurrence：先重建 artifact 并重跑 validator，再更新状态文件，不要只补状态字样。
- 若 runtime drift 发生时项目已推进到 `4-Design / 5-Image / 6-Video`，最稳的修法是“补回缺失 detail artifact，但保留后续阶段路由”；`3-Detail` recovery rerun 不能把项目状态降回较早阶段。
- 若 shared episode root 已经能用 `metadata + final_output` 表达 business truth，就不要再为“可见收束说明”强挂一个 `thinking_chain` 槽；这类说明最多保留在兼容层，而不应继续占据 canonical 输出合同。
- `分镜表现` 维度最稳的起手式不是先写构图，而是先锁组级节奏、关键节拍和镜头密度，再为每拍配景别、为每镜配焦点。
- 当 grouped script 带有 `tail-hook` 借入段时，最稳的做法是先把它记成 `hook preview`，而不是直接当作本组新增节拍；只有当前组确实需要“余波 / 预感 / 将收未收”的单独落点时，才给它分镜配额。
- 共享 phase 示例只可复用字段组织和 patch 粒度，不可复用镜头数量；如果一集里大多数组都被写成同一镜数，优先怀疑隐性模板污染，而不是先假设“这就是成熟节奏”。
- 分镜密度最稳的口径不是“一拍一镜”，也不是肉眼猜一个 `2/3/4 镜`；而是先由 quantizer 用 `动作阶段点 / 台词气口点 / 焦点切换点 / 结构转折点` 联合分段，再生成 `recommended_shot_baseline + preferred_shot_count + shot_budget_floor/ceiling` 的结构化预算。
- 当项目目标明确偏向强节奏笑点、连续反应链或高压推进时，不应再靠格式档位偷加速；更稳的做法是显式调整 `pace_tier`、节拍拆分和 `expansion/compression headroom` 证据。
- 格式类型不再额外引入密度乘数；电影、短剧、漫画页等题材在密度计算层统一等价于 `1.0`，差异只能通过节拍、节奏与拆/合镜理由体现。
- 当 `分镜表现` 进入 shot-level 结构链时，`景别` 后面不要直接跳到 `焦点/空间轴线`；更稳的顺序是先锁 `主体/陪体/背景关系 -> 构图布局 -> 构图方式`，再收束到焦点、观看路径、空间与几何写回。
- 若用户或下游需要结构化镜头标签，最稳的落点不是新开平行字段族，而是把 `景别 / 镜头属性 / 镜头框架 / 镜头类型 / 镜头视角` 作为 `FIELD-DETAIL-05` 的 shot-level 描述子槽，由 `分镜表现` 统一统筹。
- 若文档或 schema 给出结构化镜头标签示例，最稳的用法是把它当作字段形状示意，而不是把示例值当默认模板；示例里的 `中景 / 定场镜头 / 平视` 一类词必须按当前镜头重判。
- 当 reference 模块内部已经存在明确的串行、并行、条件分支或回退链时，除了表格合同，还应补一段 Mermaid，把上游输入、节点拓扑、失败回跳和下游消费关系显式画出来。
- `角色表现` 如果只写“愤怒、悲伤、紧张”这类抽象词，几乎一定会丢掉人物辨识度；更稳的写法是先锁角色会怎样露馅、怎样硬撑、怎样下意识反应。
- 想让观众共情，不应先加大情绪词，而应优先增加“想压住却露出来”“想维持却失手”的可见身体细节，尤其是眉眼、呼吸、嘴角、肩颈与手部的小失控。
- 对手戏调用知识库时，最有价值的不是“复现经典调度”，而是识别当前戏是否高命中某种权力/距离/隔阂母型，再把它翻译成演员层的让压、逼近、回避、断开和位置交换。
