# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/2-剧本` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

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
| 又把 `标准剧 / 解说剧` 拆成两个本地子技能包 | 技能治理层 | 收敛回单一 `2-剧本` 技能包 | 在 `SKILL.md` 固化“单包 + subagent 变体” | 本地目录下不再出现两个 sibling 技能真源 |
| 直接绕过 `1-分集` 输出物重做自由切分 | 输入真源层 | 回到 `1-分集/第N集.md + 执行报告 + episode-split-plan.json` | 在 `SKILL.md` 固化 `1-分集` 输出物为唯一输入锚点 | 输入链路可追溯 |
| subagent 直接写 canonical 文件 | 编排边界层 | 收回写回权到 `2-剧本` 父技能 | 在 subagent/team 与本技能合同中固化 patch-only 边界 | canonical 文件只由本技能写回 |
| validator 只做弱检测，漏掉主体/引号/画面配对问题 | 校验器层 | 补强统一 validator | 把高频硬门禁收敛到脚本 | 结构性失误能被脚本拦下 |
| `解说剧` 未显式信号却被默认启用 | 路由裁决层 | 回退到 `标准剧` 并补写裁决理由 | 在执行报告中固定记录主变体裁决证据 | 主变体选择可复盘 |
| 变体 subagent 与 skill 的执行边界重新混写 | 执行治理层 | 收回 canonical 写回、validator 与执行报告到 skill | 在 `SKILL.md` 与入口元数据同步固化“subagents 返回 `agents plan + patch / note`，skill 统筹执行” | 变体角色不再伪装成并列执行者 |
| `总字数` 未按最终 `【剧本正文】` 实算值回填，导致 validator 卡住 | 输出收尾层 | 在最终文本定稿后回填 `总字数` 并重新跑 validator | 将“字数回填 -> validator 复跑”视为 `2-剧本` 出口清单固定步骤 | `FAIL-WORDCOUNT-STALE` 不再出现 |

## Repair Playbook

1. 先确认本技能是否仍是单一技能包。
2. 再确认输入是否唯一来自 `1-分集` 输出物。
3. 再检查 `格式判模 -> 标准剧/解说剧` 的路由是否被正确执行。
4. 最后才检查 validator 是否覆盖到当前失败类型。

## Reusable Heuristics

- 在 `1-Planning` 里，`2-剧本` 最稳的形态是“一个技能包 + 多个变体 subagents”，而不是“多个本地 sibling 技能包”。
- `格式判模` 负责决定变体，`2-剧本` 负责写 canonical 主稿，`标准剧 / 解说剧` 只负责 patch；这三个层次一旦混写，就会重新长出第二真源。
- 如果 `2-剧本` 已经写了主稿，却没留下单集执行报告和 handoff patch，这轮执行仍不算闭环完成。
- `标准剧` 默认值更安全；只有用户或 `格式判模` 明确给出信号时，才应启用 `解说剧`。
- 在 `2-剧本` 里，subagents 只适合承担变体思考、`agents plan`、结构判断和文本 patch；真正的主稿写回、validator 和闭环始终属于 skill。
- `2-剧本` 若需要沉淀变体规划过程，应优先写 `agents-plan/`，而不是重新长出强制 thinking sidecar 或第二份 canonical 草稿。
- `2-剧本` 的 `总字数` 不是装饰字段；它必须在主稿最终定稿后按 `【剧本正文】` 实算值回填，否则 validator 会把产物拦在出口。

## Case Log

### Case-20260412-AIGC-PLANNING-SCRIPT-SINGLE-PACKAGE

- milestone_type: source_contract_change
- outcome: 为 `2-剧本` 建立单一技能包，并通过规划组 `标准剧 / 解说剧` subagents 完成变体路由。
- root_cause_or_design_decision: 用户明确要求“标准剧/解说剧 不要分成两个子技能包，一个技能包内完成，不同的 subagents 触发”。
- final_fix_or_heuristic: 只建立 `2-剧本/SKILL.md + CONTEXT.md + CHANGELOG.md + scripts/validate_script_output.py + agents/openai.yaml`，不再建立本地变体子目录。
- prevention_or_replication_checklist:
  - [x] 本地只保留单一 `2-剧本` 技能包
  - [x] 变体通过规划组 subagents 触发
  - [x] 已具备统一 validator
  - [x] 已补齐入口元数据
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/scripts/validate_script_output.py`
  - `.agents/skills/aigc/1-Planning/2-剧本/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求变体作为 subagents 触发，而不是本地双子技能包。
