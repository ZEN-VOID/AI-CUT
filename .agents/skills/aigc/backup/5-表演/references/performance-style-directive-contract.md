# Performance Style Directive Contract

## Purpose

本合同定义 `2-编导` director layer 的表演风格基调规划。它在导演层为每个关键角色建立表演风格基线、风格转变触发条件和转变目标，供 `2-编导` performance layer 消费后转化为具体的五层表演控制变量。

表演风格不是情绪标签，而是导演对"这个角色在这部戏里如何存在于镜头前"的整体判断。它决定角色的表达方式、身体控制、声音质感和表里关系，让 `2-编导` performance layer 在逐场执行时有风格锚点，而不是每次都从零判断。

本文件不授权新增剧情事实、对白、事件结果、人物动机、摄影方案或声音设计细节。

## Ownership

- 本文件拥有表演风格四轴定义、角色风格基线、风格转变规则、类型默认基线、风格-表演层映射和证据结构。
- `directorial-authorship-contract.md` 负责编导创作内核中的 `performance_engine`（单场表演指令）；本文件负责角色跨集的风格基调一致性。
- `actor-performance-control-contract.md` 负责五层表演控制的逐 beat 执行；本文件为其提供风格层面的约束参数。
- `performance-and-scene-craft-contract.md` 负责场景状态差和演员任务；本文件的风格基线会影响演员任务的执行方式。
- `climax-visual-treatment-contract.md` 负责高潮画面的兑现模式；本文件的风格转变可能在高潮场景中触发。
- `hollywood-quality-spec.md` 负责顶层质量标准；本文件的风格规划必须满足其"可演"维度。

## Dependency Graph

```
performance-style-directive-contract.md
├── consumed_by: N3-DIR-SUBSTANCE (形成风格基线判断)
├── consumed_by: N7-DIR-AESTHETIC (风格基线进入 scene_dramatic_map)
├── consumed_by: N9-DIR-DRAFT (风格基线内嵌到角色行为)
├── consumed_by: N10-DIR-REVIEW (验证风格一致性)
├── consumed_by: 2-编导 performance layer (风格基线约束五层表演控制)
├── produces:
│   └── performance_style_directive (必须产出，含 per-character style_baseline / style_shift_triggers / shift_target)
└── cross_reference:
    └── directorial-authorship-contract.md (performance_engine 协调)
```

## Performance Style Axes

表演风格沿四个独立轴定义，每个轴是一个连续光谱，而非二元选择。角色的风格基线在每个轴上有一个定位点，当场景触发转变时，沿该轴向目标点移动。

| axis | left pole | center range | right pole | what it controls |
| --- | --- | --- | --- | --- |
| `expressiveness` | 极度克制：情绪内化，面部肌肉几乎不动，反应延迟或压制 | 自然主义：情绪按生活逻辑自然流露，不放大不压制 | 外放表达：情绪主动外显，表情幅度大，身体语言丰富 | 情绪的表达程度——角色把内心状态在多大程度上让观众看见 |
| `physicality` | 静态内敛：极少动作，身体像被定住，变化只在微处 | 精准控制：动作有目的，每一下都服务于目标，留白与动作交替 | 丰富肢体：动作幅度大，身体参与表达，空间利用率高 | 身体的参与度——角色用身体与世界交互的密度和幅度 |
| `vocal_style` | 低沉克制：声音压低，句子短，停顿长，音量小，气息重 | 日常自然：声线按生活逻辑变化，有起伏但不刻意 | 高亢激昂：声音明亮或尖锐，语速变化大，音量波动明显 | 声音的表达方式——角色用声音传递信息和情绪的方式 |
| `mask_vs_authentic` | 深层伪装：观众看到的与角色真实状态完全相反，需要多个 beat 才能识破 | 部分隐瞒：角色暴露部分真实，隐藏关键，表面与内心有裂隙 | 完全坦露：角色的状态、意图和情绪对观众透明 | 表里关系——角色在多大程度上对镜头坦露真实自我 |

### Axis Combination Patterns

四轴不是独立滑块；常见组合有内在一致性：

