# Execution Flow

## Minimal Flow

1. 读取 `2-角色/1-清单/第N集/角色清单.json`。
2. 兼容回看 `3-Detail/第N集.json` 或 `3-Detail/第N集.json` 的镜头证据。
3. 按 `role_id + costume_state` 归一服装条目。
4. 写出 `服装清单.json`。
5. 基于同一批条目写出 `服装研究.json`。
6. 基于研究层继续写出 `costume_design_bridge.json`。

## Writeback Policy

- 只保留已有角色的服装事实，不新增角色。
- `costume_state` 缺失时保守回退为 `baseline`。
- 同一角色多套服装允许并列，但都必须有 evidence 回链。
