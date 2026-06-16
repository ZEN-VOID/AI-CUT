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
| `SWORD10-TM-01` | 主窗口开始写 2-8 主链阶段正文、风格协议、主体注册表或分组稿 | authorship boundary | 停止正文生成，只派发阶段 subagent | ledger 中只有 dispatch/gate，不含大段正文 |
| `SWORD10-TM-02` | 一个 subagent 同时处理多集导致上下文过载 | concurrency boundary | 改回一集一个 subagent | dispatch packet 每集一份 |
| `SWORD10-TM-03` | 下游阶段在上一阶段未全通过或缺少 `2-美学` 必需协议时启动 | stage merge gate | 回到阶段汇流门，先补齐失败集或补齐协议 | stage ledger 显示上一阶段全 pass |
| `SWORD10-TM-04` | 失败后从下游继续跑，造成平行真源 | handoff source | 从失败阶段或 owning stage 续跑 | retry packet 指向 owning stage |
| `SWORD10-TM-05` | subagent runtime 不可用却被描述成已后台运行 | runtime honesty | 输出 `degraded-subagent-unavailable` 并停止 | report 记录 blocking_layer 与 missing_runtime |
| `SWORD10-TM-06` | 主窗口、脚本或模板开始生成阶段正文 | scripted stage body | 标记 `FAIL-SWORD10-SCRIPTED-STAGE-BODY`，停止并回 owning stage subagent | dispatch packet 指向阶段技能，主窗口只记录路径/verdict |

## Repair Playbook

1. 先确认目标是 `2-美学 -> 3-主体 -> 4-编剧 -> 5-导演 -> 6-分镜 -> 7-摄影 -> 8-分组`，不要把 `3-主体` 之后的生成链路塞进 `sword10`。
2. 先锁项目根和集数，再决定 `bounded_episode_chain`、`episode_batch_chain` 或 `retry_from_stage`。
3. 每阶段先生成 dispatch packet，再启动 subagent；不要让 subagent 自己猜项目、集数或输出路径。
4. 阶段内允许并发，阶段间必须串行；上一阶段未全通过，不触发下一阶段。
5. 失败时保留成功分集的 canonical 产物，但 completion report 必须清楚标记未完成范围。
6. 若主窗口上下文已经接近过载，只保留路径、verdict、失败码和下一阶段触发条件，不回读完整正文。
7. 任何阶段正文、风格协议、分镜/摄影/分组稿都不能由 workflow 脚本或 completion report 补写；只能由 owning stage subagent 生成。

## Reusable Heuristics

- `sword10` 的价值是把 2-8 主链阶段变成可追踪的后台批处理链，而不是新增一份创作真源。
- “一集一个 subagent”比“一个阶段一个 subagent 批量处理所有集”更稳定，因为每集能携带独立上下文、输出路径和失败状态。
- 阶段汇流门要比单个 subagent 成功更强：只有目标集全集通过，默认才进入下一阶段。
- 续跑时最重要的是 `start_stage` 和已有产物可信度；不可信的中间产物应回到 owning stage，而不是从下游补洞。
- 主窗口状态汇总应短：项目、集数、当前阶段、通过数、失败数、下一动作，避免把后台正文带回主上下文。
- `sword10` 的形式指标是 orchestration 指标；不能用 ledger、dispatch packet 或 completion report 的字段完整性替代阶段正文的 LLM-first 验收。
