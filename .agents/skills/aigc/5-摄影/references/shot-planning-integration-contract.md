# Shot Planning Integration Contract

本文件定义 `5-摄影` 在输出 `分镜明细：分镜N` 前的强制汇流层。它的目的不是新增审美术语，而是确保 `references/` 中的节拍、画面节奏、镜头时值、高点策略、段落观看意图、逐画面点归属、连续性、摄影语法、功能性影视投影、AI 视频提示词执行稳定性、动态运镜、自然成稿和技法库真实进入思维与执行。

## Core Rule

每个 `visual_unit` 在写出 `分镜1（约X秒）:`、`分镜2（约X秒）:` 前，必须先形成内部 `shot_design_plan`。该计划不默认输出到正文，但必须支配最终 `分镜N（约X秒）` 的数量、顺序、入口、单镜时值、摄影语法、运动、落点、衔接、逐画面点归属、下游消费 payload 和视频执行稳定性。若当前段落命中 `sequence_density_curve`，`shot_design_plan` 还必须说明当前画面属于整段哪一个密度槽位，是否是峰值、恢复或 set-piece 链条。

禁止直接从画面句子跳到 `分镜N` 文案。若无法说明某个 `分镜N` 对应的节拍触发、节奏密度、时值等级、段落归属边界、连续性入口、摄影语法选择、功能 payload、AI 视频执行检查、运镜路径和交出点，该分镜视为随机分镜，必须删除或重写。若该分镜只能说明它服务“整段流畅”，但不能回指当前 `visual_unit`，它也是失主分镜，必须移动到对应画面点、改成当前画面点的进入/交出锚点，或删除。

## Required Plan Fields

| field | source contract | purpose |
| --- | --- | --- |
| `visual_unit_function` | `types/visual-unit-type-map.md`、`visual-matching-contract.md` | 当前画面句子的摄影任务：建立空间、执行动作、显影信息、承托表演、制造危险或完成反应 |
| `sequence_profile` | `visual-sequence-alignment-contract.md` | 相邻 3-6 个画面单位的视觉母题、注意力接力、运动家族、材质光色与边界策略；只作为内部连续性上下文 |
| `sequence_density_curve` | `sequence-density-curve-contract.md` | 段落级 `tempo_beats`、`density_ramp`、`peak_slots`、`recovery_slots`、`set_piece_chain_slots`、`sound_cut_pattern`、`density_budget` 与 `handoff_anchors`；指导整段变速和分镜密度预算 |
| `unit_ownership_map` | `visual-sequence-alignment-contract.md`、`visual-matching-contract.md` | 当前 `visual_unit` 拥有哪些主体、动作、道具/文字/身体锚点、对白承托和禁止跨块外溢项 |
| `functional_payload` | `functional-cinematic-projection-contract.md` | 为每个分镜锁定 shot_function、visible_subject、action_phase、camera_movement_plan、composition_anchor、light_color_material 和 downstream consumability |
| `ai_video_prompt_execution_profile` | `ai-video-prompt-execution-contract.md` | 为每个分镜锁定镜头先行执行顺序、方向参照、动作在镜头内部完成、光线结果、表演微动态和提示词模板边界 |
| `beat_sequence` | `beat-analysis-contract.md` | 每个分镜对应一个观看策略变化，不能按固定数量灌水 |
| `shot_count_decision` | `beat-analysis-contract.md`、`visual-rhythm-analysis-contract.md`、`sequence-density-curve-contract.md` | 明确本 visual_unit 为什么是 1/2/3/4 镜；2 镜不得作为默认值；5-6 镜只允许 `set_piece_chain` 例外且每镜必须有独立结果 |
| `rhythm_profile` | `visual-rhythm-analysis-contract.md` | 决定分镜数量、句子密度、运动复杂度、边界清晰度和停顿感 |
| `duration_profile` | `shot-duration-decision-contract.md` | 决定每个 `分镜N` 的时值等级、正文显示秒数、对白台词量预算、停顿/压缩理由和 15 秒分组节奏风险 |
| `shot_duration_decision` | `shot-duration-decision-contract.md` | 为每个计划分镜说明为什么是 `instant / short / standard / held / long_hold`、正文写 `约X秒`，以及缩短或拉长会损失什么 |
| `dialogue_time_budget` | `shot-duration-decision-contract.md` | 对对白/旁白/画外音/反应镜头，裁决台词量下限和跨镜承托关系 |
| `continuity_entry` | `shot-continuity-contract.md` | 当前画面从上一注意力落点、声音、动作、光色或空间轴线如何进入 |
| `handoff_profile` | `transition-design-contract.md` | 场景变化、空间重置、注意力转交、动作/声音/形态/光色/文字接口需要记录哪些交出锚点、进入提示和连续性风险 |
| `camera_grammar_plan` | `cinematic-technique-library.md`、`dynamic-lens-language-contract.md`、`shot-continuity-contract.md` | 为每个节拍裁决景别梯度、景深/焦点、镜头视角、镜头类型、构图、光影、色彩、运镜方式、速度曲线、停点和变化动机 |
| `functional_projection_plan` | `functional-cinematic-projection-contract.md` | 将每个计划分镜投影为主体、动作相位、运镜计划、构图锚点、光色/材质、空间接口、连续性交接和下游消费点 |
| `technique_selection` | `cinematic-technique-library.md`、`dynamic-lens-language-contract.md` | 从 `camera_grammar_plan` 中选择最小充分且必须显式进入成稿的 1-2 个摄影选择 |
| `natural_output_strategy` | `natural-shot-detail-writing-contract.md` | 决定哪些参数必须显式写、哪些内化为画面动作，避免模板腔和参数清单 |
| `unit_ownership_check` | `visual-sequence-alignment-contract.md` | 每条计划分镜能回指当前上游画面句子；不存在后文主体动作、对白反应、记忆段、道具揭示或转场方案提前外溢 |
| `intra_unit_handoff` | `dynamic-lens-language-contract.md` | 同一 `visual_unit` 内相邻 `分镜N` 如何从上一个终点接到下一个起点 |
| `next_handoff` | `shot-continuity-contract.md` | 最后一条分镜把注意力交给下一画面哪个入口 |

