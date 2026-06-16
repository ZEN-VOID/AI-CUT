# CHANGELOG

## 2026-06-11

- 同步 `2-美学` 输出 scope：表演阶段读取 `画面基调` 全局 singleton；角色风格和场景风格按当前 `第N集` 优先读取 `2-美学/第N集/<风格>/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`README.md` 与 agent prompt，执行报告需记录风格来源与 fallback。

## 2026-06-10

- 新增 `references/action-choreography-contract.md`，将武侠、动作、玄幻、格斗、追逐、兵器、术法对抗等打戏题材路由到动作戏编排细则。
- 新增 `GATE-PERF-22-ACTION-CHOREOGRAPHY` 与 `FAIL-PERF-ACTION-CHOREOGRAPHY`，要求打戏动作包含过程、路径、方式、力度、伴随反应和身体残留，而不是只写演技或结果。
- 同步 `CONTEXT.md`、`README.md` 与 `test-prompts.json`，加入打戏动作设计失败模式和回归 prompt。
- 接入 `../_shared/upstream-context-application-contract.md`，要求表演稿证明 `5-导演` 批注意图和 `2-美学` 三类协议如何融合为同字段表演正文。
- 新增 `FAIL-PERF-UPSTREAM-CONTEXT`、`GATE-PERF-21-UPSTREAM-CONTEXT` 和报告 `Upstream Context Application Map`；当前完成门扩展到 `GATE-PERF-01..22`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-04

- 初始化 `aigc/5-表演` Skill 2.0 runtime-spine 包。
- 建立 `SKILL.md + CONTEXT.md`、`README.md`、`agents/openai.yaml`、`test-prompts.json` 和 `knowledge-base/actor-style-index.md`。
- 从 `2-编导/references/` 接入表演相关细则，包含斯坦尼斯拉夫斯基方法、演员表演控制、角色弧线表演、受控增强、对白潜台词、群戏表演、场景工艺、表演风格、生理真实、心理反应和声音设计。
- 固化核心输出口径：默认消费 `5-导演` 导演批注稿和 `2-美学` 的画面基调、角色风格、场景风格；保留原字段标题，删除导演批注，将批注意图融合为画面化表演正文。
