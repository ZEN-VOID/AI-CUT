# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/lesson` 根技能经验层知识库，不是第二份根合同。
- 调用 `$lesson` 时，它必须与同目录 `SKILL.md` 一起加载，用于识别课程课件项目路由漂移、阶段边界缺口、三端交付分叉和卫星越权。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > `SKILL.md` > 阶段或卫星 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-root-router-heuristics

## Type Map

| type_id | symptom | likely root layer | immediate fix | verification |
| --- | --- | --- | --- | --- |
| `LESSON-TM-01` | 课程项目被写入 `projects/courseware/` 或其他 namespace | runtime route layer | 回到根 `SKILL.md`，固定 `projects/lesson/<项目名>/` | 初始化和阶段输出路径一致 |
| `LESSON-TM-02` | 根入口开始直接写课程正文、题库、PPT 文案或 HTML 页面 | root overreach layer | 路由到 owning stage，根入口只输出 route evidence | 根入口没有业务主稿写回 |
| `LESSON-TM-03` | DOC/PPT/HTML 各自演化出一套主稿 | content-model drift layer | 回到共享 `content-model/` 和 `8-多端交付生成` 上游合同 | 三端交付可追溯到同一内容模型 |
| `LESSON-TM-04` | `review/` 被重新加成独立卫星入口 | review topology drift | 删除独立 review 卫星设想；阶段内置 gate 承担验收 | root satellite table 不含 `review/` |
| `LESSON-TM-05` | `query/resume/repair/learn/benchmark` 试图改写阶段业务真源 | satellite boundary layer | 回到卫星边界：旁路只写证据、恢复路线、学习包或基准报告 | 阶段主稿由 owning stage 写回 |
| `LESSON-TM-06` | 资料吸收阶段和课程定位阶段互相吞并 | stage ordering layer | `1-课程定位` 锁项目目标和约束，`2-资料吸收与知识建模` 建知识真源 | 两阶段输出职责可区分 |
| `LESSON-TM-07` | 资料吸收阶段把来源摘要直接当知识真源 | evidence modeling layer | 先建立 source inventory 和 evidence audit，再合成概念层级、术语、案例、误区和依赖关系 | 第 2 阶段输出含来源、证据、知识模型和 handoff |
| `LESSON-TM-08` | 阶段目录和 `content-model/` 看起来像两套课程主稿 | content-model truth split layer | 明确阶段 canonical files 是阶段真源，`content-model/` 只承载索引、handoff、派生投影或 owning stage 授权写入的共享模型片段 | root `FIELD-LESSON-ROOT-03` 与 `PASS-LESSON-03` 一致 |
| `LESSON-TM-09` | 卫星包激活后根文档仍写 placeholder 或 once implemented | root index drift | 同步 root `SKILL.md` Reference Loading Guide、README 状态和 CHANGELOG | `query/resume/repair/learn/benchmark` 均可加载 `SKILL.md + CONTEXT.md` |
| `LESSON-TM-10` | `_shared/` 被误当成阶段、卫星、默认模块或第二规则源 | shared support boundary drift | 在根 `SKILL.md` 固定 `_shared/` 仅为非执行支持载体；consuming skill 必须自行显式授权 | README 树、root Shared Support Boundary 和 consuming skill Module Loading Matrix 一致 |
| `LESSON-TM-11` | 对 lesson 根目录直接跑 smoke 时出现子包 `agents/openai.yaml` broken reference 和 `_shared/` empty 条件 | nested skill smoke scope layer | 根 router 以 validator 为主；smoke 应对阶段、叶子、卫星逐包运行；根 smoke 条件需按递归扫描误报解释 | 根 validator PASS，子包 individually smoke ACCEPT，临时报表不残留 |
| `LESSON-TM-12` | 后续阶段只看上游目录存在，跳过 `downstream-handoff.md` 的缺口、N/A 或阻断项 | upstream handoff bypass | 回到根 `Upstream Loading Matrix`，把 handoff 作为状态门；局部阶段补 `upstream_handoff_status` 输入 | 阶段 `Input Contract` 和 `Read-only` 均声明 handoff 必读 |
| `LESSON-TM-13` | `content-model/` 被多个阶段随意刷新，或第 8 阶段反向补写正文 | content-model ownership drift | 回到根 `Content Model Governance Contract`，按 `modules/lessons/assessments/delivery-map` 分区归属 owning writer | root contract 与阶段 Output/Permission Boundaries 一致 |
| `LESSON-TM-14` | 阶段包只声明加载 `CONTEXT.md`、项目 `MEMORY.md` 或上游 handoff，但未说明加载后如何分类、处理缺失、解决冲突和写回 | stage context processing layer | 给 0-8 阶段补 `Context Processing Contract`，统一 `context_snapshot`、manifest、classification、missing policy、conflict map、application 和 writeback decision | 0-8 阶段 context coverage 检查通过，且逐包 delivery validator PASS |

