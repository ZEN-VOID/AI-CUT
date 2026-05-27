# Shot Planning Integration Contract

本文件定义 `5-摄影` 的 `shot_design_plan` 如何在分镜明细注入前完成决策汇流。它不是操作流程，而是每个 `visual_unit` 在进入终稿前的决策层集成器。

## Core Purpose

`shot_design_plan` 是 `5-摄影` 执行阶段内部的决策容器，不是输出字段。它必须在 `N2-BEAT`、`N2.5-RHYTHM`、`N2.5D-DURATION`、`N2.6-PEAK`、`N3-SHOT-DESIGN` 和 `N4-INJECT` 之间完成以下集成：

1. 把 `beat_map` 中的节拍触发点翻译为具体分镜数量和切换理由。
2. 把 `rhythm_profile` 中的张弛判断翻译为密度分布和速度曲线。
3. 把 `shot_duration_decision` 中的时值裁决翻译为正文 `display_seconds` 和镜头语言速度。
4. 把 `peak_shot_profile` 中的高点强化策略翻译为分镜密度、景别尺度、停顿和余波。
5. 把 `dialogue_time_budget` 中的台词量下限翻译为时长门槛或跨镜延续说明。
6. 把 `sequence_density_curve` 中的段落级密度曲线翻译为逐镜头密度分配。
7. 把 `continuity_profile` 和 `handoff_profile` 中的连续性要求翻译为入口、落点和交出接口。
8. 把 `camera_grammar_plan`、`camera_movement_emotion_plan`、`depth_of_field_narrative_plan`、`light_narrative_plan`、`attention_guidance_plan` 中的摄影语法翻译为可执行运镜策略。
9. 把 `scene_visual_constraint` 中的场景级视觉约束翻译为构图、采光、色彩和材质边界。
10. 把 `dimension_coverage` 中的维度裁决翻译为正文应覆盖的扩展信息点。
11. 把 `prop_shot_admission` 中的道具准入裁决翻译为道具能否成为焦点、反射或特写。
12. 把 `functional_projection_plan` 中的功能性 payload 翻译为下游可消费的视觉事实。
13. 把 `ai_video_prompt_execution_profile` 中的执行约束翻译为方向参照、光线结果和表演微动态。

## Decision Stack Order

`shot_design_plan` 的决策必须按以下顺序执行，不能跳步或逆序：

```
beat_map → rhythm_profile → shot_duration_decision → peak_shot_profile
    ↓              ↓                 ↓                    ↓
dialogue_time_budget → sequence_density_curve → continuity_profile
                              ↓                              ↓
                 camera_grammar_plan + camera_movement_emotion_plan
                              ↓
                 depth_of_field_narrative_plan + light_narrative_plan
                              ↓
                 attention_guidance_plan + scene_visual_constraint
                              ↓
                 dimension_coverage + prop_shot_admission
                              ↓
                 functional_projection_plan + ai_video_prompt_execution_profile
                              ↓
                 shot_count_decision + shot_design_plan (final)
```

跳步会导致决策冲突：没有 `beat_map` 就无法裁决分镜数量，没有 `shot_duration_decision` 就无法决定正文时值，没有 `camera_grammar_plan` 就无法选择景别/视角/景深/镜头类型，没有 `ai_video_prompt_execution_profile` 就无法保证下游执行稳定性。

## Shot Count Cardinality

分镜数量由以下输入共同决定，不由模板决定：

| input | influence |
| --- | --- |
| `beat_map` (有效触发点数量) | 决定最小分镜数；每个有效触发点默认对应一个分镜切换点 |
| `rhythm_profile` (密度槽位) | 决定是否收敛、标准展开或发散强化；收敛时可以合并触发点 |
| `sequence_density_curve` (段落密度曲线) | 决定哪里加密、哪里省镜头、哪里停顿；set-piece 链条可扩展到 5-6 镜 |
| `action_phase` (动作分相数量) | 决定是否需要多镜覆盖预备/执行/结果/反应各阶段 |
| `dialogue_time_budget` (台词时长) | 决定是否需要拆分说话镜/反应镜/空间压力镜 |
| `screen_information_load` (信息密度) | 决定是否需要文字/道具/微表情读秒镜 |
| `emotional_intensity` (情绪强度) | 决定是否需要崩溃/震惊/强忍等慢节奏长镜 |
| `downstream_risk` (AIGC 执行风险) | 决定是否需要拆镜重置主体/方向/光线/表演相位 |

