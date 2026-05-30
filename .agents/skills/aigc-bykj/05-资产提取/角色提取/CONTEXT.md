# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/05-资产提取/角色提取` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写角色提取的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 同一角色被拆成多个条目 | 别名归并层 | 回到 `N3-ALIAS-TEST`，按称谓、speaker、行动连续性合并 | `alias_evidence_map` 必填 | canonical 条目唯一 |
| 不同角色因同职务被误合并 | 候选区分层 | 放入 `uncertain_alias_pool` 或保持分离 | 职务称谓不能单独作为合并证据 | 冲突池记录分离理由 |
| 群体被强拆成无证据个体 | 角色粒度层 | 标记为 `importance: group` | `group` 作为合法类型 | 无名群体不伪造个体 |
| 角色设计无剧本证据 | 设计证据层 | 回到 `N6-DESIGN-SPEC`，补 `design_evidence` 或标注推断边界 | `design_spec` 必须带证据链 | 字段能回指剧本或明确推断 |
| 角色被放入剧情场景 | 画面约束层 | 改回纯色背景全身定妆照 | 参考角色 `2-设计` 固定 fitting photo 约束 | prompt 不含场景环境 |

## Repair Playbook

1. 先判断失败是漏提、误提、误合并、未合并、字段无证据还是输出路径错误。
2. 若同一角色重复，优先检查 speaker 标签和称谓绑定。
3. 若合并证据不足，不要硬合并；放入低置信池并说明需要什么证据。
4. 若角色设计字段无证据，回收为上游剧本中的视觉、表演、身份或关系线索，并标注推断边界。
5. 若完整资产汇流冲突，先修本子技能 JSON canonical 输出，再回父级汇总。

## Reusable Heuristics

- 角色提取的难点不是找人名，而是把称谓、代号、对白归属和行动主体合并到正确 canonical 角色。
- “老板/队长/母亲/医生”这类称谓只有在上下文唯一时才可直接合并。
- 低置信池比错误合并更安全；设计规格必须基于 canonical 角色，错误合并会污染所有资产链路。
