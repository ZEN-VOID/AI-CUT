# Field Master

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| FIELD-DETAIL-01 | 技能包.阶段边界 | 锁定 `3-Detail` 只负责 shot-level 明细，不越权改 `2-Global` 或下游资产阶段 | root `aigc`、`2-Global`、runtime layout | S1 | 边界清晰度 | FAIL-DETAIL-01 |
| FIELD-DETAIL-02 | 技能包.scope 与 bootstrap | 锁定命中组/镜、增量 patch 范围、是否需要 bootstrap | 用户约束、现有 `第N集.json`、bootstrap template | S2 | 路由完整性 | FAIL-DETAIL-02 |
| FIELD-DETAIL-03 | 技能包.预设显化与参考锚点 | 明确初始化预设要求呈现的元素、可参考的大师手法/作品桥段/知识库命中，并锁定 `叙事内核 / Previous End / Current Mission / Next Start / 情绪引导` 后转译为可执行表述 | `north_star`、`init_handoff`、`story-source-manifest`、`00-故事` 或等价故事源、命中知识库 | S2 | 参考可执行性 | FAIL-DETAIL-03 |
| FIELD-DETAIL-04 | 技能包.shot skeleton | 生成稳定的 `分镜ID / 时间段 / coverage` 骨架 | `第N集.md`、`grouping.json`、导演意图、参考锚点 | S3 | skeleton 稳定性 | FAIL-DETAIL-04 |
| FIELD-DETAIL-05 | 业务字段.空间与构图 | 锁定 `角色背景面`、`分镜表现` 与 shot-level 镜头描述子槽，并用量化密度机制明确主陪背景层级、构图布局、构图方式、`景别节奏预判` 与 `POV 策略预判` | skeleton、导演意图、全局风格、参考锚点、`pace_tier`、故事记忆与情绪引导 | S4 | 空间可读性 | FAIL-DETAIL-05 |
| FIELD-DETAIL-06 | 业务字段.站位与道具 | 锁定 `角色站位走位`、`道具及状态` 的几何与叙事功能；服装不上镜级常驻字段，改由父级聚合回填组级 `出场角色及穿搭` | skeleton、结构链、角色任务、组间设计 | S5 | 可拍性 | FAIL-DETAIL-06 |
| FIELD-DETAIL-07 | 业务字段.角色表现 | 把情绪/动作/关系翻译成镜头可见表演，并显化角色个性、习惯动作、下意识、`Character Arc` 中极力掩饰的内容、对手戏中的攻守与距离策略、对话互动技巧，以及可被捕捉的眉眼/身体信号与潜台词微动作 | skeleton、导演意图、结构 draft、当前镜的空间/站位/冲突关系、`2.1.1-角色清单` 或等价角色源、Dialogue & Interaction KB（若有） | S6 | 表演可见性 | FAIL-DETAIL-07 |
| FIELD-DETAIL-08 | 业务字段.场景氛围 | 把时间感、空气感、压迫/抒缓气候写成可感知条件 | 组间设计.全局风格、组间设计.导演意图、空间 draft | S7 | 氛围可感知性 | FAIL-DETAIL-08 |
| FIELD-DETAIL-09 | 业务字段.运镜手法 | 先给默认叙事路由，再吸收结构链已转译的运动提示，最后在同目标内比较更强镜头变体并按需升格挑战方案 | 组间设计.类型元素、组间设计.导演意图、core draft、`academy_hit_note`（若含运动相关提示） | S8 | 叙事优先度 | FAIL-DETAIL-09 |
| FIELD-DETAIL-10 | 业务字段.摄影美学 | 先回看上游 `组间设计` 摄影底座，再把光位/组级光影推进/色彩心理子补丁合成 single-line final look | 组间设计.全局风格、组间设计.类型元素、组间设计.导演意图、氛围、运镜、light/group/color 子补丁 | S9 | 摄影合成度 | FAIL-DETAIL-10 |
| FIELD-DETAIL-11 | 业务字段.转场特效 | 只在有明确叙事收益时补转场或特效 | 组/镜衔接关系、风格禁区、finish draft | S10 | 必要性 | FAIL-DETAIL-11 |
| FIELD-DETAIL-12 | 技能包.review / audit | 定义连续性复核、真源审计与返工入口 | candidate draft、schema、I/O contract | S11 | 闭环完整性 | FAIL-DETAIL-12 |
| FIELD-DETAIL-13 | 技能包.writeback / handoff | 定义 `第N集.json`、`validation-report.md` 与默认下一入口 | final patch set、validation evidence | S12 | 真源收束性 | FAIL-DETAIL-13 |

