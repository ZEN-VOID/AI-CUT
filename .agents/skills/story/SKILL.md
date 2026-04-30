---
name: story2026
description: "Use when coordinating story2026 novel projects across init, cards, planning, draft, polish, review, or return."
governance_tier: lite
skill_role: parent_guide
allowed-tools: Read Grep Bash Write Edit Task
---

# story2026

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载跨阶段经验层，不得覆盖本 `SKILL.md` 的总线路由与真源边界。
- 若 `CONTEXT.md` 与当前目录结构不一致，先修根级真源，再继续下游阶段。

## Overview

`story2026` 根级 skill 是整条小说流水线的总入口与总线合同。

它只统一回答四件事：

1. 当前诉求应该路由到哪个阶段 skill。
2. 哪一层才是这类问题的 canonical truth。
3. 根级 `_shared`、`scripts`、`templates` 分别承担什么共享职责。
4. 题材方向盘如何通过 `0-初始化/north_star.yaml.genre_contract` 进入 planning / drafting / review / return。

硬边界：

- 根级 `story/SKILL.md` 只负责跨阶段拓扑、共享载体边界、总路由和根因追溯总则。
- 各阶段目录下的 `SKILL.md` 负责本阶段的严格执行合同。
- `repair/SKILL.md` 负责局部修改牵动整体时的影响判型、source-first 修复计划、跨阶段分流和验收；根层只路由到 repair，不复制 repair 的类型化矩阵。
- 根级 `CONTEXT.md` 只沉淀跨阶段经验，不吞并阶段私有故障模式。

## 类型机制

`story` 现在采用：

- 固定前置主链
- 卷级创作闭环
- 人工维护的 `north_star.yaml.genre_contract`
- 三模型交叉分工

三层架构。

### 三模型交叉分工

核心创作阶段默认采用三模型交叉使用机制：

| 模型 / lane | 默认职责 | 典型阶段 | 不默认承担 |
| --- | --- | --- | --- |
| GPT / `A-GPT原生` | 总领、结构化、初始化、设定、卷章规划、问题发现、review 归因、任务调度、repair brief、跨阶段裁决 | `0-初始化`、`1-设定`、`2-卷章`、`review`、`query/resume`、返工分流 | 默认不承担 `3-初稿` 正文主写，也不把 GPT 直接改稿冒充 B/C provider 输出 |
| Doubao / `B-Doubao流` | 中文友好、人话、网文气口、章节初稿主写 | `3-初稿` 默认 lane | 默认不承担润色阶段的整章二次调优 |
| DeepSeek / `C-Deepseek流` | 长思维链、二次判断、最小局部修补、润色阶段事实锚定与分布保持 | `4-润色` 默认 lane | 默认不承担初稿主写，除非用户显式点名 DeepSeek 起草 |

硬规则：

- 默认正文主创链路为 `Doubao 初稿 -> DeepSeek 最小局部修补`。
- GPT 是总领与诊断调度层，不得在未显式切换 lane 时直接改写 B/C 正文并继续标记为原 provider。
- 若用户显式点名模型或 lane，按用户显式指令优先；但必须同步更新产物 frontmatter、sidecar 证据和 review 返工归属。

### 固定前置主链

前置主链固定不变：

1. `0-初始化`
2. `1-设定`
3. `2-卷章`

进入正文生产后，默认按卷执行创作闭环，而不是把全书多卷同时推进到同一阶段。

### 卷级创作闭环

每卷默认闭环固定为：

1. `3-初稿`
2. `review` 初稿验收
3. `4-润色`
4. `review` 终稿验收
5. `return`
6. 下一卷 `3-初稿`

硬规则：

