# Context: wjs-x-increasing-follower

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2931
current_lines: 56
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-x-increasing-follower` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 试图用 X API / xurl 读取主页访问和新增关注 ratio | data-source boundary | 要求用户从 X Analytics 导出 CSV 并放入 `inbox/` 或提供路径 | 把 CSV 导出作为每日检查前置条件 | `daily.jsonl` 中有 `profile_visits / new_follows / ratio` |
| 把单账号 profile 改动当成真正平行 A/B 测试 | experiment design | 改为时间轴前后对比，并记录 applied 前 baseline | 菜单和账本都避免宣称因果，只给方向性结论 | `actions.jsonl` 有编号、假设、metric、before、applied |
| 用 impressions 或粉丝总数评估 bio/name/banner 改动 | metric mapping | profile 类实验统一考核 ratio | 新实验必须声明 category 与 metric，且与杠杆匹配 | profile action 的 `metric=ratio` |
| 爆款当天拉高均值，被误判为实验成功 | evaluation honesty | 用中位数、7 天窗口和最少 post 数据门槛 | 保留 `thin baseline` / `confounded` 标记，不强判 | `evaluate.py` 输出方向性 verdict 而非因果断言 |
| 同一指标多个实验窗口重叠，结果互相污染 | confounding control | 减少同时运行的 profile 实验，必要时延长窗口或暂停重叠项 | To-do 菜单控制并发，scoreboard 显示 confounded | 重叠实验被标记，未被当作干净结论 |
| 判定 rollback 后静默还原 bio 或头像 | consent gate | 先把 rollback 建议发给王建硕确认 | 回滚永远是一等人工决策，不由 daily-check 自动执行 | 只有确认后才调用 API 或手改并 `ledger.py rollback` |
| 上线实验前没有抓 before，导致无法回滚 | rollback readiness | 先用 profile API 或手工记录 before，再 `ledger.py apply` | apply 前检查至少一个 before 字段 | rollback 命令能打印可还原的 before 值 |
| 手工修改头像/banner/置顶推后未记账 | state drift | 仍然用 ledger 记录 before/after 和 applied 日期 | 对 API 不支持的字段也按实验账本管理 | `actions.jsonl` 反映真实线上状态 |
| CSV 列名识别错，ratio 计算失真 | ingestion mapping | 查看 ingest 打印的列映射，不对就传 `--visits-col / --follows-col` | 每次新来源 CSV 先人工确认列映射 | `daily.jsonl` 日期和数值与 CSV 对得上 |

## Repair Playbook

1. 先确认任务是系统性 X 涨粉实验，而不是单条推文创作、skill 推广或文章分发。
2. 要求最新 X Analytics CSV； ingest 后检查列映射和 `daily.jsonl` 日期是否正确。
3. 提实验菜单时每条都必须有编号、category、hypothesis、metric，并避免同时跑太多同指标 profile 实验。
4. 上线 profile 实验前先抓 before-state；API 不支持的头像、banner、置顶推也要手工记录。
5. 每日检查只 ingest、evaluate、刷新 scoreboard 和写方向性 verdict，不直接 keep/rollback。
6. 对 `confounded`、`thin baseline` 或 post 数据不足的实验，延长观察，不给强结论。
7. 需要 rollback 时先征求王建硕确认，再按 before 值还原并更新 ledger。

## Reusable Heuristics

- ratio 是转化地基；先让来访的人愿意关注，再讨论如何扩大访问量。
- 单账号时间序列实验的目标是减少自欺，不是证明因果；所有 verdict 都应保持方向性表述。
- 爆款会污染 impressions 和 visits，但不应直接污染 profile conversion 的判断。
- `state/actions.jsonl` 是实验账本真源，`SCOREBOARD.md` 是给人看的投影；不要手工改投影替代记账。
- “可回滚”取决于 before-state 是否精确；没有 before 的 profile 改动不应轻易上线。
- CSV 手动导出绕不开，自动化只能覆盖 ingest、evaluate 和 scoreboard，不能假装 API 能拿到 ratio。

## Promotion Backlog

- [ ] 候选规则: 为 `ledger.py apply` 增加 profile 类实验 before 字段缺失警告。
  - 证据计数: 0
  - 目标落点: `scripts/ledger.py`
  - 状态: pending
- [ ] 候选规则: 在 `daily-check.sh` 或 scoreboard 中突出“需要人工确认 rollback”的实验清单。
  - 证据计数: 0
  - 目标落点: `scripts/daily-check.sh` / `scripts/scoreboard.py`
  - 状态: pending
- [ ] 候选规则: 为 CSV ingest 增加列映射确认样例，防止 X Analytics 导出格式变化后静默误读。
  - 证据计数: 0
  - 目标落点: `scripts/ingest-csv.py` 或测试样本
  - 状态: pending

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
