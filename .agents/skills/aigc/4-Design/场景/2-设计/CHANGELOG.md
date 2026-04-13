# CHANGELOG.md

本文件承载 `.agents/skills/aigc/4-Design/场景/2-设计` 的结构性变更索引，不参与默认技能预加载，也不与 `SKILL.md / CONTEXT.md` 竞争真源。

## 2026-04-12

- `Case-20260412-AIGC-SCENE-DESIGN-SINGLE-SOURCE-ELEVATION`
  - 将 `2-设计` 从“父 skill + references + 外置场景设计组”重构为知行合一单技能真源。
  - 将 `设计统筹 / 空间逻辑 / 建筑设计师 / 布景师 / 审景师 / 真源审计` 六个能力面全部内联回 `SKILL.md`。
  - 将 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md` 的规范内容全部并入 `SKILL.md`。
  - 同步刷新 `CONTEXT.md`，把经验层改成“单技能真源”口径。
  - 同步刷新 `agents/openai.yaml`，移除 subagent / team 叙述。
  - 同步删除废弃载体：
    - `.agents/skills/aigc/4-Design/场景/2-设计/references/*`
    - `.codex/agents/aigc/设计组/场景设计/*`
  - 旧载体到新真源映射：
    - `references/chain-of-thought.md` -> `SKILL.md / Field Master / Thought Pass Map / Pass Table`
    - `references/execution-flow.md` -> `SKILL.md / Context Preload / Mandatory Workflow / Scene Design Card Assembly Rules`
    - `references/type-strategies.md` -> `SKILL.md / Type System / Convergence Contract`
    - `references/output-template.md` -> `SKILL.md / One-Shot Output Contract`
    - `.codex/agents/aigc/设计组/场景设计/*.md` -> `SKILL.md / Internal Capability Fusion Contract + Thinking-Action Node Network`
  - 证据路径：
    - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
    - `.agents/skills/aigc/4-Design/场景/2-设计/CONTEXT.md`
    - `.agents/skills/aigc/4-Design/场景/2-设计/agents/openai.yaml`