- `return` 不是全本润色后的线性终章；它是每卷最终验收后的 validated actualization checkpoint。
- `return` 不因“检验完成”自动触发，只能在 `review/第V卷.validation.json` 同时满足 `validation_status == PASS`、`routing_decision == handoff_to_review_and_context_return`、`handoff_targets` 包含 `return`（兼容旧 `context-return`）时进入。
- 上下文回流必须消费“最终被接受的本卷实绩”。默认应以润色后再次 review PASS 的 `4-润色/第V卷/*` 为 accepted manuscript；若项目明确跳过润色，aggregate 必须显式声明 `accepted_manuscript_stage = 3-初稿`，不得把仍可能被润色改动的初稿态直接 actualize。
- canonical 正文生产不建议多卷并发：第 V+1 卷正式起草前，应先让第 V 卷完成 PASS + 上下文回流，使下一卷消费 validated actual，而不是过期 planning。

### 人工题材契约

题材机制不再依赖旧的“系统自动题材装配”机制。

当前规则固定为：

- `0-初始化/north_star.yaml.genre_contract` 是唯一题材方向盘真源。
- `1-设定` 不再单独设置 `类型卡`。
- `2-卷章` 只导入 `story_promise / genre_corridor / navigation_rules`，不再二次猜题材。
- `3-初稿` 只消费人工题材承诺与 planning handoff，不再消费自动 step hook。
- `review` 继续做结构/连续性/逻辑/人物/时间线/任务汇聚校验，不再保留独立自动类型兑现维度；默认后台启用 `code-reviewer` 做独立审计，再把 findings 回流为修复分流。
- `4-润色` 可以沉淀反馈，但不得自动改写 `north_star.yaml.genre_contract`。
- `return` 只承接终稿 PASS 且明确 handoff 的 validated actualization，不回写规划正文。

硬规则：

- 通用基座必须能在没有任何题材包目录的情况下独立运行。
- 题材判断默认属于人工创作层，不得再被系统隐式反向硬绑。
- 若题材方向发生变化，优先修改 `north_star.yaml.genre_contract`，不要在 downstream 阶段静默偷改。

## When to Use

- 用户只说“用 story2026 做这件事”，但还没有明确该进哪一个阶段。
- 需要设计、选择或解释某个项目的题材方向盘。
- 需要判断某个问题应归 `0-初始化 / 1-设定 / 2-卷章 / 3-初稿 / 4-润色 / repair / review / return / query / resume` 中的哪一层。
- 需要修复跨阶段路由、共享 reference、共享脚本、真源分工、运行态数据流的源层问题。

## Input Contract

- Accepted input: 泛化 story2026 请求、跨阶段路由问题、真源归属判断、共享路径/脚本/模板修复、项目运行时定位问题。
- Required input: 用户诉求文本，或可定位的项目根 `projects/story/<项目名>/`，或需要审计/修复的 story 技能树路径。
- Optional input: 卷号、章号、目标阶段、错误日志、现有项目 `STATE.json`、`MEMORY.md`、`CONTEXT/` 与报告路径。
- Reject or reroute when: 影视/电影/视频项目初始化请求应路由到 `.agents/skills/aigc/0-初始化/SKILL.md`；阶段内部创作细则必须交给 owning stage。

## System Topology

### Mainline Topology

前置主链固定为：

1. `0-初始化`
2. `1-设定`
3. `2-卷章`

正文生产从这里开始按卷循环：

`第V卷初稿 -> review -> 第V卷润色 -> review -> PASS + handoff -> return -> 第V+1卷初稿`

执行原则：

- 前置主链默认按阶段顺序串行，不得跳过上游真源直接伪造下游结论。
- 卷级正文生产默认一卷一卷推进；多卷并发只允许作为探索草稿、素材准备或非 canonical 支线，不得写成 validated final。
- `review` 不再是序号化主链的一环；它是多环节自动触发的审查层，可由初稿完卷、润色返工、恢复续跑、质量查询或维护任务触发。
- `4-润色` 只在 `review = PASS` 且 handoff 明确授予 `4-润色` 后拥有 validated truth writeback 权。
- `return` 只在终稿 review aggregate 明确授予 `handoff_to_review_and_context_return` 后执行；它不是“检验完自动执行”的默认副作用。

