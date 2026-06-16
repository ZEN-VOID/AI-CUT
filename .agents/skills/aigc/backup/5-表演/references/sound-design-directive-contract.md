# Sound Design Directive Contract

## Purpose

本合同定义 `2-编导` director layer 的声音设计策略。它不是 BGM 推荐清单、音效标签列表或配乐风格指南，而是声音作为叙事工具的导演判断：什么声音在、什么声音不在、声音从谁的视角听到、沉默何时出现、沉默被什么打破、声音母题如何跨集呼应。

声音设计是导演控制观众感知的第二把钥匙——第一把是画面。当画面展示"发生了什么"，声音决定"观众怎么感受它"。一个好的声音设计决策不是"这里配紧张的音乐"，而是"此刻环境声突然消失，只剩下角色自己的呼吸声，让观众被迫进入角色的主观空间"。

本文件不授权新增剧情事实、对白、事件结果、人物动机、摄影方案或具体音效制作参数。它只负责声音设计的叙事策略判断，供 `2-编导` performance layer 和后续音频阶段消费。

## Ownership

- 本文件拥有声音设计五轴定义、每场景声音规划结构、沉默设计策略、声音母题跨集策略和证据结构。
- `atmosphere-and-mood-contract.md` 负责五感氛围中的声景层次和质感；本文件负责声音作为叙事工具的策略判断，层次更高。
- `directorial-authorship-contract.md` 负责编导创作内核中的 `sound_or_silence_engine`（单场声音/沉默指令）；本文件负责跨集的声音策略一致性。
- `climax-visual-treatment-contract.md` 负责高潮画面的 `audio_payload`；本文件的声音策略应与高潮画面的声音设计协调。
- `episode-visual-spine-contract.md` 负责整集视觉主轴；声音母题应与视觉母题链形成呼应关系。
- `actor-performance-control-contract.md` 负责五层表演控制中的 `ambient_support`；本文件的声音策略是其上层约束。
- `performance-and-scene-craft-contract.md` 负责场景中的声音表演变量；本文件不干涉具体的对白表演细节。

## Dependency Graph

```
sound-design-directive-contract.md
├── consumed_by: N3-DIR-SUBSTANCE (形成 sound_or_silence_engine)
├── consumed_by: N4-DIR-PEAK (高潮画面的 audio_payload)
├── consumed_by: N7-DIR-AESTHETIC (声音进入 scene_dramatic_map)
├── consumed_by: N9-DIR-DRAFT (声音指令内嵌到音效/音效画面字段)
├── consumed_by: N10-DIR-REVIEW (验证声音策略一致性)
├── consumed_by: 2-编导 performance layer (ambient_support 层的上层约束)
├── produces:
│   └── sound_design_directive (必须产出，含 per-scene sound_plan)
└── cross_reference:
    ├── atmosphere-and-mood-contract.md (声景层次协调)
    └── climax-visual-treatment-contract.md (audio_payload 协调)
```

## Five-Axis Sound Strategy

声音设计沿五个独立策略轴展开，每个轴回答一个核心问题：

| axis | core question | what it controls |
| --- | --- | --- |
| `sound_motif` | 什么声音是本片的听觉母题，它在哪里出现、在哪里变奏、在哪里缺席？ | 跨集的听觉一致性——特定声音（钟声、水滴、风声、某种乐器、某种环境声）成为叙事标记，出现时观众自动联想到某个主题、角色或情绪 |
| `sound_absence` | 什么声音应该消失？消失本身传达什么？ | 声音消失的叙事力量——当观众习惯的背景声突然消失，注意力被强制聚焦，不安感产生。声音消失比声音出现更有力 |
| `sound_perspective` | 这个场景的声音是从谁的视角听到的？ | 声音的主观性——同一个场景，从 A 的视角和从 B 的视角听到的声音不同。声音主观视角可以暗示角色的心理状态、注意力焦点或感官变化 |
| `sound_reality` | 声音是客观存在的，还是角色主观感知的？ | 客观与主观的切换——客观声音是场景中物理存在的声音，主观声音是角色心理状态投射到听觉上的声音（耳鸣、放大、扭曲、选择性听觉）。切换本身是叙事信号 |
| `sound_transition` | 场景之间的声音如何桥接？ | 跨场景的声音流动——上一场的声音延续到下一场（声音先行或声音拖尾）、两个场景的声音交叉（蒙太奇中的声音对位）、声音作为转场标记 |

