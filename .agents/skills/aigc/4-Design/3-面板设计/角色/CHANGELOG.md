# CHANGELOG.md

本文件记录 `aigc/4-Design/角色/3-面板` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-ROLE-PANEL-BOOTSTRAP`
  - 新建 `3-面板` 的 `SKILL.md`、`CONTEXT.md`、`CHANGELOG.md` 与 `agents/openai.yaml`。
  - 新建 `_shared/IO_CONTRACT.md`、`references/`、`templates/角色面板-提示词.json` 与最小 runner。
  - 将参考仓的角色面板模板与 prompt 提取逻辑迁移到当前仓 `2-设计 -> 3-面板` 的 runtime 与输出口径。

- `Case-20260412-AIGC-ROLE-PANEL-ROUTE-SYNC`
  - 同步更新 `2-角色` 与 `4-Design` 父级合同，将 `3-面板` 状态从 pending 收束为 active。
  - 修正父级经验层中的 stale route 叙述，避免叶子已落地但父级仍保留旧状态。
