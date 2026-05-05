# LibTV Handoff

本文件定义 step3：根据完整分镜组内容和主体参照，调用 `.agents/skills/cli/libTV` 完成组级视频生成。C 叶子负责主体槽位和 prompt 组装；`$libTV` 负责上传本地参照图、创建会话、查询和下载。

## Required Skill Dependency

提交或查询前必须加载：

```text
.agents/skills/cli/libTV/SKILL.md
```

并调用 `.agents/skills/cli/libTV` 官方技能包完成视频生成，不得绕过其 `scripts/` 直接拼接私有 OpenAPI。确认当前命令环境存在 `LIBTV_ACCESS_KEY`，不得把 key 写入任何项目文件。

## Official Script Order

有主体参照图时固定顺序：

1. `python3 .agents/skills/cli/libTV/scripts/change_project.py`：仅在需要干净画布或用户要求隔离时执行，并把返回的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report；Markdown 输出同时写 `canvas_link: [打开画布](<projectUrl>)`。
2. `python3 .agents/skills/cli/libTV/scripts/upload_file.py <path>`：逐图上传主体、场景、道具参照，保存返回的 OSS URL。
3. `python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `python3 .agents/skills/cli/libTV/scripts/query_session.py <sessionId> --project-id <projectUuid>`：提交后必须立即查询一次，并用 `scripts/detect-libtv-stall.py` 执行 post-submit gate；通过后才进入正常轮询。
5. `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`：生成完成后自动下载到本技能的集目录。

无参照图时跳过 `upload_file.py`，其余顺序不变。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、上传参照、生成节点和结果都应保留在同一 `projectUrl`。
- queue/result/report 必须记录 `sessionId`、`projectUuid`、`projectUrl`，并在 Markdown 中给出可直接打开的 `canvas_link`，用于用户在画布查看。
- JSON 输出必须保留原始 `projectUrl`，并可额外写入 `canvasMarkdown`，便于最终回执直接投影为 Markdown 链接。
- 若画布未出现对应生成节点或结果 URL，不得把本地状态标为 downloaded / generated。

## Command Selection

| reference state | command | rule |
| --- | --- | --- |
| `bound_images` | `libtv_session_with_uploaded_references` | 一张或多张主体图片；先上传本地图片，再把 OSS URL 追加到对应主体信息后 |
| `visual_resolved` | `libtv_session_with_uploaded_references` | 多候选已通过窗口图像上下文识图消歧，按最终选中的图片上传 |
| `no_images` | `libtv_session_text_only` | 无可用主体图，使用纯文本 prompt，不传空图片 |
| `ambiguous` | blocked | 视觉消歧仍无法唯一确定，或尚未把候选图作为可加载上下文完成识图前不得提交 |
| `auth_or_script_failed` | blocked | `LIBTV_ACCESS_KEY` 或 `$libTV` 脚本不可用时只写计划和 blocked queue row |

## Remote Handoff Contract

发送给 `.agents/skills/cli/libTV/scripts/create_session.py` 的消息必须是远端可执行文本，不得直接复用本地审核 prompt。

强制要求：

- 消息第一段必须是 `video-prompt-assembly-contract.md#LibTV Remote Opening` 中的 `【LibTV 调用锁定】`。
- provider 参数前必须包含 no-ask 约束：禁止 `ask_user`、禁止确认、禁止展示“请稍候”、禁止等待下一条消息，并声明用户已授权立即生成；无法创建生成节点时直接返回 `ERROR_NO_GENERATION_NODE`。
- 有主体参照图时，必须明确 `provider=seedance2.0`、`taskType=video`、`modeType=mixed2video`、`mixedList=[{"url": "<真实 uploaded_url>", "type": "image"}]`。`mixedList` 必须是严格 JSON 对象数组，不得保留 `参照图N URL` 或 `<uploaded_url>` 占位符，不得写成 `image2video`、`singleImage2video` 或 `frames2video`。
- 无主体参照图时，必须明确 `modeType=text2video`。
- 已上传图片只能以 `参照图<upload_index> <uploaded_url>` 形式出现在远端消息中。
- 远端消息不得包含 `@projects/...`、绝对本地路径、`prompt_path`、`reference-manifest` 路径或其他本地文件路径；这些只写入本地 plan / queue / report。
- `分镜组源文本` 必须说明它是连续视频的镜头文字约束，不是图片生产清单。
- 若远端代理改用 `image2video`、`singleImage2video`、`frames2video`，或画布结构出现“多张参照图分别输出视频再合成”，应判定为 route drift；C 路线有图时只能接受 `mixed2video + mixedList`。
- 若提交后第一轮 query 发现 assistant 内容为空且 `toolCalls.name == ask_user`，或 tool 消息要求“展示 question / 等待用户下一条消息 / 请稍候”，必须判定为 `stalled_remote_ask_user`；不得标记为 `pending_remote_generation`，不得继续等待同一 session。

## Default Parameters

- `requested_model`: 默认为空，表示使用 LibTV 后端默认视频路由。用户显式指定模型时，原样写入自然语言任务。
- `duration_hint`: 默认 `15` 秒，必须写入远端提交。
- `ratio_hint`: 默认 `16:9`，必须写入远端提交。
- `video_resolution_hint`: 默认 `720p`，即用户可见规格 720P，必须写入远端提交。
- `enableSound`: 默认 `on`，必须写入远端提交。
- `poll_seconds`: 默认短轮询 `45` 秒；超时后保留 `sessionId` 并进入 queue ledger。
- `parallelism`: 默认后台多线程批量并发；实际值应记录在 submit plan，建议从 `2` 到 `4` 起步，避免上传带宽不稳。

