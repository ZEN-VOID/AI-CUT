# CHANGELOG.md

本文件记录 `aigc/4-Design/2-角色/2-设计` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-ROLE-DESIGN-SKILL-BOOTSTRAP`
  - 新建 `2-设计` 父 skill、经验层、shared I/O、模板参考与 `agents/openai.yaml`。
  - 新建 `.codex/agents/aigc/设计组/角色设计/team.md`，并把 `设计统筹 / 形象建模 / 服装设计 / 妆容设计 / 个性塑造 / 角色一致性复核 / 真源审计` 落为正式 agent contracts。
  - 将 `2-设计` 的 canonical 输出锁定为 `character_design.json + 逐角色 Markdown + _manifest.json`。

- `Case-20260412-AIGC-ROLE-DESIGN-PARENT-STATUS-SYNC`
  - 将 `.agents/skills/aigc/4-Design/SKILL.md` 与 `.agents/skills/aigc/4-Design/2-角色/SKILL.md` 中的 `2-设计` 状态从 `pending` 同步为 `active`。
  - 为 `.agents/skills/aigc/4-Design/CONTEXT.md` 与 `.agents/skills/aigc/4-Design/2-角色/CONTEXT.md` 补充本轮设计技能激活记录。
