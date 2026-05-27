# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-表演` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 20000
- status: ok
- last_checked_at: 2026-05-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 心理反应写成传统小说内心或抽象想象 | 字段语义层 | 改成有主体的身体微动作、表情、呼吸、停顿、声线变化、道具停点、空间距离、对手不接话或短促可听独白；纯语言化内容改入 `独白/内心独白` 并配画面 | `references/psychological-reaction-contract.md` 固定 `Psychological Reaction Contract`，workflow 建立 `psychological_reaction_getability_map / psychological_reaction_evidence`，review 把 `心理反应` 纳入具像化和创作证据门禁 | `心理反应` 离开字段标题仍能被演员表演、下游工具解析、观众从声画中感知 |
| 角色演技停留在情绪标签或模板化表情 | 表演控制层 | 回到 `actor_performance_control_pass`，为关键情绪 beat 补上游触发点、表层/压制/隐藏动机、微表情、身体联动、环境声或沉默余波、微动态限制 | `references/actor-performance-control-contract.md` 固定五层表演系统，workflow 建立 `actor_performance_control_plan / actor_performance_control_evidence`，review 检查情绪标签空转和过演风险 | 输出不再只写"愤怒/难过/紧张"或皱眉瞪眼流泪，能从眉眼嘴、手、呼吸、声线、道具和环境声看出演技 |
| 表情精准但仍像模板脸 | 情绪切换瞬间层 | 从“持续表情”改为“上游触发 -> 表面情绪裂开/压制情绪泄露 -> 身体联动收住”的短瞬间 | `actor-performance-control-contract.md` 的 Emotion Transition Moment Rule | 观众能看到情绪刚被触发、被压回去或从表层切到底层，而不是角色全程挂同一表情 |
| 真人表演被简化成情绪表情包 | 潜台词/人性层 | 回到 `performance_task_map`，为关键真人 beat 补目标、阻碍、压制层、未出口信息和身体泄露点；机器/非人角色可简化，真人默认不能只给开心/生气/害怕等标签 | `actor-performance-control-contract.md` 和 `performance-and-scene-craft-contract.md` 固定真人复杂性：情绪标签必须落到压制动机、微动态和行为策略 | 真人角色的笑、发呆、吃饭等表层动作能读出背后的压抑、崩塌、等待或其他上游压力，而不是只变成表情状态 |
| 上游 `表情特写` 被吞回泛化心理反应 | 字段承接层 | 保留 `表情特写` 字段名，在其中精修眉眼嘴、咬肌、下颌、喉头和眨眼频率；非面部身体联动再拆到 `心理反应`、`对白画面` 或 `角色动作` | `2-编剧` 已把 `表情特写` 作为正式面部落点；`4-表演` 负责细化，不负责取消字段 | 下游摄影/图像能直接识别面部 beat，不需要从心理段落里二次挖取 |
| 环境声变成通用 BGM 标签 | 场景身份声音层 | 删除“悲伤音乐/紧张音乐”等泛化描述，改成当前年代、空间功能和材质会自然发出的声音 | `actor-performance-control-contract.md` Environment Sound Support | 声音来自场景身份，不新增事件，也不替代角色表演 |
| 对白只保留文字或空泛状态 | 台词表演层 | 回到 `dialogue_performance_map` 和 `actor_performance_control_pass`，为每段对白补 `对白（角色，语气/情绪/状态）` 第二项，并在 `对白画面` 或相邻字段补气口、断句、停顿、声线、重音、尾音或对手反应；不得改写引号内原对白 | `performance-and-scene-craft-contract.md` 固定 `Dialogue Performance Rule`，`actor-performance-control-contract.md` 固定 `Dialogue Delivery Control`，workflow 建立 `dialogue_performance_evidence`，review 把台词表演纳入阻断门 | 每段对白离开台词文本仍能指导演员怎么说；关键对白有可听、可演的节奏和情绪控制 |
| 长对白逐句状态相同，像一口气念稿 | 长对白交付层 | 消费 `2-编剧` 的 `long_dialogue_beat_map`，补 `long_dialogue_delivery_map`：每个节拍有气口/连续气息、停顿、重音、尾音、身体联动和对手反应 | `actor-performance-control-contract.md` 固定 Long Dialogue Delivery Chain，review 固定 `GATE-PERF-14` | 长对白保持原文节拍，但表演上有压力推进、呼吸层次和听者反应链 |
| 心理潜台词权力关系仍写成解释句 | 表演工艺层 | 回到 `N5-PERF-SCENE-CRAFT`，把"想什么/关系如何变化"转成目标、阻碍、策略、停顿、视线、身体距离、道具动作或场面调度 | `performance-and-scene-craft-contract.md` 固定 `scene_turn_pass` 与 actor task rule | `表演提示` 可执行，`场面调度` 可见，画面字段不再写心理结论 |
| 表演提示在场景末尾总结式列出 | 终稿投影层 | 回到 `N5-PERF-SCENE-CRAFT` 与 `N6-PERF-BLOCKING` 的 `integration_targets`，把目标、阻碍、权力关系和视线焦点拆入对应对白画面、角色动作、环境、道具、群像和声音字段 | `performance-and-scene-craft-contract.md` 固定 planning maps 只作为规划证据，不作为终稿总结块 | 场景末尾没有 `表演提示/场面调度` 总结块，相关细节已出现在对应 beat |
| 场面调度越权成摄影方案 | 阶段边界层 | 删除机位、景别、镜头运动、分镜编号，改写为人物站坐、高低、远近、道具归属和视线方向 | `4-表演` 只写导演/演员可执行调度，摄影方案交给 `5-摄影` | 输出无 `分镜明细预设`、机位、景别或分镜编号 |
| 潜台词或转场反复写成看向远方 | 表演变量单一层 | 把第二次及以后出现的"避开对方 / 看向远方 / 顺着视线望去"改成道具状态、声音桥、群像反应、身体距离、动作中断、空间阻隔或环境刷新 | `performance-and-scene-craft-contract.md` 固定 `Transition And Subtext Variety Rule`，`field-routing` 增加转场承托选择池 | 同一场景的未出口信息和下一场压力不连续依赖同一种视线动作 |
| 主角内心想法被删掉或改成客观概括 | 主观视角层 | 把主角视角下对他人行为的判断、怀疑和解读改入 `内心独白（主角）`，并补 `内心独白画面` 承托当前可见证据 | `psychological-reaction` 与 `novel-to-screen` 固定 `protagonist_inner_voice_evidence`，review 检查 `third_person_pov_judgment` | 主角内心没有丢失，且没有写成"她在试探他"这类客观第三方总结 |
| 主角内心独白仍使用小说第三人称自指 | 主观声音人称层 | 将 `内心独白（主角）` 引号内指代主角自身的"他/她/其/角色名"改为"我/我的/自己"或角色当下自然口吻；`内心独白画面` 保留第三人称可拍描述 | `psychological-reaction`、`novel-to-screen`、`SKILL.md` Completion gate 固定 inner voice person check；review 检查 `inner_voice_person_consistency` | 内心独白读起来像角色本人正在想，而不是第三人称旁白；保留的第三人称均指向其他角色、引用文本或有自我疏离留证 |
| 动作字段混入主观预判或心理意图 | 动作纯度层 | 删除"试图、想要、打算、意图、为了掩饰"等词，改成手、眼、呼吸、停顿、声线、重心、道具和空间运动 | `field-routing` 固定 `Action Field Dynamics` 与 `objective_action_purity_map`，validator 机械拦截高频词 | `角色动作` / `动作画面` 离开解释仍能被镜头实拍 |
| 人物动作链被情绪动作或道具打断 | 动作链/空间可达层 | 回到 `Actor Action Chain And Reachability Rule`，先补人物姿态、位置、朝向、动作向量、可达对象和退出状态；删除低信息动作堆叠和无互动对象反应 | `../_shared/action-first-continuity-contract.md` 与 `performance-and-scene-craft-contract.md` 固定动作链优先和情绪动作经济 | 下一阶段能直接承接人物坐站、朝向、身体接触和注意力落点；删掉无用动作后表演更顺 |
| 角色像摆拍或所有人都在表演 | 活人感行为层 | 回到 `../_shared/lived-in-character-behavior-contract.md`，为关键单人 beat 补场景内成立的当前小事、下意识反应和情绪落点；多人 beat 只保留行动者和反应者，其他人降级为站位/朝向/低强度背景 | `performance-and-scene-craft-contract.md` 固定 Lived-In Behavior And Action-Reaction Rule，review 增加 `GATE-PERF-06` | 输出不再只展示脸、五官、光影或发丝；多人戏能读出一个人行动、另一个人反应的因果焦点 |
| 角色每场戏都像重新开始 | 角色弧线层 | 回到 `character-arc-performance-contract.md`，为关键角色补 `character_arc_profile`，把本场表演强度、压制程度和外显方式接到前后状态差 | workflow 固定 `character_arc_performance_evidence`，review 增加 `GATE-PERF-07` | 同一角色在不同场次的动作、声线、眼神和沉默能读出累积变化，而不是每场重置 |
| 导演表演风格没有进入表演稿 | 跨阶段风格消费层 | 回到 `3-导演` 的 `performance_style_directive`，把外放度、身体性、声线、面具/真实轴和转变触发转成表演强度与动作/声线取舍 | workflow 固定 `performance_style_consumption_evidence`，review 增加 `GATE-PERF-10` | 表演不是重新自由发挥，而是沿导演给出的角色风格频段细化 |
| 观众心理只停在导演报告里 | 跨阶段观众体验层 | 回到 `audience_psychology_map` 和 `conflict_legacy_transfer`，用知情层级、期待、恐惧、渴望和冲突遗产决定角色反应强弱、沉默长度和群戏注意力 | workflow 固定 `audience_psychology_performance_evidence`，review 增加 `GATE-PERF-11` | 观众比角色多知道或少知道的信息能在表演差拍、压制、隐瞒或误判中被看见 |
| 情绪节奏图没有约束表演强度 | 跨阶段节奏消费层 | 回到 `emotional_rhythm_map.scene_emotional_register`，按 suppressed/cold/violent/released 等音域分配表演强度和五层控制展开程度 | workflow 固定 `emotional_register_performance_evidence`，review 增加 `GATE-PERF-12` | 表演强度随整集峰谷和类型底色变化，不再每场同强度演满 |
| 内心独白和旁白把表演挤没 | 独白预算层 | 回到心理反应和场景工艺，把可外显心理改成呼吸、停顿、声线、手部、沉默、群像反应或动作余波 | workflow 固定 `monologue_budget_evidence`，review 增加 `GATE-PERF-13` | 观众通过表演看到心理，而不是持续听解释性心理文字 |
| 群戏人人同强度抢戏 | 群戏层次层 | 回到 `ensemble-performance-contract.md`，先区分行动者、反应者、压力源、背景参与者和被忽略者，再写表演强弱 | workflow 固定 `ensemble_layers / ensemble_performance_evidence`，review 增加 `GATE-PERF-08` | 群戏焦点清楚，背景人物服务压力和关系，不与主行动抢表演 |
| 强情绪后无身体残留 | 生理真实性层 | 回到 `physiological-realism-contract.md`，补呼吸、咽喉、手部、肩颈、重心、声线和恢复时长等身体残留 | workflow 固定 `physiological_realism_evidence`，review 增加 `GATE-PERF-09` | 震惊、压抑、崩溃或强忍后有可见生理后果，角色不会下一拍立刻恢复干净 |
| 情绪状态瞬间切换无生理过渡 | 生理真实性层 | 回到 N4-PERF-ACTOR-CONTROL 补过渡 beat | physiological-realism-contract.md | 情绪切换有≥2beat 生理残留 |
| 群戏所有角色同等强度 | 群戏层次层 | 回到 N5-PERF-SCENE-CRAFT 按 ensemble_layers 分配 | ensemble-performance-contract.md | 有明确的 foreground/mid/background 分层 |
| 角色跨集表演无变化 | 角色弧线层 | 回到 N2-PERF-TYPE 检查 arc_stage | character-arc-performance-contract.md | 本集表演与前集有可感知差异 |
| 主观情绪感受直接写进终稿 | 情绪投影层 | 把"感到恶心/难受/愤怒"等转成微表情、肢体动作、生理反应、声线变化或主角内心独白 | `psychological-reaction` 固定 `subjective_emotion_projection_map`，review 检查 direct emotion label | 终稿能看到喉头、嘴角、指节、呼吸、停顿或内心独白，而不是心理标签 |
| 无互动道具被硬写成表演承托 | 道具准入层 | 删除倒影、涟漪、餐具碰撞、影子压物等孤立物件反应；若道具重要，改成角色明确触碰/移动/交接/查看，或降级为一次环境交代 | `performance-and-scene-craft-contract.md` 固定 `Prop Interaction Economy Rule`，review 增加 `GATE-PERF-04` | 删掉道具句后人物动作衔接不受损；保留的道具均有互动、关键信息或必要环境功能 |
| 执行顾问与复核流程时跳过表演监制顾问请教 | 顾问请教层 | 回到 `team.yaml.roles.supervision.stage_profiles."4-表演"` 与共享团队顾问合同，按当前 `PASS-PERF-*` / `N*-PERF-*` 节点派生问题 | `steps/directing-workflow.md` 固定 `N6.5-PERF-ADVISOR`，review 检查 `advisor_consultation_packet` 或本地 checklist 结果 | 执行报告能看到 roster 来源、节点锚点、角色视角、可执行指导和阻断降级 |
| 表演阶段把上游画面化成果重新抽象化 | 具像表演语言层 | 把“情绪复杂/关系变化/权力压迫/内心崩塌/演员克制”等概念改成眉眼嘴、呼吸、声线、停顿、重心、距离、道具互动或对手反应，并补 `concrete_visual_language_evidence` | workflow 消费 `../_shared/concrete-visual-language-contract.md`，review 固定 `GATE-PERF-15` | 表演稿、顾问意见、报告和终稿离开概念词仍能被演员执行、镜头拍到、声音听到 |

