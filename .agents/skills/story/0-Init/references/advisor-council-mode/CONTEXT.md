# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `advisor-council-mode` 子模块的局部经验层，只服务 `智能顾问团模式`。
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
| 顾问团模式被拖回完整问卷 | mode routing | 立刻回到 `Step 0.6` 的一次性内部任务路径 | 在 `module-spec.md` 固化“仅允许确认卡/裁决卡” | 顾问团模式执行中不再出现 Step 1-4 问卷卡 |
| 多位顾问意见被强行揉成单结论 | synthesis contract | 保留 `共识 / 关键分歧 / 少数派高价值提醒` 三层输出 | 将分歧暴露设为协调汇总模板的硬输出项 | 初始化摘要里能同时看到共识与分歧 |
| 指定 agent 路径无效或不可读 | input gate | 在调度前校验路径，并阻断失效顾问 | 把路径预检放进执行 Procedure 第 1 步 | 失败路径会在发起会诊前被报告 |
| 顾问团会诊有纪要，但无法稳定映射到正式 handoff/state | landing contract | 在 `module-spec.md` 增加 `Output Landing Contract`，显式绑定 `north_star_contract.json / 初始化简报.json / .webnovel/state.json` | 把来源分层、brief 依赖边界与验证清单写成子模块硬合同 | 顾问团模式输出不再停在自然语言纪要层 |

## Repair Playbook

1. 先校验 `advisor_agents` 路径。
2. 再构造统一 `initialization_brief`，明确不可越权边界。
3. 并行发起顾问线程，而不是顺手改成问卷。
4. 汇总时先保留分歧，再判断是否真的需要用户裁决。
5. 若只能降级执行，明确标注“顺序读取 agent 文档模拟顾问纪要”。

## Reusable Heuristics

- 顾问团模式的价值不在“人多”，而在把不同 agent 的稳定立场转成结构化策划会意见。
- 如果 brief 没写清“哪些字段已确认、哪些不可越权”，顾问输出很容易变成越界创作而不是初始化会诊。
- 只有会直接改变题材承诺、主角结构、核心冲突的分歧，才值得升级成用户裁决卡。
- 顾问团模式子模块独立治理后，最关键的不是“顾问怎么说”，而是“说完以后怎样进入正式写回链且保留来源分层”。

### Case-002

- milestone_type: source_contract_change
- outcome: `智能顾问团模式` 子模块新增了共享依赖合同、正式写回位点映射与验证清单，使顾问会诊结果能直接进入正式 handoff/state，而不只停留在纪要层。
- root_cause_or_design_decision: 旧版 `module-spec.md` 虽已覆盖顾问并发与综合模板，但没有显式规定共享 reference 如何压进统一 brief、会诊结果如何回填正式 handoff/state、以及如何验证 provenance 与闭环。
- final_fix_or_heuristic: 对顾问团型 mode-playbook，必须把“统一 brief 边界 + 正式写回位点 + provenance 验证”一并写进子模块合同；否则顾问团只会显得热闹，不够可恢复。
- prevention_or_replication_checklist:
  - [x] 子模块声明共享依赖应先压进统一 brief
  - [x] 子模块声明正式 handoff/state 的写回位点
  - [x] 子模块内建分歧保留与 provenance 验证门禁
- evidence_paths:
  - `.agents/skills/story/0-Init/references/advisor-council-mode/module-spec.md`
  - `.agents/skills/story/0-Init/references/advisor-council-mode/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按 `reference-update` 继续治理 `0-Init` 的 `advisor-council-mode` 子模块。