### Axis Interaction Patterns

五轴不是独立运行的；常见的轴间联动：

| pattern | axes involved | description | example |
| --- | --- | --- | --- |
| `motif_absence` | `sound_motif` + `sound_absence` | 听觉母题在关键时刻消失，比母题出现更有力 | 贯穿全片的钟声在角色死亡时突然消失，沉默替代钟声 |
| `perspective_shift` | `sound_perspective` + `sound_reality` | 从客观视角切换到主观视角时，声音从真实变为扭曲 | 角色受到冲击后，环境声开始变远变闷，耳鸣声浮现 |
| `absence_transition` | `sound_absence` + `sound_transition` | 场景间的沉默桥接——上一场结束在沉默中，下一场从沉默中浮现新的声音 | 对决结束后的长时间沉默，被远处传来的晨钟打破，过渡到下一场 |
| `motif_transition` | `sound_motif` + `sound_transition` | 声音母题作为场景间的桥接——母题从上一场带入下一场 | 角色在 A 场景听到的雨声延续到 B 场景，但 B 场景是室内，暗示声音已从客观变为主观 |

## Per-Scene Sound Plan Structure

每个关键场景（有戏剧问题的场景、转折场景、高潮场景、场景身份独特的场景）必须形成 `sound_plan`：

```yaml
sound_plan:
  scene_id: ""
  source_anchor: ""                   # 回指上游场景锚点
  dominant_sound: ""                  # 本场景的主导声音是什么（必须来自场景本身）
  absent_sound: ""                    # 什么声音应该不存在（为什么消失了、消失传达什么）
  sound_motif_variation: ""           # 声音母题在本场景如何出现、变奏或缺席
  subjective_sound_shift: ""          # 声音是否从客观切换到主观（在哪个 beat、为什么）
  silence_as_narrative:               # 沉默作为叙事工具
    appears: true/false               # 本场景是否有设计过的沉默
    when: ""                          # 沉默出现在哪个 beat
    duration_feel: "fleeting | brief | sustained | prolonged"  # 沉默的感知时长
    broken_by: ""                     # 沉默被什么打破（必须是场景内有来源的声音）
    what_silence_conveys: ""          # 沉默传达什么叙事信息
  sound_perspective: "objective | subjective_a | subjective_b | mixed"  # 声音视角
  sound_reality_status: "real | distorted | selective | imagined"       # 声音现实状态
  directorial_intent: ""              # 声音设计的叙事目的（不是技术描述，是叙事判断）
```

### Sound Plan Constraints

- `dominant_sound` 必须来自场景本身（空间声源、人物动作声、环境声），不得是泛化的 BGM 风格标签。
- `absent_sound` 不能只写"安静"；必须说明什么声音不见了、为什么不见了、消失本身传达什么。
- `sound_motif_variation` 只在本场景与声音母题相关时填写，不相关时标注 `not_applicable`。
- `subjective_sound_shift` 不能随机切换；切换必须绑定一个明确的 beat（信息冲击、情绪临界、创伤触发）。
- `silence_as_narrative.broken_by` 必须是场景内有物理来源的声音，不得是配乐。
- `directorial_intent` 必须是叙事判断（"让观众感受到角色被世界隔绝"），不得是技术描述（"用低频混响"）。

## Silence Design Strategy

沉默是声音设计中最有力的工具。它不是"没有声音"，而是一种主动的叙事选择。

### When Silence is Needed

