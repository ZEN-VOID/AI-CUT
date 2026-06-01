# Type Map

## Package Index

| package | role |
| --- | --- |
| `visual-unit-type-map.md` | 判断画面句子、声画承托、高点画面、段落关系、逐画面点归属风险和非画面字段的分镜画面处理策略 |

## Default Package Rule

- 默认加载 `visual-unit-type-map.md`。
- 若输入含多类画面字段，先由该类型包形成 `visual_unit`、`type_profile`、`sequence_relation` 与 `ownership_risk`，再进入 `steps/cinematography-workflow.md`。
- 本索引只负责类型包发现，不替代 `SKILL.md` 的输入、输出、初始化综合消费或 review 合同。

## Loading Flow

```mermaid
flowchart TD
    A["调用 4-摄影"] --> B["加载 SKILL.md + CONTEXT.md"]
    B --> C["加载 types/type-map.md"]
    C --> D["加载 visual-unit-type-map.md"]
    D --> E["形成 visual_unit / type_profile"]
    E --> F["steps/cinematography-workflow.md"]
```
