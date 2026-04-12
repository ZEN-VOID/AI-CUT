# CHANGELOG.md

本文件记录 `aigc/4-Design/4-道具/2-设计` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-PROP-DESIGN-SUBA-BOOTSTRAP`
  - 新建 `2-设计` 父 skill、经验层、shared I/O、输出模板、执行流程与 `agents/openai.yaml`。
  - 新建 `.codex/agents/aigc/设计组/道具设计/` 的 team 与五角色合同，使 `2-设计` 采用 `skill-subagents` 父子治理结构。
  - 新建最小 runner，把 `1-清单` 的 bridge 收束为 `道具设计.json + prop_design_prompt.json + _manifest.json`。

- `Case-20260412-AIGC-PROP-DESIGN-PATH-NORMALIZATION`
  - 将用户输入中错位的 `projects/<项目名>/4-Design/2-角色/4-道具` 兼容口径统一收束到 `projects/<项目名>/4-Design/4-道具/2-设计/第N集/`。
  - 在父 skill、shared I/O 与 manifest 同步补写 path normalization 记录，避免错路径演化为第二真源。
