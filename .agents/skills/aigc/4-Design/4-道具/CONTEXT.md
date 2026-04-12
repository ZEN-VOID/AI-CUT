# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/4-道具` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 道具链只有 `1-清单`，没有设计 synthesis | 类目路由层 | 建立 `4-道具/SKILL.md` 与 `2-设计` 父 skill | 把 `清单 -> 设计 -> 面板` 固定为父级顺序 | 用户可从 bridge 稳定进入设计 |
| 道具设计把 prompt 当成唯一真源 | 输出治理层 | 区分 `道具设计.json` 与 `prop_design_prompt.json` | 将 canonical facts 与执行话术分层 | 下游能复用设计真值，不依赖单次 prompt |
| subagents 角色存在但 team 层为空 | agent team 层 | 补齐 `.codex/agents/aigc/设计组/道具设计/team.md` 与角色合同 | 让父 skill 永远回指真实 team，而不是口头想象 | team 路径存在且可被 audit 检出 |
| 道具链停在 `2-设计`，没有 panel handoff | 类目路由层 | 建立 `3-面板` 叶子技能，消费 design master 输出逐道具 layout | 把 `清单 -> 设计 -> 面板` 真正闭环，而不是只在父级写顺序 | 用户可从 `道具设计.json` 稳定进入 panel layout |

## Repair Playbook

1. 先看当前任务是对象池、设计 synthesis 还是展示面板。
2. 若还没有 `prop_design_bridge.json`，先回到 `1-清单`。
3. 若 bridge 已有、目标是设计稿或 prompt sidecar，进入 `2-设计`。
4. 若已经有 design master，再考虑后续面板或画面阶段。

## Reusable Heuristics

- 对道具链来说，`bridge` 不是终点；它只是进入设计 synthesis 的最低门槛。
- 设计阶段最稳的真源不是“长篇 prompt”，而是“可重复消费的设计事实 + 可漂移的 prompt sidecar”。
- 道具设计的多 subagent 协同最适合按结构、材质、痕迹、prompt、审计分层，而不是让一个角色重写所有字段。
- 面板阶段最稳的输入不是重新回读导演 JSON，而是已经固化好的 `道具设计.json + prop_design_prompt.json`。

## Case Log

### Case-20260412-AIGC-PROP-DESIGN-CATEGORY-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/4-道具` 补齐父类目合同，并开放 `2-设计` 作为 `skill-subagents` 治理入口。
- root_cause_or_design_decision: 现有道具链已具备 `1-清单`，但类目父级为空，导致 `2-设计` 缺少合法路由锚点与默认顺序。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md` 锁定 `清单 -> 设计 -> 面板`，再把 `2-设计` 落为 subagent-governed leaf skill。
- prevention_or_replication_checklist:
  - [x] `4-道具` 父级合同已存在
  - [x] `2-设计` 已作为 active 入口声明
  - [x] team 路径已回指到 `.codex/agents/aigc/设计组/道具设计/`
- evidence_paths:
  - `.agents/skills/aigc/4-Design/4-道具/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/SKILL.md`
- user_feedback_or_constraint: 用户明确要求以 `skill-subagents` 规范系统性完善 `.agents/skills/aigc/4-Design/4-道具/2-设计`，并让道具设计组承担专业思考。

### Case-20260412-AIGC-PROP-PANEL-CATEGORY-UPGRADE

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/4-道具` 打通了 `3-面板` 叶子入口，使类目从 `清单 -> 设计` 延伸到 `清单 -> 设计 -> 面板` 的完整闭环。
- root_cause_or_design_decision: 虽然父级合同已声明“清单 -> 设计 -> 面板”，但 `3-面板` 仍是空目录，导致上游 design master 没有稳定展示 handoff。
- final_fix_or_heuristic: 把 `3-面板` 升级为 active leaf，并将其输入锁定为 `2-设计` 产物，而不是另起一条从导演 JSON 直拼 panel 的旁路。
- prevention_or_replication_checklist:
  - [x] `3-面板` 已有本地合同与经验层
  - [x] 父级状态已从 pending 改为 active
  - [x] 类目经验层已记录 panel handoff 规则
- evidence_paths:
  - `.agents/skills/aigc/4-Design/4-道具/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/4-道具/3-面板/SKILL.md`
- user_feedback_or_constraint: 用户明确要求完善 `.agents/skills/aigc/4-Design/4-道具/3-面板`，并参考旧仓道具面板而不是继续保留空目录。
