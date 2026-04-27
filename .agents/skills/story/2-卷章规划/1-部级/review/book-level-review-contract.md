# Book-Level Review Contract

本文件定义 `story-plan-book-level` 的质量门禁。review 只裁定部级规划是否可交给卷级，不改写业务主真源。

## Review Scope

| dimension | checks |
| --- | --- |
| input_trace | 是否能追溯到 `0-初始化`、类型卡和项目记忆 |
| output_shape | 是否包含全部必填标题 |
| volume_handoff | 卷划分是否给出每卷功能、阶段职责和交接方式 |
| task_topology | `整部任务关系` 是否写清主任务树、支流簇、汇聚里程碑 |
| conflict_axis | `整体冲突` 是否能下钻到卷级 |
| rhythm_curve | 是否采用长篇化 Save the Cat 15 步拍点走廊并包含 Mermaid 图 |
| avoidance | 规避是否是可执行禁飞区 |
| planning_boundary | 是否没有混入正文、对白或完整卡册复制 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交给 `2-卷级` |
| `pass_with_followups` | 可交付，但存在非阻断增强项 |
| `needs_rework` | 存在阻断缺口，必须返回对应字段节点 |
| `blocked` | 缺项目输入、项目根或上游真源 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: input_trace | output_shape | volume_handoff | task_topology | conflict_axis | rhythm_curve | avoidance | planning_boundary
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Review Flow

1. 检查 `整体规划.md` 是否存在于 `projects/story/<项目名>/2-卷章规划/整体规划.md`。
2. 检查必填标题和 `整体节奏曲线` 的 Mermaid 图。
3. 对 `卷划分 / 整部任务关系 / 整体冲突 / 整体节奏曲线 / 规避` 执行语义门禁。
4. 若发现阻断问题，按 `steps/book-level-planning-workflow.md` 返回对应节点修复。
5. review 结论必须汇总为一个 verdict，不允许多个 reviewer 并列改写规划真源。

## Gate Rule

不得在以下情况宣布部级完成：

- 缺少 `整部任务关系`。
- `卷划分` 只有卷名，没有阶段职责。
- `整体节奏曲线` 没有 Mermaid 图。
- Save the Cat 被写成死百分比公式，未转化为跨卷拍点走廊。
- `规避` 是口号而非可执行禁飞区。
- 输出混入小说正文或完整卡册复制。
