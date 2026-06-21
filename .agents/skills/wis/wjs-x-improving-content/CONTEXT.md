# Context: wjs-x-improving-content

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 1693
current_lines: 41
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-x-improving-content` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

- 把 prompt 版本差异当强因果：单篇文章/话题主导 impression，prompt 只是二阶因素。修复时分开看版本中位数和内容特征，把内容特征作为下一版 prompt 的主要抓手。
- 样本未成熟就下判决：发布不足 3 天或每版少于 5 条成熟推时，结论噪声太大。修复时保持 measuring，不做 keep/rollback。
- 一次实验改多处 prompt：同时改长度、角度、开头和语气会无法归因。修复时只做一个可证伪改动，并用 `ledger.py register` 写清假设。
- 数据来源不稳：依赖 X API 直接拿 impression 容易失败或字段不全。修复时用 Content CSV 导出，经 `ingest-tweets.py` 与发推历史 join。
- 版本归因手填出错：手动给推标 prompt 版本容易漏历史。修复时按推发布时间 T，取 `prompts/x/prompt.md` 在 T 之前的最后一次 git 提交 short-SHA。
- 回滚未确认：prompt 回滚会影响后续 6h Action。修复时先问王建硕，确认后再 checkout 旧 SHA、commit，并登记 rollback。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认本轮是吃数据、分析内容特征、改 prompt、评估版本还是生成看板。
2. 有 Content CSV 时先运行 ingest，把 `tweet_id`、发推历史、`prompt_sha`、`char_len`、`mature` 写入 `state/tweets.jsonl`。
3. 先跑内容特征分析，再决定 prompt 改动；不要先凭直觉改 prompt。
4. prompt 改动必须一版一个假设，commit 后用 short-SHA 登记到 ledger。
5. 版本评估只看成熟推的中位 impression；样本不足显示 measuring，超过阈值再 keep/rollback/flat。
6. 回滚前先征得确认；执行后同步 ledger，并用 scoreboard 汇总当前状态和下一步。

## Reusable Heuristics

- North-star 是每条推的 impression，但 prompt 版本对比只给方向，真正能改 prompt 的是 angle、长度、钩子和话题等内容特征。
- 判决用中位数不用均值；长尾爆款会让均值误导版本选择。
- 成熟窗默认 3 天，版本判决默认至少 5 条成熟推，keep/rollback 阈值默认 ±10%。
- `prompt_sha` 由 git 历史和发布时间推导，不需要改发推 Action。
- `state/SCOREBOARD.md` 是给用户看的汇总层；`tweets.jsonl` 和 `versions.jsonl` 承载可追溯事实。

## Promotion Backlog

- 增加 CSV schema preflight：检查 `Post id`、`Impressions`、互动字段和日期字段是否可解析。
- 在 `evaluate.py` 输出中更醒目标注 measuring 原因：成熟窗不足、样本数不足或无前序版本。
- 增加实验模板，强制记录“改动点 / 假设 / 预期影响的内容特征 / 何时评估”。
- 增加 scoreboard 的 next action 区块，把内容特征发现直接映射到下一版 prompt 候选改动。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
