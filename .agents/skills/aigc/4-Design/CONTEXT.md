# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design` 的经验层知识库，不是过程日志。
- 调用本阶段父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `4-Design` 仍是空目录，根入口却把它当成已建阶段 | 阶段父级合同层 | 补齐父级 `SKILL.md + CONTEXT.md`，至少声明 active 子路径和边界 | 将“阶段已建”定义为必须存在本地合同，而不是只有目录 | 根入口与阶段真实状态一致 |
| design 阶段直接吞上游全部导演字段，不做对象池收敛 | 输出治理层 | 先进入清单子路径，把对象清单稳定落盘 | 固化“先清单、再设计、再面板”的阶段顺序 | 角色/场景/道具都有 design-source 层 |
| 道具链停在 `prop_design_bridge.json`，没有 design synthesis 真源 | 叶子治理层 | 补齐 `4-道具/2-设计` 父 skill、shared I/O、team 与 prompt sidecar | 把道具链固定为 `清单 -> bridge -> design master -> prompt sidecar` | 下游不再临时拼 prompt |
| 场景链只有对象池、没有 design synthesis 真源 | 叶子治理层 | 补齐 `1-场景` 家族父级与 `1-场景/2-设计` | 把场景链固定为 `清单 -> 设计 -> 面板` | 场景清单不再悬空 |
| 场景链已有 design synthesis，但 `panel_handoff` 没有实际消费入口 | 下游承接层 | 补齐 `1-场景/3-面板` 叶子技能 | 在阶段父级显式登记 scene panel 为 active 入口 | 场景链真正形成 `清单 -> 设计 -> 面板` 闭环 |
| 角色链停在 `1-清单`，没有 design synthesis 真源 | 叶子治理层 | 补齐 `2-角色/2-设计` 父 skill、shared I/O、team 与角色设计 carrier | 把角色链固定为 `清单 -> 设计 -> 面板/生图` | 角色设计不再依赖临时拼接 |
| 服装链只有空目录，没有独立 design-source / design / panel 真源 | 类目治理层 | 建立 `3-服装` 父级与 `1-清单 / 2-设计 / 3-面板` 三段 active 入口 | 把服装链固定为 `角色清单 -> 服装清单 -> 设计 -> 面板` | 服装链不再挤在角色设计的局部字段里 |
| 输出路径继续漂到旧仓或 `主体/` 旧口径 | 路径真源层 | 当前先统一落到 `projects/<项目名>/4-Design/` | 在阶段父级合同中固定当前 buildout 目标路径 | 产物路径可预测 |
| 父级路由状态陈旧，仍把已落地子路径写成 pending | 路由状态层 | 同步更新 `4-Design/SKILL.md` 的 active/pending 列表 | 每新增一个 active 子路径，就同步更新阶段父级状态与路由图 | 父级合同与真实可执行入口一致 |
| 新增 panel leaf 后父级仍缺少 panel route 说明 | 阶段路由层 | 在 `Execution Summary` 中补写 panel packet 入口与回接口径 | 对每个新增 panel leaf 同步更新阶段父级摘要与 case log | 用户能从父级直接进入正确 panel 入口 |
| 道具链只有 design master，没有 panel dossier handoff | 叶子治理层 | 建立 `4-道具/3-面板` 叶子技能并回接阶段父级路由 | 让 `4-Design` 的 prop 家族形成 `清单 -> 设计 -> 面板` 真正闭环 | `4-Design/SKILL.md` 能正确路由到 prop panel |

## Repair Playbook

1. 先查上游 `3-Detail/第N集.json` 是否存在且符合 shared schema。
2. 再查当前任务属于角色、场景、服装还是道具。
3. 若只需要建立对象池，优先进入对应 `1-清单`。
4. 若叶子合同未补齐，停止在父级并报告缺口。

## Reusable Heuristics

