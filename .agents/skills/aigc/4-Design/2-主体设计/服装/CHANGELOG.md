# CHANGELOG.md

本文件记录 `aigc/4-Design/服装/2-设计` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-COSTUME-DESIGN-SKILL-BOOTSTRAP`
  - 新建 `2-设计` 父 skill、经验层、shared I/O、模板参考与 `agents/openai.yaml`。
  - 新建 `.codex/agents/aigc/设计组/服装设计/team.md`，并把 `服装统筹 / 廓形层次设计师 / 材质纹样设计师 / 配饰连续性设计师 / 提示词架构师 / 服装一致性复核 / 真源审计` 落为正式 agent contracts。
  - 将 `2-设计` 的 canonical 输出锁定为 `服装设计.json + 逐服装 Markdown + costume_design_prompt.json + _manifest.json`。
