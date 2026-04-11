# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `3-明细/1-分镜表现` 的经验层知识库，不是进度日志。
- 调用 `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 两个子技能都存在，但不能形成分镜插入链 | 父级编排层 | 在父级显式写 `分镜密度 -> 分镜构图 -> 分镜插入` | 父级路由矩阵锁定 tranche 顺序 | 可按单一路径执行 |
| `[分镜N]` 有内容，但不知道插到哪里 | 句段锚点层 | 先让密度结果带出锚点计划 | 父级固化“先锚点、后插入” | 每镜都有挂点 |
| 内联字段名漂移 | 输出合同层 | 固定单行格式与字段顺序 | 父级统一内联格式 | 全文字段名一致 |
| 插入时改坏原文 | 原文守恒层 | 回滚到 grouped source，再重新插入 | 父级写死“只前插，不改原句” | 原文逐句可比对 |
| 顾问团已启用，但 `1-分镜表现` 没继承 `3-明细` 的阶段顾问运行时 | 继承层 | 明确本父技能继承上层 `3-明细` 的 `Council Runtime Contract` | 子技能不再重复发明第二套顾问团规则 | 进入 `1-分镜表现` 时会先遵守项目根 `team.yaml` 判定 |
| `chain-of-thought` 仍停留在三张表最小版，reasoning 模型读不到显式判断链 | 思维链真源层 | 将 reference 升级为 `运行模式 + 启发式工作链 + 三轴三重 + 可见快照 + Gate Summary` | 把新版 think-think 骨架固定为父级 `chain-of-thought` 的最小合同 | 遮掉字段表后，仍能读出 `panel_count -> 锚点 -> 单行插回` 的判断顺序 |

## Repair Playbook

1. 先检查父级 `1-分镜表现/SKILL.md` 是否已经明确子技能顺序。
2. 再检查密度结果是否给出 `panel_count + 锚点`。
3. 再检查构图结果是否给出逐镜静态字段。
4. 最后才执行主文件内联回写。

## Reusable Heuristics

- `1-分镜表现` 最容易误做成“写一堆镜头说明”，真正核心其实是“把镜头说明插回正确句段之前”。
- 如果父级不显式规定两个无序子目录的 tranche，执行时很容易被误当成并行关系。
- 对当前脚本阶段来说，`构图风格` 比 `构图方式` 更适合作为用户面字段名，但底层判断仍可参考导演阶段的构图方法论。
- 对 `1-分镜表现` 来说，顾问团机制应该继承自 `3-明细` 根级，不应在父子链里再复制一套。
- 对 `1-分镜表现` 这类父级编排技能，最新版思维链的比较尺不该是“镜头句是否漂亮”，而应是“能否稳定完成 `panel_count -> 锚点 -> 单行插回 -> 主文件验收` 的闭环”。

## Case Log

### Case-20260409-AIGC-SCRIPT-STORYBOARD-PARENT

- milestone_type: source_contract_change
- outcome: 为 `3-明细/1-分镜表现` 建立了父级可执行合同，把分镜密度、分镜构图与分镜插入三者接成一条明确链路。
- root_cause_or_design_decision: 用户要求的核心不是单独补“密度”或“构图”文档，而是要具备“在原句段之前内联注入 `[分镜1]/[分镜2]...`”的真正执行能力；因此父级编排是最高杠杆真源。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md`，明确子技能串行关系、组内编号、句段锚点与单行内联格式，再让子技能各自只承担一个裁决责任。
- prevention_or_replication_checklist:
  - [x] 已写清子技能串行顺序
  - [x] 已固定单行内联格式
  - [x] 已写明组内编号重置规则
  - [x] 已把原文守恒列为硬门槛
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“分镜插入”作为核心功能，且除分镜序号外，还需携带景别、景深、构图风格等内容。

### Case-20260409-AIGC-SCRIPT-STORYBOARD-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求“按照最新的思维链设计规范，优化 `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/references/chain-of-thought.md`”。
- root_cause_or_design_decision: 直接技术原因不是 `1-分镜表现` 缺少字段台账，而是现有 `chain-of-thought.md` 仍停留在老式三张表最小版，缺少最新 `think-think` 要求的运行模式、启发式工作链、可见/隐藏分层、工具后反思与 `Gate Summary`；这样会让 reasoning 模型知道“有哪些字段”，却读不到“为什么先判锚点、再判单行合同、最后才插回主文件”的判断链。
- final_fix_or_heuristic: 将 `chain-of-thought.md` 升级为 `运行模式 + 启发式工作链 + 三轴三重 + 可见快照 + Gate Summary + 字段落盘快照` 的完整合同，并把父级真正的比较尺压到 `panel_count -> 锚点 -> 单行插回 -> 主文件验收` 这条闭环上。
- prevention_or_replication_checklist:
  - [x] `references/chain-of-thought.md` 已升级为最新 `think-think` 结构
  - [x] 已显式声明“只暴露可见快照，不外显完整 CoT”
  - [x] 已补 `工具后反思` 与 `Gate Summary` 返工门
  - [x] `CONTEXT.md` 已记录本轮思维链升级 heuristic
  - [x] 已生成本轮 `思维链设计报告`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/reports/思维链设计报告-20260409.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/CONTEXT.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
- user_feedback_or_constraint: 用户明确指定按最新 `think-think` 规范升级目标文件，并要求在现有 `1-分镜表现` 分镜插入逻辑基础上优化，而不是改写父技能边界。
