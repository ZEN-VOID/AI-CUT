# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc` 根技能的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/SKILL.md` 时，应自动预加载本文件。
- 详细 rollout 时间线与状态同步流水外置到 [`CHANGELOG.md`](./CHANGELOG.md)，本文件仅保留知识库与结论化里程碑。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type                                                                                                    | root_cause_layer       | immediate_fix                                                                                                                             | systemic_prevention                                                                                                                                                          | verification_point                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 旧 harness 审计把 `aigc` 阶段细节绑定过深，导致重大改造一开始就被历史合同卡死                                            | harness / audit 控制层 | 将 `aigc` 控制面切到 `bootstrap_compat`，保留项目 runtime、治理 carriers 与卫星技能入口，放松深层阶段审计                             | 对 suite 级重大改造优先保留骨架真源，并在 registry / routes / audit 中加入显式兼容模式开关，而不是整套清空 harness                                                           | `scripts/aigc_skill_audit.py --strict` 在兼容模式下通过，且允许阶段内部重构                           |
| 技能树目录已建，但没有根总合同                                                                                             | 根技能源层             | 补根 `SKILL.md` 与根 `CONTEXT.md`，锁定总入口、总路由、总闭环                                                                         | 把根技能视为主控面真源，后续阶段一律向上挂接                                                                                                                                 | 根技能能说明项目根目录、阶段路由、治理挂载与闭环                                                        |
| 顾问团机制散落在多个阶段，无法共享消费                                                                                     | 真源治理层             | 将跨阶段规则上收至 `_shared/council-runtime/`，并把项目级团队真源固定为 `projects/<项目名>/team.yaml`                                 | 阶段根技能只保留角色适配，不再复制运行时合同                                                                                                                                 | 进入 `1-Planning / 2-Global / 3-Detail / 4-Design` 时都能先判断 `team.yaml`                         |
| 阶段目录存在，但阶段 `SKILL.md` / `CONTEXT.md` 为空                                                                    | 阶段合同层             | 在根技能中显式标记“已建骨架，待写实质合同”                                                                                              | 对空合同阶段禁止伪造执行细节，只返回缺口与补建落点                                                                                                                           | 路由时能区分“可执行阶段”和“预留阶段”                                                                |
| `subtypes/` 很多，但尚未形成受治理子技能                                                                                 | 子技能源层             | 在根技能中把 `subtypes/` 定义为未来可执行子技能槽位                                                                                     | 后续仅对高杠杆子技能逐步补 `SKILL.md + CONTEXT.md`，不一次性铺满                                                                                                           | 子技能扩展不会再次退化为纯目录分类                                                                      |
| 创作输出未绑定到 `projects/<项目名>/`                                                                                    | 项目工作区合同层       | 在根技能中把 `projects/<项目名>/` 明确为 canonical landing                                                                              | 把项目工作区写进根合同与阶段合同，不允许阶段各自发明落点                                                                                                                     | 项目输出与运行状态都能归到单个项目工作区                                                                |
| 根技能已形成总控面                                                                                                         | 根技能经验层           | 把主阶段链、治理挂载、工件落点统一写入根合同                                                                                              | 将后续阶段合同、子技能合同和 registry 注册都向根技能对齐                                                                                                                     | `aigc` 能成为仓库级核心技能包入口                                                                     |
| `0-Init` 目录存在但没有实质合同                                                                                          | 阶段合同层             | 为 `0-Init` 建立多模式初始化合同、`north_star` 主产物与项目根落盘规范                                                                 | 让根技能的阶段状态与 `0-Init` 实际合同同步，不再把初始化长期停在“预留中”                                                                                                 | 根技能可稳定路由到 `0-Init`，且产物边界清晰                                                           |
| 子阶段已补齐实质合同，但根技能仍沿用“骨架/待补”旧状态                                                                    | 元路由层               | 同步更新根技能阶段覆盖状态与调度说明                                                                                                      | 将阶段状态变更视为需要向上同步的 meta 修复，而不是停留在子阶段局部                                                                                                           | 根技能对阶段状态的描述与实际子技能覆盖一致                                                              |
| `2-Global` 已完成父子合同，但根技能状态表仍停留在旧口径                                                                  | 根技能状态同步层       | 同步更新 `.agents/skills/aigc/SKILL.md` 的阶段状态与调度说明                                                                            | 把阶段覆盖状态视为根入口投影，子阶段升级后必须回写                                                                                                                           | 根技能表格与 `2-Global` 实际状态一致                                                                  |
| 分组后节奏子技能迁到 `1-Planning`，但根技能仍把它写在 `2-Global`                                                       | 根技能状态同步层       | 同步更新根技能中 `1-Planning / 2-Global` 的阶段状态、调度策略与描述                                                                     | 把“阶段职责迁移”视为必须向上同步的元修复，而不是停留在局部技能文案                                                                                                         | 根技能能正确说明 `4-节奏` 归属与 `2-Global` 的消费关系                                              |
| `3-明细` 已完成阶段父级与 `2-角色表现` 父子合同，但根技能仍写“已建骨架”                                              | 根技能状态同步层       | 同步更新 `.agents/skills/aigc/SKILL.md` 的 `3-明细` 阶段状态                                                                          | 把脚本阶段状态同步视为阶段合同补建的收尾动作                                                                                                                                 | 根技能表格与 `3-明细` 当前状态一致                                                                    |
| `3-明细/3-运镜手法` 已建合同，但根技能仍只知道 `2-角色表现`                                                            | 根技能状态同步层       | 同步根技能中 `3-明细` 的可执行子路径说明                                                                                                | 把“关键子路径可执行状态”视为根入口必须回写的投影                                                                                                                           | 根技能能正确路由到 `3-运镜手法`                                                                       |
| `3-明细/4-场景氛围` 已建合同，但根技能仍未把它列为可路由入口                                                             | 根技能状态同步层       | 同步根技能中 `3-明细` 的可执行子路径说明                                                                                                | 把“关键子路径可执行状态”视为根入口必须回写的投影                                                                                                                           | 根技能能正确路由到 `4-场景氛围`                                                                       |
| `3-明细/5-摄影美学` 已建合同，但根技能仍不知道摄影层可执行                                                               | 根技能状态同步层       | 同步根技能中 `3-明细` 的可执行子路径说明                                                                                                | 把“编号子路径升级为可执行入口”视为根入口必须回写的投影                                                                                                                     | 根技能能正确路由到 `5-摄影美学`                                                                       |
| `3-明细/6-转场特效` 已建合同，但根技能仍只知道 `2-角色表现` 与 `3-运镜手法`                                          | 根技能状态同步层       | 同步根技能中 `3-明细` 的可执行子路径说明                                                                                                | 把“关键子路径可执行状态”视为根入口必须回写的投影                                                                                                                           | 根技能能正确路由到 `6-转场特效`                                                                       |
| `5-画面` 父子合同已补齐，但根技能仍把该阶段标记为空骨架                                                                  | 根技能状态同步层       | 同步更新 `.agents/skills/aigc/SKILL.md` 中 `5-画面` 的阶段状态与子路径说明                                                            | 把阶段合同补齐后的状态上收视为根入口必须完成的收尾动作                                                                                                                       | 根技能能正确路由到 `分镜故事板 / 分镜帧 / 漫画`                                                       |
| `4-Design` 父子合同已补齐，但 shared runtime 与根技能消费方仍沿用 `主体/` 旧目录                                       | 根技能状态同步层       | 同步 `.agents/skills/aigc/SKILL.md` 与 `_shared/project-runtime-layout.md` 中的 design 阶段 runtime 口径                              | 把“design 阶段 runtime 变更”视为必须向上同步到 query/review/council-runtime 的元修复                                                                                       | 根技能与共享载体都指向 `projects/<项目名>/4-Design/`                                                  |
| 项目根运行时与 `.codex/state/tasks` 同时存在，但没有优先级声明                                                           | harness 状态面层       | 明确 `projects/<项目名>/` 为 AIGC 项目 canonical runtime                                                                                | 将 runtime 优先级同步写入 runbook、registry、audit 与三省合同                                                                                                                | 技能树、registry、runbook 对状态真源的说法一致                                                          |
| `1-Planning/2-Global/3-Detail` 各自维护不同阶段目录与 episode 文件，导致导演真源分裂                                     | 真源治理层             | 上收统一运行时布局到 `.agents/skills/aigc/_shared/project-runtime-layout.md`，并固定 `projects/<项目名>/3-Detail/第N集.json` 为单一根文件 | 让 `1-分集` 只负责 bootstrap handoff，`2-Global` 负责写三份导演前置 Markdown并 seed `组间设计`，`3-Detail` 再围绕同一根文件补齐 shot-level 明细，所有父级合同都回指 shared layout + shared schema | 根技能、阶段技能与 shared carrier 对 `Init/1-Planning/2-Global/编导/4-Design/画面/视频/后期` 说法一致 |
| 阶段技能已声明 subagents 拓扑，但没写“默认后台执行”或仍残留失效 team 路径                                                | subagent 编排合同层    | 在父 skill / team 明确“无论有序还是无序都默认后台 subagents”，并清理失效 `.codex/agents/aigc/*` 路径                                  | 将后台执行规则与 agent 引用存在性检查同时接入阶段合同和 `scripts/aigc_skill_audit.py`                                                                                      | 角色拓扑既能解释顺序，也能解释运行形态，且审计能拦住断链                                                |
| 阶段执行状态只写在根技能表格里，registry / audit 不知道                                                                    | 注册与审计层           | 将阶段状态上收至 `.codex/registry/skills.yaml`，并补 `scripts/aigc_skill_audit.py`                                                    | 把“阶段 active / shelved”视为控制面真源，而不是仅属技能文案                                                                                                                | 审计可识别哪些阶段可执行、哪些已搁浅                                                                    |
| `7-后期` 当前不做，但仍被视为待补执行阶段                                                                                | 阶段生命周期层         | 在根技能与 registry 中显式标记为 `搁浅`                                                                                                 | 审计脚本对搁浅阶段跳过严格失败，但要求根技能与 registry 同步声明                                                                                                             | 总入口不会再把搁浅阶段误判为立即补建目标                                                                |
| `6-视频` 已补父子合同，但根技能与控制面仍写 `shelved`                                                                  | 根技能状态同步层       | 同步根技能、registry、routes 与 HARNESS 的阶段状态                                                                                        | 把“阶段由搁浅转为部分可执行”视为必须向上同步的元修复                                                                                                                       | 总入口与阶段真源对 `6-视频` 的描述一致                                                                |
| `6-视频` 父合同把 tranche 写成可执行，但磁盘上只有未治理占位目录或编号漂移                                               | 子路径真源治理层       | 收敛 tranche 编号、补齐父级 `SKILL.md + CONTEXT.md`，并把 provider 占位目录降级为非执行槽位                                             | 在审计脚本增加“文档声明的 `subtypes/...` 必须存在合同”检查                                                                                                               | 父合同、磁盘目录与审计结果对同一路径达成一致                                                            |
| 根 suite 缺 benchmark suite，导致只能做静态或低证据级评估                                                                  | 质量评测合同层         | 在 `aigc` 根目录补 `benchmark-suite.yaml`，至少覆盖 baseline 与 regression                                                            | 将 benchmark suite 作为根级质量证据载体显式挂入技能树                                                                                                                        | 评估时能直接读取任务集，而不是临时拼样本                                                                |
| governed leaf 已有字段表，但漏掉 `Root-Cause Execution Contract`                                                         | rollout 合同层         | 为 leaf 补齐根因上溯章节，并让严格审计继续把这项当成硬门槛                                                                                | 把“leaf 也必须有 root-cause 合同”视为 rollout 基线，而不是只要求父级技能齐全                                                                                               | `scripts/aigc_skill_audit.py --strict` 不再漏报或卡在同类缺项                                         |
| 根技能没有 `query / resume / review` 这类跨阶段旁路能力，导致事实查询、续跑与复核被塞回阶段链或聊天口头说明              | 根 suite contract 层   | 在 `.agents/skills/aigc/` 根目录补 `query`、`resume`、`review` 三个卫星技能，并同步 registry / routes / audit                     | 对跨全阶段但不拥有阶段内容真源的能力，优先建根级卫星技能，不再把它们藏进 `references/` 或某个阶段私有流程                                                                  | 根入口可直接路由到 `query / resume / review`，且 registry / audit 能识别                              |
| 已有 `query / resume / review`，但项目根没有结构化断点快照，导致三者仍只能围绕 `project_state.yaml` 自由文本猜恢复入口 | 根 runtime control 层  | 在 `0-Init` 新增 `governance-state.yaml` 并让卫星技能共读                                                                             | 对跨阶段治理能力，优先补共享结构化状态真源，而不是新增 `CHANGELOGS.md`                                                                                                     | 查询、续跑、复核都能从同一份 checkpoint 真源读取状态                                                    |

