# Group Multi-Image Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个普通 `group_id` 的 imagegen 多图 prompt block |
| Output format | Markdown block with full group source, reference roles, consistency contract, Image 1..N sections |
| Output path | Included inside `第N集-分镜画面-prompts.md` |
| Naming convention | Heading uses `## Group <group_id> Multi-Image Task` |
| Completion gate | `shot_count == Image section count == expected_image_count`；默认 `aspect_ratio=16:9`；任务前缀禁止拼图；每个分镜点有独立 prompt；同组一致性约束存在 |

## Template

```markdown
## Group <group_id> Multi-Image Task

Task Execution Prefix:
Imagegen storyboard-frame generation task. Generate exactly <shot_count> separate <aspect_ratio, default 16:9> 2K cinematic live-action AIGC still images, one image for each numbered shot point in this storyboard group, in the exact order listed below. Do not create a storyboard sheet, collage, contact sheet, grid, comic page, multi-panel image, or variants of one frame. Return <shot_count> independent images that preserve the same character identities, costumes, scene design, lighting logic, color palette, material atmosphere, spatial anchors, and story continuity across the whole group. Execution must be handed to `.agents/skills/cli/imagegen`; batch generation follows its built-in `image_gen` and subagents concurrency contract.

Aspect Ratio:
- default: 16:9
- selected: <16:9 unless user explicitly requested 9:16 or another ratio>
- override: <null or explicit user request>

Source Group Full Content:
```text
<完整引用 8-分组 中该组内容>
```

North Star Style:
- global_style:
- genre_elements:
- visual_style:

Reference Images:
- Characters:
- Scene:
- Props:

Group Consistency Contract:
- character_identity_lock:
- costume_and_prop_lock:
- scene_space_lock:
- lighting_color_atmosphere_lock:
- spatial_axis_and_anchor_lock:
- continuity_between_images:
- non_collage_rule:

Image Order:
1. image_index: 1; shot_id: <x-y-z-1>; source_shot_label: 分镜1

Image 1 / Shot ID <x-y-z-1>:
- source_shot_label:
- source_shot_text:
- frame_state_to_restore:
- visible_subjects:
- scene_and_spatial_state:
- camera_and_composition:
- lighting_and_atmosphere:
- reference_usage:
- avoid:
- prompt: <natural English long prompt for this one separate image>

Output Mapping:
- returned_image_1 -> <x-y-z-1>.png
```
