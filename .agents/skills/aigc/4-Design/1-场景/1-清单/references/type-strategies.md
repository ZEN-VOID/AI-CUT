# 场景清单 VSM 策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SCENE-LIST-01 | 输入 | shared schema 壳是否完整 | `ready/incomplete` | 检查 `final_output.main_content.分镜组列表[]` | P0 |
| V-SCENE-LIST-02 | 镜级抽取 | `场景及方位` 是否可直接使用 | `ready/empty/noisy` | 检查是否为空、是否仅剩噪声词 | P1 |
| V-SCENE-LIST-03 | 拆分稳定性 | `scene_name + scene_variant` 是否可保守拆开 | `split/keep_raw/unknown` | earliest-marker 规则后再检查主场景是否为空 | P1 |
| V-SCENE-LIST-04 | 输出要求 | 本轮是否需要 manifest | `json_only/full_trace` | 结合用户目标与脚本参数 | P2 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SCENE-LIST-01 | `V-SCENE-LIST-01=incomplete` | 1.0 | 互斥全部生成路由 | 无 |
| C-SCENE-LIST-02 | `V-SCENE-LIST-02=ready AND V-SCENE-LIST-03=split` | 0.95 | 互斥 C-SCENE-LIST-03 | 可并发 C-SCENE-LIST-04 |
| C-SCENE-LIST-03 | `V-SCENE-LIST-03=keep_raw OR V-SCENE-LIST-03=unknown` | 0.90 | 互斥 C-SCENE-LIST-02 | 可并发 C-SCENE-LIST-04 |
| C-SCENE-LIST-04 | `V-SCENE-LIST-04=full_trace` | 0.90 | 无 | 可并发 C-SCENE-LIST-02/C-SCENE-LIST-03 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SCENE-LIST-01 | S-SCENE-LIST-BACKTRACK | 停止并报告上游 schema 缺口 | 不伪造 `分镜组列表` 或 `分镜明细` | S-SCENE-LIST-PAUSE | 上游缺口持续存在 |
| C-SCENE-LIST-02 | S-SCENE-LIST-MAINLINE | 正常拆分并聚合 `scene_name + scene_variant` | 主场景可稳定聚合，相同场景不重复裂变 | S-SCENE-LIST-KEEP-RAW | 同名场景出现异常分叉 |
| C-SCENE-LIST-03 | S-SCENE-LIST-KEEP-RAW | 保守保留原句或回退 `unknown` | 不虚构场景研究信息 | S-SCENE-LIST-PAUSE | 原句已无法支撑下游继续消费 |
| C-SCENE-LIST-04 | S-SCENE-LIST-FULL-TRACE | 输出 `第N集.json + _manifest.json` | 两文件必须可互相追溯 | S-SCENE-LIST-MAINLINE | 本轮只要求 `json_only` |

## 路由与回退卡

- 默认判定顺序：`输入壳 -> 场景串可用性 -> scene_name 拆分稳定性 -> 输出模式`
- unknown 默认路由：仍按 `json_only` 执行，但要把 `scene_name` 标记为 `unknown`
- 停止条件：无法从上游根文件确认 `分镜组列表[]`，或 `分镜明细[]` 全部缺失 `场景及方位`
