# CHANGELOG

## 2026-06-04

- 按 `skill-2.0` runtime-spine 最新规范升级：在 `SKILL.md` 补齐业务画像、类型路由、主节点、分支规则、模块授权/触发矩阵、收敛合同、review gate binding、量化口径、注意力协议、检查点和评估 prompt 合同。
- 删除旧 workflow 第二执行链，将恢复业务画像、证据节点、分支规则和失败回路收束到 `SKILL.md`。
- 新增 `test-prompts.json` 与 canonical `review/review-contract.md` wrapper，兼容最新 validator / smoke test 的 core layout 与 review contract 检查。
- 同步 README、类型图、迁移矩阵、review gate、scripts README 与 CHANGELOG 中的旧 workflow 引用，并通过 delivery validator 与 smoke test。

## 2026-04-26

- 初始化 `.agents/skills/aigc/resume` Skill 2.0 包。
- 从 `.agents/skills/aigc-old/resume` 迁移续跑恢复卫星技能意图：断点重建、治理缺口识别、安全回接、rebootstrap 边界和 destructive 动作禁令。
- 将旧英文 runtime 口径调整为新版中文 runtime：`0-初始化 / 1-分集 / 2-编导 / 3-运动 / 4-摄影 / 10-分组 / 11-主体 / 12-图像 / 13-画布 / 14-审片`，并把 `4-设计` 标为 transition/compat 输入。
- 根据外部 reviewer provider 审计优化：恢复项目 `CONTEXT/` 加载合同、`11-主体` canonical 恢复口径、`blocked_safety_stop` 模式、`7-Cut` 搁浅语义与 `knowledge-base/` owner 边界。
- 新增 `references/`、`types/`、`review/`、`knowledge-base/`、`templates/`、`scripts/` 与 `agents/openai.yaml` 分区配置；执行节点真源收束在 `SKILL.md`。
