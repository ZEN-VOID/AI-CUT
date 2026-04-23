---
name: story-stage-review
description: Use when story2026 needs to audit a drafted volume against init/cards/planning truths through governed review specs, with background `code-reviewer` execution feeding back into repair routing before review and loopback.
governance_tier: full
allowed-tools: Read Grep Write Edit Bash Task
---

# 4-Review

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 在进入任一子技能前，必须先回读本 `SKILL.md`、`_shared/validation-root-contract.md`、`_shared/validation-child-output-contract.md`。
- 当前阶段的父单元已经从“单章终验”升级为“卷级聚合终验”；卷内逐章证据仍可保留，但最终 gate truth 只认卷级 aggregate JSON。

## Overview

`4-Review` 现在是 `story2026` 的卷级终验父 skill。

这里的关键变化不是只把目录名从 `Validation` 改成 `Review`，而是把“子技能 = 能力执行器”的旧理解收束为：

- 子技能主要定义审计规范：范围、目标、方式、证据要求、fail code、回流入口。
- 真正的自动审计执行默认由后台独立窗口/进程触发的 [$code-reviewer](/Users/vincentlee/.codex/skills/meta/构建/架构/code-reviewer/SKILL.md) 完成。
- `4-Review` 父层负责把 `code-reviewer` 结果与本地维度 packet 聚合，再自动决定是放行、打回 `3-Drafting`，还是上溯到 `0-Init / 1-Cards / 2-Planning`。

新的 canonical 结构固定为：

1. 父层先锁项目根、卷号、卷内章节范围、卷级正文快照与 `validation_fact_pack`
2. registry 当前 mandatory 子技能按 review spec 并发审查整卷；当前基线为六维卷级终验
3. 子技能输出卷级维度 verdict，同时保留章级 issue 定位
4. 父层聚合为唯一卷级 gate JSON
5. 通过后交给 `review/` 与 `5-Loopback`
6. 未通过时按 issue 级别打回 `3-Drafting` 对应 worker/step，或上溯到 `0-Init / 1-Cards / 2-Planning`

一句话裁决：

- 子技能可以并发写维度 sidecar。
- 父层只认 `第V卷.validation.json` 作为 `validation_status / routing_decision / handoff_targets` 的唯一真源。

## Parent Positioning

### 父层拥有

- `volume scope / chapter_refs` 锁定
- 卷级 `validation_fact_pack` 组装与 covenant gate
- registry 当前 mandatory 子技能的并发调度与收束
- 卷级 `validation_status / routing_decision / handoff_targets` 唯一判定权
- `4-Review/第V卷.validation.json` 正式落盘
- 章级 `rework_targets` 与 `source_trace` 汇总
- `candidate_volume_draft -> validated_volume_draft` 的最终放行裁决

### 父层不拥有

- 直接修改任何 `第N章.md`
- 代替 `review/` 生成正式业务审查报告
- 代替 `5-Loopback` 回写 validated truth
- 把各维度 sidecar 变成第二份 parallel canonical truth

## Governed Child Skills

validator roster、role_id、权重、默认返工节点与 mandatory 终验维度，统一以 `./_shared/validation-dimension-registry.yaml` 为准。

父层在这里不再手写第二张维度表，只保留两条约束：

- 当前 registry 落地的是六维卷级终验，其中新增 `任务汇聚`，且不再保留历史上的 `类型兑现`。
- 父层只负责并发调度、聚合裁决与 route 判定，不接管子技能的维度内判据。

硬规则：

1. registry 当前 mandatory 子技能默认并发，但只能读取同一份卷级 pack 与同一批正文快照。
2. 子技能只产出局部 `dimension_packet + dimension_report_ref`，不得判定最终 `validation_status`。
3. 父层不得跳过 registry 中任一 mandatory 子技能。

## Execution Provider Contract

- 默认 provider：[$code-reviewer](/Users/vincentlee/.codex/skills/meta/构建/架构/code-reviewer/SKILL.md)
- 默认执行方式：后台独立窗口/进程运行，不把主 skill 本身伪装成审计执行器。
- 当前 repo 的 canonical runner：`../scripts/review_runner.py`
- 审计汇流规则：
  - `code-reviewer` 先输出结构化 findings / report sidecar。
  - `4-Review` 再把 findings 映射为 `issues / severity_counts / rework_targets / source_trace`。
  - 聚合结论必须回写到 `4-Review/*.validation.json`，不能只停留在外部 reviewer sidecar。

## Shared Canonical Sources

