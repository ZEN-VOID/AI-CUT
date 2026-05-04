# Cinematography Workflow

本文件定义 `3-摄影` 的思行一体化执行节点。

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 给 `2-编导` 逐集稿的每个画面句子注入可执行的大师级运镜摄影设计；`分镜明细：` 仅作为下游兼容字段名 |
| `business_object` | Markdown 编导稿中的字段化画面句子 |
| `constraint_profile` | 保真、逐集落盘、LLM 主创、动态引用、下游可执行、subagents 摄影监制上下文沉淀 |
| `success_criteria` | 每个命中句子下有按节拍生成的 `分镜明细：分镜N`，内容聚焦运镜手法、摄影美学、内部注意力转交和可消费交出锚点，且专业、克制、服务剧情 |
| `non_goals` | 不改剧情、不改对白、不生成图像提示词、不替代下游视频阶段 |
| `complexity_source` | 真源语境锁定、画面匹配覆盖率、类型画像、节拍判断、画面节奏张弛、高潮分镜强化、监制顾问参谋汇流、连续性与空间语法、边界交出点、摄影语法变化、功能性影视投影、shot_design_plan 汇流、自然成稿和保真约束 |
| `topology_fit` | 串行主干 + 类型分流 + subagents 顾问分支 + review 汇流 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、集号、输入真源和上下文 | 用户请求、`2-编导/第N集.md`、项目 `MEMORY.md`、north star、team 与相关 `CONTEXT/` | 定位文件，读取相关上下文，确认不改原文，抽取长期视觉偏好、禁区、制作限制和下游约束 | `source_context_profile`、source path、episode list | `N2-TYPE` | 输入可读、真源明确、项目语境不与上游事实冲突 |
| `N2-TYPE` | 判断画面句子类型与摄影任务画像 | `types/visual-unit-type-map.md`、`source_context_profile` | 建立 visual category、`visual_unit_function` 和审美策略，区分空间建立、动作调度、表演承托、信息显影、恐怖入侵、关系停顿、群像压迫或边界交出 | type_profile、visual_unit_function | `N3-MATCH` | 类型能覆盖主要字段，且不会把非画面字段误判为视觉任务 |
| `N3-MATCH` | 执行 step1 画面匹配 | `references/visual-matching-contract.md`、正文行 | 找出所有 visual_unit，记录场景锚点和匹配理由 | visual_unit list | `N4-BEAT` | 命中行覆盖画面性字段 |
| `N4-BEAT` | 执行 step2 节拍分析 | visual_unit、`references/beat-analysis-contract.md` | 判断节拍点和分镜数量；禁止把 2 镜当默认值 | beat_map | `N5-RHYTHM` | 每个 visual_unit 至少 1 个节拍点；每个候选 `分镜2` 有第二个真实观看策略 |
| `N5-RHYTHM` | 执行 step2.5 画面节奏分析 | visual_unit、beat_map、上下文密度、`references/visual-rhythm-analysis-contract.md` | 判断收敛/发散、描述密度、运动复杂度、边界清晰度，并校准 1/2/3/4 镜是否匹配信息重要性 | rhythm_profile | `N5.5-PEAK-SHOT` | 当前画面有张弛策略；低信息不硬撑 2 镜，关键信息不被压平为 2 镜 |
| `N5.5-PEAK-SHOT` | 执行 step2.6 高点与余波策略 | visual_unit、beat_map、rhythm_profile、上游 `peak_visual_policy` 或高点证据、`references/peak-shot-language-contract.md` | 识别 `peak_visual_unit`，决定分镜密度、镜头运动、景别尺度、停顿/断裂、反应镜头和余波交出点 | peak_shot_profile | `N5.6-ADVISOR` | 高点强化可回指上游，不新增事实 |
| `N5.6-ADVISOR` | subagents 摄影监制参谋汇流 | `team.yaml`、共享顾问合同、当前 `PASS-CINE-*` / `N*-*` 节点、visual_unit、beat_map、rhythm_profile、peak_shot_profile、项目 `MEMORY.md`、`north_star.yaml` 与相关 `CONTEXT/` | 启动或按阻断报告处理 team.yaml 中明确的监制组相关智能顾问团；主 agent 从当前思维·执行节点的 input、judgment、action、evidence、gate 和 rework target 派生顾问问题，要求顾问代入角色意识、创作风格和专业水准提出参谋指导；主 agent 汇流为后续任务上下文 | `advisor_consultation_packet` 或降级报告 | `N6-CONTINUITY` | packet 已包含 roster 来源、node/pass 来源、角色视角、可执行指导、风险提示和 `execution_brief` |
| `N6-CONTINUITY` | 回看临近分镜明细并建立连续性与空间语法 | rhythm_profile、peak_shot_profile、`advisor_consultation_packet`、前 3 个 visual_unit、`references/shot-continuity-contract.md` | 建立轴线、运动方向、景别梯度、景深/焦点、光色母题、空间位置和注意力交接策略，并吸收顾问参谋但不改写上游原文 | continuity_profile | `N6.1-HANDOFF` | 当前镜头有进入点、空间轴线、变化动机和交出点 |
| `N6.1-HANDOFF` | 判断边界交出点与进入提示 | visual_unit、type_profile、rhythm_profile、continuity_profile、场景/空间/时间/叙事段落变化、`references/transition-design-contract.md` | 场景变化或边界风险只形成 `handoff_profile`；记录可见交出锚点、进入提示和连续性风险，不裁决普通切镜、软桥接、匹配剪辑或高能转场方案 | handoff_profile | `N6.2-CAMERA-GRAMMAR` | 场景变化有交出点和进入提示；没有在本阶段落盘创意转场方案 |
| `N6.2-CAMERA-GRAMMAR` | 选择摄影语法与变化梯度 | visual_unit、type_profile、beat_map、rhythm_profile、peak_shot_profile、continuity_profile、handoff_profile、`references/cinematic-technique-library.md`、`references/dynamic-lens-language-contract.md` | 为每个 beat 选择最小充分的景别/景深、镜头视角、镜头类型、构图、光影、色彩、运镜方式、速度曲线和停点；明确哪些变化延续、哪些变化重置、哪些变化必须显式写 | camera_grammar_plan | `N6.4-FUNCTIONAL-PROJECTION` | 技法选择服务节拍、空间、信息、情绪或边界交出，不随机换景别/视角/镜头类型 |
| `N6.4-FUNCTIONAL-PROJECTION` | 建立功能性影视投影与下游 payload | camera_grammar_plan、beat_map、continuity_profile、handoff_profile、`references/functional-cinematic-projection-contract.md`、下游图像/视频消费要求 | 为每个计划分镜锁定影视功能、可见主体、动作相位、运镜计划、构图锚点、光色/材质、空间接口、连续性交接、交出锚点和 AIGC 下游消费点 | functional_projection_plan | `N6.5-SHOT-PLAN` | 每个候选分镜能指导生图和视频；删掉后会损失明确观看信息 |
| `N6.5-SHOT-PLAN` | 汇流 references 形成逐分镜计划 | visual_unit、type_profile、beat_map、rhythm_profile、peak_shot_profile、continuity_profile、handoff_profile、camera_grammar_plan、functional_projection_plan、`advisor_consultation_packet`、`references/shot-planning-integration-contract.md`、动态运镜合同、自然成稿合同 | 为每个 visual_unit 形成内部 `shot_design_plan`；裁决分镜数量、顺序、入口、运镜路径、速度曲线、停点、落点、边界交出锚点、摄影语法、显式参数取舍、功能 payload 和交出点；删除没有新观看策略或下游消费价值的随机分镜 | shot_design_plan | `N7-INJECT` | 每个计划分镜可回指 beat/rhythm/continuity/handoff/camera/function/downstream/naturalness |
| `N7-INJECT` | 执行 step3 运镜摄影设计注入 | `shot_design_plan`、`advisor_consultation_packet`、`references/functional-cinematic-projection-contract.md`、`references/dynamic-lens-language-contract.md`、`references/cinematic-technique-library.md`、`references/natural-shot-detail-writing-contract.md` | LLM 直写 `分镜明细：` 与 `分镜N`，严格投影 `shot_design_plan`，把参数压成自然画面文字，吸收顾问参谋上下文但不改写上游真源；字段内容不得输出抽象主题、心理结论、世界观解释、导演阐释、不可执行气氛口号、随机好看句、参数清单或模板句法 | enriched episode draft | `N8-REVIEW` | 原文保留，注入块紧跟命中句子；字段语义纯度、摄影语法变化、功能性投影和自然成稿通过；每个分镜能反推出起点、运镜路径、速度、停点、落点、动机、交出点和下游消费 payload；顾问上下文未越权 |
| `N8-REVIEW` | 执行质量与机械门禁 | candidate enriched draft、`review/review-contract.md`、可选 validator | 检查覆盖、连续编号、节奏张弛、摄影语法变化、shot_design_plan 投影、功能性投影、连续性、保真、专业性和自然成稿，定位 repair target | review result、repair targets | `N8R-DIRECT-REPAIR` 或 `N9-WRITE` | 无阻断项才可写回 |
| `N8R-DIRECT-REPAIR` | 阶段内直接修复阻断项 | repair targets、candidate enriched draft、上游编导稿 | 最小修复 `分镜明细`、`分镜N`、连续性、节奏张弛、峰值分镜、专业可执行或报告证据；不改上游原文 | repaired draft、repair actions | `N8R-REVIEW-AGAIN` | 修复范围不越权 |
| `N8R-REVIEW-AGAIN` | 复审修复稿 | repaired draft、repair actions、上游编导稿 | 复跑阻断 gate；通过则准入写回，失败则回最早责任节点 | re-review verdict | `N9-WRITE` 或 `N3/N4/N5/N5.5/N6/N7/N8R` | 复审通过或明确阻断 |
| `N9-WRITE` | 落盘与报告 | enriched draft、review result | 写入 `3-摄影/第N集.md`，更新报告 | output path、report path | done | 路径和命名符合 Output Contract |

