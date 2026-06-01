# CHANGELOG

## 2026-06-01 (Format-Aware Continuity Strengthening)

- 将当前“原画面性字段标题 + 连续 `[起始秒-结束秒]` 时间段”明确为连续性承载面：字段标题保障逐画面点归属，字段内时间段保障镜内首尾，字段间末段/首段保障镜间交接。
- 新增 `format_continuity_surface`、`field_link_chain`、`segment_link / sequence_link` 等内部证据口径，要求正文能读出上一落点、当前入口、当前落点和下一可消费入口，而不只是报告里存在连续性计划。
- 同步更新 `SKILL.md`、`shot-continuity-contract.md`、`intra-shot-transition-contract.md`、`visual-sequence-alignment-contract.md`、workflow、review、模板和经验层；连续性不足仍回 `GATE-CINE-15D / FAIL-CINE-05AB`，跨块外溢仍回 `GATE-CINE-04D / FAIL-CINE-05M`。

## 2026-06-01 (Original Visual Field Title Carrier)

- 将 `4-摄影` canonical 输出从独立 `分镜画面：` 字段调整为“原画面性字段标题承载时间段”：保留 `动作画面/对白画面/环境描写/角色动作/心理反应/道具特写/转场` 等原字段标题，字段正文直接展开为连续 `[起始秒-结束秒]` 分镜时间段。
- 明确不采用“原字段正文 + 紧跟分镜块”的双正文结构；画面事实、心理/思考反应外化和摄影运镜语言必须在同一组时间段中融合。
- 同步更新入口合同、模板、workflow、review、references、经验层、脚本说明和 validator；独立 `分镜画面：` 现在只作为旧稿识别或禁止项存在。

## 2026-06-01 (Remove AIGC Reset As Beat Trigger)

- 从 `4-摄影` 的节拍触发矩阵中移除 `BT-16 / AIGC 执行重置点`；AIGC 视频执行稳定性不再作为增加 `分镜画面：` 时间段数量的独立理由。
- 将时间段数量依据收束为 `BT-01~BT-15` 的有效观看触发点、观看结果、平台节奏和叙事节奏价值；AIGC 视频执行稳定性保留为后续功能投影、提示词可执行性和 review 质量门。
- 同步更新 `SKILL.md`、beat/rhythm/sequence/shot-planning references、workflow、review、模板和经验层中的第二段/多段成立口径。

## 2026-06-01 (Legacy Format Reference Removal)

- 从生成侧入口、README 与模板中移除旧附着式格式样例，避免正常输出合同继续暴露历史语法。
- 保留脚本校验和 repair 触发中的 legacy 识别能力，仅用于历史稿迁移、阻断和最小修复，不作为可选输出格式。

## 2026-06-01 (Segment Switch And Duration Rule Alignment)

- 复核并同步原“分镜切换 / 分镜时长”规则，使节拍合同、计划汇流、时值裁决、连续性审查和模板统一落到 `分镜画面：` + `[起始秒-结束秒]` 时间段格式。
- 将旧规则中容易暗示 `分镜N（约X秒）` 的“分镜数量 / 第二镜 / 单镜 / 约秒数”表达，改为“时间段数量 / 第二段 / 单段 / time_range”，保留“镜头”作为摄影语言概念而非落盘列表格式。
- 同步 `references/beat-analysis-contract.md`、`shot-duration-decision-contract.md`、`shot-planning-integration-contract.md`、`intra-shot-transition-contract.md`、`review/review-contract.md`、workflow 与经验层，确保最新输出模板和审核门槛一致。

## 2026-06-01 (Integrated Storyboard Image Format)

- 将 `4-摄影` canonical 输出从旧 `分镜明细：分镜N（约X秒）:` 附着式列表，升级为 `分镜画面：` 下的连续 `[起始秒-结束秒]` 时间段。
- 明确原 `动作画面 / 对白画面 / 环境描写 / 角色动作 / 道具特写` 等画面性字段不再原样保留，而是语义保真融合进自然流畅的画面描述与镜头语言。
- 同步更新入口合同、workflow、review gate、reference 合同、type map、模板、README、脚本校验与产品侧默认提示；validator 现在阻断旧 `分镜明细` 与 `分镜N（约X秒）` 格式，并校验时间段连续性。

## 2026-06-01 (Init-Only Team Synthesis)

