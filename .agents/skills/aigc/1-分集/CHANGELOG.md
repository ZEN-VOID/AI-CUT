# CHANGELOG

## 2026-04-25

- 初始化 `aigc/1-分集` Skill 2.0 包。
- 固定默认输入为 `projects/aigc/<项目名>/源/`，并允许用户指定其他小说原文资料。
- 固定“原资料自带集数划分优先；否则默认 2500-3000 字左右一集”的分集合同。
- 固定输出路径为 `projects/aigc/<项目名>/1-分集/第N集.md`。
- 同步登记 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml`，并调整 AIGC 审计脚本允许已恢复的 `1-分集` 叶子技能入口。
