# CHANGELOG

## 2026-04-26

- 初始化 `.agents/skills/aigc/resume` Skill 2.0 包。
- 从 `.agents/skills/aigc-old/resume` 迁移续跑恢复卫星技能意图：断点重建、治理缺口识别、安全回接、rebootstrap 边界和 destructive 动作禁令。
- 将旧英文 runtime 口径调整为新版中文 runtime：`0-初始化 / 1-分集 / 2-编导 / 3-运动 / 4-摄影 / 5-分组 / 6-设计 / 7-图像 / 8-视频 / 9-审片`，并把 `4-设计` 标为 transition/compat 输入。
- 根据外部 reviewer provider 审计优化：恢复项目 `CONTEXT/` 加载合同、`6-设计` canonical 恢复口径、`blocked_safety_stop` 模式、`7-Cut` 搁浅语义与 `knowledge-base/` owner 边界。
- 新增 `references/`、`steps/`、`types/`、`review/`、`knowledge-base/`、`templates/`、`scripts/` 与 `agents/openai.yaml` 分区配置。
