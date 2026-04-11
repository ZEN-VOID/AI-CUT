# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-明细/subtypes/6-转场特效` 的经验层知识库，不是进度日志。
- 调用 `.agents/skills/aigc/3-明细/subtypes/6-转场特效/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/3-明细/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 已有 `[分镜N]`，但镜间/段间仍像生硬拼接 | 行内输出层 | 在命中位原位补写 `转场：` | 把 `转场：` 的邻接位置与五问门槛写成硬合同 | 每个命中位下有且仅有一条 `转场：` |
| `转场：` 只写“叠化/匹配切/更流畅/更电影感” | 内容门槛层 | 重写为触发、桥接、落点、作用齐备的可感知结果 | 在父合同固定“只写观众看见/听见/感到的结果” | 单条转场可直接被想象与执行 |
| 所有边界都套同一套黑场、白闪或声桥模板 | 反模板层 | 重做锚点、桥接表面与下一落点差异化 | 把“同款句法重复 > 2 次即返工”列为质量门禁 | 组内句法与桥接材料不再机械重复 |
| 直接照搬导演阶段 JSON `转场` 合同 | 真源适配层 | 保留高门槛桥接思路，改写为脚本阶段 `转场：` 行 | 在技能中显式说明“吸收而不照搬” | 导演链与脚本链真源不串台 |
| 本层开始偷写摄影/氛围或改正文事实 | 边界层 | 回滚越权改动，只保留 `转场：` 和报告 | 把“只动转场行”写成 patch-in-place 合同 | diff 中无非本层字段漂移 |
| 镜内后期结果写成软件工序说明 | 表达层 | 改写为观众可见的结果而非制作术语 | 在技能中显式禁止软件/参数/节点词 | 正文不再出现 AE、关键帧、遮罩等词 |

## Repair Playbook

1. 先检查 `第N集.md` 是否已具备 `[分镜N]` 骨架。
2. 再检查是否已读到 `2-组间` handoff、角色增强与运镜残势。
3. 先在侧车里裁决组级/段级桥接逻辑，再回写逐镜 `转场：`。
4. 落笔后检查五问门槛、模板化重复与术语泄漏。
5. 最后检查是否越权写入摄影/氛围或改坏正文事实。

## Reusable Heuristics

- `3-明细` 的转场增强，最怕的不是写少，而是“只剩方法名，没有观众感知结果”。
- 真正好用的脚本转场，不是把导演阶段的镜级字段搬过来，而是把那条桥接判断拆成逐镜可读的 `转场：` 行。
- 转场层是收束层，必须读取前面已经发酵出来的人物压力与运镜残势，不然桥接会像凭空发生。
- 不是每个 `[分镜N]` 都需要 `转场：`，但一旦命中，就必须让下一落点和情绪作用同时成立。
- 对行内落笔型子技能做 `think-think` 升级时，主合同不应只剩字段表；至少要补齐 `运行模式 + 启发式工作链 + 可见快照 + 工具后反思 + Gate Summary`，否则思维链仍会退化成表格壳。
- `DIE` 这类领域启发器应该保留，但要降级成“领域判断加速器”，不能继续冒充完整思维链主合同。

## Case Log

### Case-20260409-AIGC-SCRIPT-TRANSITION-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/6-转场特效` 建立了父级执行合同与经验层，并把导演链 `9-转场特效` 的高门槛桥接逻辑适配为脚本终稿的行内 `转场：` 落笔方式。
- root_cause_or_design_decision: 用户要求参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/9-转场特效` 完善脚本链 `6-转场特效`，同时明确整个 `3-明细` 系列都应遵循“上游分组原文 -> 分任务类型层层加权扩写 -> 发酵成最终文件”的新前提；因此不能直接复制导演阶段 JSON `转场` 合同，而必须改写为脚本链真源。
- final_fix_or_heuristic: 保留导演参考里的“发现-激发-增写”与桥接锚点/包装层/具象结果高门槛，但把 canonical 输出改为同一份 `第N集.md` 中命中位逐镜 `转场：` 行，并用侧车承接组级桥接裁决。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已建立
  - [x] `CONTEXT.md` 已建立
  - [x] 已固定 `转场：` 行内格式
  - [x] 已写明“先组级桥接，后逐镜落笔”
  - [x] 已把导演链参考改写为脚本链真源
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/9-转场特效/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“完善一下 `.agents/skills/aigc/3-明细/subtypes/6-转场特效`，参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/9-转场特效`”，并补充“整个 `.agents/skills/aigc/3-明细` 系列按照新的前提预设：对于上游分集分组好的原文，根据不同的任务类型进行层层加权扩写式任务，以其最终发酵为完善的融合组间层全部智慧的最终文件”。

### Case-20260409-AIGC-SCRIPT-TRANSITION-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/3-明细/subtypes/6-转场特效/references/chain-of-thought.md` 从旧版 `表格 + DIE` 结构升级为最新 `think-think` 口径的可见思维合同。
- root_cause_or_design_decision: 用户明确要求“按照最新的思维链设计规范，优化一下 `.agents/skills/aigc/3-明细/subtypes/6-转场特效/references/chain-of-thought.md`”；诊断后发现当前文件虽然已有字段主表和 `DIE-Transition`，但缺少运行模式判定、启发式工作链、可见快照分层、工具后反思与 Gate Summary，因此仍偏向旧版静态表格合同。
- final_fix_or_heuristic: 保留 `DIE-Transition` 作为领域启发器，但将主合同升级为 `模块定位 + 设计立场与运行模式 + Think-Think Design Snapshot + 可见快照与隐藏推理分层 + 标准思维链主链 + 工具后反思与 Gate Summary + 字段落盘快照`，并把 `Gate Summary` 并入 `FIELD-TRN-HANDOFF-06` 的收束职责。
- prevention_or_replication_checklist:
  - [x] 已补 `运行模式判定`
  - [x] 已补 `启发式工作链`
  - [x] 已补 `可见快照与隐藏推理分层`
  - [x] 已补 `工具后反思与 Gate Summary`
  - [x] 已保留 `DIE-Transition` 但降级为领域启发器
  - [x] 已同步更新本 `CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/CONTEXT.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
- user_feedback_or_constraint: 用户要求按最新 `think-think` 规范直接优化目标文件，而不是只做局部润色或停留在建议层。
