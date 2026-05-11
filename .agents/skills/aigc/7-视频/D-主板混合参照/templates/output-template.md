# Output Template: D-主板混合参照

## Output Contract Alignment

| Output Contract field | Template mapping |
| --- | --- |
| Required output | prompt 包、混合参照 manifest、LibTV submit plan、`*-libtv-submission.txt`、queue ledger、results、执行报告 |
| Output format | Markdown + LibTV submission text + JSON + queue Markdown + MP4 |
| Output path | `projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/` |
| Naming convention | 使用 `第N集-主板混合参照-video-prompts.md`、`prompts/<group_id>-libtv-submission.txt`、`第N集-reference-manifest.json`、`第N集-libtv-submit-plan.json` 等命名；视频文件固定为 `<group_id>.mp4`，同组变体为 `<group_id>-a.mp4`、`<group_id>-b.mp4` |
| Completion gate | source-first enriched YAML、故事板总参照 uploaded_url、主体 uploaded_url、LibTV plan、queue/report 均通过 review；有参照图时 `*-libtv-submission.txt` 首段锁定 `modeType=mixed2video` 和 `mixedList`；默认声明 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false` |

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

<直接保留 4-分组中该组原文；仅在 fenced YAML 内注入故事板参照.uploaded_url 和主体 uploaded_url>
```

## LibTV Submission Block

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: mixed2video
mixedList: [{"url": "<uploaded_url_1>", "type": "image"}, {"url": "<uploaded_url_2>", "type": "image"}, ...]
mixedList 单个分镜组最多 9 张图；故事板总参照与主体参照共同计入上限；提交文本不得预设“参照图1/2/N”人工编号。
duration: <duration_hint>
duration_rule: 从当前分镜组时长估算计算；小于等于4秒按4秒，4到15秒之间按估算值，大于等于15秒按15秒。
ratio: 16:9
resolution: 720p
enableSound: on
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。

【直接生成请求】
请基于下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `故事板参照.uploaded_url` 和主体列表项 `uploaded_url` 已绑定对应故事板总参照与主体参照图；请把原始正文和 YAML uploaded_url 绑定关系共同作为生成 prompt 完整体。不要自行写“参照图1/2/N”编号；如系统自动插入真实图片 token 或编号，必须把故事板身份或主体名放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<source-first enriched YAML 分镜组全文>
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
