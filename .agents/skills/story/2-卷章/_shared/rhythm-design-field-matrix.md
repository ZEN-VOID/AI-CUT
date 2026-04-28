# Rhythm Design Field Matrix

用于统一裁定 `2-卷章/1-部级`、`2-卷章/2-卷级`、`2-卷章/3-章级` 三层节奏设计各自真正 owning 的规划维度。

## Layer Summary

| 层级 | 节奏对象 | 核心问题 | 下游消费者 |
| --- | --- | --- | --- |
| `1-部级` | 整书长波节奏 | 这本书整体何时立 promise、何时改规、何时见底、何时收束 | `2-卷级` |
| `2-卷级` | 单卷中波节奏 | 这一卷作为追读单元，如何起势、首回报、反拧、冲顶、交接 | `3-章级` |
| `3-章级` | 单章短波 handoff | 这一章具体怎样跑，并如何把节奏执行蓝图交给 drafting | `3-初稿 Step 2 / 2-节奏优化` |

## Ownership Matrix

| 维度 | `1-部级` | `2-卷级` | `3-章级` |
| --- | --- | --- | --- |
| 节奏作用域 | 整部作品 | 单卷 | 单章 |
| 主要波形 | 长波 | 中波 | 短波 |
| 默认框架 | `Save the Cat 15 步` | 六拍机制 | 七步结构 + `动静结合` |
| owning 的 promise 问题 | 整书 promise 如何跨卷分配 | 本卷 promise 如何作为独立追读单元成立 | 本章 promise 如何在正文前段被感知 |
| owning 的转折问题 | 哪一卷承担整书改规 | 中卷怎样反拧而不是只加码 | 本章哪一步真正改向 |
| owning 的 payoff 问题 | 哪些卷承担前半兑现、见底、恢复、终局回收 | 本卷首回报、卷内换气与卷末冲顶怎样成立 | 本章爽点如何设计，并怎样压缩为 `payoff_type / micro_payoff` |
| owning 的 hook 问题 | 整书怎样维持跨卷续推 | 本卷尾钩怎样交接给下一卷 | 本章 `exit_hook` 怎样交给 drafting |
| owning 的 intensity 问题 | 每卷在整书中的力度曲线与呼吸位置 | 每章在本卷六拍中的强度分配 | 本章 `rhythm_intensity` 怎样落到正文前 |
| owning 的 respite 问题 | 哪些卷/卷段承担松弛、恢复、世界感和关系升温 | 哪些章节允许或需要浪能式换气 | 本章浪能 payoff 如何不空转 |
| 允许细度 | 卷职责级 | 章节职责级 | drafting handoff 级 |
| 禁止越权 | 不写卷内章级节奏与正文顺序 | 不写单章 pack/mode 与正文排版 | 不直接写正文段落 |

## 1-部级 Field Matrix

### 节奏设计目标

- 设计整书波形，而不是局部卷内快慢。
- 分配每卷在整书节奏中的职责。
- 指明整书级 promise、规则改写、见底、终局收束落在哪些卷走廊。

### 必须回答的问题

1. 哪几卷承担前半 promise 交付。
2. `Midpoint` 怎样改写整部作品的游戏规则。
3. `All Is Lost` 与 `Finale` 分别落在哪段卷级走廊。
4. 哪些卷是升压卷，哪些卷是转向卷，哪些卷是收束卷。
5. 哪些卷承担恢复、松弛、世界感扩展或关系升温的 respite corridor。

### 建议固定字段

- `长线 promise 走廊`
- `长线升压走廊`
- `卷职责分配`
  - `前半承诺交付卷`
  - `Midpoint 改规卷`
  - `All Is Lost 见底卷`
  - `Finale 收束卷`
- `节奏高点说明`
  - `承诺高点`
  - `转折高点`
  - `见底高点`
  - `收束高点`
- `book_wave_map`
  - `volume_intensity_map`
  - `volume_role_map`
  - `respite_corridor`
  - `payoff_distribution`

### 下游 handoff

- 把“每卷承担什么整书节奏职责”交给 `2-卷级`。
- 把每卷的力度、主 payoff 倾向和 respite / pressure 职责交给 `2-卷级`。
- 不交正文层面的 scene order、段落呼吸或章内 pulse。

### 常见误判

- 把部级节奏写成银幕百分比切段。
- 把多卷写成同一强度的重复推进。
- 只写卷名与大纲，不写整书波形职责。
- 只有高点，没有恢复、松弛、关系升温或世界感扩展的呼吸走廊。

## 2-卷级 Field Matrix

### 节奏设计目标

- 设计一卷作为“追读单元”的波形。
- 把本卷六拍映射到章节职责分配。
- 处理本卷起势、首回报、反拧、冲顶与跨卷交接。

