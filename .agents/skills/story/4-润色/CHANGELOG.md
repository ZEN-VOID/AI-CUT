# Changelog

## 2026-06-10

- Collapsed the old A/B/C branch topology into a single root `story-polishing` skill package.
- Moved polishing execution to root-level runtime-spine semantics: source lock, context pack, repair plan, LLM-first polishing, quality gate, writeback, and state hook.
- Replaced legacy frontmatter with `修订阶段: 润色` plus `初稿来源` and `字数`; legacy `润色模型` is read-only compatibility metadata.
