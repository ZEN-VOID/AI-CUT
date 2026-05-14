# Frame Prompt Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 单个四段式 `分镜ID` 的 prompt block |
| Output format | Markdown block with source style lines, slots, and English prompt |
| Output path | Included inside `第N集-分镜画面-prompts.md` |
| Naming convention | Heading uses `## <shot_id>` |
| Completion gate | prompt <= 800 English words; slots contain only existing image paths or remain empty; scene reference image is reviewed with `view_image` before prompt assembly when available; fixed scene-style prompt is present; the English prompt requires visual style, lighting, color palette and atmosphere to match the scene reference image; same-scene previous generated frame is reviewed with `view_image` when available; 3D spatial continuity plan and complete prompt design system are present in the English prompt body |

## Template

```markdown
## <分镜ID，如：1-1-1-1>

<直引 north_star.yaml 全局风格.全局风格提示词>
<直引 north_star.yaml 类型元素.类型元素提示词>
<直引 north_star.yaml 细分风格.画面风格>
画面风格，光影，色调和氛围与场景参照图保持一致。

Characters:
<角色名: 图片路径；无可用图片时留空或移除>

Scene:
<场景名: 图片路径；无可用图片时留空或移除>

Props:
<道具名: 图片路径；无可用图片时留空或移除>

Scene Reference Visual Style Lock:
- status: <visible_in_conversation_context | scene_reference_missing | pending_view_image>
- scene_reference_path: <场景参照图本地路径；无则留空>
- style_notes: <从场景参照图提炼的整体画面风格，不只复述 north_star>
- lighting_notes: <光源方向、光比、色温、高光/暗部形态>
- color_palette_notes: <主色、辅色、饱和度、冷暖关系>
- atmosphere_notes: <雾气、烟尘、湿度、压迫感、年代感等>
- material_notes: <木、石、金属、布料、墙面等可见材质质感>

Previous Frame Context:
- status: <visible_in_conversation_context | not_same_scene | previous_image_missing | previous_shot_not_generated | scene_first_shot>
- previous_shot_id: <上一分镜ID；无则留空>
- previous_image_path: <上一分镜本地生成图路径；无则留空>
- blocking_notes: <站位、走位、朝向、遮挡、关键道具相对位置、镜头轴线摘要；无上一图时写原因>

Spatial Continuity Plan:
- scene_space_model: <固定锚点、空间轴线、镜头轴线；不得只写同一背景>
- shot_anchor_projection_status: <projected_from_current_frame | inherited_scene_anchor_with_reason | insufficient_spatial_evidence>
- source_frame_anchor_evidence: <当前单镜文本中支持主锚点的证据；蒙太奇/插入/道具特写不得只继承分组场景>
- fixed_anchors: <门窗、桌椅、讲台、通道、墙面等相对位置>
- anchor_lock_method: <当前单镜候选锚点 -> 单镜主锚点 -> 辅助锚点 -> x/y/z 三轴 -> 逐镜投影；分组场景锚点仅在当前画面成立时继承>
- character_positions: <每个角色在 3D 空间中的当前位置、身体朝向、视线目标、前后景关系>
- movement_paths: <起始点 -> 移动轨迹 -> 终止点；无移动时写 no movement>
- camera_axis: <line of action、screen direction、是否反打/过肩/反向机位>
- shot_reverse_shot_notes: <正反打时说明相对背景面，如 north wall vs south wall / east side vs west side；非正反打写 none>

Prompt Design Blueprint:
- prompt_intent: <16:9 2K cinematic live action AIGC wuxia still + shot identity>
- source_truth: <当前单镜源真相；不吞并整组剧情>
- subject_action: <主体、动作、道具交互、谁不应出现>
- composition_lens: <镜头尺寸、焦段、机位高度、景深、构图重心>
- spatial_anchor_strategy: <Primary anchor + Support anchors 如何进入英文 prompt>
- continuity_strategy: <上一图可见时如何承接；不可见时如何记录缺失并仅按源稿规划>
- visual_style_strategy: <north_star 文字风格 + 场景参照图实际光影色调如何合成>
- material_physics: <湿、旧、风、雾、烟、火、金属、布料、纸张、木石等物理状态>
- reference_usage: <角色/场景/道具参照图的使用方式和禁用边界>
- negative_constraints: <字幕、logo、现代物、干净 CG、错误显露物、错误角色等>

<Integrated AIGC image prompt in natural English, <= 800 words; must include frame composition, subject space, subject motion, scene environment, light and atmosphere, cinematography, visual style, avoid constraints, and: "Match the scene reference image's visual style, lighting, color palette, and atmosphere.">
```
