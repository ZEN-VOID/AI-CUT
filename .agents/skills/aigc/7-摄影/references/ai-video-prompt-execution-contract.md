# AI Video Prompt Execution Contract

本文件定义 `7-摄影` 运镜注入如何为后续视频生成保留可执行信息。它不要求本阶段输出完整视频 prompt、provider 参数或镜头 JSON；它要求每条内联运镜句能被下游稳定改写为视频提示词。

## Core Rule

`7-摄影` 的运镜描述必须采用“镜头包裹动作”的顺序：

1. 先确定摄影机位置、镜头角度和观看方向。
2. 再确定镜头类型、运动路径、速度曲线和停止点。
3. 再让人物动作、表演微动态、有叙事功能的布光/阴影结果、声音或道具状态在镜头内部发生。
4. 最后明确清晰主体、景深层次、焦点静止、拉焦/转焦、失焦再合焦或深焦/深景深的观看结果。

## Required Payload

每条普通分镜运镜注入至少能抽取：

| payload | requirement |
| --- | --- |
| `camera_angle_change` | 镜头角度及其变化，例如低机位抬升、平视横移、俯角压低、过肩转正面 |
| `shot_type` | 镜头类型或观看关系，例如手持跟拍、推轨、横移、摇镜、环绕、静止长镜、rack focus |
| `movement_speed` | 速度曲线，例如极慢推进、短促急停、匀速跟随、先慢后快、静止不动及其理由 |
| `focus_behavior` | 摄影语义正确的焦点静止或变化，例如锁定双眼、从前景道具拉到人物、深景深同时保留两人关系；不得把焦点写成关注点 |
| `direction_reference` | 必要时说明画面左/右、朝镜头/远离镜头、前景/背景和轴线关系 |
| `visible_micro_action` | 抽象心理必须落到可见动作，如呼吸断拍、咬肌收紧、手指松开、视线停住 |
| `visible_light_result` | 必要时说明布光类型/光型、阴影位置、可读亮区、不可读暗区和运动/焦点交接中的可见变化；叙事美学功能只作为内部选择依据，不在正文中输出解释性因果句；光源、色温、材质/空气介质或动态光只作为 source motivation boundary 与连续性依据，不得新增无源光源 |

## Prohibitions

- 不输出 provider 指令、负面提示词、seed、比例、镜头参数表或完整 prompt 模板。
- 不用“电影感”“高级”“压迫感很强”等效果词替代可见结果。
- 不把“紧张、愤怒、压抑、心痛、痛苦”等心理标签直接作为视频可执行动作。
- 不写单眼侧面眼睛特写；眼部特写默认必须是正面双眼，眉骨到鼻尖区域。
- 不把叙事关注点、危险方向、行动压力或心理落点直接写成焦点；必须转为清晰主体、景深层次或对焦动作。
- 不把推轨、短推、横移、跟拍或靠近主体写成变焦；变焦只表示焦距改变导致视角收窄或放宽。
- 不把旧 `9-光影` 恢复成独立光影句、灯位说明、光效清单或视频 prompt。
- 不新增 source / 场景风格 / 摄影风格中没有依据的雨雪烟尘、火光、霓虹、月光、逆光、雾气、窗光或反射光。
- 不用“电影感光影”“高级光影”“宿命感逆光”“压迫感阴影”等抽象词替代布光类型、阴影组织和主体可读性。
- 不写“阴谋感由...完成”“危险感来自...”“形成某种意图/收束”等解释性结论；必须转成视频可见的亮面、暗面、阴影边界、遮挡区域和清晰主体。
- 不把光影写成发光物、反光物、色温、介质和亮度变化的观察清单；下游需要的是可见的布光结果和叙事阴影，而不是科学实验式描述。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 每条运镜句是否包含镜头角度、镜头类型、速度和焦点行为四项？ | `GATE-CAM-08-AI-01` | `FAIL-CAM-AI-PAYLOAD` | `N6-CAM-MOVEMENT-DESIGN` | payload 抽样表 |
| 抽象心理是否转译为可见表演微动态？ | `GATE-CAM-08-AI-02` | `FAIL-CAM-AI-ABSTRACT` | `N5-CAM-SHOT-ANALYZE` | 抽象词替换记录 |
| 是否没有输出视频 prompt 或 provider 参数？ | `GATE-CAM-08-AI-03` | `FAIL-CAM-AI-OVERREACH` | `N7-CAM-INJECT` | 越权扫描结果 |
| 焦点行为是否能被下游转译为可执行对焦/景深结果？ | `GATE-CAM-08-AI-04` | `FAIL-CAM-FOCUS-SEMANTIC` | `N6-CAM-MOVEMENT-DESIGN` | focus_semantic_audit |
| 光线结果是否能被下游转译为明确布光类型、阴影位置、可读亮区、不可读暗区和运动/焦点交接，而非抽象氛围词、解释性结论或发光物观察清单？ | `GATE-CAM-08-LIGHT-INTEGRATION` | `FAIL-CAM-LIGHT-INTEGRATION` | `N6-CAM-MOVEMENT-DESIGN` | visible_light_result 抽样表、lighting_design_type_map、shadow_design_map、canonical_output_projection_audit |
| 是否没有把光影输出成独立 `9-光影` payload、灯位图、光效清单或视频 prompt？ | `GATE-CAM-08-LIGHT-STAGE-BOUNDARY` | `FAIL-CAM-LIGHT-STAGE-DRIFT` | `N7-CAM-INJECT` | camera_light_integration_boundary / overreach_scan |
