# Type Map

## Package Index

| package | role |
| --- | --- |
| `prop-design-type-map.md` | 判断道具主体粒度、冷门考据、多状态道具、规则道具和 prompt 处理策略 |

## Default Package Rule

- 默认加载 `prop-design-type-map.md`。
- 单道具与批量道具都先形成 `type_profile`，再进入 `steps/prop-design-workflow.md`。
- 本索引只负责类型包发现，不替代 `SKILL.md` 的输入、输出、team advisor consultation 或 review 合同。

## Loading Flow

```mermaid
flowchart TD
    A["调用 道具/2-设计"] --> B["加载 SKILL.md + CONTEXT.md"]
    B --> C["加载 types/type-map.md"]
    C --> D["加载 prop-design-type-map.md"]
    D --> E["形成 type_profile"]
    E --> F["steps/prop-design-workflow.md"]
```
