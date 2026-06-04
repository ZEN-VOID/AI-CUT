# Shot Composition Contract

本文件融合旧 `4-摄影` 中与构图相关的 `beat-analysis-contract.md`、`depth-of-field-narrative-contract.md`、`shot-as-narrative-contract.md`、`scene-visual-constraint-contract.md` 与 `ai-video-prompt-execution-contract.md`，改写为 `7-分镜` 的 step2 构图起始状态帧细则。

## Core Rule

每条 `分镜N（N-N秒）` 必须先裁决叙事功能，再确定起始状态帧。成稿至少包含：

```text
景别，景深，构图形式，主体陪体背景描述
```

这里的“构图”不是摄影技术表，而是让下游明确：摄影机开始看哪里，主体是谁，陪体如何承托，背景提供什么空间/信息/情绪，观众第一眼如何理解当前画面。

## Narrative Function

每条分镜必须有内部 `shot_narrative_function`：

| function_id | function | use |
| --- | --- | --- |
| `NF-01` | reveal 揭示 | 新信息、空间、道具、规则显影 |
| `NF-02` | conceal 隐藏 | 悬念、危险暗示、身份遮蔽 |
| `NF-03` | emphasize 强调 | 高点、关键反应、规则突破 |
| `NF-04` | compare 对比 | 正反打、权力/态度对照 |
| `NF-05` | misdirect 误导 | 悬疑反转铺垫，必须有后续兑现 |
| `NF-06` | connect 连接 | 视线、动作、声音、光色或情绪接力 |

技术选择必须服务叙事功能；如果删掉该分镜观众不少看见、不少理解、不少感受，则应删并或重写。

## Required Composition Payload

| payload | requirement |
| --- | --- |
| `shot_scale` | 远景、全景、中景、近景、特写、大特写等；服务当前观看任务 |
| `depth_strategy` | 深景深、浅景深、前虚后实、焦点拉移、柔焦等；说明观众此刻看哪里/不看哪里 |
| `composition_form` | 对称、三分、三角、框架、引导线、前景遮挡、对角线、中心压迫、留白等 |
| `subject` | 主体位置、朝向、动作相位或表演状态 |
| `companion` | 陪体、反应者、道具、前景、群像或空间压力源 |
| `background` | 场景身份、光色、文字/屏幕/门窗/材质或氛围承托 |
| `direction_reference` | 入画、退场、视线、运动方向相对画面或镜头可执行 |
| `lighting_result` | 光造成的亮面、暗面、轮廓、反光或背景层次，不只写光源名 |

## Depth Of Field Narrative

景深是注意力控制：

| strategy | narrative use |
| --- | --- |
| `shallow_focus_subject` | 隔离主体，隐藏次要背景 |
| `shallow_focus_background` | 主体虚化，真正重要的信息在后景 |
| `rack_focus_A_to_B` | 强制注意力从 A 转到 B |
| `deep_focus_all` | 空间关系、群像或制度布局全部可读 |
| `soft_focus_subjective` | 梦境、回忆、主观状态，不能泛化为情绪感 |

若使用浅景深，必须知道什么被虚化、为什么可以虚化；不得虚化关键线索、危险源或关系信息。

## Scene Visual Constraint

同一场景内先形成内部 `scene_visual_constraint`，不进入成稿字段，但应影响每条分镜：

- `scene_identity`：年代、空间功能、社会语境、环境声底、材质年龄。
- `composition_layout`：主体、陪体、前景、背景的位置和占比。
- `composition_method`：形状感、线条感、影调感、虚实感、节奏感、纹理质感、气势中选当前最关键 2-3 项。
- `lighting_setup`：主光、辅光、逆光或实用光的可见结果。
- `color_system`：只作为内部色彩关系，不替代 `3-美学/画面基调`。

## AI Video Execution Stability

每条分镜必须能被下游视频阶段稳定理解：

- 镜头先行：先说明镜头/机位/构图起点，再让人物动作发生在镜头内部。
- 方向参照明确：使用“朝镜头”“远离摄像机”“从画面左侧进入”“停在右侧三分之一”等。
- 表演微动态可见：情绪落到眼神、咬肌、鼻翼、嘴角、肩膀、手指、呼吸、喉结或眨眼频率。
- 光线结果具体：写亮在何处、阴影落在哪里、轮廓如何分离主体。
- 眼睛特写默认使用正面双眼特写或正面上半脸特写，避免侧面单眼畸形风险。

## Output Projection

成稿不输出内部标签，不写参数表。合法写法：

```text
分镜1（0-2秒）：中景，浅景深，门框前景遮挡构图，主角站在画面右侧三分之一，左侧门缝冷光切过脸侧，后景走廊虚化成压低的灰白线条
```

不合法写法：

```text
分镜1（0-2秒）：电影感特写，氛围压迫，f/1.4，cinematic lighting
```

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条分镜是否至少含景别、景深、构图形式、主体陪体背景描述？ | `GATE-SB-05` | `FAIL-SB-COMPOSITION` | `N5-COMPOSITION-DESIGN` | `shot_composition_plan` |
| 景深是否服务注意力控制，而非泛化虚化？ | `GATE-SB-06` | `FAIL-SB-DEPTH` | `N5-COMPOSITION-DESIGN` | `depth_plan` samples |
| 分镜是否先裁决叙事功能，再选择构图？ | `GATE-SB-07` | `FAIL-SB-NARRATIVE-FUNCTION` | `N5-COMPOSITION-DESIGN` | function distribution |
| 是否具备方向参照、光线结果和表演微动态？ | `GATE-SB-08` | `FAIL-SB-AI-EXEC` | `N5-COMPOSITION-DESIGN` | ai execution samples |
