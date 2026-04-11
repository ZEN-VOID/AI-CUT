# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc` 根技能的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 技能树目录已建，但没有根总合同 | 根技能源层 | 补根 `SKILL.md` 与根 `CONTEXT.md`，锁定总入口、总路由、总闭环 | 把根技能视为主控面真源，后续阶段一律向上挂接 | 根技能能说明项目根目录、阶段路由、治理挂载与闭环 |
| 顾问团机制散落在多个阶段，无法共享消费 | 真源治理层 | 将跨阶段规则上收至 `_shared/council-runtime/`，并把项目级团队真源固定为 `projects/<项目名>/team.yaml` | 阶段根技能只保留角色适配，不再复制运行时合同 | 进入 `1-规划 / 2-组间 / 3-明细 / 4-主体` 时都能先判断 `team.yaml` |
| 阶段目录存在，但阶段 `SKILL.md` / `CONTEXT.md` 为空 | 阶段合同层 | 在根技能中显式标记“已建骨架，待写实质合同” | 对空合同阶段禁止伪造执行细节，只返回缺口与补建落点 | 路由时能区分“可执行阶段”和“预留阶段” |
| `subtypes/` 很多，但尚未形成受治理子技能 | 子技能源层 | 在根技能中把 `subtypes/` 定义为未来可执行子技能槽位 | 后续仅对高杠杆子技能逐步补 `SKILL.md + CONTEXT.md`，不一次性铺满 | 子技能扩展不会再次退化为纯目录分类 |
| 创作输出未绑定到 `projects/<项目名>/` | 项目工作区合同层 | 在根技能中把 `projects/<项目名>/` 明确为 canonical landing | 把项目工作区写进根合同与阶段合同，不允许阶段各自发明落点 | 项目输出与运行状态都能归到单个项目工作区 |
| 根技能已形成总控面 | 根技能经验层 | 把主阶段链、治理挂载、工件落点统一写入根合同 | 将后续阶段合同、子技能合同和 registry 注册都向根技能对齐 | `aigc` 能成为仓库级核心技能包入口 |
| `0-Init` 目录存在但没有实质合同 | 阶段合同层 | 为 `0-Init` 建立多模式初始化合同、`north_star` 主产物与项目根落盘规范 | 让根技能的阶段状态与 `0-Init` 实际合同同步，不再把初始化长期停在“预留中” | 根技能可稳定路由到 `0-Init`，且产物边界清晰 |
| 子阶段已补齐实质合同，但根技能仍沿用“骨架/待补”旧状态 | 元路由层 | 同步更新根技能阶段覆盖状态与调度说明 | 将阶段状态变更视为需要向上同步的 meta 修复，而不是停留在子阶段局部 | 根技能对阶段状态的描述与实际子技能覆盖一致 |
| `2-组间` 已完成父子合同，但根技能状态表仍停留在旧口径 | 根技能状态同步层 | 同步更新 `.agents/skills/aigc/SKILL.md` 的阶段状态与调度说明 | 把阶段覆盖状态视为根入口投影，子阶段升级后必须回写 | 根技能表格与 `2-组间` 实际状态一致 |
| 分组后节奏子技能迁到 `1-规划`，但根技能仍把它写在 `2-组间` | 根技能状态同步层 | 同步更新根技能中 `1-规划 / 2-组间` 的阶段状态、调度策略与描述 | 把“阶段职责迁移”视为必须向上同步的元修复，而不是停留在局部技能文案 | 根技能能正确说明 `4-节奏` 归属与 `2-组间` 的消费关系 |
| `3-明细` 已完成阶段父级与 `2-角色表现` 父子合同，但根技能仍写“已建骨架” | 根技能状态同步层 | 同步更新 `.agents/skills/aigc/SKILL.md` 的 `3-明细` 阶段状态 | 把脚本阶段状态同步视为阶段合同补建的收尾动作 | 根技能表格与 `3-明细` 当前状态一致 |
| `3-明细/3-运镜手法` 已建合同，但根技能仍只知道 `2-角色表现` | 根技能状态同步层 | 同步根技能中 `3-明细` 的可执行子路径说明 | 把“关键子路径可执行状态”视为根入口必须回写的投影 | 根技能能正确路由到 `3-运镜手法` |
| `3-明细/4-场景氛围` 已建合同，但根技能仍未把它列为可路由入口 | 根技能状态同步层 | 同步根技能中 `3-明细` 的可执行子路径说明 | 把“关键子路径可执行状态”视为根入口必须回写的投影 | 根技能能正确路由到 `4-场景氛围` |
| `3-明细/5-摄影美学` 已建合同，但根技能仍不知道摄影层可执行 | 根技能状态同步层 | 同步根技能中 `3-明细` 的可执行子路径说明 | 把“编号子路径升级为可执行入口”视为根入口必须回写的投影 | 根技能能正确路由到 `5-摄影美学` |
| `3-明细/6-转场特效` 已建合同，但根技能仍只知道 `2-角色表现` 与 `3-运镜手法` | 根技能状态同步层 | 同步根技能中 `3-明细` 的可执行子路径说明 | 把“关键子路径可执行状态”视为根入口必须回写的投影 | 根技能能正确路由到 `6-转场特效` |
| `5-画面` 父子合同已补齐，但根技能仍把该阶段标记为空骨架 | 根技能状态同步层 | 同步更新 `.agents/skills/aigc/SKILL.md` 中 `5-画面` 的阶段状态与子路径说明 | 把阶段合同补齐后的状态上收视为根入口必须完成的收尾动作 | 根技能能正确路由到 `分镜故事板 / 分镜帧 / 漫画` |
| `4-主体` 父子合同已补齐，但根技能仍写“已建骨架，待写实质合同” | 根技能状态同步层 | 同步 `.agents/skills/aigc/SKILL.md` 中 `4-主体` 的阶段状态 | 把“阶段升级为可执行入口”视为需要向上同步的元修复 | 根技能能正确路由到 `4-主体` 四个子路径 |
| 项目根运行时与 `.codex/state/tasks` 同时存在，但没有优先级声明 | harness 状态面层 | 明确 `projects/<项目名>/` 为 AIGC 项目 canonical runtime | 将 runtime 优先级同步写入 runbook、registry、audit 与三省合同 | 技能树、registry、runbook 对状态真源的说法一致 |
| `1-规划/2-组间/3-明细` 各自维护不同阶段目录与 episode 文件，导致编导真源分裂 | 真源治理层 | 上收统一运行时布局到 `.agents/skills/aigc/_shared/project-runtime-layout.md`，并固定 `projects/<项目名>/编导/第N集.json` 为单一根文件 | 让 `1-分集` 只负责 bootstrap，`2-组间` 只 patch 组级字段，`3-明细` 只 patch 镜级字段，所有父级合同都回指 shared layout + shared schema | 根技能、阶段技能与 shared carrier 对 `Init/1-规划/编导/4-主体/5-画面/视频/后期` 说法一致 |
| 阶段执行状态只写在根技能表格里，registry / audit 不知道 | 注册与审计层 | 将阶段状态上收至 `.codex/registry/skills.yaml`，并补 `scripts/aigc_skill_audit.py` | 把“阶段 active / shelved”视为控制面真源，而不是仅属技能文案 | 审计可识别哪些阶段可执行、哪些已搁浅 |
| `7-后期` 当前不做，但仍被视为待补执行阶段 | 阶段生命周期层 | 在根技能与 registry 中显式标记为 `搁浅` | 审计脚本对搁浅阶段跳过严格失败，但要求根技能与 registry 同步声明 | 总入口不会再把搁浅阶段误判为立即补建目标 |
| `6-视频` 已补父子合同，但根技能与控制面仍写 `shelved` | 根技能状态同步层 | 同步根技能、registry、routes 与 HARNESS 的阶段状态 | 把“阶段由搁浅转为部分可执行”视为必须向上同步的元修复 | 总入口与阶段真源对 `6-视频` 的描述一致 |
| governed leaf 已有字段表，但漏掉 `Root-Cause Execution Contract` | rollout 合同层 | 为 leaf 补齐根因上溯章节，并让严格审计继续把这项当成硬门槛 | 把“leaf 也必须有 root-cause 合同”视为 rollout 基线，而不是只要求父级技能齐全 | `scripts/aigc_skill_audit.py --strict` 不再漏报或卡在同类缺项 |

