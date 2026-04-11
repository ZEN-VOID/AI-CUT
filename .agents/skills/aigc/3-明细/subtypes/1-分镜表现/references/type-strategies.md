# aigc 3-明细 / 1-分镜表现 / Type Strategies

本文件承载 `aigc 3-明细 / 1-分镜表现` 的路由策略、VSM 与局部回退规则。

## 子路径路由矩阵

| 子路径 | kind | 默认调度 | tranche | 触发条件 | 主职责 |
| --- | --- | --- | --- | --- | --- |
| `分镜密度` | `unordered` | 显式串行前置 | `T1` | 需要先决定某组切几镜、每镜挂到哪些句段 | `panel_count`、句段锚点、密度理由 |
| `分镜构图` | `unordered` | 显式串行后置 | `T2` | 已有 `panel_count`，需要为每镜补静态镜头字段 | 景别、景深、构图风格等字段 |

硬规则：

1. 两个子技能目录名都不带数字前缀，默认属于 `unordered`，但本父级显式规定必须串行执行 `分镜密度 -> 分镜构图`。
2. 未完成密度裁决前，不得直接写构图字段。
3. 未完成构图字段前，不得直接把 `分镜明细[]` 节点字段块写回主文件。

## VSM

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SBP-SOURCE | 输入 | grouped source 是否可读 | `ready/missing/invalid` | 路径与结构检查 | P0 |
| V-SBP-GROUP | 结构 | 分组锚点是否稳定 | `stable/weak/broken` | 标题与分组块扫描 | P0 |
| V-SBP-DENSITY | 内容 | 每组是否已有合理 `panel_count` | `ready/missing/invalid` | 读取密度裁决结果 | P0 |
| V-SBP-COMPOSITION | 内容 | 每镜静态字段是否齐 | `ready/missing/invalid` | 读取构图结果 | P0 |
| V-SBP-INLINE | 结构 | `分镜明细[]` 节点是否正确插入 | `pass/drift` | 锚点前置检查 | P0 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SBP-01 | `V-SBP-SOURCE in {missing,invalid}` | 1.0 | 无 | 无 |
| C-SBP-02 | `V-SBP-GROUP in {weak,broken}` | 1.0 | 无 | 可并发 C-SBP-03 |
| C-SBP-03 | `V-SBP-DENSITY in {missing,invalid}` | 1.0 | 无 | 可并发 C-SBP-04 |
| C-SBP-04 | `V-SBP-COMPOSITION in {missing,invalid}` | 1.0 | 无 | 可并发 C-SBP-05 |
| C-SBP-05 | `V-SBP-INLINE=drift` | 1.0 | 无 | 无 |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SBP-01 | S-SBP-INPUT | 回退并锁定合法 grouped source | 输入唯一且可读 | S-SBP-PAUSE | 仍找不到源文本 |
| C-SBP-02 | S-SBP-GROUP | 先修分组锚点，再进入分镜插入 | 每组边界可定位 | S-SBP-PAUSE | 分组结构不可恢复 |
| C-SBP-03 | S-SBP-DENSITY | 先跑 `分镜密度` | 每组有唯一 `panel_count` | S-SBP-PAUSE | 两轮后仍无结论 |
| C-SBP-04 | S-SBP-COMPOSITION | 再跑 `分镜构图` | 每镜静态字段齐全 | S-SBP-PAUSE | 字段仍无法自洽 |
| C-SBP-05 | S-SBP-INLINE | 回滚并重写内联位置 | `分镜明细[]` 节点全部位于相关句段之前 | S-SBP-PAUSE | 锚点仍漂移 |
