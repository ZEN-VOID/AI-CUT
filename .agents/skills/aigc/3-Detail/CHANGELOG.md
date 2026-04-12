# CHANGELOG.md

本文件记录 `aigc/3-Detail` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-DETAIL-STAGE-BOOTSTRAP`
  - 新建 `3-Detail` 父 skill、经验层、shared I/O、`agents/openai.yaml` 与阶段变更记录。
  - 新建 `.codex/agents/aigc/制作组/team.md`，并把制作组 14 个既有占位角色补齐为可执行 agent contracts。
  - 自动补建 reviewer / auditor 角色：`复核审计/连续性复核.md` 与 `复核审计/真源审计.md`。
  - 同步修正与 `3-Detail` 直接相关的 shared carriers、council runtime 模板与 stage mapping，避免新阶段落地后周边仍指向空壳或旧路径。
