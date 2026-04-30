# Operation Package: Execute

## Selection Signals

- 用户明确要求“执行修改 / 改掉 / 同步修 / 写回 / 修复完成”。

## Fixed Context

- 写回必须遵循 source-first order。
- 创作性正文修复必须回到 owning stage 和原 provider lane。
- 对用户指定的目标文档，若文档头部含 `写作模型`，默认按该模型对应 lane 执行内容调整；用户显式要求切换模型时，必须同步改写模型标记与证据链。
- 破坏性覆盖已验收终稿前必须确认 review/return gate 处理方式。

## Review Gate

- 列出 changed files。
- 旧口径残留已被审计。
- 指定文档的 `写作模型`、实际 creative engine 与 provider evidence 一致。
- 状态 hook 已执行或有明确阻断说明。
