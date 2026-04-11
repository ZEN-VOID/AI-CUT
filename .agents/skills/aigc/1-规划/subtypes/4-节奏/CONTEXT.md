# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `1-规划/4-节奏` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时，应自动预加载本文件。
- 优先级固定为：用户显式请求 > 根 `AGENTS.md` > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `original_adherence: true` 仍被做结构重排 | 授权边界层 | 回退到保序 handoff，并跳过 `4-节奏` 独立执行 | 在 `FIELD-RO-01` 固化布尔门与 `FAIL-RO-01` | true 时不再生成节奏蓝图 |
| 节奏方案像统一模板，集与集长相相同 | 策略层 | 回到主驱动判定，移除无收益的冷开场/强反转/统一 cliffhanger | 在 `SKILL.md` 固化反机械化门禁与主驱动优先 | 输出能说清“为何这样裁” |
| 没有分组容器却强做七步映射 | 上游依赖层 | 停止执行并要求先补 `1-规划/3-分组` | 在执行流程固化“无分组不落笔” | 只在容器存在时继续 |
| 只给蓝图术语，没有组级节奏刀法与 handoff | 输出合同层 | 补齐 `节奏执行策略` 与 `下游加载提示` | 用固定区块与字段表接住 | `2-组间/导演意图` 与 `3-明细` 可直接继承 |
| `4-节奏` 偷改剧情事实或自造新设定 | 事实守恒层 | 回滚新增事实，改写为组级前置/压缩/留白建议 | 在输出契约固定“不得发明新事实” | 蓝图只处理节奏，不改事实 |
| 父级 `1-规划` 明说 `4-节奏` 仅在显式要求时进入，但叶子合同没写 patch-back 关系 | 父子聚合层 | 在执行流与输出契约中补“local handoff + optional parent patch-back” | 固化 optional 子技能默认不占位、仅在显式选中时回写父级主稿 | 父级主稿不会凭空长出节奏占位块 |

## Repair Playbook

1. 先检查 `0-Init` 是否已写 `original_adherence`，并将其解释为“是否保留原作节奏”。
2. 再检查 `1-规划/3-分组/第N集.md` 是否稳定存在。
3. 再检查主驱动、七步映射、峰值账本是否都落到了固定区块。
4. 再检查有没有把导演意图、脚本改写或事实增量混进来。
5. 最后检查 `2-组间/导演意图` 与 `3-明细` 是否都能直接消费 `下游加载提示`。

## Reusable Heuristics

- `4-节奏` 先问“能不能动结构”，再问“该不该动结构”；授权边界永远先于审美收益。
- 从旧仓迁来的精华不是把七步术语原样照搬，而是把 `主驱动判定 + 顺序授权 + 反机械化 + 风险回执` 迁成当前仓可执行合同。
- 对规划层来说，节奏蓝图最稳的输入不是剧本文本，而是已经稳定的分组容器与 `0-Init` 的节奏授权门。
- 只要用户没有要求保留原作节奏，`original_adherence` 默认应显式落盘为 `false`，不要再把“是否能做节奏重排”留在口头状态。
- `4-节奏` 的目标不是替 `2-组间` 或 `3-明细` 先写正文，而是降低后续阶段继续放大的猜谜成本。
- `4-节奏` 默认是 optional child skill：本地 handoff 可以独立存在，但只有父级显式选中时，才应该把节奏摘要回写到 `规划/第N集.md`。

## Case Log

### Case-20260410-AIGC-PLANNING-RHYTHM-RELOCATION

- milestone_type: source_contract_change
- outcome: 将原 `2-组间/subtypes/节奏优化` 迁移为 `.agents/skills/aigc/1-规划/subtypes/4-节奏`，并把其升级为分组后、受 `0-Init.original_adherence` 约束的规划层独立子技能。
- root_cause_or_design_decision: 直接技术原因不是“节奏内容写得不够”，而是该能力实际依赖 `3-分组` 的稳定容器，却仍被挂在 `2-组间`，形成阶段边界错位与父级双真源风险。
- final_fix_or_heuristic: 将节奏治理拆为独立 `4-节奏` 子技能，只在 `original_adherence: false` 且分组容器稳定时启用；把主驱动、七步、峰值、顺序授权与风险回执都固定到规划层输出合同，并作为 `2-组间/导演意图` 与 `3-明细` 的共同上游。
- prevention_or_replication_checklist:
  - [x] 独立子技能合同已迁入 `1-规划`
  - [x] 已接入 `0-Init.original_adherence` 布尔门
  - [x] 已改为分组后规划层入口
  - [x] 已明确不越权改写事实与对白
  - [x] 已形成到 `2-组间/导演意图` 与 `3-明细` 的节奏 handoff
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/7-节奏感/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/7-节奏感/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求将 `.agents/skills/aigc/2-组间/subtypes/节奏优化` 调整到 `.agents/skills/aigc/1-规划/subtypes/4-节奏`，命名改为 `节奏`，并沿用“是否保留原作节奏”作为执行门。

### Case-20260411-AIGC-PLANNING-RHYTHM-PARENT-PATCHBACK

- milestone_type: source_contract_change
- outcome: 为 `4-节奏` 补齐了“local handoff + optional parent patch-back”合同，和父级 `1-规划` 的默认不选规则对齐。
- root_cause_or_design_decision: 直接技术原因不是节奏蓝图内容不足，而是叶子合同只定义了本地落点，没有定义显式选中时如何回写父级主稿，导致 optional 分支在父子流转上不闭合。
- final_fix_or_heuristic: 保留 `规划/4-节奏/第N集.md` 作为 canonical child output，同时把“仅在父级显式选中时，摘要 patch 回 `规划/第N集.md`”写入执行流与输出契约。
- prevention_or_replication_checklist:
  - [x] `references/execution-flow.md` 已补父级聚合写回规则
  - [x] `references/output-template.md` 已补 parent relationship
  - [x] `CONTEXT.md` 已记录 optional child skill heuristic
- evidence_paths:
  - `.agents/skills/aigc/1-规划/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/4-节奏/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求 `4-节奏` 默认不选，仅在显式强调时再进入，并且整个 `1-规划` 最终应统一汇总到 `projects/<项目名>/规划/第N集.md`。
