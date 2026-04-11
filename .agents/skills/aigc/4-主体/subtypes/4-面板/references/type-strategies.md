# 4-面板 VSM 与域路由策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SPNL-01 | 域 | 当前命中角色、场景还是道具面板 | `character / scene / prop / mixed` | 读取面板任务与上游主体域 | P0 |
| V-SPNL-02 | 真源 | `2-设计` 或审计通过版本是否稳定 | `ready / audit_required / unstable` | 检查设计版本与审计状态 | P0 |
| V-SPNL-03 | 交付 | 主文件与 layout 是否齐备 | `full / layout_only / doc_only` | 对照交付件清单 | P1 |
| V-SPNL-04 | 下游 | 更偏向 `5-画面` 还是 `6-视频` 的参照使用 | `storyboard / video / mixed` | 结合用户目标与下游入口 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SPNL-01 | `V-SPNL-02=audit_required` | 0.95 | 无 | 无 |
| C-SPNL-02 | `V-SPNL-02=unstable` | 1.0 | 无 | 无 |
| C-SPNL-03 | `V-SPNL-03 in {layout_only, doc_only}` | 0.90 | 无 | 可并发 `C-SPNL-04` |
| C-SPNL-04 | `V-SPNL-04=mixed` | 0.85 | 无 | 可并发 `C-SPNL-03` |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SPNL-01 | S-SPNL-AUDIT-FIRST | 先关闭审计关键失败项，再面板化 | 不放大缺陷版本 | S-SPNL-HOLD | 仍有关键项未关 |
| C-SPNL-02 | S-SPNL-DESIGN-FIRST | 回到 `2-设计` 收束真源 | 面板不越权二次设计 | S-SPNL-AUDIT-FIRST | 设计仍漂移 |
| C-SPNL-03 | S-SPNL-DOUBLE | 补齐主文件与 layout 双产物 | 下游既能人读也能机读 | S-SPNL-DESIGN-FIRST | 双产物仍不齐 |
| C-SPNL-04 | S-SPNL-HANDOFF | 针对分镜/视频写清参照入口 | handoff 唯一明确 | S-SPNL-DOUBLE | 下游目标仍模糊 |

## 域路由矩阵

| 域 | kind | 默认调度 | 触发条件 | 主职责 |
| --- | --- | --- | --- | --- |
| `角色面板` | `unordered` | 可并行布局 | 需要角色参照板、展示板或后续统一角色面 | 角色面板主文件 + layout |
| `场景面板` | `unordered` | 可并行布局 | 需要场景参照板、空间板或场景统一展示面 | 场景面板主文件 + layout |
| `道具面板` | `unordered` | 可并行布局 | 需要道具参照板、材质板或道具统一展示面 | 道具面板主文件 + layout |

## 路由与回退卡

- 判定顺序：`真源稳定度 -> 域判定 -> 双产物交付 -> 下游参照目标`
- 冲突解消规则：审计未关闭关键项时，审计优先于面板美化
- unknown 默认路由：停止面板化，回到最近稳定的设计版本
- 失败重试上限：2
- 停止条件：设计真源仍未稳定或审计关键项未关闭
