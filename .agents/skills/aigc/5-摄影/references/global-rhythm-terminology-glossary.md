# Global Rhythm Terminology Glossary

本词汇表为 `5-摄影` 的全局节奏术语标准。所有 reference 文件中的节奏相关术语必须与本词汇表保持一致；若本词汇表与引用文件出现不一致，以本词汇表为准，并在更新引用文件后同步更新本词汇表。

---

## 一、术语层级与归属

| 层级 | 归属契约 | 作用域 | 核心术语 |
| --- | --- | --- | --- |
| 段落级密度曲线 | `sequence-density-curve-contract.md` | 连续 3-8 个 `visual_unit` | `density_ramp`、`tempo_beats`、`peak_slots`、`recovery_slots` |
| 单画面节奏画像 | `visual-rhythm-analysis-contract.md` | 单个 `visual_unit` | `rhythm_profile`、`tempo`、`importance_level` |
| 节拍触发与分镜数 | `beat-analysis-contract.md` | 单个 `visual_unit` 内的切换点 | `beat_trigger`、`shot_count_decision`、`BT-01~BT-16` |
| 时值决策 | `shot-duration-decision-contract.md` | 单个分镜 | `shot_duration_decision`、`duration_class` |

---

## 二、段落级密度曲线术语（sequence-density-curve-contract.md 专用）

### 2.1 Density Ramp（密度斜坡）

描述整段内每个 phase 的分镜密度倾向。

| 状态词 | 含义 | 适用场景 |
| --- | --- | --- |
| `conserve` | 收敛：每画面 1 镜，低信息、低运动 | 日常建立、动作承接、读秒停顿、边界交出 |
| `measured` | 标准：每画面 1-2 镜，信息与节奏平衡 | 常规叙事、标准对话、空间交代 |
| `build` | 建构：每画面 2-3 镜，密度渐升 | 威胁逼近、情绪积累、规则显影准备 |
| `burst` | 爆发：每画面 3-4+ 镜，高密度冲击 | 动作高点、惊吓、惩罚、群像恐慌扩散 |
| `hold` | 停顿：峰值后收束，1-2 镜读秒或反应 | 高点后反压、结果钉镜、余波吸收 |
| `release` | 释放：回归收敛，给下游留交出锚点 | 动作收尾、场景交出、情绪释放 |

**使用规则**：
- `conserve` 和 `release` 不得连续出现超过 2 个画面单位，以免节奏断崖
- `burst` 后必须接 `hold` 或 `release`，不得连续两个 `burst`
- `density_budget` 必须有 `conserve`/`measured` 占比证据，不得全场 `burst`

### 2.2 Tempo Beats（速度阶段）

描述整段的速度变化结构，用 4-7 个阶段词串联。

| 常用阶段词 | 含义 | 视觉预期 |
| --- | --- | --- |
| `setup` | 日常建立 | 流动少切，稳定空间 |
| `threat_entry` | 危险入场 | 密度渐升，景别趋紧 |
| `pressure_build` | 压力积累 | 运动加速，焦点收紧 |
| `action_burst` | 动作爆发 | 高密度冲击，景别跳变 |
| `consequence_hold` | 后果停顿 | 高点后读秒，结果钉镜 |
| `recovery_release` | 恢复释放 | 密度下降，余波交出 |
| `boundary_handoff` | 边界交出 | 收束到下游入口 |

**使用规则**：
- `tempo_beats` 不写成文学主题描述，只用行为词（如 `threat_entry`、`action_burst`）
- 每个阶段词必须对应至少 1 个 `visual_unit`；跨度过大的阶段词须拆解

### 2.3 段落级密度槽位（Density Slot）

| 槽位 | 描述 | 可允许的最高分镜数 |
| --- | --- | --- |
| `peak_slots` | 可加密的峰值位置 | 4 镜（关键揭示/动作分相/群像恐慌） |
| `set_piece_chain_slots` | 连续动作/声画打点例外 | 6 镜（连续命中/一声一结果） |
| `recovery_slots` | 爆点后恢复位置 | 2 镜（结果钉镜/普通人反应） |

---

## 三、单画面节奏画像术语（visual-rhythm-analysis-contract.md 专用）

### 3.1 Rhythm Profile（七维画像）

每个 `visual_unit` 在分镜注入前生成内部 `rhythm_profile`，包含以下维度：

| 维度 | 选项 | 说明 |
| --- | --- | --- |
| `importance_level` | low / medium / high / critical | 当前画面的叙事权重 |
| `tempo` | hold / slow_burn / steady / quick / rupture | 镜头运动速度感 |
| `density` | sparse / measured / rich / maximal | 画面信息密度感 |
| `movement_complexity` | static / single_move / combo_move / rupture_move | 运镜复杂度 |
| `description_scope` | one-line concise / standard / expanded / set-piece | 描述广度 |
| `boundary_clarity` | none / local_handoff / scene_boundary / group_boundary_candidate | 边界清晰度 |
| `peak_emphasis` | none / restrained_peak / expanded_peak / rupture_peak | 高点强调策略 |

