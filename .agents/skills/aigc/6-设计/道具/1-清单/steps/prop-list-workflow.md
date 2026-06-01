# Prop List Workflow

## Node Map

| node_id | input | judgment | action | output | gate |
| --- | --- | --- | --- | --- | --- |
| `N1-SCOPE` | 项目路径、集号范围 | 是否能定位 `5-分组/第N集.md` | 建立输入 manifest | `source_manifest` | 输入文件可读 |
| `N2-YAML-CANDIDATES` | 分镜组文本 | 是否存在组底 YAML `道具` | 采集候选项、集号、组 ID | `prop_candidates` | 候选均来自 YAML |
| `N3-EVIDENCE` | 候选项与同组正文 | 是否需要回查正文 | 摘取关键词证据 | `evidence_notes` | 回查不越组 |
| `N4-MERGE` | 候选项与证据 | 是否同一叙事道具 | LLM 裁决归并与 canonical 名称 | `merged_props` | 无重复别名项 |
| `N5-FILTER` | `merged_props` | 是否叙事/规则/视觉/生成锁定物 | 过滤背景杂物 | `accepted_props` | 保留项有理由 |
| `N6-RENDER` | `accepted_props` | 三列字段是否齐备 | 渲染 Markdown table | `道具清单.md` | 表格三列固定 |
| `N7-REVIEW` | 清单与来源 | 是否通过 review gate | 人工 review 或机械格式检查 | `review_result` | 问题已修复或报告 |

## Workflow Topology

```mermaid
flowchart TD
    N1["N1-SCOPE<br/>锁定项目与集号范围"] --> N2["N2-YAML-CANDIDATES<br/>采集组底 YAML 道具"]
    N2 --> G1{"候选均来自 YAML?"}
    G1 -->|"No"| B1["阻断 canonical 清单<br/>输出风险或要求修复上游"]
    G1 -->|"Yes"| N3["N3-EVIDENCE<br/>同组正文证据回查"]
    N3 --> G2{"回查是否越组?"}
    G2 -->|"Yes"| B2["删除越界证据<br/>回到同组证据"]
    G2 -->|"No"| N4["N4-MERGE<br/>LLM 裁决归并"]
    B2 --> N3
    N4 --> G3{"仍有明显别名重复?"}
    G3 -->|"Yes"| N4
    G3 -->|"No"| N5["N5-FILTER<br/>过滤背景杂物"]
    N5 --> G4{"保留项有叙事/规则/视觉/生成锁定理由?"}
    G4 -->|"No"| N5
    G4 -->|"Yes"| N6["N6-RENDER<br/>渲染固定三列表格"]
    N6 --> G5{"字段仅三列?"}
    G5 -->|"No"| N6
    G5 -->|"Yes"| N7["N7-REVIEW<br/>review gate"]
    N7 --> G6{"通过?"}
    G6 -->|"Yes"| DONE["写入 道具清单.md"]
    G6 -->|"No"| FIX["按 finding 返工"]
    FIX --> N4
```

```mermaid
sequenceDiagram
    participant User as 用户/上游任务
    participant Skill as $aigc-prop-list
    participant Source as 5-分组 YAML
    participant LLM as LLM 裁决
    participant Review as Review Gate
    participant Output as 道具清单.md

    User->>Skill: 指定项目、集号或修复目标
    Skill->>Source: 读取组底 YAML 道具字段
    Source-->>Skill: 候选项、集号、分镜组 ID
    Skill->>LLM: 提交候选、同组证据、项目记忆
    LLM-->>Skill: canonical 归并、过滤、三列内容
    Skill->>Review: 来源、字段、首次登场、LLM-first 检查
    Review-->>Skill: pass / needs_fix / blocked
    Skill->>Output: 仅在通过或修复后写入 canonical 清单
```

## Evidence Rules

- `首次登场` 取同一道具最早出现的分镜组。
- `原文描述（关键词式）` 来源优先级：YAML 原词 > 同组正文可见词 > 同组动作关系词。
- 回查正文只用于证据，不用于绕过 YAML 新增候选。

## Fallback

若 YAML `道具` 字段缺失或格式异常，停止生成 canonical 清单，输出风险报告或要求先修复 `5-分组`。
