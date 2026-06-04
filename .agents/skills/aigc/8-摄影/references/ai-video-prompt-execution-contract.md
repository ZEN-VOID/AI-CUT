# AI Video Prompt Execution Contract

本文件定义 `8-摄影` 运镜注入如何为后续视频生成保留可执行信息。它不要求本阶段输出完整视频 prompt、provider 参数或镜头 JSON；它要求每条内联运镜句能被下游稳定改写为视频提示词。

## Core Rule

`8-摄影` 的运镜描述必须采用“镜头包裹动作”的顺序：

1. 先确定摄影机位置、镜头角度和观看方向。
2. 再确定镜头类型、运动路径、速度曲线和停止点。
3. 再让人物动作、表演微动态、光线结果、声音或道具状态在镜头内部发生。
4. 最后明确焦点静止、拉移、失焦再合焦或保持深焦的观看结果。

## Required Payload

每条普通分镜运镜注入至少能抽取：

| payload | requirement |
| --- | --- |
| `camera_angle_change` | 镜头角度及其变化，例如低机位抬升、平视横移、俯角压低、过肩转正面 |
| `shot_type` | 镜头类型或观看关系，例如手持跟拍、推轨、横移、摇镜、环绕、静止长镜、rack focus |
| `movement_speed` | 速度曲线，例如极慢推进、短促急停、匀速跟随、先慢后快、静止不动及其理由 |
| `focus_behavior` | 焦点静止或变化，例如锁定双眼、从前景道具拉到人物、深焦保持两人关系 |
| `direction_reference` | 必要时说明画面左/右、朝镜头/远离镜头、前景/背景和轴线关系 |
| `visible_micro_action` | 抽象心理必须落到可见动作，如呼吸断拍、咬肌收紧、手指松开、视线停住 |

## Prohibitions

- 不输出 provider 指令、负面提示词、seed、比例、镜头参数表或完整 prompt 模板。
- 不用“电影感”“高级”“压迫感很强”等效果词替代可见结果。
- 不把“紧张、愤怒、压抑、心痛、痛苦”等心理标签直接作为视频可执行动作。
- 不写单眼侧面眼睛特写；眼部特写默认必须是正面双眼，眉骨到鼻尖区域。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 每条运镜句是否包含镜头角度、镜头类型、速度和焦点行为四项？ | `GATE-CAM-08-AI-01` | `FAIL-CAM-AI-PAYLOAD` | `N6-CAM-MOVEMENT-DESIGN` | payload 抽样表 |
| 抽象心理是否转译为可见表演微动态？ | `GATE-CAM-08-AI-02` | `FAIL-CAM-AI-ABSTRACT` | `N5-CAM-SHOT-ANALYZE` | 抽象词替换记录 |
| 是否没有输出视频 prompt 或 provider 参数？ | `GATE-CAM-08-AI-03` | `FAIL-CAM-AI-OVERREACH` | `N7-CAM-INJECT` | 越权扫描结果 |
