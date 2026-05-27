# Peak Shot Language Contract

## Positioning

本文件承接 `aigc/4-表演/references/climax-visual-treatment-contract.md`，用于把上游已经强化出的高潮画面成分，进一步转化为 `5-摄影` 的分镜表现、分镜明细和运镜手法。

`5-摄影` 不重新设计高潮，不新增剧情事实、对白、胜负结果、道具效果或人物动机。它只在上游画面句子已有的高点基础上，提高观看路径的戏剧强度、节拍清晰度、镜头稀缺性和运镜辨识度。

## Peak Shot Definition

高潮画面在摄影阶段表现为 `peak_visual_unit`。识别信号包括：

- 上游 frontmatter 或执行报告包含 `peak_visual_policy`、`peak_visual_pass`、`peak_visual_plan`、`micro_payoff` 或同义说明。
- 画面字段承载行动结果、认知翻转、关系暖点、规则显影、怪异落点、奇观、高超对决、群体恐慌扩散或关键道具显影。
- 同一段内出现强状态差：角色知道/不知道、赢/输、得/失、靠近/疏离、安全/危险、服从/反抗、隐蔽/暴露。
- 该画面如果按普通节奏处理，会导致本集最值得记住的观看瞬间被压平。

没有上述信号时，不得硬造 `peak_visual_unit`；按常规 visual rhythm 处理即可。

## Required Peak Shot Decisions

对每个 `peak_visual_unit`，在常规 `beat_map` 和 `rhythm_profile` 之后，必须内部形成 `peak_shot_profile`：

| slot | requirement |
| --- | --- |
| `source_anchor` | 回指上游画面字段、场景或前置 `peak_visual_pass` 证据 |
| `peak_mode` | `kinetic`、`high-skill_duel`、`potential`、`wave`、`horror_or_rule`、`spectacle` 或 `custom` |
| `emphasis_goal` | 本镜头要让观众得到行动结果、认知震荡、关系推进、情绪修复、规则压迫、奇观冲击中的哪一种主满足 |
| `beat_amplification` | 是否增加分镜、拆出反应镜头、保留读秒、加入急停或保留余波交出点 |
| `camera_motion_strategy` | 静止压迫、极慢逼近、焦点拉移、组合运镜、手持失衡、甩镜急停、环绕压缩、俯拍扫描等 |
| `shot_scale_strategy` | 是否使用大特写、微距、长焦压缩、广角畸变、深焦层次或尺度对比 |
| `pause_or_rupture` | 选择停顿、静止长镜、慢推读秒，还是断裂式切换、急摇、光变、声音先行 |
| `aftershock_handoff` | 高点之后把注意力交给哪个脸、手、道具、规则文字、空间出口或声音来源 |

`peak_shot_profile` 只作为内部判断，不作为输出标题写入成稿。最终仍落入 `分镜明细：分镜N`。

## Mode-Specific Treatment

| peak_mode | storyboard emphasis | camera movement and shot detail |
| --- | --- | --- |
| `kinetic` | 关键动作、阻碍、结果和代价必须拆清；通常 2-4 个分镜 | 跟拍、横移、急停；结果落点用反应镜头或静止镜头钉住 |
| `high-skill_duel` | 先交代胜负条件，再表现反制/识破/破招，不只放大声量 | 视线牵引、焦点拉移、轴线压缩、过肩博弈、棋盘式构图；避免乱切掩盖技术含量 |
| `potential` | 认知翻转、危险确认或艰难判断需要读秒和状态差 | 极慢推轨、焦点从人到字/物/门缝转移、长焦压缩、静止后微动；让观众”看懂一秒” |
| `wave` | 关系暖点、笑点、修复或风景高点要留呼吸，不硬推成危机 | 固定机位、慢速横移、柔和焦点转换、轻声画桥；用距离变化和手部/物件承托状态变化 |
| `horror_or_rule` | 规则显影、怪异落点、集体失控要有压迫入口和反应落点 | 低角度规则压迫、俯拍扫描、光变、声音先行、急停在字/脸/手；保持信息可读 |
| `spectacle` | 先给尺度关系，再给观看者反应和后果落点 | 大远景/远景建立尺度，广角或长焦制造失衡，形态匹配或光变转场；不得只写”大场面” |
| `emotional_slow_burn` | 崩溃/震惊/突然醒悟/强忍情绪场景；此类情绪镜头 `tempo` 标记为 `slow_burn` 或 `hold`，时长由情绪节奏决定，不受 Short Drama AIGC Bias 的 `约3秒` 证据门槛约束 | 正面多角度切换（正面中景→正面近景→正面双眼特写，每个角度 1-2 秒，硬切或焦点跳切串联）或极慢推轨（`约3-5秒`）；不用快速运镜或复杂环绕，以免破坏表演可读性；正面完整捕捉面部肌肉变化；双眼特写拍摄正面眉骨到鼻尖区域，不得只拍单眼侧面 |

### 情绪类高点的特殊处理原则

崩溃/震惊/突然醒悟/强忍类情绪高点的节奏必须放慢：