分镜数量合法性：
- `1 个分镜`：低信息过场、单一表演承托、单一文字读秒、单一反应镜头；必须通过非复述测试和功能性 payload 检查。
- `2 个分镜`：建立后揭示、动作后反应、环境后可读细节、主体后压力源、声画接口后落点、平台钩子后结果；每个分镜必须有独立触发点或观看价值，不能作为默认占位。
- `3-4 个分镜`：关键规则显影、动作分相、群像恐慌、高潮/爽点/高光、空间重置、强断裂转场、平台钩子连续推进、AIGC 执行重置；每镜必须有新主体、新动作相位、新信息、新情绪压力、新空间关系、新交接接口或新执行稳定性价值。
- `5-6 个分镜`：仅在命中 `set_piece_chain_slots` 时成立；当前画面句子必须包含连续命中、连续反弹、连续物件结果、连续声画打点或复杂动作链；每一镜必须有独立起点、撞点、结果、声音或反应，删掉任一镜都会少一个必要节奏拍。

当 `effective_trigger list` 数量大于最终 `shot_count_decision` 时，`shot_design_plan` 必须包含 `trigger_merge_exception`：说明哪些触发点被同镜承载、通过何种焦点拉移/演员走位/框内运动/景深变化完成，以及为什么不会损失观看结果、平台节奏、下游 payload、人物动作连续性或 AIGC 执行稳定性。缺少该证明时，1 镜块按 `FAIL-CINE-03F` 返工，不能用“单一观看策略”笼统带过。

## Duration Decision Integration

`shot_duration_decision` 必须集成到每个 `shot_design_plan` 中：

| duration_class | display_seconds | use when |
| --- | --- | --- |
| `instant` | 约0.5秒 | 惊吓切点、硬断裂、撞点确认 |
| `short` | 约1秒 | 单一动作、视线转交、反应入口、边界锚点 |
| `standard` | 约1.5秒 / 约2秒 | 普通揭示、动作完成、空间关系承接 |
| `held` | 约2.5秒 / 约3秒 | 表演停顿、规则读秒、空间重置；必须通过"缩短一半会损失什么"测试 |
| `long_hold` | 约4秒 / 约5秒 | 高潮读秒、关系停顿、重大认知翻转；必须有时值必要性证据 |

时值裁决规则：
- `dialogue_seconds_floor` 是硬输入：若命中，显式秒数不得低于台词量下限。
- 情绪类高点（崩溃/震惊/醒悟/强忍）标记 `tempo=slow_burn/hold`，时长由情绪节奏决定，不受 Short Drama AIGC Bias 的 `约3秒` 证据门槛约束。
- `display_seconds` 必须能从正文镜头语言反推：快速冲击镜用短句硬落，读秒镜用静止或极慢运动，内容密度镜用焦点拉移或显影。

## Continuity Handoff Integration

每个 `shot_design_plan` 必须包含连续性决策：

| continuity_element | required content |
| --- | --- |
| `entry` | 从上一镜的哪个景别、机位、焦点、空间位置、声音、动作或光色接口进入 |
| `action_anchor` | 当前镜继承上一镜的哪个动作相位、位置、朝向、注意力落点 |
| `exit` | 当前镜最后停在哪里、如何收住 |
| `handoff` | 把注意力交给下一镜/下一画面的哪个可见接口 |

场景变化时，`handoff` 必须能还原上一画面的交出点和下一画面的进入提示；组间或跨场景创意转场交给 `6-分组` 连接件，不在本阶段裁决。

## Scene Visual Constraint Integration

每个 `shot_design_plan` 必须继承 `scene_visual_constraint`（纯内部裁决，不进入成稿）：

- `构图布局`：场景级构图规则（对称/三角/引导线/框架等）
- `构图方式`：形状感/线条感/影调感/虚实感/节奏感/纹理质感/气势
- `光源设置`：主光源位置、辅光源安排、补光策略
- `照明类型`：硬光/软光/伦勃朗/蝴蝶光/分割光/显影光等
- `色彩体系`：色相/饱和度/明度的场景级约束
- `摄影技术参数`：焦段/光圈/快门/ISO 的场景级偏好

这些约束必须在景别、视角、景深、焦点、运镜选择中体现，不得违背场景级视觉合同。

## Prop Shot Admission Integration

道具镜头准入是 `shot_design_plan` 的必要决策项：

| prop_shot_admission | condition |
| --- | --- |
| `allowed` | 道具是重要信息/规则/证据/危险源；或角色与道具发生明确互动；或当前画面需要必要环境交代 |
| `denied` | 道具无互动、只是普通环境物；或成为焦点会破坏人物动作衔接；或通过反射/涟漪/孤立特写制造氛围但无信息价值 |

若 `prop_shot_admission=denied`，正文不得把该道具写成焦点、反射终点或独立特写。

## AI Video Prompt Execution Profile

每个 `shot_design_plan` 必须包含 `ai_video_prompt_execution_profile`：