### Workflow Map

```mermaid
flowchart TD
    A["用户诉求 / story2026 总入口"] --> B{"根级路由与真源判定"}
    B --> C["0-初始化<br/>north_star.yaml.genre_contract"]
    C --> D["1-设定<br/>角色 / 场景 / 物品对象真源"]
    D --> E["2-卷章<br/>部级 / 卷级 / 章级规划真源"]
    E --> F["第V卷 3-初稿<br/>候选正文"]
    F --> G1["review<br/>初稿验收 / 第V卷.validation.json"]
    G1 -->|"FAIL / 修复分流"| F
    G1 -->|"PASS + handoff: 4-润色"| H["第V卷 4-润色<br/>最小局部修补稿"]
    H --> G2["review<br/>终稿验收 / 第V卷.validation.json"]
    G2 -->|"FAIL / 修复分流"| H
    G2 -->|"PASS + handoff_to_review_and_context_return<br/>handoff_targets includes return"| I["return<br/>accepted actualization / projection refresh"]
    I --> L["第V+1卷 3-初稿<br/>消费 validated actual"]
    J["query / resume"] -.状态查询 / 续跑.-> B
    K["4-润色/C-DeepSeek流"] -.默认最小局部修补.-> H
```

### Checkpoint And Satellite Skills

无序号 checkpoint / satellite 技能固定挂在主链侧，不单独冒充新的 numbered stage：

- `review`
- `return`
- `query`
- `resume`
- `repair`

### Skill Completion State Hook

无论通过 workflow CLI 还是普通 skill / 子技能直接执行，只要本轮对 `projects/story/<项目名>/` 产生阶段性完成、失败或清理结果，都必须同步写入项目状态：

```bash
python3 .agents/skills/story/scripts/workflow_manager.py record-skill-completion \
  --project-root "projects/story/<项目名>" \
  --skill-id "<story skill id 或技能包路径>" \
  --status completed \
  --artifacts '{"outputs":["相对项目根的产物路径"]}'
```

硬规则：

- `record-skill-completion` 是普通 skill / 子技能执行的最小状态落点；不得只在对话里宣布完成。
- 子技能单独调用时也必须执行该 hook；脚本会把 `story-cards-*`、`story-plan-*`、`story-drafting-*`、`story-polishing-*` 或含 `1-设定 / 2-卷章 / 3-初稿 / 4-润色` 的技能路径归并到对应阶段。
- 状态写入目标固定为 `projects/story/<项目名>/STATE.json#workflow_runtime.execution_state.stage_progress`，并同步追加 `history`、`task_log` 与 `governance_index`。

## Root Truth Ownership Contract

