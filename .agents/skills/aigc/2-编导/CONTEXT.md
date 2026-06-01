# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-编导` 的经验层知识库，不是第二份主合同。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件只沉淀可复用判断经验、失败模式和修复打法；不改写 `SKILL.md` 的输入、输出和门禁。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-05-31

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 编导稿仍像旧三阶段拼接 | 阶段整合层 | 回到 `steps/directing-workflow.md`，把 script/director/performance 证据内嵌到同一正文 | Output Contract 固定唯一 `2-编导` 真源 | 不再生成新的 `2-编剧`、`3-导演`、`4-表演` 主稿 |
| 只保真但没有导演/表演可执行性 | 创作层缺口 | 补 director_layer_evidence 和 performance_layer_evidence | review 固定 `GATE-BD-DIRECTOR` 与 `GATE-BD-PERFORMANCE` | 下游 `3-运动` 能消费人物压力、空间关系和表演动作，`4-摄影` 再消费运动强化稿 |
| 导演/表演判断重新抽象化 | 具像画面语言层 | 把“电影感/高级感/权力压迫/内心崩塌/演员克制”等改成可见物、身体动作、声线、空间距离、道具互动或对手反应 | 强制消费 `../_shared/concrete-visual-language-contract.md` | 离开概念词仍能拍、能演、能听 |
| 对白被导演或表演层改写 | 对白冻结层 | 用上游原句逐字替换，表演只改标题状态、气口、停顿和相邻画面 | review 把对白冻结列为跨层阻断门 | 引号内文本与上游一致 |
| 长对白只有断句没有表演交付 | 长对白链路层 | 先回到 `long_dialogue_beat_map`，再补 `long_dialogue_delivery_map` | script layer 负责原文节拍，performance layer 负责呼吸、重音、尾音和对手反应 | 节拍拼回保真，表演链有压力推进 |
| 画面化语言变成堆道具或堆光影 | 动作链层 | 回到 action-first，先锁人物姿态、动作向量、可达对象和退出状态 | 道具/环境准入必须证明互动、信息、规则/证据/危险源或必要环境交代 | 删除道具句后人物动作不会更顺 |
| 表演工艺写成场景末尾总结块 | 终稿投影层 | 把演员任务、潜台词、调度拆回对应对白画面、心理反应、角色动作和沉默余波 | templates 禁止单独 `表演总结` 字段 | 正文没有场景尾部公式块 |
| 旧 `3-导演` / `4-表演` 仍被当 active stage | 路由层 | 根路由、registry、sword6、3-运动和 4-摄影改为串接 `2-编导 -> 3-运动 -> 4-摄影` | 旧名称只做兼容触发词并回接 `2-编导` | 主链为 `1-分集 -> 2-编导 -> 3-运动 -> 4-摄影` |
| 4-摄影仍直接读取 `2-编导` 或旧 `4-表演` | 下游 handoff 层 | 同步 3-运动和 4-摄影 SKILL、templates、review、steps、agents 元数据 | stage handoff contract 固定 `2-编导 -> 3-运动 -> 4-摄影` | 新摄影任务默认输入 `3-运动/第N集.md`，显式跳过时才 fallback `2-编导/第N集.md` |
| 执行报告只有规则清单没有创作证据 | 证据层 | 补 `script_layer_evidence`、`director_layer_evidence`、`performance_layer_evidence` 和 `concrete_visual_language_evidence` | review 阻断“只有文档规则、没有产物证据” | 报告能回指具体场景、字段和修复动作 |
| 执行报告只有层级摘要没有场景字段锚点 | 证据索引层 | 补 `scene_field_evidence_index`，为关键判断标出 `source_anchor`、`target_field`、`embedded_in_text` 和 `repair_owner` | 每层创作时同步登记证据索引，不等到报告末尾补编 | 任取导演/表演判断都能回到来源和正文嵌入句 |
| 到 `3-运动` 的 handoff 只有口头 ready | 下游交接层 | 补 `visual_unit_candidate_map` 和 `motion_enrichment_handoff` | `GATE-BD-18` 固定检查结构化下游交接，不接受空泛 ready | `3-运动` 可直接找到待强化动作句，且没有机位/景别/运镜/prompt 越权 |

## Repair Playbook

1. 先锁定 `source_episode_path`，确认目标输出为 `projects/aigc/<项目名>/2-编导/第N集.md`。
2. 对所有引号内对白逐字回对上游；任何导演或表演层改字都先修回。
3. 检查字段化基础：slugline、声画配对、字段纯度、小说转译、信息差、场景节奏和对白潜台词先通过。
4. 检查导演层：每个关键场景至少能回答戏剧问题、人物压力、观众位置、视觉主轴或氛围承托；答不出则回到 director layer。
5. 检查表演层：心理反应、台词状态、长对白交付、潜台词行为、场面调度和沉默余波能被演员执行；答不出则回到 performance layer。
6. 执行画面化语言 pass：所有抽象词都要替换成具体声画、身体、空间、道具、停顿、呼吸、表情或对手反应。
7. 检查无互动道具、随机忙动作、人人同强度表演和泛化 BGM；无法证明功能时删除或降级。
8. 检查 `scene_field_evidence_index`：关键导演/表演/画面化判断必须有来源、目标字段、正文嵌入句和修复 owner；缺一项就回最早责任层补证。
9. 检查 `motion_enrichment_handoff`：`visual_unit_candidate_map` 应列出可被 `3-运动` 消费的角色动作或画面句；如保留 `cinematography_handoff`，不得含机位、景别、运镜、分镜编号或 prompt。
10. 检查旧 stage 路径泄露：新生产任务不得写 `2-编剧/`、`3-导演/`、`4-表演/`；历史项目产物只做 legacy readback。
11. 交付前把 review finding 当修复输入，不把阻断项留成报告附件。

## Reusable Heuristics

- `2-编导` 的核心不是把三个旧稿顺序粘在一起，而是让同一行剧本同时具备保真、导演压力、表演动作和可拍画面。
- 编导整合后，导演和表演判断更早进入正文，但边界更硬：不能借“更有戏”改剧情，不能借“更能演”改对白。
- 最稳的落盘句式是具体变量：手、眼、呼吸、喉头、声线、重心、门槛、光线、物件状态、环境声和对手反应。
- 画面化不是“有画面感”，而是具像化、反抽象、反概念、反解释、可拍性、字段落点和保真边界同时成立。
- 导演判断先问“这场戏的问题是什么，观众站在哪里看”，再问“画面里用什么可见/可听物承托”；否则容易写成审美口号。
- 表演判断先问“演员要达成什么、不能暴露什么、用什么行为绕过去”，再写微表情；否则容易写成情绪标签。
- 长对白的链路分工仍然保留：编导阶段先锁原文节拍，再给每个节拍呼吸、重音、尾音、身体联动和对手反应。
- 下游 `3-运动` 需要的是可见动作、表演状态、空间关系和画面性字段，用来补全起点、路径、终点和参照系；`4-摄影` 需要运动强化后的可拍画面，不需要编导稿提前写机位、景别、运镜或分镜编号。
- 执行报告里的证据要服务修复和交接：层级 evidence 说明“做了什么”，`scene_field_evidence_index` 说明“落在哪里”，`visual_unit_candidate_map` 说明“摄影下一步从哪里拆”。
- 旧项目中已经存在的 `2-编剧`、`3-导演`、`4-表演` 目录是历史产物；新任务应生成 `2-编导`，不要在历史目录继续追加 canonical 主稿。
