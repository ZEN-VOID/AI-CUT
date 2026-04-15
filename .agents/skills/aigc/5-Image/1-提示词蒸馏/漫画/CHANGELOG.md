# CHANGELOG.md

本文件承载 `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画` 的结构性变更索引，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-12

- `Case-20260412-AIGC-STORYBOARD-COMIC-ZHIXING-PLAYBOOK-REFRAME`
  - 在不改变 `漫画` 既有业务边界、prompt 合同、shared template 机制与 canonical landing 的前提下，将主合同改写为知行合一单技能网络。
  - 明确声明 `skeleton_detail_split: false`，本轮不把复杂链路细则拆到 `references/`。
  - 新增 `Business Requirement Analysis Contract`、`Shared Canonical Sources`、`Total Input Contract`、`Topology Contract`、`Thinking-Action Node Network`、逐节点 `Node Execution Playbook`、`Convergence Contract` 与 `One-Shot Output Contract`。
  - 将原先偏摘要式的 workflow 展开为 9 个思行节点，并给每个节点补齐“先看什么 / 必须锁定 / 执行动作 / 常见错误 / 完成信号 / 失败回退”六类细化执行面。
  - 同步补足 4 张 Mermaid 图，用于承载主干流程、分支回退、状态推进与字段关系。
  - 未新增 `references/`、`team.md`、子代理合同或第二套模板真源。
  - 证据路径：
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`

- `Case-20260412-AIGC-STORYBOARD-COMIC-SINGLE-SOURCE-ELEVATION`
  - 将旧 `references/` 规范模块的内容全部并入 `SKILL.md`，把 `漫画` 收敛为单一真源合同。
  - 同步补建 `agents/openai.yaml`，用于技能入口元数据。
  - 同步刷新 `CONTEXT.md`，把经验层与规范层重新压实分离。
  - 同步删除废弃 `references/` 文件载体。
  - 旧路径到新真源映射：
    - `references/chain-of-thought.md` -> `SKILL.md / Field Master / Thought Pass Map / Pass Table`
    - `references/execution-flow.md` -> `SKILL.md / Canonical Inputs / Canonical Landing / Mandatory Workflow / Prompt Assembly Rules`
    - `references/type-strategies.md` -> `SKILL.md / Type System`
    - legacy output contract reference -> `SKILL.md / Handoff Contract / Synthesis Contract`
  - 同步修复的旧引用：
    - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/...` -> `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/...`
    - `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json` -> `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
  - 证据路径：
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`
    - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/agents/openai.yaml`
