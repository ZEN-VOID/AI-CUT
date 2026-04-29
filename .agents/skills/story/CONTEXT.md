# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 6200
current_lines: 52
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-22T00:00:00Z
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
| 系统把题材规则写成隐式自动机制，反过来压制人工创作判断 | creativity-governance drift | 删除旧的自动题材装配链，统一改读人工 `类型卡` | 固定“题材判断属于人工创作层，系统只负责承接与投影” | planning/drafting/validation 不再存在自动题材依赖 |
| planning 仍停留在旧 `全息地图 + 卷分片` 惯性，没有切到 `部级 / 卷级 / 章级` 三层规划 | planning architecture drift | 回到 `2-卷章` 父技能，按三层分形结构重写 | 在根级真源与 workflow 文案同步固定三层规划 | `2-卷章` 的 primary truth 已切换到三层 Markdown |
| 终验已经产出 child sidecar，但根层仍把 `review` 理解成抽象判断层，没有把父层 aggregate JSON 当成唯一 gate | validation aggregate landing gap | 把 `review/第V卷.validation.json` 明确写成父层 canonical sink | 固定“child report 只是维度证据，aggregate JSON 才是真正 gate”的根层认知 | 出现 PASS/FAIL 问题时，定位会先落到 aggregate JSON，而不是散落 child sidecar |
| 普通 skill 或子技能直接调用后只落业务产物，`STATE.json` 没有阶段完成记录 | direct skill state gap | 完成时调用 `workflow_manager.py record-skill-completion` 写入 `workflow_runtime.execution_state.stage_progress` | 在根级和 1-4 阶段完成合同固定普通 skill completion hook | 普通父技能/子技能执行后，`stage_progress`、`history`、`task_log` 都能看到对应 run |
| 初稿、润色和调度都默认落到同一个模型，导致文本气口单一或检测分布收缩 | model role collapse | 回到根级三模型交叉分工：GPT 总领/结构/review，Doubao 写初稿，DeepSeek 做最小局部修补 | 在根 `SKILL.md` 固定默认正文链路 `Doubao 初稿 -> DeepSeek 最小局部修补`，显式切 lane 才例外 | 普通章节生产默认进入 `3-初稿/B-Doubao流`，普通润色默认进入 `4-润色/C-Deepseek流` |
| 用户要求改某个局部，执行者直接进入当前章或对象卡点对点修改 | story repair scope collapse | 进入 `repair` 卫星技能，先产出 impact map，再按 source-first 顺序写回 | 根级路由把跨设定/规划/正文/review/return 的局部修改统一交给 `.agents/skills/story/repair` | 修复报告包含 upstream、同层前列、当前局部、downstream、future constraints、review/return/state |

## Repair Playbook

1. 先判断问题是“缺总入口”“路由错”“真源错认”“共享 carrier 误放置”中的哪一种。
2. 若问题涉及 runtime 根路径，先核对当前 canonical 是否仍是 `projects/story/<项目名>/`，再判断旧 `projects/aigc/<项目名>/` 是否只是 legacy 遗留。
3. 若问题跨两个以上阶段，先回根级 `story/SKILL.md` 做总线诊断，再进入阶段修复。
4. 若同一规则在多个阶段重复出现，优先找根级 canonical source，而不是逐个阶段补丁。
5. 若问题涉及题材方向盘，先检查 `0-初始化/north_star.yaml.genre_contract` 是否已经存在并被 `2-卷章` 正式导入。
6. 若问题涉及验收或回写，先确认是否已有 `review/第V卷.validation.json` 与 `context-return/第V卷.context-return.json`，不要先看 child sidecar 或口头说明。
7. 若问题涉及“完成了但状态没变”，先检查是否走了 `record-skill-completion`；普通 skill / 子技能不应依赖完整 workflow task 才能写入状态。
8. 若问题涉及 AI 检测、人工成分下降或润色后变规整，先判断是否发生整章重写式润色；默认改回 DeepSeek 最小局部修补，而不是继续加大“去 AI 味”提示。
9. 若问题是“改一个局部但可能牵动整体”，先路由到 `repair` 卫星技能产出影响图；不要由当前看起来最近的阶段直接点对点修改。

## Reusable Heuristics

- 根级 skill 最有价值的工作不是“替阶段再说一遍”，而是回答“该去哪一层、该信哪一层、哪些共享层先读”。
- 先看项目是否还被错误绑定到 `projects/aigc/<项目名>/`；对当前仓库，小说项目的 canonical runtime 已回收到 `projects/story/<项目名>/`。
- 题材判断默认属于人工创作层，系统只能承接 `类型卡`，不应替作者自动激活题材机制。
- 最稳的题材方案不是给每个题材重写一套 workflow，而是维持固定方法核，把题材判断集中在 `类型卡`，再由 downstream 显式消费。
- 新规划层的 primary truth 应先看 `1-部级 -> 2-卷级 -> 3-章级` 对应的 `整体规划.md / 第N卷/卷规划.md / 第N卷/第N章.md`；`全息地图.json` 只保留兼容消费价值，不再是创作主真源。
- `review` 真正能给下游授权的不是 child 维度报告，而是父层 `第V卷.validation.json` 里的 `validation_status / routing_decision / handoff_targets` 组合。
- workflow CLI 和普通 skill completion 是两条入口，但状态落点必须统一到项目 `STATE.json#workflow_runtime.execution_state.stage_progress`。
- 三模型分工不是能力排名，而是工序分工：GPT 管结构和调度，Doubao 负责初稿中文气口，DeepSeek 负责润色阶段的长推理局部修补。
- AI 检测友好的润色通常不是“更顺”，而是少动：保留初稿的句群骨架、长短不齐、局部粗粝和人工式不均匀，只修坏处。
- 局部 repair 的起点是影响图，不是文件 patch；需要先问旧口径在哪些源层和消费者里存在，再决定改哪里。
