# Type Map

本文件定义 `C-主体参照` 的任务分型和 route。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `target_scope` | `single_group / group_batch / episode_batch / multi_episode_batch / review_existing` | 处理范围 |
| `execution_intent` | `prompt_only / generate / query_or_download / repair / review_only` | 是否执行或查询 Dreamina |
| `source_state` | `group_source_ready / group_source_partial / group_source_missing` | `4-分组` 可用性 |
| `reference_state` | `all_bound / partial_missing / no_assets / ambiguous` | 主体参照状态 |
| `dreamina_route` | `multimodal2video / text2video / query_result / blocked` | Dreamina 路由 |
| `concurrency_state` | `serial / background_parallel / blocked` | 提交或查询并发策略 |

## Mode Matrix

| type profile | mode | route |
| --- | --- | --- |
| `single_group + generate + group_source_ready` | `single_group_generate` | `steps/subject-reference-video-workflow.md#N3-N9` |
| `episode_batch + generate + group_source_ready` | `episode_batch_generate` | `N3-N9` with background group-level parallel dispatch |
| `group_batch + generate + group_source_ready` | `group_batch_generate` | `N3-N9` for selected groups |
| `multi_episode_batch + generate + group_source_ready` | `multi_episode_batch_generate` | one episode package per source file, shared submit concurrency |
| `* + prompt_only + group_source_ready` | `prompt_only` | `N3-N6, N10-N11` |
| `review_existing + query_or_download` | `query_or_download` | `.agents/skills/cli/dreamina-cli` queue follow-up |
| `review_existing + review_only` | `review_only` | `review/review-contract.md` |
| `* + repair` | `repair` | route to owning failed section |
| `* + group_source_missing` | block | ask user to provide/fix source |

## Dreamina Route Rules

- `reference_state in {all_bound, partial_missing}` 且 `bound[]` 非空：优先 `multimodal2video`。
- `reference_state == no_assets` 或所有 YAML 主体都缺图：走 `text2video`。
- `reference_state == ambiguous`：阻断提交，先修参照。
- 已有 `submit_id`：走 `query_result`，不得重复提交，除非用户明确 rerun。

## Reroute Rules

- 单一四段式 `分镜ID` 或单帧首帧视频请求：转 `7-视频/A-分镜画面参照`。
- 需要基于组级 storyboard 图片做视频：转 `7-视频/B-分镜故事板参照`。
- 需要重写 `4-分组` 内容：转 `4-分组` 修复，不在本技能内改写。
- Dreamina 登录、安装、余额或下载排障：进入 `.agents/skills/cli/dreamina-cli`，再回本技能更新队列。

## Gate

进入 `generate` 前必须同时满足：

1. `source_state != group_source_missing`。
2. `dreamina_route != blocked`。
3. `reference_state != ambiguous`，除非 ambiguous 条目已被移除或用户确认。
4. 输出路径位于项目内 `7-视频/C-主体参照`。
