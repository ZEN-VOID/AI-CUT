# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划` 阶段的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/1-规划/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `1-规划` 目录存在但父级 `SKILL.md` 为空 | 阶段合同层 | 先补父级阶段合同，锁定子路径路由与落点 | 让所有规划子路径都从父级显式可达 | 父级能明确说明进入哪个子路径 |
| 子技能已存在内容，但父级没有入口 | 父子路由层 | 回写父级路由矩阵与 Mermaid 总览 | 形成“父级总入口 + 子级实质合同”结构 | 从父级可定位唯一子入口 |
| 直接照抄参考仓路径，导致落点不适配当前 `projects/` 体系 | 真源继承层 | 将能力继承与路径合同拆开，只迁移能力，不复制旧路径 | 在子技能中明确当前仓的 canonical landing | 产物全部落到当前项目运行时指定目录 |
| 规划阶段越权替下游阶段做细节真源 | 阶段边界层 | 收回到结构规划、格式规划、分组规划的边界 | 在父级和子级合同都显式声明“不拥有”范围 | 规划产物可交给下游继续消费，而不是代替下游 |
| `2-格式` 已有变体目录，但缺少父级裁决与默认分支 | 变体路由层 | 先补 `2-格式` 父级合同，再写 `标准剧/解说剧` 子技能 | 固化“父级裁决变体，子级细写合同” | 不再出现空壳变体目录 |
| 项目已启用顾问团，但规划阶段未读取 `team.yaml` | 共享运行时层 | 执行前先读项目根 `team.yaml` 与 `_shared/council-runtime/module-spec.md` | 在 `1-规划` 根技能固化 `策划前置 + 评审闸门` 合同 | 规划任务进入前能判断是否要启用顾问团 |
| 分组后节奏治理仍挂在 `2-组间` | 阶段边界层 | 将其迁回 `1-规划/subtypes/4-节奏`，并让 `0-Init.original_adherence` 直接作为规划阶段执行门 | 固化 `1-规划` 的第 4 个串行子路径，避免 `3-分组 -> 2-组间` 之间出现错位真源 | 分组后的节奏产物统一落到 `projects/<项目名>/1-规划/4-节奏/` |
| `1-规划` 结束后没有立即创建后续共享 episode 根文件 | 运行时真源层 | 让 `1-分集` 在分集确定后立即 bootstrap `projects/<项目名>/编导/第N集.json` | 把 `_shared/project-runtime-layout.md` 与 bootstrap template 作为规划阶段的 shared carrier，并让后续阶段都消费同一根文件 | `2-组间` 与 `3-明细` 都不再自建 episode 主文件 |

## Repair Playbook

1. 先检查父级 `1-规划/SKILL.md` 是否具备阶段定位、子路径路由与落点合同。
2. 再检查具体子路径是否已有可执行 `SKILL.md + CONTEXT.md`。
3. 若目标是 `2-格式`，继续检查父级是否已写清 `标准剧/解说剧` 的默认与进入条件。
4. 若参考仓可借鉴，只继承高价值能力和验证结构，不直接复制旧仓路径。
5. 先让父级能路由到子级，再细化子级内容。
6. 新经验优先沉淀在最窄作用域；跨子路径共性再向上晋升。

## Reusable Heuristics

- 对多子路径规划阶段来说，最常见的问题不是“子技能写得不够多”，而是父级没有入口，导致子技能变成孤岛。
- 从参考仓继承技能时，能力结构可以借，路径合同必须重写到当前仓的 canonical landing。
- `1-规划` 最稳的职责边界是“给结构，不替下游拍板表现细节”。
- 对 `2-格式` 来说，父级最重要的职责不是写某个变体的细节，而是先做唯一变体裁决。
- 只要某个能力的直接输入已经是 `3-分组` 产物，它就应优先归入 `1-规划`，而不是继续挂在 `2-组间` 假装自己是导演层真源。
- 如果用户没有显式给出“旁白主导/解说剧”信号，规划阶段默认先走 `标准剧`，通常更稳。
- 对 `1-规划` 来说，顾问团最稳的节奏是“策划先给结构建议，评审最后卡 validation gate”，不要三角色同时抢答。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 当后续多个阶段都要围绕同一集文件持续 patch 时，`1-规划` 最稳的做法不是只写报告，而是先把空的 runtime root file 创建出来。

