# Scope Package: Structure Topology

## Selection Signals

- 卷章结构、章节数、章节顺序、任务分配、章节窗口、卷标签、上下文回流、validated actual 拓扑。

## When X Then Check X

| when | must check |
| --- | --- |
| 改章节数或顺序 | 整体规划、卷规划、所有章规划、STATE、handoff |
| 改卷级任务分配 | 卷规划、章级任务、已产出章节、stage acceptance packet |
| 改上下文回流拓扑 | return actualization、项目 CONTEXT carryover、下一卷起点 |
| 改 validated actual | accepted manuscript refs、STATE、后续 provider context |

## Required Impact Additions

- `book_plan_ref`
- `volume_plan_refs`
- `chapter_window_refs`
- `state_refs`
- `handoff_refs`

## Review Gate

- 章节编号、卷标签、任务分配和后续消费路径一致。
- return carryover 不再引用旧拓扑。