## Repair Playbook

1. 先锁定用户请求类型：初始化、主链阶段、交付叶子、查询、恢复、修复、学习吸收或基准对照。
2. 若项目根缺失或漂移，优先路由 `0-初始化` 或 `resume`，不要让后续阶段自行发明项目骨架。
3. 若请求涉及 DOC/PPT/HTML，先确认是否已有共享内容模型；没有时应回到 `4/5/6/7` 的 owning stage，而不是直接导出。
4. 若用户指出课程质量问题，先判断源层：定位、资料、目标、架构、正文、练习、视觉还是交付投影；再路由修复。
5. 若新增、删除或重命名阶段/卫星，必须同步根 `SKILL.md` 的 Stage/Satellite 表、README 树和本 `CONTEXT.md` 的经验映射。
6. 若新增 `_shared/` 下的共享资产，先判定它是 schema、模板、脚本、静态资源还是资料；根层只登记边界，实际加载权必须落到使用它的阶段、叶子或卫星 `SKILL.md`。
7. 根目录包含多个完整子技能包时，根 smoke 的 Broken reference scan 会跨包递归扫描并按根目录解析子包内部相对路径；这种条件不等同于子技能包失效，必须用逐包 smoke 结果确认。
8. 若阶段上游加载口径变化，先修根 `Upstream Loading Matrix`，再同步受影响阶段的 `Context Loading Contract`、`Input Contract`、`Output Contract` 和 `Permission Boundaries`。
9. 若 `content-model/` 写入边界变化，必须同时检查 `4/5/6/8` 的 owning writer 与第 `8` 阶段只读/投影边界，避免出现第二课程主稿。

## Reusable Heuristics

- lesson 根入口最稳的职责是“选唯一入口 + 保持课程项目 runtime 真源”，不是替阶段写课程内容。
- 高质量课程课件的关键不是先导出 PPT，而是先建立：课程定位、知识真源、评价蓝图、教学策略、内容模型。
- `content-model/` 是后续 DOC/PPT/HTML 多端投影的共享上游，但不是第二份阶段主稿；阶段目录中的 canonical files 才是各阶段业务真源。
- `downstream-handoff.md` 是阶段间状态门，不是礼貌性附录；后续阶段必须读取其中的可消费字段、限制、N/A、阻断项和返工入口。
- `content-model/modules/`、`lessons/`、`assessments/`、`delivery-map.*` 必须有 owning writer；无 owning writer 的共享模型更新就是 drift 信号。
- 阶段技能的上下文治理要分两层审查：先看是否加载同目录 `CONTEXT.md`、lesson 根、项目 `MEMORY.md`、项目 `CONTEXT/` 和必要 handoff；再看是否形成 `context_snapshot`、处理缺失/冲突，并把长期偏好、经验层和一次性产物写回到正确落点。
- `1-课程定位` 回答为什么做、给谁用、在哪用、边界和约束；`3-目标与评价蓝图` 回答学完能做什么、如何证明学会。
- `2-资料吸收与知识建模` 应早于学习目标细化；否则目标和课程结构容易脱离事实资料。
- `7-视觉媒体与交互设计` 不是美化阶段，而是把课程变成可观看、可演示、可操作的学习体验。
- `8-多端交付生成` 是格式投影阶段；它可以做格式和一致性自检，但不应首次承担课程质量设计。
- 根层不保留独立 `review/` 卫星；验收机制进入各阶段 `Review Gate Binding`。
- `query/resume/repair/learn/benchmark` 是已激活卫星，不参与 0-8 主链串行推进；它们只处理查询、恢复、修复、学习吸收和基准对照，不夺取阶段业务真源。
- `_shared/` 是 lesson 技能树内部的共享支持载体，不是主链阶段、卫星技能、项目 runtime 或上下文默认加载源；空目录存在时只表达预留边界。
- lesson 根 router 的结构校验优先看 `validate_skill_2_0.py .agents/skills/lesson --mode delivery`；完整冒烟应逐包覆盖 0-8、三端叶子和卫星，而不是只看根递归 smoke。

