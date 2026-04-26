# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | `道具清单.md`、`[道具名].md`、`[道具名].json` |
| Output format | Markdown 清单、structured v2 道具设计 Markdown、道具面板 JSON |
| Output path | `projects/aigc/<项目名>/4-设计/` |
| Naming convention | 清单固定名；设计文档和 JSON 同 stem |
| Completion gate | 模板校验、同 stem 回链、review gate 通过 |

## 道具清单.md

```md
# 道具清单

| 道具名 | 道具类型 | 叙事功能 | 证据回链 | 设计状态 |
| --- | --- | --- | --- | --- |
```

## 主体文件

- `[道具名].md` 必须使用 `templates/prop_masterprompt.structured.v2.md`。
- `[道具名].json` 必须使用 `templates/道具面板-提示词.json` 的字段机制。
