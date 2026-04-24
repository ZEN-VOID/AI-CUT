# Role Processing Workflow

| node_id | input | action | output | gate |
| --- | --- | --- | --- | --- |
| `ROLE-N1-INTAKE` | 项目名、集数、`3-Detail` 或已有角色输入 | 锁定 runtime 与执行模式 | `role_type_profile` | 输入可定位 |
| `ROLE-N2-LIST` | `3-Detail/第N集.json` | LLM 主导收束角色主体，脚本只做抽取/投影辅助 | `角色清单.md` | 身份和服装锚稳定 |
| `ROLE-N3-DESIGN` | `角色清单.md` 与可选 JSON 侧车 | 使用 structured v2 角色模板生成 `[角色名].md` | N 份设计文档 | 模板校验通过 |
| `ROLE-N4-PANEL` | `[角色名].md` | 直引 prompt 生成 `[角色名].json` | N 份面板提示词 | JSON 回链同 stem Markdown |
| `ROLE-N5-REVIEW` | 本轮输出 | 执行 review gate 与路径检查 | verdict | 输出在 `4-Design/` 根 |