- **禁止**：快速运镜、复杂环绕、急促切换——会破坏演员需要停住的表演瞬间，让关键情绪一闪而过
- **必须**：正面多角度切换或极慢推轨，让咬肌收紧、眉心竖纹、肩胛内收、瞳孔变化等微动态有足够时间被观众读取
- **时长**：由情绪节奏决定，不受 Short Drama AIGC Bias 的 `约3秒` 证据门槛约束；若写 `约3秒` 以上，正文必须通过对白承托、读秒、静止、极慢运动或框内变化证明它在短剧·AIGC 节奏里成立
- **景别**：从正面中景逐步收紧到正面近景，再到正面双眼特写（眉骨到鼻尖），逐层放大情绪可读性
- **节奏标签**：`tempo = slow_burn` 或 `hold`，在 `shot_duration_decision` 和 `rhythm_profile` 中显式标记

> **注意**：当上游有 `peak_visual_pass` 且类型为情绪类高点（崩溃/震惊/醒悟/强忍），必须使用 `emotional_slow_burn` 模式，不得按普通高点加速处理。

## Shot Density Rules

- 普通高点可比同类画面多 1 个分镜，但必须有新注意力或新戏剧信息。
- 阶段性大高点可使用 3-4 个分镜，但必须包含 `建立 -> 释放/显影 -> 反应/结果 -> 余波交接`。
- 高潮不是一律更快。`potential` 和 `wave` 类高点常常需要更慢、更静、更可读。
- 高潮也不是一律更多。一个极稳定的静止长镜，如果能压住角色、信息和声音，也可以是最强处理。
- 连续多个高点时，必须用不同节奏形态区分：一个用停顿，一个用急停，一个用焦点拉移，一个用反应切，不要都写成慢推特写。

## Forbidden Patterns

- 为了“高潮感”给上游没有的爆炸、死亡、哭喊、拥抱、胜负结果或道具变化。
- 每个高点都写成大特写 + 慢推 + 急停，导致分镜明细同质化。
- 用复杂运镜覆盖演员需要停住的表演瞬间。
- 动作高点只写运动，没有结果落点或代价。
- 认知高点只写脸部震惊，没有信息显影或状态差。
- 关系高点突然套恐怖/动作节奏，破坏上游情绪承诺。
- 奇观高点只有尺度，没有观看者、环境变化或后果承接。

## Review Expectations

交付前检查：

- 上游已有 `peak_visual_pass` 或明显高点时，摄影稿没有按普通画面压平。
- 高点分镜的密度、景别、运镜、转场和停顿都能回指当前画面句子的戏剧任务。
- `peak_shot_profile` 的结果体现在 `分镜N` 中，但没有外露为冗余标签。
- 高潮强化没有改写上游编导文字、事实、对白或场景顺序。
- 同集多个高点之间在运镜速度、景别尺度、转场形态、反应落点或光色策略上有差异。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否只在上游存在 `peak_visual_pass`、明显高点或强状态差时建立 `peak_visual_unit`，没有硬造高潮？ | `GATE-CINE-14` | `FAIL-CINE-05E` | `N5.5-PEAK-SHOT` | 高点证据、`source_anchor`、未命中高点时按常规节奏处理的说明 |
| 每个高点是否形成内部 `peak_shot_profile`，并把 `peak_mode / emphasis_goal / beat_amplification / aftershock_handoff` 投影到 `分镜N`？ | `GATE-CINE-14` | `FAIL-CINE-05E` | `N5.5-PEAK-SHOT` + `N6.5-SHOT-PLAN` | 峰值镜头策略、余波交出、被压平高点的修复记录 |
| 高点密度是否来自新注意力、新戏剧信息、反应/结果或余波，而不是一律增加分镜？ | `GATE-CINE-04A` | `FAIL-CINE-03A` | `N4-BEAT` + `N5-RHYTHM` + `N5.5-PEAK-SHOT` | 分镜数量分布与高点抽样复核、删并或加密依据 |
| `emotional_slow_burn` 是否用于崩溃、震惊、醒悟、强忍等情绪高点，并以正面缓变、停顿、多角度正面切换或正面双眼特写承托？ | `GATE-CINE-04B` | `FAIL-CINE-19D` | `N5.2-DURATION` + `N5.5-PEAK-SHOT` + `N6.5-SHOT-PLAN` | 情绪类慢节奏承托、`tempo=slow_burn/hold` 标记、心理变化慢节奏修复记录 |
| 情绪类眼部特写是否限定正面双眼或正面上半脸，没有写成单眼侧面？ | `GATE-CINE-15A` | `FAIL-CINE-19B` | `N6.4-FUNCTIONAL-PROJECTION` + `N7-INJECT` | AI 视频执行稳定性检查中的眼部特写抽样、单眼侧面修复字段 |
| 高潮强化是否不新增剧情事实、对白、胜负结果、道具效果或人物动机？ | `GATE-CINE-13` | `FAIL-CINE-06` | `N5.5-PEAK-SHOT` + `N7-INJECT` | 原文保真 diff、高点强化未改写上游事实的说明 |
| 同集多个高点是否在运镜速度、景别尺度、转场形态、反应落点或光色策略上有差异，而非统一套用大特写慢推？ | `GATE-CINE-16` | `FAIL-CINE-05I` | `N6.2-CAMERA-GRAMMAR` + `N5.5-PEAK-SHOT` | 摄影语法变化检查结果、高点差异化抽样 |
