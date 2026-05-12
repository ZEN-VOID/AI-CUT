# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 分镜组 canonical package、集级 summary、生成视频 |
| Output format | Markdown + JSON + MP4/video assets |
| Output path | canonical: `projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/<分镜组ID>/`; summary: `projects/aigc/<项目名>/7-视频/C-主体参照/第N集/` |
| Naming convention | compact group package: `reference-manifest.json`、`prompt.md`、`libtv-submission.txt`、`libtv-submit-plan.json`、`queue.md`、`libtv-results.json`、`执行报告.md`、`<分镜组ID>.mp4`; optional full-trace: `debug/attempts/<attempt_id>/*`; episode summary: `第N集-*.json/md` |
| Canvas link | Markdown 报告、queue summary 和最终用户回执必须返回可直接打开的 `[打开画布](<projectUrl>)`；JSON 同时保留 `projectUrl` 与 `canvasMarkdown` |
| Completion gate | review verdict is `pass` or `pass_with_todo` |
| Reference prompt integrity | manifest、prompt、remote submission、submit plan 四者必须互证图片引用；同画布复用 URL 必须通过 project scope 与 active registry 校验；未声明共享关系时不得重复 URL |
| Audio acceptance | `enableSound:on` 只记录请求；交付必须有 `task_result.audios`、音频 URL 或 `ffprobe` 音轨证据 |

## Episode Directory Shape

```text
projects/aigc/<项目名>/7-视频/C-主体参照/第N集/
├── groups/
│   └── <分镜组ID>/
│       ├── reference-manifest.json
│       ├── prompt.md
│       ├── libtv-submission.txt
│       ├── libtv-submit-plan.json
│       ├── queue.md
│       ├── libtv-results.json
│       ├── debug/                         # optional; only artifact_mode=full_trace
│       │   └── attempts/<attempt_id>/
│       ├── <分镜组ID>.mp4
│       └── 执行报告.md
├── 第N集-主体参照-video-prompts.md      # summary only
├── 第N集-video-group-index.json        # summary only
├── 第N集-reference-manifest.json       # summary only
├── 第N集-libtv-submit-plan.json        # summary only
├── 第N集-libtv-queue.md                # summary only
├── 第N集-libtv-results.json            # summary only
└── 执行报告.md                          # episode summary
```

## Compact Artifact Rule

- `reference-manifest.json` 统一承载 `group_source`、`yaml_subjects`、`bound_references`、`missing_references`、`asset_uploads`、`generation_slots` 和 `review_snapshot`。
- `libtv-results.json` 统一承载 `attempts[]`：每次 `change_project / upload_file / create_session / query_session / gate / reference_order` 的摘要、状态、关键 URL、错误码和可选 `raw_artifact_path`。
- group 根目录不得默认平铺 `latest-*`、`post-submit-*`、`corrected-*`、`followup-*`、`upload-*.json`、`create-session*.json` 或 `change-project.json`。
- 只有排障、复盘或用户要求 full trace 时，才把原始回显写入 `debug/attempts/<attempt_id>/`；否则只写入 `libtv-results.json.attempts[].raw_summary`。

## Execution Report Template

```markdown
# 第N集 C-主体参照执行报告

## Input

- project_root:
- source_group_path:
- mode:
- scope:
- libtv_self_check:
- parallelism:

## Summary

- total_groups:
- prompted:
- submitted:
- queued:
- downloaded:
- skipped:
- failed:
- missing_references:
- reference_prompt_integrity:
- audio_acceptance:

## Review

```yaml
verdict:
checked_gates: []
todos: []
```

## Queue Snapshot

| group_id | command | sessionId | local_status | remote_status | next_action |
| --- | --- | --- | --- | --- | --- |

## Canvas Links

| group_id | canvas_link |
| --- | --- |

## Failed Or Skipped

| group_id | status | reason | rework_entry |
| --- | --- | --- | --- |
```
