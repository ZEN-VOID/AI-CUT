---
name: story-repair
description: Use when a story2026 novel project needs local change management that traces upstream sources, sibling/previous context, downstream drafts, settings, planning, review gates, and accepted actualization before writing a coherent repair.
governance_tier: full
---

# story-repair

`story-repair` 是 `story2026` 的根级修复治理技能包。它不把“改某个局部”理解为点对点替换，而是先判断该改动会牵动哪些上游真源、同层前列、下游已产物和后续生成约束，再组织统一修复、证据回写与验收。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包。
- 若任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按任务相关性加载项目根 `CONTEXT/`。
- 若改动涉及正文主创或润色，必须继续加载 owning stage 的 `SKILL.md + CONTEXT.md` 和对应 A/B/C provider lane 合同。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `story/SKILL.md` > 本 `SKILL.md` > 本技能分区文件 > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Multi-Subskill Continuous Workflow

- 整体调用 `$story-repair` 时，在项目根、目标局部、改动意图和写回权限明确后，默认连续完成影响判定、修复计划、执行分流、同步回写和验收，不再逐步询问是否继续。
- 无序号同级子技能包若被本技能显式调度，默认全选并发收集证据；父级负责汇总、裁决和 canonical 写回。
- 数字序号阶段或节点默认按数字升序串行：先修源层，再修投影，再修正文或润色，再刷新审查与状态。
- 英文序号 provider lane 默认按原产物所属 lane 或用户显式指定单选分流；只有用户明确要求多路线对比时才并行。
- 卫星技能 `query / resume / review / return` 默认不进入主链；只有定位事实、断点恢复、验收或 actualization 回接需要时才调用。
- 缺少项目根、目标局部、改动意图、破坏性写回授权、原 provider lane 证据或 canonical owner 判定时必须阻断，先输出最小缺口报告。
- 被调度的阶段、卫星或 provider 子技能仍必须加载自身 `SKILL.md + CONTEXT.md`；脚本只能做机械定位、diff、校验和落盘辅助，不得替代 LLM 创作判断。

## When to Use

- 用户要求修改某个线索、伏笔、人物设定、章节情节、关系转折、历史边界、道具机制、世界观规则或文本风格，并且该修改可能影响多个阶段。
- review、读者反馈或人工校阅指出局部错误，但错误根源可能在 `0-初始化 / 1-设定 / 2-卷章 / 3-初稿 / 4-润色 / review / return` 中的上游或旁路产物。
- 需要判断“已经产出的内容是否要改、接下来是否要改、设定和计划是否要同步改”。

## Non-Goals

- 不直接替代 `1-设定`、`2-卷章`、`3-初稿` 或 `4-润色` 的主创执行权。
- 不绕过原 provider lane 直接改写 B/C lane 正文并继续宣称为原 lane 输出。
- 不把 `review` 结论、repair brief 或脚本 patch 当成 canonical creative truth。

## Input Contract

- Accepted input: 修改目标、错误 finding、局部段落、章节路径、线索/角色/设定名称、review 失败项、跨阶段一致性修复请求。
- Required input: 可定位的 `projects/story/<项目名>/`，目标局部或问题描述，期望改动方向，是否允许写回 canonical 文件。
- Optional input: 卷章号、涉及对象、相关 finding、用户给定新设定、禁止改动范围、输出报告路径、是否只生成 repair plan。
- Reject or clarify when: 项目根不可定位；目标局部无法唯一定位；改动方向与上游硬真源冲突且用户未授权改源；需要覆盖已验收终稿但未授权破坏性写回；原 B/C lane 正文需创作性重写但 provider 不可用且用户未显式切换 lane。

## Mode Selection

| mode | 触发信号 | 默认动作 |
| --- | --- | --- |
| `impact_assessment` | 用户只问会影响哪里、是否要改全局 | 生成影响图与修复范围，不写回 |
| `repair_plan` | 用户要求规划修改或 review 失败后返工 | 生成分层修复计划、owner、写回顺序和验收门禁 |
| `execute_repair` | 用户授权执行修改 | 源层优先写回，再同步投影和正文/润色，由 owning stage 执行创作性改写 |
| `audit_only` | 用户要求检查修复是否完成 | 运行一致性审计与 code-reviewer gate，不改正文 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 判定牵动的“全身”范围 | `references/impact-scope-contract.md` |
| 锁定各层 canonical truth 与禁止越权 | `references/source-truth-ledger.md` |
| 执行修复拓扑、分支、汇流和失败回路 | `steps/repair-workflow.md` |
| 判型、通用类型化矩阵与固定上下文包 | `types/type-map.md`、命中的 `types/*/*.md`、`references/impact-scope-contract.md#Universal Type Matrix` |
| 审计、验收与默认 reviewer/provider | `review/review-contract.md` |
| 输出 repair packet 或审计报告 | `templates/output-template.md` |
| 可复用经验与局部修改陷阱 | `knowledge-base/repair-heuristics.md` |
| 机械定位、diff、状态 hook 辅助 | `scripts/README.md`、根级 `../scripts/` |
| 产品侧入口元信息 | `agents/openai.yaml` |

