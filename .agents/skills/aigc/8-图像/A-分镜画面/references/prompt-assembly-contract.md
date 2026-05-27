# Prompt Assembly Contract

本文件定义 step2：以每一个四段式分镜为单位，生成英文 AIGC 生图提示词。

批量生成任务中，step2 必须先覆盖本轮指定范围内的全部目标分镜，并落盘完整 `第N集-分镜画面-prompts.md`；不得只写当前待生图分镜的 prompt 后立即进入 imagegen，再边执行边补后续 prompt。

## Mandatory Source Lines

每个分镜 prompt 文档必须直引 `north_star.yaml` 三项字段，保持原文，不翻译、不摘要、不改写：

1. `全局风格.全局风格提示词`
2. `类型元素.类型元素提示词`
3. `细分风格.画面风格`

除此之外，若当前分镜存在本地场景参照图，必须额外加入固定提示词：

`画面风格，光影，色调和氛围与场景参照图保持一致。`

该固定提示词不是对 north_star 的替代，而是第二层视觉锁：north_star 锁定项目级文字风格，场景参照图锁定当前场景的实际画面风格、光影、色调和氛围。

## Required Markdown Shape

```markdown
## 1-1-1-1

<直引 north_star.yaml 全局风格.全局风格提示词>
<直引 north_star.yaml 类型元素.类型元素提示词>
<直引 north_star.yaml 细分风格.画面风格>
画面风格，光影，色调和氛围与场景参照图保持一致。

Characters:
Scene:
Props:

Scene Reference Visual Style Lock:
- status: visible_in_conversation_context | scene_reference_missing | pending_view_image
- scene_reference_path:
- style_notes:
- lighting_notes:
- color_palette_notes:
- atmosphere_notes:
- material_notes:

Previous Frame Context:
- status: visible_in_conversation_context | not_same_scene | previous_image_missing | previous_shot_not_generated | scene_first_shot
- previous_shot_id:
- previous_image_path:
- blocking_notes:

Spatial Continuity Plan:
- scene_space_model:
- shot_anchor_projection_status:
- source_frame_anchor_evidence:
- fixed_anchors:
- anchor_lock_method:
- character_positions:
- movement_paths:
- camera_axis:
- shot_reverse_shot_notes:

Prompt Design Blueprint:
- prompt_intent:
- scene_frame_identity:
- source_truth:
- subject_action:
- composition_lens:
- spatial_anchor_strategy:
- continuity_strategy:
- visual_style_strategy:
- material_physics:
- reference_usage:
- negative_constraints:

<Integrated AIGC image prompt in natural English, <= 800 words>
```

## Prompt Authorship

- `Integrated AIGC image prompt` 必须由 LLM 直接生成。
- 脚本可以把 LLM 直出的 prompt 投影为 Markdown 或 JSON，但不得自动扩写、补剧情、拼接主创段落。
- 允许做画面表现增量：composition, lens, shot size, camera angle, depth of field, lighting, material texture, color hierarchy, spatial blocking, visual pressure, continuity anchors.
- 禁止改变核心内容：角色身份、动作结果、剧情因果、死亡/惩罚事实、公开规则/隐藏规则、场景归属、关键道具。
- `Integrated AIGC image prompt` 不是字段拼接、中文源句翻译、剧情摘要或风格尾句，必须是 LLM 在理解当前四段式分镜、上下文和参照证据后重写出的自然英文 AIGC 画面提示词。结构化记录中的空间锚点、站位走位、场景参照图风格锁、道具显隐、负面约束和生成目标必须被自然转写进英文 prompt 本体，不得只停留在 `Spatial Continuity Plan` 或 `Scene Reference Visual Style Lock` 字段里。
- 最终英文 prompt 本体不得出现未翻译的中文源句、`Source truth: <中文原文>`、`focus on <中文原文>` 或把审查字段按顺序机械拼接成提示词。源分镜是理解依据，不是直接粘贴材料。

## Prompt Design System

每个 `Integrated AIGC image prompt` 必须按完整镜级设计体系组织。体系的作用是把 `6-分组` 的单镜真相、参照图视觉证据、空间连续性和 imagegen 执行约束合成一个可生成的英文 prompt。

### Required Prompt Layers