- **方向参照**：人物/镜头运动必须相对于摄像机或画面边界，不能含混（如"从画面右侧进入"而非"从左边来"）。
- **光线结果**：光线必须写成可见结果（如"左眼窝陷进阴影，右颧骨亮起一道白线"），不能只写光源名或效果词（如"侧光制造层次感"）。
- **表演微动态**：情绪必须落到可见物理动作（如"咬肌收紧、手指发白、眉心竖纹"），不能只写抽象词（如"紧张、压抑、恐惧"）。
- **镜头包裹动作**：镜头先行，不让动作先于镜头孤立发生。
- **主体锁定**：每镜必须锁定单一主体，避免主体漂移、方向含混或动作失控。

## Dimension Coverage Decision

`dimension_coverage` 是为每条计划分镜裁决的维度覆盖，不是逐镜硬填：

| dimension | covered when |
| --- | --- |
| 角色情绪/肢体语言 | 当前镜有情绪转折、表演提示或微动态 |
| 语气语速 | 当前镜有对白、旁白或画外音承托 |
| 镜头意识 | 当前镜有视线转交、视线钉住或画外音画内焦点不一致 |
| 运动特征 | 当前镜有角色移动、运镜或物体运动 |
| 陪体动态 | 当前镜有陪体、群体或背景人物参与叙事 |
| 前景动态 | 当前镜有前景遮挡参与构图或注意力引导 |
| 背景动态 | 当前镜有背景空间关系变化 |
| 景别变化 | 当前镜有景别切换 |
| 镜头运动 | 当前镜有运镜 |
| 镜头视角 | 当前镜有视角变化（俯拍/仰拍/平视/倾斜） |
| 光影变化 | 当前镜有光线可见结果 |
| 光影反射 | 当前镜有反射、倒影、遮蔽或轮廓分离 |
| 动态焦点 | 当前镜有焦点拉移或景深变化 |
| 节奏同步 | 当前镜有声音打点、鼓点、撞点或声画同步 |

维度覆盖必须基于当前镜实际存在的内容；不存在的不为凑数硬塞。

## Shot Design Plan Output

每个 `shot_design_plan` 必须包含以下内部决策（不输出字段标签，但必须能从正文反推）：

1. **`shot_count_decision`**：为什么是 1/2/3/4 镜；若进入 set-piece 链条，说明为何可扩展到 5-6 镜且每镜不可删。
2. **`unit_ownership_check`**：该分镜服务哪一条上游画面句子，没有吞入后文动作、对白反应、记忆段或道具揭示。
3. **`beat_trigger_reference`**：每个分镜对应的有效触发点类型（BT-01~BT-16）。
4. **`trigger_merge_exception`**：仅当有效触发点多于最终分镜数时出现；说明合并触发点为何不会造成单镜吞多 beat。
5. **`rhythm_profile_application`**：该镜应收敛、标准展开还是发散强化。
6. **`shot_duration_decision`**：显式秒数、对白台词量影响、短剧·AIGC 默认压缩应用。
7. **`camera_grammar_plan`**：景别、视角、景深、焦点、镜头类型、构图锚点的选择。
8. **`camera_movement_plan`**：运镜方式、运动方向、速度曲线、停点、落点、交接接口。
9. **`peak_shot_profile_application`**：若命中高点，是否加强分镜密度、景别尺度、运镜速度、停顿或余波。
10. **`prop_shot_admission`**：道具能否成为焦点或反射终点。
11. **`functional_projection_check`**：去掉源句已有内容后，仍能读出摄影机如何看、如何动、何时停、焦点如何转、光影如何组织或如何交接。
12. **`ai_video_prompt_execution_check`**：方向参照是否明确、光线是否写成可见结果、情绪是否落到表演微动态、镜头是否包裹动作。
13. **`dimension_coverage`**：覆盖了哪些扩展维度，不存在的不硬塞。
14. **`continuity_handoff`**：从上一镜如何进入，把注意力交给下一镜/下一画面的哪个可见接口。

## Anti-Patterns

- 没有 `beat_map` 就直接决定分镜数量。
- 没有 `shot_duration_decision` 就写正文时值。
- 没有 `camera_grammar_plan` 就选择景别/视角/景深/镜头类型。
- 没有 `ai_video_prompt_execution_profile` 就进入成稿。
- 把 `1 个分镜` 的低信息镜头写成 2-3 镜，把 set-piece 链条压成 2 镜。
- 把包含多个有效触发点的画面写成 `1 个分镜`，却没有 `trigger_merge_exception` 证明这些触发点能在同镜内清楚完成。
- 把 `5-6 个分镜` 的复杂动作链写成 1-2 镜。
- 每个分镜都按固定模板填充，没有根据 beat/密度/时值/连续性/AI 执行风险做差异化决策。
- `prop_shot_admission=denied` 时仍在正文写入道具焦点或孤立特写。
- `dialogue_seconds_floor` 超标但正文时值未反映。
- `tempo=slow_burn/hold` 的情绪类高点未在正文体现足够停留。

