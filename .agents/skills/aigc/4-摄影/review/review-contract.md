# Review Contract

本文件定义 `4-摄影` 的质量门禁。

若项目存在初始化团队综合，review gate 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Init Team Synthesis Consumption`：本阶段是否只读取 `team.yaml.init_synthesis.stage_seed_summary."4-摄影"`、`init_handoff.cinematography_seed` 与 `north_star.yaml.创作阶段不变量.摄影`，是否形成 `init_team_synthesis_context`，是否把初始化阶段已统合的可执行约束、启发和风险沉淀为后续任务上下文，并且未在创作阶段调用 team 成员身份、解析旧 stage profile、补造顾问问答或改写 `3-运动` / 回退 `2-编导` 原文。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 落盘前或修复时 | 检查原画面性字段标题覆盖、字段下 `时间段` 连续、路径和命名 |
| `cinematic_quality_review` | 交付前 | 检查构图、运镜、边界交出、光影、色彩是否服务戏剧 |
| `handoff_boundary_review` | 交付前 | 检查场景变化是否形成交出点/进入提示，是否只保留可见交出锚点而未落盘组间/跨场景创意转场方案 |
| `shot_plan_projection_review` | 交付前 | 检查 references 细则是否汇流为 `shot_design_plan`，以及每个 `时间段` 是否能反推节拍、节奏、连续性、技法和交出点 |
| `source_detail_preservation_review` | 交付前 | 检查每个 `visual_unit` 是否形成 `source_visible_fact_map`，原画面描述中的必须保留可见事实是否完整绑定到具体时间段、焦点、构图、运镜或光线变化，且未因非复述、克制或短剧压缩被摘要删短 |
| `reference_gate_coverage_review` | 交付前 | 检查本轮加载或产生强制裁决的每个 `references/` 细则是否能回指 PASS/N 节点、`GATE-CINE-*`、`FAIL-CINE-*` 和执行报告证据；解释性 glossary / example guard 不拥有独立强制裁决权，若被用作阻断依据也必须回接本表 |
| `single_shot_multi_beat_review` | 交付前 | 对所有 1 段块做全量或高风险抽样复核：源句或 `第一段` 内若出现主体切换、空间转移、动作分相、声画转交、信息揭示、情绪转折或注意力对象改变，必须拆镜或形成 `trigger_merge_exception` 证明 |
| `sequence_ownership_review` | 交付前 | 检查段落级 `sequence_profile` 是否只作为内部连续性上下文，每组原字段标题下的时间段是否仍只服务正上方画面句子，没有跨字段外溢或失主镜头 |
| `format_continuity_surface_review` | 交付前 | 检查当前原字段标题 + 连续时间段格式是否真正承载上下画面连续性：字段内相邻时间段首尾相接，字段间末段/首段可互相消费，段落级连续性未越过逐画面点归属 |
| `shot_duration_review` | 交付前 | 检查每个 `时间段` 是否以 `[起始秒-结束秒]` 显式落盘，并能反推时值等级、短剧·AIGC 压缩偏置、对白台词量预算、停顿/压缩理由、相邻时间段时值接力和 15 秒组内节奏风险 |
| `functional_projection_review` | 交付前 | 检查每个 `时间段` 是否有影视功能、运镜策略和下游 AIGC 可消费 payload，而不是随机好看句 |
| `shot_detail_completeness_review` | 交付前 | 检查每条 `[起始秒-结束秒]` 是否按 L0/L1/L2/L3 梯度覆盖必要维度：低信息镜是否克制，标准镜是否可拍可接，重点镜是否承托表演/信息/关系，峰值镜是否证明时值、余波和下游稳定性 |
| `content_paraphrase_review` | 交付前 | 对候选 `时间段` 做源句复述扣除测试：去掉上游原句已有主体、动作、道具和事实后，仍能读出摄影机如何看、动、停、转焦、布光或交接 |
| `ai_video_prompt_execution_review` | 交付前 | 检查每个 `时间段` 是否符合 AI 视频执行稳定性：镜头先行包裹动作、方向参照明确、光线写结果、表演微动态可见，且未把完整提示词分栏或命令式负向词塞入分镜正文 |
| `scene_shot_identity_review` | 交付前 | 检查需要进入图像或视频阶段的分镜是否先锁定场景身份和镜头身份：年代/空间功能/环境声基底/材质光影、摄影机位置朝向、相对画面方向和动作在镜头内部发生 |
| `two_person_axis_review` | 交付前 | 检查双人/多人对峙、追逐、动作、逼问或谈判场是否锁定 line of action、screen left/right、middle_spatial_anchor 和 camera_half_space；每条可下游消费分镜是否重复空间锚点；换轴是否通过中性、主观或运动桥接 |
| `viewer_discovery_review` | 交付前 | 检查人物行走、入场、压迫、群像和空间建立镜头是否避免无动机正面平视全信息展示；低角度、前景遮挡、透视拉伸、手持微晃或慢速揭示是否有观看任务和可见结果 |
| `action_first_continuity_review` | 交付前 | 检查每条涉及人物的 `时间段` 是否先承接人物姿态、位置、朝向、身体接触、动作方向和注意力落点；触碰/取用/查看/避开对象是否空间可达；道具/环境细节是否通过准入且未抢走动作链 |
| `intra_inter_shot_continuity_review` | 交付前 | 检查每条 `时间段` 是否能抽出 `entry/action_anchor/exit/handoff`；同一原字段标题下相邻时间段是否有物理因果链或过渡锚点，相邻字段之间是否继承人物姿态、轴线、运动方向、光色或声音余波 |
| `action_reaction_focus_review` | 交付前 | 检查多人 beat 是否明确行动者、反应者和背景参与者；镜头是否保留动作-反应因果焦点，而不是让所有角色同强度表演或用奇怪角度同时照顾所有人 |
| `thinking_action_node_review` | 交付前 | 检查 `PASS-CINE-*` / `N*-*` 是否完成真源锁定、画面匹配、类型画像、段落观看意图与逐点归属、节拍、节奏、镜头时值、高点、连续性、摄影语法、功能投影、AI 视频执行稳定性、计划汇流、自然注入和阶段内修复闭环 |
| `camera_grammar_review` | 交付前 | 检查景别梯度、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化是否有节拍、空间、信息或情绪动机 |
| `camera_design_scope_review` | 交付前 | 检查原画面性字段正文是否只承载运镜手法、摄影美学、扩展维度信息点、内部注意力转交和可消费交出锚点，没有抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 |
| `scene_visual_constraint_review` | 交付前 | 检查每个场景是否已形成内部场景视觉约束 `scene_visual_constraint`，约束覆盖构图布局（主体/陪体/前景/背景）、构图方式（形状感/线条感/影调感/虚实感/节奏感/纹理质感/气势中选取 2-3 个子维度）、光源设置效果、色彩体系和关键摄影技术参数；同一场景视觉约束不变时只裁决一次，变化时可重新裁决；纯内部裁决，不检查成稿中的画面基调语句 |
| `shot_detail_dimension_review` | 交付前 | 检查每条 `时间段` 的自然语句是否覆盖了当前画面中自然存在的扩展维度信息点（角色表演/非角色动态/镜头技术/光影精细/焦点精细/节奏同步）；遵循"应有则有、没有不必强制"原则，画面中有角色就写角色表演，没有则跳过，不为凑数虚构画面中不存在的信息；维度信息融入自然中文而非标签列表 |
| `shot_narrative_function_review` | 交付前 | 检查每条计划时间段是否形成 `shot_narrative_function`，能说明信息、关系、情绪、动作结果、观看发现或交出价值；删除后无损失的镜头必须删并或重写 |
| `movement_depth_narrative_review` | 交付前 | 检查 `camera_movement_emotion_plan` 与 `depth_of_field_narrative_plan`：运镜是否有情绪语义、速度曲线和停点，景深/焦点是否承担隐藏、揭示、隔离、主观偏差或注意力转移 |
| `light_narrative_review` | 交付前 | 检查 `light_narrative_plan`：光线是否说明照亮/遮蔽对象、阴影/轮廓结果、信息可见性、权力关系、情绪温度或危险预告，而不是只写来源词或氛围词 |
| `attention_guidance_review` | 交付前 | 检查 `attention_guidance_plan`：观众入口、遮挡/显影、焦点接力、信息获得点和离场锚点是否清楚，是否避免一次性全信息平铺 |
| `dialogue_scene_variation_review` | 交付前 | 检查对白场景是否形成 `dialogue_scene_variation_plan`，焦点选择是否来自戏剧功能、权力关系、观众知情层级和注意力路径，是否避免机械正反打、每句说话者特写和说话者/听话者覆盖式配平 |
| `long_dialogue_visual_review` | 交付前 | 检查长对白是否形成 `long_dialogue_visual_plan`，逐 beat 分配说话者、听者、空间压力、手部/道具、群像、画外声源或沉默余波焦点，并与 `dialogue_time_budget` 和 `long_dialogue_delivery_map` 连续对齐 |
| `prop_shot_admission_review` | 交付前 | 检查道具、反射、倒影、涟漪、餐具/杯子/纸张/桌面等物件细节是否通过准入：角色互动、关键信息/规则/证据/危险源或必要环境交代；无互动普通道具不得成为独立镜头、焦点拉移终点、反射主体或动作衔接节点 |
| `natural_language_review` | 交付前 | 检查原画面性字段下的时间段是否读起来像自然中文镜头文字，而不是参数清单、模板填空或连续同构句 |
| `shot_count_distribution_review` | 交付前 | 检查同一集或同一场时间段数量是否被模板化为固定 2 段；抽样确认 1/2/3/4 镜均来自有效触发点、观看结果或叙事节奏价值。机械校验提示 2 段集中时只触发复核，不默认阻断 |
| `sequence_density_curve_review` | 交付前 | 检查连续观看段落是否形成 `sequence_density_curve`：有清楚 `tempo_beats / density_ramp / peak_slots / recovery_slots / set_piece_chain_slots / sound_cut_pattern / density_budget / handoff_anchors`，而不是只做单句时间段数判断 |
| `faithfulness_review` | 有改写风险时 | diff 上游 `3-运动` 或回退 `2-编导`，确认正文事实、对白、顺序未被改写 |

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/cinematography-workflow.md` 的 `N8R-DIRECT-REPAIR`，由 `4-摄影` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `4-摄影/第N集.md`。
- 允许直接修复的范围：原画面性字段下的 `时间段` 覆盖、连续时间段、节拍数量、单段吞多 beat、画面节奏、镜头时值、`shot_design_plan` 汇流、reference gate 覆盖证据、源句复述扣除失败、AI 视频执行稳定性、镜头连续性、动作-反应焦点、专业可执行性、动态表达、峰值分镜、执行报告和 review 证据。
- 禁止直接修复的范围：改写 `3-运动` 或回退 `2-编导` 原文、对白、场景标题、字段顺序、剧情事实或上游 source truth。遇到这类问题必须输出 source owner 和不可用说明。
- `pass_with_followups` 只允许非阻断质量建议；任何覆盖、时间段、保真、空间连续性、梯度描述完整性、镜内/镜间连贯性、专业可执行、源句复述扣除失败、AI 视频执行稳定性或 LLM-first 问题不得降级为 followup。

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-CINE-01` | 输入回指 | frontmatter 或报告记录 `source_motion_path`；回退模式可记录 `source_writing_directing_path` |
| `GATE-CINE-02` | 画面覆盖 | 所有命中画面性句子的原字段标题被保留，且字段下方就地展开连续 `[起始秒-结束秒]` 时间段；`心理反应/心理变化/情绪反应/思考反应/认知变化/内心反应` 不被当作非画面字段漏掉 |
| `GATE-CINE-03` | 时间段连续性 | 每个原画面性字段标题下都从 `[0-...秒]` 开始，连续时间段，无断裂 |
| `GATE-CINE-04` | 节拍合理 | 时间段数量与当前画面句子的动作、信息、情绪节拍匹配 |
| `GATE-CINE-04A` | 数量去模板化 | 1/2/3/4 段来自 `shot_count_decision` 和有效触发点；同一集或同一场若 2 段占比异常集中，已抽样复核低信息硬撑、关键信息压平或模板继承；2 段集中本身允许通过，只有抽样发现 `第二段` 无触发、无观看结果、无叙事节奏价值时才不通过 |
| `GATE-CINE-04E` | 单段多 beat 压平 | 所有 1 段块已复核：若源句或 `第一段` 内存在多个有效触发点、连续观看策略或多段注意力转交，必须拆成多个时间段；只有同段能清楚完成且不损失观看结果、平台节奏、下游 payload 或人物动作连续性时，才允许以 `trigger_merge_exception` 合并 |
| `GATE-CINE-04A2` | 段落密度曲线 | 连续观看段落已形成内部 `sequence_density_curve`；能说明哪里省镜头、哪里加密、哪里停顿、哪里硬切、哪里交出；高密度后有恢复/反压/余波，且整段不是全满、全空或平均同密度 |
| `GATE-CINE-04A3` | set-piece 链条例外 | 单个 `visual_unit` 扩展到 5-6 段时，必须命中 `set_piece_chain_slot` 或 `sound_cut_pattern`，每段都有独立起点、撞点、动作结果、声音打点或反应落点；删掉任一段都会损失必要节奏拍 |
| `GATE-CINE-04B` | 镜头时值 | 每个 `时间段` 均写成 `[起始秒-结束秒]`，并能反推 `shot_duration_decision`：时值等级、短剧·AIGC 压缩偏置、对白台词量预算、停顿/压缩理由、缩短或拉长的损失、相邻时间段时值接力和 15 秒组内节奏风险；非 `slow_burn/hold` 的 3 秒以上时间段有台词、读秒、表演变化、复杂调度、空间重置或高点证据；情绪类 `slow_burn/hold` 时间段有可见微动态、静止压力、极慢运动或框内变化 |
| `GATE-CINE-04C` | 对白时长承托 | 原字段标题下承载对白、旁白、画外音或反应镜头的时间段，不得低于台词量最低时长；若台词跨段延续，已在 `shot_design_plan` 或报告中说明各段承载的台词与反应 |
| `GATE-CINE-04D` | 逐画面点归属 | 相邻画面单位可形成内部 `sequence_profile`，但每组时间段只服务正上方画面句子或原字段标题；每条 `时间段` 能回指所属 `visual_unit`，没有为了段落流畅吞入后文主体动作、对白反应、记忆段、道具揭示或跨场景连接方案 |
| `GATE-CINE-05` | 画面节奏 | 低信息/过场句收敛，关键揭示/强情绪/空间重置句发散，描述密度与信息重要性匹配 |
| `GATE-CINE-06` | 连续性回看 | 当前原字段标题下的时间段已在内部承接临近至少前 3 个画面单位；不足 3 个时承接已有画面单位，输出不机械展示回看过程 |
| `GATE-CINE-06A` | 动作链优先 | 每条涉及人物的 `时间段` 先承接人物姿态、站位、朝向、身体接触、动作方向和注意力落点；触碰/取用/查看/避开对象前空间可达；镜头切点、焦点和时值没有被无互动对象牵引 |
| `GATE-CINE-07` | 专业可执行 | 内部锁定景别、景深、镜头视角、镜头类型、运镜速度等必要参数；成稿只显式写当前节拍最关键的摄影选择，并按需要补充构图、机位、运动、光影、色彩或交出锚点中的有效选择 |
| `GATE-CINE-08` | 动态流畅 | 原字段标题下的时间段能反推出起点、路径、速度变化、时间范围对应的时值等级和注意力转移，不是静态标签列表，也不是机械套句 |
| `GATE-CINE-09` | 分镜计划投影 | 每个 `visual_unit` 输出前已有 `shot_design_plan`；最终 `时间段` 的数量、顺序、入口、单段时值、摄影语法、运镜路径、停点、落点和交出点可反推 beat/rhythm/duration/continuity/handoff/camera/function |
| `GATE-CINE-10` | 字段语义纯度 | 原画面性字段标题是兼容字段名，字段下时间段按运镜摄影设计写作；不输出抽象主题、裸心理结论、思考摘要、世界观解释、导演阐释或不可执行的气氛口号；心理反应和思考反应必须转译为可见表演微动态；不得新增统一 `分镜画面：` 字段 |
| `GATE-CINE-11` | 空间一致 | 没有无动机跳轴、反向运动、景别断崖、光色突变或风格断裂 |
| `GATE-CINE-12` | 戏剧服务 | 技法服务角色、危险、信息揭示或空间压迫，不是孤立炫技 |
| `GATE-CINE-13` | 原文保真 | 除新增 frontmatter/report 与画面性字段正文改写为原标题下连续时间段外，不改写 `3-运动` 或回退 `2-编导` 的场景、对白、非画面字段、画面性字段标题、字段顺序和剧情事实 |
| `GATE-CINE-14` | 高潮分镜 | 上游存在 `peak_visual_policy`、`peak_visual_pass` 或明显高潮/爽点/高光画面时，摄影稿完成峰值分镜强化，且不新增事实、对白或动作结果 |
| `GATE-CINE-15` | 功能性投影 | 每个 `时间段` 可抽取 shot_function、visible_subject、action_phase、camera_movement_plan、composition_anchor、light_color_material、continuity_handoff 和下游消费点 |
| `GATE-CINE-15C` | 梯度描述完整性 | 每条 `[起始秒-结束秒]` 已按 L0/L1/L2/L3 选择足够维度：L0 不空泛，L1 可拍可接，L2 承托表演/信息/关系，L3 承托峰值/set-piece；15 项是维度池而非逐段硬填，成稿不得标签清单化，也不得短到只剩“慢推/压迫感/电影感”；不得为了完整性堆砌分镜或把低信息画面升级为峰值镜 |
| `GATE-CINE-15D` | 镜内/镜间连贯性 | 每条 `时间段` 能抽出 `entry/action_anchor/exit/handoff`；同一原字段标题下相邻时间段有物理因果链或过渡锚点；相邻画面性字段之间继承上一字段最后一段的人物姿态、位置、朝向、身体接触、手部状态、轴线、运动方向、光色或声音余波，变化时有可见动作或桥接；当前输出格式本身能读出字段内 `segment_link`、字段间 `field_link_chain` 和段落级 `sequence_link` |
| `GATE-CINE-15A` | AI 视频执行稳定性 | 每个 `时间段` 能还原镜头先行执行顺序：镜头/运动/构图先包裹动作；人物运动有相对镜头或画面的方向参照；重要光影写成亮面、暗面、阴影、轮廓、反光或背景层次；表演情绪落到可见微动态；人物行走、入场、压迫、群像和空间建立镜头有机位高度/前景/透视/发现路径裁决，未无动机退化为正面平视全信息展示；正文不输出完整提示词分栏模板或命令式负向词 |
| `GATE-CINE-15B` | 非复述型分镜 | 每条 `时间段` 通过源句复述扣除测试：删除上游原句已有主体、动作、道具和事实后，仍保留机位/构图/运镜路径/速度/停点/焦点/光影结果/方向参照/连续性交接中的有效摄影决策；不得只是把正上方画面句子拆写成画面内容顺序 |
| `GATE-CINE-16` | 摄影语法变化 | 景别、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化服务节拍、空间、信息、情绪或交接；不存在随机换技法、无动机大远景跳大特写或视角乱跳 |
| `GATE-CINE-17` | 思维·执行节点完整 | 产物能回指 `PASS-CINE-00..12`、`PASS-CINE-02S`、`PASS-CINE-02D`、`PASS-CINE-04D` 与 `N1-INTAKE/N2-MATCH/N3-TYPE/N3.5-SEQUENCE-ALIGN/N3.6-DENSITY-CURVE/N4-BEAT/N5-RHYTHM/N5.2-DURATION/N5.5-PEAK-SHOT/N5.6-INIT-SYNTHESIS/N6-CONTINUITY/N6.1-HANDOFF/N6.2-CAMERA-GRAMMAR/N6.4-FUNCTIONAL-PROJECTION/N6.5-SHOT-PLAN/N7-INJECT/N8-REVIEW/N8R-DIRECT-REPAIR/N8R-REVIEW-AGAIN/N9-WRITE` 的关键判断：真源、画面匹配、类型、段落观看意图与逐点归属、段落密度曲线、节拍、节奏、镜头时值、高点、初始化综合、连续性、边界交出、摄影语法、功能投影、AI 视频执行稳定性、计划、注入、审查修复 |
| `GATE-CINE-17A` | reference gate 覆盖 | 本轮加载或产生强制裁决的每个 `references/` 文件均已在下方 `Reference Review Gate Matrix` 中找到审核落点，并在报告中记录相应证据；若某 reference 只是术语、示例或解释性材料，报告需说明它未被单独作为阻断依据 |
| `GATE-CINE-18` | 自然成稿 | 连续分镜不出现重复句法骨架、参数清单腔或“高级/丝滑/电影感”等空泛效果词；读起来先是画面，再是摄影 |
| `GATE-CINE-19` | 输出路径 | 写入 `projects/aigc/<项目名>/4-摄影/第N集.md` 和 `执行报告.md` |
| `GATE-CINE-20` | 初始化综合消费 | 初始化综合存在时，已只读消费 `team.yaml.init_synthesis.stage_seed_summary."4-摄影"`、`init_handoff.cinematography_seed` 或 `north_star.yaml.创作阶段不变量.摄影`，形成 `init_team_synthesis_context`；未调用 team 身份、未解析旧 stage profile、未补造本阶段顾问问答 |
| `GATE-CINE-21` | 边界交出 | 场景变化已处理上一画面交出点和下一画面进入提示；所有声画、形态、颜色、文字或高点余波只作为可见交出锚点记录，没有在本阶段写成组间/跨场景创意转场方案 |
| `GATE-CINE-22` | 场景视觉约束 | 每个场景已在内部形成 `scene_visual_constraint`，覆盖构图布局（主体/陪体/前景/背景）、构图方式（形状感/线条感/影调感/虚实感/节奏感/纹理质感/气势中选取 2-3 个子维度）、光源设置效果、色彩体系和关键摄影技术参数；同一场景视觉约束不变时只裁决一次，变化时可重新裁决；纯内部裁决，逐段时间段在约束框架内展开 |
| `GATE-CINE-23` | 时间段维度覆盖 | 每条 `时间段` 的自然语句覆盖了当前画面中自然存在的扩展维度信息点；维度选取遵循"应有则有、没有不必强制"原则——画面中有角色就写角色表演，有陪体就写陪体动态，没有则跳过，不为凑数虚构画面中不存在的信息；维度信息融入自然中文而非输出标签列表或参数清单；`shot_design_plan` 中有 `dimension_coverage` 字段说明覆盖了哪些维度及为什么 |
| `GATE-CINE-24` | 道具镜头准入 | 道具、反射、倒影、涟漪、餐具/杯子/纸张/桌面等物件细节只有在角色互动、关键信息/规则/证据/危险源或必要环境交代时成为焦点；无互动普通道具未被写成独立特写、焦点拉移终点、反射主体或多分镜衔接节点 |
| `GATE-CINE-25` | 动作-反应焦点 | 多人 beat 已区分 `action_driver/reaction_receiver/ambient_participants`；镜头先服务动作如何影响反应，没有让所有角色同强度表演，也没有为了同时照顾所有人和物件而牺牲轴线、动作链或主体焦点 |
| `GATE-CINE-26` | 场景/镜头身份 | 每条下游可消费分镜能先还原 `scene_identity` 与 `shot_identity`：场景年代/功能/环境声/材质光影明确，摄影机位置朝向明确，人物动作发生在镜头内部，方向参照相对镜头或画面边界 |
| `GATE-CINE-27` | 双人轴线与 180 度规则 | 双人/多人对峙、追逐、动作、逼问或谈判场已锁定两人连线、screen left/right、中间空间锚点和同侧 180 度拍摄半区；每条关键 `时间段` 的下游 payload 重复 `axis_continuity_anchor`；换轴有中性镜头、主观视角、可见运动镜头或角色换位桥接 |
| `GATE-CINE-28` | 镜头叙事功能 | 每条计划时间段有 `shot_narrative_function`，能说明新增信息、关系变化、动作结果、情绪压力、观看发现或交出价值；删除后无损失的分镜已删并或重写 |
| `GATE-CINE-29` | 运镜与景深叙事 | 运镜有情绪语义、速度曲线和停点；景深/焦点承担隐藏、揭示、关系隔离、主观偏差、空间压迫或注意力转移功能；不存在只写技术名的虚假专业性 |
| `GATE-CINE-30` | 光源叙事 | 关键光线能说明照亮/遮蔽对象、阴影/轮廓结果、信息可见性、权力关系、情绪温度或危险预告；来源词不替代叙事功能 |
| `GATE-CINE-31` | 注意力引导 | 每个 visual_unit 有清楚观众入口、遮挡/显影、焦点接力、信息获得点和离场锚点；没有无动机正面平铺、全信息一次性展示或焦点漂移 |
| `GATE-CINE-32` | 对白场景去模板化 | 对白场景有 `dialogue_scene_variation_plan`；焦点选择来自戏剧功能、权力关系、观众知情层级和注意力路径；没有机械正反打、每句说话者特写或说话者/听话者覆盖式配平 |
| `GATE-CINE-33` | 长对白镜头承托 | 上游长对白有 `long_dialogue_visual_plan`；每个长对白节拍能回指 `long_dialogue_beat_map` 和 `long_dialogue_delivery_map`；焦点在说话者、听者、手部/道具、空间压力、群像、画外声源或沉默余波之间变化；没有单段采访式吞完整段长对白 |
| `GATE-CINE-34` | 源画面细节增量融合 | 每个 `visual_unit` 有 `source_visible_fact_map`；上游画面描述中的必须保留可见事实均有保留/压缩/排除理由，并绑定到具体 `[起始秒-结束秒]`、焦点、构图、运镜或光线变化；终稿在保留原事实基础上新增摄影决策，没有把服装/姿态/微表情/手部动作/身体距离/场景文字/光线/道具状态/异常变化摘要成泛化词或摄影术语 |

## Reference Review Gate Matrix

所有 `references/` 细则只要参与强制裁决，就必须能落到本表。执行时不要求每个 reference 独立新增一个 gate，但不得出现“被引用、被要求、被判失败，却没有 PASS/N 节点、review gate、fail code 或报告证据”的悬空规则。

| reference_file | consumed_by_pass_or_node | review_gate | fail_code | report_evidence |
| --- | --- | --- | --- | --- |
| `references/visual-matching-contract.md` | `PASS-CINE-01` / `N2-MATCH` | `GATE-CINE-02`、`GATE-CINE-10`、`GATE-CINE-24` | `FAIL-CINE-02`、`FAIL-CINE-05A`、`FAIL-CINE-05S` | 画面性句子命中清单、心理/思考反应画面化清单、非画面字段排除、道具准入抽样 |
| `references/beat-analysis-contract.md` | `PASS-CINE-03` / `N4-BEAT` / `N6.5-SHOT-PLAN` | `GATE-CINE-04`、`GATE-CINE-04A`、`GATE-CINE-04E`、`GATE-CINE-04A3` | `FAIL-CINE-03`、`FAIL-CINE-03A`、`FAIL-CINE-03F`、`FAIL-CINE-03E` | `beat_map` 抽样、有效触发点清单、`trigger_merge_exception`、单段吞 beat 复核 |
| `references/global-rhythm-terminology-glossary.md` | `PASS-CINE-03` / `PASS-CINE-04` / `N4-BEAT` | `GATE-CINE-04A`、`GATE-CINE-04E`、`GATE-CINE-17A` | `FAIL-CINE-03A`、`FAIL-CINE-03F`、`FAIL-CINE-05REF` | 节拍/节奏/时值术语使用记录，说明其为术语口径而非独立阻断真源 |
| `references/visual-rhythm-analysis-contract.md` | `PASS-CINE-04` / `N5-RHYTHM` | `GATE-CINE-05`、`GATE-CINE-04A`、`GATE-CINE-04E` | `FAIL-CINE-05D`、`FAIL-CINE-03A`、`FAIL-CINE-03F` | 张弛抽样、低信息收敛与关键信息发散证据、2 段/1 段复核 |
| `references/shot-duration-decision-contract.md` | `PASS-CINE-04D` / `N5.2-DURATION` | `GATE-CINE-04B`、`GATE-CINE-04C`、`GATE-CINE-33` | `FAIL-CINE-03B`、`FAIL-CINE-03C`、`FAIL-CINE-05L`、`FAIL-CINE-19D`、`FAIL-LONG-DIALOGUE-CINEMATOGRAPHY` | `duration_profile`、对白台词量预算、长对白跨镜时值分配、长停顿/快速镜抽样、15 秒组内风险 |
| `references/peak-shot-language-contract.md` | `PASS-CINE-05` / `N5.5-PEAK-SHOT` | `GATE-CINE-14`、`GATE-CINE-05`、`GATE-CINE-04B` | `FAIL-CINE-05E`、`FAIL-CINE-19D` | 高点证据、峰值镜头策略、情绪类慢节奏承托和余波交出 |
| `references/visual-sequence-alignment-contract.md` | `PASS-CINE-02S` / `N3.5-SEQUENCE-ALIGN` | `GATE-CINE-04D`、`GATE-CINE-15D` | `FAIL-CINE-05M`、`FAIL-CINE-05AB` | `sequence_profile`、`unit_ownership_map`、`forbidden_bleed`、`field_link_chain`、跨块外溢抽样 |
| `references/sequence-density-curve-contract.md` | `PASS-CINE-02D` / `N3.6-DENSITY-CURVE` | `GATE-CINE-04A2`、`GATE-CINE-04A3`、`GATE-CINE-05` | `FAIL-CINE-03D`、`FAIL-CINE-03E` | `density_curve_summary`、`density_ramp`、峰值/恢复槽位、set-piece 不可删证明 |
| `references/shot-continuity-contract.md` | `PASS-CINE-07` / `N6-CONTINUITY` / `N6.5-SHOT-PLAN` | `GATE-CINE-06`、`GATE-CINE-06A`、`GATE-CINE-11`、`GATE-CINE-15D`、`GATE-CINE-25`、`GATE-CINE-27` | `FAIL-CINE-05C`、`FAIL-CINE-05AB`、`FAIL-CINE-05T`、`FAIL-CINE-05U`、`FAIL-CINE-05V`、`FAIL-CINE-19A` | 前 3 个画面回看、entry/action_anchor/exit/handoff、`format_continuity_surface`、轴线与动作锚点继承抽样 |
| `references/intra-shot-transition-contract.md` | `PASS-CINE-10` / `N6.5-SHOT-PLAN` / `N7-INJECT` | `GATE-CINE-15D`、`GATE-CINE-08` | `FAIL-CINE-05AB` | 块内相邻时间段物理因果链、过渡锚点和时值接力抽样 |
| `references/transition-design-contract.md` | `PASS-CINE-07T` / `N6.1-HANDOFF` | `GATE-CINE-21`、`GATE-CINE-04D` | `FAIL-CINE-05K`、`FAIL-CINE-05M` | 场景变化交出点/进入提示、未越权写入组间转场方案 |
| `references/cinematic-technique-library.md` | `PASS-CINE-08` / `N6.2-CAMERA-GRAMMAR` | `GATE-CINE-07`、`GATE-CINE-16`、`GATE-CINE-22` | `FAIL-CINE-05`、`FAIL-CINE-05I`、`FAIL-CINE-05P` | 景别/视角/镜头类型/构图/摄影技术选择抽样及动机 |
| `references/dynamic-lens-language-contract.md` | `PASS-CINE-08` / `PASS-CINE-11` / `N6.2-CAMERA-GRAMMAR` / `N7-INJECT` | `GATE-CINE-08`、`GATE-CINE-16`、`GATE-CINE-18` | `FAIL-CINE-05B`、`FAIL-CINE-05G`、`FAIL-SHOT-IDENTITY-02` | 动态路径、速度曲线、停点、自然成稿和正面平视动机抽样 |
| `references/camera-movement-emotion-contract.md` | `PASS-CINE-08` / `PASS-CINE-10` / `N6.2-CAMERA-GRAMMAR` | `GATE-CINE-29`、`GATE-CINE-16` | `FAIL-CINE-05X` | `camera_movement_emotion_plan` 是否说明情绪语义、速度曲线和停点 |
| `references/depth-of-field-narrative-contract.md` | `PASS-CINE-08` / `PASS-CINE-10` / `N6.2-CAMERA-GRAMMAR` | `GATE-CINE-29`、`GATE-CINE-16` | `FAIL-CINE-05X` | `depth_of_field_narrative_plan` 是否说明隐藏、揭示、隔离或注意力转移 |
| `references/scene-visual-constraint-contract.md` | `PASS-CINE-08` / `PASS-CINE-09` / `N6.3-SCENE-VISUAL-CONSTRAINT` | `GATE-CINE-22`、`GATE-CINE-26`、`GATE-CINE-30` | `FAIL-CINE-05P`、`FAIL-SCENE-IDENTITY-01`、`FAIL-CINE-05Y` | `scene_visual_constraint`、构图布局/光源/色彩/摄影技术参数内部裁决 |
| `references/light-as-narrative-contract.md` | `PASS-CINE-08` / `PASS-CINE-10` / `N6.3-SCENE-VISUAL-CONSTRAINT` | `GATE-CINE-30`、`GATE-CINE-22` | `FAIL-CINE-05Y` | `light_narrative_plan`、照亮/遮蔽对象、阴影轮廓和信息可见性抽样 |
| `references/functional-cinematic-projection-contract.md` | `PASS-CINE-09` / `PASS-CINE-10` / `N6.4-FUNCTIONAL-PROJECTION` / `N6.5-SHOT-PLAN` | `GATE-CINE-15`、`GATE-CINE-15B`、`GATE-CINE-15C`、`GATE-CINE-23`、`GATE-CINE-24`、`GATE-CINE-28` | `FAIL-CINE-05H`、`FAIL-CINE-05AA`、`FAIL-CINE-05R`、`FAIL-CINE-05Q`、`FAIL-CINE-05S`、`FAIL-CINE-05W` | 功能性 payload、梯度完整性、源句复述扣除、维度覆盖、道具准入和镜头叙事功能抽样 |
| `references/source-detail-incremental-fusion-contract.md` | `PASS-CINE-09` / `PASS-CINE-10` / `PASS-CINE-11` / `N6.4-FUNCTIONAL-PROJECTION` / `N6.5-SHOT-PLAN` / `N7-INJECT` | `GATE-CINE-34`、`GATE-CINE-15B`、`GATE-CINE-18`、`GATE-CINE-04B` | `FAIL-CINE-05AC`、`FAIL-CINE-05R`、`FAIL-CINE-05G`、`FAIL-CINE-03B` | `source_visible_fact_map`、`fact_to_segment_binding`、源事实保留测试、精准卡点抽样和有机融合重写样本 |
| `references/shot-as-narrative-contract.md` | `PASS-CINE-09` / `PASS-CINE-10` / `N6.4-FUNCTIONAL-PROJECTION` | `GATE-CINE-28`、`GATE-CINE-15`、`GATE-CINE-31` | `FAIL-CINE-05W`、`FAIL-CINE-05Z` | `shot_narrative_function` 覆盖、删除无损镜头删并情况 |
| `references/attention-guidance-contract.md` | `PASS-CINE-09` / `PASS-CINE-10` / `N6.4-FUNCTIONAL-PROJECTION` | `GATE-CINE-31`、`GATE-CINE-32`、`GATE-CINE-33`、`GATE-CINE-15` | `FAIL-CINE-05Z`、`FAIL-DIALOGUE-CINEMATOGRAPHY-TEMPLATE`、`FAIL-LONG-DIALOGUE-CINEMATOGRAPHY` | 观众入口、遮挡/显影、焦点接力、对白场景焦点变化和长对白视觉承托抽样 |
| `references/ai-video-prompt-execution-contract.md` | `PASS-CINE-09` / `PASS-CINE-10` / `N6.4-FUNCTIONAL-PROJECTION` / `N6.5-SHOT-PLAN` | `GATE-CINE-15A`、`GATE-CINE-26`、`GATE-CINE-27` | `FAIL-CINE-05N`、`FAIL-SHOT-IDENTITY-01`、`FAIL-SHOT-IDENTITY-02`、`FAIL-DIRECTION-REF-01`、`FAIL-CINE-19B`、`FAIL-CINE-19C`、`FAIL-CINE-19D` | 镜头先行、方向参照、光线结果、表演微动态、眼部特写和心理变化慢节奏抽样 |
| `references/natural-shot-detail-writing-contract.md` | `PASS-CINE-11` / `N7-INJECT` | `GATE-CINE-18`、`GATE-CINE-10`、`GATE-CINE-15B` | `FAIL-CINE-05G`、`FAIL-CINE-05R`、`FAIL-CINE-19C` | 自然中文、模板腔/参数清单、源句复述扣除和抽象情绪词转译抽样 |
| `references/shot-planning-integration-contract.md` | `PASS-CINE-10` / `N6.5-SHOT-PLAN` | `GATE-CINE-09`、`GATE-CINE-17`、`GATE-CINE-17A`、`GATE-CINE-04E` | `FAIL-CINE-05F`、`FAIL-CINE-03F`、`FAIL-CINE-05REF` | `shot_design_plan` 汇流、`shot_count_decision`、reference 覆盖证据和合并例外证明 |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-CINE-02` | 漏掉画面性句子 | `references/visual-matching-contract.md` |
| `FAIL-CINE-03` | 时间段过粗、过碎或固定模板化 | `references/beat-analysis-contract.md` |
| `FAIL-CINE-03A` | 时间段数量塌缩为固定 2 段或同数分布异常，且抽样无法证明 `第二段` 有有效触发点、观看结果或平台节奏价值 | `references/global-rhythm-terminology-glossary.md`、`references/beat-analysis-contract.md`、`references/visual-rhythm-analysis-contract.md`、`references/sequence-density-curve-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N3.6-DENSITY-CURVE`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-03F` | 单个 `第一段` 吞入多个有效触发点：源句或分镜文本内部出现主体/空间/动作相位/声画/信息/情绪/注意力对象连续转移，但没有拆成多个 `时间段`，也没有 `trigger_merge_exception` 证明同段完成不损失观看结果、平台节奏、下游 payload 或人物动作连续性 | `references/beat-analysis-contract.md`、`references/global-rhythm-terminology-glossary.md`、`references/visual-rhythm-analysis-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N4-BEAT`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-03D` | 整场或连续段落缺少密度曲线：全满、全空、平均同密度、峰值后无恢复/反压，或只统计 `shot_count_distribution` 但没有 `density_curve_summary` | `references/sequence-density-curve-contract.md`、`references/visual-rhythm-analysis-contract.md`、`steps/cinematography-workflow.md#N3.6-DENSITY-CURVE`、`steps/cinematography-workflow.md#N5-RHYTHM` |
| `FAIL-CINE-03E` | 5-6 段 set-piece 链条没有真实连续动作/声音结果，或每段不能证明独立起点、撞点、结果、声音打点、反应落点 | `references/sequence-density-curve-contract.md#set-piece-chain-exception`、`references/beat-analysis-contract.md#Shot-Count-Cardinality-Guard`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-03B` | 时间段数量正确但单段长短错误：缺少 `[起始秒-结束秒]`、文字/道具/微表情被快速切走，低信息时间段被拖长，普通氛围段普遍超过 `standard`，连续同长同速，或 15 秒组内节奏风险未裁决 | `references/shot-duration-decision-contract.md`、`references/visual-rhythm-analysis-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N5.2-DURATION` |
| `FAIL-CINE-03C` | 对白/旁白画面未按台词量裁决时长，导致台词未说完就切走、反应镜头承托不足或短对白被无意义拖长 | `references/shot-duration-decision-contract.md#Dialogue Duration Rule`、`steps/cinematography-workflow.md#N5.2-DURATION` |
| `FAIL-CINE-05M` | 段落级连续运镜吞掉逐画面点归属：分镜整体流畅但无法回指正上方画面句子，或提前写入后文主体动作、对白反应、记忆段、道具揭示、跨场景连接方案 | `references/visual-sequence-alignment-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N3.5-SEQUENCE-ALIGN`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-04` | 原字段标题下时间段缺失或时间段断裂 | `templates/output-template.md`、`scripts/validate_cinematography_markup.py` |
| `FAIL-CINE-05` | 原字段标题下时间段空泛 | `references/cinematic-technique-library.md` |
| `FAIL-CINE-05A` | 原字段标题下时间段混入抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 | `SKILL.md` Output Contract、`templates/output-template.md` |
| `FAIL-CINE-05B` | 原字段标题下时间段静态呆板，没有变化和组合运镜 | `references/dynamic-lens-language-contract.md` |
| `FAIL-CINE-05L` | 原字段标题下时间段无法反推时值等级、停顿/压缩理由或相邻镜头时值接力 | `references/shot-duration-decision-contract.md`、`references/dynamic-lens-language-contract.md`、`steps/cinematography-workflow.md#N5.2-DURATION` |
| `FAIL-CINE-05C` | 当前原字段标题下时间段与临近镜头断裂、跳轴、跳色或空间跳跃 | `references/shot-continuity-contract.md` |
| `FAIL-CINE-05D` | 原字段标题下时间段不分轻重，低信息过度发散或重信息过度收敛 | `references/visual-rhythm-analysis-contract.md` |
| `FAIL-CINE-05E` | 上游高点被按普通画面压平，或高潮强化缺少分镜/运镜/停顿/余波策略 | `references/peak-shot-language-contract.md` |
| `FAIL-CINE-05F` | references 被引用但未汇流成 `shot_design_plan`，导致时间段数量随机、上下不接或输出过短 | `references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05REF` | 强制性 `references/` 细则被加载、引用或用于阻断判断，但没有对应 PASS/N 节点、`GATE-CINE-*`、`FAIL-CINE-*` 或执行报告证据；解释性 glossary / example guard 被误当作独立强制裁决真源 | 本文件 `Reference Review Gate Matrix`、`SKILL.md#Reference Loading Guide`、`steps/cinematography-workflow.md#N8-REVIEW` |
| `FAIL-CINE-05G` | 原字段标题下时间段出现参数清单、连续同构句、模板填空腔或过度显式化内部计划 | `references/natural-shot-detail-writing-contract.md`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05H` | 原字段标题下时间段表达顺滑但缺少影视功能、运镜策略、主体/动作/构图/光色/空间锚点或下游 AIGC 可消费 payload | `references/functional-cinematic-projection-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05AA` | 梯度描述完整性失败：L0/L1/L2/L3 裁决与画面任务不匹配，低信息镜被堆砌，高信息镜被写薄，或当前梯度必需的起点、路径/静止理由、落点、时值、交接、表演/信息承托、下游稳定性缺失；常见表现是只写“慢推/压迫感/电影感”或机械填满 15 项 | `references/functional-cinematic-projection-contract.md#Gradient-Shot-Detail-Sufficiency`、`templates/output-template.md#Visual-Unit-Injection`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05AB` | 镜内或镜间连贯性不足：`entry/action_anchor/exit/handoff` 不可抽取，相邻时间段缺少物理因果链或过渡锚点，相邻画面块之间人物姿态、轴线、运动方向、光色或声音余波凭空重启，或当前原字段标题 + 连续时间段格式没有在正文中呈现字段内 `segment_link` 与字段间 `field_link_chain` | `references/shot-continuity-contract.md#Intra-And-Inter-Shot-Continuity-Gate`、`references/intra-shot-transition-contract.md`、`steps/cinematography-workflow.md#N6-CONTINUITY`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05R` | 时间段是画面内容拆写/复述：去掉源句已有主体、动作、道具和事实后，只剩景别词、空泛效果词或顺序词，无法读出独立摄影决策 | `references/functional-cinematic-projection-contract.md#Content-Paraphrase-Is-Not-Shot-Detail`、`references/natural-shot-detail-writing-contract.md#Paraphrase-Repair-Examples`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05AC` | 源画面细节增量融合失败：上游画面描述中的必须保留可见事实被摘要、删短、泛化或摄影术语替代；缺少 `source_visible_fact_map` 或 `fact_to_segment_binding`；时间段秒点存在但无法说明原动作起点、撞点、读秒、结果或交出点如何被保留 | `references/source-detail-incremental-fusion-contract.md`、`references/functional-cinematic-projection-contract.md`、`references/natural-shot-detail-writing-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05N` | 原字段标题下时间段不适合稳定改写为 AI 视频提示词：动作和镜头割裂、方向参照含混、光线只写光源或空泛效果、情绪没有可见微动态，或把完整提示词分栏/命令式负向词写进正文 | `references/ai-video-prompt-execution-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05I` | 景别、镜头视角、景深/焦点、镜头类型或构图变化随机，无法回指节拍、空间、信息、情绪或连续性交接 | `references/cinematic-technique-library.md`、`steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` |
| `FAIL-CINE-05K` | 场景变化没有交出点/进入提示，或把组间/跨场景创意转场方案落在 `4-摄影` | `references/transition-design-contract.md`、`references/shot-continuity-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05J` | 思维·执行节点缺环：未完成画面匹配、类型画像、段落观看意图与逐点归属、摄影语法、功能投影、计划汇流或阶段内修复闭环，却直接写出原字段标题下时间段 | `steps/cinematography-workflow.md`、`SKILL.md#Thought Pass Map` |
| `FAIL-CINE-06` | 改写原编导稿 | `SKILL.md` Output Contract 和本文件 `faithfulness_review` |
| `FAIL-CINE-05P` | 场景视觉约束缺失或未被消费：场景未形成内部 `scene_visual_constraint`，或构图布局/构图方式/光源/色彩/摄影技术参数未作为内部约束被下游时间段消费 | `references/scene-visual-constraint-contract.md`、`references/cinematic-technique-library.md`、`steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05Q` | 时间段维度覆盖问题：画面中存在角色表演/陪体动态/前景动态/光影反射/动态焦点/节奏同步等信息却未被摄影机表达，或维度以标签形式输出而非融入自然中文，或为凑数虚构画面中不存在的信息 | `references/functional-cinematic-projection-contract.md#Gradient-Shot-Detail-Sufficiency`、`references/functional-cinematic-projection-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05S` | 无互动普通道具被硬写成焦点、倒影、涟漪、餐具轻响、纸角阴影或独立特写；删掉该物件镜头不损失剧情/表演/空间信息，反而能恢复人物动作衔接 | `references/visual-matching-contract.md#Prop-Admission-Overlay`、`references/functional-cinematic-projection-contract.md#Gradient-Shot-Detail-Sufficiency`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05T` | 分镜为了物件、环境反应、反射或静物切点牺牲人物动作链；人物姿态、方向、可达对象或退出状态不清，删掉该细节后动作更顺 | `../../_shared/action-first-continuity-contract.md`、`references/shot-continuity-contract.md`、`steps/cinematography-workflow.md#N6-CONTINUITY`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05U` | 多人 beat 的镜头没有行动-反应焦点：所有角色同等强度表演，或为同时照顾多人/物件选择奇怪角度，导致动作因果、视线关系和主体焦点混乱 | `../../_shared/lived-in-character-behavior-contract.md`、`references/shot-continuity-contract.md#Action-Reaction-Focus`、`steps/cinematography-workflow.md#N6-CONTINUITY`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05V` | 双人/多人对峙、追逐、动作或谈判场缺少轴线锁：主角/对手 screen left/right 反复、摄影机直接越过 180 度轴线、后续分镜没有重复空间锚点，或换轴缺少中性/主观/运动桥接 | `references/shot-continuity-contract.md#Two-Person-Axis-And-180-Degree-Rule`、`references/ai-video-prompt-execution-contract.md#Repeated-Spatial-Anchor-For-AIGC`、`steps/cinematography-workflow.md#N6-CONTINUITY`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05W` | 分镜只记录动作或画面事实，无法说明镜头带来的叙事功能、观看发现、关系变化、动作结果或交出价值 | `references/shot-as-narrative-contract.md`、`references/functional-cinematic-projection-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05X` | 运镜只有推拉摇移跟等技术名，或景深只有虚实效果，没有情绪语义、速度停点、主观距离、信息隐藏/揭示、关系隔离或注意力转移 | `references/camera-movement-emotion-contract.md`、`references/depth-of-field-narrative-contract.md`、`steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` |
| `FAIL-CINE-05Y` | 光线只写来源或氛围词，无法说明照亮/遮蔽对象、阴影/轮廓结果、信息可见性、权力关系、情绪温度或危险预告 | `references/light-as-narrative-contract.md`、`references/scene-visual-constraint-contract.md`、`steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` |
| `FAIL-CINE-05Z` | 注意力引导缺失：镜头正面平铺全信息、焦点漂移、没有进入点/遮挡/显影/焦点接力/离场锚点 | `references/attention-guidance-contract.md`、`references/shot-as-narrative-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-DIALOGUE-CINEMATOGRAPHY-TEMPLATE` | 对白场景模板化：连续正反打、每句都给说话者特写、说话者/听话者覆盖式配平，或无法说明焦点选择与权力关系、观众知情层级、潜台词和注意力路径的关系 | `references/attention-guidance-contract.md`、`knowledge-base/电影镜头/一流对话场景.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-LONG-DIALOGUE-CINEMATOGRAPHY` | 长对白镜头承托失败：单段采访式吞完整段长对白，或多个节拍都拍同一说话者同一景别，缺少听者反应、空间压力、手部/道具、群像、画外声源、沉默余波和跨镜时值分配 | `references/shot-duration-decision-contract.md#Long-Dialogue-Visual-Budget`、`references/attention-guidance-contract.md#Long-Dialogue-Attention-Flow`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-SCENE-IDENTITY-01` | 分镜只写人物动作或抽象氛围，无法看出年代、空间功能、环境声底色、材质光影和场景身份 | `../../_shared/scene-shot-identity-contract.md`、`references/scene-visual-constraint-contract.md`、`steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` |
| `FAIL-SHOT-IDENTITY-01` | 动作先发生，镜头只在后面补推进/跟拍/特写，无法稳定生成连续视频 | `../../_shared/scene-shot-identity-contract.md`、`references/ai-video-prompt-execution-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` |
| `FAIL-SHOT-IDENTITY-02` | 镜头无动机保持正面平视、完整清楚展示，导致画面扁平、旁观、摆拍或资料图感 | `../../_shared/scene-shot-identity-contract.md`、`references/ai-video-prompt-execution-contract.md#Camera-Perspective-And-Discovery-Rule`、`references/dynamic-lens-language-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-DIRECTION-REF-01` | 前后左右、入画退场或光线方向没有相对镜头/画面参照 | `../../_shared/scene-shot-identity-contract.md`、`references/ai-video-prompt-execution-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-19A` | 跨原字段时间段组或跨时间段切换时动作锚点断裂，人物姿态、位置或身体接触状态在下一段凭空变化 | `references/shot-continuity-contract.md#Action-Anchor-Inheritance`、`steps/cinematography-workflow.md#N6-CONTINUITY`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-19B` | 眼睛特写没有限定正面双眼/正面上半脸，容易生成单眼侧面或畸形五官 | `references/ai-video-prompt-execution-contract.md#Eye-Close-up-Rule`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-19C` | 抽象情绪词直接进入原字段标题下时间段，未转译为面部肌肉、呼吸、手部、身体姿态或视线变化 | `references/ai-video-prompt-execution-contract.md#Performance-Microdynamic-Rule`、`references/natural-shot-detail-writing-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-19D` | 人物情绪剧烈变化时节奏过快，缺少慢镜头、正面近景/特写或多角度正面切换承托 | `references/ai-video-prompt-execution-contract.md#Psychological-Intensity-Slowdown-Rule`、`references/shot-duration-decision-contract.md`、`steps/cinematography-workflow.md#N5.2-DURATION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-07` | 初始化综合存在但缺少 `init_team_synthesis_context`，或创作阶段误调用 team 身份、解析旧 stage profile、补造本阶段顾问问答 | `../../_shared/team-advisor-consultation-contract.md` + `../SKILL.md#Init Team Synthesis Consumption` |

