# 路由判型与回退策略

| 场景信号 | 选中范围 | 必跑节点/能力链 | 额外限制 | 默认回退 |
| --- | --- | --- | --- | --- |
| 根文件不存在 | 整集 | `scope_bootstrap -> shot_skeleton -> core 并行 -> finish 并行 -> review/audit` | 必须先 bootstrap；`document_phase` 至少进入 `detail_in_progress` | 任何关键输入缺失时直接 `report`，不创建伪根文件 |
| 只修某个 `组ID` | 命中组 | `scope_bootstrap`、命中组 skeleton、相关字段链、review/audit | 不补空其他组；未命中组保持原样 | 若组边界不清，回到 `shot_skeleton_engine` |
| 只修某个 `分镜ID` | 命中镜 | `scope_bootstrap`、目标镜 skeleton 校验、相关字段链、review/audit | 不改同组其他镜的镜序与时间段 | 若目标镜不存在或编号漂移，回到 skeleton |
| 用户要求重做拆镜 | 命中组或整集 | `shot_skeleton_engine` 强制整段重跑 | 其他链必须等待新 skeleton 稳定 | 若 preset 锁轴冲突，返回 `report` |
| 重点是心理波动 / 潜台词 | 命中镜 | `performance_engine: 内心模式` | 不得越权写成动作或关系总论 | 动机不清时保守化并请求上游证据 |
| 重点是追逐 / 打斗 / 肢体推进 | 命中镜 | `performance_engine: 动作模式` | 站位调整必须服从既有空间锚点 | 空间不清先回 `structural_staging_engine` |
| 重点是对峙 / 对话张力 / 多人互动 | 命中镜 | `performance_engine: 对手戏模式` | 先锁关系轴，再补表演细节 | 主次不清先回构图重点 |
| 需要默认可用的运镜 | 命中镜 | `camera_movement_engine: 叙事派` | 默认路线，必须解释“为什么要动 / 不动” | 理由不足时回退到静止或最小必要运动 |
| 同一表现目标下需要评估更强镜头表达 | 命中镜 | `camera_movement_engine: 叙事派 + 同目标变体比较` | 先锁默认路线，再比较 2-3 个不偷换目标的更强变体 | 变体一旦改写主任务、空间轴线或表演逻辑，立即回退默认路线 |
| 用户显式要求挑战方案 | 命中镜 | `camera_movement_engine: 叙事派 + 炫技派` | `炫技派` 只能做对照，不默认覆盖 | 挑战收益说不清则回退默认路线 |
| 需要形成 final look | 命中镜 | `cinematography_engine` 全链 | 先 light/color，再摄影总协调 | 子补丁冲突时优先保守合成 |
| 只需要补氛围 | 命中镜 | `atmosphere_engine` + 必要 review | 不借机扩写摄影参数 | 只能写抽象情绪词时返回 `report` |
| 需要跨镜衔接 | 命中镜或相邻镜 | `transition_fx_engine` | 先判断直切是否更强 | 依据不足时只保留 `transition_note` |
| `respect_storyboard_presets` / `preserve_only` | 命中切片 | `scope_bootstrap` 强制锁 preset | 禁止重排镜序、改主要锁轴 | 冲突时以 preset 为准并返回 `report` |
| 多字段合成 / 精修模式 | 命中切片 | `continuity_review + source_audit` 必跑 | 任何 veto 都必须阻止写回 | 回到对应 `Rework Entry` |

## 默认路由原则

1. `shot_skeleton_engine` 是并发链的唯一前置门。
2. `structural_staging`、`performance`、`atmosphere` 是 core draft 的默认三链。
3. `camera_movement`、`cinematography`、`transition_fx` 是 finish draft 的默认三链，但其中 `transition_fx` 为条件进入。
4. `review -> audit -> writeback` 永远固定串行，不允许跳过。

## 保守回退原则

1. 证据不足时，优先缩范围，而不是补想象。
2. 多方案并存但证据不够时，优先选择更节制、更稳定、更容易被下游消费的方案。
3. 任何会影响镜序、锁轴、主叙事任务的判断，一律不得静默假设。
4. 发现上游 `2-Global` 与当前 draft 冲突时，先服从上游真源，再通过 `report` 留下返工入口。
