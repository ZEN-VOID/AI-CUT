# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `B-分镜故事板参照` 的模式判定和分型策略。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `storyboard_reference_default` | `types/storyboard-reference-default.md` | B 路线所有分镜故事板参照视频任务 | fallback | `types/storyboard-reference-default.md` | none | none |

## Default Package Rule

默认加载 `types/storyboard-reference-default.md`。当任务进入提交、查询或下载时，额外加载 `references/libtv-handoff-contract.md` 与 `.agents/skills/cli/libTV/SKILL.md`；当任务是修复或审查时，额外加载 `review/review-contract.md`。

## Loading Flow

1. 根据用户输入和既有产物锁定 `mode`、`run_scope` 与 `reference_state`。
2. 加载默认包 `types/storyboard-reference-default.md`。
3. 需要 LibTV 执行、查询或下载时加载 `references/libtv-handoff-contract.md` 和 `$libTV` 技能对。
4. 将类型画像交给 `steps/storyboard-video-workflow.md` 消费。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `run_scope` | `single_group`、`group_batch`、`episode_batch`、`multi_episode` | 本轮处理范围 |
| `execution_mode` | `prompt_only`、`generate`、`query_or_download`、`review_only`、`repair` | 是否提交 LibTV |
| `reference_state` | `found`、`missing_optional`、`ambiguous`、`skipped_by_user_policy` | 故事板图状态 |
| `libtv_command` | `libtv_session_with_uploaded_references`、`libtv_session_text_only` | 根据参照图状态选择 |
| `concurrency_mode` | `background_pool`、`serial` | 批量执行方式 |
| `storyboard_reference_prompt_binding` | `bound`、`stripped`、`unknown` | 远端生成 prompt 中故事板总参照身份是否与真实图片 token / 编号 / URL 保持绑定；提交文本不得人工预设 `参照图N` |
| `prompt_fidelity_mode` | `strict_original / transport_only / libtv_optimize` | 提示词保真与远端优化授权模式；默认 `strict_original` |
| `allow_libtv_prompt_optimization` | `false / true` | 是否允许 LibTV Agent 做提示词优化、重排、摘要或工作流规划；默认 `false` |
| `duration_source` | `group_yaml / shot_sum / fallback_default / user_override` | 组级视频时长估算来源 |
| `duration_estimate_seconds` | positive number | 从 `4-分组` 当前组得到的真实估算时长 |
| `duration_hint` | integer seconds | 提交给 LibTV 的视频时长，按 `clamp(duration_estimate_seconds, 4, 15)` 得到 |

## Mode Matrix

| mode | required_existing_input | route | skipped stages |
| --- | --- | --- | --- |
| `prompt_only` | `4-分组/第N集.md` | `N1 -> N6 -> N10 -> N11` | LibTV submit / query / download |
| `single_group_generate` | `4-分组/第N集.md` + one `group_id` | `N1 -> N11` | unrelated groups |
| `episode_batch_generate` | `4-分组/第N集.md` | `N1 -> N11` with `N7` background pool | none |
| `group_batch_generate` | `4-分组/第N集.md` + selected `group_ids` | `N1 -> N11` with selected jobs only | unselected groups |
| `query_or_download` | existing queue ledger or sessionId | `N1 -> N8 -> N9 -> N10 -> N11` | source extraction unless repair needs it |
| `repair` | existing artifacts and fail code | targeted owning node | all unrelated nodes |
| `review_only` | existing artifacts | review gate only | submit / download |

## Reroute Signals

| signal | action |
| --- | --- |
| 用户要求生成故事板图 | reroute to `6-图像/B-分镜故事板` |
| 用户要求单一四段式分镜首帧视频 | reroute to `7-视频/A-分镜画面参照` or first-frame route |
| `LIBTV_ACCESS_KEY credential check` 失败 | reroute to `.agents/skills/cli/libTV` login / auth repair |
| `4-分组` 不存在或 group_id 无法唯一追溯 | stop and return to `4-分组` |
| 故事板图多候选歧义 | block current group and return to reference binding |

## Command Selection Matrix

| reference_state | default command | reason |
| --- | --- | --- |
| `found` | `libtv_session_with_uploaded_references` | 故事板图作为视觉参照，先建立故事板总参照到 OSS URL 的身份绑定，最终按生成框 UI 图1 或 `imageList[0]` 回刷 fenced YAML |
| `missing_optional` | `libtv_session_text_only` | 无图不阻断，用完整组内容直接生成 |
| `ambiguous` | none | 歧义必须人工裁决 |
| `skipped_by_user_policy` | none | 用户明确要求缺图跳过 |

## Prompt Reference Binding Rules

- 有故事板参照图时，默认 `storyboard_reference_prompt_binding=bound`。
- 远端提交使用两段式 prompt：`draft` 保持 source-first 原组 YAML，不预填 `reference_index`、`uploaded_url` 或空 URL；生成框完成故事板图加载后，以 UI 缩略图 `图1`/`Image 1` 为优先槽位真源，回刷为 `final` 形态的 `【分镜组源文本】`，在 fenced YAML `故事板参照` 写入 `reference_index: 1`、真实 `uploaded_url` 与可选 `image_token`。
- 若 query 检测到 `create_generation_task.params.prompt` 中参照部分只剩裸 `{{Image 1}}`、裸 `图片1` 或裸 URL，没有“故事板总参照”身份邻近绑定，`storyboard_reference_prompt_binding=stripped`，状态改为 `storyboard_reference_name_stripped`，不进入正常 pending。

## Prompt Fidelity Rules

- 默认类型画像为 `prompt_fidelity_mode=strict_original` 且 `allow_libtv_prompt_optimization=false`。
- `strict_original` 和 `transport_only` 可同时生效：前者锁定 `【分镜组源文本】` 原文主体，后者只做远端技术投影。
- `transport_only` 不等于内容优化；它只允许本地路径到上传 URL、参照图数量上限、`imageList`、时长、比例、分辨率和声音参数等机械转换。
- `transport_only` 中的时长投影必须来自当前组 `duration_hint`；不得把所有组固定为 15 秒。
- `libtv_optimize` 只能由用户显式选择，或由 submit plan 明确记录 `allow_libtv_prompt_optimization=true` 后进入；不得由远端 LibTV Agent 自行升级。
- 若 query 检测到未 opt-in 的提示词优化、重新编排、摘要、改写、补镜头、镜头计划或工作流规划，路由状态改为 `prompt_fidelity_violation`，不进入正常 pending。