| pattern | expressiveness | physicality | vocal_style | mask_vs_authentic | typical character |
| --- | --- | --- | --- | --- | --- |
| `stoic_guardian` | 极度克制 | 精准控制 | 低沉克制 | 深层伪装 | 隐忍的保护者、资深卧底、沉默型领袖 |
| `open_heart` | 外放表达 | 丰富肢体 | 高亢激昂 | 完全坦露 | 热血青年、天真角色、崩溃时刻的角色 |
| `calculated_charm` | 自然主义 | 精准控制 | 日常自然 | 深层伪装 | 社交高手、政治人物、表面温和的操控者 |
| `wounded_quiet` | 极度克制 | 静态内敛 | 低沉克制 | 部分隐瞒 | 创伤幸存者、内疚者、被迫沉默的知情者 |
| `volatile_force` | 外放表达 | 丰富肢体 | 高亢激昂 | 部分隐瞒 | 暴躁但有隐情的角色、外强中干的角色 |
| `slow_burn` | 极度克制→自然主义 | 静态内敛→精准控制 | 低沉克制→日常自然 | 深层伪装→部分隐瞒 | 长线成长角色，风格随剧情逐步打开 |

注意：`slow_burn` 不是风格基线，而是风格弧。它需要 `style_arc_plan` 定义每集的轴位移量。

## Per-Character Style Directive Structure

每个关键角色（主角、主要对手、关键配角）必须形成 `performance_style_directive`：

```yaml
performance_style_directive:
  character_id: ""
  character_name: ""
  source_anchor: ""  # 回指上游角色设定锚点
  style_baseline:
    expressiveness: ""       # 轴上定位 + 一句话依据
    physicality: ""
    vocal_style: ""
    mask_vs_authentic: ""
    combination_pattern: ""  # 匹配哪种 pattern，或说明为何是独特组合
    baseline_evidence: ""    # 为什么这个角色是这个基线，来自上游哪个设定、经历或关系
  style_shift_triggers:
    - trigger_event: ""      # 什么事件触发风格转变
      affected_axes: []      # 哪些轴发生变化
      shift_direction: ""    # 向光谱哪端移动
      shift_magnitude: "subtle | moderate | dramatic"  # 移动幅度
      source_anchor: ""      # 回指上游触发事件
  shift_target:
    - triggered_by: ""       # 对应哪个 trigger_event
      target_style:
        expressiveness: ""
        physicality: ""
        vocal_style: ""
        mask_vs_authentic: ""
      recovery_pattern: ""   # 转变后是否回到基线、停留在新位置、还是继续偏移
  style_arc_plan:            # 仅 slow_burn 或长弧角色需要
    episode_1_position: ""
    midpoint_target: ""
    finale_position: ""
    arc_evidence: ""         # 上游角色成长弧依据
```

## Genre Default Baselines

不同类型片有默认表演风格基线。角色风格规划应参考类型默认值，但角色设定优先级高于类型默认值。

| genre | expressiveness | physicality | vocal_style | mask_vs_authentic | rationale |
| --- | --- | --- | --- | --- | --- |
| 悬疑/推理 | 自然主义偏克制 | 精准控制 | 日常自然偏低沉 | 部分隐瞒偏深层伪装 | 信息差驱动叙事，角色不能太透明 |
| 动作/冒险 | 自然主义偏外放 | 丰富肢体 | 日常自然 | 部分隐瞒偏坦露 | 身体参与度高，但角色可以有隐藏动机 |
| 都市情感 | 自然主义 | 精准控制 | 日常自然 | 部分隐瞒 | 情感驱动，角色之间的坦诚度是核心张力 |
| 悬疑恐怖 | 极度克制偏自然 | 静态内敛偏精准 | 低沉克制偏日常 | 深层伪装偏隐瞒 | 恐惧来自未知，角色表达被压制 |
| 古装权谋 | 极度克制 | 精准控制 | 低沉克制 | 深层伪装 | 权力场中情绪是弱点，伪装是生存策略 |
| 喜剧 | 自然主义偏外放 | 丰富肢体 | 日常自然偏高亢 | 完全坦露偏部分 | 喜剧角色通常对观众坦露，但可能对其他角色隐藏 |
| 科幻/奇幻 | 自然主义 | 精准控制 | 日常自然 | 部分隐瞒 | 异世界规则下角色仍需可信的人类行为基准 |
| 现实主义 | 自然主义 | 自然主义偏精准 | 日常自然 | 部分隐瞒偏坦露 | 生活质感优先，过度风格化破坏真实感 |
| 惊悚/犯罪 | 极度克制 | 精准控制 | 低沉克制 | 深层伪装 | 高压环境下情绪控制是生存本能 |
| 青春/校园 | 自然主义偏外放 | 自然主义 | 日常自然偏高亢 | 完全坦露偏部分 | 年轻角色的情绪管理能力较低，更直接 |