| layer | required content | purpose |
| --- | --- | --- |
| `L1 Frame Identity` | `Generate one 16:9 2K cinematic live action AIGC wuxia film still.`、`Shot ID <id>`、必要时写 `Scene first shot` / `Continuing from frame <id>`，并在首段锁定当前场景/镜头身份 | 锁定单帧、画幅、质量目标、分镜身份、场景身份和连续性入口 |
| `L2 Frame Landing Truth` | 当前 frame landing 的可见主体、动作结果、地点、叙事压力；上游 `分镜N` 只作为 `source_camera_units` 证据 | 防止 prompt 变成组级摘要或机械继承运镜单元 |
| `L3 Subject And Action` | 谁在画面中、身体动作、手部/眼神/道具交互、谁不应出现；无角色时说明由空间/道具承担主体 | 保证主体选择清楚，避免模型补人物 |
| `L4 Spatial Architecture` | `Primary anchor`、`Support anchors`、前/中/后景、遮挡层、关键道具相对位置、角色站位和走位 | 把三维空间机制写进最终 prompt |
| `L5 Continuity Logic` | 上一生成图可见时写承接的站位、朝向、光源和道具位置；无上一图时写 `no generated previous A-frame exists yet`，只按源稿和锚点规划 | 防止伪造上一图证据，给串行生图留 runtime 回看入口 |
| `L6 Camera And Composition` | 镜头尺寸、焦段、机位高度、轴线、运动状态、景深、构图重心、正反打背景面逻辑 | 把分镜明细转成可执行画面结构 |
| `L7 Reference Usage` | 已绑定角色/场景/道具参照的使用方式；明确场景参照图用于风格/光影/材质/锚点，不是平面背景粘贴 | 防止错用参照或让参考图压倒源镜头 |
| `L8 Scene Visual Style Lock` | `Match the scene reference image's visual style, lighting, color palette, and atmosphere.` 以及从图中提炼的光源方向、光比、色温、色彩、雾气、暗部/高光、材质；重要光线必须写出照亮对象和阴影/轮廓结果 | 让图像与本地场景参照一致，避免只写光源 |
| `L9 Material And Physics` | 木、石、纸、金属、布、血、水、烟、雾、风、火、盐湿、旧化、重量、反光、颗粒等可见物理状态 | 避免空泛风格词，增强真实材质 |
| `L10 Constraints And Avoid` | 不出现字幕/Logo/现代物/干净 CG/过锐/错误显露物/错误角色/猎奇化/发光武器等；必要时写 `do not show <hidden object>` | 控制模型常见偏移 |

### Required English Prompt Shape

最终英文 prompt 推荐使用短标签组织；标签不是装饰，而是 imagegen 执行约束：

```text
Generate one 16:9 2K cinematic live-action AIGC wuxia film still. Shot ID <id>.
Frame composition: <shot size / 景别, opening composition state, focus hierarchy, camera identity>.
Subject space: <visible characters or no-character evidence frame, 3D positions, foreground/midground/background>.
Subject motion: <the first legible instant of the action, not the whole camera move>.
Scene environment: <scene identity: era/period, location function, material age, soundscape/atmosphere baseline, story pressure carried by space>.
Light and atmosphere: <scene reference style lock, source-relative direction, what is illuminated, where shadows/outline separation fall>.
Cinematography: <lens, aperture/depth, camera height, frame format, film texture>.
Visual style: <global project style in natural English>.
Avoid: <negative constraints>.
```

允许在不超过 800 英文单词的前提下合并或增删标签，但不得省略画面构图、主体空间、主体运动、场景环境、光影氛围、摄影技术参数、视觉风格和 Avoid 的实质内容。结构化审查字段中的 `Primary anchor`、`Support anchors`、`Spatial blocking`、`Scene reference style lock` 等必须被自然吸收进这些段落，而不是以字段清单形式机械堆叠。

## Scene Reference Visual Style Lock

场景参照图不是只用于空间锚点；它还必须作为当前分镜的视觉风格锁。

1. 组织 `Integrated AIGC image prompt` 前，先从 `7-设计/场景/3-生成` 预绑定当前场景参照图。
2. 若存在本地场景参照图，必须先用 `view_image` 检视，使图片进入对话上下文，再组织 prompt；记录 `scene_visual_style_lock_status: visible_in_conversation_context`。
3. LLM 必须从场景参照图提炼可执行视觉信息：光源方向、光比、色温、主色/辅色、饱和度、暗部密度、高光形态、雾气/烟尘/湿度、材质质感、空间年代感和整体氛围。
4. `Integrated AIGC image prompt` 必须包含英文等价约束：`Match the scene reference image's visual style, lighting, color palette, and atmosphere.`
5. 若场景参照图与 north_star 文字风格存在张力，优先保持 north_star 的项目级风格边界，同时用场景参照图约束当前场景的具体光影、色调、材质和氛围，不得重设计场景。
6. 若缺少场景参照图，必须记录 `scene_reference_missing`；此时可仅用 north_star 文字风格，但不得声称已通过场景参照图锁定视觉风格。