## Case Log

### Case-20260409-AIGC-PLANNING-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划` 建立了父级阶段合同与经验层，并把 `1-分集` 接回到可路由的父级入口。
- root_cause_or_design_decision: 用户要求完善 `subtypes/1-分集`，但实际直接技术阻塞是父级 `1-规划/SKILL.md` 与 `CONTEXT.md` 均为空，导致子技能即使补齐也仍无上层入口。
- final_fix_or_heuristic: 先补父级 `1-规划` 的阶段定位、子路径矩阵、落点与闭环，再建设 `1-分集` 子技能；将 `2-格式`、`3-分组` 显式标为待补合同。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补齐阶段边界与路由
  - [x] 父级 `CONTEXT.md` 已建立
  - [x] `1-分集` 已成为父级可达入口
  - [x] 未完成子路径已显式标记为待补
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参照 `AIGC-ZEN-VOID` 的分集技能完善当前 `1-分集`，默认交互语言为中文。

### Case-20260409-AIGC-PLANNING-GROUPING-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划/subtypes/3-分组` 建立了正式子技能合同，并将父级 `1-规划` 的路由矩阵从“预留中”提升为可执行入口。
- root_cause_or_design_decision: 用户要求完善 `3-分组`，但直接技术阻塞是该子路径完全空白，同时父级 `1-规划/SKILL.md` 仍明确把它标为“目录已建，合同待补”，导致下游无法把它视为真实路由。
- final_fix_or_heuristic: 参照 `AIGC-ZEN-VOID` 中 `3-拍摄段落` 的“结构容器优先”思路，补出当前仓的 `3-分组/SKILL.md + CONTEXT.md`，并同步修正父级 `1-规划` 的子路径状态与硬规则；当前集粒度继续由 `1-分集` 决定。
- prevention_or_replication_checklist:
  - [x] `3-分组` 已补齐 `SKILL.md + CONTEXT.md`
  - [x] 父级 `1-规划` 已把 `3-分组` 标记为已建合同
  - [x] 当前仓仍坚持 `projects/<项目名>/1-规划/3-分组/` 作为子路径 landing，且主产物按 `第N集.md` 落盘
  - [x] 导演阶段专属字段未被误迁入规划阶段
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/3-拍摄段落/SKILL.md`
- user_feedback_or_constraint: 用户要求同时参考 `skill-通用创建`、`skill-编排优化`，并以 `AIGC-ZEN-VOID` 的 `3-拍摄段落` 作为参照源，但落地必须适配当前仓的规划阶段和中文合同。

### Case-20260409-AIGC-PLANNING-FORMAT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划/subtypes/2-格式` 建立了父级格式规划合同，并补齐 `标准剧 / 解说剧` 两个可执行变体子技能。
- root_cause_or_design_decision: 用户要求完善 `标准剧`、`解说剧`，但真正的源层缺口不是两个子目录本身，而是 `1-规划 -> 2-格式 -> 变体` 整条父子路由链尚未闭环。
- final_fix_or_heuristic: 先补 `2-格式` 父级 `SKILL.md + CONTEXT.md`，再分别补 `标准剧 / 解说剧` 的规划层合同与经验层，最后回写 `1-规划` 根级路由矩阵、落点与默认分支规则。
- prevention_or_replication_checklist:
  - [x] `1-规划` 根级已声明 `2-格式` 可执行
  - [x] `2-格式` 父级已建立唯一变体裁决合同
  - [x] `标准剧 / 解说剧` 已具备 `SKILL.md + CONTEXT.md`
  - [x] 默认分支与进入条件已写清
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/标准剧/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md`
- user_feedback_or_constraint: 用户明确要求以 `AIGC-ZEN-VOID` 的双变体结构为参照，但当前仓必须落到 `1-规划/2-格式` 的规划语境中。

### Case-20260409-AIGC-PLANNING-COUNCIL-RUNTIME

- milestone_type: source_contract_change
- outcome: 为 `1-规划` 根技能接入了基于项目根 `team.yaml` 的顾问团运行时，默认执行 `策划前置 -> 主代理草案 -> 评审闸门`。
- root_cause_or_design_decision: 用户要求进入 `1-规划` 根技能或其叶子技能时都先判断顾问团是否启用，并落实 `策划 / 评审` 职责；若只在 `0-Init` 记团队配置，规划阶段将无法稳定消费。
- final_fix_or_heuristic: 规划阶段的顾问团运行时不应各子技能自定义，而应由 `1-规划` 根技能读取项目根 `team.yaml` 并统一执行，子技能只继承。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已新增 `Council Runtime Contract`
  - [x] `2-格式` 已声明继承上层顾问团运行时
  - [x] 已固定 `策划前置 + 评审 validation gate`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `1-规划` 及其叶子技能进入时都先读取 `projects/<项目名>/team.yaml`，并默认启用 `策划 / 评审` 职责。

### Case-20260410-AIGC-PLANNING-RHYTHM-PROMOTION

- milestone_type: source_contract_change
- outcome: 将原 `2-组间/subtypes/节奏优化` 迁移为 `.agents/skills/aigc/1-规划/subtypes/4-节奏`，并把 `1-规划` 父级路由扩展为四个串行子路径。
- root_cause_or_design_decision: 用户要求“分组之后的产物，同样根据是否进行原作节奏保留执行与否”，直接技术原因是节奏治理实际依赖 `3-分组` 结果，却仍被放在 `2-组间`，导致阶段边界与执行门都错位。
- final_fix_or_heuristic: 把节奏治理上收为 `1-规划` 的第 4 个串行子路径，并沿用 `0-Init.original_adherence` 作为“是否保留原作节奏”的布尔门；同时从 `2-组间` 移除旧入口，避免双真源。
- prevention_or_replication_checklist:
  - [x] `1-规划` 根级路由已新增 `4-节奏`
  - [x] `4-节奏` 已具备 `SKILL.md + CONTEXT.md + references + agents/openai.yaml`
  - [x] `0-Init` 的节奏执行门已改为指向规划阶段
  - [x] `2-组间` 已移除旧入口并改为消费规划 handoff
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
- user_feedback_or_constraint: 用户明确要求把 `.agents/skills/aigc/2-组间/subtypes/节奏优化` 调整到 `.agents/skills/aigc/1-规划/subtypes/4-节奏`，并统一 `1-规划/subtypes` 的输出内容格式为 `.md`。

### Case-20260410-AIGC-PLANNING-BOOTSTRAP-DIRECTOR-ROOT

- milestone_type: source_contract_change
- outcome: 将 `1-规划` 的项目级运行时升级为“以 `projects/<项目名>/1-规划/` 承接父级阶段产物与验收，同时允许 `1-分集` 在 `Init/` 写 bootstrap 产物，并在分集确定后立即创建 `projects/<项目名>/编导/第N集.json` 根文件”。
- root_cause_or_design_decision: 用户明确要求后续 `2-组间` 与 `3-明细` 都围绕一个统一 JSON 根文件工作；若 `1-规划/1-分集` 不先创建这个文件，后续阶段只能继续各自生成自己的 episode 真相。
- final_fix_or_heuristic: 将目录真源上收至 `.agents/skills/aigc/_shared/project-runtime-layout.md`，并把 `1-规划` 的阶段根目录固定为 `projects/<项目名>/1-规划/`；其中仅 `1-分集` 在落 `Init/episode-split-*` 的同时，按 bootstrap template 批量创建 `projects/<项目名>/编导/第N集.json`。
- prevention_or_replication_checklist:
  - [x] `1-规划/SKILL.md` 已改写到 `1-规划/`
  - [x] `1-分集/SKILL.md` 已声明 bootstrap `编导/第N集.json`
  - [x] shared runtime layout 已建立
  - [x] 后续阶段已回指同一根文件
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“`1-规划/subtypes/1-分集` 阶段随着分集的确定，索性就把这个 json 的空内容文件落了”。
