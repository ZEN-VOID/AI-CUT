# Shot Planning Integration Contract

本文件定义 `8-摄影` 在注入正文前必须完成的内部 `camera_movement_plan`。该计划不是输出字段，但必须支撑每条最终运镜句。

## Plan Fields

| field | requirement |
| --- | --- |
| `source_line_id` | 对应原 `分镜N（N-N秒）` 行 |
| `original_content_preservation` | 原分镜正文保留方式；不得摘要、删改或替换 |
| `dramatic_function` | 当前分镜的信息、动作、情绪、关系或节奏功能 |
| `aesthetic_inheritance` | 来自画面基调和摄影风格的可执行约束 |
| `camera_angle_change` | 镜头角度及变化 |
| `shot_type` | 镜头类型或运动方式 |
| `movement_speed` | 速度曲线与停点 |
| `focus_behavior` | 焦点静止或变化 |
| `continuity_handoff` | 入点和交出点 |
| `one_take_link` | 一镜到底时与前后分镜的链路 |

## Integration Rule

只有当 `camera_movement_plan` 能同时解释剧情功能、美学继承、运镜四要素和连续性交接时，才允许进入正文注入。计划失败不得靠润色句子掩盖。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 每条最终运镜句是否可回指内部 plan？ | `GATE-CAM-08-PLAN-01` | `FAIL-CAM-PLAN-MISSING` | `N6-CAM-MOVEMENT-DESIGN` | plan coverage table |
| 是否先保留原分镜正文再追加运镜，而非替换原文？ | `GATE-CAM-08-PLAN-02` | `FAIL-CAM-SOURCE-REPLACED` | `N7-CAM-INJECT` | source preservation diff |
| 画面基调和摄影风格是否转成具体运镜约束？ | `GATE-CAM-08-PLAN-03` | `FAIL-CAM-AESTHETIC-NOT-USED` | `N3-CAM-AESTHETIC` | aesthetic inheritance map |
