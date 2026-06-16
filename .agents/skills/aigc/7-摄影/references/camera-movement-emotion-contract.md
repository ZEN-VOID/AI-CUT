# Camera Movement Emotion Contract

本文件定义 `7-摄影` 中“运镜为什么这样动”的情绪和观看动机。技术名只能作为结果，不能替代推理。

## Movement Motivation

每个运镜选择必须至少服务一种当前分镜任务：

| task | movement logic |
| --- | --- |
| 信息揭示 | 横移、转焦、慢推或遮挡滑出，让观众在某一拍获得新信息 |
| 关系压迫 | 低机位、过肩、慢推、长焦压缩或静止框线，让空间关系变紧 |
| 情绪靠近 | 极慢推进、正面近景、焦点锁眼神，减少运动花样 |
| 失控或危险 | 手持微晃、急停、快速拉远、短促摇镜，但必须有动作或风险触发 |
| 观察克制 | 静止长镜、深焦、固定构图，让观众被迫停留 |
| 转场交出 | 运动方向、声音尾巴、光色变化或遮挡边缘交给下一分镜 |

## Speed Curve Rule

速度必须是当前剧情推理结果：

- `静止`：用于制度压迫、情绪读秒、信息可读、沉默反应；必须写明静止观看什么。
- `极慢`：用于靠近、确认、逼迫面对或情绪慢燃。
- `匀速`：用于稳定跟随动作路径或空间关系。
- `先慢后快`：用于犹疑到爆发、发现到追击。
- `短促急停`：用于撞点、惊吓、动作结果钉住。

## Output Requirement

运镜句应写成自然中文综合描述，而不是清单：

```text
分镜2（2-4秒）：原有内容。镜头由低机位平视缓慢抬到她的正面近景，手持推轨极慢靠近，速度压到呼吸停顿上，焦点始终锁住她收紧的双眼。
```

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 运镜是否能说明情绪、信息或关系动机，而不是随机套技术名？ | `GATE-CAM-08-MOVE-01` | `FAIL-CAM-MOVE-RANDOM` | `N6-CAM-MOVEMENT-DESIGN` | movement_reason 抽样 |
| 速度曲线是否符合当前分镜节奏？ | `GATE-CAM-08-MOVE-02` | `FAIL-CAM-SPEED-MISMATCH` | `N6-CAM-MOVEMENT-DESIGN` | speed_curve_map |
| 静止镜头是否明确写出静止理由？ | `GATE-CAM-08-MOVE-03` | `FAIL-CAM-STILLNESS-EMPTY` | `N6-CAM-MOVEMENT-DESIGN` | stillness_reason |