| silence trigger | what it conveys | duration guidance |
| --- | --- | --- |
| 信息冲击后的消化 | 角色和观众需要时间消化刚刚发生的事 | `brief` 到 `sustained`，取决于冲击力度 |
| 关系临界点 | 两个人之间该说的话没有说出口 | `sustained`，沉默本身就是未说出的话 |
| 权力压迫 | 沉默制造压力，让对方先开口就是权力 | `sustained` 到 `prolonged`，先打破沉默的人让渡权力 |
| 创伤显影 | 角色回到创伤现场或触发创伤记忆，外部世界消失 | `sustained`，伴随主观声音（耳鸣、心跳放大、环境声变远） |
| 高潮前的蓄力 | 兑现之前最后一刻的静止，观众屏住呼吸 | `brief` 到 `sustained`，被兑现瞬间的声音暴力打破 |
| 角色独处 | 角色与自己的内心对话，不需要外部声音 | `sustained`，被外部世界的声音重新入侵而结束 |
| 死亡或离别 | 世界的声音为某个存在暂停 | `prolonged`，被非常微小的声音打破（一滴水、一阵风、远处的鸟鸣） |

### Silence Duration Perception Guide

沉默的感知时长不是秒表时间，而是观众的心理感受：

| duration_feel | approximate real time | perception |
| --- | --- | --- |
| `fleeting` | 0.5-1.5 秒 | 一个呼吸的间隙，观众感知到"顿了一下" |
| `brief` | 1.5-3 秒 | 一个明显的停顿，观众开始意识到"安静了" |
| `sustained` | 3-8 秒 | 沉默变得有重量，观众开始主动寻找声音，不安感产生 |
| `prolonged` | 8 秒以上 | 沉默成为场景的主角，观众被迫与角色共享沉默的物理空间 |

约束：

- 沉默不能被配乐填充。配乐中的"安静段落"不是沉默；沉默是所有人工声音的消失。
- `fleeting` 级别的沉默不需要 `broken_by` 设计，它可以自然过渡。
- `sustained` 及以上的沉默必须设计 `broken_by`，打破沉默的声音本身就是叙事事件。
- 沉默被打断后，环境声不能瞬间恢复到正常水平；需要一个渐进的"声音回归"过程。

### How Silence is Broken

打破沉默的声音本身就是叙事判断：

| break_source | narrative effect | example |
| --- | --- | --- |
| 角色自身的身体声（呼吸、心跳、吞咽） | 观众被迫回到角色的身体内部 | 长时间沉默后，观众第一次听到角色深吸一口气 |
| 环境中微小的声音（水滴、钟摆、风） | 世界仍在运转，但与角色的沉默形成反差 | 角色沉浸在悲伤中，远处传来日常的叫卖声 |
| 第三方介入（脚步声、开门声、说话声） | 外部世界入侵角色的沉默空间 | 角色独处时的沉默被门外的脚步声打破，被迫回到现实 |
| 动作触发声（放下杯子、拉开椅子、关门） | 角色做出决定，沉默因行动而结束 | 长时间沉默后，角色站起来，椅子发出一声响，沉默结束 |
| 母题声音回归 | 沉默后母题的再次出现标记叙事节点 | 对决后的沉默被远处的钟声打破——钟声是本片的声音母题 |

## Sound Motif Cross-Episode Strategy

声音母题是跨集听觉一致性的核心工具：

### Motif Lifecycle

| phase | description | execution |
| --- | --- | --- |
| `seeding` | 母题首次出现，观众尚不知道它是母题 | 母题以自然环境声的形式出现，不加特殊处理 |
| `recognition` | 母题再次出现，观众开始注意到"又是这个声音" | 母题在关键时刻出现，开始与特定主题、角色或情绪关联 |
| `variation` | 母题发生变奏——音高、节奏、音色、远近或上下文改变 | 变奏本身传达叙事变化（如母题变慢暗示时间感变化、变远暗示角色疏离） |
| `absence` | 母题在其预期出现的位置缺席 | 缺席比出现更有力——当观众期待母题出现但它不在时，缺席本身就是信息 |
| `climax_return` | 母题在关键高潮以最完整或最极端的形式回归 | 母题的高潮回归可以承载整部作品的情感重量 |
| `final_transformation` | 母题在终集/终场的最终变奏或消失 | 母题的结局呼应作品的结局——可以回归初始形态（圆满）、消失（失去）、或变成完全不同的东西（成长） |

### Motif Selection Rules

