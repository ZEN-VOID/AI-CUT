# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 分镜组 canonical package、集级 summary、生成视频 |
| Output format | Markdown + JSON + MP4/video assets |
| Output path | canonical: `projects/aigc/<项目名>/7-视频/C-主体参照/第N集/groups/<分镜组ID>/`; summary: `projects/aigc/<项目名>/7-视频/C-主体参照/第N集/` |
| Naming convention | group package: `group-index.json`、`reference-manifest.json`、`prompt.md`、`source-group-body.md`、`libtv-submission.txt`、`libtv-submit-plan.json`、`queue.md`、`libtv-results.json`、`执行报告.md`、`<分镜组ID>.mp4`; episode summary: `第N集-*.json/md` |
| Canvas link | Markdown 报告、queue summary 和最终用户回执必须返回可直接打开的 `[打开画布](<projectUrl>)`；JSON 同时保留 `projectUrl` 与 `canvasMarkdown` |
| Completion gate | review verdict is `pass` or `pass_with_todo` |

## Episode Directory Shape

```text
projects/aigc/<项目名>/7-视频/C-主体参照/第N集/
├── groups/
│   └── <分镜组ID>/
│       ├── group-index.json
│       ├── reference-manifest.json
│       ├── source-group-body.md
│       ├── prompt.md
│       ├── libtv-submission.txt
│       ├── libtv-submit-plan.json
│       ├── queue.md
│       ├── libtv-results.json
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