## Repair Playbook

1. 先确认 `aigc` 根目录是否已具备根 `SKILL.md` 与根 `CONTEXT.md`。
2. 先锁定主阶段链与项目工作区落点，再补阶段细节。
3. 对空合同阶段，不伪造执行规则，先在根合同里标记为“待补”。
4. 对子技能树，优先补高杠杆节点，不做一次性全量合同化。
5. 当根技能稳定后，再把阶段状态、runtime 优先级与搁浅策略同步注册进 route / audit 控制面。

## Reusable Heuristics

- 多子技能组合包最容易犯的错，是目录树长得很漂亮，但缺一个总控面；没有根合同时，阶段越多，漂移越快。
- 只要 `2-组间` 与 `3-明细` 共享同一集级事实，就不该再让两个阶段各自拥有自己的 episode 真稿；最稳的办法是让 `编导/第N集.json` 成为唯一根文件。
- 当阶段目录已经明确是 runtime 分区时，父技能最该写清的是“字段责任”和“patch 顺序”，而不是各自再定义一套集文件壳。
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
- 当某阶段明确“不在当前轮次推进”时，优先把它标成 `搁浅`，而不是继续挂着“预留中”；`搁浅` 表示有意冻结，不应被审计当作立即补全失败。
- 对跨兄弟阶段共同消费的治理工件，真源应优先放项目根；对跨兄弟阶段共同执行的运行规则，真源应优先放 `_shared/`。
- 当技能阶段名本身带序号时，不要默认把这个序号投影到项目 runtime 目录；项目目录应优先服从 `_shared/project-runtime-layout.md` 的映射。