### Genre Baseline Usage Rules

- 类型默认基线是起始参考点，不是强制执行值。角色设定明确要求不同风格时，角色优先。
- 同一集中若混合类型（如悬疑+情感），不同场景可以沿不同轴偏移，但角色基线不变。
- 类型默认基线的偏离必须有上游角色设定支撑，不得因为"更有层次"而随机偏移。

## Style-to-Performance Layer Mapping

风格基线如何影响 `2-编导` performance layer 的五层表演控制：

| performance layer | expressiveness impact | physicality impact | vocal_style impact | mask_vs_authentic impact |
| --- | --- | --- | --- | --- |
| `emotion_trigger` | 克制型角色的触发需要更具体的上游事件，自然主义型角色可以被更微妙的信号触发 | 不影响触发本身 | 不影响触发本身 | 伪装型角色的真实触发可能被表面反应掩盖 |
| `inner_motive` | 克制型角色的动机更难从外部观察，需要更多 beat 积累 | 不影响动机本身 | 不影响动机本身 | 伪装型角色的表面动机与真实动机分离 |
| `micro_expression` | 克制型：表情幅度小，变化集中在眼睛和嘴角；外放型：面部全域参与 | 静态型：表情是唯一信号源；丰富型：表情与身体同步 | 声音克制型：表情与声音不同步（嘴在动但声音晚半拍）；高亢型：表情与声音同步放大 | 伪装型：表情是面具，裂缝出现在嘴角、眉心或鼻翼；坦露型：表情即状态 |
| `body_linkage` | 克制型：身体变化幅度小，延迟长；外放型：身体即时响应 | 静态型：只在手指、呼吸、重心微处变化；精准型：关键动作一下到位；丰富型：全身参与 | 低沉型：身体配合声压，整体收缩；高亢型：身体配合声量，整体打开 | 伪装型：身体比脸更诚实（手泄露嘴在掩饰的信息） |
| `ambient_support` | 克制型角色场次：环境声更安静，声音层次更少，沉默更长；外放型角色场次：环境声可以更丰富 | 不直接影响环境声 | 低沉型角色的对白场景：环境声应压低以配合声线；高亢型角色的对白场景：环境声可以有更多层次 | 伪装型场景：环境声反映角色真实状态而非表面状态（角色说没事，但环境声开始变沉） |

## Style Shift Execution Rules

风格转变不是瞬间切换，而是有节奏的过程：

| shift type | execution rule | example |
| --- | --- | --- |
| `subtle` | 1-2 个 beat 内完成，观众可能不自觉感知，但回看时能发现 | 角色在听到某句话后，嘴角的微笑僵了半秒 |
| `moderate` | 2-4 个 beat 内完成，观众能感知到"他/她变了"，但不确定具体变了什么 | 角色在整场对话中身体逐渐从开放变为封闭 |
| `dramatic` | 单个 beat 内完成，观众明确感知到风格断裂，这本身就是叙事事件 | 角色在压力临界点突然从克制变为爆发，或从外放变为彻底沉默 |

约束：

- `subtle` 转变不需要声音或空间承托，纯粹靠表演完成。
- `moderate` 转变可以有环境声配合（声音变轻或变重），但不强制。
- `dramatic` 转变必须有至少 1 个非表演承托（环境声变化、空间距离变化、群像反应、道具状态变化），因为风格断裂本身是叙事事件，需要全场感知。
- 风格转变后的 `recovery_pattern` 必须明确：是回到基线（临时偏离）、留在新位置（永久转变）、还是继续偏移（螺旋式变化）。

## Multi-Character Style Interaction

同一场景中多个角色的风格基线差异本身就是叙事张力来源：

| interaction pattern | description | directorial use |
| --- | --- | --- |
| `style_collision` | 两个角色在同轴上处于对立端（如克制 vs 外放） | 对话场面中，一方的沉默成为另一方的压力源 |
| `style_mirroring` | 两个角色风格相似，但动机不同 | 让观众难以判断谁在伪装、谁在真诚 |
| `style_infection` | 角色 A 的风格开始影响角色 B | 角色 B 在与 A 相处后开始变得克制或变得外放 |
| `style_contrast` | 场景内切换不同角色的风格焦点 | 切到克制型角色时环境变安静，切到外放型角色时环境变丰富 |

## Boundary

**允许**：

