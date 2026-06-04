# Type Map

`sword10` 的类型包用于决定分集集合规模和续跑策略。执行时先选择类型包，再回到 `SKILL.md#Thinking-Action Node Map`。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `bounded_episode_chain` | `types/bounded-episode-chain/` | 单集、少量明确集数、从 2 到 10 完整推进 | exclusive | `types/bounded-episode-chain/bounded-episode-chain.md` | `episode_batch_chain` | none |
| `episode_batch_chain` | `types/episode-batch-chain/` | 多集批处理、范围集数、每阶段多 subagents | exclusive | `types/episode-batch-chain/episode-batch-chain.md` | `bounded_episode_chain` | none |
| `retry_from_stage` | `types/retry-from-stage/` | 续跑、重试、从某阶段继续、失败集补跑 | stackable | `types/retry-from-stage/retry-from-stage.md` | none | none |

## Selection Rules

1. 明确单集或 1-3 集，默认 `bounded_episode_chain`。
2. 明确连续区间或 4 集以上，默认 `episode_batch_chain`。
3. 用户给出 `start_stage` 不是 `2-编剧`，或存在失败阶段，叠加 `retry_from_stage`。
4. 类型歧义时先阻断澄清，不默认扩大批量范围。

## Default Package Rule

未显式指定类型时：

1. 单集或 1-3 集默认加载 `bounded_episode_chain`。
2. 4 集以上或连续区间默认加载 `episode_batch_chain`。
3. 任意续跑、失败补跑或非 `2-编剧` 起步，叠加加载 `retry_from_stage`。

## Loading Flow

1. 读取用户请求，解析项目根、分集集合、`start_stage` 和 `end_stage`。
2. 按 `Package Index` 选择一个主类型包。
3. 如存在续跑信号，叠加 `retry_from_stage`。
4. 将类型包固定上下文交给 `SKILL.md#Thinking-Action Node Map`。
5. 最终由 `review/review-contract.md` 检查类型选择是否匹配实际运行模式。
