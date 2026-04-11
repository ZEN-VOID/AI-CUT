# 2-组间阶段思维链与字段主表

## 角色定位

- 本文件承载 `2-组间` 根技能的字段中心化思维链细则。
- 主 `SKILL.md` 只保留阶段定位、路由门禁、落点合同与回指关系。
- 若阶段字段、思维链步骤或返工入口需要升级，优先修改本文件。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-DIR-ROOT-01 | 阶段定位 | 明确 `2-组间` 是脚本前的组间真源层 | S1 | 阶段边界清晰度 | FAIL-DIR-ROOT-01 |
| FIELD-DIR-ROUTE-02 | 子路径路由矩阵 | 明确三个子路径的进入条件、tranche 与落点 | S2 | 路由完整性 | FAIL-DIR-ROUTE-02 |
| FIELD-DIR-LAND-03 | Canonical Landing | 锁定 `projects/<项目名>/编导/第N集.json` 及组级字段责任 | S3 | 落点一致性 | FAIL-DIR-LAND-03 |
| FIELD-DIR-HANDOFF-04 | 阶段闭环 | 说明如何交给 `3-明细` | S4 | 交接可执行性 | FAIL-DIR-HANDOFF-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-DIR-ROOT-01 | `2-组间` 到底负责什么 | 锁定阶段边界 | 把组间设计写成脚本或规划 |
| S2 | FIELD-DIR-ROUTE-02 | 当前任务应进入哪个子路径 | 写路由矩阵与 tranche | 只有目录，没有入口 |
| S3 | FIELD-DIR-LAND-03 | 产物应落到哪里 | 固定路径 | 共享约束与分组动态落点混乱 |
| S4 | FIELD-DIR-HANDOFF-04 | 如何交给 `3-明细` | 写阶段闭环 | 能写但无法续跑 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-DIR-ROOT-01 | 阶段边界清楚且不越权 | FAIL-DIR-ROOT-01 | S1 |
| FIELD-DIR-ROUTE-02 | 子路径、tranche、进入条件、落点完整 | FAIL-DIR-ROUTE-02 | S2 |
| FIELD-DIR-LAND-03 | 所有产物路径一致 | FAIL-DIR-LAND-03 | S3 |
| FIELD-DIR-HANDOFF-04 | 有验收与唯一下一入口 | FAIL-DIR-HANDOFF-04 | S4 |
