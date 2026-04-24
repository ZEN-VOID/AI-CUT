# Scene Processing Workflow

| node_id | input | action | output | gate |
| --- | --- | --- | --- | --- |
| `SCENE-N1-INTAKE` | 项目名、集数、`3-Detail` 或已有场景输入 | 锁定 runtime 与执行模式 | `scene_type_profile` | 输入可定位 |
| `SCENE-N2-LIST` | `3-Detail/第N集.json` | LLM 主导收束场景主体，脚本只做抽取/投影辅助 | `场景清单.md` | 主体是空间实体 |
| `SCENE-N3-DESIGN` | `场景清单.md` 与可选 JSON 侧车 | 使用 structured v2 场景模板生成 `[场景名].md` | N 份设计文档 | 模板校验通过 |
| `SCENE-N4-PANEL` | `[场景名].md` | 直引 prompt 生成 `[场景名].json` | N 份面板提示词 | JSON 回链同 stem Markdown |
| `SCENE-N5-REVIEW` | 本轮输出 | 执行 review gate 与路径检查 | verdict | 输出在 `4-Design/` 根 |
