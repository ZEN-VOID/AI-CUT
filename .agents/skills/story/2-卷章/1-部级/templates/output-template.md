# 整体规划

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | `projects/story/<项目名>/2-卷章/整体规划.md` |
| Output format | Markdown；包含部级九个必填标题、整部悬念总设计、整书悬念池和 Mermaid 节奏图 |
| Output path | `projects/story/<项目名>/2-卷章/整体规划.md` |
| Naming convention | 文件名固定为 `整体规划.md`；机器字段和任务 ID 保持 ASCII 安全字符 |
| Completion gate | 通过 `review/review-contract.md`，并可交给 `2-卷级` |

## Template Body

书名：

整体故事大纲：

故事编年史：
- `chronology_axis`：
  - `prehistory_events`：
  - `main_story_start`：
  - `volume_time_spans`：
  - `causal_milestones`：
  - `hidden_events`：
  - `end_state`：

卷划分：

整部任务关系：
- 主任务树：
- 卷级支流簇：
- 关键汇聚里程碑：

整体冲突：

整部悬念总设计：
- 核心真相/核心谜面：
- 整书悬念池：
  - `suspense_id`：
  - `suspense_name`：
  - `suspense_type`：
  - `priority`：
  - `status`：
  - `owner_level`：
  - `reveal_window`：
  - `dependency`：
  - `reader_state`：
  - `pov_state`：
  - `next_action`：
- 读者认知曲线：
- 主角认知曲线：
- 卷级揭秘节奏：
- 长线误导策略：
- 多重悬念编排规则：
- 禁止提前揭露：
- 终局回收要求：

整体节奏曲线：
- 长线 promise 走廊：
- 长线升压走廊：
- 卷职责分配：
  - 前半承诺交付卷：
  - `Midpoint` 改规卷：
  - `All Is Lost` 见底卷：
  - `Finale` 收束卷：
- 节奏高点说明：
  - 承诺高点：
  - 转折高点：
  - 见底高点：
  - 收束高点：
- `book_wave_map`：
  - `volume_intensity_map`：
  - `volume_role_map`：
  - `respite_corridor`：
  - `payoff_distribution`：

```mermaid
flowchart TD
    A["Opening / Promise"] --> B["Break into Two"]
    B --> C["Midpoint"]
    C --> D["All Is Lost"]
    D --> E["Finale"]
```

规避：
