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
| 非 `PASS` 集被错误写入 Cards 或 MAP | validation gate contract | 立刻阻断写入并回滚到 validation 结果判定 | 在 `5-Loopback/SKILL.md` 写死 `PASS-only` gate | 非 PASS episode 不再产生 loopback writeback |
| `PASS` 但只被授予 `review/` 的历史复核结果被误 actualize | validation-handoff contract | 立刻阻断写回，并回看 `routing_decision / handoff_targets` | 在 `5-Loopback/SKILL.md` 与 `loopback_manager.py` 同时要求 `PASS + handoff granted` | `handoff_to_review_only` 不再落入 actualization |
| 把对象状态写进 `story_map`，或把 planning progress 写进 Cards | responsibility split | 重新拆分 `card_deltas` 与 `map_deltas` | 在父层合同固定 `Cards 管对象状态 / MAP 管规划实现进度` | 同一变化项只落到正确 truth 层 |
| `story_map.actualization` 覆盖了 `planned_*` | map actualization guardrail | 回退到 `actual_* / validated_*` 新字段 | 在合同明确“只增 actualization，不覆 planning rationale” | planning 与 actualization 可并存对照 |
| `5-Loopback` 只产出学习/恢复动作，没有 episode validated actualization | stage contract | 把主流程收回四步 actualization 协议 | 在 SKILL 中把 query / resume / learn 降为 satellite routing | PASS episode 能稳定产出 loopback artifact 与 writeback |
| `5-Loopback/SKILL.md` 的步骤编号与 `workflow_manager.py` 的 tracked steps 漂移 | workflow alignment contract | 先统一 workflow step 与 skill 主干，再修 resume/closure 文案 | 在 SKILL 中明确标出 `Step 1-4` 与 tracked workflow 对齐关系 | `resume/` 与 workflow runtime 能解释 loopback 当前停点 |
| `5-Loopback` 已升级为正式阶段合同，但 scripts / CLI / 测试仍停留在缺席状态 | source landing gap | 新增 `loopback_manager.py` 与统一 CLI 入口 | 阶段升级时同步补齐 `脚本入口 + story.py 转发 + 调用矩阵 + 最小红绿测试` | `PASS` 集可真正生成 `第N集.loopback.json` 并完成 truth writeback |
| 已移除的卫星能力仍残留在 loopback 路由、CLI 或调用矩阵 | canonical routing contract | 同步删掉技能声明、CLI 转发、workflow registry 与测试残留 | 卫星能力上下线时执行 `skill + docs + CLI + registry + tests` 五点清理 | 仓库内不再出现失效的 `/webnovel-learn` 或 `learn/` 路由 |
| loopback 已消费 PASS 结果，但没有和 `<run_id>` 级 task artifact 建立回指 | governance artifact continuity | 在 `5-Loopback` 合同中显式承认 `validation_report_ref / artifact_manifest_ref` | 让 writeback 层与验证证据层形成可追溯闭环，而不是只剩孤立的 loopback json | 任何一次 actualization 都能回溯到对应的 PASS 证据目录 |

## Repair Playbook

1. 先看这次 loopback 是否同时满足 `PASS + handoff granted`，不要只看 `validation_status`。
2. 再区分问题出在 `card_deltas`、`map_deltas`、`projection_refresh` 还是 workflow step 对齐。
3. 若对象状态与规划进度混写，优先修 Step 1 的 delta 拆分，而不是直接补丁 card 或 map。
4. 若 `story_map` 被改坏，先恢复 `planned_*`，再把执行态字段迁回 `actualization / validated_*`。
5. 若 tracked workflow 与 skill 主流程编号不一致，先修 `SKILL.md / workflow_manager.py` 对齐，再谈 resume。
6. 若只是查询/恢复或其他非 actualization 诉求，改走 satellite routing，不进入 actualization 主流程。

## Reusable Heuristics

- `5-Loopback` 最核心的价值不是“多存一份总结”，而是把单集通过验证后的真实变化，稳稳挂回未来会被消费的 truth 层。
- 对 `5-Loopback` 而言，`PASS` 只是必要条件，不是充分条件；必须再确认上游真的把本轮 handoff 给了 `5-Loopback`。
- 只要某条信息回答的是“对象现在怎样了”，优先考虑 `Cards.current_state/history`；只要回答的是“计划节点推进到哪了”，优先考虑 `story_map.actualization`。
- `planned_*` 和 `actualized_*` 同时保留，能显著降低后续返工时“到底是计划错了还是执行偏了”的诊断成本。
- 先提纯 delta，再回写 truth；如果一上来就直接改卡或改 MAP，几乎一定会把证据链弄脏。
- stage 合同里写的主干步骤必须和 `workflow_manager.py` 的 tracked steps 对齐，否则 `resume/` 很快会把 loopback 当成另一套流程来解释。
- 只要 actualization 规则同时牵涉 `Cards`、`MAP` 和卫星路由，就应用“共享 spec + 输出模板”双锚维护，避免边界只存在于某个阶段说明里。
- 当某个 stage 从“说明层”升级为“正式执行层”时，不能只改 `SKILL.md`；至少要同时落地脚本入口、统一 CLI 转发和一组最小回归测试，否则 stage 会停留在文档存在、系统缺席的伪完成态。
- 当 `5-Loopback` 的卫星拓扑发生增删时，必须同步清理技能目录、CLI、workflow registry、调用矩阵和测试；否则回环拓扑会留下伪节点。
- writeback 产物若不能回指到同一 `<run_id>` 的 PASS 证据层，后续 query/audit 很快会退化成“知道写了什么，不知道凭什么能写”。
