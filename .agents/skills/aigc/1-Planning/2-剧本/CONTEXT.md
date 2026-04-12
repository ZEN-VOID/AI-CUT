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
| 又把 `格式判模 / 标准剧 / 解说剧` 拆成外部 agent 依赖 | 真源治理层 | 收回到 `2-剧本/SKILL.md` 的内化能力面 | 在 `SKILL.md + audit` 固化 `Internal Capability Fusion Contract` | `2-剧本` 不再引用旧规划组文档 |
| 未显式信号却误切 `解说剧` | 变体裁决层 | 回退 `标准剧` 并在执行报告写明原因 | 在 `Variant Arbitration Contract` 固化“默认安全主案=标准剧” | `selected_variant` 可复盘 |
| `解说剧` 旁白主体漂移 | 体裁纪律层 | 统一为单一旁白主体，默认 `讲述者` | 在 validator 增加主体一致性检查 | 不再出现多旁白主体混写 |
| 对白被润色或改写 | 文本保真层 | 回滚为上游逐字文本 | 保留对话冻结门禁 + 上游对白比对 | `WARN/FAIL-DIALOGUE-FREEZE` 可定位 |
| 引号内混入动作或文本画面错配 | 共享门禁层 | 动作下沉到 `*画面`，重排同命题配对 | 在 `N5-normalize + validator` 固化高频结构门禁 | `FAIL-ACTION-MIXED / FAIL-VISUAL-MISSING` 可拦截 |
| `总字数` 未按最终正文回填 | 收尾层 | 重算并回写 `总字数` 后重跑 validator | 将“字数回填 -> validator 复跑”固定为出口清单 | `FAIL-WORDCOUNT-STALE` 不再复发 |
| 提前把分组/节奏结论写进剧本主稿 | 下游边界层 | 删除越权字段，只保留 handoff 接口 | 在 `Downstream Interface Contract` 固化非 owned truth | 主稿只承载本阶段内容 |

## Repair Playbook

1. 先确认输入是否唯一来自 `1-分集` 输出物。
2. 再确认业务分析与主变体裁决是否明确。
3. 再检查共享硬门禁：对白冻结、主体、双引号、动作剥离、声画配对、字数回填。
4. 最后才看 validator 是否覆盖到当前失败类型。

## Reusable Heuristics

- `2-剧本` 最稳的形态不是“skill + 一堆外部规划组 agent”，而是“一个 skill 内化判模、变体与执行闭环”。
- 默认值始终应是 `标准剧`；只有用户或上游信号明确要求讲述型消费时，才切 `解说剧`。
- `标准剧` 与 `解说剧` 的真正差异是信息承载策略，不是输出真相所有权；canonical 写回权永远只属于 `2-剧本`。
- `2-剧本` 若要保留变体思行证据，应该优先落到 `agents-plan/` 侧车，而不是再长出第二份主稿。
- 下游 `3-分组` 真正需要的是稳定的 `selected_variant + dialogue/narration policy + source_profile`，不是在剧本阶段提前拿到组边界或节奏蓝图。

## Case Log

### Case-20260412-AIGC-PLANNING-SCRIPT-ZHI-XING-INTERNALIZATION

- milestone_type: source_contract_change
- outcome: 将 `2-剧本` 从“单包 + 外部规划组判模/变体 agent”重构为知行合一的单技能内化网络。
- root_cause_or_design_decision: 用户明确要求完善 `.agents/skills/aigc/1-Planning/2-剧本`，内容与机制全量参照现有配置，但不再需要旧规划组文档，相关能力必须重新整理消化融合回 `SKILL.md`。
- final_fix_or_heuristic: 在 `2-剧本/SKILL.md` 内建立 `Internal Capability Fusion Contract + Variant Arbitration Contract + Variant Writing Contract + Thinking-Action Node Contract + Downstream Interface Contract`，并用 Mermaid 承载主干、分支、状态与字段关系；执行闭环仍由 `2-剧本` 自己写回与校验。
- prevention_or_replication_checklist:
  - [x] `2-剧本` 已不再引用旧规划组文档
  - [x] 判模、标准剧、解说剧规则已回收进单一 `SKILL.md`
  - [x] validator 仍作为统一出口门
  - [x] `3-分组 / 节奏` 只保留为下游接口，不再反客为主
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/scripts/validate_script_output.py`
  - `.agents/skills/aigc/1-Planning/2-剧本/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“根据知行合一的规范进行编排”，并废弃旧规划组文档。