## Repair Playbook

1. 先确认 `aigc` 根目录是否已具备根 `SKILL.md` 与根 `CONTEXT.md`。
2. 先锁定主阶段链与项目工作区落点，再补阶段细节。
3. 对空合同阶段，不伪造执行规则，先在根合同里标记为“待补”。
4. 对子技能树，优先补高杠杆节点，不做一次性全量合同化。
5. 当根技能稳定后，再把阶段状态、runtime 优先级与搁浅策略同步注册进 route / audit 控制面。

## Reusable Heuristics

- 多子技能组合包最容易犯的错，是目录树长得很漂亮，但缺一个总控面；没有根合同时，阶段越多，漂移越快。
- 只要 `2-Global` 与 `3-Detail` 共用同一条导演链路，就不该再让多个阶段各自拥有自己的 episode 真稿；最稳的办法是让它们共享同一份 `3-Detail/第N集.json`，由 `2-Global` 先 seed `组间设计`，`3-Detail` 再补齐镜级事实。
- 当阶段目录已经明确是 runtime 分区时，父技能最该写清的是“字段责任”和“patch 顺序”，而不是各自再定义一套集文件壳。
- 当镜级字段同时想描述“角色位移”和“背景朝向”时，应拆成 `角色站位走位` 与 `角色背景面`；服装不要继续塞进镜级站位句，默认上收为组级 `出场角色及穿搭`，再由镜级按需继承。
- 在 AIGC 影视创作场景里，先固定 `projects/<项目名>/` 这种项目工作区，比先讨论每一阶段写多少提示词更重要。
- 对于已建目录但尚未写合同的阶段，最稳的做法不是硬补执行细节，而是在根技能中显式标为“预留中/待补合同”。
- `aigc` 根技能应更像 suite router，而不是内容生成器本身。
- 对 `aigc` 来说，初始化最值得固化的不是一套长问卷，而是“模式先锁定、north_star 为主、stage seed 为伴生、项目根为治理 runtime”的四件套。
- 当某个阶段已经从“骨架”升级为真实可执行入口时，必须把这次变化同步回根技能；否则根路由会继续把可执行阶段误判为待补。
- `3-明细` 一旦从空壳升级为父级合同，就应优先同步“阶段已建、子路径按状态路由”的信息；否则所有下游 handoff 都会卡在根入口认知层。
- 当 `3-明细` 某个编号子路径补齐为可执行合同后，根入口不应只同步“阶段存在”，还应同步“哪些关键子路径现在可直接路由”。
- 对根入口来说，`3-明细` 里的关键可执行子路径清单是动态投影；只要 `5-摄影美学` 这样的编号子路径补齐合同，就必须立刻上收同步。
- `3-明细` 的后位子路径即便还未形成完整串行链，也可以在用户显式命中时作为独立可执行入口，但根入口必须如实反映这一状态。
- `4-场景氛围` 这种中位 ordered 子路径一旦补齐，应立即加入根路由清单；否则总入口会跳过已经可执行的环境层。
- 对 `aigc` 项目工作流，`projects/<项目名>/` 不是普通内容目录，而是三省六部控制面认可的 canonical runtime；只有把它同步写进 runbook / registry / audit，技能树才算真正接上 harness。
- 对正在重大重构的 suite skill，不要先清空 harness；更稳的做法是保留 runtime / registry / review gate，再给审计增加显式 `bootstrap_compat` 模式开关。
- 当某阶段明确“不在当前轮次推进”时，优先把它标成 `搁浅`，而不是继续挂着“预留中”；`搁浅` 表示有意冻结，不应被审计当作立即补全失败。
- 对跨兄弟阶段共同消费的治理工件，真源应优先放项目根；对跨兄弟阶段共同执行的运行规则，真源应优先放 `_shared/`。
- 只要 shared schema 或 phase handoff 合同发生明显升级，最稳的落地不是只补 schema `examples`，而是补一组 `_shared/examples/` 下的同 episode phase-transition 样例，让执行者能直接对照 `directing_in_progress -> detail_in_progress -> ready`。
- 当技能阶段名本身带序号时，不要默认把这个序号投影到项目 runtime 目录；项目目录应优先服从 `_shared/project-runtime-layout.md` 的映射。
- 一旦 `_shared/project-runtime-layout.md` 已明确采用技能树真实目录名，`0-Init`、共享模板、governance-state、query/resume 和 backfill 脚本都必须直接复用同一组阶段名：`0-Init / 1-Planning / 2-Global / 3-Detail / 4-Design / 5-Image / 6-Video / 7-Cut`。
- 若某项能力横跨所有阶段，但它只负责读取、恢复、复核或桥接，而不拥有阶段内容真源，最稳的落点是根级卫星技能，而不是再加一个伪 stage。
- 在 `aigc` 里，`query / resume / review` 的最稳分工分别是：尚书省+户部读真源、尚书省+兵部续跑、门下省+刑部做预审与验收桥接。
- 当根级卫星技能开始承担项目治理职责时，`project_state.yaml` 已经不够；最稳的补强不是 `CHANGELOGS.md`，而是单独的 `governance-state.yaml` 结构化快照。
- 对 subagent 阶段来说，`有序/无序` 只定义依赖，不定义交互形态；默认后台派发必须单独写进父 skill 和 team 合同。
- 只要阶段文档显式引用 `.codex/agents/aigc/**`，就不该再把“路径是否存在”留给人工记忆；审计脚本应直接把断链判成失败。

