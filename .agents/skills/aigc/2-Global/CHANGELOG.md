# CHANGELOG.md

本文件记录 `aigc/2-Global` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-GLOBAL-STAGE-BOOTSTRAP`
  - 新建 `2-Global` 父 skill、经验层、shared I/O、三份输出模板与 `agents/openai.yaml`。
  - 新建 `.codex/agents/aigc/导演组/` 的 team 与三角色合同，使 `2-Global` 采用 `skill-subagents` 的父子治理结构。
  - 同步把仓内显式旧路径 `.agents/skills/aigc/2-组间/*` 切换到 `.agents/skills/aigc/2-Global/*`。

- `Case-20260412-AIGC-GLOBAL-SUBAGENT-CONTRACT-REPAIR`
  - 清理 `SKILL.md / CONTEXT.md / CHANGELOG.md / agents/openai.yaml` 中残留的“导演组标准 / 导演组/标准”旧路径与旧口径。
  - 在 `2-Global` 父 skill 与导演组 team 明确：无论有序还是无序，默认都走后台 subagents，由父 skill 汇总写回。
  - 扩展 `scripts/aigc_skill_audit.py`，把 `规划组 / 导演组 / 制作组` 的 team/agent 存在性与引用断链纳入严格审计。

- `Case-20260412-AIGC-GLOBAL-CREATIVE-METHOD-UPGRADE`
  - 新建 `.codex/agents/aigc/导演组/_shared/CREATIVE_METHOD.md`，把导演组的证据梯度、决策顺序、质量门禁与低证据退化规则收口成共享方法真源。
  - 在 `2-Global` 父 skill、导演组 team 与三角色合同中显式回指该共享方法真源，避免角色文档只剩边界合同。
  - 为三份 `2-Global` 模板补上候选取舍与质量槽位，减少“结构有了但内容空泛”的风险。
