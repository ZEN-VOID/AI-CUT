# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `色彩设计` 的经验层知识库，不是执行日志。
- 调用 `色彩设计/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父级 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有冷暖形容词，没有主色系统 | 结构层 | 回补主色系统与显色载体 | 在 SKILL 固定“主色实体”门禁 | 能说明主色落在哪 |
| 色彩很满，但没有主辅色张力 | 关系层 | 回补辅色对位与破色刺点 | 在字段主表固定对位关系 | 不再一片平色 |
| 色彩与光影互相打架 | 协同层 | 回读 `[摄影美学].光影` 再重写色彩 | 在工作流里强制先读光影段 | 显色条件与色彩成立 |
| 色彩句子脱离可见载体 | 表达层 | 把抽象术语改写为载体化描述 | 在 leaf 合同里固定可见载体约束 | 颜色能被镜头看到 |
| 为了色彩冲击越界改写光源或参数 | 边界层 | 回滚越界改动，只保留色彩判断 | 只写 `[摄影美学].色彩` | 色彩段不再替代其他段 |

## Repair Playbook

1. 先问主色落在何物。
2. 再问哪一抹辅色或破色制造冲突。
3. 再问冷暖、明暗和饱和节奏如何一起服务情绪。
4. 最后确认有没有越界改光影或参数。

## Reusable Heuristics

- 色彩设计最怕“只有色名，没有载体”。
- 若冷暖关系说不清，多半是主色系统还没真正锁定。
- 真正有效的跳色必须绑定节拍或叙事作用，不然只是噪点。
- 光影是显色条件，色彩是情绪统摄，二者不能互相替代。

## Case Log

### Case-20260409-AIGC-SCRIPT-COLOR-DESIGN-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `色彩设计` 建立了适配当前 `3-明细` 终稿模式的 leaf 合同与经验层。
- root_cause_or_design_decision: 用户要求 `5-摄影美学` 包含色彩能力；直接技术缺口是当前仓没有任何“把导演级色彩统摄落回脚本终稿”的稳定 leaf。
- final_fix_or_heuristic: 吸收旧仓 `7-色彩美学` 的高价值判断维度，但把输出载体改写为共享终稿中的 `[摄影美学].色彩` 段。
- prevention_or_replication_checklist:
  - [x] 已固定共享终稿落点
  - [x] 已建立主色/辅色/冷暖/饱和明度门禁
  - [x] 已限制只写 `[摄影美学].色彩`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/色彩设计/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/色彩设计/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/7-色彩美学/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `5-摄影美学` 应覆盖色彩能力，并服务当前仓的“共享终稿逐层发酵”模式。
