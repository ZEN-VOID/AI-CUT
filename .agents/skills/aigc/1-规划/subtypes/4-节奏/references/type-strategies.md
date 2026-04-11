# 节奏 VSM 策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-RO-01 | 授权 | `original_adherence` 是否允许独立执行 `4-节奏` | `allow/forbid/missing` | 读取 `north_star.yaml` 与 `init_handoff.yaml` | P0 |
| V-RO-02 | 容器 | 分组结果是否清楚 | `clear/thin/missing` | 读取 `1-规划/3-分组/第N集.md` | P0 |
| V-RO-03 | 叙事 | 本集主驱动类型 | `event/relation/mystery/mood` | 抽检分组职责与冲突中心 | P0 |
| V-RO-04 | 风险 | 当前方案是否过度模板化 | `safe/risk/fail` | 检查冷开场/硬反转/统一 cliffhanger 堆叠 | P1 |
| V-RO-05 | 连续性 | 重排是否破坏时空与知情边界 | `safe/risk/fail` | 对照分组顺序与角色知情线 | P0 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-RO-01 | `V-RO-01=forbid` | 1.0 | 无 | 无 |
| C-RO-02 | `V-RO-02 in {thin,missing}` | 1.0 | 无 | 可并发 C-RO-04/C-RO-05 |
| C-RO-03 | `V-RO-03=event/relation/mystery/mood` | 0.95 | 四类互斥 | 可并发 C-RO-04/C-RO-05 |
| C-RO-04 | `V-RO-04 in {risk,fail}` | 1.0 | 无 | 可并发 C-RO-03/C-RO-05 |
| C-RO-05 | `V-RO-05 in {risk,fail}` | 1.0 | 无 | 可并发 C-RO-03/C-RO-04 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-RO-01 | S-RO-STOP | 停止本技能并返回保序结论 | 不生成节奏蓝图 | 无 | 用户改写授权 |
| C-RO-02 | S-RO-CONTAINER | 先补分组容器再继续 | 分组 ID 与职责清晰 | S-RO-PAUSE | 仍缺容器 |
| C-RO-03 | S-RO-DRIVE | 按主驱动决定节奏蓝图与峰值组织 | 主驱动与七步相互支撑 | S-RO-SAFE | 两轮后仍不清楚 |
| C-RO-04 | S-RO-DELABEL | 移除无收益的显性手法，回到主驱动路由 | 模板风险下降 | S-RO-SAFE | 仍机械 |
| C-RO-05 | S-RO-RELINK | 修复时空桥接与知情边界，再决定是否保留重排 | 连续性复核通过 | S-RO-SAFE | 仍断裂 |

## 路由与回退卡

- 判定顺序：`原作节奏保留门 -> 分组容器 -> 主驱动 -> 反机械化 -> 连续性 -> 下游 handoff`
- unknown 默认路由：暂停扩写，不做结构级节奏蓝图
- 失败重试上限：2
- 停止条件：缺授权、缺分组容器、连续性无法自洽