## Case Log

> 仅记录里程碑案例，避免过程流水账。

### Case-001

- milestone_type: workflow_root_initialization
- outcome: 建立 `lesson` 工作流根入口文件，固定 0-8 主链、`projects/lesson/<项目名>/` runtime、DOC/PPT/HTML 交付叶子和卫星边界。
- design_decision: 根入口采用 router 角色，不直接主创课程正文或最终交付物；阶段内置 gate，不设独立 `review/` 卫星。
- evidence_paths: `.agents/skills/lesson/SKILL.md`, `.agents/skills/lesson/CONTEXT.md`

### Case-002

- milestone_type: knowledge_modeling_stage_activation
- outcome: 启用 `2-资料吸收与知识建模`，固定 deep research、source inventory、evidence audit、knowledge model、case/misconception library 和 downstream handoff 的阶段边界。
- design_decision: 第 2 阶段默认消费 `1-课程定位/course-positioning.md`，正式写回多份 canonical MD，而不是把调研结论散落到后续阶段。
- evidence_paths: `.agents/skills/lesson/2-资料吸收与知识建模/SKILL.md`, `.agents/skills/lesson/2-资料吸收与知识建模/CONTEXT.md`

### Case-003

- milestone_type: satellite_activation
- outcome: 启用 `query/`、`resume/`、`repair/`、`learn/` 和 `benchmark/` 五个卫星技能包，形成课程项目事实查询、断点恢复、source-first 修复、外部资料学习吸收和基准对照的旁路能力。
- design_decision: 卫星技能默认不纳入 0-8 主链；它们输出证据、恢复裁决、repair packet、learning packet 或 benchmark matrix，不直接改写阶段业务真源。
- evidence_paths: `.agents/skills/lesson/query/SKILL.md`, `.agents/skills/lesson/resume/SKILL.md`, `.agents/skills/lesson/repair/SKILL.md`, `.agents/skills/lesson/learn/SKILL.md`, `.agents/skills/lesson/benchmark/SKILL.md`

### Case-004

- milestone_type: root_directory_index_sync
- outcome: 根层文档同步到最新目录结构：0-8 主阶段、`8/doc|ppt|html` 三端叶子、`query|resume|repair|learn|benchmark` 五个卫星和 `_shared/` 共享支持载体。
- design_decision: 根 README 负责展示目录索引，根 `SKILL.md` 负责路由与边界；`_shared/` 只作为非执行支持载体，不拥有独立 `SKILL.md + CONTEXT.md`，也不作为默认上下文加载源。
- evidence_paths: `.agents/skills/lesson/SKILL.md`, `.agents/skills/lesson/README.md`, `.agents/skills/lesson/CONTEXT.md`, `.agents/skills/lesson/CHANGELOG.md`

### Case-005

- milestone_type: upstream_loading_full_repair
- outcome: 补齐根级 `Upstream Loading Matrix` 和 `Content Model Governance Contract`，并同步 1-8 阶段上游 handoff、全局定位锚点、证据回看和 content-model 分区写入边界。
- design_decision: `1/course-positioning.md` 成为 `2-8` 的全局定位锚点；`downstream-handoff.md` 成为阶段间状态门；`content-model/` 按 `modules/lessons/assessments/delivery-map` 分区归属 owning writer。
- evidence_paths: `.agents/skills/lesson/SKILL.md`, `.agents/skills/lesson/1-课程定位/SKILL.md`, `.agents/skills/lesson/2-资料吸收与知识建模/SKILL.md`, `.agents/skills/lesson/3-目标与评价蓝图/SKILL.md`, `.agents/skills/lesson/4-教学策略与课程架构/SKILL.md`, `.agents/skills/lesson/5-课时内容开发/SKILL.md`, `.agents/skills/lesson/6-活动练习与测评开发/SKILL.md`, `.agents/skills/lesson/7-视觉媒体与交互设计/SKILL.md`, `.agents/skills/lesson/8-多端交付生成/SKILL.md`
