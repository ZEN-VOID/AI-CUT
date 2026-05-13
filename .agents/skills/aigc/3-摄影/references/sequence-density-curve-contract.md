# Sequence Density Curve Contract

本文件定义 `3-摄影` 的段落级分镜密度曲线机制。它不替代 `visual-sequence-alignment-contract.md` 的逐画面点归属，也不替代 `beat-analysis-contract.md` 对单个 `visual_unit` 的节拍判断；它负责在相邻画面单位进入逐句分镜前，先判断整段观看节奏应该如何变速：哪里省镜头，哪里加密，哪里停顿，哪里硬切，哪里交出给下游。

## Core Rule

每当相邻 `visual_unit` 构成一个连续观看段落，必须先形成内部 `sequence_density_curve`。该曲线只约束分镜密度、时值倾向、峰值槽位、恢复槽位和交出锚点；最终落盘仍按正上方画面句子逐点写 `分镜明细：`，不得把多个画面句子合并成一条失主镜头。

判断标准不是“这一句能不能多写几镜”，而是：

> 整段观看需要怎样的速度变化，才能让低信息处不拖、关键处不薄、高点处有爆发、爆发后有反压或余波？

## Activation Signals

命中以下任一情况时，必须建立 `sequence_density_curve`：

- 相邻 3-8 个 `visual_unit` 共享同一空间、动作链、道具链、声音链、光色母题或危险推进。
- 上游段落存在明显速度阶段，例如日常建立 -> 威胁入场 -> 动作爆点 -> 后果反压 -> 边界交出。
- 某个 `visual_unit` 可能需要 5-6 个短镜承托连续动作结果、连续命中、连续声画打点或 set-piece 链条。
- 同一场中 `shot_count_distribution` 呈现固定 2 镜、平均铺满、连续高密度或连续低密度风险。
- 启动 subagents 摄影监制顾问时，顾问建议给出段落变速、密度槽位、动作峰值或恢复停顿。

## Curve Fields

| field | meaning |
| --- | --- |
| `segment_span` | 当前曲线覆盖的相邻 `visual_unit` 范围与场景锚点 |
| `tempo_beats` | 段落级速度阶段，例如 `sweet_setup -> comic_lift -> threat_pressure -> action_burst -> consequence_hold -> boundary_handoff` |
| `density_ramp` | 每个阶段的分镜密度倾向：`conserve / measured / build / burst / hold / release` |
| `peak_slots` | 可加密的峰值槽位；必须说明峰值证据和允许的最高分镜数 |
| `recovery_slots` | 爆点后需要停住、反压、读秒或普通人反应的槽位 |
| `set_piece_chain_slots` | 允许 5-6 镜的连续动作/声画打点槽位；必须逐镜有独立起点、撞点、结果和节奏声 |
| `sound_cut_pattern` | 鼓点、拟声、骨哨、海螺号、骤停等声音是否决定镜头切点 |
| `density_budget` | 本段整体分镜预算与分布目标，避免全段平均同密度 |
| `handoff_anchors` | 段落末尾交给下游或下一段的可见锚点 |
| `ownership_guard` | 哪些动作、对白反应、记忆段、道具揭示或转场方案不得跨 `visual_unit` 外溢 |

## Tempo Archetypes

| archetype | use when | density pattern |
| --- | --- | --- |
| `daily-flow-to-threat` | 日常关系被危险侵入 | 日常段流动少切，威胁入场快速加密，威胁结果给停顿 |
| `comic-to-violence-snap` | 喜剧动作突然转为真实危险 | 笑点可短促，暴力或威胁切点硬停，后果反压 |
| `set-piece-chain` | 连续命中、连续反弹、连续物件结果或声画五拍 | 允许 5-6 个短镜，但每镜必须一击一结果，不许随机堆切 |
| `crowd-to-command` | 群像慌乱被战术调度收束 | 群像先扩散，再用指令和执行结果建立三股或多股行动线 |
| `pressure-hold-to-handoff` | 高点后需要给下游留下交出锚点 | 镜头密度下降，保留读秒、反应、物件水线、灯色或声音余波 |