- `.agents/skills/story/SKILL.md`
- 当前 `SKILL.md + CONTEXT.md`
- `./_shared/validation-root-contract.md`
- `./_shared/validation-child-output-contract.md`
- `./_shared/validation-dimension-registry.yaml`
- `./_shared/validation-aggregate.template.json`
- `./_shared/validation-dimension-report.template.md`
- `./_shared/validation-fact-pack-spec.md`
- `./_shared/validation-team-contract.md`
- `./_shared/checker-output-schema.md`
- `../3-Drafting/_shared/drafting-instant-validation-contract.md`

## Canonical Runtime

- 聚合 gate packet：
  - `projects/story/<项目名>/4-Review/第V卷.validation.json`
- 维度 sidecars：
  - 统一落在 `projects/story/<项目名>/4-Review/第V卷/`
  - 文件名以 `validation-dimension-registry.yaml -> report_filename` 为准

## Total Input Contract

### 必需输入

- `project_root`
- `volume / volume_ref`
- 当前卷全部正文 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`
- 当前卷批次日志 `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml`
- `candidate_volume_draft` 状态说明
- `0-Init/north_star.yaml`
- `1-Cards/0-全局卡/**/*.json`
- `1-Cards/**/*.json`
- `2-Planning/整体规划.md`
- 当前卷 `2-Planning/第V卷/卷规划.md`
- 当前卷各章 `2-Planning/第V卷/第N章.md`
- 若项目仍处于兼容态，再补读 `2-Planning/全息地图.json` 与 `卷分片/*.json`
- 本轮动态生成的 `validation_fact_pack`

### 硬规则

1. `validation_fact_pack` 缺任何 required slice，直接 `FAIL-COVENANT`。
2. pack 必须由当前轮动态生成；不得复用旧轮残包。
3. registry 当前 mandatory 子技能必须消费同一份卷级正文快照与同一份卷级 pack。
4. 子技能局部 sidecar 只做证据层，不拥有卷级总 gate 判定权。
5. `PASS` 需要同时满足：
   - 无 `critical` 问题
   - 无未解决的 source-layer 冲突
   - 无 `FAIL-COVENANT / FAIL-RUNTIME`
6. 若 `3-Drafting/第V卷.写作日志.yaml` 未能提供完整 `chapter_refs x 8 步` 的 `chapter_step_history` 与逐步 `chapter_hook_results`，直接判定 `FAIL-COVENANT`，不得把稀疏日志当作可接受输入。
7. 卷级 `PASS` 不等于“卷内没有任何小问题”，而是所有剩余问题均不构成 blocking issue。
8. 若发现 upstream truth 自相矛盾，必须优先走 `back_to_source_contract`，不得要求 `3-Drafting` 瞎改正文背锅。

## Dispatch Order Contract

### 固定主干

1. `N1-VOLUME-INTAKE`
2. `N2-CONTEXT-PACK`
3. `N3-PARALLEL-VALIDATION`
4. `N4-AGGREGATE-GATE`
5. `N5-ROUTE-HANDOFF`

### 并发规则

- 必须并发：
  - registry 当前 mandatory validation child skills
- 必须串行：
  - pack 组装
  - 聚合裁决
  - aggregate JSON 落盘
  - handoff route 判定

## Aggregate Gate Contract

- 维度权重以 `validation-dimension-registry.yaml` 为准
- `validation_status` 不以均分独裁，必须额外经过 severity / source gate：
  - `FAIL-RUNTIME`
  - `FAIL-COVENANT`
  - `FAIL-QUALITY`
  - `PASS`

### Routing Decision Contract

| routing_decision | 适用条件 | handoff_targets |
| --- | --- | --- |
| `back_to_drafting_nodes` | 问题主要落在卷内若干章节正文质量与工序执行 | `3-Drafting` 对应 workers / steps |
| `back_to_source_contract` | 上游 truth 缺失、冲突或 pack 失效 | `0-Init` / `1-Cards` / `2-Planning` |
| `handoff_to_review_and_loopback` | `PASS` 且允许进入完整闭环 | `review/`、`5-Loopback` |
| `handoff_to_review_only` | 只需要业务报告 / 历史复核，不进入 actualization | `review/` |

## Output Contract

### Canonical final output

父层最终只向下游与运行时交付一份卷级聚合 JSON，至少包含：

- `validation_status`
- `validation_mode`
- `volume_ref`
- `chapter_refs`
- `selected_agents`
- `dimension_packets`
- `dimension_report_refs`
- `issues`
- `chapter_issue_index`
- `severity_counts`
- `critical_issues`
- `overall_score`
- `dimension_scores`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `validation_ref`

## Completion Contract

- 当前卷 pack、正文快照与维度 sidecars 已锁定并可追溯
- 聚合 JSON 已能把问题回流到具体章节/worker/step
- 只有卷级 aggregate JSON 才能把本卷交给 `review/` 与 `5-Loopback`