## Submit Plan Shape

每个分镜组的 canonical submit plan 必须写入：

```text
projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/<分镜组ID>/libtv-submit-plan.json
```

集级 `第N集-libtv-submit-plan.json` 只作为派生汇总，记录每个 group package 的回指路径与状态，不作为单组任务唯一真源。分镜组 submit plan 至少包含：

```json
{
  "project_name": "诡校-测试版",
  "episode_id": "第1集",
  "package_dir": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1",
  "parallelism": 3,
  "libtv_self_check": {
    "required_env": "LIBTV_ACCESS_KEY",
    "status": "pending"
  },
  "tasks": [
    {
      "queue_id": "第1集-1-1-1",
      "group_id": "1-1-1",
      "command": "libtv_session_with_uploaded_references",
      "requested_model": "",
      "duration_hint": 15,
      "ratio_hint": "16:9",
      "video_resolution_hint": "720p",
      "prompt_path": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1/prompt.md",
      "remote_submission_path": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1/libtv-submission.txt",
      "images": [
        {
          "upload_index": 1,
          "name": "林寂",
          "category": "character",
          "path": "projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png",
          "uploaded_url": "",
          "subject_inline": "林寂 参照图1"
        }
      ],
      "projectUuid": "",
      "projectUrl": "",
      "canvasMarkdown": "",
      "download_dir": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1",
      "expected_output": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1/1-1-1.mp4"
    }
  ]
}
```

## Script Rendering

有参照图：

```bash
python3 .agents/skills/cli/libTV/scripts/upload_file.py "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
python3 .agents/skills/cli/libTV/scripts/upload_file.py "projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png"
python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1/libtv-submission.txt)"
python3 .agents/skills/cli/libTV/scripts/query_session.py "<sessionId>" --project-id "<projectUuid>"
python3 .agents/skills/cli/libTV/scripts/download_results.py "<sessionId>" --output-dir "projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1" --prefix "1-1-1"
```

prompt 文件中必须包含上传后的 URL，例如：

```text
林寂：参照图1 <uploaded_url>
永夜私立中学二年级A班教室：参照图2 <uploaded_url>
```

无参照图：

```bash
python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1/libtv-submission.txt)"
python3 .agents/skills/cli/libTV/scripts/query_session.py "<sessionId>" --project-id "<projectUuid>"
python3 .agents/skills/cli/libTV/scripts/download_results.py "<sessionId>" --output-dir "projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1" --prefix "1-1-1"
```

## Queue Ledger

任何提交、排队或待下载任务都必须先写入分镜组包内的 `groups/<分镜组ID>/queue.md`。集级 `第N集-libtv-queue.md` 只作为汇总视图，指向每个 group queue：

| queue_id | group_id | command | sessionId | projectUuid | canvas_link | local_status | remote_status | last_checked_at | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

`sessionId` 缺失时该行状态只能是 `planned`、`blocked` 或 `submit_failed`。

## Post Submit Gate

提交后必须运行：

```bash
python3 .agents/skills/cli/libTV/scripts/query_session.py "<sessionId>" --project-id "<projectUuid>" > "<package_dir>/post-submit-query.json"
python3 .agents/skills/aigc/7-视频/C-主体参照/scripts/detect-libtv-stall.py "<package_dir>/post-submit-query.json"
```

判定规则：

- 若存在可下载视频 URL、生成任务工具调用或明确的生成中工具消息，状态可进入 `pending_remote_generation`。
- 若出现 `ask_user` 等待态，状态必须写成 `stalled_remote_ask_user / no_generation_node`，并停止等待该 session。
- 若 no-ask rerun 仍触发 `ask_user`，状态升级为 `blocked_agent_im_stall`，需要换 LibTV 直达生成接口或人工画布路径。
- 同一个 stalled session 不再作为恢复目标；恢复必须新建干净 session，并使用更短的 no-ask 远端提交文本。

## Concurrency Rules

- 并发只发生在 LibTV 上传、创建会话或查询层；每个 worker 只能写自己的 `groups/<分镜组ID>/` package，不得改写其他组的 prompt、manifest、plan、queue、results 或 report。
- 集级 `group-index`、`reference-manifest`、submit plan、queue、results 和最终 `执行报告.md` 必须在汇流阶段串行重建，作为派生 summary。
- 若并发提交任一组失败，不影响其他组继续，但最终报告必须列出失败组和重试命令。

## Gate

通过 LibTV handoff 必须满足：

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 每个 runnable group 有合法命令和非空 prompt。
3. 有参照图时 `images[]` 本地路径都存在，且已记录 `uploaded_url` 或上传失败原因。
4. 无参照图时命令为 `libtv_session_text_only`，不传空图片槽。
5. 任务状态可通过 queue ledger 续查。
6. 远端提交 prompt 已通过直接生视频开头检查，且不含本地图片路径。
7. 有主体参照图时远端若没有锁定 `modeType=mixed2video` 和 `mixedList`，必须记录为 route drift 并走纠偏或 rerun，不得标记为正常 submitted。
8. 提交后 post-submit gate 已执行；`ask_user` 等待态不得进入 `pending_remote_generation`。
