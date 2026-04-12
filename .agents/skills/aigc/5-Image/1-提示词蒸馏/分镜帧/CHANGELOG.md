# CHANGELOG.md

本文件记录 `aigc/5-Image/1-提示词蒸馏/分镜帧` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-STORYBOARD-FRAME-INLINE-SKILL-CONTRACT`
  - 将原 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md` 的规范内容全部并入 `SKILL.md`，收束为单一规范真源。
  - 补建 `agents/openai.yaml`，为该叶子技能提供稳定的 interface metadata。
  - 补建本 `CHANGELOG.md`，为后续回溯提供结构变更索引。
  - 删除 `references/` 载体，并同步回扫旧 `references` 引用与 `5-画面/subtypes/...` 旧路径口径。