- 声音母题必须来自叙事世界本身（环境声、物件声、自然声、人物习惯声），不得是外部配乐。
- 声音母题必须与叙事主题有内在联系（如水声与记忆/时间、钟声与命运/规则、风声与自由/孤独）。
- 声音母题不能过于频繁出现（每集都出现会失去力量）；关键集出现、日常集缺席的节奏更有效。
- 声音母题的变奏必须有叙事理由，不能只为了"听觉多样性"而变奏。

## Sound and Emotional Rhythm

声音设计与情绪节奏的关系：

| emotional phase | sound strategy | silence strategy |
| --- | --- | --- |
| 蓄力/积累 | 声音层次逐渐增加或逐渐减少（不是突然变化），环境声密度提高或降低 | 不使用沉默，但可以使用"接近沉默"——环境声压到极低，只有底层嗡鸣 |
| 临界/拐点 | 声音突然变化（突然安静或突然出现），或声音视角从客观切到主观 | 使用 `fleeting` 或 `brief` 沉默作为拐点标记 |
| 高潮/释放 | 声音密度最大化或最小化（取决于高潮类型），声音母题可能回归 | 高潮前可使用 `brief` 到 `sustained` 沉默蓄力；高潮后可使用 `sustained` 沉默承托余韵 |
| 余波/消化 | 声音逐渐回归日常水平，但带着高潮留下的痕迹（某个声音消失了、某个声音变远了） | 高潮后的 `sustained` 沉默是消化期的核心工具 |
| 过渡/日常 | 声音回归场景自然声，不施加特殊处理 | 不在日常过渡场景中使用设计过的沉默（沉默需要叙事重量才有意义） |

## Boundary

**允许**：

- 为关键场景建立 `sound_plan`，说明主导声音、缺席声音、母题变化和沉默策略。
- 利用声音母题的跨集出现、变奏和缺席制造听觉一致性。
- 在声音视角和现实状态之间切换，但切换必须绑定明确的叙事 beat。
- 利用沉默作为叙事工具，设计沉默的出现时机、感知时长和打破方式。
- 利用声音桥接实现场景间的流畅过渡。

**禁止**：

- 把 `sound_plan` 写成 BGM 风格标签（"紧张的弦乐""温暖的钢琴""悲伤的提琴"）。声音设计必须来自场景世界，不是配乐推荐。
- 把沉默当成"没有声音设计"来处理。沉默是最强的声音设计，必须有 `when`、`duration_feel`、`broken_by` 和 `what_silence_conveys`。
- 让声音与场景身份无关。`dominant_sound` 必须来自场景的空间功能、年代、材质和人物活动。
- 随机切换声音视角。从客观切到主观必须有叙事触发（信息冲击、情绪临界、创伤显影）。
- 让声音母题过于频繁出现，失去标记功能。
- 越过音频制作边界，指定具体的音效参数、混响时间、频率范围或混音方案。

## Evidence Contract

执行报告中的 `sound_design_directive` 必须包含：

```yaml
sound_design_directive:
  motif_plan:
    primary_motif: ""          # 主声音母题是什么
    motif_source: ""           # 母题来自叙事世界的什么
    motif_thematic_link: ""    # 母题与叙事主题的联系
    motif_lifecycle_phase: "seeding | recognition | variation | absence | climax_return | final_transformation"
    episode_appearances:       # 本集母题出现/缺席记录
      - scene_id: ""
        status: "present | varied | absent"
        variation_description: ""  # 若为变奏，说明变奏方式
        source_anchor: ""
  scene_sound_plans:
    - scene_id: ""
      source_anchor: ""
      dominant_sound: ""
      absent_sound: ""
      sound_motif_variation: ""
      subjective_sound_shift: ""
      silence_as_narrative:
        appears: true/false
        when: ""
        duration_feel: ""
        broken_by: ""
        what_silence_conveys: ""
      sound_perspective: ""
      sound_reality_status: ""
      directorial_intent: ""
  cross_episode_continuity:
    motif_carry_forward: ""     # 母题从上集如何延续到本集
    motif_setup_for_next: ""    # 本集母题如何为下集铺垫
    silence_pattern: ""         # 本集沉默模式与近邻集的关系
  risk_check:
    sound_as_bgm_label: false         # 是否把声音写成了 BGM 标签
    silence_undesigned: false          # 沉默是否缺乏设计
    sound_not_from_scene: false        # 声音是否来自场景身份
    motif_overuse: false               # 母题是否出现过于频繁
    subjective_shift_random: false     # 主观切换是否有叙事触发
    directorial_intent_is_technical: false  # 意图是否写成了技术描述
```

