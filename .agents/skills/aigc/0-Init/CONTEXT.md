# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/0-Init` 的经验层知识库，不是进度日志。
- 调用 `.agents/skills/aigc/0-Init/SKILL.md` 时，应自动预加载本文件。
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
| 多模式初始化被写成重复问卷 | 模式合同层 | 把元选项收口到 `Initialization Mode Contract` 单一入口 | 所有模式细则都拆到 `references/*/module-spec.md`，模式锁定后只读一份 | 全文只有一个合法模式展示位 |
| `north_star` 与 handoff 混成一个大杂烩 | 主文件分工层 | 将长期约束留在 `north_star.yaml`，阶段种子与 unknowns 放入 `init_handoff.yaml` | 用模板真源固定两份文件的字段边界 | 模板与最终落盘能看出清晰分工 |
| 顾问团只有共享名单，没有角色职责真源 | 团队治理层 | 新增项目根 `team.yaml`，把顾问写成 `策划 / 监制 / 评审` 三角色而非平铺列表 | 用 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 固化角色、作用阶段与评审最终闸门 | 后续阶段能按角色读取顾问团队，而不是回猜 |
| 顾问团真源被挂在 `0-Init/` 下，后续阶段消费不稳定 | 真源治理层 | 将 `team.yaml` 提升到 `projects/<项目名>/team.yaml` | 把顾问团 schema 从初始化私有工件升级为项目级治理工件 | `1-规划 / 2-组间 / 3-明细 / 4-主体` 都直接读取项目根 team |
| 问题方式仍沿用小说字段 | 领域适配层 | 按 `规划/编导/脚本/主体/分镜/视频/后期` 组织提问与路由 | 在 `SKILL.md` 固化 `Question Framing Contract` | 初始化问题能映射当前影视阶段链 |
| 工件落盘仍漂向外仓或旧路径 | 路径合同层 | 固定到 `projects/<项目名>/Init/` 与项目根 | 在根 `aigc` 与 `0-Init` 双层合同中同时声明 canonical landing | 全部初始化工件都位于当前仓库项目路径 |
| 设计完成但没有可复用真源模板 | 真源治理层 | 新增 `templates/north-star.template.yaml` 与 `templates/init-handoff.template.yaml` | 后续脚本与文档都引用模板，而不是各写一份 schema | 未来实现不会再出现多份字段定义 |
| 是否允许分组后节奏治理只留在口头层 | 上游决策层 | 在 `north_star` 与 `init_handoff` 同时写入 `original_adherence` 与重排授权 | 在 `0-Init` 固化布尔门与节奏 seed 规则 | `1-规划/4-节奏` 能直接判断是否执行 |

## Repair Playbook

1. 先确认问题属于模式路由、问题设计、主文件分工、团队治理还是落盘漂移。
2. 优先回到 `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`North Star Contract` 与 `Team Manifest Contract`。
3. 若顾问团问题表现为“只有名单没有职责”，先修 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`。
4. 若问题是“后续阶段不知道去哪读团队真源”，先把 `team.yaml` 提升回项目根。
5. 若是字段边界问题，先修模板真源。
6. 若是路径问题，先回查根 `aigc/SKILL.md` 与本阶段 `Canonical Landing`。
7. 只有源层合同稳定后，才修本次具体输出。

## Reusable Heuristics

- 对当前 `aigc` 技能树来说，`0-Init` 最重要的不是“问得多”，而是“把 north star 与阶段入口种子分干净”。
- 影视初始化最容易过度下潜到主体或分镜细节；凡是会在下游阶段形成 canonical 的内容，都只应在这里保留 seed。
- 只要要支持多模式初始化，就必须先有唯一模式入口，再有 mode-specific module spec，否则很快退化成重复文案。
- 当前仓库的初始化落点必须优先服从 `projects/<项目名>/`，而不是借用其他项目系的 state/layout。
- 初始化阶段如果已经知道后续 runtime 分区，就应优先把 `Init / 1-规划 / 编导 / 4-主体 / 5-画面 / 视频 / 后期` 七个根目录一次性预落，而不是等下游阶段再各自补目录。
- 对顾问团型初始化，只有 `shared_agents` 还不够；必须把顾问转换成可被下游读取的角色团队，否则 `1-规划 / 2-组间 / 3-明细 / 4-主体` 无法知道谁该在哪个闸门发言。
- 若 `评审` 要覆盖多个阶段，最稳的表达不是“全程参与”，而是把它固定到各阶段根级 `validation-report.md` 的最终验收闸门。
- 只要某工件会被多个兄弟阶段长期共同消费，就不该继续挂在 `0-Init/` 名下；最稳的做法是提升到项目根。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 当快速模式只收到一个“角色/意象对撞”的最小概念时，优先把项目先定为概念短片或概念预告级规模，并把片长、平台、现实映射强度等高分叉问题放进 `unknowns`，比在初始化阶段硬拍长篇结构更稳。
- 只要用户没有明确要求“贴原作/保原顺序/保留原作节奏”，`original_adherence` 就应显式落盘为 `false`；否则后续 `1-规划/4-节奏` 会因为缺门信息而只能猜。