## Execution Contract

1. 先锁定项目根、目标局部、改动意图、写回权限和原产物 provider lane。
2. 加载 `types/type-map.md`，按 `Universal Type Matrix` 选择 `scope / operation / acceptance` 中的固定类型包；多对象修改必须多选叠加。
3. 按 `references/impact-scope-contract.md` 建立影响图：上游真源、同层前列、当前局部、下游已产物、后续约束、状态与审查。
4. 按 `references/source-truth-ledger.md` 锁定 canonical owner，生成“先修源层、再修投影、最后修正文/润色”的写回顺序。
5. 若需要创作性改写，输出 repair brief 并路由到 owning stage 与原 provider lane；本技能只拥有诊断、计划、约束、汇流和验收权。
6. 对已写回内容执行 `review/review-contract.md`，默认使用 `code-reviewer` 作为辅助审计口径；若上层策略阻断真实 reviewer/subagent，则降级为本地 code-reviewer checklist 并显式报告。
7. 修复完成后同步必要的 `STATE.json` skill completion hook，并给出 residual risk 与后续生成约束。

## Root-Cause Execution Contract

修复任务必须沿以下链路上溯：

`Local Symptom -> Direct Inconsistency -> Canonical Owner -> Upstream Contract -> Downstream Consumers -> Meta Rule Source`

优先修复顺序：

1. 项目记忆、初始化和题材方向盘错误：先修 `MEMORY.md`、`0-初始化/north_star.yaml` 或初始化 handoff。
2. 对象设定错误：先修 `1-设定` 对象卡及状态/历史，再修 planning 和正文投影。
3. 线索、伏笔、任务或章法错误：先修 `2-卷章` 的整体/卷级/章级规划，再修已产出章节和后续 handoff。
4. 正文局部错误但源层正确：回到原 `3-初稿` provider lane 执行 `local_repair` 或 `chapter_rewrite`。
5. 润色分布或局部表达错误：回到 `4-润色` owning lane 执行最小局部修补。
6. 已验收事实需要改写：先失效化或重跑 `review` aggregate，再决定是否进入 `return` 重新 actualize。

## Field Mapping

| field_id | owner | required_output | fail_code |
| --- | --- | --- | --- |
| `FIELD-REPAIR-01` | impact scope | `impact_map` with upstream/sibling/downstream/future/state surfaces | `FAIL-REPAIR-SCOPE` |
| `FIELD-REPAIR-02` | source truth | `canonical_owner` and `writeback_order` | `FAIL-REPAIR-OWNER` |
| `FIELD-REPAIR-03` | execution | `repair_plan` and `stage_routes` | `FAIL-REPAIR-PLAN` |
| `FIELD-REPAIR-04` | authorship | `creative_engine` and provider evidence rule | `FAIL-REPAIR-AUTHORSHIP` |
| `FIELD-REPAIR-05` | review | `audit_result` and `code_reviewer_gate` | `FAIL-REPAIR-AUDIT` |
| `FIELD-REPAIR-06` | closure | `changed_files`、`remaining_risks`、`next_generation_constraints` | `FAIL-REPAIR-CLOSURE` |

## Output Contract

- Required output: `repair_packet`，至少包含 `target_locality`、`change_intent`、`scope_packages_loaded`、`impact_map`、`canonical_owner`、`writeback_order`、`stage_routes`、`audit_result`、`changed_files`、`residual_risks`。
- Output format: 默认输出结构化 Markdown 摘要；用户要求落盘时使用 `templates/output-template.md` 生成 repair report。
- Output path: 默认对话交付；落盘时写入 `reports/story-repair-YYYYMMDD.md` 或用户指定路径；项目内证据可写入 `projects/story/<项目名>/repair/`。
- Naming convention: 报告使用 kebab-case 与 `YYYYMMDD` 日期后缀；任务 ID、sidecar slug 和路径片段保持 ASCII 安全。
- Completion gate: 已完成影响图、源层 owner、写回顺序、创作权归属、review/code-reviewer 验收和 residual risk 说明；执行型任务还必须列出实际改动文件与复验结果。
