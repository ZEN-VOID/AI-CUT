# 2-设计 VSM 与域路由策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SDES-01 | 域 | 当前命中角色、场景还是道具设计 | `character / scene / prop / mixed` | 读取 bridge 来源与任务要求 | P0 |
| V-SDES-02 | 输入 | `1-清单` bridge 是否完整 | `ready / partial / missing` | 检查 bridge 字段与证据 | P0 |
| V-SDES-03 | 交付 | 人读卡、机读 JSON、thinking 是否齐备 | `full / card_only / json_only / missing_thinking` | 对照交付件清单 | P1 |
| V-SDES-04 | 下游 | 下一步更适合审计、面板还是直接消费 | `audit / panel / downstream` | 结合用户请求与下游任务 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SDES-01 | `V-SDES-02=missing` | 1.0 | 无 | 无 |
| C-SDES-02 | `V-SDES-02=partial` | 0.95 | 无 | 可并发 `C-SDES-03` |
| C-SDES-03 | `V-SDES-03 in {card_only, json_only, missing_thinking}` | 0.90 | 无 | 可并发 `C-SDES-04` |
| C-SDES-04 | `V-SDES-04 in {audit, panel}` | 0.90 | 无 | 可并发全部 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SDES-01 | S-SDES-BLOCK | 停止设计，回到 `1-清单` 补 bridge | 不以猜测替代输入真源 | S-SDES-CLARIFY | 上游脚本仍未稳定 |
| C-SDES-02 | S-SDES-RECONCILE | 先补齐 bridge 缺口，再出设计 | bridge 与设计不冲突 | S-SDES-BLOCK | 关键字段仍缺失 |
| C-SDES-03 | S-SDES-TRIPLE | 补齐设计卡、JSON 与 thinking 三件套 | 三件套全部存在 | S-SDES-RECONCILE | 输出仍不齐 |
| C-SDES-04 | S-SDES-HANDOFF | 根据用户意图给出唯一下一入口 | handoff 唯一且可执行 | S-SDES-TRIPLE | 下游入口仍模糊 |

## 域路由矩阵

| 域 | kind | 默认调度 | 触发条件 | 主职责 |
| --- | --- | --- | --- | --- |
| `角色` | `unordered` | 可并行分析，正式落盘按主体分别写入 | 需要稳定角色外形、气质、服饰与连续性 | 角色设计卡与 `character_design.json` |
| `场景` | `unordered` | 可并行分析，正式落盘按主体分别写入 | 需要稳定空间、氛围、功能与镜头适配 | 场景设计卡与 `scene_design.json` |
| `道具` | `unordered` | 可并行分析，正式落盘按主体分别写入 | 需要稳定外观、材质、用途与叙事负荷 | 道具设计卡与 `prop_design.json` |

## 路由与回退卡

- 判定顺序：`bridge 完整度 -> 域判定 -> 三件套交付 -> 下游 handoff`
- 冲突解消规则：`1-清单` bridge 与新设计冲突时，必须先解释覆盖理由
- unknown 默认路由：回到 `1-清单` 核查输入，不直接继续创作
- 失败重试上限：2
- 停止条件：关键主体仍无稳定 bridge 支撑
