# aigc 3-明细 / 1-分镜表现 / 分镜密度 / Type Strategies

本文件承载 `aigc 3-明细 / 1-分镜表现 / 分镜密度` 的路由策略、VSM 与局部回退规则。

## VSM

## Preset Anchor Density Contract

若当前组命中 `metadata.source_profile.preset_registry`，`panel_count` 先受以下合同约束：

1. `hard_lock`
   - 默认保持锚点提供的主镜头骨架，不以“更细更丰富”为理由主动加镜。
2. `soft_lock + single_anchor_multi_shot`
   - 允许把一个粗锚点扩成多个细分镜，但这些细分镜必须连续，且仍围绕同一锚点任务。
3. `reference_only`
   - 可按常规密度逻辑裁决，不受锚点骨架约束。

一句话规则：

- `hard_lock` 先保骨架
- `soft_lock` 可细分
- `reference_only` 才自由

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SBD-RHYTHM | 叙事 | 组节奏强度 | `ultra_slow/slow/mid/fast/ultra_fast/unknown` | 动作词密度、句长、冲突节拍 | P0 |
| V-SBD-TYPE | 叙事 | 场景主类型 | `dialogue/action/crowd/inner/emotion/unknown` | 关键词与上下文判定 | P0 |
| V-SBD-DURATION | 结构 | 组时长信息是否可得 | `short/normal/long/unknown` | 上游时长或句段体量估计 | P1 |
| V-SBD-LOAD | 内容 | 信息负载强弱 | `low/mid/high` | 动作节点、人物关系、揭示节拍扫描 | P0 |
| V-SBD-DIRECTOR | 风格 | 导演意图偏置 | `neutral/spectacle_biased/subjective_biased/unknown` | `style_contract.json` 与 `4-导演意图/第N集.json` 证据扫描 | P2 |
| V-SBD-LONGTAKE | 表达 | 长镜头特例证据 | `confirmed/rejected/unknown` | 是否存在“长镜头/留白/冷观察/调度型凝视”文本证据 | P1 |
| V-SBD-COUNT | 输出 | `panel_count` 是否可解释 | `ready/unjustified/overflow` | 区间交集、候选测试与理由检查 | P0 |
| V-SBD-PEAK | 验收 | 审美峰值潜力是否成立 | `ready/flatline` | 候选值是否容纳至少一帧视觉峰值 | P1 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SBD-01 | `V-SBD-RHYTHM=unknown` | 0.9 | 无 | 可并发 C-SBD-02 |
| C-SBD-02 | `V-SBD-TYPE=unknown` | 0.9 | 无 | 可并发 C-SBD-01 |
| C-SBD-03 | `base_range ∩ scene_type_range` 过窄或无交集 | 1.0 | 无 | 可并发 C-SBD-04 |
| C-SBD-04 | `refined_range` 为空 | 1.0 | 无 | 可并发 C-SBD-05 |
| C-SBD-05 | `V-SBD-COUNT=unjustified` | 1.0 | 无 | 可并发 C-SBD-06 |
| C-SBD-06 | `panel_count=1` 且 `V-SBD-LONGTAKE!=confirmed` | 1.0 | 无 | 可并发 C-SBD-05 |
| C-SBD-07 | `V-SBD-COUNT=overflow` | 1.0 | 无 | 无 |
| C-SBD-08 | `V-SBD-PEAK=flatline` | 1.0 | 无 | 无 |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SBD-01 | S-SBD-RHYTHM | 回退为文本节奏判定 | 节奏标签可解释 | S-SBD-PAUSE | 两轮后仍无证据 |
| C-SBD-02 | S-SBD-TYPE | 回退为 `emotion` 并记录未知 | 类型可解释 | S-SBD-RHYTHM | unknown 占比过高 |
| C-SBD-03 | S-SBD-RHYTHM-PRIORITY | 保留 `rhythm`，在最接近 `scene_type` 建议区的合法值中收敛 | 回退理由明确 | S-SBD-PAUSE | 连续多组无交集 |
| C-SBD-04 | S-SBD-CONSERVATIVE-FALLBACK | 显式记录“无交集，按节奏优先保守回退” | 不伪装精确命中 | S-SBD-RHYTHM-PRIORITY | 多轮仍为空 |
| C-SBD-05 | S-SBD-REFINE | 重跑三级渐进裁决与候选测试 | `panel_count` 与理由唯一 | S-SBD-PAUSE | 仍无法收敛 |
| C-SBD-06 | S-SBD-SINGLE-PANEL-GATE | 剔除 `1`，回退到 `2` 或更高合法值 | `1帧` 有明确证据才允许 | S-SBD-REFINE | 仍坚持 `1帧` |
| C-SBD-07 | S-SBD-TRIM | 把帧数收回 `1-15` 合法区间 | 落在合法范围 | S-SBD-REFINE | 连续两轮超界 |
| C-SBD-08 | S-SBD-PEAK-UPSHIFT | 优先向上取一帧，直至能容纳至少一帧视觉峰值 | 存在峰值机会 | S-SBD-REFINE | 上调后仍 flatline |

## 三级渐进裁决（Mandatory）

总范围固定为 `1-15`。执行时只能逐层收敛，禁止 `rhythm / scene_type / info_load / template` 等多套规则并列争夺 `panel_count` 的决定权。