## Case Log

### Case-20260412-AIGC-ROOT-INIT-RUNTIME-SKELETON-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能对项目初始化目录结构的投影同步到最新 `aigc` 技能树，明确 `0-Init` 预建的不只是阶段根目录，还包括当前 active 子路径骨架。
- root_cause_or_design_decision: 根技能、`0-Init`、shared runtime layout 与审计脚本之间对“初始化该建哪些目录”出现漂移；旧口径只覆盖根目录，无法反映 `1-Planning / 4-Design / 5-Image / 6-Video` 当前真实 canonical landing。
- final_fix_or_heuristic: 让根技能回指同一套 shared runtime skeleton，并把 `Story/`、`4-Design/`、`5-Image/*`、`6-Video/*` 的当前项目目录结构同步为统一投影；初始化目录预建应永远基于 runtime canonical landing，而不是技能文件系统中间层。
- prevention_or_replication_checklist:
  - [x] 根 `SKILL.md` 已补 `projects/<项目名>/Story/`
  - [x] `0-Init/SKILL.md` 已显式列出 active child skeleton
  - [x] `_shared/project-runtime-layout.md` 已升级为统一 skeleton 真源
  - [x] `scripts/aigc_skill_audit.py` 已同步新的 runtime marker
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求“根据 `.agents/skills/aigc` 最新的目录结构，重新约定 `.agents/skills/aigc/0-Init` 初始化时项目目录结构”。