| 层 | 拥有的真源 | 不拥有的真源 |
| --- | --- | --- |
| 根级 `story2026` | 跨阶段拓扑、总路由、共享载体边界、默认加载顺序 | 各阶段内部执行细则、局部 reference 专业判断 |
| `0-初始化` | 立项合同、`0-初始化/*.yaml`、初始 seeds | 对象真源、规划真源、validated actualization |
| `1-设定` | 类型/角色/场景/物品/技能等对象真源 | 章节编排真源、章节审查判断 |
| `2-卷章` | 以 `1-部级 -> 2-卷级 -> 3-章级` 的三层分形结构持有 `2-卷章/整体规划.md`、`2-卷章/第N卷/卷规划.md`、`2-卷章/第N卷/第N章.md` 这组规划真源；`全息地图.json / 卷分片/*.json` 仅作兼容投影 | 对象当前态、validated actualization |
| `3-初稿` | 以 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 作为章节正文唯一业务真源，由 `3-初稿` 父级导引层选择 A/B/C provider lane 执行；卷级写作日志等运行时工件仅作兼容 carrier，不再定义主创拓扑 | 评估判断权、validated truth writeback |
| `review` | `validation_fact_pack` covenant、卷级隔离评估、父层 `review/第V卷.validation.json` 聚合 gate、审查报告与状态持久化 | actualization 写回 |
| `4-润色` | 基于 `3-初稿/第N卷/第N章.md` 的最小局部修补稿、`4-润色/第N卷/第N章.md`、润色 sidecar | `3-初稿` 原文覆盖权、planning/cards/north_star 真源、validation PASS/FAIL 判定权、默认整章重写权 |
| `repair` | 局部修改的 impact map、typed scope package selection、canonical owner 判定、source-first repair plan、跨阶段修复分流、code-reviewer 验收汇流 | 设定/规划/正文/润色的主创真源、review PASS 判定、return actualization 写回；repair 类型化矩阵不由根层复制 |
| `return` | 终稿 PASS-gated actualization artifact、accepted manuscript refs、Cards current_state/history、规划 actualization sidecar、story_map actualization、项目 `CONTEXT/` carryover notes、`STATE.json` projection refresh | 规划正文改写、审查判定、正文/润色正文创作、把未被终稿验收接受的初稿态 actualize |
| `query / resume` | 查询、恢复 | 主链 canonical truth 判定权 |

## Canonical Runtime Root

- 书项目正式业务根目录：`projects/story/<项目名>/`
- legacy `projects/aigc/<项目名>/` 仅允许作为兼容 fallback，不再是 canonical runtime。
- 根层项目入口文件固定写在：
  - `projects/story/<项目名>/STATE.json`
  - `projects/story/<项目名>/team.yaml`
  - `projects/story/<项目名>/MEMORY.md`
  - `projects/story/<项目名>/CHANGELOG.md`
  - `projects/story/<项目名>/CONTEXT/`

## Shared Carrier Contract

### 根级 `_shared/`

根级 `_shared/` 是当前 `story` 技能树的跨阶段共享真源层。

默认先读：

- `_shared/context-loading-contract.md`
- `_shared/core-constraints.md`

按需读取：

- `_shared/story_map.schema.json`
- `_shared/story_map_bootstrap.template.json`
- `_shared/entity-management-spec.md`
- `_shared/strand-weave-pattern.md`

可选增强材料：

- `_shared/genre-profiles.md`
- `_shared/reading-power-taxonomy.md`
- `_shared/cool-points-guide.md`

### 根级 `scripts/`

根级 `scripts/` 是 story2026 的共享脚本入口层，负责：

- canonical path helper
- workflow / state / status 管理
- shared CLI entrypoint
- 多阶段共用的数据访问与校验

### 根级 `templates/`

根级 `templates/` 只放跨阶段或跨模块共享模板、共享 schema 载体。

## Routing Contract

