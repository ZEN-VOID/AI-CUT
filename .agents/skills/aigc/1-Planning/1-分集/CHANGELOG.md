# CHANGELOG.md

本文件记录 `aigc/1-Planning/1-分集` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-ZHI-XING-NETWORK`
  - 在不改变 `1-分集` 既有输入输出、`P1>P2>P3`、VSM、字段主表与 handoff 机制的前提下，将合同重排为知行合一单技能网络：补齐业务分析、拓扑合同、思行节点、汇流门、一-shot 输出与 Mermaid 可视真源。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CHANGELOG.md`

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-DIRECT-LEAF`
  - 将 `1-分集` 从“单分集 agent + skill 收束”收敛为 direct leaf skill，删除孤立 agent 文档，并同步父级规划合同、入口元数据与 audit。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-EXECUTION-BOUNDARY`
  - 早期曾将“agent 负责边界思考与 plan，skill 负责真正分集落盘、索引更新与 QA”的边界同步到 `1-分集` 的经验层与入口元数据；后续已继续收敛为 direct leaf skill。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-MIGRATION`
  - 参照 `AIGC-ZEN-VOID` 的 `1-故事分集`，补齐 `1-分集` 的 leaf skill 合同、经验层与模板，同时改写到 DREAMER 的 `projects/<项目名>/故事 + 1-Planning + 编导` runtime。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/templates/episode-split-plan.template.json`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-REPORT-COMPACTION`
  - 将 `1-分集` 的执行证据从逐集侧车收束为全剧集单报告，保留边界、coverage、source_profile 与 QA 闭环，但不再逐集落单独报告文件。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
