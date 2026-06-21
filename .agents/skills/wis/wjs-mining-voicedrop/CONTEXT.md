# Context: wjs-mining-voicedrop

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2259
current_lines: 42
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-mining-voicedrop` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 收件箱 `list` 非零退出 | 前置环境/网络层 | 停止批处理，报告收件箱不可达或 `FILES_TOKEN` 失效 | 每批开始先载入 `~/code/.env` 并验证 list，不进入下载/删除循环 | 没有任何 R2 文件被删除，错误原因已报告 |
| 收件箱为空 | 正常空队列 | 报告没有新录音并结束 | 把空结果视为成功 no-op，不制造占位产物 | 批次报告显示处理 0 条、剩余 0 条或实际剩余数 |
| 使用相对路径调用 inbox 脚本导致换目录失败 | 执行入口层 | 改用绝对路径 `$INBOX` 调 `voicedrop-inbox.sh` | 不依赖当前工作目录；脚本定位在 Step 0 完成 | 任意 cwd 下都能 list/download/delete |
| 桶里出现非 `VoiceDrop-*.m4a` 文件 | 输入归属层 | 不处理、不删除，报告为非本技能认领对象 | list/循环只认 `VoiceDrop-` 前缀和 `.m4a` 后缀 | 非 VoiceDrop 文件仍保留在 R2 |
| 下载后发现音频损坏或时长 `< 1.0` 秒 | 输入质量层 | 跳过该条，记录原因，不转写、不删除 | 每条先 download 存档，再用 `ffprobe` 做真实性检查 | 本地 archive 有原文件，R2 仍保留该对象 |
| 转写失败、用户未通过选题闸或没有产出草稿 | 下游复用/完成门禁层 | 记录单条失败并继续下一条；该条绝不 delete | 删除 gate 固定为“已存档 + 已转写 + 已挖文 + 至少一篇草稿 + 用户未中止” | R2 中失败条目仍存在，批次报告列出原因 |
| 并行处理多条导致删除状态混乱 | 批处理编排层 | 改为串行逐条闭环，一条完成后再下一条 | 删除安全依赖单条成功，不把批次整体成功当作删除条件 | 每条都有独立处理结果和删除状态 |
| 本技能重写转写或成文逻辑 | 复用边界层 | 回到 `wjs-transcribing-audio` 与 `wjs-mining-articles`，本技能只做 inbox 编排 | Skill 合同中保持“复用，不重写”；下游人工选题闸必须照走 | 输出草稿来自 `wjs-mining-articles` 流程，SRT 来自转写技能 |

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认本轮是处理 R2 收件箱里的 `VoiceDrop-*.m4a`，不是本地散文件或已有 SRT。
2. Step 0 固定载入 `~/code/.env`，用绝对路径定位 inbox 脚本；缺 token 或网络失败时停止。
3. Step 1 只列本批未处理文件；空收件箱是正常结束，不创建伪任务。
4. Step 2 串行逐条执行：download 到 archive -> `ffprobe` 检查 -> 转写为 SRT -> 交给 `wjs-mining-articles` 走选题闸和成文 -> 成功后 delete。
5. 任一单条失败只影响该条：记录原因、保留 R2、继续下一条。
6. 批次结束报告必须覆盖处理条数、每条草稿数、archive 路径、跳过/失败原因、R2 剩余。
7. 若需要沉淀新经验，只记录可复用的 gate、失败类型或路由边界，不写一次性录音内容。

## Reusable Heuristics

- R2 是未处理队列，本地 archive 是处理后仍可追溯的音频真源；删除只表示该条已经闭环。
- “没成功就不删”比“批次尽量清空”优先级更高；宁可留下一条待处理，也不能丢录音。
- VoiceDrop 文件名里的时间、星期、时段、地点是成文上下文线索，不是替代转写内容的事实真源。
- 短录音常只有一个选题，但 `wjs-mining-articles` 的人工选题闸仍然要走，不能由本技能跳过。
- 批处理要有韧性：单条失败不该中断整批，也不该触发该条删除。
- 本技能的核心价值是 inbox lifecycle 和逐条编排；转写质量、文章挖掘质量分别回到对应下游技能治理。

## Promotion Backlog

- 可沉淀批次报告模板，固定列出 `processed / drafted / skipped / failed / remaining`，方便用户快速确认收件箱状态。
- 如果误传或极短音频频繁出现，考虑把时长阈值和跳过原因固化为脚本 dry-run 输出。
- 若 R2 文件量变大，再评估 manifest 或 per-item state 文件；在删除安全不受影响前，不引入并行删除。