## Case Log

### Case-20260409-AIGC-INIT-MULTI-MODE

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/0-Init` 建立了基于当前影视技能链的多模式初始化合同，并以 `north_star.yaml` 作为主输出物。
- root_cause_or_design_decision: 当前 `aigc` 根技能已经明确 `0-Init` 是阶段链起点，但该目录为空，导致初始化仍停留在“预留位”状态；同时用户要求参考 `story2026/0-Init` 的成熟配置机制，但问法与落盘必须回到当前影视技能包体系。
- final_fix_or_heuristic: 抽取 `story2026` 的成熟机制为“单一模式入口 + mode module specs + 主文件/伴生 handoff 分工 + 来源分层 + 模板真源”，再改写为影视向的 `north_star + stage_entry_seeds + 项目根 runtime` 合同。
- prevention_or_replication_checklist:
  - [x] 只保留一个模式展示位
  - [x] 已拆出三个模式 `module-spec.md`
  - [x] 已建立 `north_star` 与 `init_handoff` 模板真源
  - [x] 已把问题方式改写为当前影视阶段体系
  - [x] 已把落盘路径改写为 `projects/<项目名>/Init/` 与项目根
- evidence_paths:
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/CONTEXT.md`
  - `.agents/skills/aigc/0-Init/references/advisor-council-mode/module-spec.md`
  - `.agents/skills/aigc/0-Init/references/fast-mode/module-spec.md`
  - `.agents/skills/aigc/0-Init/references/autonomous-mode/module-spec.md`
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
- user_feedback_or_constraint: 用户要求“跨项目参照 `.agents/skills/story2026/0-Init` 的成熟配置机制，同样多模式初始化，但问题方式和落盘方式应以当前技能包系列为基础，主要输出物同样为 north_star”。

### Case-20260409-AIGC-INIT-TEAM-MANIFEST

- milestone_type: source_contract_change
- outcome: 将 `aigc/0-Init` 的主创会诊模式从“顾问路径列表”升级为 `team.yaml` 顾问团队真源，并固化 `策划 / 监制 / 评审` 三角色的默认作用矩阵。
- root_cause_or_design_decision: 现有合同只有 `advisor_setup.shared_agents / stage_agents`，能表达“有人参与初始化”，但不能表达“谁作用于哪个阶段、评审在哪个最终闸门介入”，导致后续阶段只能看到平铺顾问名单，无法稳定消费团队治理信息。
- final_fix_or_heuristic: 参照 `story2026/0-Init` 的 team 机制，引入 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`、`projects/<项目名>/team.yaml` 与 `team_ref`，并在主合同与顾问团子模块中固定 `策划 -> 1-规划 / 4-主体`、`监制 -> 2-组间 / 3-明细`、`评审 -> 1-规划 / 2-组间 / 3-明细 / 4-主体` 的最终验收闸门。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已新增 `Team Manifest Contract`
  - [x] `advisor-council-mode/module-spec.md` 已改为角色化写回
  - [x] 共享 `team.template.yaml` 已建立
  - [x] `init-handoff.template.yaml` 只用 `team_ref` 回指团队真源
  - [x] 已明确 `评审` 只作用于各阶段最终验收闸门
- evidence_paths:
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/CONTEXT.md`
  - `.agents/skills/aigc/0-Init/references/advisor-council-mode/module-spec.md`
  - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
- user_feedback_or_constraint: 用户明确要求复用 `story2026/0-Init` 的顾问团机制，并把职责改写为 `策划 / 监制 / 评审` 三角色，其中评审作用于 `1-规划 / 2-组间 / 3-明细 / 4-主体` 各自的最终阶段。

### Case-20260409-AIGC-INIT-TEAM-ROOT-PROMOTION

- milestone_type: repeated_pattern_promotion
- outcome: 将 `team.yaml` 从 `0-Init/` 子目录提升为 `projects/<项目名>/team.yaml` 项目级治理工件，并把模板真源上收至 `aigc/_shared/council-runtime/`。
- root_cause_or_design_decision: `team.yaml` 会被 `1-规划 / 2-组间 / 3-明细 / 4-主体` 长期共同消费，若继续挂在 `0-Init/` 下，后续阶段就会把“初始化产物”误当成“项目治理真源”，形成路径与归属混层。
- final_fix_or_heuristic: 对跨兄弟阶段共同消费的治理工件，应提升到项目根；对跨阶段共同执行的运行机制，应提升到 `aigc/_shared/`，避免阶段各自复制一套。
- prevention_or_replication_checklist:
  - [x] `team.yaml` 已提升到项目根
  - [x] `init_handoff` 改为 `team_ref: "team.yaml"`
  - [x] `0-Init` 已改为读取共享模板真源
  - [x] `advisor-council-mode` 已改为写回项目根