- 将摄影阶段 team 上下文调整为只读 `team.yaml.init_synthesis.stage_seed_summary."4-摄影"`、`init_handoff.cinematography_seed` 与 `north_star.yaml.创作阶段不变量.摄影`。
- 旧 stage profile 只作为迁移证据，不再作为 roster、members_ref 或 dispatch 来源；`init_team_synthesis_context` 只承载镜头指导、节奏取舍、审美取舍和风险提示。
- 同步 review、workflow、模板和审计脚本 marker。

## 2026-05-31 (Motion Source Handoff)

- 将默认上游输入调整为 `projects/aigc/<项目名>/3-运动/第N集.md`，用户明确跳过运动强化时才 fallback `2-编导/第N集.md`。
- 同步入口合同、模板、review、workflow、脚本读取逻辑和产品侧默认提示，使摄影分镜建立在运动强化后的角色动作连续性之上。

## 2026-05-27 (Long Dialogue Visual Plan)

- 新增长对白镜头承托规则：`4-摄影` 消费 `long_dialogue_beat_map` 与 `long_dialogue_delivery_map`，形成 `long_dialogue_visual_plan`，逐 beat 分配说话者、听者、手部/道具、空间压力、群像、画外声源或沉默余波等焦点。
- 新增 `FIELD-CINE-35`、`GATE-CINE-33` 与 `FAIL-LONG-DIALOGUE-CINEMATOGRAPHY`，阻断单镜采访式吞完整段长对白、多个节拍同一说话者同一景别、缺少反应链或跨镜时值分配的问题。
- 同步更新时值合同、注意力引导合同、workflow、review、模板和经验层，使长对白从编剧节拍、表演交付到摄影承托形成连续证据链。

## 2026-05-26 (Review Conflict Repair)

- 修复综合审查报告指出的时值门槛冲突：`约3秒` 以上的短剧·AIGC 证据门槛限定为非 `slow_burn/hold` 镜头；情绪类 `slow_burn/hold` 允许进入 held/long_hold，但必须由可见微动态、静止压力、极慢运动或框内变化支撑。
- 将情绪类高点在主入口显式接入 `peak-shot-language-contract.md#emotional_slow_burn`，避免崩溃、震惊、醒悟、强忍等情感高点落入动作/武侠式峰值节奏。
- 清理当前执行路径里的失效引用：将已整合的 `shot-detail-dimension-contract.md` 和 `unified-shot-design-workflow.md` 引用回接到 `functional-cinematic-projection-contract.md#Gradient-Shot-Detail-Sufficiency` 与 `shot-planning-integration-contract.md`。
- 新增 reference 示例护栏：所有涉及示例、正例、反例、表格样句和 `✅/❌` 的 references 均声明“仅说明判断逻辑，不是输出模板”，并在经验层新增“示例污染输出”修复项。

## 2026-05-26 (Gradient Shot Detail Completeness & Continuity Gate)

- 新增梯度描述完整性门槛：每条 `分镜N（约X秒）` 必须先按 `L0-basic / L1-standard / L2-emphasis / L3-peak` 裁决完整度；归属、功能、起点、主体、动作相位、路径、锚点、摄影语法、光线结果、时值理由、微动态、落点/交接、方向参照、道具准入和非复述等 15 项作为维度池按需启用，而非逐镜硬填。
- 明确质量优先原则：分镜明细规则用于保证观看结果、动作相位、信息揭示、情绪压力、空间关系、时值必要性和下游执行稳定性，不得为了完整性或连贯性堆砌分镜、强行加镜，或把低信息画面升级成峰值镜。
- 强化镜内/镜间连贯性：每条分镜必须能抽出 `entry/action_anchor/exit/handoff`；分镜块内相邻镜头需有物理因果链或过渡锚点，分镜块间需继承人物姿态、轴线、运动方向、光色或声音余波。
- 同步更新 `functional-cinematic-projection-contract.md`、`shot-continuity-contract.md`、`shot-planning-integration-contract.md`、`steps/cinematography-workflow.md`、`SKILL.md`、`templates/` 与 `review/review-contract.md`，新增 `FIELD-CINE-33/34`、`GATE-CINE-15C/15D`、`FAIL-CINE-05AA/05AB`，把分镜明细描述完整性和连贯性升级为写回前阻断门。

## 2026-05-26 (Fast-Platform Trigger-First Beat Model)

