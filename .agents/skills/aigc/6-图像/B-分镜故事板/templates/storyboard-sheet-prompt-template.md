# Storyboard Sheet Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个分镜组的 storyboard prompt block |
| Output format | Markdown section that can be copied into `第N集-分镜故事板-prompts.md` |
| Output path | Rendered inside `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/第N集-分镜故事板-prompts.md` |
| Naming convention | Section heading uses `## <分镜组ID>` |
| Completion gate | 固定开头完整，组正文主体完整，主体参照来自 YAML manifest |

```markdown
## <分镜组ID>

Create a multi-panel storyboard based on the following shot breakdown. Add the shot sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of shots.

<直接粘贴 4-分组 中该分镜组现有正文主体，不含底部 YAML>

### Reference Subjects

Characters:
- <角色名>: <图片路径或 missing>

Scene:
- <场景名>: <图片路径或 missing>

Props:
- <道具名>: <图片路径或 missing>
```
