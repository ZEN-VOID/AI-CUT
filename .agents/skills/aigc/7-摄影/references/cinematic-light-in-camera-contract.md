# Cinematic Light In Camera Contract

本文件把旧 `backup/9-光影` 的可取部分压回 `7-摄影`。它不是恢复独立光影阶段，也不要求在每条分镜后另追加一段光影句；它只要求 `camera_movement_plan` 在设计机位、运动、速度、景深和焦点时同步考虑布光类型、阴影组织、主体可读性和叙事光影功能。

## Core Principle

光影在 `7-摄影` 中首先是布光与阴影组织的叙事设计，而不是发光物观察清单。内部计划可以回答：当前镜头采用什么布光类型或光型，人物面部、身体和空间保留哪些阴影，这些阴影如何揭示或遮蔽信息，以及它们如何服务阴谋、权力、危险、亲密、孤立、审判感或失控感等叙事功能。

正式摄影正文只输出可被镜头和视频模型看见的结果，不输出“阴谋感由...完成”“危险感来自...”“形成某种意图”这类解释性结论。叙事功能用于选择布光方案，落到正文时必须转写为光位、光型、阴影位置、可读区域、暗部遮挡和随镜头/焦点变化的可见结果。

光源可信是边界，不是正文主轴。允许说明光源、色温、材质或空气介质，但它们只用于防止无源新增、保证连续性和支撑布光方案，不得把运镜句写成科学实验式的光照观察报告。

## Camera-Light Plan Fields

每条正式运镜计划按需要检查以下字段；只有会影响镜头可读性、下游视频稳定性或分镜功能时才进入正文。

| field | requirement |
| --- | --- |
| `lighting_design_type` | 明确布光类型、光型或光质选择，例如低位上打、伦勃朗光、分割光、侧逆光、顶光压脸、轮廓光、剪影、低调布光、高调布光、负补光、硬光、柔光、跳光或实景动机光；必须与当前分镜功能、摄影风格和主体关系绑定。 |
| `shadow_design` | 说明脸部、身体或空间保留哪些阴影，例如眼窝、颧骨、鼻梁一侧、半张脸、下颌、背后墙面、前景遮挡或背景暗区；阴影必须承担揭示、遮蔽、分割、压迫或隔离功能。 |
| `narrative_aesthetic_function` | 说明布光和阴影如何服务叙事烘托与光影美学，例如阴谋感、权力不对称、危险临近、身份割裂、道德暧昧、孤立、亲密、失控、审判感或窥视感；不得只写抽象标签，必须回到具体光型和阴影结果。 |
| `subject_readability_control` | 人脸、眼神、手部、姿态、关键道具或空间边界哪些必须保持可读，哪些可以被暗部吞掉；剪影、背光、低照不得损失必须可读的信息。 |
| `camera_light_alignment` | 推、拉、横移、跟拍、静止、对焦或转焦时，布光方案和阴影边界应说明随镜头变化、保持稳定、遮住信息或交出信息的理由。 |
| `light_continuity` | 同一场景内布光方案、主光方向、光比/明暗、阴影方向、色温倾向和光色主导权不得无故跳变。 |
| `source_motivation_boundary` | 光源、色温、材质、空气介质或动态光只作为可信边界：不得为了效果新增火、窗、屏幕、车灯、雨雪、烟雾等实体；也不得反复点名可能发光物来替代布光设计。 |
| `canonical_output_projection` | 正文只保留可见投影：例如“低位白色伦勃朗光托亮左颧骨，鼻梁右侧和右眼眼窝留暗”“纸边被窄幅硬侧光切亮，人物侧脸仍被分割阴影压住”；不得写解释性因果句。 |

## Prohibitions

- 不把“电影感、高级质感、宿命感、压迫感、诗意”写入运镜正文替代布光类型、阴影组织和可见光影结果。
- 不把内部叙事判断写成正文解释，例如“阴谋感由面部阴影遮蔽完成”“危险感来自明暗反差”“形成动作可见、意图不可见的收束”；必须改写为可见光位、阴影位置和可读/不可读区域。
- 不把光影写成发光物考据清单、可能光源罗列、科学实验观察式照明记录或“哪里亮、哪里反光”的重复描述。
- 不反复点名火、窗、屏幕、车灯、月光、霓虹、烟雾、雨雪等可能发光或显光物来冒充光影美学。
- 不复制 `2-美学` 全局 prompt 或照搬大师名场面。
- 不为光影效果新增 source 没有的实体光源、天气、烟雾、爆炸或人群。
- 不输出灯位图、器材参数、曝光参数、图像 prompt、视频 prompt 或 provider 参数。
- 不让光影抢过镜头运动、焦点行为、人物表演和动作链。
- 不把旧 `9-光影` 的“逐镜追加光影美学句”恢复为 `7-摄影` 的第二输出层。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 运镜计划是否有明确的布光类型/光型、阴影组织、叙事美学功能和主体可读性控制，并服务机位/运动/焦点？正文是否只输出可见投影，没有退化为发光物观察清单或解释性抽象结论？ | `GATE-CAM-08-LIGHT-INTEGRATION` | `FAIL-CAM-LIGHT-INTEGRATION` | `N6-CAM-MOVEMENT-DESIGN` / `N6B-CAM-ONETAKE-CHAIN` | `camera_light_plan`、`lighting_design_type_map`、`shadow_design_map`、`narrative_light_function_map`、`canonical_output_projection_audit`、`camera_light_alignment_map` |
| 同一场景内布光方案、光比/明暗、阴影方向和光色状态是否连续，必要的 source motivation boundary 是否成立？ | `GATE-CAM-08-LIGHT-CONTINUITY` | `FAIL-CAM-LIGHT-CONTINUITY` | `N4-CAM-CONTEXT` / `N6-CAM-MOVEMENT-DESIGN` | `light_continuity_map`、`lighting_scheme_continuity_map`、`source_motivation_boundary` |
| 是否没有把旧 `9-光影` 恢复成独立追加层或装饰性光影 payload？ | `GATE-CAM-08-LIGHT-STAGE-BOUNDARY` | `FAIL-CAM-LIGHT-STAGE-DRIFT` | `N7-CAM-INJECT` / `N8-CAM-REVIEW-REPAIR` | `camera_light_integration_boundary` |
