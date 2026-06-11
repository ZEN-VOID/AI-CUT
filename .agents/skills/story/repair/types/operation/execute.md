# Operation Package: Execute

## Selection Signals

- 用户明确要求“执行修改 / 改掉 / 同步修 / 写回 / 修复完成”。

## Fixed Context

- 写回必须遵循 source-first order。
- 创作性正文修复必须回到 owning stage 根技能。
- 对用户指定的目标文档，若文档头部含 legacy `写作模型` / `润色模型`，只作为历史执行环境线索读取，不作为修复路由依据。
- 破坏性覆盖已验收终稿前必须确认 acceptance/return gate 处理方式。

## Review Gate

- 列出 changed files。
- 旧口径残留已被审计。
- 指定文档的 legacy 模型字段没有被当作路由真源；报告记录了 owning stage 与执行环境说明。
- 状态 hook 已执行或有明确阻断说明。
