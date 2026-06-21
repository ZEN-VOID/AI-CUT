# Context: wjs-promoting-skills

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2499
current_lines: 45
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-promoting-skills` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| `claude`、`xurl` 或 `jq` 缺失 | 运行前置层 | 停止 setup，补齐依赖并确认 `xurl whoami` | `setup.sh` 必须先跑依赖检查，不进入定时安装 | `claude -p` 可用，`xurl whoami` 返回目标账号，`jq` 可执行 |
| X 被重复或过频发布 | 调度 / 节流层 | 检查 `history.jsonl` 和当天 outbox，必要时跳过 | 每天最多 1 条，同一 skill 7 天内不重复推 | 当天 history 至多新增 1 行 |
| Reddit/HN/Discord 被自动真发 | 渠道边界层 | 立即停止自动发布，只保留 outbox 草稿 | X 是唯一真发渠道，社区渠道永远 draft only | `outbox/<date>/` 有草稿文件，无社区 API 发布动作 |
| SKILL.md 未变化却为了发而发 | 内容新鲜度层 | 跳过当天或选择更合适 skill | 轮换逻辑把“最近改动”和“7 天未推”作为选择依据 | 推广文案能指向真实能力或近期差异 |
| 今日 outbox 已存在仍重复生成 | 幂等层 | 退出或覆盖前先让用户确认 | `daily.sh` 把 outbox 已存在视为跳过条件 | 同一天目录不会出现多套互相冲突草稿 |
| X 文案超 280 字或营销腔 | 内容质量层 | 重新生成并压到约束内 | prompt 固定禁止夸张词、火箭 emoji、`AI-powered`、`game-changer` | 文案长度合规，最多 1 个 hashtag，repo URL 单独一行 |
| `claude` 调用受 hooks / memory 干扰 | 执行确定性层 | 改用 `--bare` 生成确定性输出 | headless 生成统一使用 bare 模式，bash 只传 context | 重跑 dry-run 输出结构稳定，无本地 CLAUDE.md 干扰 |
| `state/` 或 `outbox/` 被推到 GitHub | 发布卫生层 | 从提交中移除并补 `.gitignore` | 状态和草稿都是本地运行产物，不随 skill 发布 | `git status` 不把 `state/`、`outbox/` 纳入发布清单 |
| marketplace 研究过旧 | 研究刷新层 | 手动跑 `research-marketplaces.sh` | 每周刷新 research，每月重建老 plan | `state/research.md` 存在且最近刷新，计划不超过 30 天 |

## Repair Playbook

1. 先判断用户要“每日自动推广”还是“一次手动发布”；后者不走本技能的 cron 语义。
2. setup 前确认依赖、账号、公开 repo 和 macOS launchd；任一缺失都不要安装定时器。
3. 每次排障先看 `history.jsonl`、当天 `outbox/` 和 launchd 状态，再看 prompt 或渠道问题。
4. 真发前优先跑 `DRY_RUN=1 daily.sh`，验证 pick、plan、X 文案和社区草稿都能生成。
5. 社区渠道只检查草稿质量，不排查自动发帖 API；自动发社区帖本身就是违背合同。
6. 若文案变模板腔，先修 prompt 的输入证据和禁止词，再考虑改脚本；bash 不负责营销判断。
7. 稳定的质量约束先写回本文件；能机械校验的再晋升到脚本或 smoke test。

## Reusable Heuristics

- 这个技能的核心边界是“Claude 做判断，bash 做调度”；不要把选题、角度、语气规则硬编码进 shell。
- 只有 X 可以真发；Reddit、HN、Discord 的价值是给人工 review 的高质量草稿，而不是自动 cross-post。
- `history.jsonl` 是节流真源；排查重复发布、轮换异常和 skip 行为时先读它。
- 推广角度必须来自被推广 skill 的 `SKILL.md`、最近 diff、plan 和 marketplace research，不凭空写泛泛广告。
- 同一 skill 多次推广时优先轮换“具体问题、反直觉设计、串联工作流、最近更新差异”四类角度。
- 对用户品牌语气的保护优先于增长技巧；实用、具体、不吹牛比高点击词更重要。
- outbox 是人工审阅缓冲区；忙的时候草稿停在那里即可，不需要第二天补发同一批社区帖。

## Promotion Backlog

- 给 `daily-post.md` 输出补机械校验：字符数、URL 单独一行、hashtag 数、禁用词。
- 给 `history.jsonl` 补 JSON schema 或 smoke 检查，防止轮换脚本读到坏状态后重复发布。
- 给 `setup.sh` 增加 launchd 安装后的状态检查提示，减少“以为装上但 4 AM 没跑”的排查成本。
- 为 `DRY_RUN=1 daily.sh` 固化一条验收样例：必须生成 X 文案和 4 个 outbox markdown，且不调用 X POST。