## Failure Cases

### Failure 1: 声音只是 BGM 标签

**症状**：`sound_plan` 的 `dominant_sound` 写成"紧张的弦乐""温暖的钢琴""悲伤的音乐"等配乐风格标签，不是来自场景世界的声音。

**诊断**：`2-编导` director layer 把声音设计等同于配乐选择，没有把声音当成场景世界的一部分。

**修复**：回到 `dominant_sound`，用来自场景空间功能、年代、材质和人物活动的具体声音替换 BGM 标签。例如"紧张的弦乐"→"荧光灯管的低频嗡鸣"、"温暖的钢琴"→"灶台上水壶的咕嘟声"、"悲伤的音乐"→"远处教堂的钟声穿过雨幕"。

**验证**：执行报告中每个 `dominant_sound` 都来自场景世界的物理声源，不是配乐风格描述。

### Failure 2: 沉默没有设计

**症状**：场景中出现了沉默，但 `silence_as_narrative` 的字段为空或只写了"此处沉默"，没有说明何时、多久、被什么打破、传达什么。

**诊断**：`2-编导` director layer 把沉默当成了"没有声音"的默认状态，没有把它当成需要设计的叙事工具。

**修复**：回到 `silence_as_narrative`，为每个设计过的沉默填写完整的 4 项：`when`（出现在哪个 beat）、`duration_feel`（感知时长）、`broken_by`（被什么打破，必须是场景内有物理来源的声音）、`what_silence_conveys`（传达什么叙事信息）。

**验证**：执行报告中每个 `silence_as_narrative.appears: true` 的场景，4 项字段全部填写且 `broken_by` 来自场景世界。

### Failure 3: 声音不来自场景身份

**症状**：`dominant_sound` 或 `absent_sound` 与场景的空间功能、年代、材质和人物活动无关，是泛化的"环境音"描述。

**诊断**：`2-编导` director layer 没有把声音与 `scene_identity_seed`（场景身份种子）关联，声音脱离了场景的具体身份。

**修复**：回到场景的 `scene_identity_seed`，根据空间功能（审讯室/家庭餐厅/校园操场）、年代（古代/当代）、材质（木门/瓷砖/旧墙皮）和环境声底色（荧光灯嗡鸣/门外餐厅闷响/老楼水管声）重新定义 `dominant_sound`。

**验证**：执行报告中每个 `dominant_sound` 能与该场景的 `scene_identity_seed` 对应，不是泛化描述。

### Failure 4: 声音母题过于频繁出现

**症状**：声音母题在每一集甚至每一个场景都出现，观众对母题产生疲劳，母题失去了标记功能。

**诊断**：`2-编导` director layer 认为声音母题"越多越好"，没有控制母题出现的节奏。

**修复**：回到 `motif_plan.episode_appearances`，减少母题出现频率。关键集出现、日常集缺席的节奏更有效。每集母题出现不超过 2 次（含变奏和缺席标记）。

**验证**：执行报告中 `episode_appearances` 的母题出现（`present` + `varied`）不超过 2 次，缺席（`absent`）至少 1 次。

### Failure 5: 主观声音切换没有叙事触发

**症状**：声音从客观突然切到主观（环境声变远、耳鸣出现、声音扭曲），但没有绑定任何叙事 beat（信息冲击、情绪临界、创伤显影），切换是随机的。

**诊断**：`2-编导` director layer 为了"增加主观感"而随意切换声音现实状态，没有追踪切换的叙事触发。

**修复**：回到 `subjective_sound_shift`，找到触发切换的具体 beat。若找不到叙事触发，恢复客观声音。