- 为每个关键角色建立四轴风格基线，并说明来自上游哪个角色设定或经历。
- 为风格转变定义触发事件、转变方向和恢复模式。
- 为不同类型片定义默认基线，供角色风格规划参考。
- 说明风格基线如何影响五层表演控制的每一层。
- 在多角色场景中利用风格差异制造叙事张力。

**禁止**：

- 为了"更有层次"而随机偏移类型默认基线，没有上游角色设定支撑。
- 把风格基线写成情绪标签（如"他很冷酷""她很热情"），而不是可被演员执行的表达方式。
- 让所有角色共享同一风格基线，抹平角色间的表演差异。
- 把风格转变写成结论（如"他变了"），而不说明具体哪条轴向哪个方向移动了多少。
- 越过 `2-编导` performance layer 的边界，直接规定微表情细节或对白表演方式。
- 越过摄影边界，把风格表达写成机位、景别或镜头运动方案。

## Evidence Contract

执行报告中的 `performance_style_directive` 必须包含：

```yaml
performance_style_directive:
  character_id: ""
  character_name: ""
  source_anchor: ""
  style_baseline:
    expressiveness:
      position: ""           # 轴上定位
      evidence: ""           # 上游依据
    physicality:
      position: ""
      evidence: ""
    vocal_style:
      position: ""
      evidence: ""
    mask_vs_authentic:
      position: ""
      evidence: ""
    combination_pattern: ""
    baseline_evidence: ""
  genre_reference:
    genre: ""
    default_baseline_match: true  # 是否与类型默认基线一致
    deviation_reason: ""          # 若不一致，偏离原因
  style_shift_triggers:
    - trigger_event: ""
      affected_axes: []
      shift_direction: ""
      shift_magnitude: ""
      source_anchor: ""
  shift_target:
    - triggered_by: ""
      target_style:
        expressiveness: ""
        physicality: ""
        vocal_style: ""
        mask_vs_authentic: ""
      recovery_pattern: ""
  style_interaction:
    co_scene_characters: []
    interaction_pattern: ""
    interaction_evidence: ""
  risk_check:
    all_characters_same_style: false  # 是否所有角色风格雷同
    genre_mismatch: false             # 风格与类型是否不符
    shift_without_trigger: false      # 风格转变是否有触发事件
    style_as_emotion_label: false     # 是否把风格写成了情绪标签
    upstream_anchor_missing: false    # 是否有风格判断无法回指上游
```

## Failure Cases

### Failure 1: 所有角色同一风格

**症状**：主要角色的四轴基线几乎相同，观众无法通过表演风格区分不同角色。

**诊断**：`2-编导` director layer 没有为每个关键角色分别建立风格基线，或者直接套用了类型默认基线而没有根据角色设定差异化。

**修复**：回到每个角色的 `style_baseline`，检查其 `baseline_evidence` 是否来自上游角色设定、经历、关系或社会位置。若两个角色风格基线过于接近，至少在 1 个轴上拉开差异，并说明差异依据。

**验证**：执行报告中任意两个主要角色的 `style_baseline` 至少在 2 个轴上有明确不同，且差异有上游依据。

### Failure 2: 风格与类型不符

**症状**：角色的风格基线与作品类型明显冲突（如现实主义剧中角色极度外放且完全坦露），但没有角色设定层面的特殊理由。

**诊断**：`2-编导` director layer 没有参考 `genre_reference`，或者故意偏离类型默认基线但缺少上游角色设定支撑。

**修复**：回到 `genre_reference`，确认偏离是否有角色设定层面的正当理由。若无，将角色风格拉回类型默认范围。若有，记录 `deviation_reason`。

**验证**：执行报告中每个 `genre_reference.deviation_reason` 不为空（对于偏离类型默认基线的角色），且理由来自上游角色设定。

### Failure 3: 风格转变没有触发事件

**症状**：角色在某场戏中风格发生了变化，但没有对应的上游事件、信息、关系变化或压力升级作为触发。

**诊断**：`2-编导` director layer 把风格转变当成了叙事节奏需要（"该变了"），而不是角色面对真实压力后的反应。

**修复**：回到 `style_shift_triggers`，为每个转变找到上游 `trigger_event` 和 `source_anchor`。若找不到，该转变不应发生。

**验证**：执行报告中每个 `style_shift_triggers` 条目都有可回指上游的 `source_anchor`。

### Failure 4: 风格基线是情绪标签而非表演方式

