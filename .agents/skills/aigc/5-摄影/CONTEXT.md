# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/5-摄影` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

- soft_limit_chars: 22000
- hard_limit_chars: 44000
- status: ok
- last_checked_at: 2026-05-13
- current_chars_checked_at_last_review: 19800
- action_needed: 已完成压缩；Type Map 精简、Repair Playbook 合并、Reusable Heuristics 中已正式化条目移除、项目特定内容迁移到 knowledge-base。后续若新增经验条目超限，优先将通用经验迁移到 `knowledge-base/cinematography-heuristics.md`。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | verification |
| --- | --- | --- | --- |
| 漏掉画面性字段 | 画面匹配层 | 回到标签+语义双重匹配，补齐微表情/呼吸/姿态/视线/手部动作命中行 | `visual-matching-contract.md` 固定双入口；随机抽查命中行就近有 `分镜明细：` |
| 非画面字段被滥加分镜明细 | 字段纯度层 | 删除对白/音效/心理反应下的分镜明细，除非行内有明确画面承托 | `types/` 区分 visual/audio-visual/non-visual |
| 分镜数量机械固定 | 节拍判断层 | 按注意力转移/动作相位/信息揭示/情绪转折切分 | `beat-analysis-contract.md`；同类句子分镜数可不同 |
| 分镜数量塌缩为固定 2 镜 | 节拍/模板诱导层 | 回到 `beat_map -> rhythm_profile -> shot_count_decision`；低信息合并，关键块扩展 | `shot-planning-integration-contract.md`；抽样 `分镜2` 须有真实第二观看策略 |
| 分镜明细张弛失衡 | 画面节奏层 | 内部先判 `rhythm_profile`，低信息收敛、关键信息发散 | `visual-rhythm-analysis-contract.md`；整集有呼吸 |
| 整场节奏无变速 | 段落密度曲线层 | 回到 `sequence-density-curve-contract.md`，先建 `sequence_density_curve` 再进入单句 `beat_map` | `N3.6-DENSITY-CURVE`；整段能说清哪里省/爆/停/交出 |
| 分镜切点正确但长短失衡 | 镜头时值层 | 回到 `shot-duration-decision-contract.md`，补 `shot_duration_decision` | `N5.2-DURATION`；文字/道具/微表情有可读时间 |
| 终稿缺少显式秒数 | 落盘投影层 | 每条 `分镜N:` 改为 `分镜N（约X秒）:` | 模板/validator 固定格式 |
| 对白台词量未进入镜头时值 | 声画时值层 | 先估算对白字数/语速/停顿，合并 `dialogue_seconds_floor` | `N5.2-DURATION`；台词不会没说完就切走 |
| 场景母题尾句机械灌入每条分镜 | 计划汇流/复审层 | 删除重复尾句，只在建立镜/转场镜/母题变化处保留 | review gate 增加重复句抽查 |
| 字段内容纯度不足 | 字段语义层 | 删除抽象主题/心理结论/世界观解释/气氛口号，转译为景别/机位/镜头类型/运速/焦点/构图/光色；无法转译则删除 | `SKILL.md` + `natural-shot-detail-writing-contract.md`；`cinematic-technique-library.md` 补执行参数 |
| 字段表达质量不足 | 动态表达层/自然成稿层 | 静态呆板改为"从起点到终点"变化句；参数腔/模板腔压成自然画面文字 | `dynamic-lens-language-contract.md` + `natural-shot-detail-writing-contract.md`；禁止连续同构句 |
| 分镜明细好看但功能随机 | 功能性投影层 | 回到 `functional-cinematic-projection-contract.md`，补 shot_function/主体/动作/运镜/构图/光色/空间/交接 | `N6.4-FUNCTIONAL-PROJECTION`；下游能抽取完整 payload |
| 分镜明细不适合视频生成 | AI 视频执行层 | 动作改成被镜头包裹，补方向参照，光源词改成亮暗/阴影/轮廓结果 | `ai-video-prompt-execution-contract.md` + `GATE-CINE-15A` |
| 段落运镜流畅但画面点失主 | 段落对齐/归属边界层 | 回到 `visual-sequence-alignment-contract.md`，补 `unit_ownership_map` | `N3.5-SEQUENCE-ALIGN`；每条 `分镜N` 能回指所属 `visual_unit` |
| 景别/视角/焦点变化随机 | 摄影语法层 | 回到 `N6.2-CAMERA-GRAMMAR`，先确定景别梯度/视角动机/景深焦点交接 | `cinematic-technique-library.md` + `GATE-CINE-16` |
| references 细则未进入最终分镜 | 计划汇流层 | 回到 `N6.5-SHOT-PLAN`，先建 `shot_design_plan` 再写 `分镜N` | `shot-planning-integration-contract.md` |
| 分镜数量多但随机 | 节拍计划层 | 删掉没有新观看策略的伪分镜 | `shot_design_plan.beats` 必须逐条说明 trigger/handoff |
| 上下镜衔接差 | 交出点层 | 上一分镜终点成为下一分镜入口 | `intra_unit_handoff` 和 `next_handoff` 为必填项 |
| 镜头断裂跳跃 | 连续性层 | 回看前 3 个画面单位，修正轴线/运动方向/景别梯度 | `shot-continuity-contract.md` |
| 高潮画面被压平 | 峰值分镜层 | 回到 `peak-shot-language-contract.md`，补 `peak_shot_profile` | 高点镜头有停顿/断裂/扩展策略 |
| 场景变化没有交出锚点 | 边界交出层 | 回到 `transition-design-contract.md`，补 `handoff_profile` | 下一场景不是凭空开始 |
| subagents 未请教监制 | 顾问请教层 | 回到 `team.yaml` + 共享顾问合同，按节点派生问题 | 执行报告有 roster/降级说明 |
| 顾问只给泛泛评价 | 顾问问题质量层 | 重新基于当前节点提问，输出必须可转为 `must_do/must_not_do/execution_brief` | packet 中每条意见能回指 node/pass/gate |
| 炫技盖过剧情 | 戏剧服务层 | 删除不服务信息/情绪/空间关系的运动和转场 | review gate "技术必须服务戏剧任务" |
| 改写了 4-表演 原文 | 保真层 | 恢复上游原句，只保留下方新增分镜明细块 | diff 中除 frontmatter 和分镜明细外无正文改写 |
| 创意转场滥用 | 阶段归属层 | 删除 3-摄影 中的转场方案，只保留交出锚点 | `6-分组` 再设计连接件 |

