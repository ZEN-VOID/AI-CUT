# Output Template

本模板说明 `story-drafting-deepseek` 输出文件结构，并对齐本技能 `SKILL.md` 的 Output Contract。

## Output Contract Alignment

| field | mapping |
| --- | --- |
| Required output | 当前章完整中文小说 Markdown 文件；必要 DeepSeek provider sidecar artifacts。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节正文。 |
| Output path | `projects/story/<项目名>/3-初稿/第N卷/第N章.md`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | DeepSeek provider 真实命中，极简 frontmatter（仅 `写作模型: Deepseek`）/heading/正文校验通过，canonical path 写回完成。 |

## Markdown Skeleton

```markdown
---
写作模型: Deepseek
---

# 第{{chapter_num}}章｜{{chapter_title}}

{{chapter_body}}
```
