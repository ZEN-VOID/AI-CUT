# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `C-主体参照` 的任务分型和 route。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `subject_reference_default` | `types/subject-reference-default.md` | C 路线所有主体参照视频任务 | fallback | `types/subject-reference-default.md` | none | none |

## Default Package Rule

默认加载 `types/subject-reference-default.md`。当任务进入提交、查询或下载时，额外加载 `references/libtv-handoff.md` 与 `.agents/skills/cli/libTV/SKILL.md`；当任务是修复或审查时，额外加载 `review/review-contract.md`。

## Loading Flow

1. 根据用户输入和既有产物锁定 `mode`、`target_scope` 与 `reference_state`。
2. 加载默认包 `types/subject-reference-default.md`。
3. 需要 LibTV 执行、查询或下载时加载 `references/libtv-handoff.md` 和 `$libTV` 技能对。
4. 将类型画像交给 `steps/subject-reference-video-workflow.md` 消费。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `target_scope` | `single_group / group_batch / episode_batch / multi_episode_batch / review_existing` | 处理范围 |
| `execution_intent` | `prompt_only / generate / query_or_download / repair / review_only` | 是否执行或查询 LibTV |
| `source_state` | `group_source_ready / group_source_partial / group_source_missing` | `4-分组` 可用性 |
| `reference_state` | `all_bound / partial_missing / no_assets / visual_resolved / ambiguous` | 主体参照状态 |
| `libtv_route` | `libtv_session_with_uploaded_references / libtv_session_text_only / query_session / blocked` | LibTV 路由 |
| `concurrency_state` | `serial / background_parallel / blocked` | 提交或查询并发策略 |
| `prompt_fidelity_mode` | `strict_original / transport_only / libtv_optimize` | 提示词保真与远端优化授权模式；默认 `strict_original` |
| `allow_libtv_prompt_optimization` | `false / true` | 是否允许 LibTV Agent 做提示词优化、重排、摘要或工作流规划；默认 `false` |
| `subject_reference_prompt_binding` | `bound / stripped / unknown` | 远端生成 prompt 中主体名是否与图片 token / 参照编号保持绑定；默认提交前为 `bound` |

## Mode Matrix

| type profile | mode | route |
| --- | --- | --- |
| `single_group + generate + group_source_ready` | `single_group_generate` | `steps/subject-reference-video-workflow.md#N3-N9` |
| `episode_batch + generate + group_source_ready` | `episode_batch_generate` | `N3-N9` with background group-level parallel dispatch |
| `group_batch + generate + group_source_ready` | `group_batch_generate` | `N3-N9` for selected groups |
| `multi_episode_batch + generate + group_source_ready` | `multi_episode_batch_generate` | one episode package per source file, shared submit concurrency |
| `* + prompt_only + group_source_ready` | `prompt_only` | `N3-N6, N10-N11` |
| `review_existing + query_or_download` | `query_or_download` | `.agents/skills/cli/libTV` queue follow-up |
| `review_existing + review_only` | `review_only` | `review/review-contract.md` |
| `* + repair` | `repair` | route to owning failed section |
| `* + group_source_missing` | block | ask user to provide/fix source |

## LibTV Route Rules

- `reference_state in {all_bound, partial_missing, visual_resolved}` 且 `bound[]` 非空：优先 `libtv_session_with_uploaded_references`。
- `reference_state == no_assets` 或所有 YAML 主体都缺图：走 `libtv_session_text_only`。
- 多候选主体必须先执行视觉消歧；视觉消歧成功后视为 `visual_resolved`，视觉消歧仍不能唯一选择时才进入 `ambiguous`。
- `reference_state == ambiguous`：阻断提交，先修参照或等待用户确认。
- 已有 `sessionId`：走 `query_session`，不得重复提交，除非用户明确 rerun。

## Prompt Fidelity Route Rules

- 默认类型画像为 `prompt_fidelity_mode=strict_original` 且 `allow_libtv_prompt_optimization=false`。
- `strict_original` 和 `transport_only` 可同时生效：前者锁定 `【分镜组源文本】` 原文主体，后者只做远端技术投影。
- `transport_only` 不等于内容优化；它只允许本地路径到上传 URL、参照图数量上限、`mixedList`、时长、比例、分辨率和声音参数等机械转换。
- `libtv_optimize` 只能由用户显式选择，或由 submit plan 明确记录 `allow_libtv_prompt_optimization=true` 后进入；不得由远端 LibTV Agent 自行升级。
- 若 query 检测到未 opt-in 的提示词优化、重新编排、摘要、改写、补镜头、镜头计划或工作流规划，路由状态改为 `prompt_fidelity_violation`，不进入正常 pending。
- 若 query 检测到 `create_generation_task.params.prompt` 中参照部分只剩裸 `{{Image N}}`、裸 `图片N` 或裸 URL 序列，没有主体名称邻近绑定，`subject_reference_prompt_binding=stripped`，路由状态改为 `subject_reference_name_stripped`，不进入正常 pending。

## Reroute Rules

- 单一四段式 `分镜ID` 或单帧首帧视频请求：转 `7-视频/A-分镜画面参照`。
- 需要基于组级 storyboard 图片做视频：转 `7-视频/B-分镜故事板参照`。
- 需要重写 `4-分组` 内容：转 `4-分组` 修复，不在本技能内改写。
- LibTV 登录、安装、余额或下载排障：进入 `.agents/skills/cli/libTV`，再回本技能更新队列。

## Gate

进入 `generate` 前必须同时满足：

1. `source_state != group_source_missing`。
2. `libtv_route != blocked`。
3. `reference_state != ambiguous`，除非 ambiguous 条目已被移除、视觉消歧已唯一解决或用户确认。
4. 输出路径位于项目内 `7-视频/C-主体参照`。
5. 未显式 opt-in `libtv_optimize` 时，`allow_libtv_prompt_optimization` 必须为 `false`，远端提交必须包含 strict 原文与禁止优化约束。
6. 有主体参照图时，远端提交必须把 `【主体参照说明】 + 【分镜组源文本】` 作为生成 prompt 完整体，并确保主体名与图片 token / 参照编号绑定。
