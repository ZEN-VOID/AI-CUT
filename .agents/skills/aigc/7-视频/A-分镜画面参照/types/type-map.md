# Type Map

本文件定义 `A-分镜画面参照` 的模式判定和分型策略。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `run_scope` | `single_group`、`group_batch`、`shot_batch`、`episode_batch`、`multi_episode` | 本轮处理范围 |
| `execution_mode` | `prompt_only`、`generate`、`query_or_download`、`review_only`、`repair` | 是否提交 Dreamina |
| `reference_state` | `found`、`partial`、`missing_optional`、`ambiguous`、`over_limit`、`skipped_by_user_policy` | 分镜画面图状态 |
| `dreamina_command` | `multimodal2video`、`text2video`、`blocked` | 根据参照图状态选择 |
| `concurrency_mode` | `background_pool`、`serial` | 批量执行方式 |

## Mode Matrix

| mode | required_existing_input | route | skipped stages |
| --- | --- | --- | --- |
| `prompt_only` | `4-分组/第N集.md` | `N1 -> N7 -> N11 -> N12` | Dreamina submit / query / download |
| `single_group_generate` | `4-分组/第N集.md` + one `group_id` | `N1 -> N12` | unrelated groups |
| `episode_batch_generate` | `4-分组/第N集.md` | `N1 -> N12` with `N8` background pool | none |
| `group_batch_generate` | `4-分组/第N集.md` + selected `group_ids` | `N1 -> N12` with selected jobs only | unselected groups |
| `shot_batch_generate` | `4-分组/第N集.md` + selected `shot_ids` | map shot ids to groups, then selected group jobs | unrelated groups and shots |
| `query_or_download` | existing queue ledger or submit_id | `N1 -> N9 -> N10 -> N11 -> N12` | source extraction unless repair needs it |
| `repair` | existing artifacts and fail code | targeted owning node | all unrelated nodes |
| `review_only` | existing artifacts | review gate only | submit / download |

## Reroute Signals

| signal | action |
| --- | --- |
| 用户要求生成分镜画面图 | reroute to `6-图像/A-分镜画面` |
| 用户要求故事板大图作为参照 | reroute to `7-视频/B-分镜故事板参照` |
| 用户要求角色/场景/道具主体参照 | reroute to `7-视频/C-主体参照` |
| `dreamina user_credit` 失败 | reroute to `.agents/skills/cli/dreamina-cli` login / auth repair |
| `4-分组` 不存在或 group_id / shot_id 无法唯一追溯 | stop and return to `4-分组` |
| 分镜画面图多候选歧义 | block current group and return to reference binding |

## Command Selection Matrix

| reference_state | default command | reason |
| --- | --- | --- |
| `found` | `multimodal2video` | 当前组所有目标镜头图均有参照，用 `@图N` 绑定 |
| `partial` | `multimodal2video` | 至少一张真实分镜画面图可作为多图参照，缺图镜头移除空槽位 |
| `missing_optional` | `text2video` | 无图不阻断，用完整组内容直接生成 |
| `ambiguous` | `blocked` | 歧义必须人工裁决 |
| `over_limit` | `blocked` by default | 超过 CLI 多图上限时不得静默丢图 |
| `skipped_by_user_policy` | `blocked` | 用户明确要求缺图跳过 |
