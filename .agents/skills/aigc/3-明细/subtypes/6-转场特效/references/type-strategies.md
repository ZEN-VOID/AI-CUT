# aigc 3-明细 / 6-转场特效 / Type Strategies

本文件承载 `aigc 3-明细 / 6-转场特效` 的路由策略、VSM 与局部回退规则。

## VSM

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-TRN-SCRIPT | 输入 | `第N集.json` 是否存在且可读 | `ready/missing/invalid` | 路径与结构检查 | P0 |
| V-TRN-STORYBOARD | 上游 | `分镜明细[]` 骨架是否已完成 | `ready/missing/drift` | 分镜节点扫描 | P0 |
| V-TRN-HANDOFF | 上游 | 是否具备编导、角色、运镜增强证据 | `full/partial/missing` | handoff 与正文信号扫描 | P1 |
| V-TRN-ANCHOR | 内容 | 是否提取到边界/动作/声音/母题锚点 | `full/partial/missing` | 段落与分镜联合阅读 | P0 |
| V-TRN-PACK | 策略 | 包装层与主桥接路径是否成立 | `fit/risk/missing` | 锚点与下一落点联合检查 | P0 |
| V-TRN-INLINE | 输出 | `转场特效` 字段是否存在且写位正确 | `pass/missing/drift` | 字段写位检查 | P0 |
| V-TRN-REPETITION | 质量 | 是否出现模板化重复转场 | `distinct/repetitive/flat` | 动词与句法重复检查 | P0 |
| V-TRN-BOUNDARY | 边界 | 是否越权写入摄影/氛围或改写正文事实 | `locked/drift` | 差异检查 | P0 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-TRN-01 | `V-TRN-SCRIPT in {missing,invalid}` | 1.0 | 无 | 无 |
| C-TRN-02 | `V-TRN-STORYBOARD in {missing,drift}` | 1.0 | 无 | 可并发 C-TRN-03 |
| C-TRN-03 | `V-TRN-HANDOFF in {partial,missing}` | 0.95 | 无 | 可并发 C-TRN-04 |
| C-TRN-04 | `V-TRN-ANCHOR in {partial,missing}` | 1.0 | 无 | 可并发 C-TRN-05 |
| C-TRN-05 | `V-TRN-PACK in {risk,missing}` | 1.0 | 无 | 可并发 C-TRN-06 |
| C-TRN-06 | `V-TRN-INLINE in {missing,drift}` | 1.0 | 无 | 可并发 C-TRN-07 |
| C-TRN-07 | `V-TRN-REPETITION in {repetitive,flat}` | 0.95 | 无 | 可并发 C-TRN-08 |
| C-TRN-08 | `V-TRN-BOUNDARY=drift` | 1.0 | 无 | 无 |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-TRN-01 | S-TRN-INPUT | 先修统一根文件或回到父级建主文件 | `第N集.json` 可读 | S-TRN-PAUSE | 主文件持续缺失 |
| C-TRN-02 | S-TRN-BACK-TO-STORYBOARD | 停止本层并回退 `1-分镜表现` | `分镜明细[]` 骨架恢复 | S-TRN-PAUSE | 上游骨架不可恢复 |
| C-TRN-03 | S-TRN-HANDOFF-RELOAD | 补读 `2-组间` 与角色/运镜层证据 | 输入链完整 | S-TRN-MINIMAL | 上游证据确实不足 |
| C-TRN-04 | S-TRN-DISCOVER | 重做锚点提取 | 边界/动作/声音/母题锚点齐全 | S-TRN-MINIMAL | 两轮后仍缺锚点 |
| C-TRN-05 | S-TRN-PACK-RELOCK | 重裁决包装层、桥接表面与下一落点 | 主桥接路径可解释 | S-TRN-MINIMAL | 连续两轮仍不成立 |
| C-TRN-06 | S-TRN-INLINE-REWRITE | 原位补写或重写 `转场特效` 字段 | 每个命中位都有且仅有一个 `转场特效` 写位 | S-TRN-PAUSE | 行位持续漂移 |
| C-TRN-07 | S-TRN-DETEMPLATE | 重写重复模板，拉开锚点、桥接表面与落点差异 | 组内不再机械重复 | S-TRN-MINIMAL | 连续两轮仍模板化 |
| C-TRN-08 | S-TRN-BOUNDARY-ROLLBACK | 回滚越权改动，仅保留 `转场特效` 字段 patch 与报告 | 非本层字段差异归零 | S-TRN-PAUSE | 边界回滚失败 |

### 路由与回退卡

- 判定顺序：`C-TRN-01 -> C-TRN-02 -> C-TRN-03 -> C-TRN-04 -> C-TRN-05 -> C-TRN-06 -> C-TRN-07 -> C-TRN-08`
- 默认回退：
  - 缺 `分镜明细[]`，回到 `1-分镜表现`
  - 缺运镜残势或角色压力证据，优先补读 `3-运镜手法` 与 `2-角色表现`
- unknown 默认路由：
  - 执行 `S-TRN-MINIMAL`，但仍必须满足“五问门槛”，不能退化成“更顺、更炫、更电影感”这类空话
