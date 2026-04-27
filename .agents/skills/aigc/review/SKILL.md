---
name: aigc-review
description: Use when the active AIGC workflow needs checkpoint, stage, or release review aggregated into one governed review packet.
governance_tier: full
metadata:
  short-description: AIGC governed review bus
---

# aigc / review

`aigc-review` 是 `.agents/skills/aigc` 的 review 卫星技能包。它不进入主阶段串行链，不替代 `0-初始化` 到 `7-视频` 的业务产物，只负责把 checkpoint、stage acceptance 与 package release 的审计事实收束为唯一 aggregate review packet。

## Context Loading Contract

- 每次调用 `$aigc-review` 时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若任务绑定 `projects/aigc/<项目名>/`，先加载项目根 `MEMORY.md` 与相关 `CONTEXT/`，再进入 review mode。
- 父层必须先读取 `references/review-root-contract.md`、`references/review-child-output-contract.md`、`references/review-fact-pack-spec.md`、`references/dimensions/*.md` 与 `_shared/review-dimension-registry.yaml`。
- `_shared/` 保留给 `scripts/aigc_review_runner.py` 和旧链路兼容；Skill 2.0 规范入口以 `references/`、`steps/`、`review/`、`types/`、`templates/` 为准。

## Input Contract

Accepted input:

- checkpoint 审计点、阶段总验、跨阶段 handoff review、package release gate。
- 需要把阶段问题结构化聚合成 repair route 的请求。
- `scripts/aigc_review_runner.py` 生成或读取的 `review_fact_pack`、aggregate packet、repair sidecar。

Required input:

- 项目根或项目名，对应 `projects/aigc/<项目名>/`。
- `review_mode`：`checkpoint_inline`、`stage_acceptance` 或 `package_release`。
- 对 `checkpoint_inline` 必须提供 `checkpoint_id`；对 `stage_acceptance` 必须提供 stage；对 `package_release` 必须提供 `scope_ref`。

Reject or clarify when:

- 用户要求 review 直接改写阶段 canonical 业务文件。
- 缺少项目根且无法从上下文定位。
- 需要人工审美/叙事重写时，应回到对应阶段 skill，而不是在 review 父层主创。

## Mode Selection

| mode | trigger | aggregate path |
| --- | --- | --- |
| `checkpoint_inline` | 阶段节点刚写出 canonical 输出，需要 handoff 前审计 | `projects/aigc/<项目名>/review/checkpoints/<checkpoint_id>/<scope_ref>.review.json` |
| `stage_acceptance` | 需要判断某一阶段能否放行 | `projects/aigc/<项目名>/review/stages/<stage>/<scope_ref>.review.json` |
| `package_release` | 当前集、当前包或项目准备跨阶段交付 | `projects/aigc/<项目名>/review/releases/<scope_ref>.review.json` |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 根 gate、落点、字段权属 | `references/review-root-contract.md` |
| 维度输出协议 | `references/review-child-output-contract.md` |
| fact pack 最小字段与 required slice | `references/review-fact-pack-spec.md` |
| 六维审计细则 | `references/dimensions/*.md` |
| review 执行拓扑 | `steps/review-workflow.md` |
| checkpoint / stage / package 判型 | `types/review-type-map.md` |
| 质量门禁与 provider 降级 | `review/review-gate.md` |
| 输出渲染模板 | `templates/output-template.md` |
| 可复用经验 | `knowledge-base/review-heuristics.md` |
| runner 兼容配置 | `_shared/*.yaml`、`_shared/*.json`、`_shared/*.md` |
| 产品侧入口 | `agents/openai.yaml` |

## Execution Contract

1. 锁定项目根、`review_mode`、`scope_ref` 和唯一 aggregate packet 落点。
2. 按 `types/review-type-map.md` 判定本轮需要的 checkpoint、stage 或 release 维度。
3. 按 `references/review-fact-pack-spec.md` 组装同一份 `review_fact_pack`；若 required slice 缺失，直接 `FAIL-COVENANT`。
4. 按 `_shared/review-dimension-registry.yaml` 选择 mandatory dimensions，并加载其 `dimension_spec_ref` 指向的 `references/dimensions/*.md`。
5. 若 `review_fact_pack` required slice 缺失，直接写 `FAIL-COVENANT` aggregate packet 与 repair plan，不进入 provider 或维度审计。
6. 在上层策略允许时，使用 `review/review-gate.md` 声明的 provider 路径；若真实 subagent/provider 被阻断，降级为本地 checklist 并在 packet 中记录。
7. 聚合 `dimension_packet + dimension_report_ref + dimension_runtime`，写出唯一 aggregate review packet。
8. 若未通过，写 `*.review.repair.json`，并在 `governance-state.yaml` 存在时同步 `review_bridge` 与 `resume_contract.required_repairs`。
9. 父层不得直接改写阶段业务 canonical truth；返工必须路由回阶段、source owner 或 provider handoff owner。