## Planning Procedure

1. 先用一句内部判断锁定 `visual_unit_function`，不得把一个低信息动作硬做成高密度段落。
2. 从 `Beat Trigger Matrix` 中选择真实触发点，生成 `beat_sequence`；弱触发合并，强触发拆开。
3. 若相邻画面形成连续观看段落、速度阶段、动作链或声音打点，先读取 `sequence-density-curve-contract.md` 并消费内部 `sequence_density_curve`；判断当前画面属于 `conserve / measured / build / burst / hold / release` 哪个密度槽位，是否为 `peak_slot / recovery_slot / set_piece_chain_slot`。
4. 形成 `shot_count_decision`：先允许 1 镜成立，再验证是否存在第二个真实观看策略；只有关键揭示、群像扩散、动作分相、空间重置或高点承托才继续扩展到 3-4 镜。若命中 `set_piece_chain_slot`，可扩展到 5-6 镜，但每一镜必须有独立起点、撞点、结果、声音打点或反应落点，并通过删减测试。
5. 用 `rhythm_profile` 校准分镜数量：低信息收敛，关键揭示或高点发散；分镜变多必须带来新的注意力、信息、动作相位或情绪压力。若当前批次出现大量同数分镜，尤其 2 镜集中，或连续段落没有明显密度曲线，必须抽样复判并修正 `shot_count_decision` 与 `density_budget`。
6. 形成 `duration_profile` 和每个 beat 的 `shot_duration_decision`：先判断是否承载对白/旁白并估算台词量下限，再判断缩短一半会丢失什么、拉长一倍是否只会拖慢；文字、道具、微表情、空间重置和认知高点必须给足可读时间，低信息动作和重复交出点必须压缩。每个 beat 必须得到正文 `display_seconds`。
7. 若相邻 3-6 个画面单位存在共享空间、道具链、声音链、动作链、记忆插入或视觉母题，先读取 `visual-sequence-alignment-contract.md` 并消费内部 `sequence_profile`；只吸收视觉母题、注意力接力、运动家族、材质光色和交出锚点，不吸收不属于当前画面点的主体动作、对白反应、记忆段或道具揭示。
8. 为当前 `visual_unit` 建立 `unit_ownership_map`：当前块拥有的主体、动作相位、道具/文字/身体锚点、对白承托和禁止外溢项必须清楚；若计划分镜属于其他画面点，必须转移或删除。
9. 用 `continuity_entry` 承接前 3 个画面单位中的最近落点；不能每个画面重新发明一套风格。
10. 若发生场景变化、空间重置、注意力转交、动作承接、声音先行、形态/颜色匹配、信息显影或高点断裂，先建立 `handoff_profile`，明确交出点、进入提示和连续性风险；不得在本阶段裁决普通切镜、软桥接、匹配剪辑或高能转场方案。
11. 建立 `camera_grammar_plan`：景别变化像呼吸，视角变化有权力/主观/观察/空间动机，景深和焦点负责注意力交接，镜头类型和构图服务空间压力或信息显影；运镜速度和停点必须服从 `shot_duration_decision`。
12. 建立 `functional_projection_plan`：没有主体、动作相位、运镜计划、构图锚点、光色/材质、连续性交接、显式时长、对白承托关系或下游消费意义的 beat 不能写成分镜。
13. 建立 `ai_video_prompt_execution_profile`：镜头类型/运动/构图必须先于动作成立；人物位移必须有相对镜头、摄像机、画面边界或空间锚点的方向参照；光线必须写出照亮位置、阴影、轮廓、反光或背景层次；表演情绪必须落到可见微动态；提示词分栏和命令式负向约束只能留作内部边界。
14. 为每个 beat 选择技法时遵守“最小充分”：只选择能服务当前 beat 的参数和运镜策略，不把技法库当菜单随机抽样。
15. 执行 `unit_ownership_check`：每个 beat 必须回答“它服务哪条上游画面句子”；若只服务整段气氛或流畅感，就回到 `sequence_profile`、`sequence_density_curve` 和 `unit_ownership_map` 重排。
16. 用 `natural_output_strategy` 压缩显式参数：每条分镜只写当前节拍最关键的 1-2 个摄影选择，其余通过具体画面、动作、遮挡、光色、停点和落点表达；视频执行稳定性内化为自然镜头文字，不输出完整视频提示词分栏。
17. 写 `分镜N` 时，让每条分镜的起点来自 `continuity_entry`、`sequence_profile` 中允许消费的 attention relay、`sequence_density_curve` 允许的峰值/恢复槽位，或上一条分镜的终点；让每条分镜的终点成为下一条分镜的入口或 `next_handoff`。多分镜之间还必须形成时值接力，不能每镜同长同速。
18. 最终文案必须能反推 `shot_design_plan`：读者能看出为什么有这些分镜、为什么按这个顺序、每镜为什么写 `约X秒`，对白是否被完整承托，摄影机为什么这样动或不动，景别/视角/焦点为什么这样变化，每条分镜归属于哪条画面句子，以及下游图像/视频应消费哪些主体、动作、运镜、构图、光色、空间关系、方向参照和表演微动态；但不得像计划表一样逐项暴露内部字段。

