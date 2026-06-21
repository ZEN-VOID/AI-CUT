# Context: wjs-cleaning-spam

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2171
current_lines: 41
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-cleaning-spam` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 用户说“删除 spam”但 API 实际不能删除别人的回复 | 平台能力边界 | 明确执行语义是 hide reply + mute author，block 只能网页手动 | 汇报中固定区分 hidden、muted、block-manual | spam 回复在评论区访客不可见，账号已静音 |
| recent-search 找不到旧 spam | X API 窗口限制 | 告知 recent-search 只覆盖最近 7 天，更早需网页手动 | 运行前先确认清理范围是否在 7 天内 | dry-run 结果覆盖目标时间窗内回复 |
| raw query 返回 401 被误判为认证失败 | 查询编码层 | 检查 `to:jianshuo` 等 query 参数是否 URL 编码 | 把查询编码视为第一排查点，避免盲目更换 token | 编码后 dry-run 能返回候选回复 |
| block API 反复失败 | 平台端点下线 | 停止尝试 block，改为 mute，并提醒网页手动 block | 不把 block 纳入自动化完成条件 | apply 汇总中只承诺 hide/mute 结果 |
| hide 返回 Invalid Request | 权限边界 | 记录 hide-failed；若作者是 spam 仍执行 mute | 先判断回复所在根推文是否属于用户本人 | 汇总列出 hide 失败原因和 mute 成功数 |
| hide 返回 429 限流 | API 限流 | 等约 15 分钟后重跑同一命令 | 依赖 `state/cleaned.jsonl` 幂等跳过已处理 id | 重跑后已处理 id 不重复处理，新 id 继续 apply |
| 纯文本同城话术漏网 | 启发式覆盖不足 | 增补隐形字符或话术特征到检测规则 | 新变体必须有样本证据，优先补 `NAME_KW` / `INVISIBLE` | dry-run 能把新变体归入 flagged 或 borderline |
| 真人短评被扫入 spam | 误伤风险 | borderline 必须逐条人审；真人评论即使难听也不动 | flagged/borderline 分层处理，不把启发式结果直接全量 apply | apply id 集合只包含确认 spam |

## Repair Playbook

1. 先 dry-run：拿到 flagged 与 borderline 两个名单，不直接 apply 未审过的 borderline。
2. 审 borderline：按用户名装饰、同城话术、隐形字符、纯 emoji 等证据判断；真人评论不处理。
3. 执行上限动作：对确认 spam 做 hide reply + mute author；不要承诺 API 删除或 API block。
4. 处理失败分支：401 先查 query 编码；Invalid Request 记 hide-failed；429 等窗口刷新后幂等续跑。
5. 汇报闭环：向用户列出隐藏几条、失败几条及原因、静音几个账号，并说明 block 需网页手动。
6. 经验沉淀：只有反复出现的新 spam 话术、隐形字符或误伤模式，才写入本文件或晋升脚本规则。

## Reusable Heuristics

- “删掉 spam”在本技能中等价于 hide + mute；不要把平台不支持的 delete/block 当作完成条件。
- flagged 可自动处理；borderline 是误伤缓冲区，必须由 Claude 逐条确认后再并入 apply id 列表。
- 同城引流 spam 的强信号通常是装饰性昵称、同城/上门/破处等话术、隐形字符夹杂和纯 emoji 回复。
- 429 不是失败终局；`state/cleaned.jsonl` 是续跑锚点，等待限流窗口后重跑即可。
- hide 权限跟串主有关；用户参与别人的串时不能隐藏该串回复，但仍可静音 spam 账号。
- 新启发式要服务“减少漏网且不误伤真人”，不能为了清干净而吞掉真实互动。

## Promotion Backlog

- 若同一新 spam 变体重复出现，并有 dry-run 证据，可晋升到脚本的关键词或隐形字符检测。
- 若 429 续跑频繁打断任务，可考虑让脚本在汇总中输出下一次建议重跑时间。
- 若用户经常要求拉黑，可在汇报模板中固定加入网页手动 block 路径，但不改变 API 自动化边界。
