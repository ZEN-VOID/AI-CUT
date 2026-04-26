---
name: story-review-structure-realization
description: Use when `4-Review` needs the governed child skill that checks whether the locked volume manuscript set fulfills volume-board and episode-board obligations, promise delivery, and dramatic realization.
governance_tier: lite
---

# 4-Review / 结构兑现

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `4-Review/SKILL.md`、`../_shared/validation-root-contract.md`、`../_shared/validation-child-output-contract.md`。
- 正式审查前，必须读取锁定后的 `validation_fact_pack` 与当前卷正文集合。

## Invocation Modes

- `drafting_inline`
  - 被 `3-Drafting` 在 registry 指定 step 写回后立即调用，只判断当前快照是否允许继续下一步。
- `final_acceptance`
  - 被 `4-Review` 父层在卷级终验中并发调用，参与最终 `validation_status` 聚合。

## Parent Positioning

本 child 负责：

- 检查 `promise_slice` 与 `chapter_board` 的结构义务是否被正文兑现
- 检查关键事件、冲突、任务、线索、伏笔回收是否落地
- 检查“结构是否已经写成戏，而不是摘要/提纲/说明”

它不负责：

- 上一章衔接连续性
- 角色行为一致性细化
- 时间锚精确排序
- 世界规则与对象状态的严密因果核查

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../_shared/validation-root-contract.md`
- `../_shared/validation-child-output-contract.md`
- `../_shared/validation-fact-pack-spec.md`
- `../_shared/checker-output-schema.md`
- `../../_shared/core-constraints.md`

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 判断正文是否真的兑现了这集该发生的事，而不是只“提到过”或“总结过”。 |
| `business_object` | `validation_fact_pack.promise_slice`、`volume_planning_summary / chapter_planning_packets`、当前卷正文集合。 |
| `constraint_profile` | 先看 board 义务，再看正文戏剧化落点；结构未兑现不能靠其他维度补救。 |
| `success_criteria` | 能明确回答“这一章 promised 什么、planned 什么、正文到底有没有完成”。 |
| `topology_fit` | `obligation decode -> manuscript compare -> dramatization gate -> report packet` |

## Total Input Contract

- 必需输入：
  - `validation_fact_pack.promise_slice`
  - `validation_fact_pack.chapter_planning_packet`
  - 当前卷正文集合
- 硬规则：
  - 先锁“必须发生什么”，再判正文是否实现。
  - 只出现摘要式复述、不形成戏剧场面，也视为未充分兑现。

## Output Contract

- `role_id`:
  - `structure-validator`
- `dimension_packet`:
  - 至少包含 `required_events_hit`、`missed_obligations`、`promise_breaks`、`undramatized_exposition_hits`、`anti_ai_force_check`
- `dimension_report_ref`:
  - `4-Review/第V卷/结构兑现.md`
- 默认返工节点：
  - `1-单章叙事起盘`
  - `7-追读力强化`

## Visual Map

```mermaid
flowchart TD
    A["解码 promise + chapter_planning_packet"] --> B["逐段比对正文"]
    B --> C["判定是否写成戏剧场面"]
    C --> D["输出结构兑现 packet + report"]
```

## Thinking-Action Network

| node_id | field_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-OBLIGATION-DECODE` | `FIELD-ST-01` | 锁定本章必须兑现的结构义务 | 抽取事件、冲突、任务、线索、伏笔债务 | `obligation_note` | -> `N2` | obligation 清楚 |
| `N2-MANUSCRIPT-COMPARE` | `FIELD-ST-02` | 对照正文逐项核验 | 标记命中、漏项、弱兑现 | `compare_note` | -> `N3` | 义务对齐 |
| `N3-DRAMATIZATION-GATE` | `FIELD-ST-03` | 判定是否只是摘要而非戏 | 检查说明腔、硬总结、无场面兑现 | `dramatization_note` | -> `N4` | 戏剧化成立 |
| `N4-PACKET-WRITE` | `FIELD-ST-04` | 输出结构维度结论 | 生成 `dimension_packet + report_ref` | `packet_note` | done | 只写本维度 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-ST-01` | obligation set | 本章必须兑现的结构义务已锁定 | `FAIL-ST-01` | `N1` |
| `FIELD-ST-02` | compare matrix | 每项义务都能找到正文证据或明确缺失 | `FAIL-ST-02` | `N2` |
| `FIELD-ST-03` | dramatization verdict | 不是提纲腔或总结腔式“假兑现” | `FAIL-ST-03` | `N3` |
| `FIELD-ST-04` | dimension packet | 结构维度报告完整、可聚合 | `FAIL-ST-04` | `N4` |

## Completion Contract

- 已明确列出本章结构兑现与未兑现项。
- 已区分“缺事件”与“只提到没演出来”。
- 报告已给出默认返工节点。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 维度审查入口与父层边界 | `../SKILL.md`、`../references/root-runtime-contract.md` |
| 结构兑现步骤网络 | `steps/validation-flow.md` |
| 维度判据与共享字段 | `references/README.md`、`../_shared/validation-child-output-contract.md` |
| 质量门禁与 reviewer 汇流 | `review/review-gate.md` |
| 类型化输入画像 | `types/type-map.md` |
| 输出样式 | `templates/output-template.md` |
| 脚本边界 | `scripts/README.md` |
| 可复用经验 | `knowledge-base/heuristics.md` 与 `CONTEXT.md` |
| 产品侧入口 | `agents/openai.yaml` |

## Root-Cause Execution Contract

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

若正文只提到规划义务但没有形成戏剧场面，优先打回 `1-单章叙事起盘` 或 `7-追读力强化`；若 planning 义务本身缺失，转 source route。

## Field Mapping

| field_id | owner | required_output | fail_code |
| --- | --- | --- | --- |
| `FIELD-ST-ENTRY` | `SKILL.md` | 输入、边界、维度 verdict 与父层回接 | `FAIL-ST-ENTRY` |
| `FIELD-ST-STEPS` | `steps/` | 义务解码、正文比对、戏剧化门禁 | `FAIL-ST-STEPS` |
| `FIELD-ST-REVIEW` | `review/` | 维度门禁与 packet 可聚合性 | `FAIL-ST-REVIEW` |

## Skill 2.0 Output Contract

- Required output: 结构兑现 `dimension_packet` 与 `dimension_report_ref`。
- Output format: Markdown 维度报告 + 父层可聚合结构化 packet。
- Output path: `projects/story/<项目名>/4-Review/第V卷/结构兑现.md`。
- Naming convention: report filename 以父层 registry 的 `report_filename` 为准。
- Completion gate: 缺失义务、弱兑现与返工入口均可追溯。