### Case-20260410-AIGC-ROOT-RUNTIME-DIR-NONNUMERIC

- milestone_type: source_contract_change
- outcome: 将根技能的 canonical stage landing 从带号 runtime 目录收敛为 `规划 / 主体 / 画面`，同时保留技能阶段名 `1-规划 / 4-主体 / 5-画面` 不变。
- root_cause_or_design_decision: 先前根技能把阶段名和项目目录名混用，导致用户已要求去序号后，初始化和阶段合同仍持续生成旧路径。
- final_fix_or_heuristic: 根技能只负责声明“技能阶段名”，项目目录名一律回查 `_shared/project-runtime-layout.md`；路径重命名必须先改 shared mapping，再改阶段合同和项目目录。
- prevention_or_replication_checklist:
  - [x] 根 `SKILL.md` 已改为 `projects/<项目名>/规划/`、`主体/`、`画面/`
  - [x] `_shared/project-runtime-layout.md` 已写明映射规则
  - [x] `0-Init` 已改为预建无序号 runtime 目录
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/0-Init/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `projects/晴深不渝/1-规划`、`4-主体`、`5-画面` 去掉序号。

## Case Log

### Case-20260409-AIGC-ROOT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc` 建立根 `SKILL.md` 与根 `CONTEXT.md`，将原本仅有目录层级的多子技能树接入仓库级 harness。
- root_cause_or_design_decision: `aigc` 技能树虽然已经有 `1-规划`、`2-组间`、`3-明细`、`4-主体`、`5-画面`、`6-视频`、`7-后期` 的主链结构，但缺少总入口与总路由，导致它仍是“结构先行、合同缺位”的半成品。
- final_fix_or_heuristic: 先建立根技能总合同，明确项目工作区 `projects/<项目名>/`、项目根运行时工件、主阶段链、阶段覆盖状态、三省六部挂载与总验收闭环，再逐步补阶段合同与子技能合同。
- prevention_or_replication_checklist:
  - [x] 先补根 `SKILL.md`
  - [x] 先补根 `CONTEXT.md`
  - [x] 显式标注阶段覆盖状态
  - [x] 显式锁定项目工件落点
  - [x] 将空合同阶段标记为待补，而不是伪造执行链
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.codex/registry/skills.yaml`
  - `.codex/registry/routes.yaml`
- user_feedback_or_constraint: 用户要求优先补主技能总合同，把 `.agents/skills/aigc` 先真正接上 harness，再继续扩展阶段与子技能。

### Case-20260409-AIGC-INIT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/0-Init` 建立了与当前影视技能链对齐的多模式初始化合同，并将根技能中的 `0-Init` 状态从“预留中”升级为“已建合同，脚本待补”。
- root_cause_or_design_decision: 根技能已声明 `0-Init` 是主阶段链起点，但实际目录为空，导致初始化入口无法承接用户的影视项目起盘请求；同时用户要求参考 `story2026/0-Init` 的成熟机制，但问法与落盘必须改写为当前 `aigc` 系列。
- final_fix_or_heuristic: 继承“单一模式入口 + mode playbook + 主文件/伴生 handoff 分工 + 来源分层”的成熟机制，但把主文件改为 `north_star.yaml`，把伴生文件改为 `init_handoff.yaml`，把治理 runtime 统一落到项目根目录。
- prevention_or_replication_checklist:
  - [x] `0-Init` 已有主 `SKILL.md`
  - [x] `0-Init` 已有 `CONTEXT.md`
  - [x] 三个模式 `module-spec.md` 已落盘
  - [x] `north_star` 与 `init_handoff` 模板真源已建立
  - [x] 根技能阶段状态已同步
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
- user_feedback_or_constraint: 用户要求“跨项目参照 `.agents/skills/story2026/0-Init` 的成熟配置机制，同样的多模式初始化，但问题方式和落盘方式应以当前技能包系列为基础，主要输出物同样为 north_star”。