## Review Questions

审查每个 `shot_design_plan` 时必须追问：

1. 分镜数量是否由有效触发点、密度曲线、动作分相、台词量、信息密度、情绪强度和 AIGC 执行风险共同决定，而不是模板？
2. 若有效触发点数量大于最终分镜数，是否有 `trigger_merge_exception`；若没有，是否应按 `FAIL-CINE-03F` 拆镜？
3. 时值是否由对白台词量、信息可读性、表演变化和节奏角色共同决定，并已在正文中体现？
4. 每个分镜是否能回指一条上游画面句子，且没有吞入后文动作、对白反应、记忆段或道具揭示？
5. 连续性交接是否包含入口、动作锚点、落点和交出接口？
6. 道具镜头准入是否已裁决，且被拒绝的道具未进入正文？
7. AI 视频执行约束（方向参照、光线结果、表演微动态、镜头包裹动作）是否已在正文中体现？
8. 维度覆盖是否基于当前镜实际存在的内容，不存在的不硬塞？
9. 若进入 `set_piece_chain_slots`，每镜是否都有独立起点、撞点、结果、声音或反应，删掉任一镜都会少一个必要节奏拍？
10. 若进入 `held/long_hold`，正文是否通过静止、极慢运动、读秒、焦点停留或框内变化体现了足够停留？
11. 若命中 `tempo=slow_burn/hold`，正文是否体现了情绪节奏决定了时长，而不是被短剧·AIGC 默认压缩带走？

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `shot_design_plan` 是否按决策栈完整汇流 `beat/rhythm/duration/peak/dialogue/sequence/continuity/camera/function/AI execution`，没有跳步直接成稿？ | `GATE-CINE-09` | `FAIL-CINE-05F` | `N6.5-SHOT-PLAN` | `shot_design_plan` 汇流与投影检查结果 |
| 产物是否能回指 `N1` 到 `N9` 的关键判断，尤其 `N6.5-SHOT-PLAN` 作为最终成稿硬门是否被执行？ | `GATE-CINE-17` | `FAIL-CINE-05J` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | 思维·执行节点完整检查结果、缺环节点返工记录 |
| 分镜数量是否由有效触发点、密度曲线、动作分相、台词量、信息密度、情绪强度和 AIGC 执行风险共同决定？ | `GATE-CINE-04A` | `FAIL-CINE-03A` | `N4-BEAT` + `N5-RHYTHM` + `N6.5-SHOT-PLAN` | `shot_count_decision`、分镜数量分布与抽样复核 |
| 有效触发点数量大于最终分镜数时，是否有 `trigger_merge_exception`，说明同镜完成不损失观看结果、平台节奏、payload、动作连续性或 AIGC 稳定性？ | `GATE-CINE-04E` | `FAIL-CINE-03F` | `N4-BEAT` + `N6.5-SHOT-PLAN` | 单镜吞 beat 复核结果、合并例外证明 |
| 时值、对白台词量、`slow_burn/hold` 情绪时长是否已进入计划并体现在正文秒数与镜头语言中？ | `GATE-CINE-04B` | `FAIL-CINE-03B` | `N5.2-DURATION` + `N6.5-SHOT-PLAN` | `duration_profile`、对白台词量预算、长停顿抽样 |
| 每条计划分镜是否包含 `entry/action_anchor/exit/handoff`，场景变化是否交给 `N6.1-HANDOFF` 而非在本阶段主创转场？ | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `N6-CONTINUITY` + `N6.1-HANDOFF` + `N6.5-SHOT-PLAN` | 镜内/镜间连贯性与边界交出检查结果 |
| 场景视觉约束、道具准入、维度覆盖和功能 payload 是否已进入计划，且被拒绝的道具没有成为焦点或孤立特写？ | `GATE-CINE-15` | `FAIL-CINE-05H` | `N6.3-SCENE-VISUAL-CONSTRAINT` + `N6.4-FUNCTIONAL-PROJECTION` + `N6.5-SHOT-PLAN` | 功能性影视投影、场景视觉约束、道具准入和维度覆盖抽样 |
| AI 视频执行约束是否已进入计划：镜头包裹动作、方向参照、光线结果、表演微动态和主体锁定是否清楚？ | `GATE-CINE-15A` | `FAIL-CINE-05N` | `N6.4-FUNCTIONAL-PROJECTION` + `N6.5-SHOT-PLAN` | AI 视频执行稳定性检查结果、方向/光线/微动态修复记录 |
| 本轮加载或产生强制裁决的 reference 是否都能回指 review matrix、gate、fail code 和报告证据？ | `GATE-CINE-17A` | `FAIL-CINE-05REF` | `review/review-contract.md#Reference-Review-Gate-Matrix` + `N8-REVIEW` | reference gate 覆盖检查结果、缺失映射修复记录 |