# Thought Pass Map

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-DETAIL-01 | 当前是不是 `3-Detail` 阶段问题 | 锁阶段边界与上下游职责 | 把本阶段写成 `2-Global` 或 `4-Design` |
| S2 | FIELD-DETAIL-02 `FIELD-DETAIL-03` | 本轮该覆盖哪些组/镜、是否需要 bootstrap、哪些预设与参考锚点必须显化；剥去动作外衣后的叙事内核是什么；上一镜余韵、当前段使命、下一场火药与目标心率分别是什么 | 写出 `scope_plan`、`preset_manifest`、`reference_anchor_note`，并在其中锁 `叙事内核 / Previous End / Current Mission / Next Start / 情绪引导` | 未区分增量 patch / 整集重做，参考仍停在抽象致敬，或没有锁清这一段为何不能被删 |
| S3 | FIELD-DETAIL-04 | skeleton 是否稳定可被后续能力链消费 | 生成 `分镜ID / 时间段 / coverage` 骨架 | 其他链仍需自行脑补镜序 |
| S4 | FIELD-DETAIL-05 | 空间、构图、节拍、景别、镜头属性/框架/类型/视角、主陪背景层级、构图布局/方式与焦点是否成立；authoritative quantizer 生成的 `candidate beat segments / recommended_shot_baseline / shot_count_decision` 是否共同支撑当前镜数；当前段该选哪种 `景别节奏模板` 与 `POV 策略`，并如何在命中镜头窗口里验证心理距离 | 锁 `动作阶段点 / 台词气口点 / 焦点切换点 / 结构转折点`，调用 quantizer 生成密度裁决，再锁主陪背景关系、构图布局、构图方式、镜头描述子槽、焦点、空间锚点、主体重心，并写出 `景别节奏预判 / POV 策略预判 / 节奏曲线验证 / 心理距离审视 / 反直觉检验` | 画面主重心、层级关系和空间关系模糊，镜数无法解释为何不是更少/更多，或景别/视点只服务信息传递却没有服务情感目标 |
| S5 | FIELD-DETAIL-06 | 站位与道具是否支撑动作和观看路径，且服装摘要是否已具备组级回填条件 | 补角色站位走位、道具状态，并提炼组级 `出场角色及穿搭` 摘要素材 | 结构字段彼此打架，或组级服装摘要仍为空 |
| S6 | FIELD-DETAIL-07 | 表演字段由哪种子模式负责，且该角色会以什么个性化方式显露/压住情绪、用什么行为推动叙事、把强情绪落到哪些眉眼与身体信号上；角色此刻最想掩饰什么；若为对手戏，当前空间/站位与权力关系最适合什么攻守与距离策略，以及是否需要引用 Dialogue & Interaction KB 中的特定技巧 | 选择内心 / 动作 / 对手戏一路或多路，并锁角色化表达通道、叙事性行为、微表情承载点、`Character Arc` 隐匿项、必要的对手戏策略提炼，以及 `Selected Technique / Application Logic / Subtext Visualization` | 情绪、动作、关系被混写成空话，表演失去角色辨识度，对手戏只剩抽象关系判断，或潜台词没有落成可拍的身体露馅点 |
| S7 | FIELD-DETAIL-08 | 氛围来源是否具体可感知 | 补空气、温度、密度、压迫等可体验条件 | 只剩形容词口号 |
| S8 | FIELD-DETAIL-09 | 运镜是否先服务叙事清晰度；在默认路线与动机成立后，结构链已转译的运动提示是否值得吸收；并在同目标内完成“默认路线 vs 更强变体”的比较 | 先锁默认叙事路线与运动动机，再吸收可用的上游运动提示，把它压成当前镜头的运动策略，随后比较同目标酷法，条件时追加挑战对照 | 直接默认走挑战方案，用 finish 链重写 core 事实，或以更酷为名偷换表现目标 |
| S9 | FIELD-DETAIL-10 | 摄影是否吸收了项目级风格与导演底座，并真正合成，而不是子补丁堆叠 | 回看项目级摄影底座，收束摄影执行策略，再合成光位 / 组级光影推进 / 色彩心理为 single-line 摄影判断 | `摄影美学` 变成三段口号拼接，停在抽象审美词，或完全失去组内光影推进 |
| S10 | FIELD-DETAIL-11 | 转场/特效是否有明确收益 | 判断是否保持直切、只补 note 或补字段 | 为了存在感强行加效果 |
| S11 | FIELD-DETAIL-12 | 如何证明 candidate 可读、连续、合规 | 运行 review / audit 并生成返工入口 | 没有 veto 或返工入口 |
| S12 | FIELD-DETAIL-13 | 最终如何安全写回并回接下游 | patch-in-place 写回并落 validation-report | 形成第二真源或整稿覆盖 |