### Case-20260409-AIGC-ROOT-PLANNING-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `1-规划` 的阶段状态从“已建骨架，待写实质合同”同步更新为“已建阶段合同，子路径持续补全中”。
- root_cause_or_design_decision: `1-规划` 父级合同和子路径 `1-分集`、`3-分组` 已经具备实质执行能力，但根技能仍保留旧状态描述，形成元路由层与阶段层的真源漂移。
- final_fix_or_heuristic: 当阶段从骨架升级为可执行入口时，必须把阶段状态同步回根技能与根经验层，避免总入口继续误降级该阶段。
- prevention_or_replication_checklist:
  - [x] 根技能阶段状态已同步更新
  - [x] 根经验层已记录“阶段状态上收同步”这一类失败模式
  - [x] `1-规划` 当前可执行子路径已在根层描述中体现
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
- user_feedback_or_constraint: 用户本轮要求完善 `1-规划/subtypes/3-分组`，因此需要顺带修复由此暴露出的根技能状态漂移。

### Case-20260409-AIGC-ROOT-DIRECTING-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `2-组间` 的阶段状态同步更新为“已建阶段合同，四个子路径可执行”，并同时校正 `1-规划` 的旧覆盖描述。
- root_cause_or_design_decision: `2-组间` 父子合同已经补齐，但根技能阶段覆盖表仍保留“已建骨架，待写实质合同”的旧口径，形成根入口与阶段真源不一致。
- final_fix_or_heuristic: 当阶段从空壳升级为可执行入口时，必须把状态同步回 `aigc/SKILL.md`；根入口表是投影，不应滞后于阶段真源。
- prevention_or_replication_checklist:
  - [x] `2-组间` 状态已同步
  - [x] `1-规划` 的旧覆盖描述已一并校正
  - [x] 根入口与阶段真源一致
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
- user_feedback_or_constraint: 用户要求完善 `2-组间` 阶段合同；同步根入口状态是避免真源漂移的必要收尾。

### Case-20260409-AIGC-ROOT-SCRIPT-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `3-明细` 的阶段状态同步更新为“已建阶段合同，`2-角色表现` 父子路由已补齐，其余子路径持续补全”。
- root_cause_or_design_decision: 用户要求完善 `3-明细/subtypes/2-角色表现` 及其三个子技能，并额外声明整个 `3-明细` 系列都应转为“层层加权扩写式任务”；若根技能仍保留“已建骨架，待写实质合同”，则会形成根入口与阶段真源漂移。
- final_fix_or_heuristic: 在 `3-明细` 父级与 `2-角色表现` 父子合同落地后，立即同步更新根技能阶段覆盖表与根经验层，使 `aigc` 总入口能正确识别 `3-明细` 已具备阶段合同。
- prevention_or_replication_checklist:
  - [x] `3-明细` 状态已同步
  - [x] 根经验层已记录同类漂移模式
  - [x] 根入口与阶段真源一致
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/SKILL.md`
- user_feedback_or_constraint: 用户明确要求在补齐 `2-角色表现` 及其子技能后，再把根级与整个 `3-明细` 系列前提一起补全。

### Case-20260409-AIGC-ROOT-SCRIPT-CAMERA-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `3-明细` 的可执行子路径说明，从仅可路由 `2-角色表现`，同步扩展为可路由 `2-角色表现` 与 `3-运镜手法`。
- root_cause_or_design_decision: `3-运镜手法` 已补成可执行合同；若根入口不回写这层变化，未来根路由仍会把运镜层误当作待补目录。
- final_fix_or_heuristic: 当阶段内某个带顺序信号的关键子路径从空目录升级为可执行入口时，根技能状态表必须同步“当前可路由子路径”。
- prevention_or_replication_checklist:
  - [x] 根技能状态已同步
  - [x] 根经验层已记录“可执行子路径清单也要向上同步”
  - [x] `3-明细` 当前关键可执行入口已在根层可见
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/SKILL.md`
- user_feedback_or_constraint: 用户要求在完善 `3-运镜手法` 后，让整个 `3-明细` 系列继续按新的层层加权扩写前提运行。

