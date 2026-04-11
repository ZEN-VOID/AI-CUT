# aigc 3-明细 / 5-摄影美学 / 摄影参数 / Chain Of Thought

本文件承载 `aigc 3-明细 / 5-摄影美学 / 摄影参数` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-CAP-SRC-01 | 执行报告.来源卡 | 锁定镜位、场次、分组与上游 handoff | S1 | 来源可追溯性 | FAIL-CAP-SRC-01 |
| FIELD-CAP-SHUTTER-02 | `摄影美学.摄影参数` 字段 | 快门与动作质感自洽 | S2 | 动作捕捉可执行性 | FAIL-CAP-SHUTTER-02 |
| FIELD-CAP-ISO-WB-03 | `摄影美学.摄影参数` 字段 | ISO 与白平衡匹配当前光色条件 | S3 | 感光与显色可信度 | FAIL-CAP-ISO-WB-03 |
| FIELD-CAP-TEXTURE-04 | `摄影美学.摄影参数` 字段 | 滤镜与曝光倾向支撑目标质感 | S4 | 质感控制准确性 | FAIL-CAP-TEXTURE-04 |
| FIELD-CAP-BOUNDARY-05 | 执行报告.边界留口 | 标出与静态光学字段的冲突或回退项 | S5 | 边界治理完整性 | FAIL-CAP-BOUNDARY-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-CAP-SRC-01 | 这镜的证据从哪来 | 锁定镜位与 handoff | 无来源就开始填参数 |
| S2 | FIELD-CAP-SHUTTER-02 | 快门该如何服务动作质感 | 裁决快门 | 运动镜和静场参数一样 |
| S3 | FIELD-CAP-ISO-WB-03 | 当前光色条件如何被吃住 | 裁决 ISO 与白平衡 | 参数与光色打架 |
| S4 | FIELD-CAP-TEXTURE-04 | 质感该如何落地 | 裁决滤镜与曝光倾向 | 只有参数名，没有质感意图 |
| S5 | FIELD-CAP-BOUNDARY-05 | 需不需要回退上游 | 写静态光学冲突留口 | 本层偷偷改焦距光圈 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-CAP-SRC-01 | 来源清楚，可回查上游证据 | FAIL-CAP-SRC-01 | S1 |
| FIELD-CAP-SHUTTER-02 | 快门与动作质感自洽 | FAIL-CAP-SHUTTER-02 | S2 |
| FIELD-CAP-ISO-WB-03 | ISO 与白平衡匹配当前光色条件 | FAIL-CAP-ISO-WB-03 | S3 |
| FIELD-CAP-TEXTURE-04 | 滤镜与曝光倾向具体可执行 | FAIL-CAP-TEXTURE-04 | S4 |
| FIELD-CAP-BOUNDARY-05 | 对静态光学边界有明确留口 | FAIL-CAP-BOUNDARY-05 | S5 |