**症状**：`style_baseline` 写成"冷酷""温柔""阴郁"等情绪词汇，演员无法据此判断自己的表达方式、身体控制和声音质感。

**诊断**：`2-编导` director layer 把风格基线当成了人物性格描述，而不是导演对表演方式的判断。

**修复**：回到四轴，用光谱上的具体定位替换情绪标签。例如"冷酷"→`expressiveness: 极度克制（情绪内化，面部变化只在眉心和嘴角）`、`physicality: 精准控制（动作少但每一下有目的）`、`vocal_style: 低沉克制（声音压低，句子短，停顿长）`、`mask_vs_authentic: 深层伪装（表面冷漠掩盖保护欲）`。

**验证**：执行报告中每个 `style_baseline` 的四个轴都有光谱定位和具体说明，不是情绪形容词。

### Failure 5: 风格转变后缺少恢复模式

**症状**：角色在某场戏中风格发生转变，但没有说明转变后是回到基线、留在新位置还是继续偏移，导致 `2-编导` performance layer 在下一场戏中无法确定表演方式。

**诊断**：`2-编导` director layer 只关注转变瞬间，没有追踪转变后的落点。

**修复**：回到 `shift_target`，为每个转变补充 `recovery_pattern`：`return_to_baseline`（回到基线，下一场恢复原样）、`permanent_shift`（留在新位置，后续场次使用新基线）、`continued_drift`（继续偏移，需要 `style_arc_plan`）。

**验证**：执行报告中每个 `shift_target` 条目都有明确的 `recovery_pattern`。

### Failure 6: 多角色场景风格碰撞未被利用

**症状**：同一场景中两个角色风格差异明显（如克制型面对外放型），但导演没有利用这种差异制造叙事张力，场景中风格差异没有产生任何压力。

**诊断**：`2-编导` director layer 分别规划了角色风格，但没有在 `style_interaction` 中识别风格碰撞的机会。

**修复**：回到 `style_interaction`，检查同场景角色的风格基线差异，利用差异制造至少 1 个叙事张力点（如克制型角色的沉默对另一方形成压力、外放型角色的情绪冲击让伪装型角色的面具出现裂缝）。

**验证**：执行报告中 `style_interaction` 的 `interaction_pattern` 有具体说明，不是只列出了角色名单。

## Reusable Heuristics

- 表演风格是角色的存在方式，不是角色的情绪状态。"冷酷"不是风格，"在镜头前几乎不动但眼睛一直在追踪对手的微表情"才是风格。
- 克制比外放更难演，也更有信息密度。默认偏克制，只有触发事件出现时才打开。
- 伪装型角色的力量在于裂缝：不是一直伪装，而是在某个瞬间伪装被撕开。风格转变的戏剧价值在于伪装裂缝的时机。
- 多角色场景中，风格差异比风格一致更有戏。两个克制型角色对坐不如一个克制型面对一个外放型。
- 风格基线不是监狱。角色可以在基线附近微幅波动，这本身就是"活人感"的一部分。风格基线是重心，不是牢笼。
- 沉默型角色不是没有表演的角色。沉默型角色的表演密度可能比外放型更高，因为每一个微小变化都被放大。
- 类型默认基线是起跑线，不是天花板。偏离默认基线的角色之所以有力量，恰恰因为其他角色在默认位置上。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 关键角色是否都有 `performance_style_directive`，四轴基线可被 `2-编导` performance layer 消费？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` | `performance_style_directive.style_baseline`、`baseline_evidence` |
| 角色风格是否不是情绪标签，而是 expressiveness/physicality/vocal_style/mask_vs_authentic 的可执行定位？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` | 四轴 `position` 与 `evidence`、`risk_check.style_as_emotion_label: false` |
| 类型默认基线的偏离是否有上游角色设定、经历或关系支撑？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` | `genre_reference.deviation_reason`、`source_anchor` |
| 风格转变是否有上游触发事件、影响轴、移动方向、幅度和恢复模式？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` / `N9-DIR-DRAFT` | `style_shift_triggers`、`shift_target.recovery_pattern` |
| 多角色场景是否利用风格碰撞/映照/感染/对比制造叙事压力，而非只列角色名单？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` / `N7-DIR-AESTHETIC` | `style_interaction.interaction_pattern`、`interaction_evidence` |
| 所有主要角色是否没有共享同一风格基线，至少在关键轴上形成有据差异？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` | `risk_check.all_characters_same_style: false`、角色风格差异对照 |