## Spatial Continuity Planning

每条同场景分镜 prompt 必须先消费 `references/spatial-continuity-contract.md`，形成 `Spatial Continuity Plan`：

1. 不得把场景参照图当成平面背景模板直接复用；场景参照图只提供材质、结构、风格和锚点。
2. 先建立当前桥段的 3D `scene_space_model`：固定锚点、空间轴线、镜头轴线、角色相对方位和关键道具位置。
3. 执行单镜锚点投影：先从当前四段式分镜帧的 `frame_landing_reason`、`source_camera_units`、分镜明细、直接画面字段和必要入场/出场桥段中抽取当前可见锚点，再决定 `Primary anchor` 和 `Support anchors`。不得只因分镜组场景写了某个地点，就把该地点的常规主物件套成所有单镜的主锚点。
4. 执行固定锚点锁定：列出候选锚点，筛选主锚点和至少两个辅助锚点，定义 `x/y/z` 三轴，再把角色和道具写成相对锚点的位置。
5. 对每个角色写清当前位置、起始点、终止点、移动轨迹、身体朝向、视线目标和遮挡关系。
6. 对正反打、过肩、反向机位或对话戏，写清 line of action、screen direction、opposite background plane 和 eyeline match；背景面可以是镜像相对的南北面、东西面或房间两端，但必须属于同一个空间。
7. 对追逐、进出门、围站对峙、绕物移动、上下楼、过肩/主观视角、遮挡出现、道具交接、队列移动、同场景换机位、蒙太奇插入、道具微距、路线图、战船远景、转场匹配等桥段，必须消费 `spatial-continuity-contract.md` 的 `Anchor Pattern Library` 和 `Shot-Specific Anchor Projection`。
8. 当前英文 prompt 必须把上述空间规划转成可生图的视觉语言，避免角色瞬移、视线不闭合、道具位置跳变、轴线无理由跳变或 `Primary anchor` 与当前单镜内容不匹配。

## Scene And Frame Identity In Prompt

每条英文 prompt 必须先锁定 `scene_frame_identity`，再写主体动作。这里的“先”是生成器执行顺序，不要求暴露字段名；最终文本必须能让模型先得到场景/镜头身份，再理解人物动作。

`scene_frame_identity` 至少覆盖：

- `scene_identity`: 年代/朝代/技术时代、空间功能、环境声或氛围基底、材质新旧和当前空间压力。
- `frame_identity`: 单帧画面身份、是否场景首镜或承接上一帧、当前 frame landing 的可见职责。
- `camera_identity`: 摄影机位置、朝向、景别、焦段或观察方式。
- `direction_reference`: 人物入画、退场、视线、运动或光线方向相对镜头/画面边界/固定锚点。
- `lighting_result`: 光照亮了什么、阴影或轮廓落在哪里、主体如何从背景中分离。

禁止：

- 直接以 `A woman cries...` / `He walks forward...` 等主体动作摘要开头，却没有场景和镜头身份。
- 只写 `left light/right light/top light/cinematic lighting`，没有照亮对象、阴影位置或轮廓结果。
- 在未锁定 camera axis 时使用 left/right/front/back 作为唯一方向。

## Shot-Specific Anchor In Prompt

`Integrated AIGC image prompt` 中的 `Primary anchor:` 与 `Support anchors:` 必须和当前单镜画面内容直接对应。

- 若当前镜头是环境建立镜头，主锚点应是当前画面中的建筑边线、门、屋檐、城墙、船帆、水平线、港口木栈等，而不是分组内后续角色所在的桌案或室内家具。
- 若当前镜头是道具特写或微距，主锚点应是纸边、刀尖、封蜡裂纹、油绢纤维、布纹针脚、铜镜边、朱线、血迹、酒葫芦停点等当前画面支配物。
- 若当前镜头是蒙太奇或证据链插入，主锚点应落到该插入画面的可见主体；分组主场景锚点只能作为 `Support anchors` 或 continuity 回接，不得覆盖插入画面的主锚点。
- 若当前镜头是从一个地点转场到另一个地点，prompt 应写清当前帧处于哪一个视觉端点或匹配中间态，并选择该帧真正可见的端点锚点。
- 只有当当前镜头确实拍摄分组主场景整体空间，且该主场景锚点在当前画面中承担构图中心时，才可继承分组主场景锚点；必须在 `shot_anchor_projection_status` 中写明 `inherited_scene_anchor_with_reason`。