## Dimension Spec Boundary

- `规划与种子兑现 / 分镜执行连续性 / 设计对位 / 图像交付就绪 / 视频交付就绪 / 治理闭环` 是本父包内的 governed dimension specs。
- 六维细则统一落在 `references/dimensions/*.md`，不再作为独立 Skill 2.0 包或局部 `SKILL.md + CONTEXT.md` 对外直达受理任务。
- 维度经验统一合并到父级 `CONTEXT.md`；若某条经验稳定为强规则，再晋升到对应 `references/dimensions/*.md` 或父级合同。
- 父包拥有完整 Skill 2.0 目录、aggregate gate、runtime 落盘与最终 route 判定权。
- runner 必须在 aggregate packet 的 `dimension_runtime` 中记录每个维度的 `dimension_spec_ref`、`dimension_spec_exists` 与 `execution_mode`。

## Field Mapping

### Directory Ownership Table

| field_id | directory_or_file | owner_role | must_contain | fail_code |
| --- | --- | --- | --- | --- |
| `FIELD-REVIEW-PKG-01` | `SKILL.md` | 卫星入口与聚合裁决 | Input Contract、mode、动态引用、Output Contract | `FAIL-REVIEW-ENTRY` |
| `FIELD-REVIEW-PKG-02` | `CONTEXT.md` | 经验层 | Type Map、Repair Playbook、Reusable Heuristics | `FAIL-REVIEW-CONTEXT` |
| `FIELD-REVIEW-PKG-03` | `references/` | review 强规则 | 根 gate、dimension output、fact pack spec、dimension specs | `FAIL-REVIEW-REFERENCES` |
| `FIELD-REVIEW-PKG-04` | `steps/` | 思行网络 | intake、pack、dimension、aggregate、route | `FAIL-REVIEW-STEPS` |
| `FIELD-REVIEW-PKG-05` | `review/` | 质量门禁 | provider、verdict、降级报告 | `FAIL-REVIEW-GATE` |
| `FIELD-REVIEW-PKG-06` | `types/` | 类型策略 | checkpoint/stage/release 判型 | `FAIL-REVIEW-TYPES` |
| `FIELD-REVIEW-PKG-07` | `templates/` | 输出模板 | Output Contract Alignment | `FAIL-REVIEW-TEMPLATE` |
| `FIELD-REVIEW-PKG-08` | `scripts/` | 机械辅助 | runner wrapper 与脚本说明 | `FAIL-REVIEW-SCRIPTS` |
| `FIELD-REVIEW-PKG-09` | `agents/openai.yaml` | 产品入口 | display_name、short_description、default_prompt | `FAIL-REVIEW-AGENT` |

### Node Handoff Table

| node_id | input | action | output | next_gate |
| --- | --- | --- | --- | --- |
| `N1-REVIEW-INTAKE` | 用户请求、项目根、scope | 锁 mode、checkpoint/stage、aggregate 落点 | `review_scope` | `N2-FACT-PACK` |
| `N2-FACT-PACK` | 项目产物与治理 carrier | 写同一份 `review_fact_pack` | `fact_pack_ref` | `N3-DIMENSIONS` |
| `N3-DIMENSIONS` | fact pack、registry | 调度 mandatory dimensions | `dimension_packets` | `N4-AGGREGATE` |
| `N4-AGGREGATE` | dimension packets | 计算 gate、issues、route | `aggregate_review_packet` | `N5-ROUTE` |
| `N5-ROUTE` | aggregate packet | 写 repair plan 与 handoff verdict | `repair_or_handoff` | done |

### Failure Routing Table

| fail_code | symptom | rework_target |
| --- | --- | --- |
| `FAIL-REVIEW-ENTRY` | 父 `SKILL.md` 与分区规则冲突 | `SKILL.md` + `references/review-root-contract.md` |
| `FAIL-REVIEW-COVENANT` | 维度 reviewer 读取了不同 scope 或 fact pack | `references/review-fact-pack-spec.md` |
| `FAIL-REVIEW-DIMENSION` | mandatory 维度缺失或越权写 gate | `references/review-child-output-contract.md` |
| `FAIL-REVIEW-GATE` | aggregate packet 缺 route 或 repair | `review/review-gate.md` + `_shared/review-aggregate.template.json` |

