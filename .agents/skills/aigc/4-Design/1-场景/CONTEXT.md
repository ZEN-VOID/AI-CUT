# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/1-场景` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 场景类目没有先做清单就直接进入设计 | 类目路由层 | 回退到 `1-清单` 先产出场景对象池 | 固化 `清单 -> 设计 -> 面板` 的默认顺序 | 下游能复用同一份场景清单 |
| 场景设计叶子技能缺父层边界 | 类目治理层 | 先补 `1-场景` 父级合同，再让 `2-设计` 成为场景设计入口 | 保持类目父级作为路由真源，叶子技能只承接局部执行 | `1-场景` 不再是空目录 |
| 场景链有设计 carrier，但没有面板收口入口 | 下游承接层 | 补齐 `3-面板` 叶子技能，让 `panel_handoff` 有实际接收方 | 在父级合同中把 `3-面板` 状态从 pending 提升为 active | `2-设计 -> 3-面板` 链路打通 |
| subagents 直接写最终设计稿 | 收束治理层 | 收回 canonical writeback 到 `2-设计` 父 skill | 在 team 合同中固定 `patch / note / report` | 设计组 agent 不再越权落盘 |

## Repair Playbook

1. 先查输入是否已有 `1-清单` 的 scene catalog。
2. 再查当前任务是否真的需要场景设计，而不是图片生成。
3. 若进入 `2-设计`，优先检查 team 合同和 parent writeback 是否完整。
4. 若进入 `3-面板`，优先检查 `场景设计.json -> 场景面板.json` 的 carrier handoff 是否闭环。

## Reusable Heuristics

- 场景链的第一真源不是设计稿，而是先由 `1-清单` 锁定的 scene catalog。
- 场景设计一旦引入 subagents，父 skill 的价值就不是“再多想一次”，而是统一收束和阻止越权写回。
- 当 `2-设计` 已经产出 `panel_handoff`，类目父级就不应继续把 `3-面板` 维持为 pending；否则下游字段会变成悬空合同。

## Case Log

### Case-20260412-AIGC-DESIGN-SCENE-PARENT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/1-场景` 建立了类目父级合同，并把 `2-设计` 升级为可执行入口。
- root_cause_or_design_decision: 先前目录里只有 `1-清单` 和空的 `2-设计 / 3-面板` 目录，没有场景类目父级，导致 `2-设计` 缺少稳定路由边界。
- final_fix_or_heuristic: 先建立类目级边界，再让 `1-清单` 作为对象池、`2-设计` 作为 subagent-governed 设计入口。
- prevention_or_replication_checklist:
  - [x] 类目父级合同已存在
  - [x] `1-清单 -> 2-设计 -> 3-面板` 顺序已显式化
  - [x] 场景设计 team 的 writeback 边界已回到父 skill
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/SKILL.md`
- user_feedback_or_constraint: 用户要求基于 `skill-subagents` 重构 `.agents/skills/aigc/4-Design/1-场景/2-设计`，并使用 `.codex/agents/aigc/设计组/场景设计` 作为 subagents 组。

### Case-20260412-AIGC-DESIGN-SCENE-PANEL-ACTIVATED

- milestone_type: source_contract_change
- outcome: 将 `1-场景/3-面板` 从空目录提升为 active leaf skill，并打通 `2-设计 -> 3-面板` 的 panel carrier handoff。
- root_cause_or_design_decision: `2-设计` 已经提供 `panel_handoff` 与 `final_scene_prompt`，但类目父级仍把 `3-面板` 标成 pending，导致下游合同悬空。
- final_fix_or_heuristic: 当上游叶子技能已经显式为某个下游阶段预留稳定 handoff 字段时，应尽快补齐下游叶子技能，避免 `SKILL.md` 中出现长期悬空的未来合同。
- prevention_or_replication_checklist:
  - [x] `3-面板` 已建立 `SKILL / CONTEXT / references / template / script`
  - [x] `1-场景/SKILL.md` 已把 `3-面板` 状态改为 active
  - [x] 本地经验层已记录这次收口 heuristic
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/scripts/generate_scene_panels.py`
  - `.agents/skills/aigc/4-Design/1-场景/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参照旧仓场景面板技能，完善当前仓的 `.agents/skills/aigc/4-Design/1-场景/3-面板`。
