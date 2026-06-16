# Changelog: aigc 2-美学/角色风格

## 2026-06-15

- 修订角色 8 维：补入 `形象轮廓/比例`、`群体分层`、`妆发/表面纪律`、`服装/外观结构`、`年龄/生命阶段质感` 和 `变体与一致性边界`。
- 降低旧维度对真人妆发定装的依赖，增强非人、怪物、动画化和群像角色的适配能力。
- 同步 `CONTEXT.md` 的维度泛化失败模式、非真人转译策略和 prompt 稳定结构。

## 2026-06-11

- 增加逐集输出 scope：单集来源或目标写入 `2-美学/第N集/角色风格/角色风格协议.md` 和同目录 `执行报告.md`；整季/项目基线保留项目级路径。
- 同步 `SKILL.md`、`CONTEXT.md`、`README.md` 与 agent prompt 的 review/repair 输入和输出路径说明。

## 2026-06-04

- 创建 Skill 2.0 runtime-spine core layout。
- 新增 `SKILL.md`，定义角色层视觉风格协议、输入路由、执行节点、审查门、输出合同、注意力协议、检查点和经验回写规则。
- 新增 `CONTEXT.md`，沉淀角色卡化污染、参考人物复制、维度缺失和 prompt 收束修复经验。
- 新增 `README.md`、`agents/openai.yaml` 和 `test-prompts.json`。
