# Review Contract

本文件定义 `5-摄影` 的质量门禁。

若本轮启动 subagents 模式，review gate 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`：是否从项目 `team.yaml` 解析监制组相关智能顾问团、是否基于当前 `PASS-CINE-*` / `N*-*` 思维·执行节点派生顾问问题、是否要求顾问代入角色意识/创作风格/专业水准参与节点判断和执行取舍、是否形成 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写 `4-表演` 原文。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 落盘前或修复时 | 检查 `分镜明细：` 覆盖、`分镜N` 连续、路径和命名 |
| `cinematic_quality_review` | 交付前 | 检查构图、运镜、边界交出、光影、色彩是否服务戏剧 |
| `handoff_boundary_review` | 交付前 | 检查场景变化是否形成交出点/进入提示，是否只保留可见交出锚点而未落盘组间/跨场景创意转场方案 |
| `shot_plan_projection_review` | 交付前 | 检查 references 细则是否汇流为 `shot_design_plan`，以及每个 `分镜N` 是否能反推节拍、节奏、连续性、技法和交出点 |
| `sequence_ownership_review` | 交付前 | 检查段落级 `sequence_profile` 是否只作为内部连续性上下文，每个 `分镜明细` 是否仍只服务正上方画面句子，没有跨块外溢或失主镜头 |
| `shot_duration_review` | 交付前 | 检查每个 `分镜N` 是否以 `分镜N（约X秒）:` 显式落盘，并能反推时值等级、短剧·AIGC 压缩偏置、对白台词量预算、停顿/压缩理由、相邻镜头时值接力和 15 秒组内节奏风险 |
| `functional_projection_review` | 交付前 | 检查每个 `分镜N` 是否有影视功能、运镜策略和下游 AIGC 可消费 payload，而不是随机好看句 |
| `ai_video_prompt_execution_review` | 交付前 | 检查每个 `分镜N` 是否符合 AI 视频执行稳定性：镜头先行包裹动作、方向参照明确、光线写结果、表演微动态可见，且未把完整提示词分栏或命令式负向词塞入分镜正文 |
| `thinking_action_node_review` | 交付前 | 检查 `PASS-CINE-*` / `N*-*` 是否完成真源锁定、画面匹配、类型画像、段落观看意图与逐点归属、节拍、节奏、镜头时值、高点、连续性、摄影语法、功能投影、AI 视频执行稳定性、计划汇流、自然注入和阶段内修复闭环 |
| `camera_grammar_review` | 交付前 | 检查景别梯度、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化是否有节拍、空间、信息或情绪动机 |
| `camera_design_scope_review` | 交付前 | 检查 `分镜明细：` 是否只承载运镜手法、摄影美学、内部注意力转交和可消费交出锚点，没有抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 |
| `natural_language_review` | 交付前 | 检查 `分镜明细：` 是否读起来像自然中文镜头文字，而不是参数清单、模板填空或连续同构句 |
| `shot_count_distribution_review` | 交付前 | 检查同一集或同一场分镜数量是否被模板化为固定 2 镜；抽样确认 1/2/3/4 镜均来自真实节拍 |
| `sequence_density_curve_review` | 交付前 | 检查连续观看段落是否形成 `sequence_density_curve`：有清楚 `tempo_beats / density_ramp / peak_slots / recovery_slots / set_piece_chain_slots / sound_cut_pattern / density_budget / handoff_anchors`，而不是只做单句分镜数判断 |
| `faithfulness_review` | 有改写风险时 | diff 上游 `4-表演`，确认正文事实、对白、顺序未被改写 |

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/cinematography-workflow.md` 的 `N8R-DIRECT-REPAIR`，由 `5-摄影` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `5-摄影/第N集.md`。
- 允许直接修复的范围：`分镜明细：` 覆盖、`分镜N` 连续编号、节拍数量、画面节奏、镜头时值、`shot_design_plan` 汇流、AI 视频执行稳定性、镜头连续性、专业可执行性、动态表达、峰值分镜、执行报告和 review 证据。
- 禁止直接修复的范围：改写 `4-表演` 原文、对白、场景标题、字段顺序、剧情事实或上游 source truth。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何覆盖、编号、保真、空间连续性、专业可执行、AI 视频执行稳定性或 LLM-first 问题不得降级为 followup。

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-CINE-01` | 输入回指 | frontmatter 或报告记录 `source_directing_path` |
| `GATE-CINE-02` | 画面覆盖 | 所有命中画面性句子下方就近有 `分镜明细：` |
| `GATE-CINE-03` | 分镜编号 | 每个分镜明细块从 `分镜1（约X秒）:` 开始，连续编号，无跳号 |
| `GATE-CINE-04` | 节拍合理 | 分镜数量与当前画面句子的动作、信息、情绪节拍匹配 |
| `GATE-CINE-04A` | 数量去模板化 | 1/2/3/4 镜来自 `shot_count_decision`；同一集或同一场若 2 镜占比异常集中，已抽样复判并修正低信息硬撑、关键信息压平或模板继承 |
| `GATE-CINE-04A2` | 段落密度曲线 | 连续观看段落已形成内部 `sequence_density_curve`；能说明哪里省镜头、哪里加密、哪里停顿、哪里硬切、哪里交出；高密度后有恢复/反压/余波，且整段不是全满、全空或平均同密度 |
| `GATE-CINE-04A3` | set-piece 链条例外 | 单个 `visual_unit` 扩展到 5-6 镜时，必须命中 `set_piece_chain_slot` 或 `sound_cut_pattern`，每镜都有独立起点、撞点、动作结果、声音打点或反应落点；删掉任一镜都会损失必要节奏拍 |
| `GATE-CINE-04B` | 镜头时值 | 每个 `分镜N` 均写成 `分镜N（约X秒）:`，并能反推 `shot_duration_decision`：时值等级、短剧·AIGC 压缩偏置、对白台词量预算、停顿/压缩理由、缩短或拉长的损失、相邻镜头时值接力和 15 秒组内节奏风险；`约3秒` 以上有台词、读秒、表演变化、复杂调度、空间重置或高点证据 |
| `GATE-CINE-04C` | 对白时长承托 | `对白画面`、`旁白画面`、画外音或反应镜头承载台词时，`约X秒` 不低于台词量最低时长；若台词跨镜延续，已在 `shot_design_plan` 或报告中说明各镜承载段落 |
| `GATE-CINE-04D` | 逐画面点归属 | 相邻画面单位可形成内部 `sequence_profile`，但每个 `分镜明细` 只服务正上方画面句子；每条 `分镜N` 能回指所属 `visual_unit`，没有为了段落流畅吞入后文主体动作、对白反应、记忆段、道具揭示或跨场景连接方案 |
| `GATE-CINE-05` | 画面节奏 | 低信息/过场句收敛，关键揭示/强情绪/空间重置句发散，描述密度与信息重要性匹配 |
| `GATE-CINE-06` | 连续性回看 | 当前分镜明细已在内部承接临近至少前 3 个画面单位；不足 3 个时承接已有画面单位，输出不机械展示回看过程 |
| `GATE-CINE-07` | 专业可执行 | 内部锁定景别、景深、镜头视角、镜头类型、运镜速度等必要参数；成稿只显式写当前节拍最关键的摄影选择，并按需要补充构图、机位、运动、光影、色彩或交出锚点中的有效选择 |
| `GATE-CINE-08` | 动态流畅 | 分镜明细能反推出起点、路径、速度变化、显式秒数对应的时值等级和注意力转移，不是静态标签列表，也不是机械套句 |
| `GATE-CINE-09` | 分镜计划投影 | 每个 `visual_unit` 输出前已有 `shot_design_plan`；最终 `分镜N` 的数量、顺序、入口、单镜时值、摄影语法、运镜路径、停点、落点和交出点可反推 beat/rhythm/duration/continuity/handoff/camera/function |
| `GATE-CINE-10` | 字段语义纯度 | `分镜明细：` 是兼容字段名，内容按运镜摄影设计写作；不输出抽象主题、心理结论、世界观解释、导演阐释或不可执行的气氛口号 |
| `GATE-CINE-11` | 空间一致 | 没有无动机跳轴、反向运动、景别断崖、光色突变或风格断裂 |
| `GATE-CINE-12` | 戏剧服务 | 技法服务角色、危险、信息揭示或空间压迫，不是孤立炫技 |
| `GATE-CINE-13` | 原文保真 | 除新增 frontmatter/report 和 `分镜明细` 外，不改写 `4-表演` 正文 |
| `GATE-CINE-14` | 高潮分镜 | 上游存在 `peak_visual_policy`、`peak_visual_pass` 或明显高潮/爽点/高光画面时，摄影稿完成峰值分镜强化，且不新增事实、对白或动作结果 |
| `GATE-CINE-15` | 功能性投影 | 每个 `分镜N` 可抽取 shot_function、visible_subject、action_phase、camera_movement_plan、composition_anchor、light_color_material、continuity_handoff 和下游消费点 |
| `GATE-CINE-15A` | AI 视频执行稳定性 | 每个 `分镜N` 能还原镜头先行执行顺序：镜头/运动/构图先包裹动作；人物运动有相对镜头或画面的方向参照；重要光影写成亮面、暗面、阴影、轮廓、反光或背景层次；表演情绪落到可见微动态；正文不输出完整提示词分栏模板或命令式负向词 |
| `GATE-CINE-16` | 摄影语法变化 | 景别、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化服务节拍、空间、信息、情绪或交接；不存在随机换技法、无动机大远景跳大特写或视角乱跳 |
| `GATE-CINE-17` | 思维·执行节点完整 | 产物能回指 `PASS-CINE-00..12`、`PASS-CINE-02S`、`PASS-CINE-02D`、`PASS-CINE-04D` 与 `N1-INTAKE/N2-MATCH/N3-TYPE/N3.5-SEQUENCE-ALIGN/N3.6-DENSITY-CURVE/N4-BEAT/N5-RHYTHM/N5.2-DURATION/N5.5-PEAK-SHOT/N5.6-ADVISOR/N6-CONTINUITY/N6.1-HANDOFF/N6.2-CAMERA-GRAMMAR/N6.4-FUNCTIONAL-PROJECTION/N6.5-SHOT-PLAN/N7-INJECT/N8-REVIEW/N8R-DIRECT-REPAIR/N8R-REVIEW-AGAIN/N9-WRITE` 的关键判断：真源、画面匹配、类型、段落观看意图与逐点归属、段落密度曲线、节拍、节奏、镜头时值、高点、顾问、连续性、边界交出、摄影语法、功能投影、AI 视频执行稳定性、计划、注入、审查修复 |
| `GATE-CINE-18` | 自然成稿 | 连续分镜不出现重复句法骨架、参数清单腔或“高级/丝滑/电影感”等空泛效果词；读起来先是画面，再是摄影 |
| `GATE-CINE-19` | 输出路径 | 写入 `projects/aigc/<项目名>/5-摄影/第N集.md` 和 `执行报告.md` |
| `GATE-CINE-20` | 顾问请教 | 启动 subagents 模式时，已完成 `team.yaml` 监制顾问请教；顾问问题同步于当前思维·执行节点，并沉淀为后续上下文，或记录上层阻断降级 |
| `GATE-CINE-21` | 边界交出 | 场景变化已处理上一画面交出点和下一画面进入提示；所有声画、形态、颜色、文字或高点余波只作为可见交出锚点记录，没有在本阶段写成组间/跨场景创意转场方案 |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-CINE-02` | 漏掉画面性句子 | `references/visual-matching-contract.md` |
| `FAIL-CINE-03` | 分镜过粗、过碎或固定模板化 | `references/beat-analysis-contract.md` |
| `FAIL-CINE-03A` | 分镜数量塌缩为固定 2 镜或同数分布异常，无法证明每个 `分镜2` 的真实观看策略 | `references/beat-analysis-contract.md`、`references/visual-rhythm-analysis-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-03D` | 整场或连续段落缺少密度曲线：全满、全空、平均同密度、峰值后无恢复/反压，或只统计 `shot_count_distribution` 但没有 `density_curve_summary` | `references/sequence-density-curve-contract.md`、`references/visual-rhythm-analysis-contract.md`、`steps/cinematography-workflow.md#N3.6-DENSITY-CURVE`、`steps/cinematography-workflow.md#N5-RHYTHM` |
| `FAIL-CINE-03E` | 5-6 镜 set-piece 链条没有真实连续动作/声音结果，或每镜不能证明独立起点、撞点、结果、声音打点、反应落点 | `references/sequence-density-curve-contract.md#set-piece-chain-exception`、`references/beat-analysis-contract.md#Shot-Count-Cardinality-Guard`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-03B` | 分镜数量正确但单镜长短错误：缺少 `分镜N（约X秒）`、文字/道具/微表情被快速切走，低信息镜头被拖长，普通氛围镜普遍超过 `standard`，连续同长同速，或 15 秒组内节奏风险未裁决 | `references/shot-duration-decision-contract.md`、`references/visual-rhythm-analysis-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N5.2-DURATION` |
| `FAIL-CINE-03C` | 对白/旁白画面未按台词量裁决时长，导致台词未说完就切走、反应镜头承托不足或短对白被无意义拖长 | `references/shot-duration-decision-contract.md#Dialogue Duration Rule`、`steps/cinematography-workflow.md#N5.2-DURATION` |
| `FAIL-CINE-05M` | 段落级连续运镜吞掉逐画面点归属：分镜整体流畅但无法回指正上方画面句子，或提前写入后文主体动作、对白反应、记忆段、道具揭示、跨场景连接方案 | `references/visual-sequence-alignment-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N3.5-SEQUENCE-ALIGN`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-04` | `分镜明细` 缺失或编号断裂 | `templates/output-template.md`、`scripts/validate_cinematography_markup.py` |
| `FAIL-CINE-05` | 分镜明细空泛 | `references/cinematic-technique-library.md` |
| `FAIL-CINE-05A` | 分镜明细混入抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 | `SKILL.md` Output Contract、`templates/output-template.md` |
| `FAIL-CINE-05B` | 分镜明细静态呆板，没有变化和组合运镜 | `references/dynamic-lens-language-contract.md` |
| `FAIL-CINE-05L` | 分镜明细无法反推时值等级、停顿/压缩理由或相邻镜头时值接力 | `references/shot-duration-decision-contract.md`、`references/dynamic-lens-language-contract.md`、`steps/cinematography-workflow.md#N5.2-DURATION` |
| `FAIL-CINE-05C` | 当前分镜明细与临近镜头断裂、跳轴、跳色或空间跳跃 | `references/shot-continuity-contract.md` |
| `FAIL-CINE-05D` | 分镜明细不分轻重，低信息过度发散或重信息过度收敛 | `references/visual-rhythm-analysis-contract.md` |
| `FAIL-CINE-05E` | 上游高点被按普通画面压平，或高潮强化缺少分镜/运镜/停顿/余波策略 | `references/peak-shot-language-contract.md` |
| `FAIL-CINE-05F` | references 被引用但未汇流成 `shot_design_plan`，导致分镜数量随机、上下不接或输出过短 | `references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05G` | 分镜明细出现参数清单、连续同构句、模板填空腔或过度显式化内部计划 | `references/natural-shot-detail-writing-contract.md`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05H` | 分镜明细表达顺滑但缺少影视功能、运镜策略、主体/动作/构图/光色/空间锚点或下游 AIGC 可消费 payload | `references/functional-cinematic-projection-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05N` | 分镜明细不适合稳定改写为 AI 视频提示词：动作和镜头割裂、方向参照含混、光线只写光源或空泛效果、情绪没有可见微动态，或把完整提示词分栏/命令式负向词写进正文 | `references/ai-video-prompt-execution-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05I` | 景别、镜头视角、景深/焦点、镜头类型或构图变化随机，无法回指节拍、空间、信息、情绪或连续性交接 | `references/cinematic-technique-library.md`、`steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` |
| `FAIL-CINE-05K` | 场景变化没有交出点/进入提示，或把组间/跨场景创意转场方案落在 `5-摄影` | `references/transition-design-contract.md`、`references/shot-continuity-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05J` | 思维·执行节点缺环：未完成画面匹配、类型画像、段落观看意图与逐点归属、摄影语法、功能投影、计划汇流或阶段内修复闭环，却直接写出 `分镜明细` | `steps/cinematography-workflow.md`、`SKILL.md#Thought Pass Map` |
| `FAIL-CINE-06` | 改写原编导稿 | `SKILL.md` Output Contract 和本文件 `faithfulness_review` |
| `FAIL-CINE-07` | 启动 subagents 模式时缺少顾问请教、节点同步问题、角色意识/创作风格/专业水准参谋、上下文沉淀或降级说明 | `../../_shared/team-advisor-consultation-contract.md` + `../SKILL.md#Subagents Execution Mechanism` |

