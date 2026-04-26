# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | prompt 文档、shot index、reference manifest、imagegen plan/result、执行报告 |
| Output format | Markdown + JSON + bitmap image assets |
| Output path | `projects/aigc/[项目名]/6-图像/A-分镜画面`，逐集文件组织在其下的 `第N集/` 子目录 |
| Naming convention | `第N集-分镜画面-prompts.md`、`第N集-shot-index.json`、`第N集-reference-manifest.json`、`第N集-imagegen-plan.json`、`images/<分镜ID>.png`、`执行报告.md` |
| Completion gate | review verdict is `pass` or `pass_with_todo` |

## Episode Directory Shape

```text
projects/aigc/[项目名]/6-图像/A-分镜画面/
└── 第N集/
    ├── 第N集-分镜画面-prompts.md
    ├── 第N集-shot-index.json
    ├── 第N集-reference-manifest.json
    ├── 第N集-imagegen-plan.json
    ├── 第N集-imagegen-results.json
    ├── images/
    │   └── <分镜ID>.png
    └── 执行报告.md
```

## Execution Report Template

```markdown
# 第N集 A-分镜画面执行报告

## Input

- project_root:
- source_group_path:
- north_star_path:
- mode:
- scope:

## Summary

- total_shots:
- prompted:
- generated:
- skipped:
- failed:

## Review

```yaml
verdict:
checked_gates: []
todos: []
```

## Failed Or Skipped

| shot_id | status | reason | rework_entry |
| --- | --- | --- | --- |
```