| 用户诉求 / 问题形状 | 默认入口 |
| --- | --- |
| 设计/选择/解释题材方向盘 | 根级 `story2026`，必要时修订 `0-初始化/north_star.yaml.genre_contract` |
| 初始化小说、初始化网文、新建书、新建长篇故事、小说项目起盘 | `0-初始化` |
| 初始化影片、初始化电影、初始化影视、初始化视频项目 | 不进入 story；route to `.agents/skills/aigc/0-初始化/SKILL.md` |
| 新建项目、确定创作立项、初始化问卷/顾问团 | `0-初始化` |
| 角色卡/场景卡/物品卡生成、回写、覆盖率修复 | `1-设定` |
| 全局设定/整书风格/类型方向盘修订 | `0-初始化/north_star.yaml` |
| 长篇规划、MAP、章节编排、冲突/任务/线索/伏笔设计 | `2-卷章` |
| 写章节、章节级执行包、从 planning 直接产出正文 | `3-初稿` |
| 承接已有 `3-初稿` 做最小局部修补、中文表达局部校准、题材质感微调，并输出到 `4-润色/第N卷/第N章.md` | `4-润色` |
| 明确要求“按章写正文”、输出到 `3-初稿/第N卷/第N章.md`、或要求 YAML 头携带 global/style/`north_star` 摘要 | `3-初稿` |
| 隔离评估、checker 团队、`validation_status`、审查报告、评分落库、审查结果持久化 | `review` |
| 终稿 PASS 且 `routing_decision == handoff_to_review_and_context_return`、`handoff_targets` 包含 `return`（兼容旧 `context-return`）后的 actualization、truth writeback、projection refresh | `return` |
| 查询当前态、规划态、实绩态、质量态 | `query` |
| 查看断点、续跑、清理或重启任务 | `resume` |
| 指定局部修改但可能牵动设定、规划、前后章节、已产物、后续生成、review 或 return actualization 的一致性修复 | `repair`；进入后必须由 repair 加载 `types/type-map.md` 与 `references/impact-scope-contract.md#Universal Type Matrix` |
| 中文小说润色、去 AI 检测规整化风险、保留初稿骨架的最小局部修补 | `4-润色/C-Deepseek流` |
| 明确要求整稿统修、整章重写、换模型重润或 Doubao/GPT 润色 | `4-润色` 后按显式 lane 路由 |

## Default Loading Order

1. 先读取根级 `SKILL.md`，锁定跨阶段拓扑与共享层边界。
2. 再读取根级 `CONTEXT.md`，避免重复踩跨阶段老坑。
3. 若当前任务已绑定 `projects/story/<项目名>/`，必须先读取 `projects/story/<项目名>/MEMORY.md`，再读取 `projects/story/<项目名>/CONTEXT/` 下与本轮相关的项目级上下文文件。
4. 若问题涉及共享合同，先读根级 `_shared/context-loading-contract.md` 与对应阶段的 `_shared/*`。
5. 若当前项目已锁定题材方向盘，优先读取 `0-初始化/north_star.yaml.genre_contract` 与 `2-卷章/整体规划.md`；如项目仍在兼容态，再回退到 `全息地图.json`。
6. 若当前诉求涉及终验或 actualization，继续读取：
   - `review/_shared/validation-fact-pack-spec.md`
   - `return/references/context-return-spec.md`
   - 并确认 aggregate 指向最终 accepted manuscript，默认是 `4-润色` 终稿。
7. 若路由到 `repair`，读取 `repair/SKILL.md + repair/CONTEXT.md`，再读取 `repair/types/type-map.md`、命中的 `repair/types/scope/*.md` 与 `repair/references/impact-scope-contract.md`；项目特例只从项目 `CONTEXT/` 或 `MEMORY.md` 追加。
8. 路由到目标阶段或卫星技能的 `SKILL.md`。
9. 读取目标阶段或卫星技能的 `CONTEXT.md`。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 根级共享合同 | `_shared/context-loading-contract.md`、`_shared/core-constraints.md` |
| 跨阶段路由和执行拓扑 | 本文件 `System Topology` 与目标阶段 `SKILL.md + CONTEXT.md` |
| 局部修改牵动整体、repair 判型和影响图 | `repair/SKILL.md + repair/CONTEXT.md`、`repair/types/type-map.md`、命中的 `repair/types/scope/*.md`、`repair/references/impact-scope-contract.md` |
| 质量门禁和审计 | `review/SKILL.md + CONTEXT.md`、目标阶段审查合同 |
| 请求判型 | 本文件 `Routing Table`、目标阶段 `Mode Selection` 与 `CONTEXT.md` Type Map |
| 可复用经验 | `CONTEXT.md` |
| 输出摘要 | 对话或用户指定 `reports/` 路径 |
| 共享 CLI 和路径解析 | `scripts/story.py`、`scripts/project_locator.py` |
| 产品侧入口 | `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml` |
| 父级导引最小结构 | 本父级导引 skill 只要求同目录 `SKILL.md + CONTEXT.md`；真实执行细则、模板、类型包和 review gate 由被路由到的阶段 skill 或卫星 skill 持有 |