## Review Output

执行报告至少记录：

- 输入文件与输出文件。
- 处理集号。
- 画面性句子数量。
- `分镜明细` 块数量。
- 机械校验结果或人工 review 结果。
- 画面节奏张弛结果。
- 镜头时值裁决结果：duration profile、显式秒数抽样、长停顿/快速镜抽样、15 秒组内节奏风险。
- 对白台词量预算结果：对白/旁白承托画面数量、台词量下限抽样、跨镜延续说明。
- 分镜数量分布与 2 镜集中抽样复判结果。
- 段落密度曲线结果：`density_curve_summary`、`tempo_beats`、`density_ramp`、`peak_slots`、`recovery_slots`、`set_piece_chain_slots`、`sound_cut_pattern` 和 `density_budget`。
- 段落观看意图与逐画面点归属检查结果：是否形成 `sequence_profile`、是否有 `unit_ownership_map`、是否未发生跨块外溢或失主镜头。
- 高潮分镜强化结果。
- `shot_design_plan` 汇流与投影检查结果。
- 边界交出检查结果：场景变化交出点/进入提示、可见交出锚点，以及是否未在本阶段落盘创意转场方案。
- 摄影语法变化检查结果：景别梯度、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化。
- 功能性影视投影与 AIGC 下游可消费性检查结果。
- AI 视频执行稳定性检查结果：镜头先行、方向参照、光线结果、表演微动态、提示词模板腔和命令式负向词风险。
- 顾问请教 roster 来源、问题类型、可执行指导或降级说明。
- 镜头连续性、空间一致性和风格一致性结果。
- 运镜摄影设计纯度检查结果。
- 自然成稿检查结果。
- 需要返工的行号或字段标签。
- repair actions、复审 verdict、未修复风险和是否允许进入下游阶段。
