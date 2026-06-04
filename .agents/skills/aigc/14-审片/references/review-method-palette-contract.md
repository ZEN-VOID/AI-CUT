# Review Method Palette Contract

本合同定义 `9-审片` 的方法库。`N0 -> N7` 是默认自动化载体，不是审片方法本身；真实审片必须按素材类型、分镜目标、prompt 证据、用户示例和已观察到的视频信号，动态选择审片方法，并把结论转成可执行操作。

## Method Selection Rule

- 每次审片至少覆盖三类底座方法：真实视频理解、source / prompt 对照、创作质量判断。
- 其余方法按信号选择，不要求每条视频机械跑满全部方法；但被跳过的方法必须有原因，例如 `not_applicable`、`no_audio`、`no_dialogue`、`single_static_shot`、`no_user_examples`、`evidence_missing`。
- 方法选择必须发生在 `N3-EVIDENCE` 之后、最终 `N4-COMPARE` 之前；没有 `observed_content_summary` 时不能选择或跳过方法。
- 用户明确关注的审片点必须进入 selected methods；顾问与复核流程提出的高风险点必须进入 selected methods 或写明拒绝原因。
- 方法输出不是评分表，而是 `method_findings`：每条都要包含 observable evidence、expected / actual、root cause guess、confidence 和 candidate operations。

## Method Families

| method_id | use when | checks | evidence |
| --- | --- | --- | --- |
| `source_fidelity_pass` | 任意对照分镜组或剧本原文的审片 | 事件、人物、关系、场景、道具、动作、台词/旁白、首尾状态是否承载原文目标；是否擅自增删剧情事实 | 分镜组摘录、原文摘录、prompt、关键帧/音频证据 |
| `continuity_pass` | 同组变体、连续镜头、入场/出场、角色或道具延续 | 角色身份、服装、站位、朝向、光线、空间轴线、道具状态、进入/退出状态是否连续 | 首尾关键帧、相邻组、变体对照 |
| `performance_pass` | 有人物表演、权力关系、情绪变化或动作任务 | 眼神方向、微表情、肢体语言、动作动机、情绪转折、压迫/躲避/犹豫等关系是否成立 | 人物关键帧、运动摘要、原文情绪目标 |
| `cinematography_pass` | 镜头语言影响叙事或用户关注画面表现 | 机位高度、景别、构图、前景/遮挡、焦点转移、镜头运动动机、观众位置是否服务信息揭示 | 联系表、镜头运动描述、摄影 prompt |
| `editing_rhythm_pass` | 15 秒片段承担多个 beat、转场或节奏目标 | 起承停点、信息密度、停留时长、切点可接性、是否乱切或平铺 | 时序截图、shot boundary、首尾状态 |
| `sound_pass` | 有音轨、对白、BGM、环境声或用户要求静音/声音 | 音量、同步、对白/旁白是否可辨、非预期 BGM、环境声是否破坏叙事；无音频是否符合目标 | ffprobe / 音频检测、试听笔记 |
| `prop_object_pass` | 关键物、文字、书册、武器、屏幕、门牌或剧情线索重要 | 关键物是否出现、可读性是否合适、状态是否连续、是否被替换/融化/错位 | 关键帧 crop、分组道具目标 |
| `ethics_safety_pass` | 暴力、胁迫、伤害、性暗示、未成年人、危险行为或项目禁区相关 | 是否美化伤害/胁迫、是否违反项目禁区、是否需要弱化或改写呈现方式 | 项目 MEMORY / north_star、原文上下文、画面证据 |
| `aigc_artifact_forensics` | 任意 AIGC 视频，尤其近景、手、脸、文字、运动复杂片段 | 手脸崩坏、伪文字、肢体多余、物体融化、身份漂移、空间漂移、时间闪烁、物理错误 | 逐帧关键点、联系表、局部截图 |
| `prompt_execution_pass` | 有本地 prompt、LibTV prompt、用户 prompt 或重新提交需求 | prompt 是否缺失、矛盾、过载、占位污染、图片顺序错误、负面约束不清；视频是否执行核心指令 | prompt before/after、LibTV node query、expected / actual |
| `candidate_selection_pass` | 同组多个变体或用户要求选片 | 比较共同问题、单片优势、修复成本、与原文和审美目标的距离；选择 primary / backup / reject | 变体联系表、finding 对照表 |
| `repair_design_pass` | finding 需要执行动作而不只是评价 | 是否该接受、条件接受、重跑、改 prompt、改图片顺序、拆组/并组、修资产引用、改音频策略或升级源层 | candidate operations、chosen operation、拒绝其他操作的理由 |