### 第一层：节奏主导，给出基础区间 `base_range`

艺术问题：这组戏的呼吸是什么？

| rhythm | base_range |
| --- | --- |
| `ultra_slow` | `1-2` |
| `slow` | `2-4` |
| `mid` | `5-7` |
| `fast` | `8-12` |
| `ultra_fast` | `13-15` |

裁决提示：

- 第一层先判断观众呼吸应当“停留、推进、逼近还是爆发”。
- 凡是会显著改变呼吸感的因素，优先归入本层。
- `1帧` 只是在 `ultra_slow` 中保留合法性，不等于默认落点。

### 第二层：在基础区间内继续收窄，得到 `refined_range`

艺术问题：这组戏必须让观众看到什么、感到什么？

#### `scene_type` 收窄范围

| scene_type | scene_type_range |
| --- | --- |
| `dialogue` | `1-8` |
| `action` | `6-15` |
| `crowd` | `6-15` |
| `inner` | `1-4` |
| `emotion` | `1-6` |

#### `group_duration` 收窄提示

| duration_bucket | 收窄规则 |
| --- | --- |
| `<12秒` | 默认把当前区间上限 `-1` |
| `12-18秒` | 保持不变 |
| `>18秒` | 默认把当前区间上限 `+1`，但不得超过 `15` |

#### `info_load` 落点提示

- `low`：优先取 `refined_range` 下半部。
- `mid`：优先取 `refined_range` 中部。
- `high`：优先取 `refined_range` 上半部。
- `info_load` 只负责决定落点偏下、居中或偏上，不得单独改写区间边界。

#### 细化公式

`refined_range = base_range ∩ scene_type_range ∩ duration_hint_range`

其中 `duration_hint_range` 只允许通过“收上限/保上限/放上限”的方式参与收窄，不得另起一套主区间。

#### `single_panel_long_take` 特例

- 仅当 `scene_type in {dialogue, inner, emotion}`。
- 且 `info_load != high`。
- 且 `4-导演意图/第N集.json` 的当前组构思或文本证据明确指向“长镜头 / 留白 / 冷观察 / 调度型凝视”。
- 命中特例时，必须显式说明“为什么 `1` 次切换都不需要、为什么 `1帧` 比 `2帧` 更有力量”。
- 若未满足以上条件，即使 `refined_range` 含 `1`，也必须回退到 `2`。
- 本特例默认极少触发，禁止用于 `action / crowd / 高信息负载` 组。

#### `director_intent` 偏置提示

- 若 `style_contract.json.content.director_intent.spectacle_bias in {high, aggressive}`，或 `motion_bias / transition_bias` 明显偏高，则默认在 `refined_range` 上半区取值。
- 若 `subjectivity_mode in {subjective, hybrid}` 且 `audience_distance in {immersive, intimate}`，允许增加主观切入、眩晕式断裂和高感知密度帧。
- 该偏置只能影响 `refined_range` 内的默认落点，不能推翻第一层与第二层已经确定的合法区间。

### 第三层：从 `refined_range` 中确定唯一整数 `panel_count`

艺术问题：几次切换最能保住这股力量，且其中至少有一帧让观众不敢眨眼？

执行顺序：

1. 枚举候选整数帧数。
2. 逐个检查是否能容纳当前组的信息负载而不漏拍。
3. 检查对应单帧时长是否仍可拍、可读。
4. 检查是否更容易通过模板门槛与反平庸门禁。
5. 对每个候选值执行 `Aesthetic Pressure Test`。

#### Aesthetic Pressure Test

对每个候选值额外检验，是否至少有机会策划出一帧视觉峰值：

- 反常规视角：极低角 / 鸟瞰 / 主观歪斜。
- 层次穿透帧：前景强压迫 + 中景动作 + 背景信息同帧。
- 焦点爆破帧：拉焦瞬间 / 超浅景深揭示 / 极窄景深对焦道具。

若候选值太低，无法承载任何视觉峰值，应优先向上取一帧。

#### 反平庸裁决偏好（Mandatory）

- 若多个候选值都成立，默认强制取更有冲击力、更具视听势能的较高值。
- 仅当同时满足以下三条时，才允许回退到较小值：
  - 明确属于冷观察或低能留白。
  - 用户显式要求克制。
  - 该组不存在任何情绪转折、权力关系或揭示节拍。
- 以上三条缺一不可；否则必须取较高值。

## 冲突回退（Mandatory）

- 若 `base_range` 与 `scene_type_range` 无交集，优先保留 `rhythm`，再在最接近 `scene_type` 建议区的合法值中取可解释整数。
- 若 `refined_range` 为空，必须显式记录“无交集，按节奏优先保守回退”，不得假装精确命中。

## 职责边界（Mandatory）

- `rhythm / scene_type / group_duration / info_load` 负责决定 `panel_count`。
- `director_intent` 只负责在合法区间内做表达偏置，不得翻案。
- `template`、反平庸门禁、集级序列去重只负责验收，不得在第一轮与前述裁决器并列决定帧数。

## 通过标准（Mandatory）

最终必须同时满足：

- 信息完整
- 站位清晰
- 时间可拍
- 门禁可过
- 表达意图不流失
- 至少一帧具备视觉峰值潜力
