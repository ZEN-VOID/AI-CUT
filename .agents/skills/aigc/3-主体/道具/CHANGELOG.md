# Changelog: aigc 3-主体/道具

## 2026-06-16

- 将组根 `SKILL.md` 升级为 runtime-spine Skill 2.0 router，补齐 Core Task、Business Requirement Analysis、Type Routing、Thinking-Action Node Map、Module Loading/Trigger、Convergence、Review Gate、Quantifiable Criteria、Attention、Checkpoint、Output 和 Learning 控制块。
- 新增 `README.md`、`agents/openai.yaml` 与 `test-prompts.json`，补齐组根 core layout。
- 明确 `SKILL.md` runtime spine 在叶子目录内仅作为 legacy read-only reference，运行时节点真源收回各自 `SKILL.md`。
- 强化组根 LLM-first 边界：组根只路由与验收，不直接生成清单正文、道具设计、JSON prompt 或图像资产。
