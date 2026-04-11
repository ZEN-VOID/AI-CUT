# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-明细/subtypes/3-运镜手法` 的经验层知识库，不是进度日志。
- 调用 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/SKILL.md` 时，应自动预加载本文件。
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
| 已有 `[分镜N]`，但没有 `运镜：` 行 | 行内输出层 | 在对应 `[分镜N]` 下原位补写 `运镜：` | 把 `运镜：` 的邻接位置写成硬合同 | 每个相关帧下有且仅有一条 `运镜：` |
| `运镜：` 只写“慢推/横移/更有电影感” | 内容门槛层 | 重写为起点、路径、变速、收束、目的五问齐备 | 在父合同固定五问门槛 | 单条运镜可直接执行 |
| 每镜都像独立酷句，组内没有连续波形 | 组级策略层 | 先补运镜设计侧车里的组级波形，再回写逐镜 | 先波形后逐镜，禁止直接逐镜乱写 | 相邻镜头可解释承接关系 |
| 所有镜头都套同一套推拉摇移模板 | 反模板层 | 重做动词、节拍和落点差异化 | 把“去模板化”列为显式质量门禁 | 组内句法与动势不再机械重复 |
| 本层开始偷写光色氛围或改正文事实 | 边界层 | 回滚越权改动，只保留 `运镜：` 和报告 | 把“只动运镜行”写成 patch-in-place 合同 | diff 中无非本层字段漂移 |
| 直接照搬导演阶段 JSON `镜头运动` 合同 | 真源适配层 | 保留高门槛思路，改写为脚本阶段行内落笔 | 在技能中显式说明“吸收而不照搬” | 导演链与脚本链真源不串台 |
| `references/chain-of-thought.md` 仍停留在旧版表格快照，缺少启发式工作链、工具后反思与 Gate Summary | 思维链合同层 | 重写为新版 `Think-Think Design Snapshot + 三向三重 + 可见/隐藏分层 + Gate` | 把 `chain-of-thought.md` 视为本层思维链真源，并显式要求快照只保留可审计内容 | 文件中可见 `启发式工作链`、`工具后反思`、`Gate Summary` 与新增字段映射 |

## Repair Playbook

1. 先检查 `第N集.md` 是否已具备 `[分镜N]` 骨架。
2. 再检查是否已读到 `2-组间` handoff 与当前人物增强证据。
3. 先在侧车里裁决组级/段级波形，再回写逐镜 `运镜：`。
4. 落笔后检查五问门槛与模板化重复。
5. 最后检查是否越权写入光色氛围或改坏正文事实。

## Reusable Heuristics

- `3-明细` 的运镜增强，最怕的不是写少，而是“只有镜头术语，没有观看路径”。
- 真正好用的脚本运镜，不是把导演阶段的组级 `镜头运动` 生搬过来，而是把那条组级波形拆成逐镜可读的 `运镜：` 行。
- 逐镜运镜如果不先看组级波峰波谷，很容易每镜都酷、整组全乱。
- 对脚本层来说，静止不是失败，但“静止为什么成立”必须被说清。
- 运镜思维链不该外露成长篇流程脚本；真正该留下来的，是 `dominant wave`、关键锚点、逐镜落笔计划和可返工的 Gate。
- 当上游证据变化时，运镜链必须先重判“原波形是否还成立”，而不是机械沿用第一次选中的路径。

## Case Log

### Case-20260409-AIGC-SCRIPT-CAMERA-MOVEMENT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法` 建立了父级执行合同与经验层，并把导演链里的高门槛运镜思路适配为脚本终稿的行内 `运镜：` 落笔方式。
- root_cause_or_design_decision: 用户要求完善 `3-运镜手法`，同时明确整个 `3-明细` 系列都应遵循“上游分组原文 -> 分任务类型层层加权扩写 -> 发酵成最终文件”的新前提；因此不能直接复制导演阶段 JSON `镜头运动` 合同，而必须改写为脚本链真源。
- final_fix_or_heuristic: 保留导演参考里的“发现-激发-增写”与路径/节拍/落点/目的高门槛，但把 canonical 输出改为同一份 `第N集.md` 中逐镜 `运镜：` 行，并用侧车承接组级运镜波形。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已建立
  - [x] `CONTEXT.md` 已建立
  - [x] 已固定 `运镜：` 行内格式
  - [x] 已写明“先组级波形，后逐镜落笔”
  - [x] 已把导演链参考改写为脚本链真源
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/8-运镜手法/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“完善一下 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法`，参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/8-运镜手法`”，并补充“整个 `.agents/skills/aigc/3-明细` 系列按照新的前提预设：对于上游分集分组好的原文，根据不同的任务类型进行层层加权扩写式任务，以其最终发酵为完善的融合组间层全部智慧的最终文件”。

### Case-20260409-AIGC-SCRIPT-CAMERA-MOVEMENT-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/references/chain-of-thought.md` 从旧版“表格快照 + DIE-Move”升级为符合最新 `think-think` 规范的新版思维链合同。
- root_cause_or_design_decision: 旧版文件虽然已有方向轴/成立轴/优选轴与运镜波形内容，但还缺少新版强制项：启发式工作链优先、可见快照与隐藏推理分层、工具后反思、Gate Summary，以及能把失败导回具体返工入口的新增字段。
- final_fix_or_heuristic: 保留 `运镜波形` 作为核心判断对象，同时新增 `FIELD-CAM-DSP-07 / FIELD-CAM-REFLECT-08 / FIELD-CAM-GATE-09`，把新版 `Think-Think Design Snapshot`、工具后反思与 Gate 验收链落为真源结构。
- prevention_or_replication_checklist:
  - [x] 已加入 `启发式工作链（运镜版）`
  - [x] 已加入 `三向三重自省流`
  - [x] 已加入 `可见快照 / 隐藏推理` 分层
  - [x] 已加入 `工具后反思`
  - [x] 已加入 `Gate Summary`
  - [x] 已同步新增字段与返工入口
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/references/chain-of-thought.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“按照最新的思维链设计规范，优化一下 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/references/chain-of-thought.md`”。
