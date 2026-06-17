# Book-Level Output Contract

本文件展开 `story-plan-book-level` 的部级输出字段和硬规则。入口、路由和完成门禁仍以同目录 `SKILL.md` 为准。

## Required Headings

1. `书名：`
2. `整体故事大纲：`
3. `故事编年史：`
4. `卷划分：`
5. `整部任务关系：`
6. `整体冲突：`
7. `整部悬念总设计：`
8. `整体节奏曲线：`
9. `规避：`

## Field Rules

| heading | must contain | must not contain |
| --- | --- | --- |
| `书名` | 能承载类型承诺、核心意象或主问题 | 临时编号、空泛系列名 |
| `整体故事大纲` | 主问题、主角推进、阶段性变化、终局方向 | 只有世界观介绍或设定堆叠 |
| `故事编年史` | `chronology_axis / prehistory_events / main_story_start / volume_time_spans / causal_milestones / hidden_events / end_state` | 只写节奏高低、卷名列表或无因果年表 |
| `卷划分` | 每卷标题、核心功能、阶段职责、交接方式 | 只有卷名列表 |
| `整部任务关系` | `主任务树 / 卷级支流簇 / 关键汇聚里程碑` | 只靠卷划分暗示任务从属 |
| `整体冲突` | 核心对抗轴、主要冲突走廊、终局冲突收束方向 | 局部场景冲突清单 |
| `整部悬念总设计` | `核心真相/核心谜面 / 整书悬念池 / 读者认知曲线 / 主角认知曲线 / 卷级揭秘节奏 / 长线误导策略 / 多重悬念编排规则 / 禁止提前揭露 / 终局回收要求` | 一次性讲透真相、只写“保持神秘感”、无回收承诺的假悬念、没有 ID 的谜团堆叠 |
| `整体节奏曲线` | Save the Cat 15 步长篇拍点走廊、卷职责分配、`book_wave_map`、Mermaid 图 | 银幕百分比硬切或单卷节奏细节 |
| `规避` | 创作层禁飞区和下游可执行限制 | 空泛提醒、口号、纯审美形容 |

## Hard Rules

1. `整体故事大纲` 必须说明主问题、主角推进和整体终局方向。
2. `故事编年史` 必须说明前史、正篇起点、各卷时间跨度、关键因果里程碑、幕后事件与终局状态。
3. `故事编年史` 不得只写成节奏曲线或卷职责列表；它必须锁世界内事件顺序和状态变化。
4. `卷划分` 不能只是卷名列表，至少要写每卷核心功能与阶段职责。
5. `整部任务关系` 必须至少写清 `主任务树 / 卷级支流簇 / 关键汇聚里程碑`。
6. `整体冲突` 必须说明整部作品的核心对抗轴、主要冲突走廊与终局冲突收束方向。
7. `整部悬念总设计` 必须显式区分整书真实谜底、读者认知曲线和主角认知曲线，不得把完整真相直接交给读者。
8. `整部悬念总设计` 必须给卷级下钻提供揭秘节奏、长线误导策略、禁止提前揭露和终局回收要求。
9. `整书悬念池` 必须列出主要悬念线程，并至少包含 `suspense_id / suspense_type / priority / status / owner_level / reveal_window / dependency / next_action`。
10. `多重悬念编排规则` 必须说明主悬念、次悬念、局部悬念和误导悬念如何遮蔽、递进、互证或分流。
11. `整体节奏曲线` 必须默认采用 `Save the Cat 15 步`，并附 Mermaid 图。
12. `整体节奏曲线` 必须显式回答：长线 promise 如何分配到各卷、哪段卷级走廊承担改规、哪段卷级走廊承担见底与终局收束。
13. `整体节奏曲线` 必须包含 `book_wave_map`，并写清 `volume_intensity_map / volume_role_map / respite_corridor / payoff_distribution`。
14. `规避` 必须是创作层禁飞区，而不是空泛提醒。

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 部级输出是否具备全部必填标题和字段？ | 缺 `书名 / 整体故事大纲 / 故事编年史 / 卷划分 / 整部任务关系 / 整体冲突 / 整部悬念总设计 / 整体节奏曲线 / 规避` 任一标题或硬字段即失败 | `FAIL-BOOK-OUTPUT` | `SKILL.md#Thinking-Action Node Map` | 缺失标题、缺失字段和对应节点 |
| 输出是否仍停留在 planning 层并可交给卷级？ | 出现正文段落、卡册复制、只写口号或无法供卷级继承即失败 | `FAIL-BOOK-OUTPUT` | `SKILL.md#Review Gate Binding` | planning-only 检查和卷级 handoff 证据 |
