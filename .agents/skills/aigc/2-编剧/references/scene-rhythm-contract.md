# Scene Rhythm Contract

## Purpose

定义场景级节奏控制：场景不是等长等密度的信息容器，而是有呼吸、有压缩、有释放的叙事单元。本合同让编剧阶段就能主动设计"哪场戏长、哪场戏短、哪场戏密、哪场戏疏"。

## Ownership

- 2-编剧 在 N3-SCENE 阶段为每个场景建立 `scene_rhythm_profile`。
- `scene_rhythm_profile` 被 N5-SCRIPT-DRAFT 消费，影响字段密度和留白取舍。
- 3-导演 在 N7-DIR-AESTHETIC 阶段进一步消费节奏判断做视觉节奏设计。

---

## Scene Rhythm Profile

每个场景标注以下字段：

| field | 选项 | 创作含义 |
| --- | --- | --- |
| `scene_duration_feel` | 长场 / 标准场 / 短场 / 闪回 | 观众感受到的场景长度预期 |
| `information_density` | 高密度 / 标准 / 低密度（留白场） | 信息释放的速度和数量 |
| `rhythm_type` | 紧凑推进 / 缓慢蓄压 / 松弛过渡 / 爆发冲击 / 静默留白 | 本场景的节奏情绪 |
| `beat_count` | 数字 | 该场景包含多少个叙事节拍（动作/对白/信息/情绪转折） |
| `transition_out_method` | 对白收尾 / 动作收尾 / 画面留白 / 声音余韵 / 硬切 | 场景结束方式 |

### rhythm_type 详解

| rhythm_type | 节奏感受 | 字段密度 | 常见场景类型 |
| --- | --- | --- | --- |
| `compact_push` | 紧凑推进：信息密集、beat衔接紧密 | 高密度、少留白 | 对峙、追逐、谈判、谈判、任务执行 |
| `slow_pressure` | 缓慢蓄压：表面平静但压力持续上升 | 中密度、大量微表情和沉默 | 日常中的异常、等待、监视 |
| `relaxed_transition` | 松弛过渡：放松、呼吸、信息整理 | 低密度、多环境和日常 | 战斗间歇、角色独处、旅途 |
| `explosive_burst` | 爆发冲击：突然的高能 | 瞬间高密度 | 揭示、反杀、逃亡、告白 |
| `silent_stillness` | 静默留白：沉默、凝视、空间 | 极低密度、大量环境和呼吸 | 丧亲后、重大失败后、终场余韵 |

---

## Scene Duration & Rhythm Relationship

| scene_duration_feel | 典型 beat_count | 适合的 rhythm_type | 字段写法指导 |
| --- | --- | --- | --- |
| 短场（3-8 beat） | 3-8 | explosive_burst / compact_push | 每个 beat 都是关键信息或动作，无冗余 |
| 标准场（10-20 beat） | 10-20 | compact_push / slow_pressure | 有建立-发展-转折的完整结构 |
| 长场（20+ beat） | 20+ | slow_pressure / relaxed_transition | 需要有内部小高潮维持注意力 |
| 闪回（5-10 beat） | 5-10 | varies | 简化字段、突出核心记忆点 |

---

## Transition Out Methods

| method | 视听效果 | 适合场景 | 创作技巧 |
| --- | --- | --- | --- |
| `dialogue_close` | 对白自然收尾 | 对话场景 | 最后一句对白留有余味或暗示 |
| `action_close` | 动作完成收尾 | 动作场景 | 最后一个动作指向下一场景 |
| `image_linger` | 画面留白 | 情绪场景 | 画面停留在角色/物件/空间上 |
| `sound_bridge` | 声音余韵 | 转场场景 | 本场景的声音延续到下一场景画面 |
| `hard_cut` | 硬切 | 节奏突变 | 上一 beat 突然结束，下一场景直接进入 |

---

## Genre Rhythm Baselines

| 类型 | 默认 rhythm_type 偏向 | 节奏特征 | 禁忌 |
| --- | --- | --- | --- |
| 校园规则怪谈 | slow_pressure + explosive_burst | 80%蓄压 + 20%爆发 | 不能全场景紧凑（蓄压需要时间） |
| 战斗动作 | compact_push + explosive_burst | 短促有力、即时反应 | 不能有太多松弛过渡（会失去动能） |
| 悬疑推理 | slow_pressure + compact_push | 信息控制、停顿制造张力 | 不能过早爆发（真相要最后才揭示） |
| 爱情 | relaxed_transition + slow_pressure | 日常积累、情感升温 | 不能每场都是爆发（需要日常建立亲密感） |
| 喜剧 | compact_push + relaxed_transition | 快节奏、多beat、场景短 | 不能有太多静默留白（喜剧不沉默） |

---

## Consumption

| stage | node | action |
| --- | --- | --- |
| 2-编剧 | N3-SCENE | 为每个场景建立 `scene_rhythm_profile` |
| 2-编剧 | N5-SCRIPT-DRAFT | 根据 rhythm_type 决定字段密度：compact_push 少留白、silent_stillness 多环境 |
| 2-编剧 | N6-SCRIPT-REVIEW | 检查：场景节奏是否有变化（不能全部场景同一节奏类型） |
| 3-导演 | N7-DIR-AESTHETIC | 消费 scene_rhythm_profile 做视觉节奏设计 |

---

## Failure Modes

| symptom | root_cause | fix |
| --- | --- | --- |
| 全集节奏平淡 | 所有场景的 rhythm_type 相同 | 拉开差异：至少有 2 种不同的 rhythm_type |
| 场景间的过渡生硬 | transition_out_method 全部是 hard_cut | 增加声音余韵、画面留白等过渡方式 |
| 留白场信息密度过高 | silent_stillness 场景被塞了太多 beat | 削减 beat_count，让沉默真正沉默 |
| 蓄压场缺少内部起伏 | slow_pressure 场景内节奏单一 | 在蓄压中加入 1-2 个微释放点 |
| 爆发场来得太快 | explosive_burst 前没有足够的蓄压 | 补充 slow_pressure 场景作为铺垫 |

---

## Reusable Heuristics

- 节奏不是"快就好"或"慢就好"，而是有设计的起伏。好的节奏让观众在高潮时到达情绪峰值，在低谷时获得呼吸。
- 场景长度不是信息量决定的，而是节奏位置决定的。高潮场景可以很短（爆发冲击），铺垫场景可以很长（缓慢蓄压）。
- 过渡方式是场景间的呼吸。全部硬切等于不呼吸，观众会窒息。
- 留白场不是空场。留白场的信息密度低，但情绪密度可以很高——沉默、凝视、空间本身都在说话。
- 类型决定了节奏基线，但好作品会在类型基线上制造意外。校园怪谈里的一场日常温暖，比十场恐惧更有力量。
