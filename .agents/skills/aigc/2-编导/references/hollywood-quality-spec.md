# Hollywood Quality Specification

## Purpose

本规格包为 `2-编导` director layer 提供"高质量但不越过保真"的质量标准参照。它定义了什么样的导演创作可以被视为好莱坞级质量，同时明确了哪些越权行为是禁止的。

**定位澄清**：本文件是顶层质量宪章，不是快速参考卡片；它为 `N3-DIR-SUBSTANCE`、`N4-DIR-PEAK`、`N7-DIR-AESTHETIC` 提供必须满足的质量基线，为 `N10-DIR-REVIEW` 提供可执行的检查规格。

本文件不授权新增剧情事实、对白、事件、规则、线索、因果、摄影方案或分镜编号。

## Ownership

- 本文件拥有好莱坞级质量的定义、允许/禁止边界、证据结构和失败模式。
- `directorial-authorship-contract.md` 负责导演创作内核的具体规划证据；本文件负责质量标准的顶层判断。
- `climax-visual-treatment-contract.md` 负责高潮画面的兑现模式；本文件负责判断强化是否越权。
- `visual-aesthetic-contract.md` 负责单场画面美学；本文件负责判断"画面密度"和"节奏控制"是否达标。
- `atmosphere-and-mood-contract.md` 负责五感氛围和意境技法；本文件负责判断意境是否可拍可感而非抽象。

## Dependency Graph

```
hollywood-quality-spec.md (顶层质量宪章)
├── consumed_by: N3-DIR-SUBSTANCE (编导创作内核)
├── consumed_by: N4-DIR-PEAK (高潮画面强化)
├── consumed_by: N7-DIR-AESTHETIC (画面美学)
├── consumed_by: N9-DIR-DRAFT (内嵌正文)
├── consumed_by: N10-DIR-REVIEW (验证 hollywood_quality_notes)
└── reference_to:
    ├── directorial-authorship-contract.md
    ├── climax-visual-treatment-contract.md
    ├── visual-aesthetic-contract.md
    └── atmosphere-and-mood-contract.md
```

## Quality Dimensions

以下 5 个质量维度是 `2-编导` director layer 必须同时满足的好莱坞级质量基线。

### 1. 戏剧实质深度 (Dramatic Substance Depth)

**达标标准**：人物压力、选择和隐藏恐惧必须外部化为可拍/可演/可听的具体行为，不得写成内心描述。

**强证据**：
- 角色不是"害怕"，而是"手指压住纸角、呼吸变浅、避开视线"。
- 角色不是"愤怒"，而是"咬肌绷紧、声音变硬、手背青筋凸起"。
- 压力必须有来源、阻碍和选择窗口，不是泛泛"紧张"。

**弱证据（不可接受）**：
- "角色内心很害怕。"
- "气氛很紧张。"
- "面临艰难选择。"

**evidence_field**: `director_substance_plan.character_pressure` 和对应 `角色动作` / `对白画面` 字段

### 2. 画面密度 (Visual Density)

**达标标准**：画面必须包含可感知变量（道具、空间、光、声音、材质、质感）承托情绪，而不是堆砌形容词。

**强证据**：
- "沉默不是空白，而是'灯管嗡鸣消失、笔尖悬停、群像迟半拍'。"
- "离别不是悲伤，而是'门外的廊灯把她的影子拉进屋内，影子的边缘被门槛切成两截'。"
- 环境有层次、光线有质感、声音有层次、道具痕迹可见。

**弱证据（不可接受）**：
- "夜色压抑，气氛紧张。"
- "灯光很柔和。"
- "场面很戏剧化。"

**evidence_field**: `环境描写`、`音效画面`、`道具特写` 和 `visual_aesthetic_pass` 证据

### 3. 节奏控制 (Pacing Control)

**达标标准**：画面节奏从密到疏、从压迫到释放、从静到动必须有可感知的节律设计，关键节点有延时承托或骤然加速。

**强证据**：
- 高潮前有等待，高潮后有余波。
- 紧张场有声音消失或声音替代，而不是全程高强度。
- 尾场有留白或静物状态，而不是每个场景都同等用力。

