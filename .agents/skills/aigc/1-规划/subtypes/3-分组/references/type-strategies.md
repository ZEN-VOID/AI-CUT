# 3-分组 · 统一多维量化裁决

## 模块定位

- 本文件是 `3-分组` 的统一裁决真源，不再在 `G1/G2/G3` 多路由之间做主裁决。
- 当前阶段统一按“约束抽取 -> 候选边界 -> 多维量化 -> 聚合落盘”的单一方法执行。
- `references/scene-duration-projection.md` 继续作为全流程共享的量化硬门槛真源。

## 核心立场

`3-分组` 不再回答“这次属于预设驱动、结构驱动还是负载驱动”，而是统一回答：

1. 哪些边界受上游 hard constraint 约束，不能碰
2. 哪些边界有结构锚点支撑，值得优先保留
3. 哪些边界能形成更清晰的依赖闭环与下游 handoff
4. 哪些边界在时长、字窗和有效字数上成立
5. 在以上约束同时成立的前提下，最终采用哪一组分组边界

## 统一裁决维度

| dimension_id | 维度 | 要回答的问题 | 典型证据 |
| --- | --- | --- | --- |
| `D1-CONSTRAINT` | 上游约束维 | 哪些边界被 `preset_registry`、用户硬要求、`locked_preset_axes` 或集边界锁死 | `story-source-manifest.yaml`、用户要求、`1-分集` 结果 |
| `D2-STRUCTURE` | 结构成立维 | 当前候选边界是否依附章节、场次、任务链、冲突闭环或叙事峰值 | 场景链、事件链、连续时空单元 |
| `D3-DEPENDENCY` | 依赖闭环维 | 切开后各组是否仍有清晰的前后依赖、串并行关系与 handoff | 因果链、信息揭示顺序、执行顺序 |
| `D4-QUANT` | 量化成立维 | 候选组是否满足时长策略、字窗公式、有效字数回算与尾组规则 | `scene-duration-projection.md`、主源回算 |
| `D5-HANDOFF` | 下游消费维 | 当前组容器是否足够让 `2-组间 / 3-明细 / 4-主体` 继续消费，而不是二次猜边界 | 组目标、结构锚点、交接约束、下游入口 |

## 决策顺序

1. 先锁 `D1-CONSTRAINT`：
   - 集边界不能越过
   - `hard_lock` 锚点不能切断
   - 用户显式“必须同组 / 必须拆开”的约束优先
2. 再列 `D2-STRUCTURE` 候选：
   - 连续时空单元
   - 冲突闭环
   - 峰值与尾钩
   - 明确任务包
3. 再做 `D3-DEPENDENCY` 收窄：
   - 若切开后依赖更清晰，保留
   - 若切开后形成无效孤组、假并行或重复 handoff，淘汰
4. 再用 `D4-QUANT` 校验：
   - 时长策略
   - 字窗与硬上限
   - 主源回算 `effective_text_chars`
   - 尾组 `< 5 秒` 规则
5. 最后用 `D5-HANDOFF` 做终裁：
   - 哪组写回后最利于下游直接消费
   - 哪组能减少后续重新猜边界

## 上游锚点的正确角色

若上游 `story-source-manifest.yaml` 或 `metadata.source_profile` 中存在 `preset_registry`：

1. 它是 `D1-CONSTRAINT` 的证据，不是“最终组数真相”。
2. `projected_group_ids` 只能视为投影建议或追踪索引，不能跳过当前阶段的多维裁决直接等同正式分组结果。
3. `hard_lock` / `soft_lock` / `reference_only` 决定的是“能不能切、怎么切”，不是“必须一锚一组”。

### lock_level 解释

| lock_level | 默认动作 | 允许动作 | 禁止动作 |
| --- | --- | --- | --- |
| `hard_lock` | 不得改写锚点内部顺序与 owned axes | 默认整锚点保留；若用户显式要求或结构 handoff 更清晰，可在同一锚点 span 内做连续切分，但切分后的所有子组都必须继续继承该锚点并保持原顺序 | 切断锚点内部核心链、改写顺序、做非连续切分 |
| `soft_lock` | 保持顺序与主意图 | 允许在同一锚点 span 内做连续细分 | 拆成离散跳段、倒序、跨场景乱切 |
| `reference_only` | 仅作辅助证据 | 可参考，不构成硬边界 | 不能被误读成强制组界 |

### projected_shot_mode 解释

| projected_shot_mode | 正确理解 |
| --- | --- |
| `single_anchor_single_shot` | 倾向整段保留 |
| `single_anchor_multi_shot` | 下游允许一锚多镜展开，但本阶段不必强行一锚一组 |
| `multi_anchor_fixed` | 内部存在多个固定预设，分组时应先保整体连续 |
| `reference_only` | 只提供边界与意图参考 |

## 量化继承

所有正式落盘结果都必须继承：

- `references/scene-duration-projection.md`

硬规则：

1. `group_load_score` 只是摘要指标，不能单独决定边界。
2. `effective_text_chars` 在 `storyboard_script / hybrid_story_text` 下必须优先由主源回算。
3. `window_status != ok` 的候选不能直接落盘正式 `第N集.md`。
4. 若锚点保护与量化 gate 冲突，必须判为返工或等待豁免，不能靠“先保锚点再解释偏差”直接通过。

## 统一裁决输出

执行后，至少要显式产出：

1. `边界裁决摘要`
   - 不可动约束
   - 候选边界
   - 最终选中的边界集合
   - 排除理由
2. `分组计划表`
   - 每组范围
   - 结构锚点
   - `preset_anchor_policy / preset_anchor_ids`
   - 量化字段
   - 依赖与并行性
3. `组级容器`
   - 组目标
   - 交接约束
   - 下游建议

## Unknown / 失败处理

| 情况 | 默认动作 |
| --- | --- |
| 锚点语义不清，只给出 `projected_group_ids` 但无 lock 解释 | 先回到 `D1-CONSTRAINT` 补清约束，不直接按投影成组 |
| 结构候选很多，但都无法形成清晰 handoff | 回到 `D3-DEPENDENCY` 收窄，必要时减少组数 |
| 量化通过但结构不成立 | 不落盘；说明这是“量化可行但叙事不可交接”的伪候选 |
| 结构成立但量化失败 | 回到边界层重分；不得以 `warn-*` 直接落盘 |
| 上游约束与量化硬门槛冲突 | 标记返工或等待显式豁免 |

## 使用提示

1. 先抽取 `D1-CONSTRAINT`，再看结构，不要先看 `projected_group_ids` 就直接决定组数。
2. 先问“哪里不能切”，再问“哪里最该切”。
3. 当相邻两个切点都可行时，优先选择下游 handoff 更清晰、依赖更少返工的一组。
4. 若问题是“为什么不是五组 / 为什么不是三组”，回到本文件的五维裁决，而不是回到旧 `G1/G2/G3` 思路。
