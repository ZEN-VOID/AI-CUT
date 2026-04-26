# Frame Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个四段式 `分镜ID` 的 prompt block |
| Output format | Markdown block with source style lines, slots, and English prompt |
| Output path | Included inside `第N集-分镜画面-prompts.md` |
| Naming convention | Heading uses `## <shot_id>` |
| Completion gate | prompt <= 2000 chars; slots contain only existing image paths or remain empty |

## Template

```markdown
## <分镜ID，如：1-1-1-1>

<直引 north_star.yaml 全局风格.全局风格提示词>
<直引 north_star.yaml 类型元素.类型元素提示词>
<直引 north_star.yaml 细分风格.画面风格>

Characters:
<角色名: 图片路径；无可用图片时留空或移除>

Scene:
<场景名: 图片路径；无可用图片时留空或移除>

Props:
<道具名: 图片路径；无可用图片时留空或移除>

<Integrated AIGC image prompt in English, <= 2000 characters>
```
