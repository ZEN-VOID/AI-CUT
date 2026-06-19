# Type Map

## Package Index

| package_id | path | selection signal | relation | loaded_for |
| --- | --- | --- | --- | --- |
| `scope.problem-discovery` | `types/scope/problem-discovery.md` | 模糊读感症状、宽泛质量反馈、未定位 finding、用户要求先找问题 | stackable | problem discovery |
| `scope.locality` | `types/scope/locality.md` | 用户指定某章、某段、某线索或某对象 | stackable | impact map |
| `scope.clue-thread` | `types/scope/clue-thread.md` | 线索、伏笔、证据、误导、payoff、悬念链 | stackable | typed impact matrix |
| `scope.character-state` | `types/scope/character-state.md` | 角色动机、关系、状态、声纹、阵营或人物弧 | stackable | typed impact matrix |
| `scope.mechanism` | `types/scope/mechanism.md` | 物品、技能、规则机制、能力限制、道具用法 | stackable | typed impact matrix |
| `scope.chapter-event` | `types/scope/chapter-event.md` | 章节事件、情节事实、场景动作、章末钩子 | stackable | typed impact matrix |
| `scope.timeline-place` | `types/scope/timeline-place.md` | 时间线、年代、历史边界、地点、路线、空间动线 | stackable | typed impact matrix |
| `scope.tone-contract` | `types/scope/tone-contract.md` | 题材、价值口径、风格、语体、表达分布 | stackable | typed impact matrix |
| `scope.structure-topology` | `types/scope/structure-topology.md` | 卷章结构、章节数、任务分配、validated actual 回流拓扑 | stackable | typed impact matrix |
| `scope.accepted-truth` | `types/scope/accepted-truth.md` | 已 PASS 终稿、return actualization、accepted manuscript refs | stackable | typed impact matrix |
| `operation.plan-only` | `types/operation/plan-only.md` | 只要判断范围、计划或报告，不授权写回 | mutually-exclusive operation | repair plan |
| `operation.execute` | `types/operation/execute.md` | 用户明确要求执行修改、修复、同步改 | mutually-exclusive operation | writeback |
| `acceptance.review-gate` | `types/acceptance/review-gate.md` | 需要验收、审计、code-reviewer 或 review | stackable | final gate |

## Default Package Rule

- 默认加载 `scope.locality` 和 `acceptance.review-gate`。
- 当用户只给出“不好看 / 不对 / 读不清 / AI 味 / 人物怪 / 伏笔断 / 没钩子”等模糊症状，或 finding 未定位到对象和层级时，必须先加载 `scope.problem-discovery`。
- 若用户修改对象命中 `Universal Type Matrix` 任一行，必须加载对应 `scope.*` 类型包；多对象修改可以多选叠加。
- 若用户未授权写回，选择 `operation.plan-only`。
- 若用户明确要求“执行 / 改掉 / 同步修 / 写回”，选择 `operation.execute`。
- operation 包互斥；scope 与 acceptance 包可叠加。

## Loading Flow

1. 读取用户请求和项目根。
2. 若输入是模糊症状或未定位 finding，先加载 `scope.problem-discovery`，形成 `problem_discovery_packet`。
3. 选择 scope 包定位影响对象；先加载 `scope.locality`，再按对象类型加载 1 个或多个 typed scope 包。
4. 选择 operation 包决定是否写回。
5. 选择 acceptance 包确定验收深度。
6. 将命中包作为固定上下文交给 `SKILL.md` 的 `Thinking-Action Node Map`。
