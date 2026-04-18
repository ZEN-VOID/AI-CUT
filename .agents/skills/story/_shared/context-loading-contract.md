# Context Loading Contract

跨阶段共享的上下文加载合同。

## Canonical Rules

- `story` 体系不再依赖根级 `references/` 目录。
- 跨阶段共享合同优先落在根级 `_shared/`。
- 阶段专属共享合同优先落在各阶段自己的 `_shared/`。
- `SKILL.md + CONTEXT.md` 仍是每个阶段的默认入口；`_shared/*.md` 只承载跨阶段复用的稳定合同。

## Loading Order

1. 根 `AGENTS.md`
2. 根 `story/SKILL.md + CONTEXT.md`
3. 当前阶段 `SKILL.md + CONTEXT.md`
4. 命中的根级 `_shared/` 合同
5. 命中的阶段 `_shared/` 合同
6. 当前阶段私有 `references/` / `templates/` / `scripts/`

## Hard Gates

- 不得把阶段私有 `references/` 冒充成跨阶段共享真源。
- 若某 shared contract 被 2 个以上阶段复用，应优先提升到 `_shared/` 而不是复制到兄弟目录。
- legacy `story2026` 路径只允许作为兼容 fallback，不再是 canonical source。
