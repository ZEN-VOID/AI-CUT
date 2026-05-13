# CHANGELOG

## 2026-05-13

- 基于 `浪花传说之琉球篇/第2集-电影特别版` 摄影稿复盘，新增 `references/sequence-density-curve-contract.md`，把节奏把控从单句 `beat_map/rhythm_profile` 上收为段落级 `sequence_density_curve`：先裁决 `tempo_beats`、`density_ramp`、`peak_slots`、`recovery_slots`、`set_piece_chain_slots`、`sound_cut_pattern` 和 `density_budget`，再进入单句分镜数量与时值裁决。
- 在 workflow 中新增 `N3.6-DENSITY-CURVE`，要求连续观看段落先判断哪里省镜头、哪里加密、哪里停顿、哪里硬切、哪里交出；并让 `N4-BEAT`、`N5-RHYTHM`、`N5.2-DURATION`、`N5.5-PEAK-SHOT`、`N6.5-SHOT-PLAN` 与 review 消费该曲线。
- 为动作 set-piece 增加 5-6 镜例外：连续命中、连续反弹、连续物件结果或“一声一结果”的声画打点可突破 4 镜上限，但每镜必须有独立起点、撞点、结果或反应，高密度后必须有恢复/反压/交出锚点。
- 更新 `SKILL.md`、beat/rhythm/shot-planning、review、README、模板与 `CONTEXT.md`，新增 `GATE-CINE-04A2/04A3`、`FAIL-CINE-03D/03E` 和执行报告 `density_curve_summary` 字段，防止整场全满、全空、平均同密度或只靠分布统计替代节奏曲线。
- 放宽 `分镜明细` 的分镜密度上限：将仍停留在 `1-3` / `2-3` 的 beat 与 rhythm 细则同步调整为可按真实节拍扩展到 `1-4` / `2-4`，同时保留反模板化约束，禁止把四分镜当固定占位。
- 基于 `reports/transcripts/audio/AI视频镜头与提示词学习稿.md` 新增 `references/ai-video-prompt-execution-contract.md`，把“镜头包裹动作、方向参照、光线结果、表演微动态、提示词分栏边界”转译为 `3-摄影` 的视频执行稳定性合同。
- 在 `SKILL.md`、workflow、review、README 与 `CONTEXT.md` 中接入 `ai_video_prompt_execution_profile`，要求 `N6.4-FUNCTIONAL-PROJECTION` 和 `N6.5-SHOT-PLAN` 在输出前检查镜头先行、动作发生在镜头内部、方向相对镜头/画面明确、光线写成可见结果。
- 更新动态运镜、自然成稿、功能性投影和技法库细则，补充方向参照、光线结果控制、微动态表演承托和禁止把完整视频提示词分栏模板直接落入 `分镜明细` 的规则。
- 新增 review gate `GATE-CINE-15A` 与失败路由 `FAIL-CINE-05N`，用于阻断动作镜头割裂、方向含混、光线空泛、抽象情绪和提示词模板腔。
- 根据审查结果补齐思维·执行节点闭环：将 AI 视频执行稳定性补入 `N8-REVIEW`、`N8R-DIRECT-REPAIR`、`PASS-CINE-12`、阶段末 review-repair 合同与 `thinking_action_node_review`，确保新 gate 在最终写回前是阻断项。
- 修正 `CONTEXT.md` 健康状态：当前已超过 `soft_limit_chars`，状态改为 `warn` 并记录后续定向压缩要求，本轮优先保留学习成果完整性。

## 2026-05-06

- 补全画面性字段语义入口：在 `SKILL.md`、`references/visual-matching-contract.md` 与 `CONTEXT.md` 中显式加入微表情、呼吸、沉默、姿态、视线、手部动作和身体距离，避免表演细节只隐含在类型包中。
- 新增 `references/visual-sequence-alignment-contract.md`，把段落级连续观看意图拆成内部 `sequence_profile`：只统一视觉母题、注意力接力、运动家族、材质光色和交出锚点，不改变逐画面句子归属。
- 在 `SKILL.md`、workflow、shot planning、visual matching、continuity、dynamic lens、functional projection、natural writing、types、review、templates、README 与 CONTEXT 中接入 `unit_ownership_map / unit_ownership_check`，阻断“整段运镜流畅但分镜失主”的问题。
- 新增 `PASS-CINE-02S` 与 `N3.5-SEQUENCE-ALIGN`，要求相邻 3-6 个画面单位共享空间、道具链、声音链、动作链、记忆插入或视觉母题时，先做段落对齐，再逐画面点落盘。
- 同步优化思维·执行节点拓扑：`N2-MATCH` 先建立 visual_unit 与 ownership_boundary，`N3-TYPE` 再输出 `sequence_relation / ownership_risk`，最后由 `N3.5-SEQUENCE-ALIGN` 判断段落统筹；review 返工路由改为精确节点名。
- 新增 `GATE-CINE-04D` 与 `FAIL-CINE-05M`，检查每条 `分镜N` 是否能回指正上方画面句子，且没有提前吞入后文主体动作、对白反应、记忆段、道具揭示或跨场景连接方案。
- 新增 `references/shot-duration-decision-contract.md`，把单镜长短从“节奏感”中拆出为独立 `shot_duration_decision`：每个 `分镜N` 必须能说明时值等级、内部估算范围、停顿/压缩理由和 15 秒组内节奏风险。
- 同步更新 `SKILL.md`、workflow、shot planning、visual rhythm、dynamic lens、functional projection、types、review gate、templates、README 与 CONTEXT，要求分镜数量和单镜时值同时成立。
- 新增 `PASS-CINE-04D` 与 `N5.2-DURATION`，防止“切换点正确但镜头长短错误”：文字/道具/微表情被快速切走、低信息镜头被拖长、连续同长同速或高点时值类型混淆。
- 将逐集摄影稿落盘格式收束为 `分镜N（约X秒）:`，`estimated_seconds` 保持内部裁决，`display_seconds` 必须显式进入正文，供下游视频阶段直接消费。
- 强化对白/旁白/画外音台词量预算：`N5.2-DURATION` 先估算 `dialogue_seconds_floor`，再裁决镜头长短；review 与 validator 同步阻断缺少显式秒数或对白时值承托的稿件。