## Repair Playbook

1. 确认上游 `2-编剧/第N集.md` 或 `3-导演/第N集.md` 已通过对应门禁，输出路径可读。
2. 逐场景检查 `心理反应` 字段：有主体、有上游触发点、有可见/可听/可演通道；离开字段标题仍能被演员表演和观众感知。
3. 检查关键情绪 beat 是否只写情绪标签或模板表情；若有，按 `actor-performance-control` 补触发点、情绪动机、眉眼嘴/咬肌/鼻翼、手/肩/呼吸/重心/声线、环境声和微动态限制。
3.02. 检查 `表情特写` 与关键表演：字段名保留，情绪标签细化为面部分区、切换瞬间和身体泄露点；真人角色不能只剩开心、生气、害怕、发呆等表情包，非人/机器角色按设定例外。
3.09. 检查关键角色是否缺少 `character_arc_profile`：每场表演必须回答“上一场留下什么状态、这一场新增什么压力、下一场带走什么残留”。若角色每场像重新开始，回到角色弧线表演合同补累积状态差。
3.1. 检查每段 `对白（角色，...）`：第二项必须写清语气、情绪或状态；关键对白必须在 `对白画面` 或相邻字段写出气口、断句、停顿、声线、重音、尾音或对手反应；引号内对白不得改字。
3.2. 检查上游 `long_dialogue_beat_map`：不得重切或合并节拍；逐 beat 补 `long_dialogue_delivery_map`，让气口、停顿、重音、尾音、身体联动和对手反应形成连续交付链。
4. 检查潜台词和权力关系是否仍写成解释句；若"想什么/关系如何变化/谁在试探谁"仍出现在画面或动作字段，转成目标、阻碍、策略、停顿、视线、身体距离、道具动作或场面调度。
5. 检查场景末尾是否有 `表演提示` 或 `场面调度` 总结块；若有，把其中的指节、视线、道具、位置、低声、群体反应拆回对应剧本句段。
6. 检查 `场面调度` 是否写入机位、景别、镜头运动、分镜编号或 `分镜明细预设`；若有，删除并改写为人物站坐、高低、远近、道具归属和视线方向。
7. 检查潜台词和转场变量：同一场景若已使用视线转移承托潜台词，下一处必须换成道具、声音、群像、身体距离、动作中断、空间阻隔或环境刷新。
8. 检查主角内心想法和主角视角判断：不得删掉；不得写成客观第三方概括；优先投影为 `内心独白（主角）` + `内心独白画面`。
8.0. 检查内心独白人称：`内心独白（主角）` 引号内若承接第三人称小说叙述，主角自指必须改为第一人称；只在第三人称指向其他角色、引用文本或刻意自我疏离并留证时保留。`内心独白画面` 不按此规则改成第一人称。
8.1. 检查动作客观性：`角色动作` / `动作画面` 中出现"试图、想要、打算、意图、为了掩饰、准备借此"时，删除主观意图词，改成可拍动作、神态、语气、生理反应或空间运动。
8.15. 检查动作链、空间可达和活人感：关键 beat 要有姿态、位置、朝向、动作向量、可达对象、退出状态和场景内成立的小事；多人场面先定行动者和反应者，删掉人人同强度表演和随机忙动作。
8.2. 检查直接情绪词：`感到恶心/难受/愤怒/害怕/崩溃` 不直接进终稿，改成微表情、肢体动作、生理反应、声线变化或主角内心独白。
8.22. 检查情绪动作经济、生理真实性和群戏层次：动作只保留最能改变状态差的 1-2 个；强情绪后补呼吸、喉头、手部、肩颈、重心、声线或恢复时长；多人场面回到 `ensemble_layers` 收敛焦点。
8.25. 检查道具承托：每个道具句都必须回答“角色是否正在互动、道具是否是关键信息/规则/证据/危险源、是否为必要环境交代”。答不出时删除，不要用倒影、涟漪、轻响、阴影压物等孤立物件反应填充沉默或潜台词。
8.3. 若执行顾问与复核流程，检查 `advisor_consultation_packet` 是否来自 `team.yaml.roles.supervision.stage_profiles."4-表演"` 或共享合同回退路径，且顾问问题绑定当前表演节点；没有外部 provider 调度时必须有本地 checklist 结果。
8.4. 检查 `concrete_visual_language_evidence`：心理、潜台词、关系、权力、顾问意见和终稿字段必须落到身体、声线、停顿、距离、道具互动或对手反应；概念标签回最早责任节点。
9. 交付前把 review finding 当成修复输入；阻断项先在本阶段修复并复审，仍失败再阻断或回源层。

