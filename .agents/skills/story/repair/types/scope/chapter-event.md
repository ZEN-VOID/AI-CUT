# Scope Package: Chapter Event

## Selection Signals

- 章节事件、情节事实、场面动作、冲突结果、章末钩子、任务完成/失败。

## When X Then Check X

| when | must check |
| --- | --- |
| 改当前章事件 | 当前章规划、上一章结尾、相关角色/物品/场景卡 |
| 改事件结果 | 后续承接章、卷规划任务状态、stage acceptance packet |
| 改章末钩子 | 下一章规划、下一章开篇、provider continuity bridge |
| 改场面动作 | 场景卡、人物位置、道具状态、时间线和空间动线 |

## Required Impact Additions

- `chapter_plan_ref`
- `previous_chapter_bridge`
- `event_cause_refs`
- `event_effect_refs`
- `next_chapter_guardrail`

## Review Gate

- 事件因果、任务兑现、章末牵引和下一章承接一致。
- 当前章修复不破坏卷级节奏和任务分配。
