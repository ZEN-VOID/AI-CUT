# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-画面` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/5-画面/SKILL.md` 时，应自动预加载本文件。
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
| 用户只说“做 5-画面 / 做图”，执行者却直接跳进不匹配的子路径 | 父级路由层 | 回到父级入口按默认主链重新裁决到 `分镜故事板` 或显式命中的唯一子路径 | 在父级 `子路径路由矩阵` 固化默认入口与分支关系 | 模糊请求稳定落到单一入口 |
| 执行者绕过已有文件，直接凭空发明 prompt 或镜头事实 | 输入契约层 | 退回读取 `编导/第N集.json`、`4-主体` 与已有 `5-画面` 产物，先锁权威输入 | 在父级 `Execution Summary` 与 `Chain Of Thought` 固化“只消费已有文件” | 新任务先列出权威输入再进入子路径 |
| `分镜帧` / `漫画` 被误当成 `分镜故事板` 下游 | 子路径关系层 | 重申三者是同源 sibling，而不是串行下游 | 在父级显式写出 `T1-mainline / T2-branch` 关系 | 单帧或漫画任务不再被要求先做 storyboard |
| 上游共享导演文件没有合法 `分镜组列表[] / 分镜明细[]` 却仍被推进到本阶段 | 输入契约层 | 先回到 `2-组间 / 3-明细` 补齐共享导演主文件 | 在父级输入真源合同中固化“无合法共享分镜数据不进 5-画面” | 错层输入可在父级被拦截 |
| 只出图片，不写 prompt 包、一致性说明或验收记录 | 输出契约层 | 补写 `validation-report.md` 与对应子路径 sidecar / manifest | 在父级 `output-template.md` 固化“图片不可脱离追溯” | 产物可回链 prompt、锚点与来源文件 |
| 产物路径继续沿用 ZEN-VOID 的 `output/影片/...` | 落点治理层 | 重写为 `projects/<项目名>/5-画面/...` | 在父级 `Canonical Landing` 固化当前仓路径真源 | 新文档与后续脚本不再引用旧路径 |
| `5-画面` 与上游 `1-分镜表现` 语义重叠，继续承担“重新定义分镜事实”的旧定位 | 阶段边界层 | 把父级定位改写为“围绕已有文件做 prompt 组合、一致性与生图” | 在根 `SKILL.md` 和思维链中固化“上游定事实、5-画面做图像化执行” | 阶段边界不再与上游重叠 |

## Repair Playbook

1. 先查上游 `编导/第N集.json` 是否已经具备合法 `分镜组列表[] / 分镜明细[]` 或等价画面锚点。
2. 再查 `4-主体/`、已有参考图、已有 `5-画面/` prompt / 图片里哪些文件应作为本轮权威输入。
3. 再查当前任务究竟是组级 storyboard、单帧还是漫画页。
4. 若只是“继续 5-画面”，默认先走 `分镜故事板`，但必须保留当前权威输入说明。
5. 若输入仍引用旧仓路径或旧阶段名，先修路径真源，再继续补本地内容。
6. 若子路径合同已补齐，记得回写 `aigc` 根技能状态，避免总入口继续把本阶段判为空壳。

## Reusable Heuristics

- `5-画面` 的主要复杂度不是“画什么”，而是“当前该消费哪些已有文件、该走哪一种画面类型、该怎么保持一致性”。
- 对当前仓来说，`projects/<项目名>/编导/第N集.json` 才是 `5-画面` 的第一事实源，结构口径固定遵循 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，不能在本阶段反向发明镜头事实。
- `分镜故事板` 是默认主入口；`分镜帧` 和 `漫画` 是同源分支，不要画成 storyboard 的下游。
- `5-画面` 的默认产物不应只是“图片”，而应是“prompt 包 + 一致性说明 + 图片/台账”的组合。
- 当阶段从空壳升级为真实父级合同后，必须把状态同步回根 `aigc` 技能。
- 当阶段合同开始承载过多字段、流程、路由与输出细则时，优先升级为 `SKILL.md + references/*.md` 的模块化真源结构，而不是继续在主合同里堆长表。
- 对多子路径父级阶段来说，思维链真源最先服务的不是叶子层产物细节，而是 `输入归属 -> 唯一路由 -> prompt/一致性 -> validation-report 闭环` 这条判断链。
- 对 `5-画面` 的叶子子技能来说，升级思维链时优先保住现有 `FIELD-SB-*` 接口与对象边界，再补 `模式与对象`、`Think-Think Design Snapshot`、`工具后反思` 和 `Gate Summary`，不要为了追新规范而改坏下游字段引用。

