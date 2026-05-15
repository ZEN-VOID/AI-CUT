# Visual Rhythm Analysis Contract

本文件定义 step2.5“画面节奏分析”。节拍分析决定“切换点在哪里”，画面节奏分析决定“分镜明细写多满、多快、多炫、多克制”。目标是让不同类型、不同节奏、不同信息重要性的画面句子张弛有度，该收敛的收敛，该发散的发散。每个分镜的具体时值由 `shot-duration-decision-contract.md` 继续裁决；本文件只提供节奏画像，不替代单镜长短判断。

## Core Rule

每个画面句子在注入分镜明细前必须生成 `rhythm_profile`。它决定：

| rhythm_dimension | decision |
| --- | --- |
| `importance_level` | low / medium / high / critical |
| `tempo` | hold / slow_burn / steady / quick / rupture |
| `density` | sparse / measured / rich / maximal |
| `movement_complexity` | static / single_move / combo_move / rupture_move |
| `description_scope` | one-line concise / standard / expanded / set-piece |
| `boundary_clarity` | none / local_handoff / scene_boundary / group_boundary_candidate |
| `peak_emphasis` | none / restrained_peak / expanded_peak / rupture_peak |

`rhythm_profile` 还必须承担分镜数量去模板化职责：当 `beat_map` 倾向输出 2 镜时，先判断当前画面是否真的需要“起点/揭示”“动作/反应”“空间/压力源”两段观看；如果只是一个单一观看动作，收敛为 1 镜；如果是关键揭示、动作分相、群像扩散或高点承托，不得被压平为 2 镜。

`rhythm_profile` 不能只停留在“快/慢/满/空”的模糊标签。进入 `shot_duration_decision` 前，必须给出时值倾向：哪些镜头需要快速通过，哪些镜头需要读秒，哪些镜头需要表演停顿，哪些镜头必须按短剧·AIGC 节奏压缩以保护 15 秒分组节奏，哪些镜头因对白/旁白台词量形成最低时长。

当上游已形成 `sequence_density_curve` 时，`rhythm_profile` 必须消费其 `tempo_beats / density_ramp / peak_slots / recovery_slots / set_piece_chain_slots / sound_cut_pattern / density_budget`。单句节奏不能和段落变速曲线脱节：位于 `conserve` 或 `recovery` 槽位的画面优先收敛，位于 `burst`、`peak_slot` 或 `set_piece_chain_slot` 的画面可加密，但必须逐镜证明新的观看策略和结果落点。

## Rhythm Profile Matrix

| visual_unit_type | information importance | rhythm choice | shot detail behavior |
| --- | --- | --- | --- |
| 过场动作 | low | 收敛 | 1 个分镜，单一运动或固定机位，参数准确但不铺陈 |
| 空间建立 | medium/high | 标准展开 | 1-2 个分镜，交代轴线、空间压力和视觉母题 |
| 关键规则/系统显影 | high/critical | 发散强化 | 2-4 个分镜，文字可读、角色反应、光色、焦点变化或交出点清楚 |
| 道具异常 | high | 精准发散 | 微距/特写 + 反应承接，强调材质、颜色、危险信息 |
| 表演微反应 | medium/high | 收敛加压 | 少动或极慢动，景深收窄，留停顿，不用复杂炫技盖住表演 |
| 群像混乱 | medium/high | 节奏扩散 | 2-4 个分镜，寻找恐惧传播路径，不平铺所有人 |
| 场景变化 | medium/high | 交接展开 | 1-2 个分镜，至少处理上一场景交出点和下一场景进入点；除非有强接口，不硬做高能 |
| 高能入场/惊吓 | critical | 断裂式发散 | 快速运动、急停、声画桥或光变，但要给落点 |
| 低信息对白画面 | low/medium | 克制承托 | 1 个反应或关系镜头，避免每句对白都炫技 |
| 上游高潮/爽点/高光承托 | high/critical | 峰值强化 | 按 `peak-shot-language-contract.md` 判断是停顿、扩展还是断裂，不一律更快或更多 |
| set-piece 链条 / 连续声画打点 | critical | 峰值密度爆发后恢复 | 5-6 镜例外只在连续动作结果或一声一结果真实存在时成立；高密度后必须接反应、反压或交出 |

## Decision Procedure

