# Output Template

本模板说明 `story-polishing-gpt-native` 输出文件结构，并对齐本技能 `SKILL.md` 的 Output Contract。

## Output Contract Alignment

| field | mapping |
| --- | --- |
| Required output | 基于 `3-初稿/第N卷/第N章.md` 二次改写后的完整中文小说 Markdown 文件。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节润色稿。 |
| Output path | `projects/story/<项目名>/4-润色/第N卷/第N章.md`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | GPT 原生润色完成，极简 frontmatter（`润色模型: GPT` + `初稿来源`）/heading/正文校验通过，canonical path 写回完成。 |

## Markdown Skeleton

```markdown
---
润色模型: GPT
初稿来源: "{{draft_source_ref}}"
---

# 第{{chapter_num}}章｜{{chapter_title}}

{{chapter_body}}
```
