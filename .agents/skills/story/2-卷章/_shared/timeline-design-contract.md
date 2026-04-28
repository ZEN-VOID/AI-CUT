# Timeline Design Contract

`时间线体系 / 故事编年史` 是 `2-卷章` 三层规划的基础横切合同。它回答故事世界里的事件顺序、因果链、幕后同步事件与状态变化；它不替代节奏设计，也不替代高潮/爽点设计。

## Core Distinction

| system | owning question | must not replace |
| --- | --- | --- |
| 时间线体系 | 事情在故事世界里按什么顺序发生，造成什么状态变化 | 节奏、高潮、正文排布 |
| 节奏体系 | 读者体验如何起伏、何时升压、何时换气 | 世界内真实先后顺序 |
| 高潮/爽点体系 | 读者期待如何蓄势、兑现、留余味 | 事件编年和因果审计 |

## Layer Ownership

| layer | required section | ownership |
| --- | --- | --- |
| `1-部级` | `故事编年史` | 锁整部作品的前史、正篇起点、卷级时间跨度、关键因果里程碑、幕后事件与终局状态 |
| `2-卷级` | `本卷时间线` | 锁本卷起止状态、章节事件顺序、并行/幕后事件、时间跳跃或压缩、本卷结束状态 |
| `3-章级` | `本章时间推进` | 锁章前状态、章内可见时间跨度、章内事件顺序、幕后同步事件、章末状态与下一章 handoff |

## Required Fields

### 部级 `故事编年史`

- `chronology_axis`
  - `prehistory_events`
  - `main_story_start`
  - `volume_time_spans`
  - `causal_milestones`
  - `hidden_events`
  - `end_state`

### 卷级 `本卷时间线`

- `volume_time_span`
- `chapter_chronology`
- `parallel_hidden_events`
- `time_jumps_or_compression`
- `volume_end_state`

### 章级 `本章时间推进`

- `chapter_start_state`
- `visible_time_span`
- `event_order`
- `parallel_hidden_events`
- `chapter_end_state`
- `handoff_to_next_chapter`

## Handoff Rules

1. 部级只锁整部编年骨架，不细写单章内的具体事件调度。
2. 卷级必须继承部级 `volume_time_spans / causal_milestones`，不得静默改变目标卷在整部时间轴中的位置。
3. 章级必须继承卷级 `chapter_chronology`，不得让章内事件顺序与卷级章节事件顺序冲突。
4. 幕后事件必须标明它在读者视野中的状态：`未揭示 / 局部揭示 / 已揭示 / 误导性揭示`。
5. 时间跳跃、压缩、倒叙、插叙、同步并行事件都必须说明其因果功能，不能只作为文面花活。
6. 每一层都必须写清本层结束时的状态变化；没有状态变化的事件不得伪装成关键时间节点。

## Review Risks

| risk | symptom | repair |
| --- | --- | --- |
| 时间线被节奏替代 | 只写高低起伏，不写事件先后与状态变化 | 回到本合同 Required Fields |
| 编年史只有年表没有因果 | 事件列表无法解释后续章节为什么发生 | 补 `causal_milestones` 与状态变化 |
| 幕后事件凭空出现 | 后续真相没有前置时间锚点 | 补 `hidden_events / parallel_hidden_events` |
| 卷章时间错位 | 章级事件发生顺序与卷级章节职责矛盾 | 回读上层时间线并修订低层 |
| 时间跳跃无功能 | 倒叙、插叙或跳时只制造混乱 | 写清跳时服务的信息、情绪、悬念或因果功能 |
