# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | `角色清单.md`、`[角色名].md`、`[角色名].json` |
| Output format | Markdown 清单、structured v2 角色设计 Markdown、角色面板 JSON |
| Output path | `projects/aigc/<项目名>/4-Design/` |
| Naming convention | 清单固定名；设计文档和 JSON 同 stem |
| Completion gate | 模板校验、同 stem 回链、review gate 通过 |

## 角色清单.md

```md
# 角色清单

| 角色名 | 身份层级 | 服装状态 | 证据回链 | 设计状态 |
| --- | --- | --- | --- | --- |
```

## 主体文件

- `[角色名].md` 必须使用 `templates/character_masterprompt.structured.v2.md`。
- `[角色名].json` 必须使用 `templates/角色面板-提示词.json` 的字段机制。