## Same Scene Previous Frame Review

新的画面提示词组织必须执行同场景上一画面回看门禁：

1. 先用 shot index 判断当前分镜是否为当前场景首镜；若是，记录 `scene_first_shot`。
2. 若上一分镜与当前分镜不是同一场景，记录 `not_same_scene`，不得把上一图作为空间连续性证据。
3. 若上一分镜与当前分镜同场景，先查找上一分镜本地生成图，优先使用 `第N集-imagegen-results.json` 中记录的项目内路径，其次查找 `第N集/images/<上一分镜ID>.*`。
4. 若同场景上一图存在，必须通过 `view_image` 检视该本地图片，使其进入对话上下文后再组织当前 prompt；记录 `previous_frame_context_status: visible_in_conversation_context`。
5. 检视上一图后，LLM 必须提炼可用于当前镜头的空间事实：角色站位、走位方向、身体朝向、视线、前后景遮挡、关键道具相对位置、门窗/桌椅/通道等场景锚点、镜头轴线和光源方向。
6. 当前 prompt 必须在不改写 `6-分组` 核心内容的前提下延续这些空间事实；若源镜头明确发生换位、转身、移动或镜头反打，prompt 应写清变化路径，使走位逻辑可追溯。
7. 若上一图缺失或上一分镜尚未生成，记录 `previous_image_missing` 或 `previous_shot_not_generated`，只能依赖 `6-分组` 与设计图，不得臆造上一画面的实际生成结果。
8. 两阶段批量生成时，prompt 文档阶段只能使用当时已经存在的本地上一生成图；如果上一分镜将在本轮稍后/稍早生成但此刻尚未存在，prompt block 应记录 `previous_shot_not_generated` 或 `previous_image_missing`。后续 imagegen 串行阶段若上一图已由本轮生成出来，必须在当前镜执行前作为 runtime `previous_frame_context` 回看并写入 result/report，但不得把这种 runtime 回看伪装成 prompt 文档阶段已经完成。

## English Prompt Requirements

`Integrated AIGC image prompt` 应包含：

- one single frame only;
- 16:9 2K cinematic live action AIGC still intent;
- `Shot ID` and continuity entry (`Scene first shot` / `Continuing from frame ...` / explicit missing previous generated A-frame reason);
- subject, action, location, narrative pressure;
- composition and camera language from the source shot;
- shot-specific primary anchor and support anchors as executable English prompt text; anchors must match the current single-frame source truth, not merely the group scene default;
- fixed scene-reference visual lock sentence: `Match the scene reference image's visual style, lighting, color palette, and atmosphere.`;
- concrete style, lighting, color and atmosphere cues extracted from the visible scene reference image when available;
- same-scene spatial blocking continuity from the previous generated frame when available;
- 3D spatial blocking: character start/end positions, movement path, fixed anchors, facing direction, eyeline, foreground/background depth, occlusion, and camera axis;
- shot-reverse-shot logic when relevant: reverse angle, opposite wall/background plane, line of action, screen direction, and eyeline match;
- lighting and material cues;
- style constraints from north_star, translated or integrated in English;
- reference awareness if slot images exist, without naming unavailable paths inside the prose;
- negative constraints such as no anime, no neon, no jump-scare monster when relevant.

## Word Limit

- `Integrated AIGC image prompt` 限定为 800 English words 以内，按英文空白分隔词粗算；带连字符的复合词按一个词处理即可。
- north_star 三项直引、固定中文场景参照图提示词、槽位标题、`Scene Reference Visual Style Lock`、`Previous Frame Context`、`Spatial Continuity Plan`、`Prompt Design Blueprint` 记录和 Markdown 标题不计入 800 English words 限制。
- 生成计划和审查结果应记录 `prompt_word_count`，不再以 `prompt_char_count` 作为主门禁；可保留字符数作辅助统计。
- 超限时优先删除重复风格词、泛泛情绪词和次要背景，保留 `Source truth`、主体动作、空间锚点、站位走位、镜头、场景参照图风格锁、材质物理和关键负面约束。

## Slot Semantics

`Characters:`、`Scene:`、`Props:` 是参照槽位，不是剧情正文。

