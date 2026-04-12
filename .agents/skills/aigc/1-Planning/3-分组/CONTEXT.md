# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/3-分组` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/3-分组/SKILL.md` 时，应自动预加载本文件。
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
| 输入没有锁到 `2-剧本/第N集.md` | 输入真源层 | 回到规划主稿重新锁定当前集范围 | 在 `SKILL.md + validator` 固化输入根门禁 | 输入清单与当前集一致 |
| `3-分组` 重新依赖外部 planning specialist / reviewer | 真源治理层 | 收回到 `3-分组/SKILL.md` 的内部能力面 | 在 `SKILL.md + audit` 固化 `Internal Capability Fusion Contract` | 不再引用旧规划组文档 |
| 分组切口混用了 `分镜组ID` 与 `分镜ID` | ID 合同层 | 改回三段式 `分镜组ID` | 在模板、validator 与父 skill 固化“组三级、镜四级” | 标题语义稳定 |
| 量化规则只写在 reference，计算仍靠手填 | 计算真源层 | 回到 quantizer 重新计算 | 让 validator 直接消费 quantizer 结果 | `effective_text_chars` 不再只是说明字段 |
| reviewer gate 越权接管组边界 | 复核边界层 | reviewer 仅保留说明，不改 authoritative 数值 | 在 `SKILL.md` 固化 reviewer gate 的非 owned truth 边界 | grouped script 只由父 skill 写回 |

## Repair Playbook

1. 先确认 `2-剧本/第N集.md` 是否是唯一输入主证据。
2. 再确认 quantizer 是否真的参与组界裁决。
3. 再看 grouped script 是否保持正文结构，只在切口处新增组标题。
4. 最后才检查 reviewer gate 是否被误开或越权。

## Reusable Heuristics

- `3-分组` 最稳的定位不是摘要板，而是“在 `2-剧本` 正文里切出组边界后的 grouped script”。
- 对当前阶段来说，最有效的抗漂移机制不是再造 specialist 文档，而是“主合同 digest + quantizer + validator”三件套。
- 节奏复核在规划阶段只应作为 reviewer gate 存在，除非用户明确要求，否则不要把它升级成单独执行面。
- 对 `3-分组` 来说，`effective_text_chars` 一旦进入 validator，就不应再允许人工说明替代 authoritative 结果。

## Case Log

### Case-20260412-AIGC-PLANNING-GROUPING-INTERNALIZATION

- milestone_type: source_contract_change
- outcome: 将 `3-分组` 从“stage-local parent + 外部 planning specialist/reviewer”重构为知行合一的单阶段内化网络。
- root_cause_or_design_decision: 用户要求删除旧规划组载体，因此 `3-分组` 不能继续依赖 shared specialist / reviewer 文档，必须把边界判断、量化裁决和节奏复核 gate 收回自身合同。
- final_fix_or_heuristic: 在 `3-分组/SKILL.md` 内建立 `Internal Capability Fusion Contract`，把分组边界判断、量化裁决、reviewer gate、写回与 validator 统一在一个 stage-local parent skill 中，外部 planning docs 彻底退出运行链。
- prevention_or_replication_checklist:
  - [x] `3-分组` 已不再引用旧规划组文档
  - [x] reviewer 只保留为内部 gate
  - [x] quantizer 与 validator 闭环保持不变
  - [x] grouped script 与执行报告仍是唯一 canonical 输出
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
- user_feedback_or_constraint: 用户明确要求旧规划组文档不再需要，相关能力必须重新整理吸回 `SKILL.md`。