### Case-20260409-AIGC-ROOT-SCRIPT-ATMOSPHERE-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `3-明细` 的可执行子路径说明，从 `2-角色表现`、`3-运镜手法`、`5-摄影美学`、`6-转场特效` 扩展为额外包含 `4-场景氛围`。
- root_cause_or_design_decision: `4-场景氛围` 已补成可执行合同；若根入口不回写这层变化，未来根路由仍会把氛围层误当作待补目录。
- final_fix_or_heuristic: 当阶段内某个带顺序信号的关键子路径从空目录升级为可执行入口时，根技能状态表必须同步“当前可路由子路径”。
- prevention_or_replication_checklist:
  - [x] 根技能状态已同步
  - [x] 根经验层已记录“可执行子路径清单也要向上同步”
  - [x] `3-明细` 当前关键可执行入口已在根层可见
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 ZEN-VOID 的 `6-氛围感` 完善当前仓 `4-场景氛围`，并强调整个 `3-明细` 系列都应以层层加权扩写为统一前提。

### Case-20260409-AIGC-ROOT-SCRIPT-CINEMATOGRAPHY-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `3-明细` 的可执行子路径说明，进一步同步扩展为可路由 `2-角色表现`、`3-运镜手法`、`5-摄影美学` 与 `6-转场特效`。
- root_cause_or_design_decision: `5-摄影美学` 已补成父子合同；若根入口不回写这层变化，未来根路由仍会把摄影层误判为待补目录。
- final_fix_or_heuristic: 当阶段内某个带顺序信号的关键子路径从空目录升级为可执行入口时，根技能状态表必须同步“当前可路由子路径”。
- prevention_or_replication_checklist:
  - [x] 根技能状态已同步
  - [x] 根经验层已记录“关键子路径升级要向上同步”
  - [x] `3-明细` 当前摄影层入口已在根层可见
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/SKILL.md`
- user_feedback_or_constraint: 用户要求完善 `5-摄影美学`，并希望整个 `3-明细` 系列继续按照新的层层加权扩写前提运行。

### Case-20260409-AIGC-ROOT-SCRIPT-TRANSITION-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `3-明细` 的可执行子路径说明，从 `2-角色表现 + 3-运镜手法`，同步扩展为包含 `6-转场特效`。
- root_cause_or_design_decision: `6-转场特效` 已补成可执行合同；若根入口不回写这层变化，未来根路由仍会把转场层误当作待补目录。
- final_fix_or_heuristic: 当阶段内某个带顺序信号的关键子路径从空目录升级为可执行入口时，根技能状态表必须同步“当前可路由子路径”，即便该子路径在默认串行链里位于后位。
- prevention_or_replication_checklist:
  - [x] 根技能状态已同步
  - [x] 根经验层已记录“可执行子路径清单也要向上同步”
  - [x] `3-明细` 当前关键可执行入口已在根层可见
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/SKILL.md`
- user_feedback_or_constraint: 用户要求在完善 `6-转场特效` 后，让整个 `3-明细` 系列继续按新的层层加权扩写前提运行。

### Case-20260409-AIGC-ROOT-STORYBOARD-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `5-画面` 的阶段状态，从“已建骨架，待写实质合同”同步更新为“已建阶段合同，`分镜故事板`、`分镜帧`、`漫画` 可路由，脚本待补”。
- root_cause_or_design_decision: 用户要求直接完善 `.agents/skills/aigc/5-画面/` 及三个子技能目录；若根技能不回写这层变化，`aigc` 总入口仍会把已可路由的阶段误判为空壳。
- final_fix_or_heuristic: 当一个阶段补齐了父级路由与核心子路径合同后，必须把该状态同步回根技能与根经验层，避免总入口继续沿用旧状态。
- prevention_or_replication_checklist:
  - [x] 根技能阶段状态已同步
  - [x] 根经验层已记录 `5-画面` 状态上收模式
  - [x] 根入口与 `5-画面` 阶段真源一致
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/5-画面/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
- user_feedback_or_constraint: 用户要求补完 `5-画面` 根级与三个子技能，并参考旧仓分镜能力重写到当前 `aigc` 系列。

### Case-20260410-AIGC-ROOT-VISUAL-STAGE-RENAME

