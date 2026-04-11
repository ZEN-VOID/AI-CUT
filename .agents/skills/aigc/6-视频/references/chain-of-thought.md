# 6-视频父级思维链细则

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-VIDEO-ROOT-01 | 阶段输入归属 | 明确 `编导/第N集.json` 与可选主体/画面锚点 | S1 | 输入真源清晰度 | FAIL-VIDEO-ROOT-01 |
| FIELD-VIDEO-ROOT-02 | 唯一路由 | 当前视频任务只进入一个子路径 | S2 | 路由唯一性 | FAIL-VIDEO-ROOT-02 |
| FIELD-VIDEO-ROOT-03 | 请求对象边界 | 明确本阶段产物是请求 JSON/参照包，而不是直接提交命令 | S3 | 阶段边界稳定性 | FAIL-VIDEO-ROOT-03 |
| FIELD-VIDEO-ROOT-04 | 阶段落盘与 handoff | 明确 `projects/<项目名>/视频/` 落点与下游入口 | S4 | 交接可追溯性 | FAIL-VIDEO-ROOT-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-VIDEO-ROOT-01 | 本轮视频任务的权威输入是什么 | 锁定 director root file 与可选参照锚点 | 只看临时 prompt |
| S2 | FIELD-VIDEO-ROOT-02 | 当前应进入哪个唯一子路径 | 裁决 `1-提示词蒸馏/全能参照`、`1-提示词蒸馏/首帧参照` 或报告缺口 | 同时打开多个叶子路径 |
| S3 | FIELD-VIDEO-ROOT-03 | 本阶段该交付什么 | 固定请求 JSON / 参照包边界 | 把本阶段写成提交命令 |
| S4 | FIELD-VIDEO-ROOT-04 | 产物落到哪里，之后交给谁 | 写 canonical landing 与 handoff | 只有 prompt 没落点 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-VIDEO-ROOT-01 | 权威输入明确指向 `编导/第N集.json` | FAIL-VIDEO-ROOT-01 | S1 |
| FIELD-VIDEO-ROOT-02 | 只给一个可执行子路径或一个明确缺口 | FAIL-VIDEO-ROOT-02 | S2 |
| FIELD-VIDEO-ROOT-03 | 阶段边界清楚停在请求对象层 | FAIL-VIDEO-ROOT-03 | S3 |
| FIELD-VIDEO-ROOT-04 | 路径、文件与下游 handoff 清楚 | FAIL-VIDEO-ROOT-04 | S4 |