## Branch Rules

- `N3-MATCH` 中标签命中和语义命中可以并行思考，但必须汇总为单一 visual_unit list。
- `N4-BEAT` 先给每个 visual_unit 独立判断，不允许跨句共用分镜编号，也不允许把上一条或模板中的 2 镜结构继承为默认数量。
- `N5-RHYTHM` 必须判断当前画面句子该收敛还是发散；不允许所有画面句子同等华丽。
- `N5-RHYTHM` 必须执行数量分布警戒：同一集或同一场出现 2 镜绝对集中时，抽样回查低信息、关键显影、群像和高点块，修正被硬撑或压平的分镜数。
- `N5.5-PEAK-SHOT` 只强化上游已有高点或明显 `micro_payoff`，不得把普通画面硬拔成高潮；强化必须体现为分镜密度、运镜速度、景别尺度、停顿、反应镜头或余波交出点的有动机变化。
- 若启动 subagents 模式，`N5.6-ADVISOR` 必须在 `N6-CONTINUITY` 和 `N7-INJECT` 前完成；顾问问题必须同步于当前思维·执行节点，顾问参谋只转化为 `advisor_consultation_packet` 上下文，不直接写分镜明细，不替换上游事实、对白或场景顺序。
- `N6-CONTINUITY` 必须回看临近至少前 3 个画面单位；不足 3 个时回看已有全部单位并建立本场景的初始轴线、运动方向、景别梯度、景深/焦点逻辑和光色母题。
- `N6.1-HANDOFF` 必须把场景变化视为边界风险并形成 `handoff_profile`；普通场景变化也至少要有上一画面交出点和下一画面进入提示，不得让下一场景凭空开始。
- `N6.1-HANDOFF` 不得把场景变化升级为创意转场；形态、动作、声音、光线、颜色、文字或高点余波只作为可见交出锚点记录，连接方式由 `4-分组` 裁决。
- `N6.2-CAMERA-GRAMMAR` 必须把景别、景深/焦点、镜头视角、镜头类型、构图、光影、色彩、运镜方式和速度变化作为一套摄影语法裁决；不得只在成稿阶段临时挑“特写/推近/俯拍”等孤立词。
- `N6.2-CAMERA-GRAMMAR` 的变化必须有动机：远景建立、中景调度、近景加压、特写揭示；视角变化必须服务权力关系、主观发现、空间重置、观察关系或信息显影。
- `N6.4-FUNCTIONAL-PROJECTION` 必须把每个候选分镜投影为主体、动作相位、运镜计划、构图锚点、光色/材质、空间接口、连续性交接和下游消费点；缺少关键 payload 的候选分镜不得进入 `shot_design_plan`。
- `N6.5-SHOT-PLAN` 是 references 进入最终输出的硬门：不得跳过；分镜数量增加必须来自新的注意力、信息、动作相位、空间关系、情绪压力、摄影语法变化、运镜策略或边界交出锚点。
- `N6.5-SHOT-PLAN` 必须显式形成内部 `shot_count_decision`：先证明 1 镜是否足够，再证明 2 镜是否有第二个真实观看策略，最后只在关键揭示、群像扩散、动作分相、空间重置或高点承托时扩展到 3-4 镜。
- `N6.5-SHOT-PLAN` 必须保证同一 `visual_unit` 内相邻分镜首尾相接：上一条的落点必须成为下一条的入口、反应、动作、声音、光色、焦点、运镜变化或交出锚点。
- `N7-INJECT` 的技法选择可同时参考构图、运镜、边界交出、光影、色彩，但最终输出必须凝成可执行、连贯、张弛得当的自然分镜句；不要把内部参数逐项摊开。
- 若 `N7-INJECT` 把 `分镜明细：` 写成抽象阐释，必须回退：把抽象判断翻译为可见的景别、机位、镜头类型、运镜速度、焦点、构图、光影、色彩或交出锚点；无法转译的内容删除。
- 若 `N7-INJECT` 输出太简略，无法反推起点、路径、速度、落点、动机或交出点，必须回到 `N6.5-SHOT-PLAN` 重建计划后再写。
- 若 `N7-INJECT` 输出连续同构、参数堆叠或模板填空腔，必须回到 `references/natural-shot-detail-writing-contract.md` 重写成自然中文；不得只替换形容词。
- 若 `N7-INJECT` 输出看起来顺但无法抽取主体、动作相位、运镜计划、构图锚点、光色材质或下游消费点，必须回到 `references/functional-cinematic-projection-contract.md` 和 `N6.5-SHOT-PLAN`，不得靠润色解决。
- 若 `N7-INJECT` 缺少景别/视角/景深/焦点/镜头类型的变化逻辑，或相邻镜头只是随机换技法，必须回到 `N6.2-CAMERA-GRAMMAR`；不得在成稿里补几个摄影词冒充专业性。
- 任一节点发现需要改写剧情或对白才能成立，必须回退：分镜明细应服务原句，而不是修补原句。
- 若 review 发现 subagents 启用但缺 `team.yaml` 监制顾问请教、节点同步问题、角色意识/创作风格/专业水准参谋或上下文沉淀，回到 `N5.6-ADVISOR`。
- 若 review 发现上游高点被压平，回到 `N5.5-PEAK-SHOT`；若发现高潮强化导致跳轴、跳色或风格断裂，继续回到 `N6-CONTINUITY`。
- 若 review 发现场景变化没有交出点/进入提示，或把创意转场方案落在 `3-摄影`，回到 `N6.1-HANDOFF` 和 `N6.5-SHOT-PLAN`。
- 若 review 发现分镜随机、上下衔接差、数量多但无递进、摄影语法随机、功能 payload 缺失、输出过短或 references 未真实汇流，按责任回到 `N6.2-CAMERA-GRAMMAR`、`N6.4-FUNCTIONAL-PROJECTION` 或 `N6.5-SHOT-PLAN`。
- 若 review 发现可由本阶段修复的覆盖、编号、节拍、张弛、计划汇流、连续性或专业性问题，先进入 `N8R-DIRECT-REPAIR` 并复审；不得跳过复审写回。

## Output Shape Per Visual Unit

```markdown
动作画面：林寂猛地睁开眼，身体在座位上僵住，视线从白光里落回现实。
分镜明细：
分镜1: 白光还压在林寂的瞳孔里，镜头慢慢贴近他僵住的眼角；过曝退下去时，焦点刚好落在重新合上的视线。
分镜2: 画面从他的眼神退到肩膀和课桌边，轻微手持让身体的僵硬露出来，最后把视线留给教室前方。
```

不同画面句子的 `分镜N` 均从 `分镜1` 重新编号。
上例是两段观看策略同时存在时的示例，不是固定两镜模板；低信息或单一反应块可以只有 `分镜1`，关键显影、群像扩散、动作分相或高点承托可按真实节拍扩展到 `分镜3` / `分镜4`。