## Case Log

### Case-20260410-AIGC-VISUAL-STAGE-REPOSITION

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/5-画面` 从“分镜父级路由”重定位为“围绕已有文件进行多种画面类型 prompt 组合、一致性处理和图像生成”的阶段真源。
- root_cause_or_design_decision: 原 `5-分镜` 语义与上游 `3-明细/1-分镜表现` 有明显重叠，导致父级阶段容易被误用为重新定义镜头事实，而不是消费已有文件做图像化执行。
- final_fix_or_heuristic: 保留 `分镜故事板 / 分镜帧 / 漫画` 三个子路径不变，但把父级 `SKILL.md + references/*.md` 改写为“先锁已有文件，再裁决画面类型，再组合 prompt 与一致性，最后落盘与验收”的合同。
- prevention_or_replication_checklist:
- [x] 旧 `5-分镜` 阶段目录已改为当前 `.agents/skills/aigc/5-画面`
  - [x] 父级 `SKILL.md` 已改写为画面生成定位
  - [x] 父级 `references/*.md` 已同步改写
  - [x] 根 `aigc` 技能与直接上游回指已同步到 `5-画面`
- evidence_paths:
  - `.agents/skills/aigc/5-画面/SKILL.md`
  - `.agents/skills/aigc/5-画面/CONTEXT.md`
  - `.agents/skills/aigc/5-画面/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/references/execution-flow.md`
  - `.agents/skills/aigc/SKILL.md`
- user_feedback_or_constraint: 用户明确要求把原 `5-分镜` 重命名为 `画面`，并把语义调整为围绕已有文件展开的多画面类型提示词组合、一致性处理和图像生成。

### Case-20260409-AIGC-STORYBOARD-STAGE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/5-画面` 建立父级 `SKILL.md + CONTEXT.md`，并锁定三个 canonical 子路径。
- root_cause_or_design_decision: 当前仓 `aigc` 根技能已经把 `5-画面` 定义为“分镜故事板、分镜帧、漫画化表达”三路，但阶段目录与根经验层仍为空，导致根入口与阶段真源脱节。
- final_fix_or_heuristic: 以当前仓 `projects/<项目名>/3-明细 -> 4-主体 -> 5-画面` 主链为准，补齐父级边界、三路路由矩阵、阶段落点与经验层知识库，并把执行关系写成显式 `mainline + branch`。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补
  - [x] 父级 `CONTEXT.md` 已补
  - [x] 三个子路径已被父级显式路由
  - [x] 当前仓路径真源已改写为 `projects/<项目名>/5-画面/`
  - [x] 根技能状态待同步上收
- evidence_paths:
  - `.agents/skills/aigc/5-画面/SKILL.md`
  - `.agents/skills/aigc/5-画面/CONTEXT.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参考 `AIGC-ZEN-VOID` 的分镜能力，但目标落点必须改成当前仓 `aigc/5-画面` 及其根级真源。

### Case-20260409-AIGC-STORYBOARD-LATEST-NORM-REFRACTOR

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/5-画面` 从单文件重载合同重构为“主合同 + references 模块细则”的最新内容输出型规范结构。
- root_cause_or_design_decision: 父级 `5-画面` 已有稳定边界与路由语义，但字段主表、执行流程、路由矩阵与输出契约全部挤在单一 `SKILL.md` 中，已偏离当前仓 `1-规划`、`2-组间` 的 canonical 模块化结构。
- final_fix_or_heuristic: 保留既有阶段边界、默认入口、子路径关系与落点不变，只把详细细则下沉到 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md`，让根 `SKILL.md` 回到摘要式主合同。
- prevention_or_replication_checklist:
  - [x] 根 `SKILL.md` 已瘦身为主合同
  - [x] 四个 `references/*.md` 已补齐
  - [x] 路由、流程、字段与输出契约已有明确模块归属
  - [x] 原有 canonical landing 与 sibling 关系未改变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/SKILL.md`
  - `.agents/skills/aigc/5-画面/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/references/output-template.md`
- user_feedback_or_constraint: 用户要求“加载最新的规范，重构 `.agents/skills/aigc/5-画面`，不改变内容基础”。

### Case-20260409-AIGC-STORYBOARD-CHAIN-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/5-画面/references/chain-of-thought.md` 从旧版三张表升级为最新版 `think-think` 父级思维链合同。
- root_cause_or_design_decision: 旧版文件虽保留 `FIELD-SB-ROOT-01` 到 `04`，但缺少 `模式与任务对象`、`启发式工作链`、`三轴三重`、`可见快照分层`、`工具后反思` 与 `Gate Summary`，无法承载 `5-画面` 这种多子路径父级真正需要的唯一路由与阶段闭环判断。
- final_fix_or_heuristic: 保留原字段接口不变，把父级判断升级为“先锁 `[分镜N]` 与阶段归属，再裁决 `分镜故事板 / 分镜帧 / 漫画` 唯一路由，最后收口到 `projects/<项目名>/5-画面/` 与 `validation-report.md`”的 reasoning-friendly 合同。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与任务对象`
  - [x] 已补 `Think-Think Design Snapshot`
  - [x] 已补 `可见快照与隐藏推理分层`
  - [x] 已补 `工具后反思与 Gate Summary`
  - [x] 已保留 `FIELD-SB-ROOT-01` 到 `04` 不变
  - [x] 已就近补 `思维链设计报告`
- evidence_paths:
  - `.agents/skills/aigc/5-画面/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/reports/思维链设计报告-20260409.md`
  - `.agents/skills/aigc/5-画面/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“按照最新的思维链设计规范”优化父级 `chain-of-thought.md`，且应对齐 `think-think` 最新合同。

### Case-20260409-AIGC-STORYBOARD-LEAF-CHAIN-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板 / 分镜帧 / 漫画` 三个叶子子技能的 `references/chain-of-thought.md` 从旧版三张表统一升级为最新版 `think-think` 合同。
- root_cause_or_design_decision: 三个叶子子技能虽然已完成“主合同 + references 模块细则”重构，但 `chain-of-thought.md` 仍停留在 `Field Master / Thought Pass Map / Pass Table` 的旧形态，缺少 `模式与对象`、`启发式工作链`、`三轴三重`、`工具后反思` 与 `Gate Summary`，导致对象边界与返工闭环只能靠读者自行脑补。
- final_fix_or_heuristic: 保留各子技能既有 `FIELD-SB-*` 字段接口和对象边界不变，把叶子层判断升级为“先锁对象，再裁决成立条件，再收口到 JSON / manifest / 图片与 Gate”的 reasoning-friendly 可见合同。
- prevention_or_replication_checklist:
  - [x] 三个叶子 `chain-of-thought.md` 已补 `模式与对象`
  - [x] 三个叶子 `chain-of-thought.md` 已补 `Think-Think Design Snapshot`
  - [x] 三个叶子 `chain-of-thought.md` 已补 `工具后反思与 Gate Summary`
  - [x] 原 `FIELD-SB-SHEET-*`、`FIELD-SB-FRAME-*`、`FIELD-SB-COMIC-*` 接口保持不变
  - [x] 经验层已回写根 `5-画面/CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/reports/思维链设计报告-20260409.md`
- user_feedback_or_constraint: 用户明确要求使用 `think-think` 最新规范优化三个 `5-画面` 叶子子技能的思维链文件，且不应破坏现有子技能对象边界。

### Case-20260410-AIGC-VISUAL-STAGE-SHARED-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `5-画面` 父级与 `分镜故事板` 子技能的输入真源同步到 `projects/<项目名>/编导/第N集.json + director_episode_output.schema.json`。
- root_cause_or_design_decision: 上游统一输出模板已经改为 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，但 `5-画面` 仍把 `3-明细/第N集.md` 当成第一输入真源，导致父级共享规则会覆盖子技能的新口径。
- final_fix_or_heuristic: 保留 `5-画面` 的阶段落点与三子路径关系不变，只把父级 `SKILL.md + references/*.md` 和 `分镜故事板` 子技能一起改成“优先消费 `编导/第N集.json`，必要时回读 `3-明细/第N集.md` 做人工校对”的 shared-schema 口径。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已改成 shared schema 输入真源
  - [x] 父级 `references/execution-flow.md`、`references/type-strategies.md`、`references/chain-of-thought.md` 已同步 shared director JSON 口径
  - [x] `分镜故事板` 子技能与父级不再冲突
- evidence_paths:
  - `.agents/skills/aigc/5-画面/SKILL.md`
  - `.agents/skills/aigc/5-画面/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
- user_feedback_or_constraint: 用户要求由于上游输出内容模板改为 shared schema，因此同步调整 `5-画面/subtypes/1-提示词蒸馏/分镜故事板` 相关配置。
