# Episode Rhythm Rules

## Purpose

给 `2-章节规划` 的 `episode_rhythm_roles` 用的集节奏规则真源。

这里不改动现有部节奏 / 卷节奏设计，只负责回答：

1. 单集应该共用什么基础节奏骨架。
2. 在同一骨架上，如何挂接不同“子节奏包”。
3. 当前默认包 `动静结合` 应该如何进入 planning 与 drafting。

## Core Principle

集节奏不再只是一组松散职责标签，而是采用：

- 一个统一的 `seven-step base spine`
- 多个可切换的 `episode rhythm packs`
- 每个 pack 下可进一步选择 `mode / polarity / usage pattern`

默认规则：

- `seven-step base spine` 是所有集节奏包的共同底板。
- `episode_rhythm_roles` 必须先锁基础七步，再声明本集采用哪一个节奏包、哪一种 mode。
- 在有更高级方法论加入前，`动静结合` 视为当前默认集节奏方法。

## Seven-Step Base Spine

所有集节奏先共享统一七步：

1. `入场`
2. `推动`
3. `转折`
4. `发展`
5. `升级`
6. `高潮`
7. `尾钩`

### Seven-Step Questions

| base_step | 核心问题 | planning 最低交付 |
| --- | --- | --- |
| `入场` | 这一集怎样把读者拉进来？ | 开场切口、初始失衡、进入方式 |
| `推动` | 当前局面靠什么开始移动？ | 当集问题、欲望、压力或谜面 |
| `转折` | 这一集第一个明显改向在哪里？ | 首次改向点或错判翻面点 |
| `发展` | 改向后人物/局势如何继续缠绕？ | 中段发展轴、关系/矛盾延展 |
| `升级` | 哪个压力被继续推高？ | 风险升级、陷落加深或局势逼近 |
| `高潮` | 本集不可逆的最高点是什么？ | 冲突峰值、兑现或灾变节点 |
| `尾钩` | 下一集为什么必须点开？ | 余波、悬念、压力转移、未闭合期待 |

硬规则：

- 七步是基础骨架，不是要求所有集都机械等长。
- 每一集都必须能回答七步各自承担的职责。
- `episode_rhythm_roles` 若只写“这集是 midpoint-turn / pressure-squeeze”，但没有投影到七步骨架，视为集节奏规则不完整。

## Pack System

### Canonical Contract

每个集节奏包至少声明：

- `pack_id`
- `pack_label`
- `base_spine_alignment`
- `mode_catalog`
- `polarity_usage_rule`
- `fit_signals`
- `misuse_signals`

### Current Default Pack

- `pack_id`: `dynamic-static-duality`
- `pack_label`: `动静结合`
- `default_status`: `active-default`

## Pack 01: 动静结合

### Positioning

`动静结合` 是一个二元一体的集节奏包。

它由两种互补 mode 组成：

- `势能式`
- `动能式`

它们共享同一套七步骨架，但进入方式、推进方式和高潮质感不同。

### Polarity Rule

- `势能式` 偏阴：
  - 蓄压
  - 纠葛
  - 内伤
  - 逃避
  - 越陷越深
- `动能式` 偏阳：
  - 激突
  - 迷阵
  - 反打
  - 升压
  - 冲击兑现

使用规则：

- 可一集阴一集阳交替。
- 也可若干集偏阴，随后若干集偏阳。
- 编排目标不是平均分配，而是让整部作品像由两种节奏音符共同谱写。

planning 层至少要回答：

- 当前集为什么选 `势能式` 或 `动能式`
- 与前后集的阴阳关系是什么
- 本集承担“蓄势 / 爆发 / 转调 / 回声”中的哪一种 duty

## Mode A: 势能式

### Tone

偏静中有压、缓中有刺、表面平静而内里持续积压。

### Seven-Step Projection

| base_step | 势能式默认写法 |
| --- | --- |
| `入场` | 回忆、梦境、碎片蒙太奇、快闪事件或其他非稳态开篇 |
| `推动` | 醒来、转场、落回当下，面对一种表面平静 |
| `转折` | 矛盾开始显形、旧伤或纠葛被重新拉开 |
| `发展` | 人物以无所谓、戏谑、轻慢、自嘲等方式对待问题 |
| `升级` | 逃避、拖延、错置回应，导致矛盾或纠葛越陷越深 |
| `高潮` | 抵达不可逆转的矛盾高点，关系/局势被迫穿透 |
| `尾钩` | 把未化解的压强留到下一集，形成追读牵引 |

### Fit Signals

- 这一集更适合写余震、心病、宿债、未说破关系、静场压迫。
- 戏剧张力来自“越不面对，越无法收场”。
- 高潮不是最大动作，而是最大不可逆。

### Misuse Signals

- 只有氛围和回忆，没有真实矛盾推进。
- 一直压着不爆，导致第 6 步没有真正不可逆。
- 用“静”掩盖无事发生。

## Mode B: 动能式

### Tone

偏烈、偏显、偏外放，强调冲击力、迷阵感、翻面感和高压兑现。

### Seven-Step Projection

| base_step | 动能式默认写法 |
| --- | --- |
| `入场` | 开场爽点、激突、突发对撞或高压事件 |
| `推动` | 抛出悬念、迷阵、错位信息或危险诱饵 |
| `转折` | 第一轮反转，打破观众对局势的初始判断 |
| `发展` | 新局面继续推进，人物在新压力下重新布局 |
| `升级` | 再次反转、再度升压、战线外扩或代价上升 |
| `高潮` | 冲突高潮；可借鉴强冲击叙事的做法，用权力翻覆、成人后果、暴烈代价等高压元素形成压顶感 |
| `尾钩` | 在高压余震或更大迷阵上收束到下一集 |

### Fit Signals

- 当前集需要明显外压、强冲突、快速翻面。
- 卖点依赖爽点、激突、迷局、强刺激推进。
- 高潮需要给读者明显“炸到位”的体感。

### Misuse Signals

- 只有噪音和事件，没有迷阵或反转结构。
- 第 4-5 步只是重复加码，没有真正翻面。
- 高潮只靠尺度堆砌，没有前面积累的局势压力。

## Planning Writeback Contract

`episode_rhythm_roles` 至少应能表达：

- `episode_id / chapter_range`
- `selected_pack_id`
- `selected_mode`
- `yin_yang_polarity`
- `polarity_sequence_note`
- `base_spine_projection`
- `entry_promise`
- `exit_hook`
- `why_this_pack`

推荐写法：

- 先写这集的 `role duty`
- 再写采用哪个 `pack + mode`
- 再把七步骨架映射成当集的具体推进说明

## Drafting Handoff

下游 `3-Drafting/2-节奏优化` 默认消费：

- `episode_rhythm_framework.default_pack`
- `episode_rhythm_framework.base_spine_steps`
- 当前集 `episode_rhythm_roles[].selected_pack_id`
- 当前集 `episode_rhythm_roles[].selected_mode`
- 当前集 `episode_rhythm_roles[].base_spine_projection`

`3-Drafting` 不应再自行发明本集是偏阴还是偏阳；若 planning 已声明，就应优先服从 planning。

## Future Extension Rule

未来允许继续新增更高级节奏包，但必须遵守：

- 不得绕开统一七步骨架另起第二套基础结构。
- 新 pack 必须说明它如何映射到七步，而不是只给抽象美学描述。
- 新 pack 必须写清适配信号、误用信号和与相邻 pack 的边界。
