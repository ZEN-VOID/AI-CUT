# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `B-分镜故事板参照` 的模式判定和分型策略。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `run_scope` | `single_group`、`group_batch`、`episode_batch`、`multi_episode` | 本轮处理范围 |
| `execution_mode` | `prompt_only`、`generate`、`query_or_download`、`review_only`、`repair` | 是否提交 Dreamina |
| `reference_state` | `found`、`missing_optional`、`ambiguous`、`skipped_by_user_policy` | 故事板图状态 |
| `dreamina_command` | `multimodal2video`、`text2video` | 根据参照图状态选择 |
| `concurrency_mode` | `background_pool`、`serial` | 批量执行方式 |

## Mode Matrix

| mode | required_existing_input | route | skipped stages |
| --- | --- | --- | --- |
| `prompt_only` | `4-分组/第N集.md` | `N1 -> N6 -> N10 -> N11` | Dreamina submit / query / download |
| `single_group_generate` | `4-分组/第N集.md` + one `group_id` | `N1 -> N11` | unrelated groups |
| `episode_batch_generate` | `4-分组/第N集.md` | `N1 -> N11` with `N7` background pool | none |
| `group_batch_generate` | `4-分组/第N集.md` + selected `group_ids` | `N1 -> N11` with selected jobs only | unselected groups |
| `query_or_download` | existing queue ledger or submit_id | `N1 -> N8 -> N9 -> N10 -> N11` | source extraction unless repair needs it |
| `repair` | existing artifacts and fail code | targeted owning node | all unrelated nodes |
| `review_only` | existing artifacts | review gate only | submit / download |

## Reroute Signals

| signal | action |
| --- | --- |
| 用户要求生成故事板图 | reroute to `6-图像/B-分镜故事板` |
| 用户要求单一四段式分镜首帧视频 | reroute to `7-视频/A-分镜画面参照` or first-frame route |
| `dreamina user_credit` 失败 | reroute to `.agents/skills/cli/dreamina-cli` login / auth repair |
| `4-分组` 不存在或 group_id 无法唯一追溯 | stop and return to `4-分组` |
| 故事板图多候选歧义 | block current group and return to reference binding |

## Command Selection Matrix

| reference_state | default command | reason |
| --- | --- | --- |
| `found` | `multimodal2video` | 故事板图作为视觉参照，用 `@图1` 绑定 |
| `missing_optional` | `text2video` | 无图不阻断，用完整组内容直接生成 |
| `ambiguous` | none | 歧义必须人工裁决 |
| `skipped_by_user_policy` | none | 用户明确要求缺图跳过 |