**弱证据（不可接受）**：
- "节奏明快，戏剧张力强。"（无具体节律描述）
- "每一场都很紧凑。"（无节律变化说明）
- "结尾留下悬念。"（无画面/声音/表演落点）

**evidence_field**: `visual_aesthetic_pass.visual_rhythm_notes` 和 `atmosphere_mood_evidence`

### 4. 表演承托 (Performance Support)

**达标标准**：演员必须有可执行的微表情、身体联动和道具动作，而不是表演说明或内心描述。

**强证据**：
- 不只写"愤怒"，而写"咬肌绷紧、声音变硬、手背青筋凸起"。
- 不只写"震惊"，而写"瞳孔收缩、后退半步、视线在半空中停住"。
- 潜台词通过视线、手部、空间距离和停顿承托，不通过内心独白。

**弱证据（不可接受）**：
- "演员要有内心戏。"
- "表现出复杂的情感。"
- "角色内心很矛盾。"（无外部行为支撑）

**evidence_field**: `对白画面`、`角色动作`、`表情特写` 和 `director_substance_plan.performance_engine`

### 5. 视觉主轴 (Visual Spine)

**达标标准**：整集必须有可记忆的母题链和材质/色彩弧，核心物件在不同场景承担不同压力。

**强证据**：
- "纸面→火光→殷红→海雾压低"作为材质/色彩弧。
- 同一扇门在不同场景从"出口"变成"封锁"，承担不同压力。
- 视觉母题有变化，不机械重复。

**弱证据（不可接受）**：
- "整集有统一风格。"（无具体母题链）
- "画面很有电影感。"（无材质/色彩变化说明）
- "每场都很好看。"（无主轴记忆点）

**evidence_field**: `episode_visual_spine` 和 `visual_aesthetic_pass.image_motif_map`

## Forbidden Overreach

以下 8 类越权行为是 `2-编导` director layer 的绝对禁止项，任何一个发生即为 quality failure。

| forbidden action | reason | detection method | example |
| --- | --- | --- | --- |
| **新增剧情事实** | 破坏上游保真 | 逐项对比上游，若输出中存在上游原文没有的"发生了 X"即为越权 | "新增角色背景故事" |
| **未锚定新增对白** | 改写上游正文或脱离叙事锚点自由加话 | 检查引号内内容；若既不是上游已有对白，也没有通过 `narration-to-voice-adaptation-contract.md` 留证，即为新增 | "为角色添加没有原文锚点的内心独白对白" |
| **新增因果** | 改变事件逻辑 | 若角色行为原因在上游无锚点即为新增因果 | "让角色因为新原因做出选择" |
| **新增桥段** | 增加上游没有的事件 | 若场景中出现上游无描述的动作序列即为新增桥段 | "新增追逐戏" |
| **摄影越权** | 越界到下游 4-摄影 | 检查是否出现机位、景别、镜头运动、分镜编号或图像提示词 | "写分镜编号、机位、景别、镜头运动" |
| **改写对白** | 改变角色语言 | 若角色语言在上游对白中找不到对应表述即为改写 | "让角色说更高级的话" |
| **改写场景顺序** | 改变叙事结构 | 若事件发生的先后顺序与上游不一致即为改写 | "调整事件发生的先后" |
| **改写场景标题** | 改变场景功能 | 若场景功能（压迫/转折/释放）与上游设定不符即为改写 | "把场景改得更戏剧化" |

## Hollywood Quality Notes

当 `hollywood_quality_notes` 被产出时，必须包含以下完整证据结构：

