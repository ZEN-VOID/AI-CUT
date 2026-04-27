# Entity Management Spec

对象真源最小合同。

## Shared Fields

- `core`: 长期稳定身份与不可轻易改写的基底。
- `current_state`: 当前默认生效状态。
- `history`: 已发生且可追溯的对象变化。
- `experience_timeline`: 角色经历轴；只用于角色，不泛化到所有对象。
- `core.growth_contract`: 角色长期成长合同；只用于角色，且默认只对主角强制启用。
- `current_state.growth_state`: 角色当前 validated 成长态；只用于角色。

## Hard Rules

- 不得用 `core` 冒充 `current_state`。
- 已 validated actual 的变化，才允许进入 `history` / `current_state`。
- query / drafting / validation 都必须承认 `Cards` 是对象真源。
- `growth_contract` 记录长期 ceiling、初始态与三轴设计；`growth_state` 只记录当前已经被 validation + 上下文回流 确认的阶段状态。