- 明确快节奏短视频平台的节拍定义：`节拍` 等价于有效分镜触发点，`BT-01~BT-16` 命中后默认可 1:1 落为 `分镜N（约X秒）:`；合并只是例外，必须证明不损失观看结果、平台节奏、下游 payload 或动作连续性。
- 扩展触发点矩阵：新增平台钩子/停滑点、微动作/微表情跳点、文字/屏幕/字幕可读点、物理接触/道具交互点、构图/画幅刺激点、AIGC 执行重置点。
- 将 `references/global-rhythm-terminology-glossary.md` 纳入节奏术语争议和分镜密度审查入口，统一 `sequence_density_curve`、`rhythm_profile`、`beat_trigger`、`shot_count_decision` 与 `shot_duration_decision` 的层级边界。
- 调整 2 镜集中闭环：快节奏平台默认允许高切换密度；机械校验只给 warning，只有显式 `--strict-shot-distribution` 才升级为错误。review 重点改为抽样确认第二镜是否有有效触发、观看结果、平台节奏价值或 AIGC 执行稳定性价值。
- 同步更新 `SKILL.md`、`beat-analysis-contract.md`、`visual-rhythm-analysis-contract.md`、`sequence-density-curve-contract.md`、`shot-planning-integration-contract.md`、workflow、review gate、templates、README、scripts README 与 `CONTEXT.md`，将节拍模型从“双层复判”简化为 trigger-first 细则。

## 2026-05-23 (Two-Person Axis / 180-Degree Rule)

- 吸收 `input/13424024829236292.mp4` 音频教程：双人/多人对峙、追逐、动作和谈判场必须先建立 line of action、screen left/right、中间空间锚点和同侧 180 度拍摄半区。
- 更新 `shot-continuity-contract.md` 与 `ai-video-prompt-execution-contract.md`：新增逐镜 `axis_continuity_anchor`，要求下游可消费分镜重复空间锚点，避免 AI 生图/视频随机左右反转；换轴必须通过中性、主观、可见运动镜头或角色换位桥接。
- 同步 `SKILL.md`、`steps/cinematography-workflow.md`、`review/review-contract.md` 与 `CONTEXT.md`，新增 `FIELD-CINE-27` / `GATE-CINE-27` / `FAIL-CINE-05V`，使轴线规则进入计划汇流、审查门禁和修复打法。

## 2026-05-22 (Scene / Shot Identity)

- 吸收 AI 视频提示词与光线学习：新增共享 `../_shared/scene-shot-identity-contract.md`，要求先锁定场景身份和镜头身份，再组织人物动作。
- 更新 `ai-video-prompt-execution-contract.md`：把执行顺序扩展为 scene/shot identity -> camera -> motion -> action -> microdynamic -> lighting result，收紧相对镜头方向和光线结果写法。
- 更新 `scene-visual-constraint-contract.md`、`SKILL.md`、review 与经验层：内部 `scene_visual_constraint` 先裁决年代、空间功能、环境声、材质年代感和天然光影，再裁决构图、光源、色彩与摄影参数。

## 2026-05-22 (Prop Shot Admission)

- 吸收“角色活人感行为动机”学习：摄影阶段新增多人动作-反应焦点检查，要求先区分 `action_driver/reaction_receiver/ambient_participants`，避免所有角色同强度表演或为同时照顾多人/物件制造奇怪角度。
- 同步 `SKILL.md`、`shot-continuity-contract.md`、review 与经验层，新增 `FIELD-CINE-25` / `GATE-CINE-25` / `FAIL-CINE-05U`，并接入共享 `lived-in-character-behavior-contract.md`。
- 新增人物动作链优先分镜规则：每条涉及人物的 `分镜N` 必须先承接姿态、站位、朝向、身体接触、动作方向和注意力落点，再决定镜头切点、焦点、道具插入和时值。
- 同步 `SKILL.md`、`shot-continuity-contract.md`、review 与经验层，新增动作链优先检查和 `FAIL-CINE-05T`，防止物件切点牺牲人物动作连续性。
- 新增道具镜头准入规则：道具、反射、倒影、涟漪、餐具/杯子/纸张/桌面等物件细节，只有在角色互动、关键信息/规则/证据/危险源或必要环境交代时才可成为焦点、特写、反射主体或衔接节点。
- 同步更新 `SKILL.md`、`CONTEXT.md`、`visual-matching-contract.md`、`visual-sequence-alignment-contract.md`、`shot-detail-dimension-contract.md`、`shot-planning-integration-contract.md`、`unified-shot-design-workflow.md`、review gate 与模板，新增 `FIELD-CINE-23` / `GATE-CINE-24` / `FAIL-CINE-05S`。
- 下游 `5-分组/references/bridge-shot-contract.md` 同步收紧连接件锚定物：不得把普通无互动道具升级为组间连接锚点。