```yaml
hollywood_quality_notes:
  dimensions:
    dramatic_substance_depth:
      satisfied: true/false
      evidence_field: ""  # 来自 director_substance_plan 或具体剧本字段
      upstream_anchor: ""   # 回指上游原文锚点
      what_improved: ""    # 具体提升了什么
    visual_density:
      satisfied: true/false
      evidence_field: ""
      upstream_anchor: ""
      what_improved: ""
    pacing_control:
      satisfied: true/false
      evidence_field: ""
      upstream_anchor: ""
      what_improved: ""
    performance_support:
      satisfied: true/false
      evidence_field: ""
      upstream_anchor: ""
      what_improved: ""
    visual_spine:
      satisfied: true/false
      evidence_field: ""
      upstream_anchor: ""
      what_improved: ""
  fidelity_verified:
    no_new_fact: true
    no_unlicensed_dialogue: true
    narration_to_voice_adaptation_source_grounded: true
    no_new_causality: true
    no_new_episode: true
    no_photography_overreach: true
    no_diatribe_reorder: true
    no_scene_title_change: true
  risk_check:
    field_drift_to_abstract: false  # 是否有从具体描述漂移到抽象评价
    over_reliance_on_adjectives: false  # 是否堆砌形容词而非可拍细节
    missing_upstream_anchor: false  # 是否有提升内容无法回指上游
  review_gate:
    passed: true/false
    blocking_issues: []  # 若有阻断项，列出具体问题
```

## Weak-to-Strong Examples

### 戏剧实质

弱：`角色内心很恐惧。`

强：`角色把签字的笔尖压住纸面，指节发白，视线落在纸角已经洇开的那滴墨渍上，迟迟没有移开。`

### 画面密度

弱：`环境描写：夜色压抑，气氛紧张。`

强：`环境描写：廊下的灯火被风压得忽明忽暗，门槛外一线雨水沿石缝往里渗，墙面旧灰浮起潮痕；灯管的嗡鸣在第三次闪烁后停了，空气像被按了暂停。`

### 表演承托

弱：`表情特写：演员要表现出震惊。`

强：`表情特写：他的瞳孔在半空中停了一拍，下颌微微往后收，手指还停在刚才握笔的位置，像是忘了下一步该做什么。`

### 视觉主轴

弱：`视觉母题：每场都有好看的画面。`

强：`视觉母题：纸面从第1场的空白密报，变成第3场的殷红残页，再到第7场的油绢入袖，材质从木案暗色过渡到火光和殷红，最后被海雾和残金日光压低——同一载体在不同场景承担了不同压力。`

## Failure Cases

### Failure 1: Abstract Quality Claims Without Concrete Evidence

**症状**：输出包含"很有电影感""高级感很强""很有戏剧张力"等抽象评价，但没有对应的画面/声音/表演证据。

**诊断**：N7-DIR-AESTHETIC 或 N9-DIR-DRAFT 跳过了 `visual_aesthetic_pass` 的具体轴，只输出了审美判断而非可拍描述。

**修复**：回到 `visual_aesthetic_pass`，为每个声称"有质感"的场景补 `visual_core`、`image_hierarchy` 和 `contrast_axis_map`，让证据字段能回答"什么画面、什么质感、什么对比"。

**验证**：执行报告中 `hollywood_quality_notes` 的每个维度必须有 `upstream_anchor` 和 `evidence_field`，不是只有 `satisfied: true`。

### Failure 2: Performance Notes Stay Internal

**症状**：`director_substance_plan.performance_engine` 写了"停顿""视线压力""身体距离"等方向，但没有投影到 `对白画面` 或 `角色动作` 字段。

**诊断**：N9-DIR-DRAFT 把 `director_substance_plan` 作为规划段落而非分配指令，表演指导没有内嵌进正文。

**修复**：回到 N9-DIR-DRAFT，把 `performance_engine` 的每条指令对应到最近的 `对白画面` 或 `角色动作` 字段，用具体视线、手部、距离和停顿替换规划段落的通用描述。

**验证**：终稿正文中每个高情绪场至少有 1 个可演的视线/手部/距离/停顿细节，不是只有内心描述或表演说明。

### Failure 3: Visual Spine Decays to Decorations

**症状**：`episode_visual_spine` 写了母题链，但每个场景的 `visual_aesthetic_pass` 没有呼应、变奏或克制母题链，整集视觉记忆散乱。

**诊断**：N7-DIR-AESTHETIC 只做了单场美学 pass，没有读取 `episode_visual_spine` 并为每个关键场景分配呼应/变奏/克制策略。

**修复**：回到 N7-DIR-AESTHETIC，检查每个关键场景的 `visual_aesthetic_pass`，确认 `motif_and_variation` 轴有具体的呼应/变奏/克制说明；若有场景遗漏，补全 `callback_targets`。

