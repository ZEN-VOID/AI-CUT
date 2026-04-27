# Context Loading Contract

跨阶段共享的上下文加载合同。

## Canonical Rules

- `story` 体系不再依赖根级 `references/` 目录。
- 跨阶段共享合同优先落在根级 `_shared/`。
- 阶段专属共享合同优先落在各阶段自己的 `_shared/`。
- `SKILL.md + CONTEXT.md + 选中的 types/ 类型包` 是每个阶段的默认入口；`_shared/*.md` 只承载跨阶段复用的稳定合同。

## Loading Order

1. 根 `AGENTS.md`
2. 根 `story/SKILL.md + CONTEXT.md`
3. 识别并加载根 `types/` 中选中的类型包（单选或多选）
4. 当前阶段 `SKILL.md + CONTEXT.md`
5. 识别并加载当前阶段 `types/` 中选中的类型包（单选或多选）
6. 命中的根级 `_shared/` 合同
7. 命中的阶段 `_shared/` 合同
8. 当前阶段私有 `references/` / `templates/` / `scripts/`

## Hard Gates

- 不得把阶段私有 `references/` 冒充成跨阶段共享真源。
- 不得把 `knowledge-base/` 当作每次固定加载的类型包；题材、阶段、任务模式等固定上下文必须落在 `types/` 并由 `type-map` 或 route profile 选择。
- 若某 shared contract 被 2 个以上阶段复用，应优先提升到 `_shared/` 而不是复制到兄弟目录。
- legacy `story2026` 路径只允许作为兼容 fallback，不再是 canonical source。
