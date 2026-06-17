# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 4630
current_lines: 59
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-10T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 根目录缺少总 `SKILL.md` / `CONTEXT.md`，导致执行者只能看到分阶段 skill | root source contract | 在 `.agents/skills/story/` 补齐根级入口与根级经验层 | 把跨阶段拓扑、总路由、共享 carrier 边界固定在根级真源，不再散落到各阶段自己解释 | 泛化 `story2026` 请求能先命中根入口，再转到唯一阶段 |
| 跨阶段共享 reference 被误下沉到某一阶段，后续产生第二真源 | canonical source governance | 回到根级 `_shared/` 与对应阶段 `_shared/` 重新确认共享归属 | 跨阶段共享合同只放根级 `_shared/`，阶段共享合同只放 owning stage `_shared/` | 同一份 schema/contract 不再被多个阶段各自改写 |
| 用户问题同时触发多个阶段，执行者直接跳到“看起来最像”的下游阶段 | routing contract | 先判 truth role，再按总路由表选择最早 owner | 在根级 `SKILL.md` 固化 route matrix 与 owner 表 | 问题能稳定落到唯一默认入口 |
| story 阶段链已把 `projects/story/<项目名>/` 当真实项目根，但根合同、脚本或默认示例仍把 `projects/aigc/<项目名>/` 当 canonical | runtime namespace drift | 先把根级 `SKILL.md`、shared contract、registry、locator/init 脚本统一改回 `projects/story/<项目名>/`，仅把旧路径保留为 legacy fallback | 固定“`projects/story/<项目名>/` 是小说项目 canonical runtime，`projects/aigc/<项目名>/` 只作兼容回读”到根 skill、脚本候选根、帮助文案与测试 | 新项目初始化、根技能路由与 project locator 默认都会先落到 `projects/story/<项目名>/` |
| 题材方向盘停留在 planning 阶段临时 artifact，或被误拆成 `1-设定/类型卡` | north-star boundary drift | 把题材锁定统一收回 `0-初始化/north_star.yaml.genre_contract`，planning 只导入 | 固定“north_star 持有 promise/corridor，planning 只消费不拥有” | `north_star.yaml.genre_contract` 成为题材方向盘真源 |
| 系统把题材规则写成隐式自动机制，反过来压制人工创作判断 | creativity-governance drift | 删除旧的自动题材装配链，统一改读人工 `north_star.yaml.genre_contract` | 固定“题材判断属于人工创作层，系统只负责承接与投影” | planning/drafting/built-in acceptance 不再存在自动题材依赖 |
| planning 仍停留在旧 `全息地图 + 卷分片` 惯性，没有切到 `部级 / 卷级 / 章级` 三层规划 | planning architecture drift | 回到 `2-卷章` 父技能，按三层分形结构重写 | 在根级真源与 workflow 文案同步固定三层规划 | `2-卷章` 的 primary truth 已切换到三层 Markdown |
| 终验仍被当成独立 `story/review` 阶段，导致任务执行完还要另跑验收 | standalone review drift | 把验收收回 `3-初稿` 与 `4-润色` 的自动节点，并写出 `第N章.acceptance.json` | 固定“阶段产物和阶段验收包同轮生成，PASS/handoff 由 owning stage 裁决” | 出现 PASS/FAIL 问题时，定位到 owning stage 的 `stage_acceptance_packet` |
| 普通 skill 或子技能直接调用后只落业务产物，`STATE.json` 没有阶段完成记录 | direct skill state gap | 完成时调用 `workflow_manager.py record-skill-completion` 写入 `workflow_runtime.execution_state.stage_progress` | 在根级和 1-4 阶段完成合同固定普通 skill completion hook | 普通父技能/子技能执行后，`stage_progress`、`history`、`task_log` 都能看到对应 run |
| 初稿、润色和调度继续走历史子目录，导致路由断链和规则重复 | stage-root topology drift | 回到 `3-初稿` / `4-润色` 根技能包 | 在根 `SKILL.md` 固定正文阶段根技能包，禁止历史子目录成为入口、返工归属或 frontmatter 真源 | 普通章节生产进入 `3-初稿`，普通润色进入 `4-润色` |
| 用户要求改某个局部，执行者直接进入当前章或对象卡点对点修改 | story repair scope collapse | 进入 `repair` 卫星技能，先产出 impact map，再按 source-first 顺序写回 | 根级路由把跨设定/规划/正文/阶段验收包/return 的局部修改统一交给 `.agents/skills/story/repair` | 修复报告包含 upstream、同层前列、当前局部、downstream、future constraints、acceptance/return/state |
| 类型化场面强化被误解成武侠专用能力，或被新增为 `3.5/5-强化` 独立主阶段 | genre-scene owner drift | 回到 `_shared/genre-scene-strengthening-contract.md`，按项目题材轴和场景功能轴双轴路由 | 根 `SKILL.md` 固定首写归 `3-初稿`、源章修复归 `4-润色`、跨阶段影响归 `repair`，禁止第三正文真源 | `genre_scene_route.owner_stage` 指向 `3-初稿/4-润色/repair`，无新增 numbered stage |

