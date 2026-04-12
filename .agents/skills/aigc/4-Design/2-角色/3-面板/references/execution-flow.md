# Execution Flow

## Minimal Flow

1. 读取 `character_design.json`，锁定本轮 `selected_roles[]`。
2. 对每个命中角色读取 `structured_markdown_path`，优先抽 `**prompt整合**`。
3. 若 Markdown 缺失或不含 `prompt整合`，从 JSON 字段合成保守版 `design_subject`。
4. 加载 `templates/角色面板-提示词.json`，继承 layout、modules 与 critical requirements。
5. 组装每角色 layout packet，写回 `projects/<项目名>/4-Design/2-角色/3-面板/第N集/`。
6. 写 `_manifest.json`，记录输入、输出、统计与下游 handoff target。

## Writeback Policy

- 只更新命中角色 packet。
- 角色顺序以 `character_design.json.roles[]` 为准。
- 默认每角色一份 packet，不额外生成 episode 级平行总稿。
- `_manifest.json` 可覆盖更新，但不得吞掉未命中角色已有 packet。

## Rework Policy

- `prompt整合缺失`：先回到当前角色 Markdown；仍缺失时退到 JSON synthesis。
- `layout 漂移`：回到模板真源 `templates/角色面板-提示词.json`。
- `角色主体不完整`：回到 `2-设计` 补 `character_design.json` 或逐角色 Markdown。
- `群像误判`：回到 `references/type-strategies.md` 的 tier 策略重新判断。
