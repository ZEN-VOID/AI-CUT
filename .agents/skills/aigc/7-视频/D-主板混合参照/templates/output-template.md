# Output Template: D-主板混合参照

## Output Contract Alignment

| Output Contract field | Template mapping |
| --- | --- |
| Required output | prompt 包、混合参照 manifest、LibTV submit plan、`*-libtv-submission.txt`、queue ledger、results、执行报告 |
| Output format | Markdown + LibTV submission text + JSON + queue Markdown + MP4 |
| Output path | `projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/` |
| Naming convention | 使用 `第N集-主板混合参照-video-prompts.md`、`prompts/<group_id>-libtv-submission.txt`、`第N集-reference-manifest.json`、`第N集-libtv-submit-plan.json` 等命名；视频文件固定为 `<group_id>.mp4`，同组变体为 `<group_id>-a.mp4`、`<group_id>-b.mp4` |
| Completion gate | 固定开头、故事板总参照、主体后缀参照、LibTV plan、queue/report 均通过 review；有参照图时 `*-libtv-submission.txt` 首段锁定 `modeType=mixed2video` 和 `mixedList`；默认声明 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false` |

## Runtime Layout

```text
projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/
├── 第N集-hybrid-group-index.json
├── 第N集-主板混合参照-video-prompts.md
├── 第N集-reference-manifest.json
├── 第N集-libtv-submit-plan.json
├── 第N集-libtv-queue.md
├── 第N集-libtv-results.json
├── 执行报告.md
├── prompts/
│   ├── <group_id>.txt
│   └── <group_id>-libtv-submission.txt
└── <group_id>.mp4
```

## Prompt Block

```markdown
## <group_id>

请参考故事板总参照图作为本分镜组的整体构图、镜头顺序、角色站位、场景连续性与情绪节奏参考；不要把故事板参照当作单一首帧。后文每个主体名称后的 @参照图 用于锁定对应角色、场景或道具外观，不得互相替换。根据以下完整分镜组内容生成一条连续视频。保持分镜顺序、角色动作、镜头运动、场景与情绪连续；不生成字幕，不生成BGM，保留物理互动音效与环境音。

故事板总参照：@图1 -> <storyboard_path 或 缺失说明>

主体参照：
- 角色：<name> @图2（<path>）
- 场景：<name> @图3（<path>）
- 道具：<name> @图4（<path>）

<完整 4-分组组正文>
```

## LibTV Submission Block

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
主体名：参照图2 <subject_uploaded_url>

【直接生成请求】
请基于【混合参照说明】（包含故事板总参照、主体名、主体类别、参照图编号和主体参照 URL）和下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。请直接把【混合参照说明】中与本组相关的故事板总参照绑定关系、主体名/参照图绑定关系 + 【分镜组源文本】原文作为生成 prompt 完整体。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<完整 4-分组组正文>
```

## Report Block

```markdown
# 第N集 D-主板混合参照执行报告

## Verdict

- verdict:
- processed_groups:
- submitted:
- skipped:
- failed:

## Reference Summary

| group_id | storyboard | subjects_bound | missing | over_limit |
| --- | --- | --- | --- | --- |

## Queue Summary

| group_id | sessionId | local_status | remote_status | next_action |
| --- | --- | --- | --- | --- |
```
