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
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../5-设计/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许出现 `参照图N：<uploaded_url>` 与故事板总参照 / 主体参照用途说明。
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

参照图1：<storyboard_uploaded_url>
参照图1 是整组分镜故事板总参照，只用于整体构图、镜头顺序、画面连续性和节奏，不作为唯一首帧。

参照图2：<subject_uploaded_url>
角色 林寂 的外观参照为参照图2；仅用于主体外观一致性，不改写剧情事实。

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