## Operation Palette

| operation_id | use when | required evidence |
| --- | --- | --- |
| `accept_as_candidate` | 视频匹配目标且质量足够，可作为当前组候选 | verdict、优势点、残留风险 |
| `conditional_accept` | 技术可用但有轻微缺陷或创作质量不是最优 | 条件、适用位置、为什么不阻断 |
| `compare_variants` | 同组存在多个候选或需要选片 | variant ranking、共同问题、单片问题 |
| `rerun_same_prompt` | prompt 清楚但单次模型瑕疵或 seed 漂移 | model_problem 证据、无需改 prompt 的理由 |
| `rerun_with_seed_or_model_change` | 同 prompt 多次失败或模型弱点明显 | 重复证据、建议参数/模型变化 |
| `libtv_prompt_repair_and_rerun` | LibTV prompt 有缺失、过载、占位污染或用户要求修后重提 | before query、clean prompt、final query、task id / result URL |
| `group_prompt_repair` | `5-分组` 组正文或节奏导致生成不稳定 | 目标 group patch、稳定性理由 |
| `shot_split_or_merge` | 单组承载过多 beat 或相邻组切分破坏连续性 | beat list、拆/并后的首尾状态 |
| `asset_reference_repair` | 角色、场景、道具、参考图或图片绑定错误 | 资产引用证据、正确引用目标 |
| `image_order_repair` | LibTV `imageList/mixedList` 顺序或图片占位导致错配 | node query、图片顺序 before/after |
| `sound_policy_repair` | 音频策略、BGM、对白或静音要求不清 | 音频事实、目标声音策略 |
| `download_or_naming_repair` | 下载落点、文件名、variant、node key 或外部 id 漂移 | 原始路径、canonical path、命名修复 |
| `request_missing_evidence` | 无法形成真实视频理解或源/prompt 证据不足 | 缺失证据清单、最小补充输入 |
| `source_escalation_candidate` | 多例复现且能定位阶段合同或模板问题 | 多例证据、source owner、升级门检查 |
| `archive_rejected_candidate` | 候选不可用但需保留证据避免重复使用 | reject reason、归档路径或报告标记 |

## Operation Design Rule

- 每条 `P0` / `P1` finding 必须至少给出一个 `candidate_operations` 和一个 `chosen_operation`。
- 对 `rerun`、`group_repair`、`libtv_prompt_repair_and_rerun`、`source_escalation_candidate` 这类互斥动作，必须说明为什么没有选择其他动作。
- `landing` 是写回层级，`operation` 是具体动作；例如同为 `group_repair`，操作可以是 `group_prompt_repair`、`shot_split_or_merge` 或 `asset_reference_repair`。
- 用户授权重新提交时，操作设计必须先通过 prompt hygiene，再运行 LibTV rerun；不得用“建议重跑”冒充已重新提交。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否在真实视频理解之后选择了适配目标视频的方法，而不是机械套固定三层流程或漏掉用户关注审片点？ | `GATE-REVIEW-16` | `FAIL-REVIEW-METHOD-SELECTION` | `steps/video-review-workflow.md#N4 Method Palette Compare`、本文件 `Method Selection Rule` | `method_selection.selected_methods`、`skipped_methods`、选择理由 |
| 选定方法是否覆盖真实视频理解、source/prompt 对照和创作质量底座，并按视频信号扩展到表演、摄影、节奏、声音、道具、伦理、安全或 AIGC 伪影等适用方法？ | `GATE-REVIEW-16` | `FAIL-REVIEW-METHOD-SELECTION` | 本文件 `Method Families` | method coverage table、未覆盖项理由 |
| 每条重要 finding 是否从 verdict 转化为候选操作和最终操作，而不是只写“好/坏/重跑”？ | `GATE-REVIEW-17` | `FAIL-REVIEW-OPERATION-DESIGN` | `steps/video-review-workflow.md#N5 Landing And Operation Design`、本文件 `Operation Palette` | `candidate_operations`、`chosen_operation`、拒绝其他操作的理由 |
| operation 与 landing 是否区分清楚，且受控动作如 LibTV rerun、`5-分组` patch、源层升级都有授权和证据闭环？ | `GATE-REVIEW-10` / `GATE-REVIEW-17` | `FAIL-REVIEW-OPERATION-DESIGN` | `references/finding-landing-contract.md`、`references/libtv-intake-contract.md` | operation plan、authorization note、changed files / task id |
