# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/2-角色/2-设计` 的经验层知识库，不是过程日志。
- 调用本父 skill 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-设计` 跳过 `1-清单` 直接发明角色设计 | 输入锚点层 | 强制回到 `角色清单.json` 锁角色 canonical identity | 在 `SKILL.md` 和 team 合同中固化“先清单、再设计” | 不再出现无对象池设计 |
| 四个 specialist 各写一整份角色稿，父 skill 无法收束 | 编排边界层 | 收回写回权到父 skill，只允许返回 `agents_plan + patch / note / report` | 在 `team.md` 与 `_shared/IO_CONTRACT.md` 固化 agents-plan-aware handoff | canonical 输出只由父 skill 写回 |
| `形象建模` 与 `服装 / 妆容 / 个性` 三条线互相打架 | reviewer 合同层 | 进入 `角色一致性复核`，要求指出冲突字段与返工入口 | 将跨字段一致性检查设为默认 tranche | reviewer 能给出明确 rework |
| 角色设计只剩 Markdown，没有 machine-first carrier | 输出治理层 | 补回 `character_design.json` 并让 Markdown 与其同源 | 在输出模板中固定 JSON 为 canonical | 下游面板/生图能稳定消费 JSON |
| 角色设计吞掉场景或道具职责 | 边界治理层 | 将场景/道具信息降级为只读 context packet | 在父 skill 中固化“只读桥接，不并入常驻团队” | 不再出现跨模块越权 |
| `.codex/agents/aigc/设计组/角色设计/*.md` 只有空文件或断链 | subagent 真源层 | 补齐 `team.md + planner + 4 specialists + reviewer + auditor` | 让父 skill 只回链真实存在的 agent docs | team 引用与物理文件一致 |

## Repair Playbook

1. 先查 `1-清单/角色清单.json` 是否存在且角色 identity 稳定。
2. 再看 `team.md` 是否仍把写回权保留在父 skill。
3. 再看 `character_design.json` 是否与逐角色 Markdown 同源。
4. 若角色设计冲突，优先回到 `角色一致性复核` 指定的字段槽位返工。
5. 最后才调整单次角色文案或 prompt 话术。

## Reusable Heuristics

- 角色设计最稳的入口不是“从镜头里直接想象角色”，而是先有角色对象池，再做结构化设计。
- `形象建模` 先跑不是为了抢权，而是为了给服装、妆容、个性三条线提供同一个视觉锚点。
- reviewer 最有价值的工作不是润色，而是阻止多个 specialist 把角色拉向不同的人设。
- 对 `2-设计` 来说，`character_design.json` 不是附属 sidecar，而是下游面板和生图可持续复用的 canonical carrier。
- 场景和道具信息适合作为只读兼容约束，不适合让角色设计组扩张成跨模块常驻团队。
- 对角色设计来说，`agents_plan` 最适合承载角色批次、字段补位顺序与 reviewer/auditor 返工摘要；最终 design carrier 仍只能由父 skill 写回。

## Case Log

### Case-20260412-AIGC-ROLE-DESIGN-SKILL-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/2-角色/2-设计` 建立了父 skill、经验层、shared I/O、模板、入口元数据与角色设计组 team。
- root_cause_or_design_decision: `2-角色` 类目已经把 `2-设计` 标为预留入口，但本地目录为空，同时 `.codex/agents/aigc/设计组/角色设计` 只有 0 字节占位文件，导致“有路径、无真源、无 team contract”。
- final_fix_or_heuristic: 将 `2-设计` 定义为 full 父 skill，采用 `设计统筹 -> 形象建模 -> 三 specialist 并行 -> reviewer -> auditor -> 父 skill 写回` 的 mixed tranche，并以 `character_design.json + 逐角色 Markdown + _manifest.json` 作为 canonical 输出。
- prevention_or_replication_checklist:
  - [x] 父 skill 已建立
  - [x] `_shared/IO_CONTRACT.md` 已建立
  - [x] `agents/openai.yaml` 已建立
  - [x] 角色设计组 team 与 agent docs 已落盘
  - [x] 父类目状态已从 pending 刷新为 active
- evidence_paths:
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/角色设计/team.md`
  - `.agents/skills/aigc/4-Design/2-角色/SKILL.md`
- user_feedback_or_constraint: 用户明确要求以 `skill-subagents + brainstorming + senior-prompt-engineer` 深度重构 `2-设计`，并让 subagents 负责思考与 plan，父 skill 统筹输入输出。

### Case-20260412-AIGC-ROLE-DESIGN-AGENTS-PLAN-ALIGNMENT

- milestone_type: source_contract_change
- outcome: 将角色设计链的 subagent handoff 从 patch-only 语义升级为 `agents_plan + patch / note / report`。
- root_cause_or_design_decision: `1-Planning` 已将 subagent 语义收口到“agents plan + skill execution”，但角色设计链仍把 handoff 描述成 patch-only，导致角色设计组与上游阶段之间的执行语义不一致。
- final_fix_or_heuristic: 同步更新父 skill、shared I/O、team、planner 角色与入口元数据，明确 `agents_plan` 只承载角色批次、字段补位顺序与 review/audit 返工摘要，不冒充 `character_design.json`。
- prevention_or_replication_checklist:
  - [x] 父 skill 已改为 agents-plan-aware handoff
  - [x] shared I/O 已同步 slot ownership 新口径
  - [x] team 与角色入口元数据已同步 `allowed_return_types`
  - [x] 经验层已登记新 handoff 语义
- evidence_paths:
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/角色设计/team.md`
  - `.codex/agents/aigc/设计组/角色设计/设计统筹.md`
- user_feedback_or_constraint: 用户要求把 `1-Planning` 已完成的 agents-plan 口径继续推广到 `2-角色/2-设计`，避免父 skill 和 role contract 对 subagent 职责理解不一致。
