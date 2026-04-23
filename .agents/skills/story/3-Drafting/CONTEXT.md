# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按“单章父流程 + 上一章阻塞下一章”运行 drafting | stage topology | 把父层切回卷级 orchestrator，并把上一章终稿降为增强输入 | 固定“卷级父流程、章级 worker、worker 内串行”的执行合同 | 卷内 10 章可以启动并发 worker，而不是排队等全文 |
| 卷内并发名义存在，但实际没有真实 subagent/worker dispatch | execution mode governance | 在批次日志中明确记录真实启动的 worker 与监制 | 将 `team.yaml + 卷级日志 + 真实 dispatch` 绑定为同一治理链 | 能说明每一章由哪个 worker 执行、由谁监制 |
| volume continuity 仍靠临场总结上一章，而不是规划 truth | continuity contract | 优先从卷地图 continuity pack 装配当前章入口状态 | 把“planning continuity pack 为硬输入、上一章正文为增强输入”写死 | 前序集未完成时，当前章仍有稳定起盘依据 |
| worker 内把 1-8 又合成一次大改稿 | step gate | 回到“一 step 一写回一 hook” | 在 child output contract 与卷级日志中固定 step 粒度 | 每个 worker 的 step history 完整可追 |
| 卷内某一集阻塞后，整卷无差别停摆 | orchestration routing | 只阻断受影响 worker，并显式标记波及范围 | 在卷级日志中记录 `block_reason / affected_workers` | 非受影响 worker 仍可继续推进 |
| 卷内前序集实际正文与 planning continuity pack 偏离，但后续 worker 没有 re-sync | intra-volume drift | 对受影响 worker 触发 targeted re-sync，而不是全卷重来 | 将 `actual delta -> continuity refresh` 作为卷级日志中的显式动作 | 能指出哪几集需要重读新完成的前序正文 |
| 正文只是压缩剧情稿，却因 hook 与 ledger 齐全被误判为 `candidate_final_draft` | manuscript completeness gate | 回退该章正文，补到章节级完整度，再重跑收口 | 在 `3-Drafting` completion gate 与 `workflow_manager.complete_task` 之间增加 `drafting_manuscript_guard.py` | 正文过短、段落过稀或缺失 exit hook 时无法完成 `story-write` |
| 卷一整卷可读但平庸，像稳定推进的 dossier，而不是有后劲的小说 | volume quality gate missing | 先做卷级会审并把结论压成 `quality_gate_snapshot`，再决定返工或终验 | 在 `3-Drafting` handoff 前增加 `drafting_volume_quality_guard.py + quality_gate_snapshot`，让 runtime 能识别“先返工再 validation” | `candidate_volume_draft` 不再天然等于 `ready-for-validation` |
| 明确命中 `正文/` child 时，仍只读取 planning 而没有加载 `全局卡 / 风格卡 / north_star / 项目 CONTEXT / 上一章正文` | chapter-native lane contract | 回到 `正文/SKILL.md` 组装完整 context pack，再重写本章 | 在父层 `3-Drafting/SKILL.md` 与 `正文/SKILL.md` 同步固定 chapter-native 加载清单 | `第N卷/第N章.md` 的 YAML 头能追溯这些来源 |
| 明确命中 `正文/` child 时，正文仍落到平铺 `3-Drafting/第N章.md`、`正文/` 或临时 sibling 文件 | chapter-native runtime drift | 改回 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md` | 在父层合同、child 合同与 registry 路由同时固定输出路径 | chapter-native 直写不会误落旧路径 |
| 明确命中 `正文/` child 时，执行上仍由本地 GPT 会话直接出稿，没有真实调用豆包 provider | chapter-native provider drift | 回到 `正文/scripts/write_chapter_via_doubao.py` 的桥接路径，补齐 provider 调用与结果校验 | 在父层与 child 合同中同步固定“actual creative step = doubao-seed-2.0-pro” | chapter-native 执行能留下 provider artifacts 与正式写回的同轮证据 |

## Repair Playbook

1. 先判断问题出在卷级调度、worker 串行、continuity pack，还是上游 source truth。
2. 若并发失效，先查 `team.yaml`、卷级日志和 dispatch 证据，不先查 prose。
3. 若 continuity 漂移，先比对卷地图入口状态与已完成前序正文，再决定是 re-sync 还是 source fix。
4. 若问题只影响单一章节，不要把整卷一起打回。
5. 收尾时同时核对：卷级日志、受影响 `第N章.md`、当前卷 `卷规划.md / 第N章.md`，兼容项目再补读卷分片投影。
6. 若正文“看起来能读”但不像完整章节，优先怀疑 `candidate_final_draft` gate 过松；先跑 `scripts/drafting_manuscript_guard.py`，再决定是否回退到 `Step 1` 或 `Step 8`。
7. 若整卷“什么都对，但就是不够好看”，优先怀疑缺的是卷级质量闸门，而不是继续让 `4-Validation` 替 `3-Drafting` 兜底；先写 `quality_gate_snapshot`，再跑 `scripts/drafting_volume_quality_guard.py`。

## Reusable Heuristics

- 卷级 drafting 的核心不是“同时生成 10 章”，而是“让 10 个 worker 共享同一卷地图与监制纪律”。
- 真正阻塞并发的往往不是文笔，而是把上一章正文误写成硬前置依赖。
- 对卷内连续性来说，规划层的 `entry_state / expected_exit_delta` 比事后总结上一章更适合做并发开工输入。
- 卷级父层最重要的不是替 worker 写稿，而是保证谁能并发、谁该等待、谁需要 re-sync。
- 单 worker 串行、跨 worker 并发，是这个阶段最容易被说错也最容易漂移的边界。
- 对 `3-Drafting` 来说，“短稿”与“平稿”是两类不同故障：前者靠正文完整度 guard 拦，后者必须靠卷级质量闸门拦。
- 会审结论只有落进写作日志，才算 runtime 可消费的真源；只停在聊天里，resume 很容易继续错判下一入口。
