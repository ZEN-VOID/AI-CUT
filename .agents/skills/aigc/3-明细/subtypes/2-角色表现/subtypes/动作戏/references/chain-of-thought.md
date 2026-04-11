# aigc 3-明细 / 2-角色表现 / 动作戏 / Chain Of Thought

本文件承载 `aigc 3-明细 / 2-角色表现 / 动作戏` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-ACT-SRC-01 | 执行报告.来源卡 | 锁定动作段所在场次、分组、上游 handoff；若涉及兵器，顺带锁兵器子类型证据 | S1 | 来源可追溯性 | FAIL-ACT-SRC-01 |
| FIELD-ACT-BEAT-02 | 终稿.动作节拍链 | 将关键动作拆成至少一个完整交换回合，并写清切入线与接触点 | S2-S3 | 节拍清晰度 | FAIL-ACT-BEAT-02 |
| FIELD-ACT-CAUSE-03 | 终稿.因果受力链 | 写清动作触发、受力传递、失衡改线与再逼近关系 | S4 | 因果成立性 | FAIL-ACT-CAUSE-03 |
| FIELD-ACT-SPACE-04 | 终稿.环境参与 | 让空间/道具/障碍参与动作，形成借景借物结构 | S5 | 空间可拍性 | FAIL-ACT-SPACE-04 |
| FIELD-ACT-REC-05 | 终稿.余波回收 | 在爆点后补伤势、喘息、握力松动、兵器下沉或短停顿 | S6 | 回收完整性 | FAIL-ACT-REC-05 |
| FIELD-ACT-HANDOFF-06 | 执行报告.留口 | 标出需要后续镜头/摄影层继续处理的问题 | S7 | 交接可执行性 | FAIL-ACT-HANDOFF-06 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-ACT-SRC-01 | 这段动作到底从哪来，若有兵器又属于哪一类 | 锁定场次、分组、handoff 与兵器证据 | 没有来源或兵器类型就开写 |
| S2 | FIELD-ACT-BEAT-02 | 关键动作由哪些节拍构成 | 拆成连续节拍链与完整交换回合 | 只有“打起来了” |
| S3 | FIELD-ACT-BEAT-02 | 哪些节拍最该被放大 | 锁关键爆点与承压点 | 节拍平均铺开 |
| S4 | FIELD-ACT-CAUSE-03 | 动作为什么成立 | 写触发、受力、失衡、结果 | 动作像漂浮特效 |
| S5 | FIELD-ACT-SPACE-04 | 空间如何参与动作 | 补环境、道具、障碍 | 动作发生在真空里 |
| S6 | FIELD-ACT-REC-05 | 爆点后如何回收 | 补余波、喘息、伤势与短静默 | 只有起势没有余波 |
| S7 | FIELD-ACT-HANDOFF-06 | 后面谁来接 | 写给后续 sibling 的留口 | 当前层把所有问题都硬吞 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-ACT-SRC-01 | 来源清楚，可回查到上游证据 | FAIL-ACT-SRC-01 | S1 |
| FIELD-ACT-BEAT-02 | 节拍链连续、具体、可演，且至少包含一个完整交换回合 | FAIL-ACT-BEAT-02 | S2-S3 |
| FIELD-ACT-CAUSE-03 | 动作因果、受力与失衡改线成立 | FAIL-ACT-CAUSE-03 | S4 |
| FIELD-ACT-SPACE-04 | 空间/道具参与明确，不在真空里互打 | FAIL-ACT-SPACE-04 | S5 |
| FIELD-ACT-REC-05 | 余波与回收存在，不断头，不只剩“受伤倒地” | FAIL-ACT-REC-05 | S6 |
| FIELD-ACT-HANDOFF-06 | 有明确后续留口 | FAIL-ACT-HANDOFF-06 | S7 |
