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
| 仍按“单集父流程 + 上一集阻塞下一集”运行 drafting | stage topology | 把父层切回卷级 orchestrator，并把上一集终稿降为增强输入 | 固定“卷级父流程、集级 worker、worker 内串行”的执行合同 | 卷内 10 集可以启动并发 worker，而不是排队等全文 |
| 卷内并发名义存在，但实际没有真实 subagent/worker dispatch | execution mode governance | 在批次日志中明确记录真实启动的 worker 与监制 | 将 `team.yaml + 卷级日志 + 真实 dispatch` 绑定为同一治理链 | 能说明每一集由哪个 worker 执行、由谁监制 |
| volume continuity 仍靠临场总结上一集，而不是规划 truth | continuity contract | 优先从卷地图 continuity pack 装配当前集入口状态 | 把“planning continuity pack 为硬输入、上一集正文为增强输入”写死 | 前序集未完成时，当前集仍有稳定起盘依据 |
| worker 内把 1-8 又合成一次大改稿 | step gate | 回到“一 step 一写回一 hook” | 在 child output contract 与卷级日志中固定 step 粒度 | 每个 worker 的 step history 完整可追 |
| 卷内某一集阻塞后，整卷无差别停摆 | orchestration routing | 只阻断受影响 worker，并显式标记波及范围 | 在卷级日志中记录 `block_reason / affected_workers` | 非受影响 worker 仍可继续推进 |
| 卷内前序集实际正文与 planning continuity pack 偏离，但后续 worker 没有 re-sync | intra-volume drift | 对受影响 worker 触发 targeted re-sync，而不是全卷重来 | 将 `actual delta -> continuity refresh` 作为卷级日志中的显式动作 | 能指出哪几集需要重读新完成的前序正文 |

## Repair Playbook

1. 先判断问题出在卷级调度、worker 串行、continuity pack，还是上游 source truth。
2. 若并发失效，先查 `team.yaml`、卷级日志和 dispatch 证据，不先查 prose。
3. 若 continuity 漂移，先比对卷地图入口状态与已完成前序正文，再决定是 re-sync 还是 source fix。
4. 若问题只影响单一章节，不要把整卷一起打回。
5. 收尾时同时核对：卷级日志、受影响 `第N集.md`、卷分片 planning truth。

## Reusable Heuristics

- 卷级 drafting 的核心不是“同时生成 10 集”，而是“让 10 个 worker 共享同一卷地图与监制纪律”。
- 真正阻塞并发的往往不是文笔，而是把上一集正文误写成硬前置依赖。
- 对卷内连续性来说，规划层的 `entry_state / expected_exit_delta` 比事后总结上一集更适合做并发开工输入。
- 卷级父层最重要的不是替 worker 写稿，而是保证谁能并发、谁该等待、谁需要 re-sync。
- 单 worker 串行、跨 worker 并发，是这个阶段最容易被说错也最容易漂移的边界。