- milestone_type: source_contract_change
- outcome: 将根技能中的阶段 `5-分镜` 口径统一重命名并重定位为 `5-画面`，并明确其职责是围绕已有文件进行多类型画面生成，而非重复上游分镜事实定义。
- root_cause_or_design_decision: 原阶段名和父级定位过于贴近“分镜任务”，会与 `3-明细/1-分镜表现` 产生边界重叠；用户要求改成更贴近图像化执行层的 `5-画面`。
- final_fix_or_heuristic: 在根技能中将阶段 landing、阶段说明与状态表同步到 `5-画面`，并把阶段职责重写为“prompt 组合 + 一致性处理 + 图像生成”。
- prevention_or_replication_checklist:
  - [x] 根技能阶段名已同步为 `5-画面`
  - [x] 根技能阶段 landing 已改为 `projects/<项目名>/画面/`
  - [x] 根经验层已记录本次更名与重定位
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/5-画面/SKILL.md`
- user_feedback_or_constraint: 用户明确确认阶段口径应为 `5-画面`。

### Case-20260410-AIGC-ROOT-VIDEO-STAGE-ACTIVATE

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `6-视频` 的阶段状态，从 `shelved` 同步升级为“父级已建、`1-提示词蒸馏/全能参照` 可执行、其余子路径待补”。
- root_cause_or_design_decision: 用户已明确要求完善 `6-视频/subtypes/1-提示词蒸馏/全能参照` 并指定上游 director JSON 与目标视频请求模板；若根入口和 registry 仍维持 `shelved`，会让总路由继续把已可执行阶段误判为 frozen。
- final_fix_or_heuristic: 当某阶段从空壳/搁浅升级为部分可执行时，必须同步更新根技能、registry、routes 与 HARNESS，不允许只补叶子子技能。
- prevention_or_replication_checklist:
  - [x] 根技能阶段状态已同步
  - [x] registry 状态已同步
  - [x] routes 已同步
  - [x] HARNESS 总览已同步
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/6-视频/SKILL.md`
  - `.codex/registry/skills.yaml`
  - `.codex/registry/routes.yaml`
  - `HARNESS.md`
- user_feedback_or_constraint: 用户要求直接完善 `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照`，而不是继续把 `6-视频` 留在纯预留状态。

### Case-20260409-AIGC-ROOT-SUBJECT-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `4-主体` 的阶段状态，从“已建骨架，待写实质合同”同步更新为“已建阶段合同，四个子路径可路由”。
- root_cause_or_design_decision: `4-主体` 父级与四个子路径合同已经补齐；若根入口不回写这一变化，未来根路由仍会把主体阶段误判为待补目录。
- final_fix_or_heuristic: 当一个阶段从空骨架升级为可执行入口时，根技能状态表必须同步写出当前可路由的子路径，而不是只写“阶段存在”。
- prevention_or_replication_checklist:
  - [x] 根技能阶段状态已同步
  - [x] 根经验层已记录同类漂移模式
  - [x] `4-主体` 当前四个子路径已在根层可见
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/4-主体/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `ZEN-VOID` 的设定阶段，完善当前仓 `4-主体` 下四个子技能；根入口状态同步是避免真源漂移的必要收尾。

### Case-20260409-AIGC-HARNESS-ALIGNMENT

