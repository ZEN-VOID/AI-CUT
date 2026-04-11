# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-视频/3-视频生成` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/6-视频/subtypes/3-视频生成/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 请求对象还没稳定，却直接组织提交计划 | 输入完备性层 | 停止并回到命中的 `1-提示词蒸馏` 子技能 | 在本层固定 `request_ready` 检查，不允许空转 handoff | `submit-plan.json` 的 source request 可追溯 |
| provider 目录存在就被误判为本地可执行 skill | provider 槽位语义层 | 把 provider 目录收敛到 `providers/` 并显式声明“非执行槽位” | 只有出现 `SKILL.md + CONTEXT.md` 的 provider 才算 governed child skill | 不再把空目录当能力存在 |
| 只给一句“去用某 provider”，不写 `submit-plan.json` | 输出契约层 | 补齐 `submit-plan.json + submit-brief.md` | 将 handoff 包固定为 tranche 最低交付 | 计划目录中有完整可读计划 |
| tranche 编号与磁盘目录不一致 | 真源治理层 | 收敛到唯一 `3-视频生成` 路径 | 在审计脚本增加文档声明路径检查 | 父合同、references 与磁盘一致 |

## Repair Playbook

1. 先确认本轮目标是否真的属于“提交前组织”。
2. 再确认上游请求 JSON 是否稳定可提交。
3. 再判断 provider 是否已明确，还是只输出推荐与对比。
4. 产出 `submit-plan.json` 与 `submit-brief.md`。
5. 最后给唯一下一入口：外部 provider skill、人工提交，或回上游补请求对象。

## Reusable Heuristics

- `3-视频生成` 的价值不在“替代 provider”，而在“把提交前的不确定性压缩成可复核的 handoff 包”。
- provider 名称如果只有目录没有合同，就应该被视为槽位，而不是能力。
- 对视频阶段来说，最危险的跳步是“有请求 JSON 就直接下命令”，因为这样会丢失下一入口、失败回放与计划证据。

## Case Log

### Case-20260411-AIGC-VIDEO-SUBMIT-CONTRACT-BOOTSTRAP

- milestone_type: source_contract_change
- symptom_or_outcome: 为 `6-视频/subtypes/3-视频生成` 建立 tranche-3 父技能合同，并把历史遗留的 provider 空目录从 `subtypes/` 收敛为 `providers/`。
- root_cause_or_design_decision: 质量评估暴露出 `6-视频` 真实生成入口存在“文档有、目录有、合同没有”的假成熟度问题；继续保留会使提交层长期漂在技能树之外。
- final_fix_or_heuristic: 将 `3-视频生成` 定义为“稳定请求 JSON -> provider 路由 -> submit-plan -> submit-brief -> 外部执行入口”的唯一 tranche-3 真源。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已建立
  - [x] `CONTEXT.md` 已建立
  - [x] `references/*` 已建立
  - [x] `providers/README.md` 已明确槽位语义
- evidence_paths:
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/SKILL.md`
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/CONTEXT.md`
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/references/execution-flow.md`
  - `.agents/skills/aigc/6-视频/subtypes/3-视频生成/providers/README.md`
- user_feedback_or_constraint: 用户要求对评估暴露出的 `6-视频` 成熟度漂移做全量修复。
