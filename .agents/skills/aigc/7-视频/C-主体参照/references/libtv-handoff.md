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

1. `python3 .agents/skills/cli/libTV/scripts/change_project.py`：新建主体参照视频任务时必须先执行，或由用户显式指定一个可继续使用的 existing `projectUuid/projectUrl`；把锁定后的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report；Markdown 输出同时写 `canvas_link: [打开画布](<projectUrl>)`。
2. `python3 .agents/skills/cli/libTV/scripts/upload_file.py <path>`：在上述 `projectUuid` 已锁定后上传主体、场景、道具参照，保存返回的 OSS URL；每个 uploaded URL 的 `/claw/<projectUuid>/` 必须与 submit plan 中锁定的 `projectUuid` 一致。上传脚本返回值只视为裸 URL，C 技能必须在 `reference-manifest.json.asset_uploads` 记录 `yaml_name -> uploaded_url` 身份映射；OSS 上传顺序本身不得被当作图N顺序真源。`upload-*.json` 原始回显只在 `artifact_mode=full_trace` 时写入 `debug/attempts/<attempt_id>/`。
3. `python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `python3 .agents/skills/cli/libTV/scripts/query_session.py <sessionId> --project-id <projectUuid>`：提交后必须立即查询一次，并用 `scripts/detect-libtv-stall.py` 与 `scripts/validate-post-submit-reference-order.py` 执行 post-submit gate；通过后才进入正常轮询。
5. `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <group_package_dir> --filename <group_id>.mp4`：生成完成后自动下载到本技能的分镜组包目录，并使用精确文件名避免生成 `<group_id>_01.mp4`。
6. 下载后必须对 `<group_id>.mp4` 运行音轨探测，例如 `ffprobe -v error -select_streams a -show_entries stream=index,codec_type,codec_name -of json <video>`；没有音频 stream 时，状态必须写成 `audio_missing / no_audio_stream`，不得交付。

无参照图时跳过 `upload_file.py`，其余顺序不变。禁止先上传图片再切换画布；否则 LibTV UI 自动生成的 `图片N` token 可能和主体说明脱节。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、上传参照、生成节点和结果都应保留在同一 `projectUrl`。
- 有主体参照图时，上传 URL 的 `claw` project scope、submit plan `projectUuid`、queue `projectUuid` 和 `create_session.py` 返回的 `projectUuid` 必须一致；不一致时状态写成 `reference_project_scope_mismatch`，不得提交或继续等待。
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

## Audio Control Policy

- C 路线默认请求有声视频；远端提交必须保留 `enableSound:on`、声音/音效要求和禁止 BGM 要求。
- 当前 `.agents/skills/cli/libTV/scripts/create_session.py` 只向 Agent-IM 发送消息，本地 CLI 本身没有独立的 `--enable-sound` 或等价音频开关。若不能在生成前验证 `create_generation_task.params.enableSound`，记录为 `audio_preflight_unverified_non_blocking`，但不得因此阻断提交。
- 若后续 query 能看到 `create_generation_task.params.enableSound`，应记录其值；字段缺失或关闭只作为音频风险，不再作为提交失败。
- 生成后仍需音频验收：优先记录 `task_result.audios` 或音频 URL；下载后用 `ffprobe` 检查音轨。若最终无音轨，结果不得判定为完整通过，应写为 `audio_missing` 或 `audio_unverified` 并进入返工。

强制要求：

- 消息第一段必须是 `video-prompt-assembly-contract.md#LibTV Remote Opening` 中的 `【LibTV 调用锁定】`。
- 默认远端 handoff 必须采用 `strict_original + transport_only`：`prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false`。默认不允许 LibTV 优化、润色、压缩、摘要、重排或改写提示词表达。
- `strict_original` 表示 source-first enriched YAML 分镜组全文是生成 prompt 的事实真源：分镜组标题、正文、原 YAML 字段、对白、旁白、音效文字和主体 URL 绑定必须保真；远端只可执行技术投影和生成，不得改写台词、音效文字、主体绑定、分镜顺序、画面表达或视频参数。
- `transport_only` 只允许上传 URL、`mixedList`、时长、比例、分辨率、声音等技术投影；不得改变分镜事实、镜头顺序、角色动作、对白、音效文字或主体绑定。
- `prompt.md` 和 submit plan 必须声明槽位绑定相位：`slot_binding_phase=draft` 时只允许保留未绑定 YAML 和上传/匹配证据，不得创建最终远端提交；`slot_binding_phase=final` 时必须已用最终 `generation_slots` 回刷 YAML `reference_index + uploaded_url + portrait_token`，才可提交或重提。
- 时长投影必须使用当前分镜组的 `duration_hint`，不得固定写 15 秒；`duration_hint=clamp(duration_estimate_seconds, 4, 15)`。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=controlled_libtv_optimize` 或更强 `prompt_fidelity_mode=libtv_optimize` 时，才允许 LibTV 做远端提示词优化；即便 opt-in，也不得改写对白、旁白或音效文字。
- provider 参数前必须包含 no-ask 约束：禁止 `ask_user`、禁止确认、禁止展示“请稍候”、禁止等待下一条消息，并声明用户已授权立即生成；无法创建生成节点时直接返回 `ERROR_NO_GENERATION_NODE`。
- 有主体参照图时，必须明确 `provider=seedance2.0`、`taskType=video`、`modeType=mixed2video`、`mixedList=[{"url": "<真实 uploaded_url>", "type": "image"}]`。`mixedList` 必须是严格 JSON 对象数组，不得保留 `参照图N URL` 或 `<uploaded_url>` 占位符，不得写成 `image2video`、`singleImage2video` 或 `frames2video`。
- 单个分镜组 `mixedList` 最多 9 张图；当可用参照超过 9 张时，先从道具取舍，其次再考虑重复/不必要场景或次要主体。被取舍的主体只保留在本地 manifest / report 与源文本约束中，不进入 `mixedList`，也不得写入远端 `libtv-submission.txt` 的缺图/未入预算说明行。
- final 相位的 `mixedList`、submit plan `images[]` 和 source-first enriched YAML 的 `reference_index / uploaded_url / portrait_token` 必须完全一致：以 `reference-manifest.json.generation_slots` 为槽位注册真源，按 `reference_index` 排序后的主体名和 URL 必须逐项一致、每个 URL 邻近对应主体名、`reference_index` 等于 `images[].upload_index` 且对应 `mixedList[reference_index-1]`，未声明共享关系时 URL 不得重复，每个 uploaded URL 的 `/claw/<projectUuid>/` 与本任务画布 `projectUuid` 一致。若出现已绑定主体同时列入缺图、同一 URL 静默绑定多个主体、YAML `reference_index/name/uploaded_url` 与最终槽位注册表不一致、或 URL project scope 与会话画布不一致，必须判定为 `reference_prompt_integrity_error / reference_project_scope_mismatch`，不得提交或继续等待。
- LibTV UI 的 `{{Portrait N}}`、`{{Image N}}`、`图片N` 或等价系统 token 是生成框实际槽位证据：`reference_index=1` 对应 UI 图1 / `Portrait 1`，`reference_index=2` 对应 UI 图2 / `Portrait 2`。本地 YAML 的 canonical `uploaded_url` 必须是真实上传 URL，不得把 `uploaded_url` 改成占位符；可额外写 `portrait_token` 记录 UI 槽位。远端 prompt 中若出现系统 token，必须邻近对应主体名与 `reference_index`。人工排查时以视频生成框 UI 缩略图槽位回写 `reference-manifest.json.generation_slots`；工具层 `create_generation_task.params.mixedList` 只作校验项，不能覆盖已观测 UI 槽位。
- 源层规则：`asset_uploads` 只证明“哪个 YAML name 对应哪个 OSS URL”；`generation_slots` 才证明“图N/Portrait N/mixedList[n] 对应哪个 OSS URL 和 YAML name”。最终匹配目标是 LibTV 端视频生成时实际传入的参照图 URL 与 YAML 中 `@` 或 `uploaded_url` 对应名称同槽一致。若视频生成框 UI 槽位与本地预期不同，必须以 UI 图N 反查或人工确认 name-URL 后，回刷 YAML 的 `reference_index=N`、`portrait_token` 和真实 `uploaded_url` 后重新提交；只有 UI 槽位不可观测时才使用远端 query 的实际 `mixedList[n].url` 反查 `asset_uploads`。不得继续沿用旧 YAML 顺序。
- 远端 `create_generation_task` 工具 envelope 只作为 query 后观测项。`task_type`、字符串型 `params` 等字段变体不得单独判死；只有明确 tool error、`params is required`、无生成节点超时或主体名绑定丢失时，才记录为失败。C 路线本地真源只裁决投递文本中的主体名+URL绑定、`mixedList`、时长、比例、分辨率、声音请求和源文本保真。
- 无主体参照图时，必须明确 `modeType=text2video`。
- 已上传图片必须以原组 YAML 的 `name + reference_index + uploaded_url` 对象项出现在远端消息中；不得额外生成长篇主体参照说明，不得在每个主体行后重复连续性长句，不得脱离 YAML 另造 `参照图1/2/N` 映射，也不得只有裸图片 token 或裸 URL。
- 远端消息不得包含 `@projects/...`、绝对本地路径、`prompt_path`、`reference-manifest` 路径或其他本地文件路径；这些只写入本地 plan / queue / report。
- `分镜组源文本` 必须说明它是连续视频的镜头文字约束，不是图片生产清单；`【直接生成请求】` 必须写成“在严格原文模式下，基于下方【分镜组源文本】原始正文及其 YAML uploaded_url 主体绑定”，不得只写“基于上述主体参照 URL”。
- `【直接生成请求】` 不写“不生成字幕，不生成背景音乐”句；字幕/BGM 类视频规格只写在 `【视频默认规格】`、源文本或 provider 参数区。
- 参照连续性不得单独列 `【参照连续性总领】` 标题；连续性句只出现一次，并入 `【直接生成请求】` 或首段生成请求，位置在 `【分镜组源文本】` 前；缺图、无可复用 URL、未进入预算或被取舍主体不得进入远端消息，只能写在本地 manifest / submit plan / report。
- 远端 `create_generation_task.params.prompt` 必须保留主体名、`reference_index` 与图片 token/编号/URL 绑定；只有当 LibTV 自动插入真实图片编号后，才把主体名和 `reference_index` 邻近该真实编号，例如 `任盈盈 reference_index=1 {{Image 1}}` 或 `{{Image 1}} 任盈盈 reference_index=1`。不得把参照区压成 `{{Image 1}} {{Image 2}} ...`、`图片1 图片2 ...` 或裸 URL 列表。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前改写台词、删改音效文字、改变主体绑定、改变分镜顺序、优化提示词表达，或执行重新编排/摘要/镜头计划且本地未 opt-in `controlled_libtv_optimize` 或更强 `libtv_optimize`，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。
- 若远端 query 显示 `create_generation_task` tool error 为 `params is required` 或其他明确工具错误，必须判定为 `generation_tool_error`；仅出现 `task_type`、字符串型 `params` 等 envelope 变体但无明确错误时，只记录 `generation_envelope_variant`，不得因此阻断正常轮询。
- 若远端 query 显示 `create_generation_task.params.prompt` 只含裸图片 token/编号/URL，未邻近主体名称，必须判定为 `subject_reference_name_stripped`；不得把该 session 标为正常 pending。
- 若远端代理改用 `image2video`、`singleImage2video`、`frames2video`，或画布结构出现“多张参照图分别输出视频再合成”，应判定为 route drift；C 路线有图时只能接受 `mixed2video + mixedList`。
- 若提交触发或任意轮询返回“内容不符合平台规则”，不得中止任务、不得把画布空置视为完成、不得要求用户手动改稿；必须判定为 `platform_policy_rejected / needs_moderation_safe_rerun`，自动执行“平台安全重提”。安全版只改远端提交文本：保留 `group_id`、source-first 事实、主体 `reference_index + uploaded_url`、`mixedList` 顺序、duration、ratio、resolution、enableSound 和镜头顺序；对远端可见的辱骂、过细暴力、儿童/老人伤害、女性贩卖/剥削等平台高风险表达做最小降敏。优先向同一 `sessionId/projectUuid` 追加安全版；若同一会话继续被拦截或无法产生生成节点，再新建干净画布重提。原始 `4-分组` 和 canonical `prompt.md` 不因此改写；安全版路径、拦截原因、重提状态必须写入 submit plan、queue、`libtv-results.json.attempts[]` 和执行报告。
- 若提交后第一轮 query 发现 assistant 内容为空且 `toolCalls.name == ask_user`，或 tool 消息要求“展示 question / 等待用户下一条消息 / 请稍候”，必须判定为 `stalled_remote_ask_user`；不得标记为 `pending_remote_generation`，不得继续等待同一 session。

## Default Parameters

- `requested_model`: 默认为空，表示使用 LibTV 后端默认视频路由。用户显式指定模型时，原样写入自然语言任务。
- `duration_estimate_seconds`: 默认从 `4-分组` 组底 YAML 的 `时长估算` 读取；缺失时按组内分镜秒数求和，区间取上限，仍无法确定才回退 15 秒并记录原因。
- `duration_hint`: 必须写入远端提交；按 `clamp(duration_estimate_seconds, 4, 15)` 计算，小于等于 4 秒用 4 秒，4 到 15 秒之间用估算值，大于等于 15 秒用 15 秒。
- `ratio_hint`: 默认 `16:9`，必须写入远端提交。
- `video_resolution_hint`: 默认 `720p`，即用户可见规格 720P，必须写入远端提交。
- `enableSound`: 默认 `on`，必须写入远端提交。
- `audio_preflight`: 默认写入 `enableSound:on`；若生成前不可验证，记录 `audio_preflight_unverified_non_blocking` 并继续提交。
- `audio_acceptance`: 可下载视频 URL 不能单独构成音频成功；应有 `task_result.audios` 非空、音频 URL 证据，或下载后 `ffprobe` 证明 MP4 含音频 stream。缺少音频证据时结果为 `audio_unverified`，确认无音轨时为 `audio_missing`。
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
      "prompt_fidelity_mode": "strict_original",
      "allow_libtv_prompt_optimization": false,
      "transport_only_projection": true,
      "duration_source": "group_yaml",
      "duration_estimate_seconds": 12,
      "duration_rule": "clamp(duration_estimate_seconds, 4, 15)",
      "duration_hint": 12,
      "ratio_hint": "16:9",
      "video_resolution_hint": "720p",
      "slot_binding_phase": "final",
      "generation_slot_source": "ui_thumbnail_order | post_submit_mixedList | submit_plan_expected_order",
      "prompt_path": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1/prompt.md",
      "remote_submission_path": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/groups/1-1-1/libtv-submission.txt",
      "reference_image_budget": {
        "max_images": 9,
        "selection_rule": "角色和场景优先；超过上限时先从道具取舍，其次再考虑其他不必要主体。",
        "excluded_due_to_budget": []
      },
      "images": [
        {
          "upload_index": 1,
          "reference_index": 1,
          "oss_upload_index": 1,
          "name": "林寂",
          "category": "character",
          "path": "projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png",
          "reuse_policy": "same_canvas_active_url",
          "asset_registry_lookup_key": "<projectUuid>|character|林寂",
          "source_sha256": "",
          "source_size_bytes": 0,
          "source_mtime_ns": 0,
          "uploaded_url": "",
          "portrait_token": "{{Portrait 1}}",
          "slot_source": "ui_thumbnail_order | post_submit_mixedList | submit_plan_expected_order",
          "subject_inline": "林寂 reference_index=1 uploaded_url portrait_token={{Portrait 1}}"
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

默认 `artifact_mode=compact`。submit plan 不再要求 `group-index.json`、`source-group-body.md` 或独立 `upload-ledger.json` 落盘；这些字段归并到 `reference-manifest.json`。需要排障时可切换 `artifact_mode=full_trace`，把原始命令回显写入 `debug/attempts/<attempt_id>/`。

## Script Rendering

有参照图：

```bash
python3 .agents/skills/cli/libTV/scripts/change_project.py
python3 .agents/skills/cli/libTV/scripts/upload_file.py "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
python3 .agents/skills/cli/libTV/scripts/upload_file.py "projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png"
python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1/libtv-submission.txt)"
python3 .agents/skills/cli/libTV/scripts/query_session.py "<sessionId>" --project-id "<projectUuid>"
python3 .agents/skills/cli/libTV/scripts/download_results.py "<sessionId>" --output-dir "projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1" --filename "1-1-1.mp4"
ffprobe -v error -select_streams a -show_entries stream=index,codec_type,codec_name -of json "projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1/1-1-1.mp4"
```

final prompt 文件中必须包含按最终 `generation_slots` 回刷后的上传 URL、reference_index 和可选 portrait_token；draft prompt 不得提前写死这些字段。例如：

```text
林寂：reference_index=1 uploaded_url=<真实URL> portrait_token={{Portrait 1}}
永夜私立中学二年级A班教室：reference_index=2 uploaded_url=<真实URL> portrait_token={{Portrait 2}}
```

无参照图：

```bash
python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1/libtv-submission.txt)"
python3 .agents/skills/cli/libTV/scripts/query_session.py "<sessionId>" --project-id "<projectUuid>"
python3 .agents/skills/cli/libTV/scripts/download_results.py "<sessionId>" --output-dir "projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/1-1-1" --filename "1-1-1.mp4"
```

## Queue Ledger

任何提交、排队或待下载任务都必须先写入分镜组包内的 `groups/<分镜组ID>/queue.md`。集级 `第N集-libtv-queue.md` 只作为汇总视图，指向每个 group queue：

| queue_id | group_id | command | sessionId | projectUuid | canvas_link | local_status | remote_status | last_checked_at | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

`sessionId` 缺失时该行状态只能是 `planned`、`blocked` 或 `submit_failed`。

## Post Submit Gate

提交后必须运行，并按 `artifact_mode` 持久化：

```bash
python3 .agents/skills/cli/libTV/scripts/query_session.py "<sessionId>" --project-id "<projectUuid>"
python3 .agents/skills/aigc/7-视频/C-主体参照/scripts/detect-libtv-stall.py "<query-json>"
python3 .agents/skills/aigc/7-视频/C-主体参照/scripts/validate-post-submit-reference-order.py "<package_dir>" "<query-json>"
```

- `compact`：query 摘要、stall gate、reference-order gate、tool envelope 变体、错误码和关键 URL 写入 `libtv-results.json.attempts[]`，不在 group 根目录额外生成 `post-submit-query.json / post-submit-reference-order.json / *-gate.json`。
- `full_trace`：原始 query 和 gate 输出写入 `debug/attempts/<attempt_id>/query.json`、`stall-gate.json`、`reference-order.json`，`libtv-results.json.attempts[]` 只保存摘要和相对路径。

判定规则：

- 若存在可下载视频 URL、生成任务工具调用或明确的生成中工具消息，状态可进入 `pending_remote_generation`。
- 若存在可下载视频 URL，但 `task_result.audios` 为 `[]`、没有音频 URL，且尚未下载并通过 `ffprobe` 音轨检查，状态必须写成 `audio_unverified` 或 `audio_missing`，不得写成 `generated`、`downloaded`、`pass` 或 `pending_remote_generation`。
- 若下载后的视频没有音频 stream，状态必须写成 `audio_missing / no_audio_stream`，并进入 rerun；不得用后期静音视频补声来覆盖本阶段失败，除非用户显式改为后期配音/配乐流程。
- 若 query 中远端实际 `create_generation_task.params.enableSound` 缺失、关闭或不可解析，状态写成 `audio_preflight_unverified_non_blocking` 并继续按正常生成状态追踪；最终交付仍依赖生成后音频验收。
- 若未 opt-in `controlled_libtv_optimize` 或 `libtv_optimize`，但 query 显示远端 assistant 先产出优化版提示词、重新编排脚本、镜头计划、摘要版分镜或任何表达层优化，再试图创建任务，状态必须写成 `prompt_fidelity_violation / libtv_optimize_without_opt_in`，并停止等待该 session。
- 若 tool 消息返回 `params is required` 或其他明确 tool error，状态必须写成 `generation_tool_error`，并停止把该 session 当作正常生成队列等待；query 中仅出现 `task_type`、字符串型 `params` 等 envelope 变体时，只记录 `generation_envelope_variant`，继续按是否有生成节点、视频 URL 和音频证据裁决。
- 若 query 中的 `create_generation_task.params.prompt` 将参照部分压成裸 `{{Image N}}`、裸 `图片N` 或裸 URL 列表，没有主体名称邻近绑定，状态必须写成 `subject_reference_name_stripped / prompt_reference_binding_lost`，并停止把该 session 当作正常生成队列等待。
- 若 query 中的 `create_generation_task.params.mixedList` 或 `imageList` 顺序与本地最终 `generation_slots` 顺序不同，或 `modeType` 不是 `mixed2video`，状态必须写成 `reference_order_mismatch / route_drift`，并停止把该 session 当作正常生成队列等待；若本地最终 `generation_slots` 来自用户截图或 UI 缩略图确认，以该 UI 槽位顺序为准。纠偏时必须先回到 `asset_uploads` 做 `uploaded_url -> name` 反查，再重建 final YAML，不得用原 YAML 文本顺序覆盖 UI 图N顺序。
- 若第一轮 query 尚未出现 `create_generation_task`，`validate-post-submit-reference-order.py` 可输出 `pending`；一旦 query 观测到生成工具调用，远端顺序校验必须为 `pass` 才能继续正常轮询。
- 若 query 返回“内容不符合平台规则”，状态必须写成 `platform_policy_rejected / needs_moderation_safe_rerun` 并立即自动重提安全版；该状态不作为终止态。安全版重提后若看到生成任务工具调用、生成中工具消息或视频 URL，恢复正常轮询；若安全版仍被平台拒绝，状态升级为 `blocked_platform_moderation_after_safe_rerun`，并保留人工画布路径或进一步降敏入口。
- 若出现 `ask_user` 等待态，状态必须写成 `stalled_remote_ask_user / no_generation_node`，并停止等待该 session。
- 若 no-ask rerun 仍触发 `ask_user`，状态升级为 `blocked_agent_im_stall`，需要换 LibTV 直达生成接口或人工画布路径。
- 同一个 stalled session 不再作为恢复目标；恢复必须新建干净 session，并使用更短的 no-ask 远端提交文本。

## Concurrency Rules

- 并发只发生在 LibTV 上传、创建会话或查询层；每个 worker 只能写自己的 `groups/<分镜组ID>/` package，不得改写其他组的 prompt、manifest、plan、queue、results 或 report。compact 模式下，worker 不得在 group 根目录写临时 `latest-* / corrected-* / followup-* / post-submit-*` 文件；多轮状态必须追加到 `libtv-results.json.attempts[]`。
- 集级 `group-index`、`reference-manifest`、submit plan、queue、results 和最终 `执行报告.md` 必须在汇流阶段串行重建，作为派生 summary。
- 若并发提交任一组失败，不影响其他组继续，但最终报告必须列出失败组和重试命令。

## Gate

通过 LibTV handoff 必须满足：

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 每个 runnable group 有合法命令和非空 prompt。
3. 有参照图时 `images[]` 本地路径都存在，且已记录 `uploaded_url` 或上传失败原因。
4. 无参照图时命令为 `libtv_session_text_only`，不传空图片槽。
5. `mixedList` 不超过单组 9 图上限；超过上限时已优先从道具取舍并记录 `excluded_due_to_budget`。
6. 任务状态可通过 queue ledger 续查。
7. 远端提交 prompt 已通过直接生视频开头检查，且不含本地图片路径。
8. 默认提交 prompt 已声明 `strict_original + transport_only`，且 submit plan 中 `allow_libtv_prompt_optimization=false`，同时硬锁定分镜正文、对白、旁白、音效文字和主体绑定。
9. 有主体参照图时远端若没有锁定 `modeType=mixed2video` 和 `mixedList`，必须记录为 route drift 并走纠偏或 rerun，不得标记为正常 submitted。
10. 远端工具 envelope 变体只记录为观测项；明确 tool error、`params is required`、`ask_user`、无生成节点超时或主体名绑定丢失才阻断。
11. 远端提交文本请求 `enableSound:on`；若当前调用面无法生成前验证，则记录 `audio_preflight_unverified_non_blocking`，不阻断提交。最终音频成败由生成后音频 URL / `task_result.audios` / `ffprobe` 验收裁决。
12. 远端工具 prompt 保留主体名、reference_index 与图片 token/编号/URL 绑定，提交文本未脱离 YAML 另造 `参照图N` 映射，且不存在裸图片 token 序列。
13. 同画布 active uploaded URL 复用证据成立；所有 uploaded URL 的 `/claw/<projectUuid>/` 与 submit plan `projectUuid` 一致。图片已调整或用户显式要求替换时，必须重新上传并更新 active URL。
14. prompt 引用一致性已通过；同一主体不得同时已绑定和缺图，final YAML 按 `reference_index` 排序后的 `uploaded_url`、`mixedList` 和 `images[]` URL 逐项顺序一致，未声明共享时不得重复 URL；远端提交不得包含“无独立参照图 / 无可复用 URL / 未进入预算主体 / 不创建空图片槽”等缺图列表。draft 相位允许 YAML 未绑定，但不得作为最终远端提交。
15. 提交后 post-submit gate 已执行；若远端已出现 `create_generation_task`，`params.mixedList` / `imageList` 顺序必须与本地最终 `generation_slots` 完全一致，且 `modeType=mixed2video`。若 UI 截图或视频生成框缩略图已确认槽位，UI 图N顺序高于 submit plan 初始顺序和旧工具回显。`ask_user` 等待态、未 opt-in 的 prompt 优化、明确生成工具错误、主体名绑定丢失、远端参照顺序错位、音频缺失或音频未验证不得进入完成态。音频预检不可验证只记录风险，不阻断提交或排队。
16. `生成时保持` 连续性句在远端提交中最多出现一次，并且必须并入 `【直接生成请求】` 或首段生成请求，不得单独列 `参照连续性总领` 标题，也不得附着在每个角色、场景或道具 URL 行。
