# Prop Processing Workflow

| node_id | input | action | output | gate |
| --- | --- | --- | --- | --- |
| `PROP-N1-INTAKE` | 项目名、集数、`3-Detail` 或已有道具输入 | 锁定 runtime 与执行模式 | `prop_type_profile` | 输入可定位 |
| `PROP-N2-LIST` | `3-Detail/第N集.json` | LLM 主导收束道具主体，脚本只做抽取/投影辅助 | `道具清单.md` | 主体是物件实体 |
| `PROP-N3-DESIGN` | `道具清单.md` 与可选 JSON 侧车 | 使用 structured v2 道具模板生成 `[道具名].md` | N 份设计文档 | 模板结构稳定 |
| `PROP-N4-PANEL` | `[道具名].md` | 直引 prompt 生成 `[道具名].json` | N 份面板提示词 | JSON 回链同 stem Markdown |
| `PROP-N5-REVIEW` | 本轮输出 | 执行 review gate 与路径检查 | verdict | 输出在 `5-设计/` 根 |
