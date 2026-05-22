# Visual Aesthetic Contract

## Purpose

本细则定义 `3-导演` 的画面美学层：在编剧保真、导演创作内核、高潮承托和受控增强边界成立之后，进一步组织画面的审美品质、景境层次和情绪承托。

它不是摄影方案，不写机位、景别、镜头运动、分镜编号或图像提示词；它也不是自由改写授权，不新增剧情事实、对白、事件、规则、线索、因果或结果。

## Ownership

- 本文件拥有单场画面美学的组织规则、字段集成规范、证据结构和越权检测。
- `episode-visual-spine-contract.md` 负责整集视觉主轴；本文件负责单场如何呼应、变奏或克制整集主轴。
- `atmosphere-and-mood-contract.md` 负责五感氛围和意境技法；本文件消费其五感框架和 6 种意境技法。
- `controlled-enrichment-contract.md` 负责 B 路线的承托增强；景境增强需通过其风险检查并记录 ledger。
- `hollywood-quality-spec.md` 负责顶层质量标准；本文件负责画面密度和节奏控制维度的达标。

## Dependency Graph

```
visual-aesthetic-contract.md
├── consumed_by: N7-DIR-AESTHETIC (单场美学执行)
├── consumed_by: N9-DIR-DRAFT (内嵌终稿)
├── consumed_by: N10-DIR-REVIEW (验证画面美学质量)
├── consumes:
│   ├── episode-visual-spine-contract.md (整集视觉主轴)
│   ├── atmosphere-and-mood-contract.md (五感框架和意境技法)
│   └── controlled-enrichment-contract.md (B路线风险检查)
└── produces:
    └── visual_aesthetic_pass (单场美学证据)
```

## Visual Aesthetic Pass

单场美学必须消费 `references/episode-visual-spine-contract.md` 形成的 `episode_visual_spine`，判断本场要呼应、变奏还是克制整集视觉主轴。

关键场景、强情绪场、压迫场、离别场、高潮场和类型氛围场执行 `visual_aesthetic_pass`，形成以下规划证据，再内嵌进既有字段：

| axis | question | output evidence |
| --- | --- | --- |
| `visual_tone` | 本场画面气质是什么，冷峻、潮湿、肃杀、空旷、灼热、破败、明净或压抑？ | `atmospheric_palette` |
| `visual_core` | 本场最应该被观众记住的一个核心画面是什么？ | `core_image` |
| `image_hierarchy` | 主视觉、次视觉、背景细节分别承担什么？ | `primary_image / secondary_image / background_texture` |
| `motif_and_variation` | 是否有可重复但不机械重复的视觉母题，如门、火光、空席、雨线、纸张、血色、倒影、落尘？本场对整集母题是呼应、变奏还是克制？ | `image_motif_map` |
| `contrast_axis` | 本场靠什么产生审美张力：明/暗、静/动、近/远、冷/暖、空/满、软/硬、整洁/破败、喧闹/寂静？ | `contrast_axis_map` |
| `atmospheric_scenery` | 是否需要自然景物或景境细节衬托心境，如飘雪、落叶、朝露、风沙、雨丝、雾气、日影、火光、尘土？ | `scenic_support_plan` |
| `rhythm_and_negative_space` | 哪些画面需要快、慢、停半拍、骤然爆发或留白？ | `visual_rhythm_notes` |
| `restraint` | 哪些地方不该堆砌形容、比喻或符号，应该保留朴素、空白或沉默？ | `restraint_notes` |
| `transition_variety` | 场景转场和下一场压力是否只能靠人物看远方？能否改由声音、道具、群像、空间或环境刷新承担？ | `transition_support_plan` |
| `atmosphere_mood` | 本场需要什么情绪氛围？用哪些五感通道和意境技法承托？详见 `references/atmosphere-and-mood-contract.md`。 | `atmosphere_mood_evidence` |

## Field Integration Rules