- `4-Design` 的首要价值不是立即出设计图，而是把导演事实收敛成可复用的 design-source 对象池。
- 阶段父级一旦从空骨架升级为可用入口，就应显式列出当前 active 子路径，避免用户被过时状态误导到 pending 分支。
- 当类目父级已经存在且叶子技能已落地时，阶段父级应路由到“类目父级 -> active 叶子”，而不是继续把该类目写成空目录。
- 对道具链来说，`bridge` 不是最终交付；最稳的落点是把稳定设计事实写进 canonical JSON，把 prompt 下放 sidecar。
- 对场景链来说，`1-清单` 和 `2-设计` 必须一起出现才算闭环；只有对象池没有设计接手合同，仍不算可执行。
- 对场景链来说，`2-设计` 出现后如果 `panel_handoff` 已稳定，就应继续补齐 `3-面板`；否则会在 design 阶段留下悬空的下游合同。
- 对服装链来说，最稳的 canonical source 不是再扫一遍导演 JSON，而是消费 `2-角色/1-清单/角色清单.json` 里已经锁定的穿搭事实，再独立沉淀服装真源。

## Case Log

### Case-20260412-AIGC-4-DESIGN-STAGE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为空置的 `.agents/skills/aigc/4-Design` 补齐了父级阶段合同，并锁定首个 active 入口为 `2-角色/1-清单`。
- root_cause_or_design_decision: 根技能与 registry 已把 `4-Design` 标成 active stage，但本地阶段目录仍是空骨架，导致阶段路由链断裂。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md` 锁边界与路径，再把执行能力落到最小可闭环的角色清单叶子技能。
- prevention_or_replication_checklist:
  - [x] 父级合同已存在
  - [x] active 子路径已显式声明
  - [x] 经验层已记录本轮 buildout 口径
- evidence_paths:
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/4-Design/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求完善 `.agents/skills/aigc/4-Design/角色/1-清单`，并以前代参考技能为基底。

### Case-20260412-AIGC-4-DESIGN-ROUTE-SYNC

- milestone_type: source_contract_change
- outcome: 在道具清单叶子落地后，同步修正了 `4-Design` 父级的 active 路由状态，并补齐 `4-道具` 类目父级合同。
- root_cause_or_design_decision: 若只补叶子技能、不同步父级状态，执行者仍会看到过时的 pending 描述，造成“源层已实现、父级仍宣称未实现”的第二真源。
- final_fix_or_heuristic: 每新增一个 active leaf，都同步更新阶段父级的路由图、active/pending 列表和类目父级合同，避免父级状态漂移。
- prevention_or_replication_checklist:
  - [x] `4-道具/SKILL.md + CONTEXT.md` 已落地
  - [x] `4-Design/SKILL.md` 已同步 active 路由状态
  - [x] `4-Design/CONTEXT.md` 已记录状态同步 heuristic
- evidence_paths:
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/4-Design/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/道具/SKILL.md`
  - `.agents/skills/aigc/4-Design/道具/CONTEXT.md`
- user_feedback_or_constraint: 用户在道具叶子技能落地后要求继续“补”父级合同与路由层。

### Case-20260412-AIGC-4-DESIGN-SCENE-DESIGN-UPGRADE

- milestone_type: source_contract_change
- outcome: 为 `4-Design` 阶段补上了 `1-场景` 类目父级与 `1-场景/2-设计` 子技能，使场景链从对象池延伸到设计稿收束。
- root_cause_or_design_decision: 阶段父级虽然能把任务路由到场景方向，但场景类目此前只有 `1-清单` 和空目录，导致对象池之后没有稳定接手合同。
- final_fix_or_heuristic: 让 `1-场景` 成为类目路由真源，再把 `2-设计` 升级为知行合一单技能场景设计真源。
- prevention_or_replication_checklist:
  - [x] `1-场景` 父级合同已补齐
  - [x] `2-设计` 已具备 SKILL / CONTEXT / CHANGELOG / openai.yaml
  - [x] `2-设计` 已承担场景设计唯一执行真源
