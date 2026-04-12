# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-视频/2-视频生成` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 请求对象还没稳定，却直接组织提交计划 | 输入完备性层 | 停止并回到命中的 `1-提示词蒸馏/*` 子技能 | 在本层固定 `request_ready` 检查，不允许空转 handoff | `submit-plan.json` 的 source request 可追溯 |
| provider 目录存在就被误判为本地可执行 skill | provider 槽位语义层 | 把 provider 目录收敛为槽位说明，不把其当作能力存在 | 只有出现 `SKILL.md + CONTEXT.md` 的 provider 才算 governed child skill | 不再把空目录当能力存在 |
| 主合同之外仍把规则下沉到 `references/` 或 `providers/README.md` | 真源治理层 | 把字段、流程、路由与输出契约收束回 `SKILL.md` | 保持 `SKILL.md` 为唯一规范真源，其他文件只做经验或说明 | 关键规则不再分散 |
| `2-视频生成` 与 `3-视频生成` 混写 | 路径归一层 | 统一收敛到真实磁盘路径 `.agents/skills/aigc/6-Video/2-视频生成/` | 在父级、根级与经验层同步路径口径 | 不再出现双编号漂移 |
| 只给一句“去用某 provider”，不写 `submit-plan.json` | 输出契约层 | 补齐 `submit-plan.json + submit-brief.md` | 将 handoff 包固定为叶子最低交付 | 计划目录中有完整可读计划 |

## Repair Playbook

1. 先确认本轮目标是否真的属于“提交前组织”。
2. 再确认上游请求 JSON 是否稳定可提交。
3. 再判断 provider 是否已明确，还是只输出推荐与对比。
4. 产出 `submit-plan.json` 与 `submit-brief.md`。
5. 最后给唯一下一入口：外部 provider skill、人工提交，或回上游补请求对象。
6. 收尾复扫是否仍残留 `3-视频生成` 或 `references/` 作为规则真源。

## Reusable Heuristics

- `2-视频生成` 的价值不在“替代 provider”，而在“把提交前的不确定性压缩成可复核的 handoff 包”。
- provider 名称如果只有目录没有合同，就应该被视为槽位，而不是能力。
- 对视频阶段来说，最危险的跳步是“有请求 JSON 就直接下命令”，因为这样会丢失下一入口、失败回放与计划证据。
- 只要字段表、流程或输出契约还散落在 sidecar 文件里，父 skill 就还没有真正升格成单一真源。

## Case Log

### Case-20260411-AIGC-VIDEO-SUBMIT-CONTRACT-BOOTSTRAP

- milestone_type: source_contract_change
- symptom_or_outcome: 为 `6-Video/2-视频生成` 建立提交前组织叶子合同，并将 provider 空目录收敛为 `providers/` 槽位说明。
- root_cause_or_design_decision: 质量评估暴露出 `6-Video` 的真实生成入口存在“文档有、目录有、合同不完整”的假成熟度问题；继续保留会使提交层长期漂在技能树之外。
- final_fix_or_heuristic: 将 `2-视频生成` 定义为“稳定请求 JSON -> provider 路由 -> submit-plan -> submit-brief -> 外部执行入口”的唯一叶子真源。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已建立
  - [x] `CONTEXT.md` 已建立
  - [x] `providers/README.md` 已明确槽位语义
- evidence_paths:
  - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/providers/README.md`
- user_feedback_or_constraint: 用户要求对评估暴露出的 `6-Video` 成熟度漂移做全量修复。

### Case-20260412-AIGC-VIDEO-GENERATION-SINGLE-SOURCE-UPLIFT

- milestone_type: source_contract_change
- symptom_or_outcome: 将 `2-视频生成` 从“主合同摘要 + references 细则”升格为单一 `SKILL.md` 真源，并统一修复 `2/3-视频生成` 路径漂移。
- root_cause_or_design_decision: 原结构同时存在主合同、`references/*.md` 与 `providers/README.md` 三处局部规则承载，导致字段、流程、输出契约和路径回链无法稳定收束。
- final_fix_or_heuristic: 把 `references/*.md` 的规范内容内联进 `SKILL.md`，让 `CONTEXT.md` 只保留经验层，并把全仓当前路径口径统一收敛到 `.agents/skills/aigc/6-Video/2-视频生成/`。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已成为唯一规范真源
  - [x] `CONTEXT.md` 仅保留经验层
  - [x] `references/` 已退出规范承载
  - [x] 根级与父级路径回指已同步
- evidence_paths:
  - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
- user_feedback_or_constraint: 用户明确要求将 `references` 内容整合到 `SKILL.md` 内，不再以 `references` 作为载体引用。
