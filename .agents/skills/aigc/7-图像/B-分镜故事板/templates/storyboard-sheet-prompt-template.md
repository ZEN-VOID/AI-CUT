# Storyboard Sheet Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个分镜组的 storyboard prompt block |
| Output format | Markdown section that can be copied into `第N集-分镜故事板-prompts.md` |
| Output path | Rendered inside `projects/aigc/<项目名>/7-图像/B-分镜故事板/第N集/第N集-分镜故事板-prompts.md` |
| Naming convention | Section heading uses `## <分镜组ID>` |
| Completion gate | 固定开头完整并声明 4K，frame-unit plan 可追溯，组正文主体完整，主体参照来自 YAML manifest，场景参照图承担风格/光影/氛围锚定 |

```markdown
## <分镜组ID>

Create a multi-panel storyboard based on the following grouped shot source. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Render the final storyboard at 4K resolution so each panel remains clear and readable. Add the storyboard panel sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of storyboard panels. Match the generated image style, lighting, and atmosphere to the bound scene reference image whenever a scene reference is provided.

### Storyboard Frame Units

1. source_shot_labels: <分镜N 或多个源分镜标签>
   visual_beat: <该 panel 要表现的视觉节拍>
   source_span: <可回指的组正文片段或摘要>

<直接粘贴 5-分组 中该分镜组现有正文主体，不含底部 YAML>

### Reference Subjects

Characters:
- <角色名>: <图片路径或 missing>

Scene:
- <场景名>: <图片路径或 missing>
  visual_anchor: style_lighting_atmosphere

Props:
- <道具名>: <图片路径或 missing>
```
