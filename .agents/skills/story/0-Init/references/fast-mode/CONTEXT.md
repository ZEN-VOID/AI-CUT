# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `fast-mode` 子模块的局部经验层，只服务 `快速模式`。
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
| 快速模式被拖回长问卷 | mode routing | 立刻回到 `Step 0.6` 的一次性补全路径 | 在 `module-spec.md` 固化“仅允许确认卡/阻塞卡” | 快速模式执行中不再出现 Step 1-4 问卷卡 |
| 助手脑补和用户确认混写 | source attribution | 在 `sources_breakdown` 中显式区分 `user_confirmed` 与 `assistant_inferred` | 把字段归属写成输出合同硬要求 | 初始化草案里每类字段来源都可追溯 |
| 用户输入极少时仍硬填满所有字段 | risk control | 把争议字段写入 `unknowns`，必要时只补 1 张阻塞卡 | 把“够下游起跑即可”固定为补全准则 | `unknowns` 保留真实不确定项，而不是假装确定 |
| 快速模式草案能生成，但无法稳定回写正式 handoff/state | landing contract | 在 `module-spec.md` 增加 `Output Landing Contract`，显式绑定 `north_star_contract.json / 初始化简报.json / .webnovel/state.json` | 把落盘位点映射与验证清单写成子模块硬合同 | 快速模式输出不再只是“看起来像草案”，而是能直接进入正式写回链 |

## Repair Playbook

1. 先抽取 brief 里的硬信号与禁飞区。
2. 再判断哪些字段可以保守补完，哪些必须留给 `unknowns`。
3. 输出时强制区分用户确认项与助手推断项。
4. 若出现高后果分叉，只允许升级成 1 张阻塞卡。
5. 外部核验失败时回退到本地知识保守方案，并标注不确定性。

## Reusable Heuristics

- 快速模式的目标是“缩短输入链”，不是“伪装成什么都已确定”。
- 如果 `unknowns` 被写空，但用户输入其实很少，往往意味着快速模式已经越界脑补。
- 快速模式里最值钱的不是补得满，而是补得稳且来源清楚。
- 快速模式子模块一旦独立治理，就不能只给生成模板；还要把正式写回位点和验证门禁写进 `module-spec.md`，否则主合同仍要替它兜底。

### Case-002

- milestone_type: source_contract_change
- outcome: `快速模式` 子模块新增了共享依赖合同、正式写回位点映射与验证清单，使其从“会生成草案”升级为“能独立指导快速模式闭环”的 mode-playbook。
- root_cause_or_design_decision: 旧版 `module-spec.md` 已能描述一次性补全流程，但没有显式写出共享 reference 如何参与、结果如何回填正式 handoff/state，以及如何在子模块层验证闭环，导致其“唯一模板真源”地位仍偏弱。
- final_fix_or_heuristic: 对独立治理的模式子模块，仅有任务模板不够；还要补齐 `Shared Dependency Contract + Output Landing Contract + Verification Checklist`，这样执行者不必回到主 `SKILL.md` 才知道如何闭环。
- prevention_or_replication_checklist:
  - [x] 子模块声明共享依赖的读取边界
  - [x] 子模块声明正式 handoff/state 的写回位点
  - [x] 子模块内建验证门禁
- evidence_paths:
  - `.agents/skills/story/0-Init/references/fast-mode/module-spec.md`
  - `.agents/skills/story/0-Init/references/fast-mode/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按 `reference-update` 继续治理 `0-Init` 的 `fast-mode` 子模块。