- evidence_paths:
  - `.agents/skills/aigc/4-Design/场景/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
- user_feedback_or_constraint: 用户先前要求补齐 `1-场景/2-设计`，随后进一步要求按 `skill-知行合一` 对其做系统性重构，并废弃旧场景设计组 agent。

### Case-20260412-AIGC-4-DESIGN-ROLE-DESIGN-ACTIVE

- milestone_type: source_contract_change
- outcome: 将 `4-Design` 阶段中的 `2-角色/2-设计` 从预留入口升级为 active 子路径。
- root_cause_or_design_decision: 角色链已经有了 `1-清单`，但没有与之衔接的 `2-设计` 父 skill 和 team contract，导致“先清单、再设计”的阶段顺序在进入设计时失效。
- final_fix_or_heuristic: 同步补齐 `2-设计` 父 skill、shared I/O、templates、openai metadata 与角色设计组 team，并把阶段父级状态更新为 active。
- prevention_or_replication_checklist:
  - [x] `4-Design/SKILL.md` 已同步 active 状态
  - [x] `2-设计` 真源已落盘
  - [x] 角色设计组 team 已落盘
- evidence_paths:
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/4-Design/角色/2-设计/SKILL.md`
  - `.codex/agents/aigc/设计组/角色设计/team.md`
- user_feedback_or_constraint: 用户要求系统性重构 `4-Design/角色/2-设计`，并明确 subagents 负责思考与 plan，父 skill 统筹输入输出。

### Case-20260412-AIGC-4-DESIGN-RUNTIME-CANONICALIZED

- milestone_type: source_contract_change
- outcome: 将 `4-Design` 的父级合同从“本地先用 `4-Design/`”正式提升为 shared runtime 的 design 阶段唯一 canonical 目录，并同步回链 query/review/council-runtime。
- root_cause_or_design_decision: 父级合同和叶子技能已经稳定落到 `projects/<项目名>/4-Design/`，但 shared runtime 与治理消费方仍沿用 `主体/` 旧口径，导致 design 阶段出现双真源。
- final_fix_or_heuristic: 把 `.agents/skills/aigc/_shared/project-runtime-layout.md` 明确改成 `4-Design/`，并让 query/review/council-runtime/5-Image/6-Video 全部回指这一个 runtime。
- prevention_or_replication_checklist:
  - [x] shared runtime 已将 design 阶段固定为 `projects/<项目名>/4-Design/`
  - [x] query/review/council-runtime 已回链同一路径
  - [x] 本地 `CONTEXT.md` 已记录这次 canonicalization
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/query/SKILL.md`
  - `.agents/skills/aigc/review/SKILL.md`
- user_feedback_or_constraint: 用户在场景清单落地后明确要求“继续把 `4-Design` 父级与 shared runtime 一并收口”。

### Case-20260412-AIGC-4-DESIGN-ROLE-PANEL-ROUTE-SYNC

- milestone_type: source_contract_change
- outcome: 在 `2-角色/3-面板` 落地后，同步刷新了 `4-Design` 父级中的 active route、execution summary 与 panel packet 回接口径。
- root_cause_or_design_decision: 若只补叶子技能、不刷新阶段父级，执行者仍会看到“角色链止于 `2-设计` 或仍 pending”的过时描述，形成新的路由漂移。
- final_fix_or_heuristic: 每落地一个新的 panel leaf，都要把它同步写进阶段父级的 active 列表、执行摘要和经验层 case log。
- prevention_or_replication_checklist:
  - [x] `4-Design/SKILL.md` 已纳入 `2-角色/3-面板`
  - [x] `4-Design/CONTEXT.md` 已记录 panel route sync 经验
  - [x] `2-角色` 父级状态已同步为 active
- evidence_paths:
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/4-Design/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/角色/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/角色/SKILL.md`
- user_feedback_or_constraint: 用户要求补齐当前仓的角色面板技能，而不是只保留参考仓能力。

