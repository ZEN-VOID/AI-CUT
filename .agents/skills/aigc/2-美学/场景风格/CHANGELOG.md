# Changelog: aigc 2-美学/场景风格

## 2026-06-15

- 修订场景九维：从具体 `烟雾 / 自然元素 / 科技元素` 转为 `空间尺度/秩序`、`氛围介质/粒子层`、`生态系统组织`、`人工/科技系统组织` 等更稳定的场景层属性。
- 修正父级整体调用下的并发语义：缺失 `画面基调` 时标记 `candidate/dependency_gap`，不得把父级 fan-out 降级为串行链。
- 同步 `CONTEXT.md` 的九维缺项、prompt 稳定结构和场景元素泛化 heuristics。

## 2026-06-11

- 增加逐集输出 scope：单集来源或目标写入 `2-美学/第N集/场景风格/场景风格协议.md` 和同目录 `执行报告.md`；整季/项目基线保留项目级路径。
- 同步 `SKILL.md`、`CONTEXT.md`、`README.md` 与 agent prompt 的 review/repair 输入和输出路径说明。

## 2026-06-04

- 新建 `场景风格` Skill 2.0 core layout。
- 增加 runtime-spine `SKILL.md`，覆盖输入合同、类型路由、思行节点、视觉图、模块授权、审查门、输出合同、注意力协议、检查点和学习回写。
- 增加 `CONTEXT.md`，沉淀地点清单污染、画面基调继承、参考环境误读和约 100 字场景风格 prompt 的可复用经验。
- 增加 `agents/openai.yaml`、`README.md` 和 `test-prompts.json`，用于入口索引、快速说明和回归验证。