### 必须回答的问题

1. 本卷新的 promise 或新压力是什么。
2. 本卷前半第一次回报落在哪几章。
3. 本卷中段怎样反拧，而不是只加码。
4. 本卷冲顶发生在哪几章，完成什么。
5. 本卷尾钩怎样把压力交给下一卷。
6. 本卷如何把六拍拆成章节级的 payoff、强度和换气安排。

### 建议固定字段

- `本卷 promise`
- `六拍职责`
  - `卷钩`
  - `铺展`
  - `首回报`
  - `中卷反拧`
  - `卷末冲顶`
  - `尾钩/收束`
- `章节职责分配`
  - `起势章节`
  - `首回报章节`
  - `反拧章节`
  - `冲顶章节`
  - `交接章节`
- `volume_orchestration_map`
  - `chapter_payoff_map`
  - `chapter_intensity_map`
  - `respite_chapters`
  - `pressure_chapters`
  - `handoff_to_chapter_level`

### 下游 handoff

- 把“每章在本卷六拍中承担什么职责”交给 `3-章级`。
- 把每章的建议 payoff 倾向、建议强度、是否需要浪能式换气交给 `3-章级`。
- 不直接锁单章 `selected_pack / selected_mode`。

### 常见误判

- 直接把部级 15 步缩小一轮塞进单卷。
- 本卷前半连续多章只铺不收。
- 中卷没有反拧，只有更大声量的重复加码。
- 卷级只给六拍名，不给章节强度与 payoff 倾向，导致章级必须重新猜中波配器。
- 把所有章节都推成高压，导致章级没有合法的浪能式或低强度恢复空间。

## 3-章级 Field Matrix

### 节奏设计目标

- 设计单章执行蓝图，而不是直接写正文。
- 把章级节奏 handoff 结构化给 `3-初稿 Step 2 / 2-节奏优化`。
- 区分结构义务与建议写法。

### 必须回答的问题

1. 当前章采用哪个 `selected_pack / selected_mode`，以及选择该 mode 的 planning 证据是什么。
2. 本章主要 `payoff_type`、`rhythm_intensity` 与前后章节奏对比是什么。
3. 本章主爽点的读者期待、上承 promise、爽点形态、蓄势、兑现动作、满足差值、代价余波与余味牵引是什么。
4. 七步各自承担什么推进职责。
5. 本章 `entry_promise / conflict_axis / micro_payoff / exit_hook` 是什么。
6. 哪些段位必须兑现，哪些只是建议写法。

### 建议固定字段

- `selected_pack`
- `selected_mode`
- `mode_selection_reason`
- `payoff_type`
- `rhythm_intensity`
- `previous_next_contrast`
- `本章爽点设计`
  - `reader_desire`
  - `promise_source`
  - `payoff_mode`
  - `build_up`
  - `delivery_action`
  - `satisfaction_delta`
  - `cost_or_aftershock`
  - `aftertaste_hook`
- `七步职责映射`
- `规划义务`
  - `entry_promise`
  - `conflict_axis`
  - `micro_payoff`
  - `exit_hook`
- `义务段位`
- `建议写法`

### 下游 handoff

- 把结构义务、mode、mode 选择理由、payoff 类型、节奏强度、前后章波形意图与建议写法交给 `3-初稿 Step 2 / 2-节奏优化`。
- 把章级爽点设计交给 drafting 作为读者满足真源；drafting 可以重排兑现方式，但不得静默改写主爽点。
- 不直接锁正文句段、段长与最终 pulse ladder。

### 常见误判

- 只有“本章节奏曲线”一句自然语言，没有结构化 handoff。
- `selected_mode` 只有枚举值，没有能回指本章冲突、任务、信息压力或 `micro_payoff` 的选择理由。
- 只写本章内部七步，不说明与上一章/下一章的节奏对比，导致长篇波形变平。
- 把 `rhythm_intensity=高` 当作默认好选择，导致高点密度过高、真正爆点失效。
- 把 `浪能式` 误解成“没有推进”；浪能式也必须有情绪、关系、世界感、软信息或状态修复层面的 `micro_payoff`。
- 把爽点设计压扁成 `payoff_type` 单字段，导致 drafting 不知道读者欲望、兑现动作和余味牵引。
- 把建议写法写成不可动的硬法律。
- 把正文句段直接写进章级规划。

## Non-Drift Rules

1. `1-部级` 只处理整书波形，不偷写卷内章节排兵。
2. `2-卷级` 只处理单卷波形与章节职责，不偷写章内 pack/mode。
3. `3-章级` 只处理节奏 handoff，不偷写正文节奏兑现。
4. 任何层级若回答的问题已经需要“段落并拆、reaction bridge、middle build”，那已经越界到 drafting。
