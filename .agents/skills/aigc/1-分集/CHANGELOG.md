# CHANGELOG

## 2026-06-04

- 将 `SKILL.md` 升级为 Skill 2.0 runtime-spine 主合同，补齐业务画像、类型路由、思行节点、模块加载、模块触发、量化口径、汇流合同、检查点、注意力协议和学习回写。
- 删除 `steps/episode-split-workflow.md` 的第二节点真源，并把 `references/`、`review/`、`types/` 中的返工目标同步回 `SKILL.md#T*` 主节点。
- 新增 `test-prompts.json`，覆盖 source scan、原生集标分集、章节型小说切分和 repair/review 回归场景。
- 更新 `README.md` 与 `CONTEXT.md`，明确模块只做授权展开，不维护平行执行链。

## 2026-04-25

- 初始化 `aigc/1-分集` Skill 2.0 包。
- 固定默认输入为 `projects/aigc/<项目名>/源/`，并允许用户指定其他小说原文资料。
- 固定“原资料自带集数划分优先；否则默认 2500-3000 字左右一集”的分集合同。
- 固定输出路径为 `projects/aigc/<项目名>/1-分集/第N集.md`。
- 同步登记 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml`，并调整 AIGC 审计脚本允许已恢复的 `1-分集` 叶子技能入口。