**重要区分**：
- `rhythm_profile` 的 `tempo`（hold / slow_burn / steady / quick / rupture）与 `sequence_density_curve` 的 `density_ramp`（conserve / measured / build / burst / hold / release）不是同一层级
- 前者描述单画面镜头运动速度，后者描述段落级分镜密度
- `rhythm_profile` 的 `density`（sparse / measured / rich / maximal）描述画面信息量感，与段落级 `density_ramp` 有对应但不等同

### 3.2 Tempo（速度感）对应

| rhythm_profile.tempo | 对应的运镜速度 | 典型时值倾向 |
| --- | --- | --- |
| `hold` | 静止或极慢，停顿感 | standard / held，约1.5-3.5秒；低信息交出可压短 |
| `slow_burn` | 极慢推进/拉，悬疑感 | standard / held，约2-3.5秒 |
| `steady` | 中速稳定，观察感 | short / standard，约1.5-3秒 |
| `quick` | 快速运动，冲击感 | short，1-2 秒 |
| `rupture` | 断裂跳切，急停/光变 | instant，<1 秒 |

### 3.3 Density（信息密度感）对应

| rhythm_profile.density | 描述广度 | 分镜数量倾向 |
| --- | --- | --- |
| `sparse` | 一行完成，单一运动 | 1 镜 |
| `measured` | 标准展开，单一主体 | 1-2 镜 |
| `rich` | 组合运镜，多重信息 | 2-3 镜 |
| `maximal` | 多镜高密度，复杂运动 | 3-4 镜 |

---

## 四、节拍触发术语（beat-analysis-contract.md 专用）

### 4.0 Beat / Trigger（节拍 / 触发点）

`节拍` 在 `5-摄影` 中等价于“有效分镜触发点”。快节奏短视频平台默认采用 `trigger-first` 口径：`BT-01~BT-16` 命中的有效触发点默认 1:1 落为一个 `分镜N（约X秒）:`。只有当多个触发点能在同一镜头内清楚完成，且不损失平台节奏、观看结果、下游 payload、人物动作连续性或 AIGC 执行稳定性时，才合并。

| 术语 | 含义 | 落盘关系 |
| --- | --- | --- |
| `beat_trigger` | 有效触发点，说明哪里需要换观看策略、平台刺激、可读性或执行稳定性 | 默认 1 个触发点 = 1 个 `分镜N` |
| `trigger_merge_exception` | 合并例外，说明多个触发点可在同一镜头内完成 | 只在不损失观看结果时使用 |
| `shot_count_decision` | 对当前 `visual_unit` 最终分镜数的裁决 | 必须说明每个 `分镜N` 对应哪个触发点或合并例外 |

### 4.1 Beat Trigger Matrix（BT-01~BT-16）

| 触发ID | 节拍触发 | 典型镜头响应 |
| --- | --- | --- |
| `BT-01` | 主体切换 | 景别切换、焦点转移、反打、插入特写 |
| `BT-02` | 动作分相 | 连续分镜、跟拍、甩镜、动作落点 |
| `BT-03` | 信息揭示 | 推轨、微距、焦点拉移、显影式特写 |
| `BT-04` | 情绪转折 | 由宽到近、压缩焦段、停顿长镜、反应镜头 |
| `BT-05` | 空间关系 | 建立镜头、俯拍、轴线重置、遮挡构图 |
| `BT-06` | 声画驱动 | 声音先行转场、切反应、空镜承压 |
| `BT-07` | 视觉形态变化 | 形态锚点、光变状态、显影推进 |
| `BT-08` | 权力关系变化 | 高低机位、对称构图破坏、压迫式前景 |
| `BT-09` | 摄影参数变化 | 景别切换、景深变化、固定机位切换手持 |
| `BT-10` | 声音打点切分 | 声画切点、硬切、结果钉镜、反应落点 |
| `BT-11` | 平台钩子/停滑点 | 快速切入、异常细节、反差揭示、危险预告 |
| `BT-12` | 微动作/微表情跳点 | 眼神、呼吸、手指、肩膀、嘴角、喉结等微动态特写 |
| `BT-13` | 文字/屏幕/字幕可读点 | 黑板字、屏幕、规则文字、道具标签读秒 |
| `BT-14` | 物理接触/道具交互点 | 接触点特写、动作落点、结果反应 |
| `BT-15` | 构图/画幅刺激点 | 视角切换、遮挡揭示、低角度压迫、俯拍重置 |
| `BT-16` | AIGC 执行重置点 | 短镜重置主体、方向、光线、动作相位或空间关系 |

