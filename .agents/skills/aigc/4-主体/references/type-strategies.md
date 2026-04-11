# 4-主体 VSM 与路由策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SUBJECT-01 | 主链 | `1-清单 / 2-设计` 是否已完成 | `missing_inventory / missing_design / complete` | 读取 `projects/<项目名>/4-主体/` 现有产物 | P0 |
| V-SUBJECT-02 | 任务意图 | 用户当前要抽取、设计、复核还是布局 | `inventory / design / audit / panel / vague` | 解析用户请求与现有产物 | P0 |
| V-SUBJECT-03 | 运行时 | 顾问团是否启用 | `disabled / planning_only / planning_and_review` | 读取 `projects/<项目名>/team.yaml` | P1 |
| V-SUBJECT-04 | 下游阻塞 | 是否因一致性或参照面不足卡住下游 | `none / needs_audit / needs_panel` | 结合 `5-画面 / 6-视频` 消费反馈与阶段现状 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SUBJECT-01 | `V-SUBJECT-01=missing_inventory` | 1.0 | 互斥 `C-SUBJECT-02` | 可并发 `C-SUBJECT-03` |
| C-SUBJECT-02 | `V-SUBJECT-01=missing_design` | 1.0 | 互斥 `C-SUBJECT-01` | 可并发 `C-SUBJECT-03` |
| C-SUBJECT-03 | `V-SUBJECT-03 in {planning_only, planning_and_review}` | 1.0 | 无 | 可并发全部 |
| C-SUBJECT-04 | `V-SUBJECT-04=needs_audit` | 0.90 | 无 | 可并发 `C-SUBJECT-03` |
| C-SUBJECT-05 | `V-SUBJECT-04=needs_panel` | 0.90 | 无 | 可并发 `C-SUBJECT-03` |
| C-SUBJECT-06 | `V-SUBJECT-02=vague` | 0.85 | 无 | 可并发 `C-SUBJECT-01/C-SUBJECT-02` |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SUBJECT-01 | S-SUBJECT-INVENTORY | 先补 `1-清单`，锁主体池、命名与 bridge | `2-设计` 不再需要重做抽取 | S-SUBJECT-CLARIFY | 上游脚本仍不稳定 |
| C-SUBJECT-02 | S-SUBJECT-DESIGN | 在 `1-清单` 基础上形成设计真源 | 至少形成人读卡 + 机读侧车 | S-SUBJECT-INVENTORY | bridge 缺失或冲突 |
| C-SUBJECT-03 | S-SUBJECT-COUNCIL | 启用 `策划前置 + 评审闸门` | 顾问意见被显式整合 | S-SUBJECT-DIRECT | 环境无法并发 |
| C-SUBJECT-04 | S-SUBJECT-AUDIT | 进入 `3-审计` 收束失败维度与返工入口 | 每条问题可回链上游约束 | S-SUBJECT-DESIGN | 证据链不足 |
| C-SUBJECT-05 | S-SUBJECT-PANEL | 进入 `4-面板` 形成统一参照面 | 面板不越权二次设计 | S-SUBJECT-AUDIT | 关键失败项未关闭 |
| C-SUBJECT-06 | S-SUBJECT-DEFAULT | 按“最高优先级未完成主链阶段”路由 | 路由结果唯一 | S-SUBJECT-PAUSE | 仍无法判定 |

## 子路径路由矩阵

| 子路径 | kind | 默认调度 | tranche | 当前状态 | 触发条件 | 主职责 |
| --- | --- | --- | --- | --- | --- | --- |
| `1-清单` | `ordered` | 串行首站 | `T1` | 已建合同 | 需要先从脚本中提取角色/场景/道具并做主体归一 | 主体抽取、研究桥接、连续性建档 |
| `2-设计` | `ordered` | 串行第二站 | `T2` | 已建合同 | 已有主体清单，需要形成设计真源 | 主体卡、设计侧车、下游消费入口 |
| `3-审计` | `ordered` | 显式按需 | `T3-opt` | 已建合同 | 设计已出，需要复核、修正或回写 | 主体一致性审计与修订裁决 |
| `4-面板` | `ordered` | 显式按需 | `T4-opt` | 已建合同 | 需要把主体进一步布局化为参照板 | 布局板、面板文案、下游参照面 |

## 路由与回退卡

- 判定顺序：`主链完成度 -> 用户任务意图 -> 顾问团运行时 -> 下游阻塞`
- 冲突解消规则：主链未完成时，优先级永远高于扩展链诉求
- unknown 默认路由：回到“最高优先级未完成主链阶段”
- 失败重试上限：2
- 停止条件：`3-明细` 真源仍在大幅漂移，无法稳定抽取主体
