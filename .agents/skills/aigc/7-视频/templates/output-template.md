# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | route note、review note 或子技能产物 |
| Output format | Markdown + 子技能 JSON/queue/video assets |
| Output path | `projects/aigc/<项目名>/7-视频/` |
| Naming convention | `执行报告.md`、`validation-report.md` 或子技能命名 |
| Completion gate | route unique and child verdict pass/pass_with_todo |

## Stage Directory Shape

```text
projects/aigc/<项目名>/7-视频/
├── A-分镜画面参照/
├── B-分镜故事板参照/
├── C-主体参照/
└── validation-report.md
```
