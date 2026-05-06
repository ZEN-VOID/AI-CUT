# LibTV Handoff

本文件定义 `D-主板混合参照` 与 `.agents/skills/cli/libTV` 的交接规则。D 叶子负责把故事板总参照和主体参照绑定到同一组级任务；`$libTV` 负责上传、会话、查询和下载。

## Official Skill Dependency

- 视频生成必须调用 `.agents/skills/cli/libTV` 官方技能包完成；不得绕过其 `scripts/` 直接拼接私有 OpenAPI。
- 提交前加载 `.agents/skills/cli/libTV/SKILL.md`，并确认 `LIBTV_ACCESS_KEY` 已在当前命令环境中可用。
- 如需新画布隔离当前分镜组，先运行 `python3 .agents/skills/cli/libTV/scripts/change_project.py`，并把返回的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report。

## Official Script Order

有故事板或主体参照图时固定顺序：

1. `change_project.py`：仅在需要干净画布或用户要求隔离时执行。
2. `upload_file.py <path>`：逐图上传故事板总参照和主体参照，保存返回的 OSS URL。
3. `create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `query_session.py <sessionId> --project-id <projectUuid>`：按官方 `$libTV` 轮询策略查询画布消息和生成结果。
5. `download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`：生成完成后自动下载到本技能的集目录。

无参照图时跳过 `upload_file.py`，其余顺序不变。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、上传参照、生成节点和结果都应保留在同一 `projectUrl`。
- queue/result/report 必须记录 `sessionId`、`projectUuid`、`projectUrl`，用于用户在画布查看。
- 若画布未出现对应生成节点或结果 URL，不得把本地状态标为 downloaded / generated。

## Prompt Fidelity And Optimization Authorization

- 默认远端 handoff 必须采用 `strict_original + transport_only`：`prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false`，并禁止提示词优化、重新编排、摘要、改写和补镜头。
- `strict_original` 表示 `【混合参照说明】` 中的故事板总参照/主体名/参照图/URL 绑定关系与 `【分镜组源文本】` 原文必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`mixedList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Command Selection

| reference state | command | rule |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 逐个上传故事板图和主体图，再把 URL 按 `参照图N` 写入 prompt |
| `reference_images` 为空 | `libtv_session_text_only` | 无参照图时只发送完整组级 prompt |
| `$libTV` 脚本或凭据不可用 | blocked | 写入 `blocked`，不得伪造 `sessionId` |

## Defaults

- `requested_model`: 默认为空，表示使用 LibTV 后端默认视频路由。用户显式指定模型时，原样写入自然语言任务。
- `duration_hint`: 默认 `15` 秒，必须写入远端提交。
- `ratio_hint`: 默认 `16:9`，必须写入远端提交。
- `video_resolution_hint`: 默认 `720p`，即用户可见规格 720P，必须写入远端提交。
- `enableSound`: 默认 `on`，必须写入远端提交。
- `poll_seconds`: 默认 `45`。
- 图片路径必须存在；空数组不传参照。

## Remote Handoff Contract

本地审核 prompt 可以保留故事板和主体本地路径，便于 review gate 回查；发送给 LibTV 画布的 `*-libtv-submission.txt` 是另一层远端提交文本，必须满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 第一段必须使用 `hybrid-prompt-assembly-contract.md#LibTV Remote Opening` 中的 D 专属调用锁，明确 `provider=seedance2.0`、`taskType=video`、有图时 `modeType=mixed2video` 和 `mixedList`，无图时 `modeType=text2video`。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../5-设计/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许出现 `故事板总参照：参照图N <uploaded_url>`、`主体名：参照图N <uploaded_url>` 与故事板总参照 / 主体参照用途说明。
- `【直接生成请求】` 必须写成“基于【混合参照说明】（包含故事板总参照、主体名和主体参照 URL）和下方【分镜组源文本】”，不得只写“基于上述参照图 URL”。
- 远端 `create_generation_task.params.prompt` 必须保留故事板身份、主体名与图片 token/编号绑定，例如 `故事板总参照 参照图1`、`林寂 参照图2`、`林寂 {{Image 2}}`；不得把参照区压成 `{{Image 1}} {{Image 2}} ...`、`图片1 图片2 ...` 或裸 URL 列表。
- 默认提交文本必须声明 `strict_original + transport_only`，且 `allow_libtv_prompt_optimization=false`；未显式 opt-in 时不得要求或默许 LibTV 重新组织、压缩、合并或摘要分镜组源文本。
- 不得把 D 任务拆成 B 路线和 C 路线分别提交；故事板总参照和主体参照必须在同一个 `mixed2video` 任务中生效。

## Mixed Reference Prompt Rule

发送给 LibTV 的消息必须清楚区分两类参照：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: mixed2video
mixedList: [{"url": "<uploaded_url_1>", "type": "image"}, {"url": "<uploaded_url_2>", "type": "image"}, ...]
duration: 15
ratio: 16:9
resolution: 720p
enableSound: on
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。

【混合参照说明】
故事板总参照：参照图1 <storyboard_uploaded_url>
参照图1 是整组分镜故事板总参照，只用于整体构图、镜头顺序、画面连续性和节奏，不作为唯一首帧。

林寂：参照图2 <subject_uploaded_url>
角色 林寂 的外观参照为参照图2；仅用于主体外观一致性，不改写剧情事实。

【直接生成请求】
请基于【混合参照说明】（包含故事板总参照、主体名、主体类别、参照图编号和主体参照 URL）和下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。请直接把【混合参照说明】中与本组相关的故事板总参照绑定关系、主体名/参照图绑定关系 + 【分镜组源文本】原文作为生成 prompt 完整体。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<完整分镜组内容>
```

## Submit Plan Requirements

`第N集-libtv-submit-plan.json` 每个 task 至少记录：

- `queue_id`
- `group_id`
- `command`
- `prompt_path`
- `storyboard_reference.path`
- `storyboard_reference.uploaded_url`
- `subject_references[].path`
- `subject_references[].uploaded_url`
- `download_dir`
- `expected_output`
- `sessionId`
- `projectUuid`
- `projectUrl`
- `prompt_fidelity_mode`
- `allow_libtv_prompt_optimization`
- `transport_only_projection`
- `next_action`

## Queue Ledger

| queue_id | group_id | command | sessionId | projectUuid | local_status | remote_status | reference_count | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Query And Download

- 查询使用 `python3 .agents/skills/cli/libTV/scripts/query_session.py <sessionId> --project-id <projectUuid>`。
- 按官方 `$libTV` 轮询策略查询完成后必须自动下载；下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`。
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/
```
- 短轮询超时必须保留 `sessionId` 并用 `query_session.py` 后续查询。

## Gate

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 所有本地参照路径可读；上传失败必须进入 blocked 或 submit_failed。
3. prompt 同时保留完整组正文、故事板总参照说明和主体参照说明；远端 `*-libtv-submission.txt` 首段为 `【LibTV 调用锁定】` 和正确 `modeType`。
4. 队列能用 `sessionId` 续查。
5. 有任一故事板或主体参照图时，远端调用必须为 `modeType=mixed2video` 且使用 `mixedList`；不得退回 `singleImage2video`、`image2video` 或 B/C 分开提交。
6. 远端工具 prompt 保留故事板身份、主体名与图片 token/编号绑定，不存在裸图片 token 序列。
7. 默认提交 prompt 已声明 `strict_original + transport_only`，且 submit plan 中 `allow_libtv_prompt_optimization=false`。
8. 未显式 opt-in `libtv_optimize` 时，远端 query 不得出现优化版提示词、重新编排脚本、镜头计划或摘要版分镜。