- evidence_paths:
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/CONTEXT.md`
  - `.agents/skills/aigc/0-Init/references/advisor-council-mode/module-spec.md`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
  - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- user_feedback_or_constraint: 用户明确要求后续多个兄弟阶段都默认读取同一份 `team.yaml`，因此需要先完成真源提升，而不是继续把团队工件留在初始化目录内。

### Case-20260409-AIGC-INIT-FAST-MINIMAL-BRIEF

- milestone_type: new_success_class
- outcome: 在 `快速成案模式` 下，仅凭一句“波斯猫大战白头鹰”的最小 brief，为新项目成功落出完整 `0-Init` 起盘包，并把高分叉问题保留给后续阶段。
- root_cause_or_design_decision: 当用户只给出“角色/意象对撞”级概念时，若在初始化阶段强拍世界观、片长或现实立场，最容易让 `north_star` 失真；更稳的做法是把项目先定义为概念短片级起盘，并将高分叉决策留在 `unknowns`。
- final_fix_or_heuristic: 对单句对抗型概念，快速模式应优先补齐 `north_star` 的长期冲突约束与 `init_handoff` 的阶段 seeds，同时把平台、片长、政治映射强度等不确定项延后到 `1-规划`。
- prevention_or_replication_checklist:
  - [x] 未回流成长问卷
  - [x] `user_confirmed` 与 `assistant_inferred` 已分层
  - [x] `unknowns` 已保留高分叉问题
  - [x] 唯一推荐下一阶段为 `1-规划`
- evidence_paths:
  - `projects/测试1/Init/north_star.yaml`
  - `projects/测试1/Init/init_handoff.yaml`
  - `projects/测试1/validation-report.md`
- user_feedback_or_constraint: 用户选择 `快速成案模式`，并只提供一句项目概念“波斯猫大战白头鹰”。

### Case-20260409-AIGC-INIT-ADAPTATION-PACING-GATE

- milestone_type: source_contract_change
- outcome: 为 `0-Init` 新增 `original_adherence` 与剧本节奏相关字段，并把其升级为 `1-规划/4-节奏` 的上游执行门。
- root_cause_or_design_decision: 若“是否贴原作、是否允许节奏重排”只停留在对话层，规划阶段就无法稳定判断分组后该不该进入独立节奏子路径，导致同类项目执行口径漂移。
- final_fix_or_heuristic: 在 `north_star.yaml` 固化长期 `adaptation_strategy`，在 `init_handoff.yaml` 固化 `directing_seed.original_adherence + reorder_authorization + pacing_focus`，并明确默认 `original_adherence: false`。
- prevention_or_replication_checklist:
  - [x] `north_star` 已新增 `adaptation_strategy`
  - [x] `init_handoff` 已新增 `directing_seed.original_adherence`
  - [x] `0-Init/SKILL.md` 已新增节奏 seed 合同
  - [x] `1-规划` 已可直接消费该布尔门
- evidence_paths:
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/SKILL.md`
- user_feedback_or_constraint: 用户要求“在未强调原作遵循的情况下”允许分组后独立节奏规划，并明确由相关 YAML 字段决定执行与否。

### Case-20260410-AIGC-INIT-RUNTIME-ROOT-PRECREATE

- milestone_type: source_contract_change
- outcome: 将 `0-Init` 的 canonical landing 从 `projects/<项目名>/0-Init/` 统一改为 `projects/<项目名>/Init/`，并允许初始化阶段一次性预创建 `1-规划 / 编导 / 4-主体 / 5-画面 / 视频 / 后期` 等项目运行时根目录。
- root_cause_or_design_decision: 用户明确要求整套项目目录结构“甚至可以一开始就在初始化中落盘”；若初始化仍只把自己视为 `0-Init/` 私有目录，就无法承担后续 harness 的项目运行时脚手架职责。
- final_fix_or_heuristic: 在 `0-Init` 父级合同和模板回指中同步改为 `Init/`，并把 runtime 目录真源上收至 `.agents/skills/aigc/_shared/project-runtime-layout.md`，由初始化阶段负责预落目录骨架。
- prevention_or_replication_checklist:
  - [x] `0-Init/SKILL.md` 已改为 `Init/`
  - [x] `init-handoff.template.yaml` 已回指 shared runtime layout
  - [x] `0-Init` 经验层已记录预落目录策略
  - [x] 后续规划/编导阶段已消费该布局
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/0-Init/SKILL.md`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
  - `.agents/skills/aigc/1-规划/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“以上目录结构甚至可以一开始就在初始化中落盘”。
