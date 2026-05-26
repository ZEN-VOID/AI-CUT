# Emotional Rhythm Map Contract

## Purpose

定义整集情绪节奏曲线：从 3-导演 产出，被 4-表演 和 5-摄影 消费，确保全链路的情绪节奏是一致的——导演设计的"安静承压"不会被摄影变成"密集特写运动"，表演也不会把每个场景都演到满。

## Ownership

- **产出者**：3-导演 在 N7-DIR-AESTHETIC 节点形成 `emotional_rhythm_map`
- **消费者**：
  - 4-表演 在 N2-PERF-TYPE 消费 `scene_emotional_register` 决定表演强度层级
  - 5-摄影 在 N3.6-DENSITY-CURVE 消费 `peak_valley_sequence` 决定镜头密度与节奏
- 本合同不定义"什么是好节奏"，只定义"节奏必须是被设计的"。

---

## Emotional Rhythm Map Structure

### episode_emotional_arc — 整集情绪弧线

```
开场基调 -> 渐变路径 -> 峰值时刻 -> 谷值时刻 -> 终场落点
```

| field | description | 示例 |
| --- | --- | --- |
| opening_register | 开场情绪基调 | 冷寂 / 日常 / 紧张余波 / 不安 |
| gradient_path | 从开场到高潮的情绪渐变路径 | 冷寂→隐压→试探→爆发→冷却 |
| peak_moment | 全集情绪最高点 | 第X场景的揭示/对决/突破 |
| valley_moment | 全集情绪最低点 | 第Y场景的失败/分离/沉默 |
| closing_register | 终场情绪落点 | 余震 / 空洞 / 不安 / 温暖 |

### scene_emotional_register — 每场景情绪音域

每场景标注其情绪音域等级（从该场景选择 1-2 个标签）：

| register | 描述 | 表演强度参考 | 摄影密度参考 |
| --- | --- | --- | --- |
| `suppressed` | 压抑、冻结、表面平静 | 低外显、高内心 | 长镜头、少切、静止 |
| `tense` | 紧张、蓄压、悬而未决 | 中外显、高微表情 | 慢推、手持微晃、焦点追 |
| `warm` | 温暖、亲近、安全感 | 自然外显 | 稳定、中景、自然光 |
| `released` | 释放、爆发、畅快 | 高外显 | 快切、运动、多角度 |
| `cold` | 冷寂、疏离、空旷 | 极低外显 | 远景、固定、冷调 |
| `violent` | 暴烈、冲击、破坏 | 瞬间爆发 | 闪切、手持剧烈、运动 |
| `eerie` | 怪异、不安、违和 | 克制外显+异常细节 | 慢推、异常构图、低角度 |
| `melancholic` | 忧郁、怀念、失落 | 低外显+微颤 | 柔焦、慢运动、留白 |

### peak_valley_sequence — 情绪峰谷序列

全集的情绪起伏序列，标注每个场景的情绪高度和过渡方式：

```
[
  {scene: 1, register: "suppressed", height: 3, transition: "cold_open"},
  {scene: 2, register: "tense", height: 5, transition: "sound_bridge"},
  {scene: 3, register: "warm", height: 4, transition: "contrast_relief"},
  {scene: 4, register: "violent", height: 9, transition: "rupture"},
  {scene: 5, register: "melancholic", height: 2, transition: "decay"},
  ...
]
```

- `height` 范围 1-10，1=最低谷，10=最高峰
- `transition` 标注从前一场景到本场景的过渡方式

### tension_release_budget — 紧张-释放预算

| field | description |
| --- | --- |
| total_tension_budget | 全集紧张总配额（高/中/低） |
| total_release_budget | 全集释放总配额（高/中/低） |
| tension_distribution | 紧张如何分布在场景中（前重后重/均匀/波浪） |
| release_spots | 释放点在哪些场景（不应在高潮前释放） |
| climax_tension_reserve | 为高潮保留的紧张额度 |

### anti_climax_strategy — 反高潮策略

| field | description |
| --- | --- |
| use_anticlimax | 是否在本集使用反高潮（true/false） |
| anticlimax_location | 在哪个场景使用 |
| anticlimax_type | deliberate_anticlimax / delayed_gratification / pyrrhic_payoff / false_payoff / interrupted_payoff / reversed_payoff |
| payoff_delay_to | 延迟到哪一集兑现（如果是延迟满足） |

### genre_emotional_coloring — 类型情绪着色

类型持续影响各场景情绪底色的规则：

| genre | emotional_bias | scene_impact |
| --- | --- | --- |
| 校园规则怪谈 | `eerie` 底色 + `tense` 持续 | 即使温暖场景也有不安底色 |
| 悬疑推理 | `tense` 底色 + 信息蓄压 | 每个场景都有一层"不对劲" |
| 爱情 | `warm` 底色 + `melancholic` 波动 | 对手戏偏暖，独处戏偏冷 |
| 动作战斗 | `tense` 蓄压 + `violent` 爆发 | 文戏节奏也偏快 |
| 喜剧 | `warm` 底色 + 节奏偏快 | 沉默场景极少 |

---

## Per-Stage Consumption Contract

### 3-导演 产出规则

- 在 N7-DIR-AESTHETIC 节点必须形成 `emotional_rhythm_map`
- 整集弧线必须有明确的 peak 和 valley（不能全是中段）
- 峰谷序列中相邻场景不应连续两个都是相同 height（避免节奏平坦）

### 4-表演 消费规则

- 在 N2-PERF-TYPE 节点消费 `scene_emotional_register`
- 根据 register 决定表演强度层级：`suppressed` 场景不演满、`violent` 场景留爆发空间
- 不是每个场景都需要五层表演控制的全部层级——`cold` 场景可能只需要姿态和微表情

### 5-摄影 消费规则

- 在 N3.6-DENSITY-CURVE 节点消费 `peak_valley_sequence`
- 根据 height 决定镜头密度：高点场景多分镜、低谷场景少分镜或长镜头
- 根据 transition 决定场景间过渡方式：`rupture` 用硬切、`decay` 用慢推、`sound_bridge` 用声音先行

---

## Failure Modes

| symptom | root_cause | fix |
| --- | --- | --- |
| 全集节奏平淡无起伏 | peak_valley_sequence 的 height 差异不足 | 拉高峰值或降低谷值，制造更大落差 |
| 表演每场都演到满 | scene_emotional_register 没有被消费 | N2-PERF-TYPE 必须读取 register 并分配强度 |
| 摄影每场都同等精致 | peak_valley_sequence 没有被消费 | N3.6-DENSITY-CURVE 必须读取 height 并分配密度 |
| 高潮后没有冷却 | 缺少 closing_register 设计 | 补充终场落点和 valley_moment |
| 类型底色消失 | genre_emotional_coloring 没有持续影响 | 每场景的 register 必须叠加类型偏置 |

---

## Reusable Heuristics

- 节奏不是"快就好"或"慢就好"，而是有设计的起伏。好的节奏让观众在高潮时刻到达情绪峰值，在谷值时刻获得呼吸空间。
- 紧张是有限资源。在低信息场景消耗紧张额度，高潮场景就没有余量了。
- 反高潮不是失败，是最高级的导演策略之一。《绝命毒师》用延迟满足创造了电视史上最令人窒息的高点。
- 表演和摄影必须服从情绪节奏设计。如果导演设计了"安静承压"场景，表演和摄影不应该自作主张把它变成"紧张爆发"。
- 类型不是路由变量，而是持续的情绪底色。校园怪谈类型的"温暖"场景和爱情类型的"温暖"场景，温度完全不同。
