# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/_shared/council-runtime` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/_shared/council-runtime/module-spec.md` 时，应预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 后续阶段忘记读取 `team.yaml` | 共享运行时层 | 在阶段根技能强制先读项目根 `team.yaml` | 用共享 `council-runtime/module-spec.md` 作为单一真源 | 阶段执行前能判断顾问团是否启用 |
| 四个阶段各自复制一套顾问团规则 | 真源治理层 | 把共性规则上收至 `_shared/council-runtime/` | 阶段根技能只保留本阶段适配，不再平行维护通用规则 | 共性规则只在共享目录维护 |
| `评审` 过早参与前置发散 | 角色边界层 | 将 `评审` 固定到阶段级 `validation-report.md` 前后 | 在共享运行时写死 `pre_and_post_validation_gate` | 评审不再抢前置创作职责 |

## Reusable Heuristics

- 对跨阶段顾问团机制来说，最重要的不是“顾问很多”，而是“团队真源只有一份、运行时只有一套”。
- `策划 / 监制` 更适合做前置参谋，`评审` 更适合卡最终闸门；三者不要混成一轮齐发。

## Case Log

### Case-20260409-AIGC-COUNCIL-RUNTIME-SHARED-SOURCE

- milestone_type: source_contract_change
- outcome: 为 `aigc` 新建 `_shared/council-runtime/`，把跨阶段顾问团机制从阶段私有规则升级为共享运行时真源。
- root_cause_or_design_decision: 用户要求 `1-规划 / 2-组间 / 3-明细 / 4-Design` 在进入阶段根技能或叶子技能时都先读取同一份 `team.yaml`，若继续把规则散落在四个阶段内部，后续极易形成平行真相。
- final_fix_or_heuristic: 将项目级团队真源固定为 `projects/<项目名>/team.yaml`，将跨阶段运行合同固定为 `_shared/council-runtime/module-spec.md`，让阶段根技能只做角色映射适配。
- prevention_or_replication_checklist:
  - [x] 项目根 `team.yaml` 已成为唯一团队真源
  - [x] 共享运行时已建立单一 module-spec
  - [x] `评审` 已被固定到阶段级 validation gate
- evidence_paths:
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
  - `.agents/skills/aigc/_shared/council-runtime/CONTEXT.md`
  - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- user_feedback_or_constraint: 用户明确要求后续四个创作阶段及其叶子技能默认读取 `projects/<项目名>/team.yaml`，并按角色职责启用智能顾问团 subagents。

### Case-20260412-AIGC-COUNCIL-RUNTIME-4-DESIGN-PATH-SYNC

- milestone_type: source_contract_change
- outcome: 将共享顾问团运行时里针对 design 阶段的角色映射与 validation gate，从旧的 `4-主体 / projects/<项目名>/主体/validation-report.md` 收口到 `4-Design / projects/<项目名>/4-Design/validation-report.md`。
- root_cause_or_design_decision: `4-Design` 父级和 shared runtime 已经分裂成两套目录口径；若不先修共享顾问团 carrier，后续 `策划 / 评审` 仍会在旧 runtime 前后介入。
- final_fix_or_heuristic: 以 `project-runtime-layout.md` 为 canonical runtime，对 `module-spec.md` 与 `team.template.yaml` 做同轮回链更新。
- prevention_or_replication_checklist:
  - [x] `module-spec.md` 已改为 `4-Design`
  - [x] `team.template.yaml` 的 `source_skill_refs / operates_on / gate_artifact` 已同步
  - [x] 本地 `CONTEXT.md` 已记录这次 runtime 收口
- evidence_paths:
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
  - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
  - `.agents/skills/aigc/_shared/council-runtime/CONTEXT.md`
- user_feedback_or_constraint: 用户要求继续把 `4-Design` 父级与 shared runtime 一并收口。
