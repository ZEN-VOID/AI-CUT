# Visual Rhythm Analysis Contract

本文件定义 step2.5“画面节奏分析”。节拍分析决定“切换点在哪里”，画面节奏分析决定“分镜明细写多满、多快、多炫、多克制”。目标是让不同类型、不同节奏、不同信息重要性的画面句子张弛有度，该收敛的收敛，该发散的发散。

## Core Rule

每个画面句子在注入分镜明细前必须生成 `rhythm_profile`。它决定：

| rhythm_dimension | decision |
| --- | --- |
| `importance_level` | low / medium / high / critical |
| `tempo` | hold / slow_burn / steady / quick / rupture |
| `density` | sparse / measured / rich / maximal |
| `movement_complexity` | static / single_move / combo_move / rupture_move |
| `description_scope` | one-line concise / standard / expanded / set-piece |
| `transition_strength` | none / soft_bridge / match_cut / high_energy |
| `peak_emphasis` | none / restrained_peak / expanded_peak / rupture_peak |

`rhythm_profile` 还必须承担分镜数量去模板化职责：当 `beat_map` 倾向输出 2 镜时，先判断当前画面是否真的需要“起点/揭示”“动作/反应”“空间/压力源”两段观看；如果只是一个单一观看动作，收敛为 1 镜；如果是关键揭示、动作分相、群像扩散或高点承托，不得被压平为 2 镜。

## Rhythm Profile Matrix

| visual_unit_type | information importance | rhythm choice | shot detail behavior |
| --- | --- | --- | --- |
| 过场动作 | low | 收敛 | 1 个分镜，单一运动或固定机位，参数准确但不铺陈 |
| 空间建立 | medium/high | 标准展开 | 1-2 个分镜，交代轴线、空间压力和视觉母题 |
| 关键规则/系统显影 | high/critical | 发散强化 | 2-3 个分镜，文字可读、角色反应、光色或焦点变化清楚 |
| 道具异常 | high | 精准发散 | 微距/特写 + 反应承接，强调材质、颜色、危险信息 |
| 表演微反应 | medium/high | 收敛加压 | 少动或极慢动，景深收窄，留停顿，不用复杂炫技盖住表演 |
| 群像混乱 | medium/high | 节奏扩散 | 2-4 个分镜，寻找恐惧传播路径，不平铺所有人 |
| 场景变化 | medium/high | 交接展开 | 1-2 个分镜，至少处理上一场景交出点和下一场景进入点；除非有强接口，不硬做高能 |
| 高能入场/惊吓 | critical | 断裂式发散 | 快速运动、急停、声画桥或光变，但要给落点 |
| 低信息对白画面 | low/medium | 克制承托 | 1 个反应或关系镜头，避免每句对白都炫技 |
| 上游高潮/爽点/高光承托 | high/critical | 峰值强化 | 按 `peak-shot-language-contract.md` 判断是停顿、扩展还是断裂，不一律更快或更多 |

## Decision Procedure

1. 先判断当前画面句子的叙事权重：是否带来新信息、新危险、新关系、新空间或新情绪峰值。
2. 再判断当前上下文节奏：上一组镜头是否已经高密度、高运动、高转场；若是，当前可适当收敛。
3. 判断观众是否需要停顿读信息：规则文字、道具细节、微表情需要留读秒，不应被高速运动带走。
4. 判断是否需要发散：关键揭示、空间重置、情绪峰值、威胁入场可提高分镜数量和动态复杂度。
5. 若发生场景变化，固定标记转场动机并交给 `references/transition-design-contract.md` 形成 `transition_profile`；`transition_strength` 可为 `soft_bridge` 或 `match_cut`，不必默认 `high_energy`。
6. 若画面承载上游高潮/爽点/高光成分，先标记 `peak_emphasis`，再交给 `references/peak-shot-language-contract.md` 裁定具体峰值镜头策略。
7. 形成内部 `rhythm_profile` 后再写分镜明细；`rhythm_profile` 不显式输出，只通过描述密度、运动复杂度、转场强度和停顿感体现在成稿中。
8. 对批量输出做分布抽查：若同一集或同一场中 2 镜块占比异常集中，回到低信息、关键显影、群像和高点样本复判，证明每个 `分镜2` 都有真实节拍，或删并/扩展到正确数量。

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
- 需要把上一组镜头的压抑释放成高能转场或视觉爆点。
- 上游已经存在明确高点，且普通节奏会削弱行动结果、认知震荡、关系暖点、规则压迫或奇观冲击。

发散不是堆满参数，而是让信息、情绪和运动同时升级。

## Output Guidance

| profile | recommended output |
| --- | --- |
| `sparse + static` | `分镜1` 一句完成，固定机位或极慢推拉，强调落点 |
| `measured + single_move` | `分镜1` 或 `分镜1-2`，一个清楚运动从 A 到 B |
| `rich + combo_move` | `分镜1-3`，组合运镜、焦点/景别变化、反应承接 |
| `maximal + rupture_move` | `分镜1-4`，高能转场或断裂节奏，但必须给空间/反应落点 |
| `peak_emphasis + selected_move` | 先按 `peak_shot_profile` 决定停顿、扩展或断裂，再写入 `分镜N`；高点也可以用静止长镜完成 |

`profile` 标签仅用于内部判断，不写入 `分镜N`。输出应直接进入当前画面的镜头运动。

## Anti-Patterns

- 每条画面句子都写成长段大师炫技。
- 每条画面句子都写成 2 个分镜，导致低信息画面被硬撑、关键画面被压平。
- 关键规则显影只写一句“特写规则文字”，没有读秒、反应和光色层次。
- 低信息动作写 3-4 个分镜，拖慢节奏。
- 强表演瞬间用复杂运镜抢走演员。
- 连续多个高密度画面没有收束，导致整集只有“满”没有呼吸。
