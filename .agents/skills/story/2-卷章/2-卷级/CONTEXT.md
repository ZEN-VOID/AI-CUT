# CONTEXT.md

本文件是 `story-plan-volume-level` 的经验层知识库，不是执行合同，也不是任务流水。执行时必须先以 `SKILL.md` 锁定入口与输出，再用本文件选择修复策略和避坑口径。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 卷级像缩写版总纲 | volume-level thinness | 补卷职责、章功能和卷末达成 | 在模板固定卷级六拍和章功能 | `第N卷/卷规划.md` 具备中观密度 |
| 卷级任务线没有主支区分 | mission folding drift | 补 `主线 / 支线` | 在模板写死段落名 | 章级能承接任务线 |
| 卷级没有本卷时间线 | volume chronology gap | 补 `本卷时间线` 的起止状态、章节事件顺序、并行/幕后事件、时间跳跃或压缩和卷末状态 | 在模板和 review gate 固定时间线槽位 | 章级能继承每章事件顺序与状态变化 |
| 本卷时间线漂离部级编年史 | chronology inheritance drift | 回读 `整体规划.md` 的 `故事编年史` 后重写本卷时间线 | 在 steps 固定上游时间线回读 | 卷级不改写整部关键因果 |
| 卷级支线没有回主线方案 | task aggregation drift | 补 `汇聚回主线` 与 `下钻章级任务分配` | 把汇聚槽位固定进模板 | 章级不会把支流写成游离副本 |
| 卷级只给六拍不给章级配器 | orchestration gap | 补 `volume_orchestration_map`，写清每章 payoff、强度、respite/pressure 与章级 handoff | 在模板和 review gate 固定中波配器槽位 | 章级不必重新猜每章强度和读者满足 |
| 卷级只管剧情，不管资源 | planning resource gap | 补人物/场景/道具 | 在模板固定三组资源段落 | 章级不再临时发明 |
| 卷级技能包结构不完整 | Skill 2.0 layout drift | 补 `review/steps/types/knowledge-base/agents/scripts` 与根文件 | 用工作车间 validator 作为结构门 | validator 返回 `[OK]` |

## Repair Playbook

1. 若缺 `整体规划.md`，先停止卷级落盘，只报告缺上游真源。
2. 若卷级规划像总纲摘要，先补“本卷职责 + 章划分功能 + 卷末达成”，再补人物/场景/道具。
3. 若卷级时间顺序不清，先补 `本卷时间线`，再谈节奏和任务线。
4. 若节奏误套部级 `Save the Cat 15 步`，立刻回到 `references/volume-rhythm-framework.md` 改成六拍。
5. 若章级无法继承中波职责，补 `volume_orchestration_map`，先写 `chapter_payoff_map / chapter_intensity_map / respite_chapters / pressure_chapters / handoff_to_chapter_level`。
6. 若任务线漂成支线列表，强制补 `上承部级主任务 / 主线 / 支线 / 支流角色 / 下钻章级任务分配 / 汇聚回主线`。
6. 若只是局部修订，读取旧 `卷规划.md` 后只 patch 相关段落，避免重写用户未要求修改的卷内容。
7. 若模板与 `SKILL.md` Output Contract 冲突，以 `SKILL.md` 为准，修复 `templates/output-template.md`。
8. 若技能包结构校验失败，先修 canonical 目录和缺失 marker，再处理业务语义。

## Reusable Heuristics

- 卷级最怕平均主义，每卷必须有不同 duty。
- `本卷时间线` 是章节事件顺序的真源；它可以服务悬念和倒叙，但不能让世界内因果失踪。
- 如果卷末达成写不清，多半说明卷故事大纲其实没有真正收束。
- 卷级 `支线` 不是“额外热闹”，而是要么服务主线，要么制造下一轮必须回收的压力。
- 六拍不是六段剧情梗概，而是六个追读职责；每一拍都要能映射到章节职责。
- `volume_orchestration_map` 是中波配器表；它只给章级 payoff 和强度建议，不替章级决定 `selected_mode`。
- `本卷登场人物 / 场景 / 道具` 只做 planning 所需的最小投影，不复制卡册正文。
