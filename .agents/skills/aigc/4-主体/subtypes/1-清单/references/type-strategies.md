# 1-清单 VSM 与域路由策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SINV-01 | 域 | 当前命中角色、场景还是道具 | `character / scene / prop / mixed` | 读取脚本段落与主体用途 | P0 |
| V-SINV-02 | 命名 | 同一主体是否存在别名或异写 | `stable / alias / ambiguous` | 做同集命名归一 | P0 |
| V-SINV-03 | 证据 | 主体用途与连续性证据是否充分 | `sufficient / partial / weak` | 回查脚本出现位置与上下文 | P1 |
| V-SINV-04 | 下游 | `2-设计` 是否需要补强解释层 | `normal / strong` | 检查 bridge 字段完备度 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SINV-01 | `V-SINV-01=mixed` | 0.95 | 无 | 可并发 `C-SINV-02` |
| C-SINV-02 | `V-SINV-02 in {alias, ambiguous}` | 0.90 | 无 | 可并发 `C-SINV-03` |
| C-SINV-03 | `V-SINV-03 in {partial, weak}` | 0.90 | 无 | 可并发全部 |
| C-SINV-04 | `V-SINV-04=strong` | 0.90 | 无 | 可并发全部 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SINV-01 | S-SINV-SPLIT | 先分域再落盘，禁止混表 | 三类主体各自独立落盘 | S-SINV-CLARIFY | 仍无法判域 |
| C-SINV-02 | S-SINV-NORMALIZE | 写规范名、别名与变体说明 | 同主体不再重复出稿 | S-SINV-HOLD | 仍无法确认是否同体 |
| C-SINV-03 | S-SINV-EVIDENCE | 标记待补字段，保留证据缺口 | 不臆造事实属性 | S-SINV-HOLD | 关键字段仍无依据 |
| C-SINV-04 | S-SINV-BRIDGE | 强化用途、连续性与设计桥接字段 | `2-设计` 可直接消费 | S-SINV-EVIDENCE | bridge 仍不足 |

## 域路由矩阵

| 域 | kind | 默认调度 | 触发条件 | 主职责 |
| --- | --- | --- | --- | --- |
| `角色` | `unordered` | 可并行分析 | 需要稳定角色身份、称谓、关系与连续性 | 生成 `角色清单.json + role_design_bridge.json` |
| `场景` | `unordered` | 可并行分析 | 需要稳定空间、功能、时段与情境用途 | 生成 `场景清单.json + scene_design_bridge.json` |
| `道具` | `unordered` | 可并行分析 | 需要稳定道具名称、所属、用途与象征性 | 生成 `道具清单.json + prop_design_bridge.json` |

## 路由与回退卡

- 判定顺序：`分域 -> 命名归一 -> 证据充分度 -> bridge 完整度`
- 冲突解消规则：证据不足时不发明属性，只写待补与来源片段
- unknown 默认路由：暂停最终归一，保留候选并显式标记待复核
- 失败重试上限：2
- 停止条件：主体身份在当前脚本版本中仍无法稳定确认