## Repair Playbook

1. 先锁定 `source_directing_path`，确认输出对应的上游 `4-表演/第N集.md`。
2. 抽取 `【剧本正文】` 后正文，建立画面性字段清单：标签命中优先，语义命中补充。
3. 对每个画面句子做节拍复判：主体变化、动作分相、信息揭示、情绪反转、视线/呼吸/微表情转移。
4. 对每个画面句子做画面节奏复判：信息重要性、上下文密度、情绪压力和收敛/发散倾向。
5. 对每个候选分镜做时值复判：先估算对白/旁白字数和台词量下限，再判断缩短一半丢失什么、拉长一倍是否只是拖慢；落盘必须是 `分镜N（约X秒）:`。
6. 对上游已有高点执行峰值分镜复判：行动结果看钉镜，认知翻转看读秒，关系暖点看温柔停顿，规则/恐怖看断裂入侵。
7. 若启用 subagents，先把 `team.yaml` 监制顾问团作为摄影监制请教；问题从当前节点派生，输出必须可转为 `must_do/must_not_do/execution_brief`。
8. 分镜过少时查找被压成一镜的动作相位或信息揭示；分镜过多时合并没有新观看策略的切点。
9. 若大面积都是 2 镜，抽样低信息/过场/表演停顿/关键显影/群像/高点块，逐条追问 `分镜2` 删除会少什么。
10. 若多镜数量合理但观看别扭，按时值问题处理：快速镜是否带走该读的信息，长镜是否只有气氛。
11. 若连续 3-6 个画面单位共享空间/道具链/声音链/动作链/记忆插入/视觉母题，先建立内部 `sequence_profile`，同步写清 `unit_ownership_map`。
12. 若连续观看段落存在速度阶段/动作链/声音打点/峰值爆发，先建立 `sequence_density_curve`。
13. 在写任何 `分镜N` 前先走完节点链：`N2-MATCH -> N3-TYPE -> N3.5-SEQUENCE-ALIGN -> N3.6-DENSITY-CURVE -> N4-BEAT -> N5-RHYTHM -> N5.2-DURATION -> N5.5-PEAK-SHOT -> N5.6-ADVISOR -> N6-CONTINUITY -> N6.1-HANDOFF -> N6.2-CAMERA-GRAMMAR -> N6.4-FUNCTIONAL-PROJECTION -> N6.5-SHOT-PLAN`；缺任一层都不能直接成稿。
14. 在 `camera_grammar_plan` 中先裁决景别梯度/镜头视角/景深焦点/镜头类型/构图/光色/运镜速度；不要到成稿阶段临时补孤立词。
15. 在 `functional_projection_plan` 中补 payload：每条分镜必须有影视功能/主体/动作/运镜/时值理由/构图锚点/光色材质/空间接口/连续性交接/下游消费点/所属 visual_unit。
16. 做 AI 视频执行稳定性检查：动作是否被镜头包裹、方向是否有参照、光线是否写出亮暗面结果、表演是否落到微动态。
17. 检查多分镜递进：上一镜落点必须成为下一镜入口；每条都像重新开始则回到连续性和计划汇流层。
18. 若发生场景变化，检查 `handoff_profile`：上一画面从哪里交出，下一画面从哪里进入。
19. 检查每个 `分镜明细：` 是否包含可执行摄影信息；空泛词和抽象阐释改成景别/机位/镜头类型/运速/焦点/构图/光色/色彩/转场。
20. 把 `分镜明细：` 当作兼容字段名；凡出现主题寓意/心理结论/世界观解释/导演阐释/不可执行气氛口号，必须转译为可见运镜或摄影美学，无法转译则删除。
21. 检查每个 `分镜N` 是否动态：起点、运镜、速度变化、停点、落点。
22. 检查连续分镜是否句法同构：若多条都像"从……以……变化到……最终……"，必须参数内化为画面。
23. 检查连续性：内部回看前 3 个画面单位，只有跳变时才短写承接动机。
24. 光影和色彩必须与项目视觉母题绑定；具体母题参见 `knowledge-base/cinematography-heuristics.md`。
25. 若分镜明细改变剧情理解，回到保真层：原字段只提供事实，分镜明细只能强化观看路径。
26. 最后做一次机械检查：覆盖率、连续编号、输出路径、分镜数量分布、显式秒数、逐画面点归属和 AI 视频执行稳定性。
27. 交付前把 review finding 当成修复输入；阻断项先在本阶段修复并复审，仍失败再阻断。