### Case-20260412-AIGC-ROOT-DIRECTOR-PHASE-TRANSITION-EXAMPLE

- milestone_type: source_contract_change
- outcome: 曾为 shared director root 补过同一 episode 的 phase-transition 三段样例，用于解释 `2-Global -> directing_in_progress -> 3-Detail -> detail_in_progress -> ready`。
- root_cause_or_design_decision: 仅靠 schema 的内嵌 examples 一度不足以充当真实项目 seed 样例，执行者难以把“同一 root、跨 phase patch-in-place”的关系看清，尤其容易把 `ready` 误解为另起一份终稿。
- final_fix_or_heuristic: 当前口径已从“依赖静态共享示例”调整为“直接读取真实项目里同一 `第N集.json` 的 `metadata.document_phase` 与 `分镜明细[]` 变化”；共享示例因会引入模板污染风险而退役，不再作为规范真源。
- prevention_or_replication_checklist:
  - [x] `group_design_seed_contract.md` 已回指样例
  - [x] `project-runtime-layout.md` 已给出 phase 读取规则
  - [x] 当前已改为直接读取真实项目 root 的 phase 推进，不再依赖静态样例
- evidence_paths:
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
- user_feedback_or_constraint: 用户明确要求“直接补一轮真实项目样例 seed”，希望能看到某个 `第N集` 从 `2-Global` seed 到 `3-Detail` 继续补全的完整示例 JSON。

