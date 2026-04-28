# Volume Planning Contract

本文件承载 `2-卷级` 的业务规则展开。入口、路由和输出验收仍以 `../SKILL.md` 为准。

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把整部总纲拆解成单卷可执行的中观规划。 |
| `business_object` | `2-卷章/第N卷/卷规划.md`、`2-卷章/整体规划.md`、`类型卡`、`角色卡 / 场景卡 / 物品卡 / 技能卡`。 |
| `constraint_profile` | 卷级时间线必须继承部级 `故事编年史`，锁定本卷起止状态、章节事件顺序、并行/幕后事件、时间跳跃或压缩；卷级节奏不能直接复制部级 15 步，必须使用卷级六拍机制；节奏字段必须符合 `rhythm-design-field-matrix.md` 中的卷级定义，并通过 `volume_orchestration_map` 向章级传递 payoff、强度和换气安排。 |
| `success_criteria` | 单卷规划可直接供章级细化，不需要再补一层“冲突/任务/道具/时间线”独立 skill；同时能看清本卷事件怎样按世界内顺序发生、本卷任务怎样从属于部级主任务、哪些支流在本卷扩张、最终如何汇聚回主线。 |

## Required Headings

1. `卷标题：`
2. `本卷故事大纲：`
3. `本卷时间线：`
4. `章划分：`
5. `本卷冲突：`
6. `本卷节奏曲线：`
7. `本卷登场人物：`
8. `本卷主要场景：`
9. `本卷关键道具：`
10. `本卷任务线`
11. `卷末达成：`
12. `规避：`

## Hard Rules

1. `本卷时间线` 必须写清 `volume_time_span / chapter_chronology / parallel_hidden_events / time_jumps_or_compression / volume_end_state`。
2. `本卷时间线` 必须继承部级 `故事编年史`，不得静默改变目标卷的时间跨度、关键因果或幕后事件锚点。
3. `章划分` 至少要说明每章功能，不得只列章名。
4. `本卷冲突` 必须说明本卷主冲突、副冲突、冲突升级机制与卷末冲突状态。
5. `本卷节奏曲线` 必须采用卷级六拍机制，并附 Mermaid 图。
6. `本卷节奏曲线` 必须显式说明：本卷 promise、首回报、中卷反拧、卷末冲顶与跨卷交接分别落在哪些章节职责上。
7. `本卷节奏曲线` 必须包含 `volume_orchestration_map`，并写清 `chapter_payoff_map / chapter_intensity_map / respite_chapters / pressure_chapters / handoff_to_chapter_level`。
8. `本卷任务线` 必须至少写清 `上承部级主任务 / 主线 / 支线 / 支流角色 / 下钻章级任务分配 / 汇聚回主线`，不再单列旧 `任务设计` 技能。
9. 旧 `冲突 / 线索 / 伏笔` 的卷级取舍，应内化在卷故事大纲、章划分和任务线里，而不是另起并列 skill。
10. 任何卷级局部修订都必须以上游 `2-卷章/整体规划.md` 为最高上下文，不得让卷级局部修订静默漂离整部总纲。
11. 卷级不得锁定章级 `selected_pack / selected_mode`，这些属于 `3-章级`。

## Resource Projection Rules

- `本卷登场人物`：只写本卷所需人物、关系压力和任务钩子，不复制角色卡全量背景。
- `本卷主要场景`：只写本卷中承担冲突、揭示或转向功能的场景，不建立第二场景卡册。
- `本卷关键道具`：只写本卷会被使用、争夺、误读或交接的道具，不做静态清单堆叠。

## Handoff To Chapter Level

`2-卷级` 给 `3-章级` 的 handoff 必须包含：

- 每章功能职责。
- 每章在本卷时间线里的事件顺序和状态变化。
- 本卷六拍对应的章节位置。
- 每章建议 `payoff_type` 倾向与 `rhythm_intensity` 倾向。
- 哪些章节建议承担 respite / pressure。
- 主线与支线在章级的分配建议。
- 未汇聚任务的去向和回主线要求。