`visual_aesthetic_pass` 不新增终稿字段，只为既有字段提供审美组织：

| target field | aesthetic responsibility |
| --- | --- |
| `环境描写` | 写场景本身的景境层次：空间、光线、天气、自然景物、空气介质、材质、静置物件和整体氛围。可在同一 slugline 内随空间/背景/光线/空气/材质焦点变化重复刷新；不得写人物动作、对白引出、剧情结果或心理解释。可按 `atmosphere-and-mood-contract.md` 使用五感细节（光线纹理、空气湿度、声音质感、气味、时间痕迹）和意境技法（通感、微观放大、反衬、声景层次、延时承托、留白）增强氛围密度。 |
| `角色动作` / `动作画面` | 写人物可拍动作的速度、力度、节奏和空间路径；审美来自动作节奏与姿态，不来自心理解释。 |
| `对白画面` | 写对白附近可见的视线、手部、距离、停顿、对手反应和环境压迫；引号内不加动作，字段正文不得输出说明性规则。 |
| `道具特写` | 让物件状态、痕迹、归属、规则文字或信息载体承载视觉信息；不得写成固定物件清单或推理结论。 |
| `群像画面` | 写群体密度、队形、迟疑、退避、围合、沉默或骚动；不要把群体反应塞进 `环境描写`。 |
| `心理反应` | 写内心状态，但必须有外部化锚点（详见本文件心理反应字段约束）。不得写无表演支撑的纯内心描述。 |
| 声音字段与对应画面字段 | 声音只写可听本体；画面可用空间余波、静物震动、众人反应或自然声后的空白承托声音。 |

## 心理反应字段约束

`心理反应` 字段是唯一允许写内心状态的字段，但必须满足以下约束：

### 必须有外部化锚点

`心理反应` 中的内心状态必须能在其他字段找到对应的外部化证据。

| 心理反应写法 | 对应外部化锚点 |
| --- | --- |
| "他感到不安" | `对白画面` 中视线回避、`角色动作` 中手指压纸/敲桌/握拳、`音效画面` 中声音消失或异常 |
| "她觉得被背叛" | `对白画面` 中沉默/距离变化、`群像画面` 中群体反应 |
| "他内心在挣扎" | `角色动作` 中犹豫动作/停顿、`环境描写` 中选择物的特写 |

### 禁止的写法

- 纯内心描述无外部化证据：`心理反应：他心里很矛盾，不知道该怎么办。`
- 用心理反应替代表演任务：`心理反应：她的内心在翻涌。`（应改为 `对白画面` 中的具体停顿、视线或手部动作）
- 用心理反应解释剧情：`心理反应：其实他早就知道了。`（这是旁白越权，不是心理反应）

### 允许的写法（有外部化锚点）

`心理反应：她忽然意识到自己说错了，但话已经出口。` + `对白画面：她说完后没有抬头，指尖在袖口边缘反复摩挲。`

（心理反应有外部化锚点：`对白画面` 中的"没有抬头"和"指尖摩挲"承托"说错话后的懊悔"）

## Aesthetic Enrichment Boundary

**允许**：

- 在不改变剧情条件的前提下，补足符合地点、时段、季节、类型气质和人物处境的景境细节。
- 同一场景标题下，开篇环境描写负责建立空间；后续若剧情从主厅转向角落、从屋内贴近门廊、从桌案转向窗边、从船舱走到船舷，或自然光、火光、雾气、雨声、尘土、墙面/地面/水面材质成为新的情绪背景，可再次使用 `环境描写` 做景境刷新。
- 使用自然景物衬托情绪，但只改变氛围密度，不制造新的障碍、线索、行动结果或规则条件。
- 让视觉母题反复出现并变化，例如同一盏灯从温暖变成刺眼，同一道门从出口变成封锁。
- 呼应或变奏整集视觉主轴，例如纸面、衣料、血色、海雾、袖口或空鞘在不同场景承担不同压力。
- 用对比轴提升审美张力，例如静物不动而人群躁动、室内烛火温暖而门外风雨冷硬。
- 让转场由声音、道具、群体动作、空间阻隔、环境刷新或未完成动作承担；只有当"看见"本身是剧情信息时，才让人物看向远方或地标。