## Root-Cause Execution Contract (Mandatory)

当 `story2026` 出现跨阶段路由错误、真源分工混乱、共享 reference 漂移、共享脚本路径失配、根入口缺失或总线合同断裂时，必须按以下链路上溯：

1. `Symptom / Failure`
2. `Direct Technical Cause`
3. `Rule Source`
4. `Meta Rule Source`
5. `Fix Landing Points`

执行顺序硬约束：

- 先修总线真源，再修阶段投影。
- 若同一条规则需要在两个以上阶段重复改写，必须先判断是否缺少根级 canonical source。

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| FIELD-SYS-ROUTING-01 | Step 1 | 判定当前诉求属于哪个阶段与 truth role | `target_stage`、`truth_role` | FAIL-SYS-ROUTING-01 | 回到路由表，先判真源再判阶段 |
| FIELD-SYS-CARRIER-02 | Step 2 | 判断应读取哪些根级共享 carrier | `shared_refs_to_load`、`shared_scripts_needed` | FAIL-SYS-CARRIER-02 | 回到根级 `_shared/*.md` 与共享层边界合同 |
| FIELD-SYS-TYPECARD-03 | Step 3 | 判断当前项目的题材方向盘是否已被 `north_star.yaml.genre_contract` 正式承接 | `genre_contract_ref`、`story_promise_summary`、`genre_corridor_summary` | FAIL-SYS-TYPECARD-03 | 回到 `0-初始化/north_star.yaml` 与 `2-卷章` 导入链 |
| FIELD-SYS-OWNER-04 | Step 4 | 锁定该问题的 canonical owner | `canonical_owner`、`non_owner_layers_to_avoid` | FAIL-SYS-OWNER-04 | 回到真源分工表，禁止让下游冒充上游 |
| FIELD-SYS-TRACE-05 | Step 5 | 完成跨阶段 root-cause trace | `symptom`、`direct_cause`、`rule_source`、`meta_rule_source` | FAIL-SYS-TRACE-05 | 重新补全分层 trace，不能停在局部症状 |
| FIELD-SYS-CLOSURE-06 | Step 6 | 产出修复闭环与防回归结果 | `root_cause_location`、`immediate_fix`、`systemic_prevention_fix` | FAIL-SYS-CLOSURE-06 | 回到修复落点，优先改根级真源 |

## Output Contract

- Required output: `target_stage`、`truth_role`、`canonical_owner`、`shared_refs_to_load`、`next_action`，或跨阶段修复摘要。
- Output format: 简短路由报告、修复报告或 `templates/output-template.md` 对齐的结构化摘要。
- Output path: 默认输出到对话；用户要求保存时写入 `reports/story-router-YYYYMMDD.md` 或任务指定报告路径。
- Naming convention: 报告文件使用 kebab-case 与 `YYYYMMDD` 日期后缀；路径示例必须保持 ASCII 安全任务 ID。
- Completion gate: 请求已路由到唯一默认入口，canonical truth 与非 owner 层已区分，必要的 `SKILL.md + CONTEXT.md` 加载边界已说明。

## Completion Gate

- 已能明确把任一泛化 `story2026` 请求路由到唯一默认入口。
- 已能说明该请求应读的 canonical truth 与不该误读的非真源层。
- 已区分根级 `_shared`、`scripts/`、`templates/` 的共享职责。
- 已能说明当前项目的题材方向盘如何从 `north_star.yaml.genre_contract` 进入 planning / drafting / validation。
- 已能指出 repo 级 `.codex/` 真源与项目级 `STATE.json.workflow_runtime` 内联工件链的分工。
- 已能说明 planning root/slice 的分工、`validation_fact_pack` 的 covenant，以及 上下文回流 的 PASS+handoff gate。
