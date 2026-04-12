# CHANGELOG.md

本文件承载 `aigc/6-Video/1-提示词蒸馏/全能参照` 的结构性迁移记录，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-12

- `Case-20260412-AIGC-VIDEO-SUBJECT-SINGLE-SOURCE-CONTRACT`
  - 将 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/output-template.md`、`references/type-strategies.md` 全量回收到 `SKILL.md`，把 `SKILL.md` 升格为子技能唯一规范真源。
  - 同步补建 `agents/openai.yaml` 与 `CHANGELOG.md`，并把经验层引用改到 `SKILL.md` / shared templates。
  - 将旧写法 `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/` 统一收敛为当前 canonical 路径 `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/`。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`
