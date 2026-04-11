# aigc 3-明细 / 5-摄影美学 / 光影设计 / Chain Of Thought

本文件承载 `aigc 3-明细 / 5-摄影美学 / 光影设计` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-LGT-SRC-01 | 执行报告.来源卡 | 锁定镜位、场次、分组与上游 handoff | S1 | 来源可追溯性 | FAIL-LGT-SRC-01 |
| FIELD-LGT-SOURCE-02 | `摄影美学.光影` 字段 | 写清主光实体与方向 | S2 | 光源成立性 | FAIL-LGT-SOURCE-02 |
| FIELD-LGT-SHADOW-03 | `摄影美学.光影` 字段 | 写清阴影关系与明暗结构 | S3 | 影调可见性 | FAIL-LGT-SHADOW-03 |
| FIELD-LGT-EFFECT-04 | `摄影美学.光影` 字段 | 写清落在何物与为何存在 | S4 | 叙事作用清晰度 | FAIL-LGT-EFFECT-04 |
| FIELD-LGT-HANDOFF-05 | 执行报告.留口 | 标出需要后续色彩或参数层继续处理的问题 | S5 | 交接可执行性 | FAIL-LGT-HANDOFF-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-LGT-SRC-01 | 这镜的证据从哪来 | 锁定镜位与 handoff | 无来源就开始补光 |
| S2 | FIELD-LGT-SOURCE-02 | 光到底从哪里来 | 裁决主光实体与方向 | 只有抽象亮暗，没有光源 |
| S3 | FIELD-LGT-SHADOW-03 | 影子如何切画面 | 补明暗与阴影关系 | 只有亮，没有影调 |
| S4 | FIELD-LGT-EFFECT-04 | 为什么这样照 | 写对象绑定与叙事作用 | 光很美但无戏 |
| S5 | FIELD-LGT-HANDOFF-05 | 后面谁来接 | 写给色彩/参数层的留口 | 本层把所有问题都硬吞 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-LGT-SRC-01 | 来源清楚，可回查上游证据 | FAIL-LGT-SRC-01 | S1 |
| FIELD-LGT-SOURCE-02 | 光源实体与方向明确 | FAIL-LGT-SOURCE-02 | S2 |
| FIELD-LGT-SHADOW-03 | 明暗结构具体可见 | FAIL-LGT-SHADOW-03 | S3 |
| FIELD-LGT-EFFECT-04 | 对象绑定与叙事作用清楚 | FAIL-LGT-EFFECT-04 | S4 |
| FIELD-LGT-HANDOFF-05 | 有明确后续留口 | FAIL-LGT-HANDOFF-05 | S5 |
