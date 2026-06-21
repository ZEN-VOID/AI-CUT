# Context: wjs-syndicating-articles

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2404
current_lines: 44
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-syndicating-articles` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 重复分发同一篇文章到同一平台 | 幂等状态 | 查 `state/history.jsonl`，只补发未成功平台 | 所有发布结果按 `(slug, platform)` 记录，不绕过 `syndicate.sh` | 重跑只处理 failed/queued/缺失项，不重复 posted |
| 某平台凭证缺失或过期导致全流程中断 | 平台隔离 | 该平台降级到 outbox/manual，其他平台继续 | 每个平台独立 try/catch，缺 key 不报错终止 | 汇总表能同时出现 posted 与 queued |
| `--dry-run` 误写真发或 history | 模式分支 | dry-run 只打印 post.txt 和各平台将发内容，不进入真实发布写状态 | dry-run 分支必须在 Step 3 前短路或传 `--dry-run` | history 无新增，平台无真实帖子 |
| 手动平台被默认自动打开浏览器 | 交互边界 | 只有 `--open` 才复制剪贴板并打开网页 | scheduled/default run 只生成 outbox 和通知 | 默认汇总只给 outbox 路径 |
| 文案过长或平台口吻发散 | LLM 文案层 | 抽 ≤120 字核心句/小段 + 软 CTA + 链接 | 一套文案走所有平台，不堆 hashtag/@/emoji | X 280 字符约束内，仍保留王建硕语气 |
| slug 或平台循环手写导致状态漂移 | 脚本边界 | 交给 `syndicate.sh "$FOLDER" "$POST_TXT"` 处理 slug、平台和 history | 不手写平台循环，不自行拼 slug | stdout 平台行和 history slug 一致 |
| 用户指定 `--mark` 但仍继续分发 | 入口短路 | 只执行 history record 后结束 | `--mark <slug> <platform>` 作为 Step 0 hard short-circuit | 对应平台被标记，未产生新 outbox/发布动作 |
| 没有未分发文章 | 文章选择 | 告知今天 rest day，结束 | `pick-next-article.sh` 输出为空即短路 | 不生成空 outbox，不写 history |
| API 平台和 tweeting skill history 冲突 | 跨技能去重 | 让脚本检查 X/tweeting history，必要时 skipped | X 发布必须经脚本统一处理 | 汇总中显示 skipped/posted 原因 |

## Repair Playbook

1. 先判模式：`--mark` 立即记录并结束；`--dry-run` 只草拟；`--open` 只处理手动发布辅助；默认走完整分发。
2. 选文章：显式 folder 直接使用；否则运行 pick-next，空结果就是 rest day。
3. 写核心文案：LLM 读 article/meta，抽 ≤120 字可引用小段，加软 CTA 与文章链接，署名/口吻保持王建硕。
4. 扇出发布：调用 `syndicate.sh`，不要手写平台循环、slug、凭证读取或 history 写入。
5. 解析汇总：用脚本 stdout 平台行和 outbox 路径生成 posted/queued/failed/skipped 表。
6. 手动平台：默认只准备 outbox；只有 `--open` 才复制文案、打开网页并提示用户发布后 `--mark`。
7. 失败处理：单平台失败不阻断其他平台；凭证问题降级 queued，重复发布依赖 history 跳过。

## Reusable Heuristics

- 稳定性高于“全平台一次全成”：一个平台失败只影响该平台，最终汇报要保留每个平台的独立状态。
- 幂等真源是 `state/history.jsonl`；任何人工补发都应通过 `--mark` 回写状态。
- 文案是一套核心文案走天下，不为每个平台临时改写成营销腔。
- 公众号文章分发默认不堆 hashtag、@ 和 emoji；除非原文或用户明确要求。
- 凭证缺失是正常降级路径，不是任务失败；outbox 是无 API 平台和缺凭证平台的共同落点。
- scheduled/default run 不打开浏览器；交互动作必须由 `--open` 显式触发。
- `secrets.json` 只作为本地配置，不应进入报告、outbox 或版本控制。

## Promotion Backlog

- 可增加 post.txt 长度/链接/CTA 检查，避免 X 字符预算或缺链接问题到发布阶段才暴露。
- 可为 outbox 增加 manifest，记录 queued 平台、复制文案、图片路径和待手动标记命令。
- 若同类平台凭证降级频繁出现，可在汇总中输出具体缺失字段，但不得泄露 secret 值。