## Internal Plan Shape

```text
shot_design_plan:
  visual_unit_function: <当前画面摄影任务>
  sequence_profile: <如命中，相邻画面单位共享的视觉母题、注意力接力、运动家族、材质光色；不改变逐句归属>
  sequence_density_curve: <如命中，tempo_beats、density_ramp、peak/recovery/set_piece 槽位、声音切点、密度预算和交出锚点>
  unit_ownership_map: <当前块拥有的主体、动作、道具/文字/身体锚点、对白承托和禁止外溢项>
  shot_count_decision: <为什么是 1/2/3/4 镜；2 镜必须说明第二个真实观看策略；5-6 镜只允许 set_piece_chain 且每镜不可删>
  rhythm_profile: <收敛/标准/发散/断裂的内部判断，不输出标签>
  duration_profile: <整体时值策略、显式秒数分布、对白台词量预算、15 秒分组风险和相邻分镜时值接力>
  continuity_entry: <承接上一落点、声音、动作、光色或空间轴线>
  handoff_profile: <如触发，记录场景/空间/注意力/动作/声音/形态/光色/文字接口、交出点、进入提示和连续性风险>
  ai_video_prompt_execution_profile: <镜头先行、方向参照、动作在镜头内部完成、光线结果、表演微动态和提示词模板边界>
  beats:
    - beat: <节拍1的观看策略变化>
      trigger: <BT-xx>
      camera_grammar_plan:
        shot_scale_path: <景别梯度：建立/调度/加压/揭示/回收>
        angle_strategy: <平视/低角度/高角度/俯拍/仰拍/过肩/主观/窥视及其动机>
        depth_focus_plan: <景深与焦点如何承接注意力>
        lens_and_composition: <镜头类型、构图锚点、前中后景或遮挡关系>
        light_color_motion: <光色母题与运镜速度/停点如何配合>
      functional_payload:
        shot_function: <本镜影视功能>
        visible_subject: <可见主体>
        action_phase: <动作/信息/反应相位>
        camera_movement_plan: <运镜方式、方向、速度、停点、焦点/景别变化、交接接口>
        composition_anchor: <构图锚点>
        light_color_material: <光色/材质/视觉母题>
        downstream_consumability: <图像/视频可消费点>
      ai_video_prompt_execution:
        camera_first_opening: <这一镜开头先声明的镜头、机位、运动或构图关系>
        direction_reference: <运动、入画、退场、视线或镜头路径的相对镜头/画面参照>
        action_inside_camera: <人物动作如何在同一个镜头逻辑内部发生>
        microdynamic_visibility: <情绪是否落到面部肌肉、身体联动、呼吸、手部或视线变化>
        lighting_result: <光线造成的亮面、暗面、阴影、轮廓、反光或背景层次>
        prompt_boundary: <是否避免把完整提示词分栏或命令式负向词落入正文>
      shot_duration_decision:
        duration_class: <instant / short / standard / held / long_hold>
        estimated_seconds: <内部估算范围；通常不输出到正文>
        display_seconds: <正文写入的约X秒>
        dialogue_time_budget: <none / inherited / local_line / voiceover；如命中则写台词量下限和承托关系>
        duration_reason: <冲击/动作完成/可读性/表演停顿/空间定位/反应吸收/边界交出>
        compression_risk: <none / too_short / too_long / conflicts_with_15s_group>
      technique: <从 camera_grammar_plan 中显式进入成稿的必要项>
      density_curve_check: <本镜是否符合当前 density_ramp / peak_slot / recovery_slot / set_piece_chain_slot>
      natural_output_strategy: <显式写哪些关键选择，哪些内化成自然画面文字>
      unit_ownership_check: <本镜服务哪条上游画面句子，是否存在跨块外溢；若有，如何移走或改写>
      start: <镜头起点>
      path: <运动路径与速度曲线>
      end: <注意力落点>
      handoff: <交给下一分镜或下一画面的接口>
```

