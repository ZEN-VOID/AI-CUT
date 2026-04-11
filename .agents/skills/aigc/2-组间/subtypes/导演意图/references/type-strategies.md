# 导演意图 VSM 策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-DI-01 | 上游 | 风格与类型真源是否齐备 | `full/partial/missing` | 读取项目级文档 | P0 |
| V-DI-02 | 容器 | 分组结果是否明确 | `clear/thin/missing` | 读取 `1-规划/3-分组/第N集.md` | P0 |
| V-DI-03 | 集级 | 本集情绪线是否清楚 | `clear/mixed/thin` | 读取分集与分组材料 | P0 |
| V-DI-04 | 维度 | 五个导演维度是否覆盖完整 | `full/partial/thin` | 抽检固定区块与组级条目 | P0 |
| V-DI-05 | 翻译 | 是否已把抽象判断翻译为部门可执行语言 | `translated/mixed/abstract` | 抽检摄影/声音/表演等提示 | P0 |
| V-DI-06 | 边界 | 粒度是否越权滑向镜头脚本 | `contract-safe/mixed/overspecified` | 抽检是否出现逐镜头分镜化 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-DI-01 | `V-DI-01 in {partial,missing}` | 1.0 | 无 | 可并发 C-DI-02 |
| C-DI-02 | `V-DI-02 in {thin,missing}` | 1.0 | 无 | 可并发 C-DI-03 |
| C-DI-03 | `V-DI-03 in {mixed,thin}` | 0.95 | 无 | 可并发 C-DI-04 |
| C-DI-04 | `V-DI-04 in {partial,thin}` | 1.0 | 无 | 可并发 C-DI-05/C-DI-06 |
| C-DI-05 | `V-DI-05 in {mixed,abstract}` | 1.0 | 无 | 可并发全部 |
| C-DI-06 | `V-DI-06 in {mixed,overspecified}` | 0.95 | 无 | 可并发 C-DI-04/C-DI-05 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-DI-01 | S-DI-SOURCE | 先补齐风格/类型依赖，再继续 | 上游口径清楚 | S-DI-PAUSE | 仍缺关键真源 |
| C-DI-02 | S-DI-CONTAINER | 只围绕已存在的分组容器写作 | 每组有稳定 ID | S-DI-PAUSE | 分组仍不成立 |
| C-DI-03 | S-DI-ARC | 先拉清本集情绪线，再分组落笔 | 集级命题可复述 | S-DI-SOURCE | 情绪线仍散 |
| C-DI-04 | S-DI-FIVE-DIMENSIONS | 先补齐主题/基调/视点/视听/表演五个维度 | 五维度均有落点 | S-DI-ARC | 补齐后仍空转 |
| C-DI-05 | S-DI-TRANSLATE | 把空话改成可见画面、可听声音与可演动作 | 每组至少有部门级后果 | S-DI-FIVE-DIMENSIONS | 两轮后仍抽象 |
| C-DI-06 | S-DI-BOUNDARY | 把越权的 shot list 收回为导演法则与 handoff 原则 | 不直接代写分镜/镜头表 | S-DI-TRANSLATE | 仍持续越权 |

## 路由与回退卡

- 判定顺序：`上游真源 -> 分组容器 -> 本集命题/视点 -> 五维度覆盖 -> 部门翻译 -> 下游交接`
- unknown 默认路由：暂停扩写，要求先补风格/类型或分组容器
- 失败重试上限：2
- 停止条件：没有稳定分组容器