## Field Master

| field_id | output_slot | requirement | owner_node | quality_dimension | fail_code |
| --- | --- | --- | --- | --- | --- |
| `FIELD-REVIEW-01` | review scope | mode、checkpoint、stage、scope_ref 唯一 | `N1-REVIEW-INTAKE` | scope clarity | `FAIL-REVIEW-01` |
| `FIELD-REVIEW-02` | review fact pack | 同一轮 dimension review 消费同一份 pack | `N2-FACT-PACK` | pack covenant | `FAIL-REVIEW-02` |
| `FIELD-REVIEW-03` | dimension dispatch | registry mandatory 维度全部命中 | `N3-DIMENSIONS` | dispatch completeness | `FAIL-REVIEW-03` |
| `FIELD-REVIEW-04` | aggregate gate | 只有 aggregate packet 写最终 gate | `N4-AGGREGATE` | gate authority | `FAIL-REVIEW-04` |
| `FIELD-REVIEW-05` | route handoff | 必须给出唯一返工或放行入口 | `N5-ROUTE` | closure completeness | `FAIL-REVIEW-05` |

## Thought Pass Map

| pass_id | focus | actions | evidence | route_out | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `PASS-REVIEW-01` | scope lock | 判定 mode 与落点 | `review_scope_note` | `PASS-REVIEW-02` | `N1` |
| `PASS-REVIEW-02` | fact pack covenant | 校验 required slice | `fact_pack_ref` | `PASS-REVIEW-03` | `N2` |
| `PASS-REVIEW-03` | mandatory dimensions | 收集维度 packets | `dimension_packet_refs` | `PASS-REVIEW-04` | `N3` |
| `PASS-REVIEW-04` | aggregate authority | 计算唯一 gate | `aggregate_review_packet` | `PASS-REVIEW-05` | `N4` |
| `PASS-REVIEW-05` | route closure | 写 repair 或 handoff | `repair_plan_ref` | done | `N5` |

## Pass Table

| pass_id | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- |
| `PASS-REVIEW-01` | mode、checkpoint/stage、scope_ref 唯一 | `FAIL-REVIEW-01` | `N1-REVIEW-INTAKE` |
| `PASS-REVIEW-02` | required slice 完整；缺失时停止 | `FAIL-REVIEW-02` | `N2-FACT-PACK` |
| `PASS-REVIEW-03` | mandatory dimensions 全部可聚合，且 `dimension_runtime` 记录 spec 证据 | `FAIL-REVIEW-03` | `N3-DIMENSIONS` |
| `PASS-REVIEW-04` | aggregate packet 拥有唯一 gate authority | `FAIL-REVIEW-04` | `N4-AGGREGATE` |
| `PASS-REVIEW-05` | route / handoff 唯一且可执行 | `FAIL-REVIEW-05` | `N5-ROUTE` |

## Root-Cause Execution Contract (Mandatory)

遇到 review 漂移时，沿以下链路追溯：

`Symptom -> Direct Technical Cause -> Section Owner -> Source Contract -> AGENTS.md / skill-工作车间`

优先修复顺序：

1. scope 或 mode 不唯一：修 `types/review-type-map.md` 与 intake。
2. fact pack 缺 required slice：修 `references/review-fact-pack-spec.md` 或项目阶段 carrier。
3. 维度 reviewer 越权写 gate：修 `references/review-child-output-contract.md`。
4. aggregate 缺 route / repair：修 `review/review-gate.md` 与 `_shared/review-aggregate.template.json`。
5. runner 与 Skill 2.0 分区断链：修 `scripts/` 说明与 `_shared/` 兼容配置。

## Output Contract

- Required output: 唯一 aggregate review packet，以及按需派生的 fact pack、dimension reports、repair plan、review summary。
- Output format: JSON aggregate packet 为 gate 真源；Markdown review summary 只作人读摘要；dimension report 是 sidecar。
- Output path: `projects/aigc/<项目名>/review/checkpoints/`、`projects/aigc/<项目名>/review/stages/` 或 `projects/aigc/<项目名>/review/releases/`。
- Naming convention: aggregate 文件名固定为 `<scope_ref>.review.json`；fact pack 为 `<scope_ref>.review.fact-pack.json`；repair 为 `<scope_ref>.review.repair.json`；summary 为 `<scope_ref>.review.review.md`。
- Completion gate: `templates/output-template.md` 与 `_shared/review-aggregate.template.json` 字段对齐，mandatory dimensions 已聚合并有 `dimension_runtime` 证据，最终 `routing_decision` 可执行。