该结构只作为内部计划或执行报告证据，不作为逐集摄影稿正文的固定输出字段。

## Output Sufficiency Gate

每个 `分镜N` 必须至少满足以下七点：

1. `start` 明确：从哪个景别、焦点、空间位置、动作、声音或光色接口进入。
2. `path` 明确：使用哪类镜头、运镜方向、速度曲线和焦点/景别变化。
3. `end` 明确：落到哪个人物、道具、文字、危险源、反应或转场接口。
4. `motivation` 明确：能看出该运动服务信息揭示、动作相位、情绪压力、空间关系或转场。
5. `duration` 明确：每条分镜写成 `分镜N（约X秒）:`，能反推该镜是快速通过、标准承接、读秒停留还是长停顿；缩短或拉长的取舍有理由。
6. `dialogue_budget` 明确：若承载对白/旁白/画外音，显式秒数不低于台词量下限，或已说明跨镜延续。
7. `handoff` 明确：多分镜时相邻分镜首尾相接，最后一镜能交给下一画面。
8. `downstream_payload` 明确：能抽取主体、动作、运镜、构图锚点、光色/材质和图像/视频可消费点。
9. `camera_grammar` 明确：景别、视角、景深/焦点、镜头类型或构图变化至少有一个真实服务当前节拍，且变化不破坏连续性。
10. `ai_video_execution` 明确：镜头先行包裹动作、方向参照明确、光线写出结果、表演微动态可见，且没有直接输出完整提示词分栏或命令式负向词。
11. `naturalness` 合格：读起来不是字段展开、参数清单或模板填空。
12. `unit_ownership` 合格：每条分镜能回指当前画面句子，没有把后文主体动作、对白反应、记忆段、道具揭示或组间连接方案提前写进当前块。
13. `density_curve` 合格：连续段落能说明哪里省镜头、哪里加密、哪里停顿、哪里硬切和哪里交出；5-6 镜链条每镜都有独立结果，且高密度后有恢复或反压。

