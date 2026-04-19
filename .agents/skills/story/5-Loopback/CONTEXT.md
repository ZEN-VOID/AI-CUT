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
| `PASS` 但只被授予 `review/` 的历史复核结果被误 actualize | validation-handoff contract | 立刻阻断写回，并回看 `routing_decision / handoff_targets` 的完整组合 | 在 `5-Loopback/SKILL.md` 与 `loopback_manager.py` 同时要求 `routing_decision=handoff_to_review_and_loopback` 且 `handoff_targets` 同含 `review/ + 5-Loopback` | `handoff_to_review_only` 或缺失 `review/` 的 packet 不再落入 actualization |
| aggregate JSON 不带 `loopback_delta` 时，loopback 产出空 artifact 却返回成功 | actualization delta gate | 直接阻断为 `loopback_delta_empty`，要求补足 `card_deltas / map_deltas / projection_refresh` 之一 | `loopback_manager.py` 把“空 delta”视为硬失败，并为此保留回归测试 | 任何 loopback 成功包都至少真正写回一类 validated actualization |
| 主角成长变化被写成模糊 prose 历史，没有同步刷新 `growth_state` | character growth actualization | 把 validated 蜕变拆成 `current_state.growth_state + experience_timeline + history[].growth_delta` 三写位 | 主角成长一律结构化 actualize，不再只追加“变强了/想开了”式摘要 | query 能直接回答主角三轴现在走到哪，history 也能回放每集蜕变 |
| 把对象状态写进 `story_map`，或把 planning progress 写进 Cards | responsibility split | 重新拆分 `card_deltas` 与 `map_deltas` | 在父层合同固定 `Cards 管对象状态 / MAP 管规划实现进度` | 同一变化项只落到正确 truth 层 |
| `story_map.actualization` 覆盖了 `planned_*` | map actualization guardrail | 回退到 `actual_* / validated_*` 新字段 | 在合同明确“只增 actualization，不覆 planning rationale” | planning 与 actualization 可并存对照 |
| 规划阶段已进入十集分片模式，但 loopback 仍把 episode-local actualization 细节直接写进 `全息地图.json` | root-vs-slice writeback drift | 先把明细落到命中的 `story_map_slice_ref`，再回刷 root summary/index | 在 `loopback-actualization-spec.md` 固定 `Cards -> slice actualization -> root actualization summary -> STATE` 顺序 | root 不再膨胀成第二份 actualization 明细仓 |
| `projection_refresh` 声称支持 `merge/append`，实现却只会整体覆盖 | projection refresh contract | 为 `target_ref + refresh_mode` 建立统一解析，并在写盘前校验目标位类型 | 模板 / SKILL / `loopback_manager.py` / tests 四层同时维护 refresh 语义，禁止只在模板里写能力 | `merge` 保留旧字段，`append` 只对数组生效，未知类型在写盘前失败 |
| 上游 delta 基于旧 truth 版本生成，却在 loopback 阶段静默覆盖新状态 | revision guardrail | 为 card / map / projection delta 引入可选 `expected_revision`，命中漂移时直接阻断写回 | 把 actualization 相关 revision 固化到 card `loopback_revision`、`story_map.actualization.revision`、`STATE.runtime_markers.loopback_state_revision`，并为 drift 场景补回归测试 | revision 不一致时 loopback 失败，而不是覆写已更新 truth |
| delta 包混入 `core / planned_* / review_* / source-fix` 等越权字段 | delta whitelist contract | 在 loopback intake 先做 envelope/patch 白名单校验 | 让 `SKILL + shared spec + template + tests` 共同承认白名单，禁止把 review/source-fix 建议伪装成 validated delta | 越权字段在正式 staged patch 之前就被拦截 |
| `5-Loopback` 只产出学习/恢复动作，没有 episode validated actualization | stage contract | 把主流程收回四步 actualization 协议 | 在 SKILL 中把 query / resume / learn 降为 satellite routing | PASS episode 能稳定产出 loopback artifact 与 writeback |
| `5-Loopback/SKILL.md` 的步骤编号与 `workflow_manager.py` 的 tracked steps 漂移 | workflow alignment contract | 先统一 workflow step 与 skill 主干，再修 resume/closure 文案 | 在 SKILL 中明确标出 `Step 1-4` 与 tracked workflow 对齐关系 | `resume/` 与 workflow runtime 能解释 loopback 当前停点 |
| `5-Loopback` 已升级为正式阶段合同，但 scripts / CLI / 测试仍停留在缺席状态 | source landing gap | 新增 `loopback_manager.py` 与统一 CLI 入口 | 阶段升级时同步补齐 `脚本入口 + story.py 转发 + 调用矩阵 + 最小红绿测试` | `PASS` 集可真正生成 `第N集.loopback.json` 并完成 truth writeback |
| 已移除的卫星能力仍残留在 loopback 路由、CLI 或调用矩阵 | canonical routing contract | 同步删掉技能声明、CLI 转发、workflow registry 与测试残留 | 卫星能力上下线时执行 `skill + docs + CLI + registry + tests` 五点清理 | 仓库内不再出现失效的 `/webnovel-learn` 或 `learn/` 路由 |
| loopback 已消费 PASS 结果，但没有和 `<run_id>` 级 task artifact 建立回指 | governance artifact continuity | 在 `5-Loopback` 合同中显式承认 `validation_report_ref / artifact_manifest_ref` | 让 writeback 层与验证证据层形成可追溯闭环，而不是只剩孤立的 loopback json | 任何一次 actualization 都能回溯到对应的 PASS 证据目录 |
| Cards 使用 `content.card_schema.*.current_state/history` 嵌套结构时，loopback 却把 validated patch 写到 JSON 顶层 | card schema landing gap | 让 `loopback_manager.py` 先解析实际 card schema owning node，再回写其 `current_state/history`；顶层只保留扁平 legacy fallback | 为 loopback 增加 nested-card 回归测试，禁止再假设所有 Cards 都是扁平结构 | validated card 写回进入 `content.card_schema.*`，JSON 顶层不再长出脏 `current_state/history` |
| Cards / MAP / STATE / artifact 串行提交时中途失败，留下半完成 actualization | multi-target commit discipline | 先在内存 staging 所有 patch，再用统一 commit plan 写盘；提交期失败时回滚已写目标 | 对所有多目标 writeback 阶段建立“先验证、再提交、失败回滚”的统一纪律，并补 commit-failure 回归测试 | 任何提交异常后，Cards/MAP/STATE 与 artifact 要么一起成功，要么一起回到提交前 |
| 进程在正式提交中途崩溃，rollback 没有机会执行 | pending marker continuity | 在 commit 前先写 `runtime_markers.loopback_pending` manifest，成功后移除并固化 committed manifest | 让 resume/query/audit 至少能发现“上次 loopback 曾进入提交期”，而不是把 crash 当成完全没发生 | 异常退出后，状态层能留下 pending 痕迹；正常成功时 pending 会被清理 |