**验证**：执行报告中每个 `subjective_sound_shift` 不为空的场景，都有明确的叙事触发事件和 `source_anchor`。

### Failure 6: 沉默被打断的声音来自配乐

**症状**：`silence_as_narrative.broken_by` 写成了"音乐渐入""弦乐轻起""背景音乐回来"等配乐描述，不是场景内有物理来源的声音。

**诊断**：`2-编导` director layer 没有把打破沉默的声音限制在场景世界内，用配乐替代了场景声音。

**修复**：回到 `broken_by`，用场景内有物理来源的声音替代配乐。例如"音乐渐入"→"远处传来的晨钟"、"弦乐轻起"→"雨滴重新落在窗台上的声音"。

**验证**：执行报告中每个 `broken_by` 都有明确的物理声源，不是配乐描述。

## Reusable Heuristics

- 声音消失比声音出现更有力。当观众习惯的声音突然消失，注意力被强制聚焦，不安感从身体内部产生。
- 沉默是最强的声音设计。沉默不是"没有声音设计"，而是把所有设计的能量集中在"什么都没有"上。
- 声音必须来自场景世界，不是来自配乐库。角色听到的声音和观众听到的声音应该共享同一个物理空间。
- 声音母题的力量在于稀有性。出现越多越廉价，缺席一次抵过出现十次。
- 主观声音是角色心理的外化。当角色的世界在崩塌，声音也应该崩塌——变远、变闷、变扭曲、被耳鸣覆盖。
- 场景之间的声音桥接比画面剪辑更平滑。声音先行（下一场的声音提前进入）和声音拖尾（上一场的声音延续）可以让观众在不知不觉中完成场景过渡。
- 沉默被打断的方式本身就是叙事。一声微弱的鸟鸣意味着世界仍在运转；一声暴力的撞击意味着现实入侵。
- 最好的声音设计是观众事后才意识到的。如果观众在现场注意到声音设计，它可能太刻意了；如果观众在角色沉默时屏住呼吸，声音设计就成功了。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 关键场景是否形成 `sound_design_directive` / `sound_plan`，且声音作为叙事策略存在？ | `GATE-DIR-14` | `FAIL-SOUND-DESIGN-DIRECTIVE` | `N7-DIR-AESTHETIC` | `sound_design_directive.scene_sound_plans`、`directorial_intent` |
| `dominant_sound` 和 `absent_sound` 是否来自场景身份与物理声源，而非 BGM 风格标签？ | `GATE-DIR-14` | `FAIL-SOUND-DESIGN-DIRECTIVE` | `N7-DIR-AESTHETIC` / `N3-DIR-SUBSTANCE` | `scene_identity_seed`、`dominant_sound`、`risk_check.sound_as_bgm_label: false` |
| 沉默是否被设计为叙事工具，`when/duration_feel/broken_by/what_silence_conveys` 完整且 `broken_by` 来自场景世界？ | `GATE-DIR-14` | `FAIL-SOUND-DESIGN-DIRECTIVE` | `N7-DIR-AESTHETIC` | `silence_as_narrative`、`risk_check.silence_undesigned: false` |
| 声音母题是否有来源、主题关联、生命周期和受控出现频率，没有过度使用？ | `GATE-DIR-14` | `FAIL-SOUND-DESIGN-DIRECTIVE` | `N7-DIR-AESTHETIC` | `motif_plan`、`episode_appearances`、`risk_check.motif_overuse: false` |
| 主观声音切换是否绑定信息冲击、情绪临界或创伤触发，没有随机切换？ | `GATE-DIR-14` | `FAIL-SOUND-DESIGN-DIRECTIVE` | `N7-DIR-AESTHETIC` | `subjective_sound_shift`、`sound_perspective`、`sound_reality_status`、`source_anchor` |
| 声音策略是否能供 `2-编导` performance layer 的 ambient support 消费，但没有越过音频制作参数边界？ | `GATE-DIR-14` | `FAIL-SOUND-DESIGN-DIRECTIVE` | `N7-DIR-AESTHETIC` / `N9-DIR-DRAFT` | `sound_design_directive.cross_episode_continuity`、`risk_check.directorial_intent_is_technical: false` |