## Reusable Heuristics

- `4-表演` 聚焦于可演、可感知和可执行，不创造剧情事实。
- 上游画面不能在表演层被压回概念；“内心崩塌/关系变化/权力压迫/演员克制”必须继续落到眉眼嘴、呼吸、声线、手、重心、距离和对手反应。
- 高阶表演不是把心理词写得更文学，而是让演员知道"我要达成什么、不能暴露什么、用什么行为绕过去"。
- 角色演技不是情绪词堆叠，而是触发点、压制动机、微表情、身体联动、环境声和微动态限制共同工作；真人表层动作必须追到没说出口的压力。
- 微表情优先写情绪刚裂开、刚压回去、刚被看见的瞬间；面部找眉眼嘴、咬肌、鼻翼、下颌和眨眼频率，非面部找手指、肩颈、呼吸、重心、道具停点和声线。
- 台词保真不等于台词表演空白；引号内不动，`对白（角色，状态）` 和 `对白画面` 必须告诉演员这句话的语气、情绪、气口、断句、声线和尾音怎么处理。
- 长对白的表演责任不是“再断一次句”，而是给 `2-编剧` 已拆好的节拍分配呼吸、重音、尾音、身体联动和对手反应；同一段话里的压力推进要被演出来。
- “平静/紧张/生气”单独放在对白状态里通常不够；要写成可执行状态，例如“强作平静，尾音发紧”“压低怒意，字字停顿”“先轻后断，句尾收住”。
- `心理反应` 的标题不是抽象心理许可证；它应像演员表演 beat：谁、身体哪里变了、声音哪里断了、道具怎么被处理、对手如何接不到回应。
- 潜台词优先通过停顿、避视、反问、道具动作、身体距离和沉默余波表现；不要用新增对白解释潜台词。若同场已经用过避视或看向远方，下一次必须换变量。
- 转场不是只能靠人物看远方：声音桥、道具状态、群像欢呼变弱、动作中断、空间阻隔、环境刷新和未完成动作都能把下一场压力引进来。
- 声音承托从场景身份长出来；泛化 BGM 会把表演变成外部解释。
- 场面调度是权力关系和信息差的可见形态：站坐、高低、门槛、道具归属和视线方向比结论句更可拍。
- 主角内心尤其要保留：主角对他人行为的判断、怀疑、误读和确认，是主观视角资产；它应进入 `内心独白（主角）`，而不是被删掉或改成全知客观结论。
- 内心独白不是旁白。把第三人称小说叙述投进 `内心独白（主角）` 时，主角自指要变成"我/我的/自己"；画面承托再用第三人称写可拍动作。
- 动作字段是镜头事实，不是动机说明书；"试图/想要/打算/意图"和直接情绪词都要回收到手、眼、呼吸、停顿、声线、重心和道具。
- 表演动作要像一条可交给摄影的链：当前姿态、动作方向、接触对象、停点和退出状态清楚；角色真实感来自场景内成立的小事被压力打断或带偏。
- 道具不是默认表演救场手段。没有互动的杯子、餐具、保单、桌角、倒影和涟漪会把下游镜头强行拐到物件上，破坏人物动作衔接；除非它是关键道具或必要环境交代，否则优先删掉。
