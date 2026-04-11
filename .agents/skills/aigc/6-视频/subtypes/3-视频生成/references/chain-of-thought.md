# 3-视频生成思维链细则

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-VIDSUB-ROOT-01 | `submit-brief.md / tranche 判定` | 说明当前任务为何属于提交前组织层 | S1 | 边界清晰度 | FAIL-VIDSUB-ROOT-01 |
| FIELD-VIDSUB-INPUT-02 | `submit-plan.json / source_request` | 记录稳定请求对象来源与版本 | S2 | 输入可追溯性 | FAIL-VIDSUB-INPUT-02 |
| FIELD-VIDSUB-PROVIDER-03 | `submit-plan.json / provider` | 给出唯一 provider 或明确推荐主案 | S3 | 路由准确性 | FAIL-VIDSUB-PROVIDER-03 |
| FIELD-VIDSUB-PACK-04 | `submit-plan.json / handoff` | 形成提交参数、目标目录与执行说明 | S4 | 提交计划完整性 | FAIL-VIDSUB-PACK-04 |
| FIELD-VIDSUB-HANDOFF-05 | `submit-brief.md / next_entry` | 给出唯一下一入口与返工入口 | S5 | 交接可执行性 | FAIL-VIDSUB-HANDOFF-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-VIDSUB-ROOT-01 | 当前任务是不是提交前组织层 | 锁定 tranche 边界与排除项 | 本层开始重写 prompt 或剧情 |
| S2 | FIELD-VIDSUB-INPUT-02 | 当前请求对象是否可提交 | 记录 source request 与 readiness verdict | 没有稳定请求对象却继续向下 |
| S3 | FIELD-VIDSUB-PROVIDER-03 | 应该交给哪个 provider | 给唯一 provider 或推荐主案 | 同时给多个无序 provider |
| S4 | FIELD-VIDSUB-PACK-04 | handoff 包要包含什么 | 输出 `submit-plan.json` 主体 | 只留口头说明 |
| S5 | FIELD-VIDSUB-HANDOFF-05 | 下一步到底去哪 | 给唯一下一入口与返工入口 | 执行者仍需自己猜下一步 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-VIDSUB-ROOT-01 | tranche 边界与排除项清楚 | FAIL-VIDSUB-ROOT-01 | S1 |
| FIELD-VIDSUB-INPUT-02 | source request 可追溯且状态明确 | FAIL-VIDSUB-INPUT-02 | S2 |
| FIELD-VIDSUB-PROVIDER-03 | provider 唯一或推荐主案明确 | FAIL-VIDSUB-PROVIDER-03 | S3 |
| FIELD-VIDSUB-PACK-04 | `submit-plan.json` 可供下游直接消费 | FAIL-VIDSUB-PACK-04 | S4 |
| FIELD-VIDSUB-HANDOFF-05 | 下一入口与返工入口明确 | FAIL-VIDSUB-HANDOFF-05 | S5 |