## 2026-05-21 (Refinement & Optimization)

- 重命名 `references/transition-anchor-contract.md` → `references/intra-shot-transition-contract.md`：更准确反映"分镜块内过渡"而非"边界交出"的功能定位，与 `transition-design-contract.md`（边界交出）形成清晰区分。
- 更新 `SKILL.md` 中的引用路径。

## 2026-05-21 (Unified Shot Design Workflow)

- 新增 `references/unified-shot-design-workflow.md`：整合 `shot-planning-integration-contract.md`、`shot-detail-dimension-contract.md` 和 `natural-shot-detail-writing-contract.md` 三份文件的核心理论，形成从内部计划到外部成稿的完整链路。
- 本文件定位为 `4-摄影` 的设计层核心文档，原三份文件作为历史参考保留，待框架稳定后可逐步废弃。
- 文档包含：8个设计前必填字段清单、6大维度家族详解、18步设计流程、自然成稿策略、13项输出充分性门槛。

## 2026-05-21 (Transition Anchor Contract - Shot-level Continuity)

- 新增 `references/transition-anchor-contract.md`：定义分镜间「过渡锚点」的标准描述格式和执行规则，填补 `shot-continuity-contract.md` 在分镜明细内部连续性设计的空白。
- 过渡锚点类型：运动延续锚点、道具形态锚点、声音时序锚点、光色明暗锚点，每种类型包含标准化格式模板和正反示例。
- 制定过渡帧时长规则：高速运动0.2-0.3秒、中速运动0.3-0.5秒、慢速/静止0.5-1秒。
- 制定验收审计检查表：因果链覆盖率100%、过渡帧可见性、道具唯一性、声音时序、叙事意图标注、过渡帧时长六项检查。
- 定义因果黑洞禁令：禁止在相邻分镜间留下没有物理因果过渡的断裂。
- 更新 `shot-continuity-contract.md` 关联说明：将本契约标记为镜头连续性规则的延续，专注于分镜明细内部的过渡设计。
- 解决案例：第4集4-1-2枪击分镜（分镜1→分镜2缺少枪刃接触鱼篓的瞬间）已通过本契约提供修复模板。

## 2026-05-20 (Execution Completeness Gate Repair)

- 统一运行入口命名：`SKILL.md` frontmatter、标题、Context Loading Contract、`agents/openai.yaml`、README、types Mermaid 和相关合同均收束为 `$4-摄影` / `4-摄影`，移除当前源层的旧摄影阶段唤起名混淆口径。
- 强化 completion gate：`scripts/validate_cinematography_markup.py` 只作为机械校验证据，不能替代 `review/review-contract.md` 的质量门禁；交付前必须同时完成机械校验和质量 review。
- 将 `GATE-CINE-15B` / `FAIL-CINE-05R` 非复述型分镜门禁贯通到 templates、report template、README、workflow pass evidence 和 review output，要求记录源句复述扣除测试结果。
- 补齐 `FAIL-CINE-19A/19B/19C/19D` failure routing，使动作锚点继承、正面双眼特写、抽象情绪词转译和心理剧烈变化慢镜头规则都有明确返工入口。
- 更新 `scripts/README.md`，明确脚本不得裁决源句复述扣除测试、功能性影视投影、非复述型分镜、摄影美学或 AI 视频执行稳定性。

## 2026-05-14 (Scene Visual Constraint Refactor)

- 将"组级画面视觉基调"从 4-摄影 的成稿输出降级为内部场景视觉约束，并将正式的组级画面属性输出移至 5-分组 阶段。
- 重命名 `references/group-visual-profile-contract.md` → `references/scene-visual-constraint-contract.md`：定义不变（构图布局/构图方式/光源/照明类型/色彩体系/摄影技术参数），但明确为纯内部裁决不进入成稿。
- `steps/cinematography-workflow.md`：`N6.3-GROUP-VISUAL-PROFILE` → `N6.3-SCENE-VISUAL-CONSTRAINT`；N6.4/N6.5/N7 同步更新引用；N7 不再注入画面基调语句。
- `SKILL.md`：Execution Contract step 9/10 移除组级画面属性成稿注入；Field Mapping FIELD-CINE-20 改为场景视觉约束内部裁决；PASS-CINE-08B 改名为场景视觉约束；Output Contract 删除画面基调输出要求。
- `review/review-contract.md`：`group_visual_profile_review` → `scene_visual_constraint_review`；`GATE-CINE-22` 改为内部裁决检查；`FAIL-CINE-05P` 重新定义。
- `templates/episode-cinematography.template.md`：删除画面基调行和组级画面属性输出。
- `CONTEXT.md`、`knowledge-base/cinematography-heuristics.md`：所有"组级画面属性"→"场景视觉约束"。
- 正式的"组级画面属性"输出由下游 `5-分组` 新增 `N4-VISUAL-TONE` 节点负责。