- milestone_type: source_contract_change
- outcome: 将 `aigc` 技能树的 runtime 真源、阶段注册状态、搁浅阶段策略与 harness 控制面重新对齐；新增 `scripts/aigc_skill_audit.py`。
- root_cause_or_design_decision: 技能树内容已大幅完善，但项目级运行时真源尚未完整上收进 runbook / registry / audit，控制面仍残留 `.codex/state/tasks/` 默认视角，且 `6-视频 / 7-后期` 没有被显式声明为搁浅。
- final_fix_or_heuristic: 对 AIGC 项目型工作流，先把 `projects/<项目名>/` 升为 canonical runtime，再把阶段 `active / shelved` 状态上收进 registry，并让审计脚本读取这些控制面声明，而不是只看技能正文。
- prevention_or_replication_checklist:
  - [x] runbook 已声明 `projects/<项目名>/` 为 AIGC 项目 canonical runtime
  - [x] registry 已注册 `aigc` 阶段状态与 runtime control
  - [x] `6-视频 / 7-后期` 已标记为 `搁浅`
  - [x] 已新增 `scripts/aigc_skill_audit.py`
  - [x] harness audit 已检查 runtime / shelved / skill audit 锚点
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.codex/registry/skills.yaml`
  - `.codex/registry/routes.yaml`
  - `.codex/runbooks/task-lifecycle.md`
  - `scripts/aigc_skill_audit.py`
  - `scripts/aigc_harness_audit.py`
- user_feedback_or_constraint: 用户先要求把注册面与审计面修成完全版，并明确 `6-视频 / 7-后期` 当前先搁浅。

### Case-20260409-AIGC-PROJECT-ROOT-RUNTIME

- milestone_type: source_contract_change
- outcome: 将 `aigc` 根技能、`0-Init`、registry、state README、三省治理合同与审计说明中的项目运行时真源统一收口到 `projects/<项目名>/`，移除隐藏运行时子目录作为第二真源的口径。
- root_cause_or_design_decision: 先前把隐藏运行时子目录当作项目运行时目录，会把“项目根目录”与“隐藏运行时目录”并列成双真源；用户随后明确裁决不需要这层目录，项目根目录本身就是运行时真源。
- final_fix_or_heuristic: 对 AIGC 项目型工作流，优先把 `projects/<项目名>/` 设计成唯一运行时真源，再把 `project_state / mandate / mission-brief / route-plan / preflight-verdict / validation-report / learning-record` 直接落到项目根，而不是再包一层隐藏目录。
- prevention_or_replication_checklist:
  - [x] 根技能已移除隐藏运行时子目录口径
  - [x] `0-Init` 已改写为项目根落盘
  - [x] registry / routes / state README 已同步
  - [x] 三省治理文档与 eval 说明已同步
  - [x] 审计脚本报错文案已改成 project-root runtime
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.codex/registry/skills.yaml`
  - `.codex/registry/routes.yaml`
  - `.codex/state/tasks/README.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确裁决：`projects/<项目名>/` 才是对的，不需要额外隐藏运行时目录。

### Case-20260409-AIGC-LEAF-ROLLOUT-CLOSURE

- milestone_type: source_contract_change
- outcome: 为 `3-明细/2-角色表现` 与 `3-明细/5-摄影美学` 下 6 个 governed leaf 补齐 `Root-Cause Execution Contract`，并让 `scripts/aigc_skill_audit.py` 对 `shelved` 阶段跳过 leaf 级严格失败。
- root_cause_or_design_decision: 严格审计暴露出两个控制面缺口：一是多个 leaf 虽已具备字段表和 pass table，但缺少根因上溯合同；二是审计脚本虽已识别 `6-视频 / 7-后期` 为 `shelved`，却仍在全树扫描时把其空壳 `SKILL.md` 计为失败。
- final_fix_or_heuristic: 对 governed leaf，`Root-Cause Execution Contract` 不是可选润色，而是 rollout 基线；对已注册为 `shelved` 的阶段，严格审计应验证“是否显式搁浅”，而不是继续按活跃技能合同逐项卡死。
- prevention_or_replication_checklist:
  - [x] 6 个 active leaf 已补齐 `Root-Cause Execution Contract`
  - [x] `scripts/aigc_skill_audit.py` 已跳过 `shelved` 阶段子树的 leaf 级严格失败
  - [x] `python3 scripts/aigc_skill_audit.py --strict` 已通过
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/对手戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/光影设计/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/色彩设计/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/摄影参数/SKILL.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户本轮先纠正运行时真源，随后严格审计继续暴露 rollout 缺口，因此顺手收口到“project-root runtime + governed leaf rollout 完整”这一版。

### Case-20260409-AIGC-ROOT-COUNCIL-RUNTIME

- milestone_type: source_contract_change
- outcome: 将 `team.yaml` 提升为项目根团队真源，并在 `aigc` 根技能中新增 `_shared/council-runtime/` 共享运行时入口。
- root_cause_or_design_decision: 用户要求 `1-规划 / 2-组间 / 3-明细 / 4-主体` 在进入阶段根技能或叶子技能时都先读取同一份 `team.yaml`，若继续把顾问团规则散落在各阶段，将很快形成平行真相。
- final_fix_or_heuristic: 对跨兄弟阶段共同消费的团队工件，真源应上收至项目根；对跨兄弟阶段共同执行的顾问团规则，真源应上收至 `_shared/council-runtime/`。
- prevention_or_replication_checklist:
  - [x] 项目根 `team.yaml` 已写入根技能工件落点
  - [x] `_shared/council-runtime/` 已作为共享运行时入口接入
  - [x] 根技能已要求四个创作阶段进入前先判定顾问团运行时
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- user_feedback_or_constraint: 用户明确要求后续四个创作阶段及其叶子技能都默认读取 `projects/<项目名>/team.yaml`，并按角色职责启用智能顾问团 subagents。

### Case-20260410-AIGC-RUNTIME-LAYOUT-UNIFICATION

- milestone_type: source_contract_change
- outcome: 将 `aigc` 全树的项目运行时布局收敛为 `Init / 1-规划 / 编导 / 4-主体 / 5-画面 / 视频 / 后期` 七个 canonical runtime roots，并固定 `projects/<项目名>/编导/第N集.json` 为 `1-规划 -> 2-组间 -> 3-明细` 的单一编导根文件。
- root_cause_or_design_decision: 用户明确要求后续 harness 工程化重构要围绕“统一根文件 + 不同字段定向输出”推进；直接技术原因是原有 `1-规划/2-组间/3-明细` 各自落盘到阶段目录，会形成多个 episode 真相与重复上下文加载。
- final_fix_or_heuristic: 将共享运行时布局上收至 `.agents/skills/aigc/_shared/project-runtime-layout.md`，由 `1-分集` 先创建空的 bootstrap JSON，由 `2-组间` patch 组级字段，由 `3-明细` patch 镜级字段，并让父级合同和输出契约统一回指 shared layout + shared schema。
- prevention_or_replication_checklist:
  - [x] shared runtime layout 已建立
  - [x] shared bootstrap template 已建立
  - [x] root `aigc/SKILL.md` 已同步新目录结构
  - [x] `1-分集 / 2-组间 / 3-明细` 已同步单一根文件责任链
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“2组和3组都将围绕一个统一根文件（确定为 json）进行不同字段分属下的定向输出”，并要求初始化阶段可预落整套目录结构。

### Case-20260410-AIGC-RUNTIME-MAPPING-RECONCILIATION

- milestone_type: source_contract_change
- outcome: 将 shared runtime layout、根技能、`1-规划`、`0-Init`、顾问团 checkpoint 与 `6-视频` 输入合同统一到同一套 runtime mapping：`Init / 1-规划 / 编导 / 4-主体 / 5-画面 / 视频 / 后期`。
- root_cause_or_design_decision: 直接技术原因不是“没有 runtime layout”，而是 shared layout 与阶段合同分别演化出了 `设定/画面`、`Init/1-规划` 两套并行口径；更高层根因是审计脚本只检查壳体与注册关系，没有检查 runtime mapping 一致性。
- final_fix_or_heuristic: runtime 命名一旦被 shared layout 宣布，就必须被根技能、阶段合同、顾问团 validation checkpoint 与审计器共同消费；其中 `1-分集` 的 `Init/` bootstrap 属于例外型子路径，而不是 `1-规划` 整阶段的父级根目录。
- prevention_or_replication_checklist:
  - [x] shared runtime layout 已改为单一 authoritative mapping
  - [x] 根技能 stage landing 已同步
  - [x] `1-规划` 已改为 `1-规划/validation-report.md` 作为阶段验收根
  - [x] `0-Init` 预建目录已同步
  - [x] council runtime checkpoint 已与阶段 runtime 对齐
  - [x] 审计脚本已新增 runtime consistency checks
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
  - `.agents/skills/aigc/6-视频/references/execution-flow.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户要求直接继续做 P0/P1：统一 runtime 真源口径，并把审计器补上。