- 有真实图片参照时写主体名与图片路径。
- 暂无真实图片时可只写主体名，或在最终 manifest 中移除空槽位。
- 不得把不存在的图片、JSON prompt 文件或外部未知 URL 写入参照槽位。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 批量任务是否先覆盖本轮全部目标分镜并落盘完整 prompts 文档，而不是写一镜就进入 imagegen？ | `G4A-PROMPT-PACKAGE-FIRST` | `FAIL-FRAME-IMAGEGEN` | `N5A-PERSIST-PACKAGE` | `第N集-分镜画面-prompts.md`、`reference-manifest.json`、`imagegen-plan.json` 均覆盖目标 `shot_id`；plan 记录 `prompt_package_status: complete_before_imagegen`。 |
| 每个 prompt block 是否直引 north_star 三项字段，保持原文且未翻译、摘要或改写？ | `G2-NORTHSTAR` | `FAIL-FRAME-PROMPT` | `N2-CONTEXT` / `N4-PROMPT` | prompt block 中三项文字与 `north_star.yaml` 原字段逐字一致；review note 记录字段路径。 |
| 若当前分镜存在本地场景参照图，是否先 `view_image` 并写入固定中文提示词与英文等价约束，而不是只追加“参考场景图”？ | `G3C-SCENE-VISUAL-STYLE-LOCK` | `FAIL-FRAME-SCENE-STYLE` | `N3A-SCENE-STYLE` / `N4-PROMPT` | `Scene Reference Visual Style Lock` 记录 `visible_in_conversation_context`、图像路径、style/lighting/color/atmosphere/material notes；英文 prompt 含 `Match the scene reference image's visual style, lighting, color palette, and atmosphere.` |
| 英文 prompt 是否由 LLM 直接创作成自然单帧生图指令，而不是字段拼接、中文源句翻译、剧情摘要或脚本扩写？ | `G3-PROMPT` | `FAIL-FRAME-PROMPT` | `N4-PROMPT` | prompt 本体无未翻译中文源句、`Source truth:` 粘贴、字段清单串接；报告记录 LLM-first prompt authorship。 |
| frame identity、source truth、subject/action、3D spatial architecture、continuity、camera/composition、reference usage、scene style lock、materials/physics、avoid constraints 是否自然进入英文 prompt 本体？ | `G3D-PROMPT-DESIGN-SYSTEM` | `FAIL-FRAME-PROMPT-SYSTEM` | `N4-PROMPT` | review note 按 Required Prompt Layers 勾选覆盖；缺层指向具体 prompt block 与缺失层。 |
| 英文 prompt 是否先锁定场景/画面/镜头身份，再写主体动作，并把方向参照和光线结果写成可见结果？ | `G3F-SCENE-FRAME-IDENTITY` | `FAIL-FRAME-SCENE-IDENTITY` | `N4-PROMPT` | prompt 首段含 scene/frame/camera identity、direction reference、lighting result；不以主体动作摘要直接开头。 |
| 同场景非首镜是否先检查上一生成图状态：有图则 `view_image` 并延续站位/朝向/遮挡/道具/轴线，无图则记录准确缺失原因？ | `G3A-PREV-FRAME-CONTINUITY` | `FAIL-FRAME-CONTINUITY` | `N4A-PREV-FRAME` / `N4-PROMPT` | `Previous Frame Context` 记录 `visible_in_conversation_context` / `not_same_scene` / `previous_image_missing` / `previous_shot_not_generated` / `scene_first_shot`，并有 blocking notes。 |
| prompt 文档阶段与 imagegen 串行阶段的上一画面回看是否区分清楚，runtime 新生成上一图没有被伪装成 prompt 阶段已完成？ | `G3A-PREV-FRAME-CONTINUITY` | `FAIL-FRAME-CONTINUITY` | `N4A-PREV-FRAME` / `N7-IMAGEGEN` | prompt block 记录文档阶段状态；result/report 单独记录 runtime `previous_frame_context` 和当前镜执行前的 `view_image` 状态。 |
| `Integrated AIGC image prompt` 是否在 800 English words 以内，并以 English word count 而非字符数作为主门禁？ | `G3-PROMPT` | `FAIL-FRAME-PROMPT` | `N4-PROMPT` | review note / plan 记录 `prompt_word_count <= 800`；超限返工保留 source truth、锚点、站位、场景风格锁和关键负面约束。 |
| `Characters:`、`Scene:`、`Props:` 是否只作为参照槽位，不把不存在图片、JSON prompt 文件或未知 URL 写入槽位？ | `G4-SLOTS` | `FAIL-FRAME-REF` | `N5-REF-BIND` | prompt block / manifest 中真实图片路径可读；无图主体为空、移除或记录 missing，未把 JSON 当图片。 |
