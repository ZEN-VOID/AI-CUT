# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/SKILL.md` 时，应自动预加载本文件。
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
| 父 skill 仍引用已删除的 planning agent 文档 | 路由锚点层 | 收回到父 skill 或对应 stage skill | 在 audit 固化 `1-Planning` 的内化合同检查 | 旧规划组文档不再出现在运行链 |
| `1-分集 / 2-剧本 / 3-分组` 真源边界混写 | 输出治理层 | 回到 `_shared/IO_CONTRACT.md` 重新锁定边界 | 在父 skill 固化 `Story -> 1-分集 -> 2-剧本 -> 3-分组` 单线结构 | 三层真源不再互相覆盖 |
| `2-剧本` 又退回“外部判模 + 内部写回”的半断链形态 | 子阶段治理层 | 把判模与变体能力继续收回 `2-剧本/SKILL.md` | 在 `2-剧本` 与 audit 中固化 `Internal Capability Fusion Contract` | `2-剧本` 自足执行 |
| `3-分组` 又退回“外部 specialist/reviewer + 本地量化”的双真源形态 | stage-local 治理层 | 收回 reviewer/specialist 到 `3-分组/SKILL.md` | 在 `3-分组` 与 audit 中固化内化执行面 | `3-分组` 自足执行 |
| 节奏复核在默认场景被滥开 | 阶段路由层 | 只在明确条件下开启 reviewer gate | 在 `1-Planning` 与 `3-分组` 同步 reviewer 进入条件 | reviewer gate 不再膨胀默认工作量 |

## Repair Playbook

1. 先检查 `1-Planning/SKILL.md` 是否仍清楚声明 `Story -> 1-分集 -> 2-剧本 -> 3-分组`。
2. 再检查 `_shared/IO_CONTRACT.md` 是否仍把三层真源分开。
3. 再看 `2-剧本` 与 `3-分组` 是否仍可在不依赖外部 planning docs 的情况下自足执行。
4. 最后才看具体产物是否需要返工。

## Reusable Heuristics

- 对规划阶段来说，最容易坏的不是 leaf 本身，而是父 skill 和子阶段 skill 之间的真源边界。
- 如果某个阶段的高分叉能力已经稳定地可以写回单一 `SKILL.md`，就不要再保留外部 agent/team 文档充当第二真源。
- `1-Planning` 最稳的总线始终是：父 skill 负责路由与验收，子阶段 skill 负责 stage-local 执行与写回。
- 节奏在当前规划阶段应优先作为 reviewer gate 存在，而不是默认独立执行面。

## Case Log

### Case-20260412-AIGC-PLANNING-INTERNAL-CAPABILITY-FUSION

- milestone_type: source_contract_change
- outcome: 将 `1-Planning` 从“父 skill + 外部 planning group docs”重构为“父 skill + 内化型 stage skills”的单线治理结构。
- root_cause_or_design_decision: 用户明确要求废弃旧规划组文档，并把相关能力重新整理吸回 `SKILL.md`；因此规划阶段不能再把外部 planning docs 当作执行真源。
- final_fix_or_heuristic: 在父 `1-Planning` 中明确 `1-分集 / 2-剧本 / 3-分组` 的 stage-local ownership；在 `2-剧本` 与 `3-分组` 中分别内化原来的判模/变体与分组/reviewer 能力；同步让 audit 改查内化合同，而不再要求旧 planning docs。
- prevention_or_replication_checklist:
  - [x] `1-Planning` 已不再回链旧 planning docs
  - [x] `2-剧本` 已内化判模/标准剧/解说剧
  - [x] `3-分组` 已内化分组/reviewer gate
  - [x] audit 已转为检查新合同
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求旧规划组文档不再需要，并要求按知行合一规范重排 `2-剧本`。
