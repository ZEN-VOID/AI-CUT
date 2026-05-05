# Good/Bad Learning Workflow

本文件是 `好好坏坏` 的思行网络真源。节点同时表达判断、动作、证据、路由和 gate。

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-LOCK-CONTRAST-TASK` | 锁定可比较任务面 | `target_skill_ref`、好/坏示例、任务环节 | 确认示例同属一个输出面，列出缺口和允许修改范围 | intake summary | `N2` | 目标 skill 与好/坏示例均可定位 |
| `N2-LOAD-TARGET-SOURCE` | 读取目标源层配置 | 目标 skill 根目录 | 加载 `SKILL.md + CONTEXT.md`，按环节读取分区、shared、registry/routes | source file list | `N3` | 不跳过目标 `CONTEXT.md` |
| `N3-LOAD-REQUIREMENTS-AND-MATERIALS` | 读取任务要求与资料来源 | task requirements、source materials、current outputs | 区分事实、偏好、格式、阶段合同和证据边界 | evidence package | `N4` | 事实判断有来源，缺来源则记录风险 |
| `N4-TYPE-CONTRAST` | 选择对比类型包 | evidence package、`types/type-map.md` | 形成 `contrast_type`，加载对应类型包 | type profile | `N5` | 类型包命中理由清楚 |
| `N5-COMPARE-GOOD-AND-BAD` | 生成诊断矩阵 | 好/坏示例、要求、资料 | 逐项提炼 `good_signals`、`bad_signals` 和直接原因 | diagnosis matrix | `N6` | 每个坏信号绑定依据或风险 |
| `N6-TRACE-TO-SOURCE-OWNER` | 裁决最窄源层 owner | diagnosis matrix、目标配置 | 生成 `source_patch_plan`、`sync_scope`、`parity_targets` | patch plan | `N7` 或阻断 | 不形成平行真源 |
| `N7-PATCH-SOURCE-LAYER` | 执行源层调优 | patch plan、允许修改范围 | 修改目标 owner，并同步必要 registry/routes、模板、review 或 shared carrier | file diff | `N8` | 脚本不替代 LLM 判断 |
| `N8-VALIDATE-AND-LEARN` | 验证与学习沉淀 | file diff、诊断矩阵 | 运行结构/引用/语义检查，写入目标或本技能经验层 | validation summary | done 或 `N6` | 好信号可保留，坏路径被阻断 |

## Failure Loops

- `N1` 缺少好/坏任一侧示例：阻断并请求最小补充。
- `N3` 缺少资料来源但需要事实判断：降级为相对风格/结构诊断，并把事实判断列入 `residual_risks[]`。
- `N6` 找不到单一 owner：先输出候选 owner 和风险，不做多处强行改写。
- `N8` 验证失败：回到 `N6` 重新裁决源层 owner，而不是继续堆规则。

## Merge Rules

- 多个坏信号可并行分析，但必须汇流成一个 `source_patch_plan`。
- 同一条规则只能有一个 canonical owner；同步文件只承接发现、路由、模板或 parity，不重写主规则。
- 若修改了目标 `SKILL.md` 的入口、路由或输出合同，必须同步检查目标 README、templates、registry/routes 和相关父级合同。
- 若修改了目标 `types/` 或 `steps/`，必须在 review gate 中回放好/坏样例验证路线是否正确。
