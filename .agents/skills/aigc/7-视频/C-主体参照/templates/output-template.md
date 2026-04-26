# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、group index、reference manifest、Dreamina submit plan、queue ledger、results、执行报告 |
| Output format | Markdown + JSON + MP4/video assets |
| Output path | `projects/aigc/<项目名>/7-视频/C-主体参照/第N集/` |
| Naming convention | `第N集-主体参照-video-prompts.md`、`第N集-video-group-index.json`、`第N集-reference-manifest.json`、`第N集-dreamina-submit-plan.json`、`第N集-dreamina-queue.md`、`第N集-dreamina-results.json`、`videos/<分镜组ID>.mp4`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo` |

## Episode Directory Shape

```text
projects/aigc/<项目名>/7-视频/C-主体参照/第N集/
├── 第N集-主体参照-video-prompts.md
├── 第N集-video-group-index.json
├── 第N集-reference-manifest.json
├── 第N集-dreamina-submit-plan.json
├── 第N集-dreamina-queue.md
├── 第N集-dreamina-results.json
├── prompts/
│   └── <分镜组ID>.txt
├── videos/
│   └── <分镜组ID>.mp4
└── 执行报告.md
```

## Execution Report Template

```markdown
# 第N集 C-主体参照执行报告

## Input

- project_root:
- source_group_path:
- mode:
- scope:
- dreamina_self_check:
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

| group_id | command | submit_id | local_status | remote_status | next_action |
| --- | --- | --- | --- | --- | --- |

## Failed Or Skipped

| group_id | status | reason | rework_entry |
| --- | --- | --- | --- |
```
