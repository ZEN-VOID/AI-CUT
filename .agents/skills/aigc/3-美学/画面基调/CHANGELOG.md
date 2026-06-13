# Changelog: aigc 3-美学/画面基调

## 2026-06-11

- 明确 `画面基调` 是项目级 `global_singleton`：单集来源只能作为样本范围或候选证据，正式 canonical output 仍写 `3-美学/画面基调/全局风格协议.md`。
- 同步 `SKILL.md`、`CONTEXT.md`、`README.md` 与 agent prompt，禁止创建 `3-美学/第N集/画面基调/` 作为正式真源。

## 2026-06-04

- 新建 `画面基调` Skill 2.0 core layout。
- 增加 runtime-spine `SKILL.md`，覆盖输入合同、类型路由、思行节点、模块授权、审查门、输出合同、注意力协议、检查点和学习回写。
- 增加 `CONTEXT.md`，沉淀风格污染、参考图误读、大师锚点和全局 prompt 蒸馏的可复用经验。
- 增加 `agents/openai.yaml`、`README.md` 和 `test-prompts.json`，用于入口索引、快速说明和回归验证。
