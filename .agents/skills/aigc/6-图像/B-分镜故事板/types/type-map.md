# Type Map

本文件定义 `B-分镜故事板` 的任务分型和 route。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `target_scope` | `single_group / group_batch / episode_batch / review_existing` | 处理范围 |
| `execution_intent` | `prompt_only / generate / repair / review_only` | 是否执行 imagegen |
| `source_state` | `group_source_ready / group_source_partial / group_source_missing` | `4-分组` 可用性 |
| `reference_state` | `all_bound / partial_missing / no_assets / ambiguous` | 主体参照状态 |
| `imagegen_route` | `built_in / cli_confirmed / blocked` | imagegen 路由 |

## Mode Matrix

| type profile | mode | route |
| --- | --- | --- |
| `single_group + generate + group_source_ready` | `single_group_generate` | `steps/storyboard-sheet-workflow.md#N3-N8` |
| `episode_batch + generate + group_source_ready` | `episode_batch_generate` | `N3-N8` with group-level sequential or controlled batch dispatch |
| `group_batch + generate + group_source_ready` | `group_batch_generate` | `N3-N8` for selected groups |
| `* + prompt_only + group_source_ready` | `prompt_only` | `N3-N6, N9-N10` |
| `review_existing + review_only` | `review_only` | `review/review-contract.md` |
| `* + repair` | `repair` | route to owning failed section |
| `* + group_source_missing` | block | ask user to provide/fix source |

## Reroute Rules

- 单一四段式 `分镜ID` 或单帧画面请求：转 `A-分镜画面`。
- 漫画页、气泡文字、阅读顺序或漫画分镜页：转 repo-local `comic` workflow。
- 视频生成前故事板参照：转 `7-视频/B-分镜故事板参照`。
- 需要重写 `4-分组` 内容：转 `4-分组` 修复，不在本技能内改写。

## Gate

进入 `generate` 前必须同时满足：

1. `source_state != group_source_missing`。
2. `imagegen_route == built_in`，除非用户显式确认 CLI/API fallback。
3. `reference_state != ambiguous`，除非 ambiguous 条目已被移除或用户确认。
4. 输出路径位于项目内 `6-图像/B-分镜故事板`。