## Review Output

执行报告至少记录：

- 输入文件与输出文件。
- 处理集号。
- 画面性句子数量。
- 原画面性字段时间段组数量。
- 机械校验结果与质量 review 结果；机械校验只证明结构有效，不替代本文件的 `GATE-CINE-*` 质量门禁。
- 画面节奏张弛结果。
- 镜头时值裁决结果：duration profile、时间范围抽样、长停顿/快速镜抽样、15 秒组内节奏风险。
- 对白台词量预算结果：对白/旁白承托画面数量、台词量下限抽样、跨镜延续说明。
- 时间段数量分布与 2 段集中抽样复核结果。
- 1 段吞多 beat 复核结果：1 段块数量、全量或抽样范围、发现的多触发点压平块、`trigger_merge_exception` 证明或拆镜修复记录。
- 段落密度曲线结果：`density_curve_summary`、`tempo_beats`、`density_ramp`、`peak_slots`、`recovery_slots`、`set_piece_chain_slots`、`sound_cut_pattern` 和 `density_budget`。
- 段落观看意图与逐画面点归属检查结果：是否形成 `sequence_profile`、是否有 `unit_ownership_map`、是否未发生跨块外溢或失主镜头。
- 高潮分镜强化结果。
- `shot_design_plan` 汇流与投影检查结果。
- 源画面细节增量融合检查结果：`source_visible_fact_map` 抽样、必须保留事实数量、压缩/排除理由、`fact_to_segment_binding`、因 `FAIL-CINE-05AC` 修复的字段标签。
- reference gate 覆盖检查结果：本轮加载的 `references/` 文件清单、对应 `PASS/N` 节点、`GATE-CINE-*`、`FAIL-CINE-*`、报告证据项；解释性 reference 未被单独作为阻断依据的说明。
- 边界交出检查结果：场景变化交出点/进入提示、可见交出锚点，以及是否未在本阶段落盘创意转场方案。
- 摄影语法变化检查结果：景别梯度、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化。
- 功能性影视投影与 AIGC 下游可消费性检查结果。
- 梯度描述完整性检查结果：抽样说明 `时间段` 的 L0/L1/L2/L3 裁决是否匹配画面任务、信息重要性、动作复杂度、情绪强度、段落位置和下游风险；说明低信息镜是否克制、高信息镜是否足够、是否存在堆砌分镜，因 `FAIL-CINE-05AA` 修复的字段标签。
- 镜内/镜间连贯性检查结果：`entry/action_anchor/exit/handoff` 是否可抽取，块内相邻时间段是否有物理因果链或过渡锚点，块间人物姿态、轴线、运动方向、光色或声音余波是否连续，当前输出格式是否形成 `format_continuity_surface / field_link_chain`，因 `FAIL-CINE-05AB` 修复的字段标签。
- 源句复述扣除测试结果：抽样说明候选时间段是否脱离“画面内容拆写/复述”，以及因 `FAIL-CINE-05R` 修复的行号或字段标签。
- AI 视频执行稳定性检查结果：镜头先行、方向参照、光线结果、表演微动态、提示词模板腔和命令式负向词风险。
- 观众发现路径检查结果：正面平视使用理由、低角度/前景/透视/手持/慢拉等观看选择是否有证据，因 `FAIL-SHOT-IDENTITY-02` 修复的行号或字段标签。
- 场景/镜头身份检查结果：场景年代/功能/环境声/材质光影、摄影机位置朝向、动作是否发生在镜头内部、方向参照是否相对镜头或画面边界。
- 双人轴线与 180 度规则检查结果：涉及对峙、追逐、动作、逼问或谈判的分镜是否锁定 line of action、screen left/right、中间空间锚点和同侧 180 度半区；是否逐段重复 `axis_continuity_anchor`；因 `FAIL-CINE-05V` 修复的行号或字段标签。
- 人物动作链优先检查结果：涉及人物的分镜是否承接姿态、位置、朝向、身体接触、动作方向和注意力落点；对象是否空间可达；因 `FAIL-CINE-05T` 删除或降级的物件/环境切点。
- 动作-反应焦点检查结果：多人 beat 是否明确行动者、反应者和背景参与者；因 `FAIL-CINE-05U` 收敛或改写的多人同强度表演、奇怪角度或抢焦物件。
- 初始化综合消费结果：synthesis 来源、采纳约束、可执行指导、风险提示、被拒/延后点，以及未触发 team 身份调用、旧 stage profile 或本阶段伪顾问问答的证据。
- 镜头连续性、空间一致性和风格一致性结果。
- 运镜摄影设计纯度检查结果。
- 场景视觉约束内部裁决结果：每个场景是否已形成 `scene_visual_constraint`、构图布局/构图方式/光源/色彩/摄影技术参数覆盖情况、逐段时间段是否在约束框架内展开。
- 时间段维度覆盖检查结果：每条时间段覆盖的维度及来源（画面中确实存在的信息）、维度信息自然化程度、是否存在虚构维度或遗漏已存在维度。
- 镜头叙事功能检查结果：`shot_narrative_function` 覆盖情况、删除无损镜头删并情况、因 `FAIL-CINE-05W` 修复的字段标签。
- 运镜与景深叙事检查结果：`camera_movement_emotion_plan` 与 `depth_of_field_narrative_plan` 是否进入 `shot_design_plan`，因 `FAIL-CINE-05X` 修复的技术名空转。
- 光源叙事检查结果：`light_narrative_plan` 是否说明照亮/遮蔽对象、阴影轮廓、信息可见性或关系功能，因 `FAIL-CINE-05Y` 修复的来源词空转。
- 注意力引导检查结果：`attention_guidance_plan` 的入口、遮挡/显影、焦点接力和离场锚点，因 `FAIL-CINE-05Z` 修复的全信息平铺或焦点漂移。
- 对白场景去模板化检查结果：`dialogue_scene_variation_plan` 是否说明焦点选择与戏剧功能、权力关系、观众知情层级和注意力路径的关系，因 `FAIL-DIALOGUE-CINEMATOGRAPHY-TEMPLATE` 修复的字段标签。
- 长对白镜头承托检查结果：`long_dialogue_visual_plan` 是否逐 beat 回指 `long_dialogue_beat_map` / `long_dialogue_delivery_map`，焦点、反应链、时值和连续性如何分配，因 `FAIL-LONG-DIALOGUE-CINEMATOGRAPHY` 修复的字段标签。
- 道具镜头准入检查结果：涉及物件焦点、反射、倒影、涟漪或独立特写的分镜是否有互动、关键信息、规则/证据/危险源或必要环境理由；因 `FAIL-CINE-05S` 删除或降级的行号/字段标签。
- 自然成稿检查结果。
- 需要返工的行号或字段标签。
- repair actions、复审 verdict、未修复风险和是否允许进入下游阶段。