## 2026-05-04

- 将 `3-摄影` 的转场职责降级为边界交出职责：保留镜头内部连续性、进入点、最后一镜可消费交出锚点和连续性风险，不再主创组间或跨场景创意转场方案。
- 保留 `references/transition-design-contract.md` 路径但重写为 `Handoff Boundary Contract`，将 `transition_profile` 迁移为 `handoff_profile`，连接方式、强度和 3-4 秒连接件提示交由 `4-分组` 裁决。
- 同步更新 SKILL、workflow、types、review、templates、README、CONTEXT 和相关 references，避免 `PASS-CINE-07T`、review gate 或类型路由继续把普通切镜、软桥接、匹配剪辑和高能转场拉回摄影阶段。

## 2026-05-03

- 新增 `references/transition-design-contract.md`：场景变化固定视为明确转场动机，但转场强度另判；普通切镜、软桥接、匹配剪辑和高能转场按交出点/进入点与接口证据分级。
- 在 `SKILL.md`、types、visual rhythm、continuity、shot planning、workflow、技法库、功能投影、review gate、README 与 CONTEXT 中同步接入 `transition_profile`，要求场景变化至少处理上一画面交出点和下一画面进入点。
- 源层修复分镜数量塌缩问题：明确 `分镜2` 不是默认占位，只有存在第二个真实观看策略时才成立；低信息块可收敛为 1 镜，关键显影、群像扩散、动作分相或高点承托可按真实节拍扩展到 3-4 镜。
- 在 `beat-analysis-contract.md`、`visual-rhythm-analysis-contract.md`、`shot-planning-integration-contract.md`、workflow、review gate 与模板中新增 `shot_count_decision` 和 2 镜集中复判规则，防止批量输出被模板诱导为固定两镜。
- 更新 `validate_cinematography_markup.py` 与脚本说明，新增分镜数量分布统计和 2 镜异常集中提示；脚本只做机械告警，不替代 LLM 节拍判断。
- 同步升级 `3-摄影` 思维·执行节点：`Thought Pass Map` 扩展为 `PASS-CINE-00..12`，覆盖真源语境、画面边界、类型画像、节拍、节奏、高点、顾问、连续性、摄影语法、功能投影、分镜计划、注入和审查修复闭环。
- 在 `steps/cinematography-workflow.md` 新增 `N6.2-CAMERA-GRAMMAR` 与 `N6.4-FUNCTIONAL-PROJECTION`，把景别/视角/景深/焦点/镜头类型/构图/光色/运镜变化和下游 payload 从 `N6.5-SHOT-PLAN` 中拆成显式前置节点。
- 更新 `shot-planning-integration-contract.md`，新增 `camera_grammar_plan` 与 `functional_projection_plan`，要求每个 `分镜N` 能回指摄影语法选择、功能 payload、连续性交接和自然成稿策略。
- 更新 review gate：新增 `thinking_action_node_review`、`camera_grammar_review`、`GATE-CINE-16 摄影语法变化`、`GATE-CINE-17 思维·执行节点完整` 以及 `FAIL-CINE-05I/05J`。
- 调整 `3-摄影` subagents 参谋机制：顾问问题不再固定为摄影字段清单，而是同步于当前 `PASS-CINE-*` / `N*-*` 思维·执行节点。
- 要求监制顾问代入角色意识、创作风格和专业水准，基于节点的判断、动作、证据、gate 与返工风险提供参谋指导。
- 同步更新 `SKILL.md`、workflow、review gate、`CONTEXT.md` 与共享 team advisor 合同，要求 `advisor_consultation_packet` 记录 node/pass/gate 来源和角色视角。

## 2026-05-01

