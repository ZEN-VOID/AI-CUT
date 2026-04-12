# CHANGELOG.md

本文件承载 `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画` 的结构性变更索引，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-12

- `Case-20260412-AIGC-STORYBOARD-COMIC-SINGLE-SOURCE-ELEVATION`
  - 将 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md` 的规范内容全部并入 `SKILL.md`，把 `漫画` 收敛为单一真源合同。
  - 同步补建 `agents/openai.yaml`，用于技能入口元数据。
  - 同步刷新 `CONTEXT.md`，把经验层与规范层重新压实分离。
  - 同步删除废弃 `references/` 文件载体。
  - 旧路径到新真源映射：
    - `references/chain-of-thought.md` -> `SKILL.md / Field Master / Thought Pass Map / Pass Table`
    - `references/execution-flow.md` -> `SKILL.md / Canonical Inputs / Canonical Landing / Mandatory Workflow / Prompt Assembly Rules`
    - `references/type-strategies.md` -> `SKILL.md / Type System`
    - `references/output-template.md` -> `SKILL.md / Handoff Contract / Synthesis Contract`
  - 同步修复的旧引用：
    - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/...` -> `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/...`
    - `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json` -> `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
  - 证据路径：
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/agents/openai.yaml`
