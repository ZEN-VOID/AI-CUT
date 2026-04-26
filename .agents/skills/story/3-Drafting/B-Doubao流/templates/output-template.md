# Output Template

本模板说明 `story-drafting-doubao` 输出文件结构，并对齐本技能 `SKILL.md` 的 Output Contract。

## Output Contract Alignment

| field | mapping |
| --- | --- |
| Required output | 当前章完整中文小说 Markdown 文件；必要 provider sidecar artifacts。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节正文。 |
| Output path | `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | provider 真实命中，frontmatter 可解析且关键摘要非空，heading/正文完整度校验通过，canonical path 写回完成；覆盖已有章节时必须有 backup sidecar。 |

## Markdown Skeleton

```markdown
---
story_name: "{{story_name}}"
volume_num: {{volume_num}}
chapter_num: {{chapter_num}}
chapter_title: "{{chapter_title}}"
planning_global_ref: "2-Planning/整体规划.md"
planning_volume_ref: "2-Planning/第{{volume_num}}卷/卷规划.md"
planning_chapter_ref: "2-Planning/第{{volume_num}}卷/第{{chapter_num}}章.md"
写作模型: Doubao
rhythm_type: "{{rhythm_type}}"
global_card_refs: []
style_card_refs: []
north_star_ref: "0-Init/north_star.yaml"
project_context_refs: []
previous_chapter_ref: ""
global_context:
  worldview_summary: ""
  rule_pressure: ""
  faction_or_system_pressure: ""
style_context:
  tone_summary: ""
  prose_summary: ""
  dialogue_summary: ""
north_star_chapter_brief: ""
---

# 第{{chapter_num}}章｜{{chapter_title}}

{{chapter_body}}
```
