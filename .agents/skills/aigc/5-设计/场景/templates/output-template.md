# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | `场景清单.md`、`[场景名].md`、`[场景名].json` |
| Output format | Markdown 清单、structured v2 场景设计 Markdown、场景面板 JSON |
| Output path | `projects/aigc/<项目名>/4-设计/` |
| Naming convention | 清单固定名；设计文档和 JSON 同 stem |
| Completion gate | 模板校验、同 stem 回链、review gate 通过 |

## 场景清单.md

```md
# 场景清单

| 场景名 | 空间类型 | 叙事功能 | 证据回链 | 设计状态 |
| --- | --- | --- | --- | --- |
```

## 主体文件

- `[场景名].md` 必须使用 `templates/scene_masterprompt.structured.v2.md`。
- `[场景名].json` 必须使用 `templates/场景面板-提示词.json` 的字段机制。
