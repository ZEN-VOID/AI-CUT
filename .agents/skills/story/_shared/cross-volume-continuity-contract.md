# Cross-Volume Continuity Contract

本文件是 `story2026` 的跨卷叙事一致性追踪合同。它用于在多卷长篇小说中追踪伏笔、人物状态、物件/道具和能力成长的跨卷演变，防止上下文窗口限制导致细微伏笔、人物微妙变化丢失。

本文件不拥有正文写权，不是独立阶段。跨卷追踪数据由 `return` 阶段在 actualization 完成后增量生成，由 `3-初稿` 与 `4-润色` 在创作/润色时按需消费。

## Core Principle

跨卷叙事一致性不是"把前卷的关键信息全量加载进上下文"，而是用最小粒度的结构化摘要，让创作阶段能快速判断"前卷留下了什么承诺、哪些人物经历了什么变化、关键物件经历了怎样的流转"。摘要格式采用增量结构，每卷只追加变化，不重复历史全量数据。

## Four-Dimensional Tracking Model

### 1. 伏笔追踪表 (Foreshadowing Tracker)

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `foreshadow_id` | string | 唯一伏笔标识，格式 `FSH-{卷号}-{序号}` |
| `plant_volume` | integer | 埋设所在卷号 |
| `plant_chapter` | integer | 埋设所在章号（全局章号） |
| `plant_excerpt` | string (≤80字) | 伏笔埋设的关键文本摘要 |
| `promise_type` | enum | 伏笔类型：`人物身份/能力伏笔/关系伏笔/事件伏笔/物件伏笔/信息伏笔/世界观伏笔` |
| `expected_payoff_window` | string | 预期兑现窗口，如 `第3卷-第5卷` 或 `未定` |
| `status` | enum | 当前状态：`未兑现` / `部分兑现` / `已兑现` / `已废弃` |
| `payoff_records` | array | 兑现记录：`[{volume, chapter, excerpt, is_complete}]` |
| `notes` | string | 备注：跨卷关联、注意事项 |

### 2. 人物状态快照 (Character State Snapshot)

每卷完成后，为核心人物（出场角色卡中 `group` 为 `主要角色` 或 `次要角色` 且有显著情节参与的角色）生成轻量状态摘要：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `character_id` | string | 角色卡唯一 ID |
| `name` | string | 角色姓名 |
| `volume_appearance` | integer | 本卷出场卷号 |
| `chapter_range` | string | 本卷出场章范围 |
| `key_actions_this_volume` | string (≤200字) | 本卷关键行动摘要 |
| `relationship_changes` | array | 关系变化：`[{target_character, change_type, new_status, evidence_chapter}]` |
| `ability_changes` | array | 能力/修为变化：`[{ability_name, before, after, evidence_chapter}]` |
| `key_items_held` | array | 当前持有的关键物件：`[{item_name, source_volume, status}]` |
| `psychological_state` | string (≤100字) | 当前心理状态摘要 |
| `current_goal` | string (≤100字) | 当前目标/驱动 |
| `pending_promises` | array | 未兑现的承诺/伏笔：`[{promise_ref, expected_chapter}]` |

### 3. 物件/道具追踪 (Item/Prop Tracker)

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `item_id` | string | 物件唯一标识 |
| `item_name` | string | 物件名称 |
| `item_type` | enum | `线索物/装备物/装饰物/叙事物` |
| `origin_volume` | integer | 首次出现卷号 |
| `origin_chapter` | integer | 首次出现章号 |
| `transfer_history` | array | 流转记录：`[{from, to, volume, chapter, transfer_type}]` |
| `current_holder` | string | 当前持有者角色 ID |
| `status_changes` | array | 状态变化：`[{volume, chapter, change_desc}]` |
| `narrative_significance` | string (≤80字) | 叙事意义说明 |

### 4. 能力成长曲线 (Ability Growth Curve)

为主角和核心配角追踪关键能力/修为的变化序列：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `character_id` | string | 角色卡唯一 ID |
| `ability_name` | string | 能力/修为名称 |
| `milestones` | array | 成长里程碑：`[{volume, chapter, level_before, level_after, trigger_event, evidence}]` |
| `current_level` | string | 当前等级/阶段 |
| `growth_notes` | string | 成长路径备注 |

## Volume State Summary Format

每卷 actualization 完成后，`return` 阶段应生成卷级状态摘要文件：

```
projects/story/<项目名>/CONTEXT/volume-状态摘要/第V卷-状态.md
```

摘要文件标准格式：

```markdown
# 第V卷 状态摘要

## 本卷关键事件
（3-5条简述，每条≤50字）

## 伏笔变动
| ID | 类型 | 状态变化 | 摘要 |
| --- | --- | --- | --- |
| FSH-V-01 | 事件伏笔 | 新埋 | xxx |
| FSH-2-03 | 身份伏笔 | 已兑现 | xxx |

## 人物状态变化
### 人物A
- 能力变化：xxx → xxx（第N章）
- 关系变化：与人物B xxx → xxx（第N章）
- 当前目标：xxx
- 持有关键物件：xxx

## 物件流转
| 物件 | 来源 | 去向 | 当前状态 |
| --- | --- | --- | --- |

## 能力成长
| 角色 | 能力 | 变化 | 触发事件 |
| --- | --- | --- | --- |

## 跨卷待办
- 第2卷埋下的伏笔 FSH-2-01 尚未兑现，预期第V+1卷
- 人物C 的心理创伤尚未处理
```

## Context Loading Integration

### 3-初稿 加载策略

- **卷首章（新卷第1章）**：必须加载所有已完成卷的 `第V卷-状态.md`，但每个已完成卷只加载"伏笔变动"和"人物状态变化"两个摘要段（而非完整文件）
- **卷中章（卷内第2章起）**：按现有 `N3-CONTINUITY` 逻辑加载当前卷前序章即可；可选加载本卷的状态摘要作为参考
- **上下文控制**：10卷长篇的摘要总字数控制在 5000-15000 字以内

### 4-润色 加载策略

- 润色时可选加载当前卷的状态摘要，用于检查连续性回归
- 卷内跨章润色（P4B-CROSS-CHAPTER-CHECK）时必须加载卷级状态摘要

### return 生成策略

- 卷 actualization 完成时，必须生成 `第V卷-状态.md`
- 生成逻辑：以接受的终稿（4-润色）为数据源，LLM 辅助提取结构化信息
- 伏笔追踪需要人工/LLM 判断"是否埋了伏笔"和"是否兑现了伏笔"

## Hard Rules

1. 卷级状态摘要是对已完成卷的事实记录，不是对未写内容的承诺或规划。
2. 状态摘要不得重复角色卡中的静态信息（如基本外貌、历史背景），只记录"本卷发生的变化"。
3. 伏笔追踪以"可被读者回忆的承诺"为判断标准，不要求追踪每一个"作者认为的 hint"。
4. 人物状态快照只覆盖出场且有情节参与的角色；静态背景角色不记录。
5. 状态摘要文件不参与验收 PASS/FAIL 判定，仅作为创作辅助参考。

## Owner Routing

| task_shape | owner | output |
| --- | --- | --- |
| 卷 actualization 后生成状态摘要 | `return` | `CONTEXT/volume-状态摘要/第V卷-状态.md` |
| 新卷首章前消费跨卷状态 | `3-初稿` (N3-CONTINUITY 节点) | `cross_volume_bridge` |
| 卷内跨章一致性检查时消费 | `4-润色` (P4B 节点) | `cross_chapter_audit` |
| 查询跨卷伏笔/人物/物件信息 | `query` | 路由到 volume-状态摘要 目录 |
