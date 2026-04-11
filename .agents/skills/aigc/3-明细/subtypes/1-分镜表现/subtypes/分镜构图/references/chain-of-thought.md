# aigc 3-明细 / 1-分镜表现 / 分镜构图 / Chain Of Thought

本文件承载 `aigc 3-明细 / 1-分镜表现 / 分镜构图` 的字段主表、思维链与返工入口真源。

执行前提：

- `panel_count / template_id / candidate_counts / decision_reason` 已由上游 `分镜密度` 锁定。
- 本层默认不重跑候选镜数比较，只把上游结果落成真实可拍的逐帧构图。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SBC-01 | 上游继承位 | `panel_count / template_id / group_duration` 均可追溯 | S1 | 真源继承准确性 | FAIL-SBC-UPSTREAM |
| FIELD-SBC-02 | `scene_type` | 主类型判定可解释，未知时有默认回退 | S2 | 类型判定稳定性 | FAIL-SBC-SCENE-TYPE |
| FIELD-SBC-03 | `时间` | 连续、闭合且符合组总时长 | S3 | 时间连续性 | FAIL-TIME-CONTINUITY |
| FIELD-SBC-04 | canonical shot 字段 | 每镜字段齐全且自洽 | S4 | 完整性 | FAIL-SBC-FIELDS |
| FIELD-SBC-05 | 模板落地 | 实际镜头设计满足上游 `template_id` 门槛 | S5 | 反平庸成立度 | FAIL-ANTI-MEDIOCRITY |
| FIELD-SBC-06 | 审美峰值镜 | 至少一镜形成全组最大胆的构图峰值 | S5 | 审美振幅 | FAIL-SBC-PEAK |
| FIELD-SBC-07 | 组间回溯 | 同场景相邻组首帧能回溯上一组尾势 | S2 | 连续性 | FAIL-INTERGROUP-ECHO-MISSING |
| FIELD-SBC-08 | 父级投影与边界 | 八字段投影可回写，且无越界项 | S6 | 边界控制 | FAIL-SBC-SCOPE |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SBC-01 | 上游镜数与组总时长真源是否已经锁住 | 继承 `panel_count / template_id / duration chain`，不重开第二裁决 | 上游真源缺失，或把整集时长误当组时长 |
| S2 | FIELD-SBC-02, FIELD-SBC-07 | 这一组究竟是什么戏、是否需要承接上一组尾势 | 判 `scene_type`，并在同场景时给首帧补回溯锚 | 类型漂移，或首帧与上一组断开 |
| S3 | FIELD-SBC-03 | 这些镜各持续多久才可拍、可读 | 按 `scene_type + rhythm + group_duration` 切连续时间段 | 时间不连续，或总时长不闭合 |
| S4 | FIELD-SBC-04 | 每一镜究竟如何被观看 | 补 canonical shot 字段，并锁 `角色及站位 / 构图布局 / 构图方式 / 摄影参数` | 字段残缺，或只剩安全模板 |
| S5 | FIELD-SBC-05, FIELD-SBC-06 | 上游模板门槛是否在真实镜头里成立，哪一镜最不敢眨眼 | 检查景别/角度/滑窗/功能位，并指定全组最大胆峰值镜 | 全组平庸，或模板门槛只停留在口头 |
| S6 | FIELD-SBC-08 | 如何把 canonical shot 投影回父级，又不越权 | 生成八字段单行投影，并清理运镜/色彩/转场正文 | 回写格式漂移，或混入他层内容 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SBC-01 | `panel_count / template_id / group_duration` 三者均可追溯到上游真源 | FAIL-SBC-UPSTREAM | S1 |
| FIELD-SBC-02 | `scene_type` 可解释；未知时已显式回退并记录 | FAIL-SBC-SCENE-TYPE | S2 |
| FIELD-SBC-03 | 时间字段连续、总和正确、边界闭合 | FAIL-TIME-CONTINUITY / FAIL-TIME-OVERFLOW | S3 |
| FIELD-SBC-04 | canonical shot 字段完整，且 `转场` 为空值 | FAIL-SBC-FIELDS | S4 |
| FIELD-SBC-05 | 实际构图满足上游 `template_id` 对应门槛 | FAIL-ANTI-MEDIOCRITY | S5 |
| FIELD-SBC-06 | 至少一镜是全组最大胆、最非常规的构图峰值 | FAIL-SBC-PEAK | S5 |
| FIELD-SBC-07 | 同场景相邻组首帧完成压缩回溯，而非断裂或逐字复制 | FAIL-INTERGROUP-ECHO-MISSING / FAIL-INTERGROUP-ECHO-VERBATIM | S2 |
| FIELD-SBC-08 | 父级八字段投影稳定，且无运镜/光色/转场正文越界 | FAIL-SBC-SCOPE | S6 |
