# aigc 3-明细 / 2-角色表现 / 内心戏 / Chain Of Thought

本文件承载 `aigc 3-明细 / 2-角色表现 / 内心戏` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-INN-SRC-01 | 执行报告.来源卡 | 锁定场次、分组、角色与上游 handoff | S1 | 来源可追溯性 | FAIL-INN-SRC-01 |
| FIELD-INN-TRIGGER-02 | 执行报告.触发卡 | 写清触发语句、情绪轴、剧情节点、题材风格与音频 cue 证据 | S2 | 触发成立性 | FAIL-INN-TRIGGER-02 |
| FIELD-INN-TYPE-03 | 执行报告.主类型卡 | 裁决 `primary_type`，若为 `内心OS` 需同时给出 `os_variant` 与理由 | S3 | 类型匹配度 | FAIL-INN-TYPE-03 |
| FIELD-INN-BLEND-04 | 执行报告.协同卡 | 判定是否需要 `secondary_type`，并锁 `blend_mode / landing_mode / landing_order` | S4 | 组合合法性 | FAIL-INN-BLEND-04 |
| FIELD-INN-LANDING-05 | 终稿.主观落点 | 将主观层落成自然句，至少含一个可见动作/物象，不得显式输出类型标签 | S5 | 内层可见性 | FAIL-INN-LANDING-05 |
| FIELD-INN-RECOVERY-06 | 终稿.回收钩子 | 把角色拉回当下动作、关系对象、对白语境或下一决定 | S6 | 回收完整性 | FAIL-INN-RECOVERY-06 |
| FIELD-INN-GUARD-07 | 执行报告.门禁校验 | 逐项确认未改对白、未越权、未超密度、未跨场景漂移 | S7 | 契约遵守度 | FAIL-INN-GUARD-07 |
| FIELD-INN-HANDOFF-08 | 执行报告.留口 | 标出留给氛围/摄影层的未处理问题 | S8 | 交接可执行性 | FAIL-INN-HANDOFF-08 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-INN-SRC-01 | 这场内心戏从哪来 | 锁定场次/角色/hand off | 没有来源就写主观段 |
| S2 | FIELD-INN-TRIGGER-02 | 为什么此刻会内层裂开 | 按情绪轴/剧情节点/题材风格/音频 cue 建立证据卡 | 主观段无因而起或 cue 不可追溯 |
| S3 | FIELD-INN-TYPE-03 | 该用哪一种主类型 | 依 `NRVM-3D` 裁决主类型；若是 `内心OS`，继续锁 `OS-V1~V6` | 类型与情绪节点不匹配 |
| S4 | FIELD-INN-BLEND-04 | 是否真的需要辅类型 | 只有在提供第二叙事价值时才开放 `1 主 + 1 辅`，并规范落盘模式 | 同义重复、时间冲突或落点漂移 |
| S5 | FIELD-INN-LANDING-05 | 主观层如何可见 | 按自然句落盘，至少写出一个镜头可见锚点 | 只有抽象情绪词或标签式行首 |
| S6 | FIELD-INN-RECOVERY-06 | 如何回到现实层 | 补动作/关系/对白语境/下一决定回钩 | 主观段悬空或非现实段吞掉现实层 |
| S7 | FIELD-INN-GUARD-07 | 是否触发硬禁令 | 校验对白逐字不变、单段单条、单场密度、非现实就近落盘 | 改对白、超密度、跨段漂移、越权扩写 |
| S8 | FIELD-INN-HANDOFF-08 | 后续谁来接 | 写给氛围/摄影层的留口 | 当前层把所有美术问题吞掉 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-INN-SRC-01 | 来源明确，可回查上游证据 | FAIL-INN-SRC-01 | S1 |
| FIELD-INN-TRIGGER-02 | 触发点成立，不凭空主观化 | FAIL-INN-TRIGGER-02 | S2 |
| FIELD-INN-TYPE-03 | 主类型唯一，且与触发证据匹配；`内心OS` 已完成 IOS-Visual 裁决 | FAIL-INN-TYPE-03 | S3 |
| FIELD-INN-BLEND-04 | 辅类型仅在提供第二价值时成立，且 `blend_mode / landing_mode` 合法 | FAIL-INN-BLEND-04 | S4 |
| FIELD-INN-LANDING-05 | 主观层可见、可感、不空泛，且没有标签式写法 | FAIL-INN-LANDING-05 | S5 |
| FIELD-INN-RECOVERY-06 | 有明确回收钩子，能回到现实动作或对白语境 | FAIL-INN-RECOVERY-06 | S6 |
| FIELD-INN-GUARD-07 | 未改对白、未新增关键事实、密度合规、未跨场景漂移 | FAIL-INN-GUARD-07 | S7 |
| FIELD-INN-HANDOFF-08 | 有后续 sibling 留口 | FAIL-INN-HANDOFF-08 | S8 |
