# Changelog: aigc 2-美学/摄影风格

## 2026-06-15

- 修订摄影 8 维：将 `机位高度` 扩展为 `机位关系/视角距离`，新增 `透视/景深纪律` 与 `焦点行为`，并合并节奏/速度密度。
- 同步 prompt 蒸馏、grammar gate、field master 和 context heuristics，使摄影协议覆盖焦点、景深、透视与稳定性。
- 同步 `CONTEXT.md` 的焦点/景深缺失失败模式和约 100 字 prompt 稳定结构。

## 2026-06-11

- 增加逐集输出 scope：单集来源或目标写入 `2-美学/第N集/摄影风格/摄影风格协议.md` 和同目录 `执行报告.md`；整季/项目基线保留项目级路径。
- 同步 `SKILL.md`、`CONTEXT.md`、`README.md` 与 agent prompt 的 review/repair 输入和输出路径说明。

## 2026-06-04

- 新建 `摄影风格` Skill 2.0 core layout。
- 增加 runtime-spine `SKILL.md`，覆盖输入合同、类型路由、思行节点、视觉拓扑、模块授权、审查门、输出合同、注意力协议、检查点和学习回写。
- 增加 `CONTEXT.md`，沉淀摄影层污染、参考视频误读、运动连招、连续性和约 100 字摄影 prompt 蒸馏的可复用经验。
- 增加 `agents/openai.yaml`、`README.md` 和 `test-prompts.json`，用于入口索引、快速说明和回归验证。