## 2026-05-14 (Group Visual Profile & Shot Detail Dimensions)

- 新增 `references/group-visual-profile-contract.md`：定义分镜组级 `group_visual_profile` 的结构化字段——构图布局（主体/陪体/前景/背景分配）、构图方式（形状感/线条感/影调感/虚实感/节奏感/纹理质感/气势七个子维度）、光源设置（主光/辅助光/逆光效果）、照明类型、色彩体系（色相/明度/饱和度/色温/色彩心理）和摄影技术参数（机型/光圈/快门/ISO/焦距/分辨率）。要求每个 visual_unit 在摄影语法裁决后形成内部组级画面属性，成稿在场景标题下方以自然语句呈现。
- 新增 `references/shot-detail-dimension-contract.md`：定义每条 `分镜N` 需覆盖的扩展维度族群——角色表演（情绪表现/肢体语言/语气语速/镜头意识）、非角色动态（运动特征/陪体动态/前景动态/背景动态）、镜头技术（景别变化/镜头运动/镜头视角）、光影精细（光影变化/光影反射）、焦点精细（动态焦点与景深变化）、节奏同步。低信息镜覆盖 2-3 个维度，高信息镜覆盖 6-8 个维度，维度信息融入自然中文而非标签列表。
- 在 `references/cinematic-technique-library.md` 新增"构图方式"大分区（含形状感/线条感/影调感/虚实感/节奏感/纹理质感/气势七个子分区的完整技法表）和"摄影技术参数"大分区（机型/光圈/快门/ISO/焦距/分辨率的选项和使用场景）。
- 在 `steps/cinematography-workflow.md` 新增节点 `N6.3-GROUP-VISUAL-PROFILE`（位于 N6.2-CAMERA-GRAMMAR 和 N6.4-FUNCTIONAL-PROJECTION 之间），更新 N6.4 增加维度覆盖裁决、N6.5 消费组级属性和维度覆盖、N7 注入组级画面属性语句和扩展维度信息点；同步更新 Mermaid 拓扑图、分支规则和返工路由。
- 更新 `SKILL.md`：Reference Loading Guide 新增组级画面属性和分镜明细维度入口；Execution Contract step 9/10 接入 `group_visual_profile`、`dimension_coverage`；Thought Pass Map 新增 `PASS-CINE-08B` 组级画面属性，更新 `PASS-CINE-09/10/11` 消费组级属性和维度覆盖；Field Mapping 新增 `FIELD-CINE-20`（组级画面属性）和 `FIELD-CINE-21`（分镜明细维度覆盖）；Output Contract 和 Completion gate 新增组级属性和维度覆盖要求。
- 更新 `templates/episode-cinematography.template.md`：frontmatter 新增 `group_visual_profile_policy` 和 `shot_detail_dimension_policy`；模板正文新增组级画面属性行；示例 1 更新为带组级画面属性的完整格式。
- 更新 `review/review-contract.md`：新增 `group_visual_profile_review` 和 `shot_detail_dimension_review` review 模式；新增 `GATE-CINE-22`（组级画面属性）和 `GATE-CINE-23`（分镜明细维度覆盖）验收门禁；新增 `FAIL-CINE-05P`（组级属性缺失/退化）和 `FAIL-CINE-05Q`（维度覆盖不足/标签化）失败路由。
- 更新 `CONTEXT.md`：Type Map 新增 4 条组级属性和维度覆盖相关失败模式与修复路径；Repair Playbook 新增步骤 28-30（组级属性检查、维度覆盖抽样、组级属性更新时机）；Reusable Heuristics 新增 4 条组级属性和维度覆盖经验。
- 更新 `knowledge-base/cinematography-heuristics.md`：新增"Group Visual Profile Heuristics"和"Shot Detail Dimension Heuristics"两个分区，沉淀组级属性和维度覆盖的可复用经验。