# Pass Table

| field_id | 质量维度 | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- | --- |
| FIELD-DETAIL-01 | 边界清晰度 | 明确只负责 `3-Detail` shot-level 明细 | FAIL-DETAIL-01 | S1 |
| FIELD-DETAIL-02 | 路由完整性 | scope、bootstrap、preset 保护都已锁定 | FAIL-DETAIL-02 | S2 |
| FIELD-DETAIL-03 | 参考可执行性 | 预设元素、参考锚点与具像化表述都已显化，且 `叙事内核 / Previous End / Current Mission / Next Start / 情绪引导` 已锁定 | FAIL-DETAIL-03 | S2 |
| FIELD-DETAIL-04 | skeleton 稳定性 | 所有命中镜都有稳定 `分镜ID / 时间段 / coverage` | FAIL-DETAIL-04 | S3 |
| FIELD-DETAIL-05 | 空间可读性 | 构图、节拍、景别、镜头属性/框架/类型/视角、主陪背景层级、构图布局/方式与空间锚点明确，镜数已通过 authoritative quantizer 校验，且 `景别节奏模板 / POV 策略 / 心理距离` 已完成预判与验证，可支撑后续链路 | FAIL-DETAIL-05 | S4 |
| FIELD-DETAIL-06 | 可拍性 | 站位走位、道具状态可直接消费，且组级 `出场角色及穿搭` 已可由当前组镜头稳定回填 | FAIL-DETAIL-06 | S5 |
| FIELD-DETAIL-07 | 表演可见性 | 情绪/动作/关系都已落成镜头可见表演，且带有角色个性痕迹、能推动叙事、有明确的眉眼/身体承载点；`Character Arc` 的隐匿项、对话互动技巧与潜台词微动作都已落成可演策略 | FAIL-DETAIL-07 | S6 |
| FIELD-DETAIL-08 | 氛围可感知性 | 氛围来源具体，可被摄影和画面阶段理解 | FAIL-DETAIL-08 | S7 |
| FIELD-DETAIL-09 | 叙事优先度 | 运镜先服务信息与情绪递送；若上游已转译出运动提示，必须已被吸收到当前镜头可执行的运动语言；若提出更酷变体，必须证明其仍服务同一表现目标且收益明确 | FAIL-DETAIL-09 | S8 |
| FIELD-DETAIL-10 | 摄影合成度 | `摄影美学` 吸收了项目级摄影底座，并把光位、组级光影推进与色彩心理压成单一协调判断 | FAIL-DETAIL-10 | S9 |
| FIELD-DETAIL-11 | 必要性 | 转场/特效只在明确收益成立时补入 | FAIL-DETAIL-11 | S10 |
| FIELD-DETAIL-12 | 闭环完整性 | review / audit 均可否决并给出返工入口 | FAIL-DETAIL-12 | S11 |
| FIELD-DETAIL-13 | 真源收束性 | 只有 `第N集.json` 与 `validation-report.md` 被写回 | FAIL-DETAIL-13 | S12 |