- 收紧 `分镜明细：` 字段语义：字段名为下游兼容保留，实际写作心智固定为“运镜摄影设计”。
- 新增 `references/natural-shot-detail-writing-contract.md`，把内部摄影参数与最终自然中文成稿拆开，避免参数清单、模板填空和连续同构句。
- 调整 `SKILL.md`、workflow、模板、review gate 与 CONTEXT：必要摄影参数改为内部锁定，成稿只显式写当前节拍最关键的摄影选择。
- 在 `SKILL.md`、workflow、模板和 review gate 中新增字段语义纯度约束，要求内容聚焦运镜手法、摄影美学、构图/机位/光影/色彩与有动机转场特效。
- 在 `CONTEXT.md` 沉淀“字段标题诱发抽象阐释”的修复打法，禁止主题寓意、心理结论、世界观解释、导演阐释或不可执行气氛口号进入 `分镜明细：` 块。
- 新增 `references/shot-planning-integration-contract.md`，把 beat/rhythm/peak/continuity/dynamic/technique 细则汇流为输出前的 `shot_design_plan` 硬门。
- 在 workflow 中新增 `N6.5-SHOT-PLAN`，要求分镜数量、顺序、入口、路径、落点和交出点均可回指前序判断，防止“分镜变多但随机”和上下衔接断裂。
- 同步更新模板、review gate、动态表达与连续性合同，要求每个 `分镜N` 能反推起点、路径、速度、落点、节拍动机和交出点。

## 2026-04-30

- 明确 `3-摄影` 启动 subagents 模式时的执行机制：以项目 `team.yaml` 中明确的监制组相关智能顾问团作为摄影监制。
- 新增 `Subagents Execution Mechanism`，要求顾问代入专业视角和个人风格，对已知上下文提出摄影方向参谋指导，并由主 agent 汇流为 `advisor_consultation_packet`。
- 在 workflow 中新增 `N5.6-ADVISOR`，将顾问参谋沉淀为 LLM 分镜明细注入、阶段内修复和复审的后续上下文。
- 同步更新 review gate 与 CONTEXT 经验层，阻断“泛泛电影感评价”“本地模拟顾问”和“顾问意见越权改写上游编导稿”。

## 2026-04-29

- 新增阶段末 `Stage-End Review-Repair Contract`，将候选摄影稿固定为 `candidate -> review -> direct repair -> re-review -> canonical writeback` 闭环。
- 在 workflow 中新增 `N8R-DIRECT-REPAIR` 与 `N8R-REVIEW-AGAIN`，要求 review 阻断项在 `3-摄影` 阶段内最小修复并复审后才能交给下游。
- 更新 review gate、CONTEXT 和执行报告字段，明确覆盖、编号、节拍、连续性、专业可执行、峰值分镜和保真问题不得降级为交付后 followup。

## 2026-04-28

- 新增 `references/peak-shot-language-contract.md`，承接 `2-编导` 的高潮画面机制，补齐摄影阶段的峰值分镜、分镜明细和运镜强化合同。
- 在 workflow 中新增 `N5.5-PEAK-SHOT`，要求上游高点形成内部 `peak_shot_profile`，决定分镜密度、景别尺度、运镜速度、停顿/断裂和余波交接。
- 在 review gate 中新增高潮分镜检查，避免上游高点被按普通画面压平，也禁止为了强化高潮新增事实、对白或动作结果。
- 同步更新技法库、画面节奏、模板、README 与 CONTEXT，明确高潮镜头不等于一律加速加镜头。

## 2026-04-25

- 初始化 `aigc/3-摄影` Skill 2.0 包结构。
- 建立以 `2-编导/第N集.md` 为输入、`3-摄影/第N集.md` 为输出的摄影分镜明细注入合同。
- 新增画面匹配、节拍分析、分镜明细注入、经典构图、高超运镜、高能转场、光影美学、色彩美学等动态引用分区。
- 增加 `诡校-测试版` 编导稿样本导出的封闭校园惊悚视觉母题经验。
- 补充景别、景深、镜头视角、镜头类型、运镜速度等摄影执行参数细则，并同步到输出模板与 review gate。
- 新增动态分镜明细表达合同，要求 `分镜N` 写成从起点到终点的变化、组合运镜、速度曲线和注意力转移路径，避免静态呆板参数堆叠。
- 新增镜头连续性合同，要求每个画面句子的分镜明细回看临近至少前 3 个画面单位，避免无动机跳轴、跳色、跳景别、空间跳跃和风格断裂。
- 新增画面节奏分析合同，用 `rhythm_profile` 控制分镜明细的收敛、标准展开、发散强化和断裂发散，保证不同信息重要性的画面句子张弛有度。
- 调整连续性输出策略：前 3 画面回看作为内部判断，不在每条 `分镜N` 中机械显式展示；输出集中于当前画面，仅在明显跳变或强转场时短写承接动机。
- 调整画面节奏输出策略：`rhythm_profile` 作为内部判断，不在 `分镜N` 中显式展示“收敛/标准展开/发散强化/断裂发散”标签。
- 补充项目级上下文加载要求：绑定具体项目时必须加载 `MEMORY.md`、`0-初始化/north_star.yaml`、`team.yaml` 与相关 `CONTEXT/`。
