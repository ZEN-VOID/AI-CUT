# CHANGELOG

## 2026-04-12 - scene-design subagent upgrade

### 新增

- 新建 `.agents/skills/aigc/4-Design/1-场景/2-设计/SKILL.md`
- 新建 `.agents/skills/aigc/4-Design/1-场景/2-设计/CONTEXT.md`
- 新建 `.agents/skills/aigc/4-Design/1-场景/2-设计/agents/openai.yaml`
- 新建 `.agents/skills/aigc/4-Design/1-场景/2-设计/references/{chain-of-thought,execution-flow,type-strategies,output-template}.md`
- 新建 `.agents/skills/aigc/4-Design/1-场景/2-设计/templates/scene-design-card.md`
- 新建 `.codex/agents/aigc/设计组/场景设计/team.md`
- 新建 `.codex/agents/aigc/设计组/场景设计/{设计统筹,审景师,真源审计}.md`

### 修改

- 补齐 `.codex/agents/aigc/设计组/场景设计/{空间逻辑,建筑设计师,布景师}.md` 的稳定角色合同

### 关键迁移映射

- 旧状态：`1-场景/2-设计/` 仅为空目录，场景设计组 agent 文档为空
- 新状态：`2-设计` 作为 canonical scene design skill，场景设计组仅返回 `agents_plan + patch / note / report`

### Harness / Handoff 同步

- `1-清单 -> 2-设计` 的 handoff 关系已在新技能合同中显式化
- `team.md` 已明确 canonical writeback owner 为父 skill
- 默认 mixed tranche + 后台 subagents 模式已显式写入 team 与 skill
