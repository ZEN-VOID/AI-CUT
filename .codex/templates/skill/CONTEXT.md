# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.codex/templates/skill` 模板技能的经验层知识库，不是过程日志。
- 调用同目录 `SKILL.md` 或以该模板创建新技能时，必须同时加载本文件作为预加载上下文。
- 冲突优先级遵循：用户显式请求 > 仓库 `AGENTS.md` / 元规则 > 同目录 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对当前技能上下文做定向压缩与结构整理。
  - critical: 先归档旧案例，再继续大规模追加。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 新技能只有 `SKILL.md`，缺少经验层 | 模板基线层 | 在模板中明确同目录 `CONTEXT.md` 必须同步创建和加载 | 新技能脚手架默认生成 `SKILL.md + CONTEXT.md` 双载体 | 新建技能目录同时具备两个文件 |
| `CONTEXT.md` 被写成流水账 | 经验层治理层 | 改写为 Type Map / Repair Playbook / Reusable Heuristics | 模板说明中固定知识库模式，长过程外置到 `CHANGELOG.md` 或 `reports/` | 上下文文件不出现低价值进度日志 |

## Repair Playbook

1. 创建或更新技能模板时，先确认同目录 `SKILL.md` 与 `CONTEXT.md` 是否同时存在。
2. `SKILL.md` 只放触发、流程、输出与质量门槛；`CONTEXT.md` 只放经验型知识库。
3. 若模板字段变化会影响审计脚本或注册流程，同轮检查相关脚本和 registry 说明。
4. 结束前用 `find` 或 `rg --files` 检查新技能目录是否缺少双载体之一。

## Reusable Heuristics

- 新技能模板必须从一开始就把规范合同和经验层分开，否则后续很容易把 `SKILL.md` 写成经验备忘录。
- 模板里的加载合同要短、强制、可复制，避免每个技能自行发明不同说法。
