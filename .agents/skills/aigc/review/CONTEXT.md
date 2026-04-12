# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `review/` 的经验层知识库，不是过程日志。
- 每次调用 `review/` 时，应自动预加载本文件，用于预审 / 验收 / 学习桥接的模式判断与常见故障闭环。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 高风险执行没有 `preflight-verdict.yaml` 就要往下跑 | review gate | 先进入 `preflight-review` | 把 preflight 写成 review 的显式 mode | 高风险执行前存在 verdict 文件 |
| 阶段产物存在就被当作“已通过验收” | acceptance contract | 同时更新对应 `validation-report.md` | 在 review mode 中固定 acceptance carrier | 验收结论能回到 canonical report |
| `review/` 越权修改 stage 业务真源 | satellite boundary | 只写 verdict 与下一入口 | 在 skill 中固定“不代替阶段执行” | review 输出不再改写业务内容 |
| project / stage report 路径写旧 runtime | runtime mapping | 回查 `project-runtime-layout.md` 后改正 carrier | 把 runtime mapping 当 review 的必读真源 | `validation-report.md` 落点与当前 runtime 一致 |
| learning 只停在聊天说明，没有落 `learning-record.md` | learning bridge | 进入 `learning-bridge` mode | 把 learning record 固定为 canonical carrier | 学习沉淀能在项目目录读回 |
| review 只写 report，不同步断点治理摘要 | governance snapshot sync | 同步更新 `governance-state.yaml.review_bridge` 与 `resume_contract` | 在 review contract 固定“carrier 本体 + governance-state 摘要”双写位 | review 结束后 `resume/query` 能读到最新 gate 状态 |
| 父级 `review/` 同时承载 preflight / acceptance / learning 细则，导致边界再次混层 | subtype governance | 将三种 mode 下沉到 `subtypes/` | 父级只保留 mode router，局部合同放到 subtype | review 根合同不再平行复制三套细则 |

## Repair Playbook

1. 先判定是 `preflight-review`、`acceptance-review` 还是 `learning-bridge`。
2. 再锁定 scope 对应的 canonical carrier。
3. 若问题涉及高风险执行，先查 `mission-brief / route-plan / preflight-verdict`。
4. 若问题涉及阶段验收，先查该 scope 的 `validation-report.md`。
5. 只有 carrier 锁定后，才给出 verdict 与下一入口。

## Reusable Heuristics

- `review/` 最重要的不是“评价得多漂亮”，而是“把 gate 写回 canonical carrier”。
- 对 `aigc` 来说，review 是门下省桥接层，不是阶段执行层。
- 只要 scope 是阶段级，就应该先写该阶段 runtime 下的 `validation-report.md`，而不是默认写项目根报告。
- 若 review 发现的是治理链缺口，最稳的下一入口通常不是阶段 skill，而是根 `aigc` 或 `resume/`。
- `governance-state.yaml` 只记录 review 摘要和下一入口投影，真正 verdict 仍应回到 `preflight-verdict.yaml`、`validation-report.md`、`learning-record.md`。
- 当 `review` 同时拥有 3 种长期模式时，最稳的演化方向不是继续给父技能加段落，而是提升为 `subtypes/preflight-review / acceptance-review / learning-bridge`。

## Case Log

### Case-20260411-AIGC-REVIEW-BOOTSTRAP

- milestone_type: source_contract_change
- symptom_or_outcome: `aigc` 根技能此前没有根级 `review/` 卫星技能，门下省侧 preflight、acceptance 与 learning bridge 只能散落在阶段说明或 harness 文档里。
- root_cause_or_design_decision: review 类能力横跨阶段与项目治理工件，但不拥有阶段执行权，因此更适合作为根级卫星技能而不是新主阶段。
- final_fix_or_heuristic: 新建 `review/`，固定三种 mode：`preflight-review`、`acceptance-review`、`learning-bridge`，并把 carrier 明确映射到项目根或阶段 runtime 的治理工件。
- prevention_or_replication_checklist:
  - [x] 已建立 `review/SKILL.md`
  - [x] 已建立 `review/references/review-modes.md`
  - [x] 已建立 `review/CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/review/SKILL.md`
  - `.agents/skills/aigc/review/CONTEXT.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
- user_feedback_or_constraint: 用户要求参照 `story2026/review` 的卫星技能形态，在 `aigc` 根目录补同名卫星技能，并结合 `harness治理` 进一步考虑配置。

### Case-20260411-AIGC-REVIEW-SUBTYPE-SPLIT

- milestone_type: source_contract_change
- symptom_or_outcome: 将 `review` 从单体卫星技能进一步拆分为 `preflight-review / acceptance-review / learning-bridge` 三个受治理子技能。
- root_cause_or_design_decision: preflight、acceptance 和 learning 的 carrier、scope、输出边界都不同，若继续混在父技能里，会再次形成父级长文并行真源。
- final_fix_or_heuristic: 父级 `review/` 只保留 mode router、scope 判定与 governance-state 摘要同步；三类局部合同分别下沉到 `subtypes/`。
- prevention_or_replication_checklist:
  - [x] `subtypes/preflight-review/` 已建立
  - [x] `subtypes/acceptance-review/` 已建立
  - [x] `subtypes/learning-bridge/` 已建立
  - [x] `review/references/review-modes.md` 已回指 subtype
- evidence_paths:
  - `.agents/skills/aigc/review/SKILL.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
  - `.agents/skills/aigc/review/subtypes/preflight-review/SKILL.md`
  - `.agents/skills/aigc/review/subtypes/acceptance-review/SKILL.md`
  - `.agents/skills/aigc/review/subtypes/learning-bridge/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“1+2”，即同时完成治理状态回填与 review 专项 reviewer 拆分。

### Case-20260412-AIGC-REVIEW-4-DESIGN-CARRIER-SYNC

- milestone_type: source_contract_change
- symptom_or_outcome: `review/` 仍把 `4-Design` 的 acceptance carrier 写成旧的 `projects/<项目名>/主体/validation-report.md`，与当前 `4-Design` runtime 不一致。
- root_cause_or_design_decision: design 阶段 runtime 已经迁到 `projects/<项目名>/4-Design/`，但 review scope mapping 和 acceptance subtype 没有同步跟进，形成了 gate carrier 漂移。
- final_fix_or_heuristic: 以 `project-runtime-layout.md` 为单一 runtime 真源，同步更新 `review/SKILL.md`、`review-modes.md` 与 `subtypes/acceptance-review/SKILL.md` 的 `4-Design` carrier。
- prevention_or_replication_checklist:
  - [x] `review/SKILL.md` 已改到 `projects/<项目名>/4-Design/validation-report.md`
  - [x] `review-modes.md` 已同步 scope mapping
  - [x] `acceptance-review/SKILL.md` 已同步 carrier
- evidence_paths:
  - `.agents/skills/aigc/review/SKILL.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
  - `.agents/skills/aigc/review/subtypes/acceptance-review/SKILL.md`
  - `.agents/skills/aigc/review/CONTEXT.md`
- user_feedback_or_constraint: 用户要求继续把 `4-Design` 父级与 shared runtime 一并收口，避免 review 继续写旧 gate 路径。