## Repair Playbook

1. 先判断问题是“缺总入口”“路由错”“真源错认”“共享 carrier 误放置”中的哪一种。
2. 若问题涉及 runtime 根路径，先核对当前 canonical 是否仍是 `projects/story/<项目名>/`，再判断旧 `projects/aigc/<项目名>/` 是否只是 legacy 遗留。
3. 若问题跨两个以上阶段，先回根级 `story/SKILL.md` 做总线诊断，再进入阶段修复。
4. 若同一规则在多个阶段重复出现，优先找根级 canonical source，而不是逐个阶段补丁。
5. 若问题涉及题材方向盘，先检查 `0-初始化/north_star.yaml.genre_contract` 是否已经存在并被 `2-卷章` 正式导入。
5A. 若问题涉及武戏、文戏、言情拉扯、玄幻能力兑现、恐怖悬疑、现实压力等类型化场面强化，先建立 `project_genre_axis + scene_function_axis`，再判断 owner：未写/重写进入 `3-初稿`，已有源章最小修补进入 `4-润色`，跨阶段影响进入 `repair`。
6. 若问题涉及验收或回写，先确认 owning stage 是否已有 `第N章.acceptance.json`，以及 `return` 是否已有 actualization artifact；不要先看口头说明或旧 child sidecar。
7. 若问题涉及“完成了但状态没变”，先检查是否走了 `record-skill-completion`；普通 skill / 子技能不应依赖完整 workflow task 才能写入状态。
8. 若问题涉及 AI 检测、人工成分下降或润色后变规整，先判断是否发生整章重写式润色；默认回到 `4-润色` 的最小局部修补边界，而不是继续加大“去 AI 味”提示。
9. 若问题是“改一个局部但可能牵动整体”，先路由到 `repair` 卫星技能产出影响图；不要由当前看起来最近的阶段直接点对点修改。

## Reusable Heuristics

- 根级 skill 最有价值的工作不是“替阶段再说一遍”，而是回答“该去哪一层、该信哪一层、哪些共享层先读”。
- 先看项目是否还被错误绑定到 `projects/aigc/<项目名>/`；对当前仓库，小说项目的 canonical runtime 已回收到 `projects/story/<项目名>/`。
- 题材判断默认属于人工创作层，系统只能承接 `north_star.yaml.genre_contract`，不应替作者自动激活题材机制。
- 最稳的题材方案不是给每个题材重写一套 workflow，而是维持固定方法核，把题材判断集中在 `north_star.yaml.genre_contract`，再由 downstream 显式消费。
- 类型化场面强化的稳定抽象是“题材轴 + 场景功能轴”，不是“武侠动作强化”；武侠打斗、言情拉扯、玄幻能力兑现、恐怖遮蔽、悬疑线索和现实制度压力都应共享同一 owner-safe 路由。
- 不要新增默认 `3.5-类型强化`；这会制造第三正文真源。首写的类型化判断留在 `3-初稿`，已有源章的 affected-span patch 留在 `4-润色`。
- 新规划层的 primary truth 应先看 `1-部级 -> 2-卷级 -> 3-章级` 对应的 `整体规划.md / 第N卷/卷规划.md / 第N卷/第N章.md`；`全息地图.json` 只保留兼容消费价值，不再是创作主真源。
- `return` 真正能消费的不是口头 PASS 或旧 child 维度报告，而是 owning stage 的 `stage_acceptance_packet` 里的 `acceptance_status / accepted_manuscript_stage / handoff_targets / accepted_manuscript_refs` 组合。
- workflow CLI 和普通 skill completion 是两条入口，但状态落点必须统一到项目 `STATE.json#workflow_runtime.execution_state.stage_progress`。
- `3-初稿` 和 `4-润色` 的根技能包持有业务合同；阶段内模块只服务根技能，不再拆平行入口。
- AI 检测友好的润色通常不是“更顺”，而是少动：保留初稿的句群骨架、长短不齐、局部粗粝和人工式不均匀，只修坏处。
- 局部 repair 的起点是影响图，不是文件 patch；需要先问旧口径在哪些源层和消费者里存在，再决定改哪里。