### Case-20260410-AIGC-ROOT-VIDEO-FIRST-FRAME-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将根技能 `.agents/skills/aigc/SKILL.md` 中 `6-视频` 的阶段状态，从“仅 `全能参照` 可执行”同步更新为“`全能参照` 与 `首帧参照` 均可执行”。
- root_cause_or_design_decision: `6-视频/subtypes/1-提示词蒸馏/首帧参照` 已被补成可执行叶子技能；若根入口仍沿用旧口径，会让总路由继续把帧级视频请求误判为待补槽位。
- final_fix_or_heuristic: 当阶段内新增一个已验证的可执行叶子子技能时，根技能覆盖表必须同步扩展“可路由子路径”清单，而不是只更新阶段局部合同。
- prevention_or_replication_checklist:
  - [x] 根技能 `6-视频` 状态已同步更新
  - [x] 根经验层已记录该类“叶子升级需向上同步”的模式
  - [x] `6-视频` 当前两个可执行入口已在根层可见
- evidence_paths:
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - `.agents/skills/aigc/6-视频/SKILL.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/首帧参照/SKILL.md`
- user_feedback_or_constraint: 用户明确要求完善 `6-视频/subtypes/1-提示词蒸馏/首帧参照`，因此根级入口也需要同步把该叶子路径标成可执行。
