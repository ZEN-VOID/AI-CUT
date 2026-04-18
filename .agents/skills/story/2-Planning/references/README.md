# Planning References

`references/` 现在只承担一件事：为单一 skill [`2-Planning/SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/SKILL.md) 提供按需加载的 planning module 细则。

它们不是子技能，不单独拥有路由权，不单独拥有 skill id。
每个被治理模块固定采用：

```text
references/<module-name>/
  module-spec.md
  CONTEXT.md
```

## 加载规则

1. 先由主 `SKILL.md` 判定当前处于哪个 planning step。
2. 再按 step 加载对应 `references/<module>/module-spec.md`。
3. 若当前模块存在局部异常、返工信号或历史兼容风险，再按需读取同目录 `CONTEXT.md`。
4. 再读取根级对应模板。
5. 再把结果正式落盘到 `Planning/*.json` 并列文件。
6. 只有第 8 步可以把前 1-7 收束为唯一真源 `Planning/8-全息地图.json`。

## 模块索引

| 模块 | 类型 | 何时加载 | 解决问题 | 模板 | 正式输出 |
| --- | --- | --- | --- | --- | --- |
| [`genre-selection/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/genre-selection/module-spec.md) | `mode-playbook` | Step 1 或题材漂移返工 | 题材走廊、平台承诺、禁飞区 | [`../templates/genre-selection.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/genre-selection.json) | `Planning/1-题材选型.json` |
| [`chapter-planning/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/chapter-planning/module-spec.md) | `mode-playbook` | Step 2 或章节挂载返工 | 章节容器、节奏窗口、密度合同 | [`../templates/chapter-planning.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/chapter-planning.json) | `Planning/2-章节规划.json` |
| [`story-outline/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/story-outline/module-spec.md) | `mode-playbook` | Step 3 或主干失焦返工 | 叙事脊柱、卷级推进、关键转折 | [`../templates/story-outline.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/story-outline.json) | `Planning/3-故事大纲.json` |
| [`conflict-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/conflict-design/module-spec.md) | `mode-playbook` | Step 4 或对抗失真返工 | 冲突系统、升级链、解决窗口 | [`../templates/conflict-design.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/conflict-design.json) | `Planning/4-冲突设计.json` |
| [`mission-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/mission-design/module-spec.md) | `mode-playbook` | Step 5 或目标链返工 | 任务系统、门槛、奖励代价 | [`../templates/mission-design.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/mission-design.json) | `Planning/5-任务设计.json` |
| [`clue-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/clue-design/module-spec.md) | `mode-playbook` | Step 6 或证据链返工 | 发现路径、误导结构、揭晓窗口 | [`../templates/clue-design.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/clue-design.json) | `Planning/6-线索设计.json` |
| [`foreshadow-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/foreshadow-design/module-spec.md) | `mode-playbook` | Step 7 或回照系统返工 | 铺设、加深、静默、兑现窗口 | [`../templates/foreshadow-design.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/foreshadow-design.json) | `Planning/7-伏笔设计.json` |
| [`holomap/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/holomap/module-spec.md) | `mode-playbook` | Step 8 或真源收束返工 | 三轴组织、章节编组、跨线程索引、actualization 兼容 | [`../templates/holomap.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/templates/holomap.json) | `Planning/8-全息地图.json` |

## 统一原则

- 共同长期约束来自 `Init/north_star_contract.json` 与 `Cards/**`。
- 题材工法来自共享 `templates/genres/` 根目录；`references/` 只保留 step module 细则。
- 每个模块的局部经验单独写入同目录 `CONTEXT.md`；跨模块经验仍回写到 `2-Planning/CONTEXT.md`。
- 共同输出路径来自 `Planning/*.json` 并列文件合同。
- `1-7` 是 evidence layer，`8` 是 canonical truth。
- 任何 module 返工都必须服从“最早失稳模块优先”。

## Think-Think 可视化工作台

### 三轴

| 轴角色 | 本轮轴名 | 关键判断字段 | 结论 |
| --- | --- | --- | --- |
| `方向轴` | `消费路径对齐` | `planning_step`、`primary_consumers`、`template`、`formal_output`、`handoff_contract` | 8 个 planning references 都应一一对应到单步消费链路，不能再以“资料文档”方式散挂 |
| `成立轴` | `分层与耦合成立` | `module_type`、`load_contract`、`shared_dependency`、`template_dependency`、`local_context_scope` | 模块合同应留在 `module-spec.md`，局部故障与返工启发式下沉到同目录 `CONTEXT.md`，不再混在单文档里 |
| `优选轴` | `检索复用收益比` | `module_name` 一致性、目录粒度、`source_route` 稳定性、入口压缩比 | `references/<module>/module-spec.md + CONTEXT.md` 是当前最稳的目录方案，既可检索，也便于路径同步和复用 |

### 三重

| 裁决层 | 本层关键字段 | 本层动作 | 本层结论 |
| --- | --- | --- | --- |
| `粗裁决 / Base Range` | `reference_type`、`planning_step`、`service_object`、`output_slot` | 先把 8 份 reference 判定为 Step 型 `mode-playbook`，并补齐消费对象与输出槽 | 不保留“单文档直接治理”，全部升格为独立子模块 |
| `细裁决 / Range Narrowing` | `boundary_owner`、`local_vs_global_context`、`template_split`、`path_sync_scope` | 区分模块合同、局部经验、模板骨架与路径同步责任 | 专业内容保留，承载层重建；模板继续放 `templates/`，局部经验放模块 `CONTEXT.md` |
| `离散裁决 / Final Selection` | `directory_shape`、`entry_order`、`source_route`、`naming_consistency` | 选定最终目录结构、导航顺序与模板元数据路径 | 主入口固定为 `README -> module-spec -> 模块 CONTEXT -> template`，模板 `source_route` 全部切到新入口 |
