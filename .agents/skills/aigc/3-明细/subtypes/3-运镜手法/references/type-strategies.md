# aigc 3-明细 / 3-运镜手法 / Type Strategies

本文件承载 `aigc 3-明细 / 3-运镜手法` 的路由策略、VSM 与局部回退规则。

## VSM

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-CAM-SCRIPT | 输入 | `第N集.json` 是否存在且可读 | `ready/missing/invalid` | 路径与结构检查 | P0 |
| V-CAM-STORYBOARD | 上游 | `分镜明细[]` 骨架是否已完成 | `ready/missing/drift` | 分镜节点扫描 | P0 |
| V-CAM-HANDOFF | 上游 | 是否具备编导与角色增强证据 | `full/partial/missing` | handoff 与正文信号扫描 | P1 |
| V-CAM-ANCHOR | 内容 | 是否提取到节拍/空间/视线锚点 | `full/partial/missing` | 段落与分镜联合阅读 | P0 |
| V-CAM-WAVE | 策略 | 组级运镜波形是否成立 | `fit/risk/missing` | 起点/路径/变速/收束联合检查 | P0 |
| V-CAM-INLINE | 输出 | `运镜手法` 字段是否存在且写位正确 | `pass/missing/drift` | 字段写位检查 | P0 |
| V-CAM-REPETITION | 质量 | 是否出现模板化重复运镜 | `distinct/repetitive/flat` | 动词与句法重复检查 | P0 |
| V-CAM-BOUNDARY | 边界 | 是否越权写入光色氛围或改写正文事实 | `locked/drift` | 差异检查 | P0 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-CAM-01 | `V-CAM-SCRIPT in {missing,invalid}` | 1.0 | 无 | 无 |
| C-CAM-02 | `V-CAM-STORYBOARD in {missing,drift}` | 1.0 | 无 | 可并发 C-CAM-03 |
| C-CAM-03 | `V-CAM-HANDOFF in {partial,missing}` | 0.95 | 无 | 可并发 C-CAM-04 |
| C-CAM-04 | `V-CAM-ANCHOR in {partial,missing}` | 1.0 | 无 | 可并发 C-CAM-05 |
| C-CAM-05 | `V-CAM-WAVE in {risk,missing}` | 1.0 | 无 | 可并发 C-CAM-06 |
| C-CAM-06 | `V-CAM-INLINE in {missing,drift}` | 1.0 | 无 | 可并发 C-CAM-07 |
| C-CAM-07 | `V-CAM-REPETITION in {repetitive,flat}` | 0.95 | 无 | 可并发 C-CAM-08 |
| C-CAM-08 | `V-CAM-BOUNDARY=drift` | 1.0 | 无 | 无 |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-CAM-01 | S-CAM-INPUT | 先修统一根文件或回到父级建主文件 | `第N集.json` 可读 | S-CAM-PAUSE | 主文件持续缺失 |
| C-CAM-02 | S-CAM-BACK-TO-STORYBOARD | 停止本层并回退 `1-分镜表现` | `分镜明细[]` 骨架恢复 | S-CAM-PAUSE | 上游骨架不可恢复 |
| C-CAM-03 | S-CAM-HANDOFF-RELOAD | 补读 `2-组间` 与角色层证据 | 输入链完整 | S-CAM-MINIMAL | 上游证据确实不足 |
| C-CAM-04 | S-CAM-DISCOVER | 重做锚点提取 | 节拍/空间/视线锚点齐全 | S-CAM-MINIMAL | 两轮后仍缺锚点 |
| C-CAM-05 | S-CAM-WAVE-RELOCK | 重裁决主路径、变速与收束位 | 波形可解释 | S-CAM-MINIMAL | 连续两轮仍不成立 |
| C-CAM-06 | S-CAM-INLINE-REWRITE | 原位补写或重写 `运镜手法` 字段 | 每个相关命中分镜节点都有且仅有一个 `运镜手法` 写位 | S-CAM-PAUSE | 行位持续漂移 |
| C-CAM-07 | S-CAM-DETEMPLATE | 重写重复模板，拉开动词、节拍与落点差异 | 组内不再机械重复 | S-CAM-MINIMAL | 连续两轮仍模板化 |
| C-CAM-08 | S-CAM-BOUNDARY-ROLLBACK | 回滚越权改动，仅保留 `运镜手法` 字段 patch 与报告 | 非本层字段差异归零 | S-CAM-PAUSE | 边界回滚失败 |

### 路由与回退卡

- 判定顺序：`C-CAM-01 -> C-CAM-02 -> C-CAM-03 -> C-CAM-04 -> C-CAM-05 -> C-CAM-06 -> C-CAM-07 -> C-CAM-08`
- 默认回退：
  - 缺 `分镜明细[]`，回到 `1-分镜表现`
  - 缺人物压力与节奏证据，优先补读 `2-角色表现` 与 `2-组间`
- unknown 默认路由：
  - 执行 `S-CAM-MINIMAL`，但仍必须满足“五问门槛”，不能退化成“轻微推进，更有电影感”这类空话