## Reusable Heuristics

- 一个短句也可能有多个分镜：例如"门被推开"可以拆成门缝、手、反应、主体入场；一个长环境句也可能只需要一镜，如果注意力没有转移。
- 恐怖校园题材的分镜明细要让秩序变成压迫：横平竖直的课桌、封死的窗帘、冷白灯、黑板字、红色道具都应成为构图武器。
- 高超运镜不是镜头一直动，而是镜头在观众意识到之前已经把注意力转交给下一个危险点。
- 边界交出最适合寻找形态相似、运动方向相同、声音余波或信息显影的地方；不适合覆盖需要演员表演停顿的瞬间。
- 高潮分镜不是每次都加速加镜头；认知高点常用读秒，关系高点常用停顿，动作高点才更常用急停、跟拍和结果钉镜。
- 一个好用的分镜句式是"景别/景深 + 视角 + 镜头类型 + 运镜速度 + 戏剧动作"：例如"中近景、浅景深、过肩窥视视角、长焦压缩、极慢推轨到林寂停住的手指"。
- 上一句只适合内部计划，不适合连续成稿。最终优先写成："长焦压扁后排课桌，镜头慢慢贴近林寂停住的手指。"
- 更好的成稿要保留变化但不露骨架："长焦压扁后排课桌，镜头慢慢贴近林寂停住的手指；背景黑板字退成一片冷白。"
- 输出太短通常不是"克制"，而是缺计划：克制分镜也要有清楚入口、运动方式、速度、落点和交出点。
- 最稳的连续性做法是"内部承接上一镜落点"：先在判断中确认上一镜的焦点、声音、动作或光色，再把输出集中写成当前镜头的变化；只有跳变时才短写承接动机。
- 节奏张弛的判断要先于炫技：低信息动作精准一句足够，关键显影可以多分镜铺开，强表演瞬间宁可让镜头停住也不要抢戏。
- "这条分镜服务哪一句原文？"是归属检查的最低门槛。