### 4.2 Shot Count Decision（分镜数裁决）

| 条件 | 允许分镜数 | 必须满足 |
| --- | --- | --- |
| 低信息/单一观看 | 1 镜 | 一个镜头完成观看策略，不得硬补 |
| 存在第二个有效触发点 | 2 镜 | 建立后揭示、动作后反应、环境后可读细节、平台钩子后结果等 |
| 关键规则显影/动作分相/群像恐慌/高潮承托/空间重置/平台钩子连续推进/AIGC 执行重置 | 3-4 镜 | 每镜必须有新触发、新主体、新动作相位、新信息、新交接或新执行稳定性价值 |
| 连续动作/声画打点（set-piece-chain 例外） | 5-6 镜 | 每镜独立起点/撞点/结果/声音，删掉任一镜少一节拍 |

---

## 五、时值决策术语（shot-duration-decision-contract.md 专用）

### 5.1 Duration Class（时长等级）

| 等级 | 描述 | 典型范围 |
| --- | --- | --- |
| `instant` | 闪切，<1 秒 | 用于惊吓、断裂、声音打点后硬切 |
| `short` | 短镜，约 1-2 秒 | 用于动作通过、快速切入、hold 节奏 |
| `standard` | 标准镜，约 2-4 秒 | 用于标准叙事、观察、空间交代 |
| `held` | 读秒镜，约 3-6 秒 | 用于关键文字/道具/微表情可读、表演停顿、高点读秒 |
| `long_hold` | 长停顿，>6 秒 | 用于情绪峰值、关系暖点、规则显影、slow_burn |

**短剧·AIGC 压缩规则**：
- 默认优先 `short / standard`，普通氛围镜、过场动作、常规反应不得沿用传统影视宽停顿
- `约3秒` 以上必须有台词、读秒、表演变化、复杂调度、空间重置或高点证据
- AIGC 工具片段时长不得反推拉长单镜叙事时值

### 5.2 Duration Mode（时长模式）

| 模式 | 适用场景 |
| --- | --- |
| `short_drama_aigc` | 短剧·AIGC 项目，默认压缩 |
| `traditional_cinematic` | 长片/传统影视，允许宽松时值 |
| `project_override` | 项目特定覆盖，需显式说明 |

---

## 六、跨层级对应关系

### 6.1 段落级 → 单画面级映射

当 `sequence_density_curve` 已建立时：

| density_ramp（段落级） | rhythm_profile.tempo（单画面） | rhythm_profile.density（单画面） |
| --- | --- | --- |
| `conserve` | `hold` / `slow_burn` | `sparse` / `measured` |
| `measured` | `steady` | `measured` |
| `build` | `steady` / `quick` | `measured` / `rich` |
| `burst` | `quick` / `rupture` | `rich` / `maximal` |
| `hold` | `hold` / `slow_burn` | `sparse` / `measured` |
| `release` | `hold` | `sparse` |

### 6.2 节拍 → 节奏画像映射

| beat_trigger | 典型 rhythm_profile 画像 |
| --- | --- |
| `BT-01` 主体切换 | tempo: steady, density: measured, movement: single_move |
| `BT-02` 动作分相 | tempo: quick, density: rich/maximal, movement: combo_move |
| `BT-03` 信息揭示 | tempo: slow_burn, density: rich, movement: single_move + focus_shift |
| `BT-04` 情绪转折 | tempo: hold/slow_burn, density: measured/rich, movement: static/single_move |
| `BT-05` 空间关系 | tempo: steady, density: measured/rich, movement: single_move |
| `BT-06` 声画驱动 | tempo: rupture/quick, density: measured/rich, movement: rupture_move |
| `BT-07` 视觉形态变化 | tempo: slow_burn/hold, density: measured, movement: static/single_move |
| `BT-08` 权力关系变化 | tempo: steady/quick, density: rich, movement: combo_move |
| `BT-09` 摄影参数变化 | tempo: steady/quick, density: measured/rich, movement: varies |
| `BT-10` 声音打点切分 | tempo: quick/rupture, density: maximal (set-piece), movement: rupture_move |

---

## 七、禁止混用的术语对照

| 错误用法 | 正确用法 | 归属层级 |
| --- | --- | --- |
| 将 `density_ramp` 的 "burst" 用于单画面 `rhythm_profile` | 单画面用 `tempo: quick / rupture` | 单画面节奏画像 |
| 将 `rhythm_profile` 的 "sparse / rich" 用于段落级 `density_ramp` | 段落级用 `conserve / measured / build / burst` | 段落级密度曲线 |
| 将 `tempo_beats` 的阶段词（如 `action_burst`）作为 `rhythm_profile.tempo` 值 | `rhythm_profile.tempo` 只用 hold/slow_burn/steady/quick/rupture | 单画面节奏画像 |
| 用 `peak_emphasis: expanded_peak` 替代段落级 `density_ramp` 的 "burst" | 两者分属不同层级，可同时存在 | 分属段落/单画面 |
| 用 `shot_count_decision: 4` 替代 `rhythm_profile` 的判断 | 先判断 `rhythm_profile`，再输出 `shot_count_decision` | 节拍触发后置 |

