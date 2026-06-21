# Context: wjs-tweeting-from-articles

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2947
current_lines: 101
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-tweeting-from-articles` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

### source-detached-tweet

- 症状：候选 tweet 像重新构思的观点，找不到对应 `article.md` 句段。
- 根因层：违反“文章是源头，tweet 只是再短一格”的核心原则。
- 立即修复：回到文章，直接挑最 quotable 的一句/一段，再按 X 节奏切短。
- 系统预防：每条候选都能回指文章里的原句或明确段落。
- 验证点：候选不是凭空新写，且保留王建硕原文语气。

### duplicate-article-posted

- 症状：同一篇文章被重复发推，或最近 7 天都发过还继续硬选。
- 根因层：没有先读取 `state/history.jsonl` 或跳过 `pick-next-article.sh` 的未推过滤。
- 立即修复：先挑最新未推文章；若全推过，告诉用户今天 rest day。用户显式指定时再例外处理。
- 系统预防：成功发布后必须写 history，作为下一次去重真源。
- 验证点：history 中 article slug 与 tweet_id 对应，状态为 `posted`。

### overlength-or-no-buffer

- 症状：tweet 超过 X 限制，或中文接近 140 字导致发布失败风险高。
- 根因层：忽略中文字符按 2 计和“留 buffer 到 120 字以内”的合同。
- 立即修复：压到 120 个中文字符以内，保留最有力的一句。
- 系统预防：候选展示前先做长度检查。
- 验证点：每条候选都小于 280 字符，中文优先小于 120 字。

### style-drift-marketing

- 症状：加 hashtag、@、emoji、mp.weixin 链接，或写成营销腔。
- 根因层：风格约束没有执行。
- 立即修复：去掉 hashtag、@、emoji 和默认链接；链接如需保留，建议放 reply。
- 系统预防：候选生成后用“平实、家常比喻、不营销”过滤一遍。
- 验证点：tweet 像从文章里抠出来的短句，而不是推广文案。

### user-choice-skipped

- 症状：生成 A/B/C 后直接发布，或三条都发。
- 根因层：Step 3 的用户选择 gate 被跳过。
- 立即修复：用 A 金句、B 比喻、C 反差三条候选让用户选；不选就不发。
- 系统预防：真发前必须有用户确认，dry-run 只给草稿。
- 验证点：发布的文本能对应用户选择的 angle 或 `other`。

### xurl-response-parse-failure

- 症状：`jq -r '.data.id'` 因返回 text 中 raw newline 报 control character 错，导致误判发布失败。
- 根因层：发布步骤没有采用技能合同指定的 id 提取方式。
- 立即修复：从原始响应中用 grep 提取 `"id":"[0-9]+"`；失败时把原响应给用户重试。
- 系统预防：不要在该步骤改回严格 jq 解析 id。
- 验证点：成功时能输出 `https://x.com/jianshuo/status/<tweet_id>`。

### history-write-missing

- 症状：tweet 已发出，但下一次仍认为该文章未推。
- 根因层：Step 5 未写 `state/history.jsonl`。
- 立即修复：补写 date、slug、angle、tweet_id、text、status。
- 系统预防：发布成功与 history 写入视为同一个收尾动作。
- 验证点：最终汇报包含 tweet URL、文章 slug、angle 和 history 已写入。

### batch-mode-flood-risk

- 症状：一次要发多篇文章时逐篇人工选三条或连续发送，触发刷屏风险。
- 根因层：没有切换到批量排期模式。
- 立即修复：为每篇挑一条最 quotable 的短 tweet，生成队列并按 `MIN_GAP` 节流发布。
- 系统预防：多篇文章默认走 queue、cursor、last-post-epoch 和单机锁。
- 验证点：首条可 FORCE 验证，后续由 cron/脚本节流，失败不推进 cursor。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认入口、路由、输出合同和门禁。
2. 判断任务是否属于“从最近公众号文章发一条 X”；无关内容或产品推广不要走本技能。
3. 默认用 `pick-next-article.sh` 找最近 7 天未推文章；用户指定 folder 时才跳过自动选择。
4. 读取 `<folder>/article.md`，按 A 金句、B 比喻、C 反差各起草一条，先检查长度和风格。
5. 让用户在 A/B/C/其他中选择；未确认不发布，`--dry-run` 也不发布。
6. 真发时用 `xurl POST /2/tweets`，按合同从原始响应 grep tweet id，失败则保留原文响应给用户。
7. 发布成功后立即写 `history.jsonl`，再汇报 URL、slug、angle 和 history 状态。
8. 一次处理多篇时切换批量排期：队列、cursor、last-post-epoch、单机锁和自动清理 cron 都要保持一致。

## Reusable Heuristics

- 本技能的创作边界很窄：不是写新观点，而是把已发表文章再短一格。
- 三个 angle 是选择框架，不是三条都要发布；一天最多一条，一篇文章默认只推一次。
- 中文 tweet 宁短不满格；120 字以内通常比贴近 140 字更稳。
- 默认不带公众号链接；如果用户需要链接，优先建议放在 reply。
- history 是去重真源，发布成功但不写 history 等于状态损坏。
- 批量排期时“失败不推进 cursor”比“尽快发完”重要，避免漏发和刷屏。

## Promotion Backlog

- 若长度超限反复出现，考虑增加候选展示前的字符计数 helper。
- 若风格漂移反复出现，考虑增加 hashtag/@/emoji/mp.weixin 默认拦截检查。
- 若 history 漏写反复出现，考虑把发布与 history 写入包装成单个脚本事务。
- 若 xurl 响应解析问题复发，考虑把 grep id 提取封装进脚本，避免临场写错。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
