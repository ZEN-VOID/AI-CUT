# CHANGELOG.md

本文件记录 `aigc/5-Image/1-提示词蒸馏/分镜帧` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-STORYBOARD-FRAME-INLINE-SKILL-CONTRACT`
  - 将原 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md` 的规范内容全部并入 `SKILL.md`，收束为单一规范真源。
  - 补建 `agents/openai.yaml`，为该叶子技能提供稳定的 interface metadata。
  - 补建本 `CHANGELOG.md`，为后续回溯提供结构变更索引。
  - 删除 `references/` 载体，并同步回扫旧 `references` 引用与 `5-画面/subtypes/...` 旧路径口径。

- `Case-20260412-AIGC-STORYBOARD-FRAME-THINKING-ACTION-REORCHESTRATION`
  - 在不改变业务输出机制的前提下，将 `分镜帧` 从线性叶子合同重排为知行合一式单文件真源。
  - 新增 `Total Input Contract`、`Internal Capability Fusion Contract`、`Topology Contract`、`Thinking-Action Node Network`、`Convergence And Audit Contract` 与 `One-Shot Output Contract`。
  - 为每个节点补齐“从哪些方面着手 / 一步一步怎么做 / 未达标信号”，并增加 3 张 Mermaid 图承载主流程、分支和状态关系。
  - 显式固定 `复杂链路的骨架 / 细则分层 = false`，避免未来再次回退到 `references/` 分层。