1. 先判断当前画面句子的叙事权重：是否带来新信息、新危险、新关系、新空间或新情绪峰值。
2. 再判断当前上下文节奏：上一组镜头是否已经高密度、高运动、高转场；若是，当前可适当收敛。
3. 若存在 `sequence_density_curve`，判断当前画面落在整段哪个速度槽位；不得让全段同密度、全满、全空或没有峰值/恢复。
4. 判断观众是否需要停顿读信息：规则文字、道具细节、微表情需要留读秒，不应被高速运动带走；但普通氛围、过场动作和常规反应默认压缩，不沿用传统影视宽停顿。
5. 判断是否需要发散：关键揭示、空间重置、情绪峰值、威胁入场可提高分镜数量和动态复杂度。
6. 若发生场景变化，固定标记边界风险并交给 `references/transition-design-contract.md` 形成 `handoff_profile`；本阶段只记录交出锚点、进入提示和连续性风险，不裁决连接方式。
7. 若画面承载上游高潮/爽点/高光成分，先标记 `peak_emphasis`，再交给 `references/peak-shot-language-contract.md` 裁定具体峰值镜头策略。
8. 若画面命中 `set_piece_chain_slot` 或 `sound_cut_pattern`，允许 5-6 镜例外，但必须逐镜执行删减测试：删掉任一镜是否会少一个必要动作结果、声音打点、反应或交出接口。
9. 形成内部 `rhythm_profile` 后，交给 `references/shot-duration-decision-contract.md` 生成每个计划分镜的 `shot_duration_decision` 和正文 `display_seconds`；没有短剧·AIGC 压缩复判和时值裁决，不得直接写 `分镜N（约X秒）`。
10. `rhythm_profile` 不显式输出，只通过描述密度、运动复杂度、边界清晰度、时值分配和停顿感体现在成稿中。
11. 对批量输出做分布抽查：若同一集或同一场中 2 镜块占比异常集中、连续多镜时值等级相同，或段落没有 `density_curve_summary`，回到低信息、关键显影、群像、高点和 set-piece 样本复判，证明每个 `分镜2`、高密度链条和长停顿都有真实节拍，或删并/扩展/压缩到正确数量与时值。

## Convergence Rules

以下情况应收敛：

- 画面只是承接动作，信息量低。
- 上一镜头已经强运动、强转场、强光色变化。
- 演员表演需要观众停住看。
- 文字或道具需要清楚可读。
- 画面功能是让观众恢复空间方向。

收敛不是平庸，而是精准：少分镜、少运动、清楚落点、保留呼吸。

## Expansion Rules

以下情况可发散：

- 第一次出现关键规则、系统信息或隐藏真相。
- 角色第一次发现危险、能力或关系变化。
- 空间结构需要重新建立。
- 危险源入场、惩罚发生、群体恐慌扩散。
- 需要把上一组镜头的压抑释放成视觉爆点或清楚的余波交出点。
- 上游已经存在明确高点，且普通节奏会削弱行动结果、认知震荡、关系暖点、规则压迫或奇观冲击。
- 当前段落的 `sequence_density_curve` 已把该画面标为 `peak_slot` 或 `set_piece_chain_slot`，且新增镜头能提供独立结果或声音打点。

发散不是堆满参数，而是让信息、情绪和运动同时升级。

## Output Guidance

| profile | recommended output |
| --- | --- |
| `sparse + static` | `分镜1` 一句完成，固定机位或极慢推拉，强调落点 |
| `measured + single_move` | `分镜1` 或 `分镜1-2`，一个清楚运动从 A 到 B |
| `rich + combo_move` | `分镜1-4`，组合运镜、焦点/景别变化、反应承接或交出点 |
| `maximal + rupture_move` | `分镜1-4`，断裂节奏或强余波交出点，但必须给空间/反应落点 |
| `peak_emphasis + selected_move` | 先按 `peak_shot_profile` 决定停顿、扩展或断裂，再写入 `分镜N`；高点也可以用静止长镜完成 |
| `set_piece_chain + sound_cut_pattern` | 可扩展到 `分镜1-5/6`，每镜短促但必须一声一结果；链条后需要恢复、反压或交出 |

`profile` 标签仅用于内部判断，不写入 `分镜N`。输出应直接进入当前画面的镜头运动。
具体单镜时值继续按 `shot-duration-decision-contract.md` 形成 `instant / short / standard / held / long_hold` 裁决；短剧·AIGC 模式下优先让镜头在 `short / standard` 内成立，最终通过句子密度、运动速度、停点和读秒感体现。

## Anti-Patterns

- 每条画面句子都写成长段大师炫技。
- 每条画面句子都写成 2 个分镜，导致低信息画面被硬撑、关键画面被压平。
- 只看单句节奏，不看整段 `sequence_density_curve`，导致全场没有变速曲线。
- 把 5-6 镜链条当成新的固定爽点模板，而不是连续动作/声音结果的例外。
- 关键规则显影只写一句“特写规则文字”，没有读秒、反应和光色层次。
- 低信息动作写 3-4 个分镜，拖慢节奏。
- 强表演瞬间用复杂运镜抢走演员。
- 连续多个高密度画面没有收束，导致整集只有“满”没有呼吸。