**验证**：`episode_visual_spine.callback_targets` 中的每个呼应目标在终稿中至少出现 1 次变奏，不是机械重复。

### Failure 4: Peak Visual Pass Overreaches

**症状**：`peak_visual_pass` 新增了上游没有的"胜负已定""对手退让""规则改写"等结果，或改变了兑现方式。

**诊断**：N4-DIR-PEAK 为了让高潮"更炸"，在强化过程中不知不觉改变了上游已有的事件结果。

**修复**：回到 `peak_visual_pass`，逐项检查 `delivery_action` 是否与上游原文一致；若不一致，删除不一致项，只保留画面/声音/表演/余波的承托增强。

**验证**：执行报告 `peak_visual_plan.delivery_action` 能回指上游原文，没有新增上游没有的胜负、表白、死亡或反转。

## Integration

- 由 `N3-DIR-SUBSTANCE` 消费，用于判断编导创作内核是否符合好莱坞质量标准。
- 由 `N4-DIR-PEAK` 消费，用于判断高潮画面强化是否越权。
- 由 `N7-DIR-AESTHETIC` 消费，用于判断画面美学是否有具体证据而非抽象评价。
- 由 `N9-DIR-DRAFT` 嵌入正文，不得以注释形式泄露。
- 由 `N10-DIR-REVIEW` 验证 `hollywood_quality_notes` 是否有回指上游锚点、维度覆盖完整和风险检查。

## Review Checklist

- `hollywood_quality_notes` 的 5 个维度是否全部覆盖，且每个都有 `upstream_anchor` 和 `evidence_field`？
- 是否有越权行为（新增事实/对白/因果/桥段/摄影方案）？
- 提升的内容是否只改变表现层，不改变剧情层？
- 是否有抽象审美词（"电影感""宿命感""高级感"）直接进入正文？
- 证据是否包含完整的 fidelity_verified 和 risk_check 块？
- 若有 failure case 中的症状，是否已回到对应节点修复？

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `hollywood_quality_notes` 是否覆盖戏剧实质、画面密度、节奏控制、表演承托和视觉主轴 5 个维度，且每项有上游锚点和证据字段？ | `GATE-DIR-06` | `FAIL-CREATIVE-EVIDENCE` | `N3-DIR-SUBSTANCE` / `N7-DIR-AESTHETIC` / `N11-DIR-WRITEBACK` | `hollywood_quality_notes.dimensions.*.upstream_anchor`、`evidence_field` |
| 质量提升是否只改变表现层，未新增事实、对白、因果、桥段、场景顺序、场景标题或摄影方案？ | `GATE-DIR-06` | `FAIL-CREATIVE-EVIDENCE` | `N9-DIR-DRAFT` / `N10R-DIR-REPAIR` | `hollywood_quality_notes.fidelity_verified`、终稿与上游对比 |
| 抽象质量词是否已替换为可拍/可听/可演证据，没有直接进入正文？ | `GATE-DIR-05` | `FAIL-VISUAL-AESTHETIC` | `N7-DIR-AESTHETIC` / `N9-DIR-DRAFT` | `risk_check.field_drift_to_abstract: false`、`visual_aesthetic_evidence` |
| 表演承托是否投影到 `对白画面` / `角色动作` / `表情特写`，没有停留在内部规划？ | `GATE-DIR-15` | `FAIL-PERFORMANCE-STYLE` | `N3-DIR-SUBSTANCE` / `N9-DIR-DRAFT` | `director_substance_plan.performance_engine`、终稿对应字段 |
| 视觉主轴是否在关键场景中有呼应/变奏/克制落点，而非只写“统一风格”？ | `GATE-DIR-05` | `FAIL-VISUAL-AESTHETIC` | `N7-DIR-AESTHETIC` | `episode_visual_spine`、`scene_items.motif_and_variation` |
| 高潮强化是否通过好莱坞质量检查而未越过上游 `delivery_action` 和 `satisfaction_delta`？ | `GATE-DIR-01` | `FAIL-PEAK-VISUAL` | `N4-DIR-PEAK` | `peak_visual_plan.delivery_action`、`satisfaction_delta`、`hollywood_quality_notes.blocking_issues` |