### Case-20260412-AIGC-4-DESIGN-SCENE-PANEL-UPGRADE

- milestone_type: source_contract_change
- outcome: 为 `4-Design` 阶段补上了 `1-场景/3-面板` 的 active 入口，并让 `4-Design` 父级从“场景设计停在 carrier”升级为“场景设计可继续收束到 panel carrier”。
- root_cause_or_design_decision: `1-场景/2-设计` 已经输出 `panel_handoff`，但 `4-Design/SKILL.md` 仍只把 scene panel 视作未来保留槽位，形成路由层与叶子需求的错位。
- final_fix_or_heuristic: 当某个类目下游已经在上游合同中被显式预留为稳定 handoff 时，阶段父级应同步把对应叶子入口的 active/pending 状态更新为真实状态，避免第二真源。
- prevention_or_replication_checklist:
  - [x] `1-场景/3-面板` 已建立 skill package
  - [x] `4-Design/SKILL.md` 已新增 scene panel active 路由
  - [x] `4-Design/CONTEXT.md` 已记录这次状态同步经验
- evidence_paths:
  - `.agents/skills/aigc/4-Design/场景/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/SKILL.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
- user_feedback_or_constraint: 用户明确要求完善当前仓的场景面板技能，而不是只保留目录占位。

### Case-20260412-AIGC-4-DESIGN-PROP-PANEL-ROUTE-SYNC

- milestone_type: source_contract_change
- outcome: 将 `4-Design` 父级路由状态同步到 `4-道具/3-面板`，使 prop 家族的 active 链路从 `1-清单 / 2-设计` 扩展为 `1-清单 / 2-设计 / 3-面板`。
- root_cause_or_design_decision: 若只补 `4-道具/3-面板` 叶子技能而不改阶段父级，`4-Design` 仍会保留“其余 3-面板 pending”的过时状态，形成父级第二真源。
- final_fix_or_heuristic: 每当 design 阶段新增 active leaf，都要同步更新阶段父级 Visual Map、active 列表和经验层 Type Map。
- prevention_or_replication_checklist:
  - [x] `4-Design/SKILL.md` 已新增 prop panel active 路由
  - [x] `4-Design/CONTEXT.md` 已记录 route sync 经验
  - [x] `4-道具/SKILL.md` 与阶段父级状态一致
- evidence_paths:
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/4-Design/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/道具/SKILL.md`
  - `.agents/skills/aigc/4-Design/道具/3-面板/SKILL.md`
- user_feedback_or_constraint: 用户要求直接完善 prop panel skill，而不是只把空目录留在阶段树里。

### Case-20260412-AIGC-4-DESIGN-COSTUME-ACTIVATED

- milestone_type: source_contract_change
- outcome: 将 `4-Design` 阶段中的 `3-服装` 从 pending 空目录升级为 active 类目，并一次性开放 `1-清单 / 2-设计 / 3-面板`。
- root_cause_or_design_decision: 父级合同此前把 `3-服装` 视为预留槽位，导致服装事实只能零散寄生在角色设计里，没有独立 design-source、design master 与 panel handoff。
- final_fix_or_heuristic: 把 `3-服装` 升级为完整类目，并将其第一输入根固定为 `2-角色/1-清单/角色清单.json`，避免与角色链争抢 canonical source。
- prevention_or_replication_checklist:
  - [x] `4-Design/SKILL.md` 已同步 active 状态
  - [x] `3-服装` 父级与三段叶子真源已落盘
  - [x] `4-Design/CONTEXT.md` 已记录服装链路的 canonical source 决策
- evidence_paths:
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `.agents/skills/aigc/4-Design/服装/SKILL.md`
  - `.agents/skills/aigc/4-Design/服装/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/服装/3-面板/SKILL.md`
- user_feedback_or_constraint: 用户要求根据 `角色 / 场景 / 道具` 及相关 subagents 配置，完善 `.agents/skills/aigc/4-Design/服装`。
