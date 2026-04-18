# story2026 Validation Team Contract

## Purpose

本文件是 `4-Validation` 阶段评估团队的单一真源，用于定义：

- 白名单 checker 角色
- 各角色职责边界
- 允许的调度与聚合关系

边界：

- 当前仓库**未维护** `.codex/agents/story/` 或 `.codex/agents/story2026/` 独立 agent 文档树。
- 因此，评估团队的 authoritative source 固定为：
  - 当前文件
  - `4-Validation/SKILL.md`
  - `checker-output-schema.md`

## Canonical Roster

| role_id | role_type | mandatory | purpose | must_not_do |
| --- | --- | --- | --- | --- |
| `context-agent` | support | yes | 组装 `validation_fact_pack` 与最小评估上下文 | 不给最终质量裁决 |
| `consistency-checker` | checker | yes | 检查设定、一致性、规则边界 | 不替代 continuity / ooc 判断 |
| `continuity-checker` | checker | yes | 检查时间线、承接、推进连续性 | 不直接改写对象真源 |
| `ooc-checker` | checker | yes | 检查角色行为、声口与人格偏离 | 不代替剧情结构判断 |
| `immersion-voice-checker` | checker | yes | 检查说明腔、冷评论腔、AI 感表达 | 不单独决定 PASS |
| `reader-pull-checker` | checker | conditional | 检查追读钩子、读者拉力与回收张力 | 不代替节奏系统判断 |
| `high-point-checker` | checker | conditional | 检查爽点、高点、兑现密度 | 不代替完整质量聚合 |
| `pacing-checker` | checker | conditional | 检查 Strand、节奏与推进速度 | 不代替 continuity 判断 |
| `spoiler-checker` | checker | conditional | 检查提前解题、伏笔剧透与过度明示 | 不代替 consistency 判断 |

## Dispatch Rules

1. `context-agent` 必须先于所有 checker 运行。
2. 基础 checker 默认必开：
   - `consistency-checker`
   - `continuity-checker`
   - `ooc-checker`
   - `immersion-voice-checker`
3. 条件 checker 按章节类型、用户要求与 `validation_fact_pack` 动态开启：
   - `reader-pull-checker`
   - `high-point-checker`
   - `pacing-checker`
   - `spoiler-checker`
4. 若 `validation_fact_pack.foreshadow_silence_slice.has_active_foreshadowing = true`，则 `spoiler-checker` 默认必开。
5. 若 `validation_fact_pack.style_gate.anti_ai_required = true` 或 `style_gate.no_poison_required = true`，则 `immersion-voice-checker` 不得关闭。
6. 未登记在本文件中的角色，不得作为正式 checker 注入 `selected_agents`。

## Governance Layering

- `team.yaml.roles.review`（缺失时回退 `team.yaml["评审"]`）
  - 只允许作为评审专家组的增量治理层。
  - 不得覆盖本文件定义的 checker roster。
- `review/`
  - 只消费聚合结果与阶段结论。
  - 不得改写 roster 或 checker 职责。

## Output Alignment

- 所有 checker 的结构化输出字段，统一回指 `checker-output-schema.md`。
- `selected_agents` 必须只包含本文件登记的 `role_id`，外加已激活的评审专家组成员摘要字段。
