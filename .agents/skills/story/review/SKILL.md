---
name: story-review
description: Use when the story workflow needs the parent guide skill for the review skill group, including validation routing, dimension roster loading, reviewer dispatch, aggregation, and PASS/FAIL gate ownership.
governance_tier: lite
---

# story / review

`review` 是 `story2026` 的技能组导引入口，不是第七个审查维度。

它负责组队、锁定输入 covenant、调度六个维度子技能、聚合维度证据，并写出卷级唯一验收 gate。各子技能只拥有自己的维度 verdict 与 sidecar report 权，不拥有最终 `validation_status` 判定权。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 若当前任务绑定 `projects/story/<项目名>/`，必须先读取项目根 `MEMORY.md`，再读取项目根 `CONTEXT/` 中与审查目标相关的上下文。
- 正式进入审查前必须读取 `_shared/validation-root-contract.md`、`_shared/validation-dimension-registry.yaml`、`_shared/validation-fact-pack-spec.md`、`_shared/validation-child-output-contract.md`。
- 若进入任一维度子技能，必须继续加载该子技能自己的 `SKILL.md + CONTEXT.md`。
- `CONTEXT.md` 只承载父层聚合、路由和失败模式经验，不得改写本文件的 gate ownership。

## When To Use

- 用户要求对小说卷、章节集合、初稿、润色稿或运行态产物做终验、质检、review、校验、验收。
- 需要判断 `validation_status`、`routing_decision`、`handoff_targets`、`rework_targets`。
- 需要把多个维度审查结果聚合成 `projects/story/<项目名>/review/第V卷.validation.json`。
- 需要解释或修复 review 技能组的 roster、维度权重、sidecar 文件名、review runner 路由或聚合门禁。
- `3-初稿` 或其他阶段需要调用 drafting inline hooks 时，按 registry 读取本技能组的维度定义。

## Input Contract

- Required input:
  - 项目根或项目名，能定位到 `projects/story/<项目名>/`。
  - 审查 mode：`final_acceptance`、`drafting_inline`、`repair_route` 或 `governance_repair`。
  - 卷号、章节范围或已有 `validation_fact_pack` 引用。
- Conditional input:
  - `final_acceptance` 必须能组装同一轮卷级 `validation_fact_pack`。
  - `drafting_inline` 必须提供当前 drafting step、章节快照和 registry hook 所需字段。
  - `repair_route` 必须提供既有 `第V卷.validation.json` 或等价 review 状态。
  - `governance_repair` 必须指出漂移对象：registry、shared contract、child skill、runner 或 schema。
- Reject or clarify when:
  - 无法定位项目根、卷号或受审文本。
  - 用户要求直接把 child sidecar 当作最终 PASS/FAIL。
  - 用户要求 review 父层直接改写正文、规划或 cards truth。

## Non Goals

- 不直接替代六个维度子技能做细项判断。
- 不生成正文、补写剧情、润色章节或改写上游 source truth。
- 不让任一 child sidecar 直接成为最终 PASS/FAIL gate。
- 不把 review 结果直接写回 `0-初始化 / 1-设定 / 2-卷章规划 / 3-初稿 / 4-润色` 的 canonical truth；回写必须经由对应 owning stage 或 `5-上下文回流` 的 handoff gate。

## Group Topology

当前 review 技能组由父导引入口和六个受治理子技能组成：

| 维度 | 子技能路径 | role_id | 默认职责 |
| --- | --- | --- | --- |
| 结构兑现 | `结构兑现/` | `structure-validator` | 检查 planning / promise 的事件、冲突、线索、伏笔和戏剧化义务是否被正文兑现 |
| 连续性 | `连续性/` | `continuity-validator` | 检查卷内承接、章节转场、threads 和压力线是否持续可追踪 |
| 逻辑自洽校验 | `逻辑自洽校验/` | `logic-validator` | 检查因果链、状态、能力边界、世界规则、例外代价与 source truth 归因 |
| 人物一致性 | `人物一致性/` | `character-validator` | 检查人物行为、动机、关系压力、成长承接与对白声口 |
| 时间线 | `时间线/` | `timeline-validator` | 检查时间锚、事件顺序、持续时长与伏笔静默窗口 |
| 任务汇聚 | `任务汇聚/` | `task-convergence-validator` | 检查卷级/章级任务是否从属于主任务并完成汇聚、转挂或显式保留开放 |