## 2026-05-14

- 将 `4-摄影` 单镜时值默认口径调整为短剧·AIGC 节奏偏置：默认优先 `short / standard`，普通氛围镜、过场动作和常规反应不得沿用传统影视宽停顿；`约3秒` 以上必须有台词、读秒、表演变化、复杂调度、空间重置或高点证据。
- 更新 `references/shot-duration-decision-contract.md`：新增 `short_drama_aigc_duration_bias`、`duration_mode`，整体下压 `instant / short / standard / held / long_hold` 的估算范围，并明确 AIGC 工具片段时长不得反推拉长单镜叙事时值。
- 同步更新 `SKILL.md`、`steps/cinematography-workflow.md`、`references/visual-rhythm-analysis-contract.md`、`references/shot-planning-integration-contract.md`、`review/review-contract.md`、模板、README、CONTEXT 和 knowledge-base，使生成、计划汇流、review 与修复都检查短剧·AIGC 时值压缩。
- 调整 `templates/episode-cinematography.template.md` 示例：环境、对白、动作和高点样例整体压短，保留高点读秒但不再以 4-6 秒作为默认诱导。
- 更新机械校验脚本：`validate_cinematography_markup.py` 对 `<1s`、`>3s`、`>5s` 给出分级告警，提示闪切、短剧·AIGC 必要性和强例外确认。

## 2026-05-13 (Optimization Pass)

- CONTEXT.md 全量压缩：Type Map 从 31 行精简为 26 行（合并字段纯度 4→2 行，删除已被 gate 覆盖的节点缺环和交付未修行）；Repair Playbook 从 27 步压缩为 27 步但去除重复展开；Reusable Heuristics 从 ~39 条压缩为 12 条，其中 19 条已正式化为 contract/gate 的条目删除，6 条通用经验迁移到 knowledge-base。项目特定（诡校-测试版）内容迁移并在原位改为指向 knowledge-base 的通用引用。CONTEXT.md 从 ~25,600 字符压缩到 ~12,000 字符，status 从 warn 恢复为 ok。
- knowledge-base/cinematography-heuristics.md 从 37 行扩展到 ~130 行，新增 Shot Count & Beat、Duration & Time-Value、Sequence & Ownership、AI Video Execution 四个分类分区，吸收 CONTEXT.md 中的可复用经验并补充 15+ 条新通用经验（含对白拆镜、群像扩散、规则文字显影、秒数门槛、连续 held 镜头风险、sequence_profile 建立门槛、density_curve peak/recovery 成对、镜头/人物运动时序、方向含动作词、光线写可见结果等）。
- templates/episode-cinematography.template.md 从 33 行扩展到 ~100 行，新增 5 个具体场景示例：单镜低信息环境建立、双镜对白身体锚点（快慢接力）、三镜动作序列（动作分相递进）、高点 held 镜头（读秒 + 反应）和内部 shot_design_plan 计划结构展示。
- references/transition-design-contract.md 清理开头"保留旧路径/语义已迁移"混淆性说明，改为清晰的角色声明："本文件定义 4-摄影 的边界交出合同"。
- scripts/validate_cinematography_markup.py 新增 4 项机械检查：frontmatter 存在性（stage/source_writing_directing_path/output_path/duration_policy）、秒数范围提示（<1s 闪切确认 / >15s 内部变化确认）、抽象阐释词扫描（象征/隐喻/寓意/暗示了等 12 个词）和空分镜明细块检查。scripts/README.md 同步更新允许职责列表。
- README.md 快速入口新增 `templates/episode-cinematography.template.md` 和 `knowledge-base/cinematography-heuristics.md`；输出说明新增机械校验脚本扩展能力描述。

## 2026-05-13

