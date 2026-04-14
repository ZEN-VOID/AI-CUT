# Execution Flow

## Minimal Flow

共享合同回指：

- 输入消费：`../../_shared/detail-output-consumption-contract.md`
- 对象归一：`../../_shared/object-normalization-contract.md`

1. 读取 `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json`。
2. 补证默认回看 `projects/aigc/<项目名>/3-Detail/第N集.json`，只有主路径缺失时才 fallback 到 legacy `projects/aigc/<项目名>/编导/第N集.json`。
3. 先确认 `角色清单.json` 已完成对象池收口，再按 `role_id + costume_state` 归一服装条目。
4. 写出 `服装清单.json`。
5. 基于同一批条目写出 `服装研究.json`。
6. 基于研究层继续写出 `costume_design_bridge.json`。

## Writeback Policy

- 只保留已有角色的服装事实，不新增角色。
- `costume_state` 缺失时保守回退为 `baseline`。
- 同一角色多套服装允许并列，但都必须有 evidence 回链。
- 导演句子残片不得反向生成新的 `role_id` 或 costume identity。
