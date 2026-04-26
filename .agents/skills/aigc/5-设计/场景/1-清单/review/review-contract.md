# Review Contract

## Review Goals

场景清单验收聚焦来源、归并、字段和越权边界。

## Review Flow

```mermaid
flowchart TD
    A["读取 场景清单.md"] --> B["核对候选来源记录"]
    B --> C{"每行可回指 YAML 场景字段?"}
    C -->|"否"| D["rework: N2-YAML-SCAN"]
    C -->|"是"| E{"表头是否固定三列?"}
    E -->|"否"| F["rework: N6-RENDER"]
    E -->|"是"| G{"首次登场是否最早?"}
    G -->|"否"| H["rework: N5-MERGE"]
    G -->|"是"| I{"归并/拆分是否有证据?"}
    I -->|"否"| J["rework: N3-EVIDENCE"]
    I -->|"是"| K{"是否越权扩写设计?"}
    K -->|"是"| F
    K -->|"否"| L{"是否仍有待核风险?"}
    L -->|"是"| M["pass_with_risks"]
    L -->|"否"| N["pass"]
```

## Checklist

| check_id | requirement | severity |
| --- | --- | --- |
| `REV-SCENE-01` | 每个场景主体都能回指至少一个组底 YAML `场景` 字段 | blocking |
| `REV-SCENE-02` | 表格字段固定为 `名称`、`首次登场`、`原文描述（关键词式）` | blocking |
| `REV-SCENE-03` | `首次登场` 是归并后最早分镜组 ID | blocking |
| `REV-SCENE-04` | 别名、代称、区域、时段、子空间处理有可解释依据 | major |
| `REV-SCENE-05` | 没有把不同空间误合，也没有把同一空间机械重复拆分 | major |
| `REV-SCENE-06` | 关键词没有扩写成场景设计、视觉方案或新增设定 | major |
| `REV-SCENE-07` | 脚本只做机械校验，没有生成归并或创作性裁决 | blocking |

## Finding Schema

| field | required | meaning |
| --- | --- | --- |
| `check_id` | yes | 命中的 review 条目。 |
| `severity` | yes | `blocking`、`major` 或 `minor`。 |
| `scene_name` | yes | 涉及的 canonical 场景名或候选值。 |
| `evidence` | yes | YAML 来源、分镜组 ID、表格行或缺失证据说明。 |
| `route` | yes | 返工目标节点：`N2-YAML-SCAN`、`N3-EVIDENCE`、`N5-MERGE` 或 `N6-RENDER`。 |
| `suggested_fix` | yes | 最小修复动作，不直接替主执行者改写真源。 |

## Verdict

| verdict | meaning |
| --- | --- |
| `pass` | 可交付 |
| `pass_with_risks` | 可交付，但报告中必须列出待核风险 |
| `rework` | 必须回到对应 workflow 节点修复 |

## Severity Routing

| severity | effect | required_action |
| --- | --- | --- |
| `blocking` | 不可交付 | 修复后重新 review。 |
| `major` | 可导致后续设计缺资产或重复资产 | 默认 rework；若证据不足但风险已记录，可 `pass_with_risks`。 |
| `minor` | 不影响清单真源但影响可读性 | 可随本轮修正或记录到报告。 |

## Provider Note

可使用 reviewer 或机械脚本辅助检查格式与来源完整性；任何 provider 输出都不得直接改写场景清单真源，必须由主执行者聚合裁决后落盘。