## Anti-Patterns

- 只因为“想更电影感”就把一个画面拆成多个分镜。
- 只因为模板里有 `分镜2` 就把每个画面写成 2 镜。
- 只做单个画面句子的 `shot_count_decision`，没有为连续段落形成 `sequence_density_curve`，导致整场没有速度变化。
- `分镜1`、`分镜2`、`分镜3` 彼此都在重新描述同一个状态，没有新的观看策略。
- 把 5-6 镜 set-piece 当作通用高光模板，而不是连续动作结果或声音打点的例外。
- 每条分镜都换一套技法，读不出上一镜如何进入下一镜。
- 分镜数量确实变多了，但没有主体、动作、信息或情绪的递进。
- 每条分镜都同样长度、同样速度，或长停顿没有可读性/表演/空间/高点理由。
- 快速切走必须读清的文字、道具或微表情，导致分镜数量对了但观看时值错了。
- 对白/旁白画面没有根据台词量决定显式秒数。
- `分镜N` 缺少 `（约X秒）`，导致下游视频阶段无法消费时长。
- 分镜读起来顺，但下游无法判断该画谁、摄影机怎么动或为什么不动、构图锚点是什么、光色如何继承。
- 分镜读起来顺，但动作和镜头割裂，无法按镜头先行顺序改写为视频提示词。
- 写“人物向前走、往后退、从左边进入”，但没有说明相对镜头、画面边界、前中后景或空间锚点。
- 写“左侧光、顶光、电影感光线”，但没有说明照亮哪里、阴影在哪里、背景如何压暗、轮廓如何分离。
- 写“愤怒、紧张、难过”，但没有任何眼神、咬肌、鼻翼、嘴角、肩膀、手指、呼吸或身体联动。
- 把“镜头与构图 / 人物与动作 / 光线 / 声音与环境 / 画面质感 / 不要夸张表情”这类完整视频提示词分栏直接粘进 `分镜明细`。
- 分镜读起来顺，段落也很流畅，但无法判断它属于哪条上游画面句子。
- 当前块为了承接段落运镜，把下一块的主体动作、对白反应、记忆插入、道具揭示或创意转场方案提前吞进来。
- 分镜出现景别、视角、焦点或镜头类型变化，但变化没有服务节拍、空间、信息、情绪或交接，只是为了显得专业。
- 只写“推近”“特写”“压迫感”，没有起点、路径、落点和交出点。
- 为了证明起点、路径、速度、落点齐全，把每条分镜都写成同一个“从……以……变化到……最终……”骨架。
