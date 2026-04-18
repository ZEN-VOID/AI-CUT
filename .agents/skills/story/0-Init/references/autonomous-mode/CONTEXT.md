# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `autonomous-mode` 子模块的局部经验层，只服务 `自主模式`。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 跨模式、跨模块的经验仍优先回写到 `0-Init/CONTEXT.md`，不在本文件横向扩张。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 自主模式退化成“一次只问一个问题” | questionnaire planning | 恢复 4-8 题的成组问卷卡 | 把问卷卡粒度写成规划模板硬约束 | 用户收到的是成组问卷卡而不是零碎追问 |
| 用户自由叙述后仍被要求重填格式 | normalization contract | 先结构化回填，再针对缺口补问 | 把“先吸收后补问”固定为执行 Procedure | 自由文本能被归一化为结构字段 |
| 初始化层试图拍死下游问题 | truth-owner routing | 把不该现在决定的字段写进 `unknowns` 并标注下游归属 | 在问卷规划时先判断 `cards_seed / planning_seed / unknowns` | 输出摘要里能看到清晰的下游路由 |
| 问卷回合聊得很多，但无法稳定沉淀为正式 handoff/state | landing contract | 在 `module-spec.md` 增加 `Output Landing Contract`，显式绑定 `north_star_contract.json / 初始化简报.json / .webnovel/state.json` | 把回合摘要与最终确认卡的写回位点、验证清单写成子模块硬合同 | 自主模式不再只是“对话充分”，而是能恢复、能交接 |

## Repair Playbook

1. 先看当前缺口是否真的阻塞下一步，而不是机械继续追问。
2. 每轮保持 4-8 题的成组粒度，并给自由描述入口。
3. 用户自由叙述时先做结构化吸收，再决定缺什么。
4. 回合摘要必须同时返回 `已确认 / 助手推断 / 仍缺失 / 下游路由`。
5. 若用户改口“你直接补完”或指定顾问团，应升级模式而不是硬守原路径。

## Reusable Heuristics

- 自主模式的核心不是“问得细”，而是“每一轮都在减少真正阻塞的未知项”。
- 当用户已经给了长段自由描述，继续逐格追问往往说明结构化回填没有先做好。
- 自主模式最容易失控的地方不是信息不足，而是把本该留给下游的选择过早拍板。
- 自主模式子模块若要真正独立治理，必须同时定义“怎么问”和“问完落到哪里”；否则问卷合同会强、正式 handoff 会弱。

### Case-002

- milestone_type: source_contract_change
- outcome: `自主模式` 子模块新增了共享依赖合同、正式写回位点映射与验证清单，使问卷编排与正式 handoff/state 之间形成稳定闭环。
- root_cause_or_design_decision: 旧版 `module-spec.md` 已经能指导问卷编排，但没有显式规定共享 reference 的按需读取边界，也没有把回合摘要和最终确认卡如何回填正式 handoff/state 写成子模块级合同。
- final_fix_or_heuristic: 对问卷型 mode-playbook 来说，“提问逻辑”与“正式写回逻辑”必须并列出现；否则执行者只会觉得聊完了，却不知道何时算真正交接完成。
- prevention_or_replication_checklist:
  - [x] 子模块声明共享依赖的读取边界
  - [x] 子模块声明回合中间态与最终 handoff/state 的写回位点
  - [x] 子模块内建问卷路由与写回验证门禁
- evidence_paths:
  - `.agents/skills/story/0-Init/references/autonomous-mode/module-spec.md`
  - `.agents/skills/story/0-Init/references/autonomous-mode/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按 `reference-update` 继续治理 `0-Init` 的 `autonomous-mode` 子模块。