- 基于 `浪花传说之琉球篇/第2集-电影特别版` 摄影稿复盘，新增 `references/sequence-density-curve-contract.md`，把节奏把控从单句 `beat_map/rhythm_profile` 上收为段落级 `sequence_density_curve`：先裁决 `tempo_beats`、`density_ramp`、`peak_slots`、`recovery_slots`、`set_piece_chain_slots`、`sound_cut_pattern` 和 `density_budget`，再进入单句分镜数量与时值裁决。
- 在 workflow 中新增 `N3.6-DENSITY-CURVE`，要求连续观看段落先判断哪里省镜头、哪里加密、哪里停顿、哪里硬切、哪里交出；并让 `N4-BEAT`、`N5-RHYTHM`、`N5.2-DURATION`、`N5.5-PEAK-SHOT`、`N6.5-SHOT-PLAN` 与 review 消费该曲线。
- 为动作 set-piece 增加 5-6 镜例外：连续命中、连续反弹、连续物件结果或“一声一结果”的声画打点可突破 4 镜上限，但每镜必须有独立起点、撞点、结果或反应，高密度后必须有恢复/反压/交出锚点。
- 更新 `SKILL.md`、beat/rhythm/shot-planning、review、README、模板与 `CONTEXT.md`，新增 `GATE-CINE-04A2/04A3`、`FAIL-CINE-03D/03E` 和执行报告 `density_curve_summary` 字段，防止整场全满、全空、平均同密度或只靠分布统计替代节奏曲线。
- 放宽 `分镜明细` 的分镜密度上限：将仍停留在 `1-3` / `2-3` 的 beat 与 rhythm 细则同步调整为可按真实节拍扩展到 `1-4` / `2-4`，同时保留反模板化约束，禁止把四分镜当固定占位。
- 基于 `reports/transcripts/audio/AI视频镜头与提示词学习稿.md` 新增 `references/ai-video-prompt-execution-contract.md`，把“镜头包裹动作、方向参照、光线结果、表演微动态、提示词分栏边界”转译为 `4-摄影` 的视频执行稳定性合同。
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

- 将 `4-摄影` 的转场职责降级为边界交出职责：保留镜头内部连续性、进入点、最后一镜可消费交出锚点和连续性风险，不再主创组间或跨场景创意转场方案。
- 保留 `references/transition-design-contract.md` 路径但重写为 `Handoff Boundary Contract`，将 `transition_profile` 迁移为 `handoff_profile`，连接方式、强度和 3-4 秒连接件提示交由 `5-分组` 裁决。
- 同步更新 SKILL、workflow、types、review、templates、README、CONTEXT 和相关 references，避免 `PASS-CINE-07T`、review gate 或类型路由继续把普通切镜、软桥接、匹配剪辑和高能转场拉回摄影阶段。

## 2026-05-03

- 新增 `references/transition-design-contract.md`：场景变化固定视为明确转场动机，但转场强度另判；普通切镜、软桥接、匹配剪辑和高能转场按交出点/进入点与接口证据分级。
- 在 `SKILL.md`、types、visual rhythm、continuity、shot planning、workflow、技法库、功能投影、review gate、README 与 CONTEXT 中同步接入 `transition_profile`，要求场景变化至少处理上一画面交出点和下一画面进入点。
- 源层修复分镜数量塌缩问题：明确 `分镜2` 不是默认占位，只有存在第二个真实观看策略时才成立；低信息块可收敛为 1 镜，关键显影、群像扩散、动作分相或高点承托可按真实节拍扩展到 3-4 镜。
- 在 `beat-analysis-contract.md`、`visual-rhythm-analysis-contract.md`、`shot-planning-integration-contract.md`、workflow、review gate 与模板中新增 `shot_count_decision` 和 2 镜集中复判规则，防止批量输出被模板诱导为固定两镜。
- 更新 `validate_cinematography_markup.py` 与脚本说明，新增分镜数量分布统计和 2 镜异常集中提示；脚本只做机械告警，不替代 LLM 节拍判断。
- 同步升级 `4-摄影` 思维·执行节点：`Thought Pass Map` 扩展为 `PASS-CINE-00..12`，覆盖真源语境、画面边界、类型画像、节拍、节奏、高点、顾问、连续性、摄影语法、功能投影、分镜计划、注入和审查修复闭环。
- 在 `steps/cinematography-workflow.md` 新增 `N6.2-CAMERA-GRAMMAR` 与 `N6.4-FUNCTIONAL-PROJECTION`，把景别/视角/景深/焦点/镜头类型/构图/光色/运镜变化和下游 payload 从 `N6.5-SHOT-PLAN` 中拆成显式前置节点。
- 更新 `shot-planning-integration-contract.md`，新增 `camera_grammar_plan` 与 `functional_projection_plan`，要求每个 `分镜N` 能回指摄影语法选择、功能 payload、连续性交接和自然成稿策略。
- 更新 review gate：新增 `thinking_action_node_review`、`camera_grammar_review`、`GATE-CINE-16 摄影语法变化`、`GATE-CINE-17 思维·执行节点完整` 以及 `FAIL-CINE-05I/05J`。
- 调整 `4-摄影` 顾问与复核流程 参谋机制：顾问问题不再固定为摄影字段清单，而是同步于当前 `PASS-CINE-*` / `N*-*` 思维·执行节点。
- 要求监制顾问代入角色意识、创作风格和专业水准，基于节点的判断、动作、证据、gate 与返工风险提供参谋指导。
- 同步更新 `SKILL.md`、workflow、review gate、`CONTEXT.md` 与共享 team advisor 合同，要求 `init_team_synthesis_context` 记录 node/pass/gate 来源和角色视角。

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

