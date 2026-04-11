# aigc 3-明细 / 1-分镜表现 / 分镜密度 / Chain Of Thought

本文件承载 `aigc 3-明细 / 1-分镜表现 / 分镜密度` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SBD-01 | `base_range` | 按节奏给出唯一基础区间 | S1 | 节奏裁决准确性 | FAIL-SBD-RHYTHM-RANGE |
| FIELD-SBD-02 | `refined_range` | 按 `scene_type + duration + info_load` 收窄后的合法区间 | S2 | 区间收窄合理性 | FAIL-SBD-REFINED-RANGE |
| FIELD-SBD-03 | `panel_count` | 每组有唯一整数镜数，落在 `1-15` | S3 | 密度合理性 | FAIL-SBD-PANEL-COUNT |
| FIELD-SBD-04 | `句段锚点表` | 每镜有挂点与覆盖说明 | S4 | 锚点稳定性 | FAIL-SBD-ANCHOR-MAP |
| FIELD-SBD-05 | `decision_reason` | 说明为何取此镜数，以及为何不取相邻值 | S5 | 可解释性 | FAIL-SBD-DECISION-REASON |
| FIELD-SBD-06 | `功能位` | 至少标注建立/推进/揭示/收束中的一种 | S6 | 节奏组织性 | FAIL-SBD-FUNCTION-FLAT |
| FIELD-SBD-07 | `aesthetic_peak_plan` | 至少预留一帧视觉峰值机会；若 `panel_count=1` 需额外说明其强度 | S3 | 审美势能 | FAIL-COMPOSITION-FLATLINE |
| FIELD-SBD-08 | `template_gate_verdict` | 根据 `panel_count -> template_id` 映射，检查景别/角度/滑窗/附加约束是否可成立 | S6 | 反平庸门控 | FAIL-SBD-TEMPLATE-GATE |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SBD-01 | 这组戏的呼吸是什么 | 按节奏锁定 `base_range` | 基础区间漂移或越界 |
| S2 | FIELD-SBD-02 | 这组戏必须让观众看到什么、感到什么 | 按 `scene_type + duration + info_load` 收窄到 `refined_range`，并检查 `single_panel_long_take` 资格 | 直接跳到具体镜数，缺少收窄过程 |
| S3 | FIELD-SBD-03, FIELD-SBD-07 | 几次切换最能保住力量，且至少有一帧不敢眨眼 | 枚举候选整数，执行可拍性检查、`Aesthetic Pressure Test` 与反平庸取高 | 候选值缺测试，或全是安全平镜 |
| S4 | FIELD-SBD-04 | 每镜挂在哪句之前 | 生成锚点表 | 一镜无挂点 |
| S5 | FIELD-SBD-05 | 为什么是这个镜数，而不是相邻值 | 写决策理由与回退说明 | 只有数字，没有排除依据 |
| S6 | FIELD-SBD-06, FIELD-SBD-08 | 这些镜在组内各担什么任务，且能否通过模板级反平庸门控 | 标功能位，并按 `template_id` 预检查景别/角度/滑窗/附加约束 | 功能位塌缩，或模板门控显然不成立 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SBD-01 | `base_range` 与节奏标签一致，且落在 `1-15` 合法域 | FAIL-SBD-RHYTHM-RANGE | S1 |
| FIELD-SBD-02 | `refined_range` 来自合法交集；若为空，已显式记录节奏优先回退 | FAIL-SBD-REFINED-RANGE | S2 |
| FIELD-SBD-03 | `panel_count` 唯一、可拍、可读，且 `1帧` 仅在特例命中时成立 | FAIL-SBD-PANEL-COUNT | S3 |
| FIELD-SBD-04 | 每镜锚点清晰 | FAIL-SBD-ANCHOR-MAP | S4 |
| FIELD-SBD-05 | 决策理由完整，能解释为何取该值而不取相邻值 | FAIL-SBD-DECISION-REASON | S5 |
| FIELD-SBD-06 | 功能位分配可解释 | FAIL-SBD-FUNCTION-FLAT | S6 |
| FIELD-SBD-07 | 至少有一帧具备审美峰值潜力；若全组只能导向安全常规构图，触发失败 | FAIL-COMPOSITION-FLATLINE | S3 |
| FIELD-SBD-08 | 所选 `panel_count` 对应模板的景别多样性、角度多样性、滑动窗口与附加约束均可成立 | FAIL-SBD-TEMPLATE-GATE | S6 |

## Template Gate Hook (Mandatory)

- 模板级反平庸门控的完整矩阵以 `.agents/skills/aigc/3-明细/references/output-template.md` 为真源。
- `chain-of-thought` 只负责规定何时检查、失败如何返工，不在本文件复制第二套完整模板表。
- 若 `template_gate_verdict=fail`，优先回到 `S6` 重排功能位与锚点；若仍无法满足，再回到 `S3` 重选候选值。
