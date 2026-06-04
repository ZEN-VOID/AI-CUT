# CONTEXT.md

## Purpose & Loading Contract

本文件是 `aigc-workflow-sword10` 的经验层知识库，不是第二份执行合同。调用 `$aigc-workflow-sword10` 时，它必须与同目录 `SKILL.md` 一起加载，用于识别 subagent 编排、阶段交接、批处理续跑和上下文过载风险。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-orchestrator-heuristics-only

## Type Map

| type_id | symptom | likely root layer | immediate fix | verification |
| --- | --- | --- | --- | --- |
| `SWORD10-TM-01` | 主窗口开始写 2-10 主链阶段正文、风格协议或分组稿 | authorship boundary | 停止正文生成，只派发阶段 subagent | ledger 中只有 dispatch/gate，不含大段正文 |
| `SWORD10-TM-02` | 一个 subagent 同时处理多集导致上下文过载 | concurrency boundary | 改回一集一个 subagent | dispatch packet 每集一份 |
| `SWORD10-TM-03` | 下游阶段在上一阶段未全通过或缺少 `3-美学` 必需协议时启动 | stage merge gate | 回到阶段汇流门，先补齐失败集或补齐协议 | stage ledger 显示上一阶段全 pass |
| `SWORD10-TM-04` | 失败后从下游继续跑，造成平行真源 | handoff source | 从失败阶段或 owning stage 续跑 | retry packet 指向 owning stage |
| `SWORD10-TM-05` | subagent runtime 不可用却被描述成已后台运行 | runtime honesty | 输出 `degraded-subagent-unavailable` 并停止 | report 记录 blocking_layer 与 missing_runtime |

## Repair Playbook

1. 先确认目标是 `2-编剧 -> 3-美学 -> 4-导演 -> 5-表演 -> 6-氛围 -> 7-分镜 -> 8-摄影 -> 9-光影 -> 10-分组`，不要把 `11-主体` 之后的生成链路塞进 `sword10`。
2. 先锁项目根和集数，再决定 `bounded_episode_chain`、`episode_batch_chain` 或 `retry_from_stage`。
3. 每阶段先生成 dispatch packet，再启动 subagent；不要让 subagent 自己猜项目、集数或输出路径。
4. 阶段内允许并发，阶段间必须串行；上一阶段未全通过，不触发下一阶段。
5. 失败时保留成功分集的 canonical 产物，但 completion report 必须清楚标记未完成范围。
6. 若主窗口上下文已经接近过载，只保留路径、verdict、失败码和下一阶段触发条件，不回读完整正文。

## Reusable Heuristics

- `sword10` 的价值是把 2-10 主链阶段变成可追踪的后台批处理链，而不是新增一份创作真源。
- “一集一个 subagent”比“一个阶段一个 subagent 批量处理所有集”更稳定，因为每集能携带独立上下文、输出路径和失败状态。
- 阶段汇流门要比单个 subagent 成功更强：只有目标集全集通过，默认才进入下一阶段。
- 续跑时最重要的是 `start_stage` 和已有产物可信度；不可信的中间产物应回到 owning stage，而不是从下游补洞。
- 主窗口状态汇总应短：项目、集数、当前阶段、通过数、失败数、下一动作，避免把后台正文带回主上下文。
