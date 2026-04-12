# Type Strategies

## Costume State Strategy

| 情况 | 默认处理 | 说明 |
| --- | --- | --- |
| 明确写出状态变化 | 保留显式 `costume_state` | 如 `战损 / 仪式 / 夜行` |
| 只有一套常驻服装 | 回退 `baseline` | 作为该角色当前集主状态 |
| 同一镜头同时提到内外层 | 合并为一个 costume entry 的 `layer_system` 线索 | 不拆成两件独立服装 |
| 证据明显不足 | 保守记为 `unspecified-state` 并写入 notes | 不擅自发明状态名 |

## Tie-Break Rules

1. `角色清单.json` 的 `role_id / canonical_name` 优先。
2. `3-Detail/第N集.json` 的镜头证据高于研究层推测。
3. 若状态名不稳定，优先保守归到 `baseline`，并在 bridge 中说明。