## Repair Playbook

1. 先看这次 loopback 是否同时满足 `PASS + handoff granted`，不要只看 `validation_status`。
2. 再区分问题出在 `card_deltas`、`map_deltas`、`projection_refresh` 还是 workflow step 对齐。
3. 若对象状态与规划进度混写，优先修 Step 1 的 delta 拆分，而不是直接补丁 card 或 map。
4. 若 `story_map` 被改坏，先恢复 `planned_*`，再把执行态字段迁回 `actualization / validated_*`。
5. 若 tracked workflow 与 skill 主流程编号不一致，先修 `SKILL.md / workflow_manager.py` 对齐，再谈 resume。
6. 若 `projection_refresh` 带有 `target_ref / refresh_mode`，先在内存里完成目标位解析与类型校验，再决定是否允许写盘。
7. 若 delta 附带 `expected_revision`，先比对当前 truth revision；revision 漂移说明 delta 已经过时，应失败而不是覆盖。
8. 若正式写盘牵涉 `Cards + MAP + STATE + artifact` 多目标，必须先做 staged patch，再做统一 commit；不要边写边验证。
9. 若只是查询/恢复或其他非 actualization 诉求，改走 satellite routing，不进入 actualization 主流程。
10. 若 aggregate 未给 `loopback_delta`，不得生成“空成功” artifact；先补 delta，再允许 actualize。
11. 若当前集涉及主角成长推进，优先写结构化 `growth_delta`，不要把成长变化只塞进 `change_summary`。

## Reusable Heuristics

- `5-Loopback` 最核心的价值不是“多存一份总结”，而是把单集通过验证后的真实变化，稳稳挂回未来会被消费的 truth 层。
- 对 `5-Loopback` 而言，`PASS` 只是必要条件，不是充分条件；必须再确认上游真的把本轮 handoff 给了 `5-Loopback`。
- 对 `5-Loopback` 而言，真正可写回的 gate 不是“看起来像 PASS”，而是完整的 `handoff_to_review_and_loopback + review/ + 5-Loopback` 组合。
- 只要某条信息回答的是“对象现在怎样了”，优先考虑 `Cards.current_state/history`；只要回答的是“计划节点推进到哪了”，优先考虑 `story_map.actualization`。
- 在 story2026 的 canonical cards 里，`current_state/history` 默认属于 `content.card_schema.<具体卡型>`；只有 legacy 扁平 fixture 才允许直接挂在 JSON 顶层。
- `planned_*` 和 `actualized_*` 同时保留，能显著降低后续返工时“到底是计划错了还是执行偏了”的诊断成本。
- 先提纯 delta，再回写 truth；如果一上来就直接改卡或改 MAP，几乎一定会把证据链弄脏。
- 模板里声明了 `refresh_mode`，脚本就必须真的消费；否则这不是“兼容保守实现”，而是模板和执行器双真源漂移。
- 对 loopback 这类“validated truth writeback”阶段，revision 不是可选装饰，而是防止旧 delta 覆盖新 truth 的最低成本护栏。
- 白名单规则最该拦的不是“字段拼错”，而是“把不属于 validated actualization 的内容伪装成 delta”；一旦让 `review_* / planned_* / source-fix` 漏进去，truth split 就失效了。
- 多目标 actualization 最稳的做法不是“按顺序写”，而是“按顺序 commit”；顺序只定义提交次序，不等于允许中途留下半成品。
- rollback 只能处理可捕获异常，不能处理进程崩溃；因此 pending marker 不是多余信息，而是 crash 之后唯一能被 resume/query 看到的提交期证据。
- stage 合同里写的主干步骤必须和 `workflow_manager.py` 的 tracked steps 对齐，否则 `resume/` 很快会把 loopback 当成另一套流程来解释。
- 只要 actualization 规则同时牵涉 `Cards`、`MAP` 和卫星路由，就应用“共享 spec + 输出模板”双锚维护，避免边界只存在于某个阶段说明里。
- 当某个 stage 从“说明层”升级为“正式执行层”时，不能只改 `SKILL.md`；至少要同时落地脚本入口、统一 CLI 转发和一组最小回归测试，否则 stage 会停留在文档存在、系统缺席的伪完成态。
- 当 `5-Loopback` 的卫星拓扑发生增删时，必须同步清理技能目录、CLI、workflow registry、调用矩阵和测试；否则回环拓扑会留下伪节点。
- writeback 产物若不能回指到同一 `<run_id>` 的 PASS 证据层，后续 query/audit 很快会退化成“知道写了什么，不知道凭什么能写”。
