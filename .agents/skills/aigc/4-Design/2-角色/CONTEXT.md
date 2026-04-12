# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/2-角色` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 角色类目没有先做清单就进入设计 | 类目路由层 | 回退到 `1-清单` 先产出角色对象池 | 固化 `清单 -> 设计 -> 面板` 的默认顺序 | 下游能复用同一份角色清单 |
| 角色清单脚本与 shared schema 不对齐 | 输入契约层 | 改按 `final_output.main_content.分镜组列表[].分镜明细[]` 取数 | 在叶子技能合同中回指 shared schema | `角色及站位和穿搭` 可被稳定读取 |
| `2-设计` 目录存在但没有父 skill 与 team contract | 子技能治理层 | 补齐 `2-设计/SKILL.md + CONTEXT.md + _shared/IO_CONTRACT.md`，并落盘角色设计组 team | 将“active 入口”定义为必须同时具备父 skill 与真实 agent docs | `2-设计` 不再是空目录入口 |
| 角色面板 leaf 已落地，父级合同仍写 pending | 路由状态层 | 同步更新 `2-角色/SKILL.md` 与 `4-Design/SKILL.md` 的 active 列表 | 每新增 active leaf 同步回写父级合同与经验层 | 父级状态与真实入口一致 |

## Repair Playbook

1. 先查输入是否为 shared director schema。
2. 再查当前任务是否需要角色对象池，而不是角色图。
3. 若只是建立对象清单，固定进入 `1-清单`。
4. 若对象池和设计稿都已存在，继续判断当前是进入 `2-设计` 还是 `3-面板`，不要停在父级口头描述。

## Reusable Heuristics

- 角色链最重要的第一步不是“做得华丽”，而是先把同一角色对象的 canonical identity 锁住。
- 只要上游已经统一成导演 episode JSON，角色链就不该再保留第二套平行输入格式作为第一真源。
- 当 `2-设计` 或 `3-面板` 已落地，父级合同若仍写成 pending，本身就会变成第二真源，必须同步纠正。

## Case Log

### Case-20260412-AIGC-DESIGN-ROLE-PARENT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/2-角色` 建立了类目父级合同，并把 `1-清单` 固定为首个 active 入口。
- root_cause_or_design_decision: 叶子技能若脱离类目父级单独存在，会导致后续 `2-设计 / 3-面板` 无法共享同一条角色对象池来源。
- final_fix_or_heuristic: 先建立类目级边界，再让 `1-清单` 成为角色链的 canonical source builder。
- prevention_or_replication_checklist:
  - [x] 类目父级合同已存在
  - [x] active 入口已固定为 `1-清单`
  - [x] 经验层已写明 shared schema 对齐要求
- evidence_paths:
  - `.agents/skills/aigc/4-Design/2-角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/CONTEXT.md`
- user_feedback_or_constraint: 用户本轮只要求完善角色清单路径，因此设计/面板保持 pending。

### Case-20260412-AIGC-DESIGN-ROLE-DESIGN-ACTIVATION

- milestone_type: source_contract_change
- outcome: 将 `2-设计` 从 pending 预留目录升级为 active 父 skill，并同步落盘角色设计组 team 与七个角色合同。
- root_cause_or_design_decision: `2-角色` 父类目已经明确存在 “清单 -> 设计 -> 面板” 顺序，但 `2-设计` 目录和 `.codex/agents/aigc/设计组/角色设计` 仍是空壳，占位存在、合同缺失，导致类目路由在进入设计时断链。
- final_fix_or_heuristic: 把 `2-设计` 建成 full 父 skill，采用 `设计统筹 -> 形象建模 -> 三 specialist 并行 -> reviewer -> auditor -> 父 skill 写回` 的 mixed tranche，保持父 skill 独占 canonical writeback。
- prevention_or_replication_checklist:
  - [x] `2-设计` 父 skill 已建立
  - [x] `2-设计` shared I/O 已建立
  - [x] 角色设计组 team 与 agent docs 已建立
  - [x] 父类目状态已同步为 active
- evidence_paths:
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/SKILL.md`
  - `.codex/agents/aigc/设计组/角色设计/team.md`
  - `.agents/skills/aigc/4-Design/2-角色/SKILL.md`
- user_feedback_or_constraint: 用户要求以 `skill-subagents + brainstorming + senior-prompt-engineer` 为基础，系统性重构 `4-Design/2-角色/2-设计`。

### Case-20260412-AIGC-DESIGN-ROLE-PANEL-ACTIVATION

- milestone_type: source_contract_change
- outcome: 将 `3-面板` 从 pending 预留目录升级为 active leaf，并同步纠正了 `2-角色` 父级中的 route 状态。
- root_cause_or_design_decision: 当前仓已经具备 `2-设计` 角色设计 carrier，但缺少与之衔接的角色面板 leaf，导致角色链在“设计稿 -> 面板 packet”这里断开，父级状态也随之滞后。
- final_fix_or_heuristic: 让 `3-面板` 直接消费 `character_design.json + [角色名].md`，把 `prompt整合` 收束成 layout packet，并同步刷新父级 active 列表。
- prevention_or_replication_checklist:
  - [x] `3-面板` 主合同已建立
  - [x] `3-面板` shared I/O 与 runner 已建立
  - [x] `2-角色/SKILL.md` 已同步 active 状态
  - [x] 经验层已记录 route-sync 经验
- evidence_paths:
  - `.agents/skills/aigc/4-Design/2-角色/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/3-面板/scripts/build_character_panel_packets.py`
  - `.agents/skills/aigc/4-Design/2-角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/CONTEXT.md`
- user_feedback_or_constraint: 用户本轮要求直接完善 `.agents/skills/aigc/4-Design/2-角色/3-面板`，并参照前代 `角色面板` 技能。
