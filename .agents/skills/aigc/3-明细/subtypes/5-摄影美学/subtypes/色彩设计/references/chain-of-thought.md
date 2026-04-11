# aigc 3-明细 / 5-摄影美学 / 色彩设计 / Chain Of Thought

本文件承载 `aigc 3-明细 / 5-摄影美学 / 色彩设计` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-CLR-SRC-01 | 执行报告.来源卡 | 锁定镜位、场次、分组与上游 handoff | S1 | 来源可追溯性 | FAIL-CLR-SRC-01 |
| FIELD-CLR-PALETTE-02 | `摄影美学.色彩` 字段 | 写清主色系统与显色载体 | S2 | 主色系统清晰度 | FAIL-CLR-PALETTE-02 |
| FIELD-CLR-CONTRAST-03 | `摄影美学.色彩` 字段 | 写清主辅色对位与冷暖关系 | S3 | 色彩张力 | FAIL-CLR-CONTRAST-03 |
| FIELD-CLR-RHYTHM-04 | `摄影美学.色彩` 字段 | 写清饱和与明度节奏、情绪导向 | S4 | 节奏与情绪可读性 | FAIL-CLR-RHYTHM-04 |
| FIELD-CLR-HANDOFF-05 | 执行报告.留口 | 标出需要参数层继续处理的问题 | S5 | 交接可执行性 | FAIL-CLR-HANDOFF-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-CLR-SRC-01 | 这镜的证据从哪来 | 锁定镜位与 handoff | 无来源就开始配色 |
| S2 | FIELD-CLR-PALETTE-02 | 这镜的综合色板是什么 | 裁决主色系统与载体 | 只有色名，没有载体 |
| S3 | FIELD-CLR-CONTRAST-03 | 张力从哪里来 | 补主辅色与冷暖对位 | 画面只有一种平色 |
| S4 | FIELD-CLR-RHYTHM-04 | 节奏和情绪如何成立 | 写饱和明度节奏与心理导向 | 色彩很满但无情绪组织 |
| S5 | FIELD-CLR-HANDOFF-05 | 后面谁来接 | 写给参数层的留口 | 曝光与白平衡问题无人处理 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-CLR-SRC-01 | 来源清楚，可回查上游证据 | FAIL-CLR-SRC-01 | S1 |
| FIELD-CLR-PALETTE-02 | 主色系统明确且有显色载体 | FAIL-CLR-PALETTE-02 | S2 |
| FIELD-CLR-CONTRAST-03 | 主辅色与冷暖关系清楚 | FAIL-CLR-CONTRAST-03 | S3 |
| FIELD-CLR-RHYTHM-04 | 饱和明度节奏与情绪导向成立 | FAIL-CLR-RHYTHM-04 | S4 |
| FIELD-CLR-HANDOFF-05 | 有明确后续留口 | FAIL-CLR-HANDOFF-05 | S5 |