## Archive Index

- 详细 rollout 时间线已外置到 [`CHANGELOG.md`](./CHANGELOG.md)。
- 已迁出的阶段状态同步与目录命名过程记录：
  - `Case-20260410-AIGC-ROOT-RUNTIME-DIR-NONNUMERIC`
  - `Case-20260409-AIGC-ROOT-PLANNING-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-DIRECTING-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-SCRIPT-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-SCRIPT-CAMERA-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-SCRIPT-ATMOSPHERE-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-SCRIPT-CINEMATOGRAPHY-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-SCRIPT-TRANSITION-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-STORYBOARD-STATUS-SYNC`
  - `Case-20260409-AIGC-ROOT-SUBJECT-STATUS-SYNC`
  - `Case-20260410-AIGC-ROOT-VISUAL-STAGE-RENAME`
  - `Case-20260410-AIGC-ROOT-VIDEO-STAGE-ACTIVATE`
  - `Case-20260410-AIGC-ROOT-VIDEO-FIRST-FRAME-STATUS-SYNC`
  - `Case-20260411-AIGC-ROOT-VIDEO-SUBMIT-STATUS-SYNC`
- 已迁出的 rollout / 控制面补丁记录：
  - `Case-20260409-AIGC-INIT-CONTRACT`
  - `Case-20260409-AIGC-PROJECT-ROOT-RUNTIME`
  - `Case-20260409-AIGC-LEAF-ROLLOUT-CLOSURE`
  - `Case-20260409-AIGC-ROOT-COUNCIL-RUNTIME`
  - `Case-20260410-AIGC-RUNTIME-MAPPING-RECONCILIATION`
  - `Case-20260411-AIGC-ROOT-BENCHMARK-SUITE-BOOTSTRAP`
