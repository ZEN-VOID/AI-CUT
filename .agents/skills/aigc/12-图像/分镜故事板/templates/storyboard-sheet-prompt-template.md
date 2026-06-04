# Storyboard Sheet Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个分镜组的 storyboard prompt block |
| Output format | Markdown section that can be copied into `第N集-分镜故事板-prompts.md` |
| Output path | Rendered inside `projects/aigc/<项目名>/12-图像/B-分镜故事板/第N集/第N集-分镜故事板-prompts.md` |
| Naming convention | Section heading uses `## <分镜组ID>` |
| Completion gate | 任务执行前缀完整并声明黑白线稿基底、受控彩色标注系统、每个可见角色头顶黑色角色名、4K、默认 16:9 panel 图片区、panel 下方 `rich_brief` 描述文字、自适应排版；frame-unit plan 可追溯；完整分镜组内容保留；主体参照来自 YAML manifest 并用于身份/空间/道具保真 |

```markdown
## <分镜组ID>

Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a 16:9 image area by default, with a storyboard description text area directly below that panel image. Auto-adapt the sheet layout to the total number of storyboard panels, using pagination or multiple sheets when needed. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable.

### Storyboard Frame Units

1. panel_no: 1
   panel_image_aspect_ratio: 16:9
   visual_beat: <该 panel 要表现的视觉节拍>
   panel_description: <rich_brief；从 source_span 和分组稿分镜描述原文保真精简为 1-2 句>
   panel_description_density: rich_brief
   character_name_labels:
     - <角色名>: above_character_head
   annotation_plan:
     red_body_movement_arrows: <身体运动方向；不适用写 none>
     blue_camera_movement_arrows: <摄影机运动方向；不适用写 none>
     green_framing_composition_marks: <取景/构图笔记；不适用写 none>
     orange_lighting_direction_marks: <灯光方向；不适用写 none>
     purple_emotion_sound_narrative_marks: <情绪/声音/叙事强调；不适用写 none>
     black_text_notes_and_panel_label: <简短镜头笔记和面板标签>
   source_shot_labels: <分镜N 或多个源分镜标签>
   source_span: <可回指的组正文片段或摘要>

### Complete Group Source From 10-分组

<直接粘贴 10-分组 中该分镜组完整内容，包含组正文和底部 fenced YAML>

### Reference Subjects

Characters:
- <角色名>: <图片路径或 missing>

Scene:
- <场景名>: <图片路径或 missing>
  visual_anchor: spatial_structure_and_subject_identity

Props:
- <道具名>: <图片路径或 missing>
```
