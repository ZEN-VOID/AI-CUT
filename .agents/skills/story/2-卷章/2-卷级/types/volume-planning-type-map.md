# Volume Planning Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件用于先判型，再让 `steps/volume-planning-workflow.md` 消费 `type_profile`。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `operation` | `create` / `revise` / `audit` / `repair` | 本轮动作类型 |
| `scope` | `whole_volume` / `field_patch` / `structure_only` | 影响范围 |
| `upstream_state` | `available` / `missing` / `ambiguous` | `整体规划.md` 状态 |
| `output_state` | `absent` / `exists` / `invalid` | 目标 `卷规划.md` 状态 |

## Routing Matrix

| type_profile | trigger | route | required_reference | review_gate |
| --- | --- | --- | --- | --- |
| `create_volume_plan` | 目标卷无 `卷规划.md` | `N1 -> N2 -> N3 -> N4 -> N5 -> N6 -> N7` | `references/volume-planning-contract.md`、`references/volume-rhythm-framework.md` | full content review |
| `revise_volume_plan` | 用户要求补写或改写已有卷规划 | `N1 -> N2 -> N3R -> affected nodes -> N7` | 旧 `卷规划.md` 与相关 reference | patch review |
| `audit_volume_plan` | 用户只要求检查 | `N1 -> N2 -> N7` | `review/review-contract.md` | findings-only |
| `repair_structure` | 技能包结构漂移或 validator 失败 | `N2 -> structural repair -> validator` | `references/legacy-upgrade-matrix.md`、`scripts/README.md` | structure validator |

## Clarification Triggers

- `upstream_state=missing`：不得生成卷级规划。
- `operation=create` 但目标卷序号不明：必须追问或从 `整体规划.md` 中唯一推断。
- `operation=revise` 且用户要求“全部重写”：按 `whole_volume` 处理，但仍保留上游总纲约束。
- `operation=audit`：默认不落盘业务内容。