维度名单、权重、drafting hook 与 sidecar 文件名的单一真源是 `_shared/validation-dimension-registry.yaml`。本表只作入口导览；发生冲突时以 registry 为准，并同步修正本表。

## Canonical Sources

- 父层入口：`SKILL.md`、`CONTEXT.md`
- root gate 合同：`_shared/validation-root-contract.md`
- 维度 roster 真源：`_shared/validation-dimension-registry.yaml`
- 输入包规范：`_shared/validation-fact-pack-spec.md`
- child 输出合同：`_shared/validation-child-output-contract.md`
- 输出 schema：`_shared/checker-output-schema.md`
- 聚合模板：`_shared/validation-aggregate.template.json`
- 维度报告模板：`_shared/validation-dimension-report.template.md`
- 团队共享规则：`_shared/validation-team-contract.md`

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 确认最终 gate ownership、写入路径、覆盖规则 | `_shared/validation-root-contract.md` |
| 确认维度名单、权重、role_id、sidecar 文件名、drafting hooks | `_shared/validation-dimension-registry.yaml` |
| 构建或校验审查输入包 | `_shared/validation-fact-pack-spec.md` |
| 校验子技能输出是否可聚合 | `_shared/validation-child-output-contract.md`、`_shared/checker-output-schema.md` |
| 生成父层 aggregate JSON | `_shared/validation-aggregate.template.json` |
| 生成维度 sidecar 报告 | `_shared/validation-dimension-report.template.md` |
| 解释 reviewer 团队共享规则 | `_shared/validation-team-contract.md` |
| 执行某个维度判断 | 对应子目录的 `SKILL.md + CONTEXT.md` |

## Invocation Modes

| mode | 触发信号 | 默认动作 | 输出 |
| --- | --- | --- | --- |
| `final_acceptance` | 卷级终验、整卷 review、PASS/FAIL gate、进入润色或回流前验收 | 锁定同一轮 `validation_fact_pack`，按 registry 调度所有 `final_acceptance.mandatory=true` 的维度，聚合为唯一卷级 JSON | `review/第V卷.validation.json` 与各维度 sidecar |
| `drafting_inline` | `3-初稿` 指定 step hook 触发即时审查 | 按 registry 中当前 step 的 enabled checkpoints 只调度命中的维度，返回阻断、回退或继续信号 | inline dimension packet，不直接写最终 gate |
| `repair_route` | 已有 review 失败，需要判断返工归属 | 读取 aggregate JSON，按 `source_layer_owner / rework_targets / handoff_targets` 分流 | 返工路由建议 |
| `governance_repair` | roster、schema、runner、sidecar 文件名或合同漂移 | 以 registry 和 shared contracts 为真源同步修复 | 技能组结构或合同补丁 |

## Dispatch Contract

- `final_acceptance` 默认采用技能组并行审查语义：每个 mandatory 维度对应一个独立 reviewer / child skill 结果，再由父层聚合。
- 在仓库治理语义中，review 技能组属于已声明 reviewer runtime 的任务，默认应真实启动子 reviewer；若当前会话上层策略、工具或用户指令阻断真实 dispatch，必须显式报告降级来源、原本应启动的维度、实际采用的降级路径。
- `drafting_inline` 只调度 registry 命中的维度，不得为了结构完整性补空维度或虚构未执行的 child packet。
- 子技能输出必须是局部维度 packet 与 sidecar，不得写父层 aggregate JSON。
- 父层聚合时只消费本轮真实调度并通过 schema 校验的维度结果。

## Root Gate Ownership

父层 `review` 独占以下最终 gate 字段：

- `validation_status`
- `validation_mode`
- `volume_ref`
- `chapter_refs`
- `selected_agents`
- `overall_score`
- `dimension_scores`
- `issues`
- `chapter_issue_index`
- `severity_counts`
- `critical_issues`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `validation_ref`

硬规则：