**禁止**：

- 为了美而新增人物看见的新线索、突然出现的新道具、额外伤势、额外天气灾害或行动阻碍。
- 把"电影感""高级感""宿命感"等抽象评价直接写入终稿。
- 每个字段都堆形容词、比喻或符号，导致画面没有主次。
- 把摄影、分镜或图像提示词提前写入 `3-导演`。
- `心理反应` 字段没有外部化锚点。

## Weak-To-Strong Examples

弱：`环境描写：夜色压抑，气氛紧张。`

强：`环境描写：廊下灯火被风压得忽明忽暗，门槛外一线雨水沿石缝往里渗，墙面旧灰浮起潮痕。`

弱：`对白画面：说话者的视线、手部动作和对手反应承托对白。`

强：`对白画面：他说完后没有抬头，拇指在杯沿停住；对面的人把半开的门又推窄了一寸。`

弱：`对白画面：她没有看他，而是看向远方；他顺着她的视线望去。`

强：`对白画面：她把臂弯里的布料收紧，指尖停在折口；身后的欢呼声一点点散开。`

弱：`道具特写：密报很重要，说明有人背叛。`

强：`道具特写：纸角被汗水洇软，封口蜡印只剩半枚，折痕里露出一行被反复压过的墨字。`

弱：`心理反应：他心里很害怕，但强撑着。`

强：`心理反应：他心里知道这事瞒不住，但还有最后一个机会。` + `对白画面：他没有说话，签字的笔尖在纸面上停了三秒，最后落下的笔迹比平时轻了半度。`

（心理反应有外部化锚点：笔尖停顿和笔迹变轻承托"害怕但强撑"）

## Evidence Contract

执行报告中的 `visual_aesthetic_evidence` 必须包含：

```yaml
visual_aesthetic_evidence:
  scene_id: ""
  visual_tone: ""
  visual_core: ""
  image_hierarchy:
    primary_image: ""
    secondary_image: ""
    background_texture: ""
  motif_and_variation:
    episode_motif_strategy: "呼应 | 变奏 | 克制"  # 本场对整集母题的策略
    scene_motifs: []
    variation_note: ""  # 母题如何在本场变化
  contrast_axis_map: {}
  rhythm_and_negative_space:
    beats:
      - position: ""
        type: "快 | 慢 | 停半拍 | 骤然爆发 | 留白"
        description: ""
  restraint_notes: ""
  transition_support_plan: ""
  atmosphere_mood_evidence:
    - target_mood: ""
      technique_used: ""
      sensory_channels: {}
  risk_check:
    fact_drift: false
    dialogue_drift: false
    new_event: false
    abstract_aesthetic: false  # 是否有抽象审美词空转
    photography_overreach: false
    motif_mechanical_repetition: false  # 是否有母题机械重复
    psychological_reaction_no_anchor: false  # 心理反应是否无外部化锚点
```

## Failure Cases

### Failure 1: 画面美学变成抽象审美词集合

**症状**：`visual_tone` 写成"高级感"，`visual_core` 写成"好看的画面"，`contrast_axis` 写成"有质感"，无法落地为可拍描述。

**诊断**：N7-DIR-AESTHETIC 在建立 `visual_aesthetic_pass` 时跳过了具体化步骤，直接写了审美方向。

**修复**：回到每个 axis，用具体叙事内容替换审美方向。例如"高级感"→"冷峻：光线从窗棂切进来，把石板切成明暗分明的边界，灯管的光被压得很低"。

**验证**：执行报告中每个 `visual_aesthetic_evidence` 字段必须能被下游分解为可见/可听/可感的具体描述。