---

## 八、引用规范

所有 reference 文件中涉及节奏术语时，必须遵守以下引用格式：

```
段落级密度曲线：
→ 来自 `references/sequence-density-curve-contract.md`
→ 术语：`tempo_beats`、`density_ramp`（conserve/measured/build/burst/hold/release）、`peak_slots`、`recovery_slots`、`set_piece_chain_slots`、`sound_cut_pattern`、`density_budget`

单画面节奏画像：
→ 来自 `references/visual-rhythm-analysis-contract.md`
→ 术语：`rhythm_profile`（七维度）、`importance_level`（low/medium/high/critical）、`tempo`（hold/slow_burn/steady/quick/rupture）、`density`（sparse/measured/rich/maximal）、`movement_complexity`、`description_scope`、`boundary_clarity`、`peak_emphasis`

节拍触发与分镜数：
→ 来自 `references/beat-analysis-contract.md`
→ 术语：`beat_trigger`、`BT-01~BT-16`、`trigger_merge_exception`、`shot_count_decision`

时值决策：
→ 来自 `references/shot-duration-decision-contract.md`
→ 术语：`shot_duration_decision`、`duration_class`（instant/short/standard/held/long_hold）、`duration_mode`
```

---

**关联文件**：
- `references/sequence-density-curve-contract.md`
- `references/visual-rhythm-analysis-contract.md`
- `references/beat-analysis-contract.md`
- `references/shot-duration-decision-contract.md`
- `references/shot-planning-integration-contract.md`（整合层）
- `references/functional-cinematic-projection-contract.md#Gradient-Shot-Detail-Sufficiency`（梯度与维度覆盖）

## Review Gate Mapping

No independent gate: this glossary is the terminology authority for rhythm words, but it does not independently block a deliverable. Any blocking finding must route through the owning rhythm, beat, duration, density or reference-coverage gate below.

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Are `sequence_density_curve`, `rhythm_profile`, `beat_trigger` and `shot_duration_decision` kept in their correct ownership layers? | `GATE-CINE-17A` | `FAIL-CINE-05REF` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N8-REVIEW` | terminology usage notes and reference coverage report entry |
| If paragraph-level density is invoked, does the work use `density_ramp`, `tempo_beats`, `peak_slots`, `recovery_slots`, `set_piece_chain_slots` and `density_budget` through the density-curve owner? | `GATE-CINE-04A2` | `FAIL-CINE-03D` | `references/sequence-density-curve-contract.md` / `steps/cinematography-workflow.md#N3.6-DENSITY-CURVE` | `density_curve_summary`, ramp/stage evidence and all-full/all-empty risk notes |
| If single-visual-unit rhythm is invoked, does it use `rhythm_profile` values rather than paragraph density terms or literary mood labels? | `GATE-CINE-05` | `FAIL-CINE-05D` | `references/visual-rhythm-analysis-contract.md` / `steps/cinematography-workflow.md#N5-RHYTHM` | `rhythm_profile` samples and corrected terminology |
| If beat or shot count is invoked, does `beat_trigger` default to trigger-first shot count while treating merge as an exception with proof? | `GATE-CINE-04` / `GATE-CINE-04E` | `FAIL-CINE-03` / `FAIL-CINE-03F` | `references/beat-analysis-contract.md` / `steps/cinematography-workflow.md#N4-BEAT` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `BT-01~BT-16`, `shot_count_decision` and `trigger_merge_exception` evidence |
| If duration terms are invoked, are `duration_class` and `duration_mode` used through the shot-duration owner and checked against short-drama AIGC compression? | `GATE-CINE-04B` | `FAIL-CINE-03B` / `FAIL-CINE-05L` | `references/shot-duration-decision-contract.md` / `steps/cinematography-workflow.md#N5.2-DURATION` | `shot_duration_decision`, displayed seconds and compression evidence |
| Are forbidden terminology substitutions, such as using `burst` as `rhythm_profile.tempo` or using `shot_count_decision: 4` as rhythm reasoning, caught and routed to the owner layer? | `GATE-CINE-17A` / `GATE-CINE-05` | `FAIL-CINE-05REF` / `FAIL-CINE-05D` | this glossary / owning reference file / `steps/cinematography-workflow.md#N8-REVIEW` | terminology correction list and impacted plan fields |
