# CONTEXT.md

本文件是 `story-plan-volume-level` 的经验层知识库，不是执行合同，也不是任务流水。执行时必须先以 `SKILL.md` 锁定入口与输出，再用本文件选择修复策略和避坑口径。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 卷级像缩写版总纲 | volume-level thinness | 补卷职责、章功能和卷末达成 | 在模板固定卷级六拍和章功能 | `第N卷/卷规划.md` 具备中观密度 |
| 卷级任务线没有主支区分 | mission folding drift | 补 `主线 / 支线` | 在模板写死段落名 | 章级能承接任务线 |
| 卷级没有本卷时间线 | volume chronology gap | 补 `本卷时间线` 的起止状态、章节事件顺序、并行/幕后事件、时间跳跃或压缩和卷末状态 | 在模板和 review gate 固定时间线槽位 | 章级能继承每章事件顺序与状态变化 |
| 本卷时间线漂离部级编年史 | chronology inheritance drift | 回读 `整体规划.md` 的 `故事编年史` 后重写本卷时间线 | 在 steps 固定上游时间线回读 | 卷级不改写整部关键因果 |
| 本卷把部级核心谜底提前下放给章级正文 | volume suspense leak | 补 `本卷悬念开关`，区分本卷需要隐藏、允许露出、误导/疑阵、揭秘和延后项 | 模板、steps、review 固定悬念开关与章级约束 | 章级能知道本卷哪些信息可写、哪些必须继续扣住 |
| 本卷同时推进多条悬念但没有线程状态 | volume suspense thread gap | 补 `本卷悬念线程表` 与 `本卷悬念负载` | 线程表固定 ID、优先级、状态、依赖和 next_action | 章级能按线程执行开启、加压、误导、局部揭秘或延后 |
| 卷级支线没有回主线方案 | task aggregation drift | 补 `汇聚回主线` 与 `下钻章级任务分配` | 把汇聚槽位固定进模板 | 章级不会把支流写成游离副本 |
| 卷级只给六拍不给章级配器 | orchestration gap | 补 `volume_orchestration_map`，写清每章 payoff、强度、respite/pressure 与章级 handoff | 在模板和 review gate 固定中波配器槽位 | 章级不必重新猜每章强度和读者满足 |
| 卷级只管剧情，不管资源 | planning resource gap | 补人物/场景/道具 | 在模板固定三组资源段落 | 章级不再临时发明 |
| 卷级技能包结构不完整 | Skill 2.0 layout drift | 补 `review/steps/types/knowledge-base/agents/scripts` 与根文件 | 用工作车间 validator 作为结构门 | validator 返回 `[OK]` |
| 启用 subagents 后没有按项目顾问请教卷级执行问题 | advisor consultation gap | 按 `team.yaml` 的 `roles.planning.members` 追问本卷职责、章划分、六拍配器、悬念负载、资源和卷末兑现 | 显式启用 subagents 时先生成 `advisor_consultation_packet`，再进入卷级规划创作 | `卷规划.md` 能说明顾问建议如何转成六拍、章职责、资源投影或悬念开关指导 |

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
9. 如果显式启用 subagents，顾问问题要围绕“这一卷如何不同于上一卷/下一卷”和“哪些章节承担压力、换气、兑现”，不要让顾问泛谈剧情好坏。

## Reusable Heuristics

- 卷级最怕平均主义，每卷必须有不同 duty。
- `本卷时间线` 是章节事件顺序的真源；它可以服务悬念和倒叙，但不能让世界内因果失踪。
- `本卷悬念开关` 是章级信息释放的真源；它不替代线索/伏笔，只规定哪些信息现在能露、哪些必须藏。
- `本卷悬念负载` 是防疲劳阀门；一卷可以多线并行，但必须说明主线压力和局部压力如何分配。
- 如果卷末达成写不清，多半说明卷故事大纲其实没有真正收束。
- 卷级 `支线` 不是“额外热闹”，而是要么服务主线，要么制造下一轮必须回收的压力。
- 六拍不是六段剧情梗概，而是六个追读职责；每一拍都要能映射到章节职责。
- `volume_orchestration_map` 是中波配器表；它只给章级 payoff 和强度建议，不替章级决定 `selected_mode`。
- `本卷登场人物 / 场景 / 道具` 只做 planning 所需的最小投影，不复制卡册正文。
- 卷级顾问请教最适合用来防平均主义：把建议落成卷职责差异、章节配器、悬念负载、资源调度和卷末兑现，而不是新增一堆情节点。