- 每一轮卷级终验只能写一份 `projects/story/<项目名>/review/第V卷.validation.json`。
- 维度 sidecar 与 aggregate JSON 冲突时，以 aggregate JSON 为 gate 真源，并在下一轮前修正 child output contract。
- `5-上下文回流` 只能消费 aggregate JSON 中的 PASS 与 handoff，不得直接消费某个维度 sidecar 作为回写授权。

## Output Contract

- Required output:
  - `final_acceptance` 必须产出父层 aggregate JSON；有维度问题时必须保留 issue、severity、source owner、rework target 与 handoff 信息。
  - 各 mandatory 子技能应产出对应 `review/第V卷/<维度名>.md` sidecar。
- Output format:
  - 父层 gate 使用 JSON，字段遵循 `_shared/validation-aggregate.template.json` 与 `_shared/checker-output-schema.md`。
  - 维度报告使用 Markdown，格式遵循 `_shared/validation-dimension-report.template.md`。
- Output path:
  - 父层 gate：`projects/story/<项目名>/review/第V卷.validation.json`
  - 维度证据：`projects/story/<项目名>/review/第V卷/<report_filename>`
- Naming convention:
  - 卷号使用中文卷序：`第V卷.validation.json`、`第V卷/结构兑现.md` 等。
  - `report_filename` 由 `_shared/validation-dimension-registry.yaml` 单点定义。
- Completion gate:
  - mandatory 维度已按 registry 调度或已明确记录降级原因。
  - 父层 aggregate JSON 已生成并能解释 PASS/FAIL、返工归属和 handoff。
  - 不存在 child sidecar 覆盖父层 gate 的情况。

## Lite Field Mapping

| field_id | step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `FIELD-REVIEW-01` | `N1-INTAKE` | 锁定项目、卷号、mode 与输入包 | `review_scope`、`validation_fact_pack_ref` | `FAIL-REVIEW-INTAKE` | 回到输入包规范与项目根加载 |
| `FIELD-REVIEW-02` | `N2-ROSTER` | 按 registry 选择本轮维度 | `selected_agents` | `FAIL-REVIEW-ROSTER` | 回到 `validation-dimension-registry.yaml` |
| `FIELD-REVIEW-03` | `N3-DISPATCH` | 调度子技能并收集 packets | `dimension_packets`、`dispatch_notes` | `FAIL-REVIEW-DISPATCH` | 回到 child `SKILL.md + CONTEXT.md` |
| `FIELD-REVIEW-04` | `N4-SCHEMA-GATE` | 校验 child 输出可聚合 | `schema_validation_result` | `FAIL-REVIEW-SCHEMA` | 回到 child output contract 与 checker schema |
| `FIELD-REVIEW-05` | `N5-AGGREGATE` | 生成唯一父层 gate | `第V卷.validation.json` | `FAIL-REVIEW-AGGREGATE` | 回到 validation root contract |
| `FIELD-REVIEW-06` | `N6-ROUTE` | 输出返工、handoff 或 PASS 路由 | `routing_decision`、`handoff_targets`、`rework_targets` | `FAIL-REVIEW-ROUTE` | 回到 source trace 与 aggregate fields |

## Root-Cause Execution Contract

当 review 出现错误时，必须沿以下链路上溯：

`Symptom -> Direct Cause -> Dimension Or Parent Owner -> Shared Contract -> Story Root Contract -> Meta Rule Source`

优先修复顺序：

1. gate ownership 错误：先修 `_shared/validation-root-contract.md` 与父 `SKILL.md`。
2. 维度名单、权重、sidecar 文件名或 hook 漂移：先修 `_shared/validation-dimension-registry.yaml`。
3. 子技能输出不可聚合：先修 `_shared/validation-child-output-contract.md` 与对应 child `SKILL.md`。
4. 输入包缺字段：先修 `_shared/validation-fact-pack-spec.md`，再追上游 source owner。
5. 返工归属不清：先补 aggregate 中 `source_layer_owner / rework_targets / handoff_targets`。

## Completion Gate

- 已能把任一 review 请求路由到 `final_acceptance / drafting_inline / repair_route / governance_repair`。
- 已按 registry 明确本轮应启动哪些维度。
- 已区分父层 gate truth 与 child sidecar evidence。
- 已能说明 PASS 后是否允许进入 `4-润色` 或 `5-上下文回流`。
- 已能在失败时给出最早 source owner 与可执行返工入口。
