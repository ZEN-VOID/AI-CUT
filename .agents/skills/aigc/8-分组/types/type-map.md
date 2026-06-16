# Type Map

本文件是 `8-分组` 的 types 索引。它只负责把输入状态路由到已授权类型包，不替代 `SKILL.md` 的 `Type Routing Matrix`。

## Package Index

| package | load_when | purpose | return_to |
| --- | --- | --- | --- |
| `types/grouping-type-map.md` | 任意生成、source override、direct screenplay、repair 或 review | 固定 source_state、duration_signal、style_payload、continuity_risk 与 repair_need 画像 | `N1-INTAKE` / `N2-SOURCE-INVENTORY` |

## Default Package Rule

- 默认加载 `types/grouping-type-map.md`，用于识别 `complete_camera`、`partial_camera`、`direct_screenplay`、`legacy_grouped`、`broken_markup` 等输入状态。
- 类型包只提供判型上下文；不得新增输出路径、完成门、fail code 真源或第二执行链。

## Loading Flow

1. `N1-INTAKE` 先锁定 source、episode scope 和写回模式。
2. 加载 `types/grouping-type-map.md` 形成 `type_profile`。
3. `type_profile` 回流到 `Type Routing Matrix` 与 `Thinking-Action Node Map`，由 `SKILL.md` 裁决后续节点。
