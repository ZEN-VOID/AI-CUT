# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 非 `PASS` 卷被错误写入 Cards 或 MAP | validation gate contract | 立刻阻断写入并回滚到 validation 结果判定 | 在 `5-Loopback/SKILL.md` 写死 `PASS-only` gate | 非 PASS 卷不再产生 loopback writeback |
| `PASS` 但只被授予 `review/` 的历史复核结果被误 actualize | validation-handoff contract | 立刻阻断写回，并回看 `routing_decision / handoff_targets` 的完整组合 | 在 `5-Loopback` 合同与脚本中同时要求完整 handoff | `handoff_to_review_only` 不再落入 actualization |
| 新三层规划已经成为 primary truth，但 loopback 仍只写兼容 `story_map`，没有把 validated 结果挂回三层规划 companion sidecar | planning-sidecar disconnect | 为 `整体规划 / 第N卷 / 第N章` 各写 actualization sidecar，并保留规划正文不变 | 在 skill/spec/template/script/tests 中统一固定 `planning sidecars -> holomap fallback` | 三层规划有 companion actualization 记录可回读 |
| 规划阶段已进入卷分片模式，但 loopback 仍把卷级 actualization 细节直接写进根 `全息地图.json` | root-vs-slice writeback drift | 先把明细落到命中的卷分片，再回刷 root summary/index | 在 shared spec 固定 `Cards -> slice actualization -> root summary -> STATE` 顺序 | root 不再膨胀成第二份明细仓 |
| 卷级 aggregate 已通过，但没有把变化拆成 `card_deltas / map_deltas / projection_refresh` | delta normalization gap | 先做 `loopback_delta` 提纯，再允许写盘 | 让模板、spec、脚本、测试共同承认 delta 拆分 | 成功包都至少真实写回一类 validated actualization |
| 只写了一半 truth 就中途失败 | multi-target commit discipline | 先做 staged patch，再做统一 commit；失败时 best-effort rollback | 维持 `Cards -> MAP -> STATE -> artifact` 的提交纪律，并保留 pending marker | 任何提交异常后不会留下静默半成品 |

## Repair Playbook

1. 先看这次 loopback 是否同时满足 `PASS + handoff granted`，不要只看 `validation_status`。
2. 再区分问题出在 `card_deltas`、`map_deltas`、`projection_refresh` 还是 commit 纪律。
3. 若对象状态与规划进度混写，优先修 delta 拆分，而不是直接补卡或补 map。
4. 若 `story_map` 被改坏，先恢复 `planned_*`，再把执行态迁回 `actualization`。
5. 若只是查询/恢复或其他非 actualization 诉求，改走 satellite routing。

## Reusable Heuristics

- `5-Loopback` 最核心的价值不是“多存一份总结”，而是把整卷通过验证后的真实变化，挂回未来还会继续被消费的 truth 层。
- 对 loopback 而言，`PASS` 只是必要条件，不是充分条件。
- 新三层规划要保持 planning-only；如果 loopback 直接改正文，就会把 planned truth 和 validated actual 混成一层。
- 只要某条信息回答的是“对象现在怎样了”，优先考虑 `Cards.current_state/history`；只要回答的是“本卷计划推进到哪了”，优先考虑 `story_map.actualization`。
- 先提纯 delta，再回写 truth；如果一上来就直接改卡或改 MAP，几乎一定会把证据链弄脏。
