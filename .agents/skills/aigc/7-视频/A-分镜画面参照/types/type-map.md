# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `A-分镜画面参照` 的模式判定和分型策略。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `frame_reference_default` | `types/frame-reference-default.md` | A 路线所有分镜画面参照视频任务 | fallback | `types/frame-reference-default.md` | none | none |

## Default Package Rule

默认加载 `types/frame-reference-default.md`。当任务进入提交、查询或下载时，额外加载 `references/libtv-handoff-contract.md` 与 `.agents/skills/cli/libTV/SKILL.md + CONTEXT.md`；当任务是修复或审查时，额外加载 `review/review-contract.md`。

## Loading Flow

1. 根据用户输入和既有产物锁定 `mode`、`run_scope` 与 `reference_state`。
2. 加载默认包 `types/frame-reference-default.md`。
3. 需要 LibTV 执行、查询或下载时加载 `references/libtv-handoff-contract.md` 和 `$libTV` 技能对。
4. 将类型画像交给 `steps/frame-reference-video-workflow.md` 消费。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `run_scope` | `single_group`、`group_batch`、`shot_batch`、`episode_batch`、`multi_episode` | 本轮处理范围 |
| `execution_mode` | `prompt_only`、`generate`、`query_or_download`、`review_only`、`repair` | 是否提交 LibTV |
| `reference_state` | `found`、`partial`、`missing_optional`、`ambiguous`、`over_limit`、`skipped_by_user_policy` | 分镜画面图状态 |
| `libtv_command` | `libtv_session_with_uploaded_references`、`libtv_session_text_only`、`blocked` | 根据参照图状态选择 |
| `concurrency_mode` | `background_pool`、`serial` | 批量执行方式 |

## Mode Matrix

| mode | required_existing_input | route | skipped stages |
| --- | --- | --- | --- |
| `prompt_only` | `4-分组/第N集.md` | `N1 -> N7 -> N11 -> N12` | LibTV submit / query / download |
| `single_group_generate` | `4-分组/第N集.md` + one `group_id` | `N1 -> N12` | unrelated groups |
| `episode_batch_generate` | `4-分组/第N集.md` | `N1 -> N12` with `N8` background pool | none |
| `group_batch_generate` | `4-分组/第N集.md` + selected `group_ids` | `N1 -> N12` with selected jobs only | unselected groups |
| `shot_batch_generate` | `4-分组/第N集.md` + selected `shot_ids` | map shot ids to groups, then selected group jobs | unrelated groups and shots |
| `query_or_download` | existing queue ledger or sessionId | `N1 -> N9 -> N10 -> N11 -> N12` | source extraction unless repair needs it |
| `repair` | existing artifacts and fail code | targeted owning node | all unrelated nodes |
| `review_only` | existing artifacts | review gate only | submit / download |

## Reroute Signals

| signal | action |
| --- | --- |
| 用户要求生成分镜画面图 | reroute to `6-图像/A-分镜画面` |
| 用户要求故事板大图作为参照 | reroute to `7-视频/B-分镜故事板参照` |
| 用户要求角色/场景/道具主体参照 | reroute to `7-视频/C-主体参照` |
| `LIBTV_ACCESS_KEY credential check` 失败 | reroute to `.agents/skills/cli/libTV` login / auth repair |
| `4-分组` 不存在或 group_id / shot_id 无法唯一追溯 | stop and return to `4-分组` |
| 分镜画面图多候选歧义 | block current group and return to reference binding |

## Command Selection Matrix

| reference_state | default command | reason |
| --- | --- | --- |
| `found` | `libtv_session_with_uploaded_references` | 当前组所有目标镜头图均有参照，用 `@图N` 绑定 |
| `partial` | `libtv_session_with_uploaded_references` | 至少一张真实分镜画面图可作为多图参照，缺图镜头移除空槽位 |
| `missing_optional` | `libtv_session_text_only` | 无图不阻断，用完整组内容直接生成 |
| `ambiguous` | `blocked` | 歧义必须人工裁决 |
| `over_limit` | `blocked` by default | 超过 LibTV 参照数量限制时不得静默丢图 |
| `skipped_by_user_policy` | `blocked` | 用户明确要求缺图跳过 |