- 明确 `4-摄影` 执行顾问与复核流程时的执行机制：以项目 `team.yaml` 中明确的监制组相关智能顾问团作为摄影监制。
- 新增 `Init Team Synthesis Consumption`，要求顾问代入专业视角和个人风格，对已知上下文提出摄影方向参谋指导，并由主 agent 汇流为 `init_team_synthesis_context`。
- 在 workflow 中新增 `N5.6-ADVISOR`，将顾问参谋沉淀为 LLM 分镜明细注入、阶段内修复和复审的后续上下文。
- 同步更新 review gate 与 CONTEXT 经验层，阻断“泛泛电影感评价”“本地模拟顾问”和“顾问意见越权改写上游编导稿”。

## 2026-04-29

- 新增阶段末 `Stage-End Review-Repair Contract`，将候选摄影稿固定为 `candidate -> review -> direct repair -> re-review -> canonical writeback` 闭环。
- 在 workflow 中新增 `N8R-DIRECT-REPAIR` 与 `N8R-REVIEW-AGAIN`，要求 review 阻断项在 `4-摄影` 阶段内最小修复并复审后才能交给下游。
- 更新 review gate、CONTEXT 和执行报告字段，明确覆盖、编号、节拍、连续性、专业可执行、峰值分镜和保真问题不得降级为交付后 followup。

## 2026-04-28

- 新增 `references/peak-shot-language-contract.md`，承接 `2-编导` 的高潮画面机制，补齐摄影阶段的峰值分镜、分镜明细和运镜强化合同。
- 在 workflow 中新增 `N5.5-PEAK-SHOT`，要求上游高点形成内部 `peak_shot_profile`，决定分镜密度、景别尺度、运镜速度、停顿/断裂和余波交接。
- 在 review gate 中新增高潮分镜检查，避免上游高点被按普通画面压平，也禁止为了强化高潮新增事实、对白或动作结果。
- 同步更新技法库、画面节奏、模板、README 与 CONTEXT，明确高潮镜头不等于一律加速加镜头。

## 2026-04-25

- 初始化 `aigc/4-摄影` Skill 2.0 包结构。
- 建立以 `2-编导/第N集.md` 为输入、`4-摄影/第N集.md` 为输出的摄影分镜明细注入合同。
- 新增画面匹配、节拍分析、分镜明细注入、经典构图、高超运镜、高能转场、光影美学、色彩美学等动态引用分区。
- 增加 `诡校-测试版` 编导稿样本导出的封闭校园惊悚视觉母题经验。
- 补充景别、景深、镜头视角、镜头类型、运镜速度等摄影执行参数细则，并同步到输出模板与 review gate。
- 新增动态分镜明细表达合同，要求 `分镜N` 写成从起点到终点的变化、组合运镜、速度曲线和注意力转移路径，避免静态呆板参数堆叠。
- 新增镜头连续性合同，要求每个画面句子的分镜明细回看临近至少前 3 个画面单位，避免无动机跳轴、跳色、跳景别、空间跳跃和风格断裂。
- 新增画面节奏分析合同，用 `rhythm_profile` 控制分镜明细的收敛、标准展开、发散强化和断裂发散，保证不同信息重要性的画面句子张弛有度。
- 调整连续性输出策略：前 3 画面回看作为内部判断，不在每条 `分镜N` 中机械显式展示；输出集中于当前画面，仅在明显跳变或强转场时短写承接动机。
- 调整画面节奏输出策略：`rhythm_profile` 作为内部判断，不在 `分镜N` 中显式展示“收敛/标准展开/发散强化/断裂发散”标签。
- 补充项目级上下文加载要求：绑定具体项目时必须加载 `MEMORY.md`、`0-初始化/north_star.yaml`、`team.yaml` 与相关 `CONTEXT/`。
