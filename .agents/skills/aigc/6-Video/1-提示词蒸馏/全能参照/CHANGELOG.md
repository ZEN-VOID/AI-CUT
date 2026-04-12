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

- `Case-20260412-AIGC-VIDEO-SUBJECT-ZXY-REFACTOR`
  - 在不改变现有输入、输出、模板、字段、字数窗与禁止项的前提下，将 `全能参照` 重写为知行合一式单技能思行网络。
  - 新增 `业务需求分析合同 / 总输入合同 / 拓扑合同 / N0-N8 思行节点 / 汇流门 / 一次性输出门`，并显式声明 `复杂链路的骨架 / 细则分层: false`。
  - 新增执行闭环要求：最终结案除三件套外，必须包含 `思考过程 + 关键证据 + 风险/例外`。
  - 同步刷新 `CONTEXT.md` 的 Type Map、Heuristics 与案例记录，并更新 `agents/openai.yaml` 的入口描述。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`