## Set-Piece Chain Exception

通常关键块扩展到 3-4 镜已经足够；但当当前画面句子明确包含连续动作结果、连续命中、连续反弹、连续物件变化或连续声画打点时，可启动 `set_piece_chain_slots`，允许单个 `visual_unit` 写到 5-6 镜。

启动条件：

- 每一镜都有新的动作相位、撞击点、物件状态、身体结果、声音打点或反应落点。
- 删掉任一镜都会少一个必要结果或少一个清楚节奏拍。
- 镜头方向、空间锚点和因果顺序清楚，不能让 AIGC 视频生成不可读的飞物乱切。
- 高密度链条后必须安排 `recovery_slot`：普通人反应、威胁反压、结果钉镜或边界交出。

禁止：

- 为了“更爽”把同一状态拆成 5 镜。
- 用 5-6 镜替代不清楚的动作因果。
- 把高密度链条扩展成新增剧情事实、额外招式结果或下游转场方案。

## Sound Cut Pattern

声音可成为分镜密度触发器，但必须落回可见结果。

可用声音：

- 连续拟声：`啪 / 嚓 / 哐 / 咚 / 噗` 等一声一结果。
- 鼓点、舞步、拍手、箫声骤停、骨哨、海螺号、木牌/刀鞘/酒坛撞击。
- 台词被打断、笑声断掉、群像吸气、火堆爆响。

规则：

- 声音决定切点时，每个切点必须有可见主体、动作相位和结果。
- 声音不能替代画面归属；当前声音承托哪条上游画面句子必须清楚。
- 声音高点后应检查是否需要读秒或反应镜，避免爽点过快带走威胁后果。

## Decision Procedure

1. 在 `N3.5-SEQUENCE-ALIGN` 建立 `sequence_profile / unit_ownership_map` 后，判断相邻画面是否需要段落密度曲线。
2. 提炼 `tempo_beats`：用 4-7 个阶段词描述整段速度变化，不写成文学主题。
3. 为每个阶段分配 `density_ramp`：哪些 `visual_unit` 应收敛，哪些标准展开，哪些加密，哪些必须停住。
4. 标记 `peak_slots` 和 `recovery_slots`：峰值不是越多越好，峰值之后必须有结果、反应、反压或交出。
5. 若存在连续动作/声画打点，判断是否进入 `set_piece_chain_slots`；若进入，允许 5-6 镜，但必须逐镜可删减测试。
6. 形成 `density_budget`：检查全段是否过于平均、全满、全空或固定两镜。
7. 形成 `handoff_anchors` 与 `ownership_guard`：曲线只给当前阶段可见锚点，不写 `4-分组` 的创意连接件。
8. 将 `sequence_density_curve` 交给 `N4-BEAT`、`N5-RHYTHM`、`N5.2-DURATION`、`N5.5-PEAK-SHOT` 和 `N6.5-SHOT-PLAN` 消费；单个 `visual_unit` 的最终分镜数仍必须由本句真实节拍证明。

## Review Questions

1. 整段是否有清楚的速度变化，而不是每句同样密度？
2. 低信息处是否被省掉了不必要的镜头？
3. 关键高点是否获得足够分镜密度、时值和结果钉镜？
4. 高密度之后是否有恢复、反压、普通人反应或交出锚点？
5. 5-6 镜链条是否每镜都有独立动作结果或声音打点？
6. 声音切点是否对应可见结果，而不是只靠拟声制造节奏？
7. 曲线是否仍保持逐画面点归属，没有吞入后文动作、对白反应、道具揭示或下游转场方案？

## Anti-Patterns

- 只看单句 `beat_map`，不判断整场戏该如何变速。
- 机械限制所有关键块最多 4 镜，导致连续动作结果被压平。
- 看到动作就一路高密度，没有日常建立、恢复停顿或威胁反压。
- 只有 `shot_count_distribution` 统计，没有 `density_curve_summary`。
- subagents 顾问只给“更快、更电影感”建议，没有给出段落变速、峰值槽位或恢复槽位。
