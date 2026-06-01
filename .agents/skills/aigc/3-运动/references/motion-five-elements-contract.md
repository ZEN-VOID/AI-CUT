# Motion Five Elements Contract

本文件定义 `3-运动` 的运动描写最小可执行单元。

## Core Rule

每个被扩写的原有运动字段或动作句必须能读出五个要素。扩写只允许发生在 source 已有字段的字段值中；字段名必须逐字保留，不得新增、重命名或拆分字段。

| element | meaning | evidence |
| --- | --- | --- |
| `motion_subject` | 发生运动的角色、身体部位或被角色带动的物件 | 原文主语、动作承载者 |
| `start_point` | 运动开始的位置或姿态 | 上一画面 final_state 或当前句锚点 |
| `path` | 从起点到终点的经过路线、方向、接触面或相对移动关系 | 场景空间、参照物、动作因果 |
| `end_point` | 运动结束的位置、姿态、接触关系或状态 | 当前画面结果 |
| `reference_frame` | 用来定位起点、路径和终点的稳定参照 | 门、桌、墙、台阶、地线、对手、角色身体部位 |

方向、面向、速度、力道和身体重心是扩展属性；它们服务五要素，但不能替代五要素。

## Reference Frame Selection

### Scene / Segment Consistency Rule

- 本阶段默认尚未进入下游分组，必须按同一场景、连续动作段或相邻 motion units 建立临时 `reference_cluster`，并在 `group_reference_profile` 中记录参照簇边界；该 cluster 只用于参照系一致性判断，不得生成或改写下游分镜编号。
- 只有 source 已显式包含分镜组标题、`group_id` 或可回指的组边界时，才继承源内真实组边界并选出 `primary_reference_frame`；不得把本阶段的场景/动作段参照簇伪装成下游分镜组。
- 同一场景或连续动作段内，局部手部、眼神、重心等微动作可以使用 `local_reference_frame`，但必须能回接主参照系，不得让参照簇内表达在“门边、桌旁、她前方、那里”等之间无理由漂移。
- 主参照系切换只允许发生在场景切换、主体离开原参照范围、原参照不可见、动作重心转到新的互动对象或身体部位微动作无法由主参照解释时；切换必须记录 `reference_switch_reason`。

### Best Reference Identification Mechanism

1. 从 source、项目上下文和上一画面 final_state 中列出候选参照：场景固定物、门窗墙面、地面线/台阶、稳定道具、持续互动对象、对手/搭档、角色身体部位。
2. 按六项判断候选优先级：source 证据是否明确、空间是否稳定、同一场景/动作段内是否持续可见、是否能定位起点/路径/终点、是否贴近当前动作因果、是否能承接上一 final_state 并交给下一 unit。
3. 默认优先级为：同一场景/动作段内持续可见的固定空间锚点 > 当前持续互动对象或稳定道具 > 对手/搭档角色 > 身体部位微参照 > 抽象方向词。抽象方向词只能做补充，不能单独成为最佳参照系。
4. 选择能覆盖同一场景/动作段内最多 motion units、且不会造成路径误读的候选作为 `primary_reference_frame`；局部动作另设 `local_reference_frame` 时，正文仍应让读者知道它相对主参照落在哪里。
5. 若两个候选同样稳定，优先选 source 明示、画面中更可见、后续还会被继承的参照；若无法确定，记录 `reference_frame_basis: ambiguous` 并采用最保守可复查表达。

## Expansion Pattern

默认句式可以是：

```text
<同一 source 字段名>：在[参考系]XXX处，XXX面向XXX，从XXX沿XXX[动词]到XXX，最后在[参考系]XXX处XXX。
```

上方 `<同一 source 字段名>` 不是新增字段名，只表示输出行必须沿用 source 中已经存在的字段名。

执行时不强制套模板。只要自然中文能明确五要素，就可以调整语序，例如：

- 若 source 原字段名是 `画面（动作）`，输出仍使用 `画面（动作）` 作为字段名，只扩写冒号后的值。
- 若 source 原字段名是 `动作`，输出仍使用 `动作` 作为字段名，只扩写冒号后的值。

## Anti-Patterns

- 只写“走过去、跑过去、冲上前、转身离开”，没有起点和终点。
- 用“镜头跟随、特写、推近、摇到”替代角色运动。
- 用“旁边、前方、那里”作为唯一参照，读者无法复原空间。
- 同一场景或连续动作段内无理由连续更换参照系，导致相邻 motion units 读起来像换了空间。
- 为了统一参照系，强行使用已经不可见、已被角色离开或不能解释当前微动作的主参照。
- 补出原文没有的跳跃、翻滚、绕行、抓人、摔倒或撞击。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个被扩写的原有运动字段或动作句是否具备运动主体、起点、路径、终点和参照系？ | `GATE-MOTION-03` | `FAIL-MOTION-ELEMENTS` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT` | `motion_state_ledger` 中五要素字段和正文摘录 |
| 是否没有新增、重命名或拆分字段，且没有新增独立 `运动强化：` 字段，而是只扩写 source 原有运动承载字段值？ | `GATE-MOTION-08A` | `FAIL-MOTION-FIELD-PLACEMENT` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT`、`N5R-MOTION-REPAIR` | 正文 diff 或 field placement review |
| 参照系是否足够稳定可复查，而不是抽象方向词？ | `GATE-MOTION-04` | `FAIL-MOTION-REFERENCE` | `steps/motion-workflow.md#N5R-MOTION-REPAIR` | report 记录替换后的 reference frame |
| 同一场景或连续动作段是否建立 `group_reference_profile`，并尽量统一 `primary_reference_frame`；若输入源显式已有分镜组，是否仅继承源内组边界？ | `GATE-MOTION-04A` | `FAIL-MOTION-REFERENCE-GROUP` | `steps/motion-workflow.md#N3-MOTION-STATE-LEDGER`、`steps/motion-workflow.md#N5R-MOTION-REPAIR` | `group_reference_profile`、场景/动作段 reference frame 对照和切换理由 |
| 所选参照系是否经过最佳参照系识别机制，而不是随手选最近名词或抽象方向？ | `GATE-MOTION-04B` | `FAIL-MOTION-REFERENCE-SELECTION` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT`、`steps/motion-workflow.md#N5R-MOTION-REPAIR` | `reference_frame_basis`、候选参照和最终选择理由 |
| 扩写是否保持自然中文，而不是机械套句或参数清单？ | `GATE-MOTION-07` | `FAIL-MOTION-NATURALNESS` | `templates/output-template.md`、`N5R-MOTION-REPAIR` | review report 中的 rewrite sample |
