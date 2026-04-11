# aigc 1-规划 / Chain Of Thought

本文件承载 `aigc 1-规划` 的字段主表、思维链摘要与返工入口真源。

## 模块定位

- 主 `SKILL.md` 只保留阶段边界、路由摘要与硬门槛。
- 本文件负责沉淀根技能级的 `field_id -> step_id -> pass/fail` 设计，尤其是上游来源类型与预设保真交接。

## 字段主表

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-PLAN-ROOT-01 | 阶段定位 | 明确 `1-规划` 是结构规划阶段，而不是编导/脚本替身 | S1 | 阶段边界清晰度 | FAIL-PLAN-ROOT-01 |
| FIELD-PLAN-ROUTE-02 | 子路径路由矩阵 | 明确 `分集 / 格式 / 分组 / 节奏` 的进入条件、状态与落点 | S2 | 路由完整性 | FAIL-PLAN-ROUTE-02 |
| FIELD-PLAN-LAND-03 | Canonical Landing | 锁定 `projects/<项目名>/规划/` 及各子路径产物落点 | S3 | 落点一致性 | FAIL-PLAN-LAND-03 |
| FIELD-PLAN-CLOSE-04 | 阶段闭环 | 说明验收、缺口报告和下一阶段唯一入口 | S4 | 闭环可执行性 | FAIL-PLAN-CLOSE-04 |
| FIELD-PLAN-SRC-05 | 来源类型与预设交接 | 锁定 `story-source-manifest.yaml -> references/type-strategies.md -> 编导根文件 source_profile -> 3-明细` 的保真链 | S5 | 类型化处理完整性 | FAIL-PLAN-SRC-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-PLAN-ROOT-01 | `1-规划` 到底负责什么 | 锁定阶段边界与上下游关系 | 把规划写成编导或脚本说明 |
| S2 | FIELD-PLAN-ROUTE-02 | 当前任务应进入哪个子路径 | 明确四个子路径的路由矩阵与状态 | 只有目录，没有进入条件 |
| S3 | FIELD-PLAN-LAND-03 | 规划结果落到哪里 | 固定阶段根目录与各子路径落点 | 产物路径漂移 |
| S4 | FIELD-PLAN-CLOSE-04 | 阶段如何结案并交接 | 固定验收、缺口报告、下一阶段推荐 | 任务完成但无法续跑 |
| S5 | FIELD-PLAN-SRC-05 | 上游是小说原文型还是分镜脚本型，后续应如何顺承 | 固定 source mode、preset retention、detail expansion mode 与回写位置 | 分镜脚本预设点只存在口头说明，没有可消费写位 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-PLAN-ROOT-01 | 阶段边界清晰且不越权 | FAIL-PLAN-ROOT-01 | S1 |
| FIELD-PLAN-ROUTE-02 | 子路径进入条件、状态、落点完整 | FAIL-PLAN-ROUTE-02 | S2 |
| FIELD-PLAN-LAND-03 | 所有规划产物路径一致 | FAIL-PLAN-LAND-03 | S3 |
| FIELD-PLAN-CLOSE-04 | 有缺口报告、验收与唯一下一入口 | FAIL-PLAN-CLOSE-04 | S4 |
| FIELD-PLAN-SRC-05 | 来源类型、预设保护规则与 `3-明细` 交接链完整 | FAIL-PLAN-SRC-05 | S5 |
