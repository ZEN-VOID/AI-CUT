# Volume Planning Review Contract

本文件定义 `2-卷级` 的质量门禁。它不拥有业务主真源改写权，只给出 verdict、findings 与返工目标。

## Default Provider

- 默认辅助 provider：`code-reviewer` 或等价 subagent reviewer。
- 若上层策略阻断真实 reviewer/subagent，允许降级为主 agent 本地 review，但必须报告阻断层级、原路径、实际路径和未启动 reviewer。

## Review Flow

```mermaid
flowchart TD
    A["读取卷规划.md"] --> B["检查上游锚点"]
    B --> C["检查 required headings"]
    C --> D["检查本卷时间线"]
    D --> E["检查六拍节奏、配器表与 Mermaid"]
    E --> F["检查人物/场景/道具/任务线"]
    F --> G["检查卷末达成与规避"]
    G --> H{"verdict"}
    H -->|"pass"| I["可交付"]
    H -->|"needs_rework"| J["返回对应 owner"]
```

## Checks

| dimension | checks |
| --- | --- |
| upstream | 是否显式服从 `整体规划.md` 中目标卷职责 |
| headings | 是否包含 `references/volume-planning-contract.md` 的 12 个 required headings |
| timeline | 是否包含 `volume_time_span / chapter_chronology / parallel_hidden_events / time_jumps_or_compression / volume_end_state`，并继承部级 `故事编年史` |
| chapter_partition | `章划分` 是否说明每章功能，而不是只列章名 |
| conflict | 是否包含主冲突、副冲突、升级机制与卷末状态 |
| rhythm | 是否使用六拍、章节职责分配、`volume_orchestration_map` 和 Mermaid 图 |
| orchestration | 是否包含 `volume_orchestration_map`，并写清章节 payoff、强度、respite/pressure 与章级 handoff |
| resources | 人物、场景、道具是否为本卷最小可执行投影 |
| mission | 是否写清 `上承部级主任务 / 主线 / 支线 / 支流角色 / 下钻章级任务分配 / 汇聚回主线` |
| planning_only | 是否避免正文、对白和章级 pack/mode 越权 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可供 `3-章级` 消费 |
| `pass_with_followups` | 可交付，但存在非阻断优化项 |
| `needs_rework` | 有阻断缺口，必须返工 |
| `blocked` | 缺上游总纲、项目根或目标卷定位 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: upstream | headings | timeline | rhythm | orchestration | mission | resources | planning_only
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Completion Gate

不得在以下情况宣布卷级规划完成：

- 缺 `整体规划.md` 或无法确定目标卷职责。
- 缺任一 required heading。
- `本卷时间线` 缺失，或没有写清 `volume_time_span / chapter_chronology / parallel_hidden_events / time_jumps_or_compression / volume_end_state`。
- `本卷节奏曲线` 没有六拍、`volume_orchestration_map` 或 Mermaid 图。
- 缺 `volume_orchestration_map`，或没有写清 `chapter_payoff_map / chapter_intensity_map / respite_chapters / pressure_chapters / handoff_to_chapter_level`。
- `本卷任务线` 没有上承部级主任务或汇聚回主线。
- 输出包含正文段落、对白或章级 `selected_pack / selected_mode` 决策。
