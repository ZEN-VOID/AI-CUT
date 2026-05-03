# LibTV Handoff

本文件定义 `D-主板混合参照` 与 `.agents/skills/cli/libTV` 的交接规则。D 叶子负责把故事板总参照和主体参照绑定到同一组级任务；`$libTV` 负责上传、会话、查询和下载。

## Command Selection

| reference state | command | rule |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 逐个上传故事板图和主体图，再把 URL 按 `参照图N` 写入 prompt |
| `reference_images` 为空 | `libtv_session_text_only` | 无参照图时只发送完整组级 prompt |
| `$libTV` 脚本或凭据不可用 | blocked | 写入 `blocked`，不得伪造 `sessionId` |

## Defaults

- `requested_model`: 默认为空，表示使用 LibTV 后端默认视频路由。用户显式指定模型时，原样写入自然语言任务。
- `duration_hint`: 默认 `15` 秒。
- `ratio_hint`: 默认 `16:9`。
- `poll_seconds`: 默认 `45`。
- 图片路径必须存在；空数组不传参照。

## Mixed Reference Prompt Rule

发送给 LibTV 的消息必须清楚区分两类参照：

```text
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
- 下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <videos_dir> --prefix <group_id>`。
- 短轮询超时必须保留 `sessionId` 并用 `query_session.py` 后续查询。

## Gate

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 所有本地参照路径可读；上传失败必须进入 blocked 或 submit_failed。
3. prompt 同时保留完整组正文、故事板总参照说明和主体参照说明。
4. 队列能用 `sessionId` 续查。