### Failure 2: 母题机械重复无变化

**症状**：同一物件（如"一盏灯"）在每个场景都出现，但每次只是"出现"，没有承担不同的压力、距离或情绪温度。

**诊断**：`visual_aesthetic_pass` 建立了母题链但没有为每项分配变化策略，没有选择本场对整集母题是呼应/变奏/克制。

**修复**：回到 `motif_and_variation` 轴，为每个母题注明变化策略：例如"灯在第1场是温暖光源（呼应压迫前夕），在第3场是刺眼光源（变奏审讯压力），在第7场是熄灭状态（克制代价余韵）"。

**验证**：执行报告中 `visual_aesthetic_evidence.motif_and_variation.episode_motif_strategy` 至少有一处明确的变奏或克制，不是所有场景都呼应。

### Failure 3: 转场过度依赖"看远方"

**症状**：连续多个场景使用"人物看向远方/顺着视线望去/地标飘动"作为转场承托，导致转场方式单一。

**诊断**：N7-DIR-AESTHETIC 没有主动寻找替代转场方式，默认使用视觉引导转场。

**修复**：回到 `transition_variety` 轴，为每个转场设计至少 2 种替代方案：声音转场（远处传来什么声音）、道具转场（物件状态变化）、群像转场（群体动作节奏）、空间转场（门/窗/廊的位置刷新）。只有在"看见本身是剧情信息"时才使用视觉引导。

**验证**：终稿中连续不超过 2 个场景使用相同的转场承托方式。

### Failure 4: 心理反应无外部化锚点

**症状**：`心理反应` 写了纯内心描述，但在其他字段找不到对应的外部化证据。

**诊断**：N7-DIR-AESTHETIC 或 N9-DIR-DRAFT 把 `心理反应` 当成独立字段，没有为每条内心状态在其他字段找对应的视线、手部、停顿、声音或空间反应。

**修复**：回到 N9-DIR-DRAFT，为 `心理反应` 中的每条内心状态补至少一个其他字段的外部化锚点。例如"他心里很难过"→"他没有说话，指节在桌沿敲了两下"。

**验证**：终稿中每个 `心理反应` 字段都必须在最近的对白画面、角色动作、环境描写或音效画面中有对应的外部化证据。

### Failure 5: 画面没有主次和节奏

**症状**：`环境描写` 每个句子都同等用力，没有主视觉、次视觉和背景纹理的层次区分，也没有快慢节奏设计。

**诊断**：N7-DIR-AESTHETIC 把所有景境细节平铺，没有建立 `image_hierarchy` 和 `rhythm_and_negative_space`。

**修复**：回到 `image_hierarchy`，为主视觉/次视觉/背景纹理分配不同的描述密度；回到 `rhythm_and_negative_space`，为关键节点设计延时承托或骤然加速。

**验证**：执行报告中每个关键场景的 `visual_aesthetic_evidence.image_hierarchy` 有明确的主次区分，`rhythm_and_negative_space` 有具体的节奏落点。

## Review Checklist

- 关键场景是否有可命名的 `visual_core`，而不是散乱堆砌细节？
- 本场是否合理消费 `episode_visual_spine`：呼应、变奏或克制整集母题？
- 画面是否有主次、对比和节奏，而不是每句都平均用力？
- 转场和下一场压力是否有多样承托，避免连续使用看向远方、顺着视线望去或地标飘动？
- `环境描写` 是否真正写景，且景境能烘托心境或叙事压力？
- 新增景物或氛围细节是否符合情境，并通过 B 路线风险检查？
- 是否存在抽象审美词直接进入终稿，如"很有电影感""宿命感很强"？
- 是否误写摄影术语、分镜术语或图像提示词？
- `心理反应` 字段是否有对应的外部化锚点？
- 连续转场是否使用了超过 2 次相同的承托方式？
