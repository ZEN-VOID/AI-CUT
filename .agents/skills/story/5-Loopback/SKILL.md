---
name: story-loopback
description: "Use when a PASS-validated episode must be actualized back into Cards and story_map, or when query/resume style loopback routing must be judged without rewriting truth."
governance_tier: lite
---

# 5-Loopback

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只沉淀 actualization 经验、写回陷阱与 projection 修复启发，不得覆盖本 `SKILL.md` 的 PASS-only 写回契约。
- 若 `CONTEXT.md` 与 `loopback.json` 模板或上游 validation 结论冲突，以本 `SKILL.md` 与模板为准。

## Purpose

- `5-Loopback` 的主职责不是泛化“收尾”，而是把**已通过验证**的单集结果沉淀成后续可消费的正式真相增量。
- 它承接三类 truth：
  - `Cards.current_state/history`
  - `story_map.actualization`
  - `loopback artifact`
- 其中：
  - `Cards` 回答“对象现在怎样了”
  - `story_map.actualization` 回答“计划节点实际推进到哪了”
  - `draft/manuscript/validation/loopback` 保存单集运行证据

## Stage Position

- `2-Planning` 的 canonical planning truth 仍是 `Planning/8-全息地图.json`。
- `5-Loopback` 不另造第二张“执行 MAP”，而是在 `story_map` 内补入 `actualization / validated_*` 执行态字段。
- `5-Loopback` 只在 `4-Validation = PASS` 后执行 actualization 主流程。
- 若当前诉求是查询或恢复，而不是 episode validated actualization，则路由到卫星技能：
  - `query/`：运行时信息查询
  - `resume/`：中断恢复

## Primary Truth & Inputs

actualization 主流程的正式主产物：

- `Loopback/第N集.loopback.json`

生成前必须动态读取：

- `templates/loopback.json`

最小输入：

- `project_root`
- `episode_ref`
- `manuscript_ref`
- `validation_ref`
- `validation_status=PASS`
- `story_map_ref`，默认指向 `Planning/8-全息地图.json`

可选输入：

- `draft_packet_ref`
- 当前集相关的 `Cards`
- 上一集 `carryover_context`
- 需要刷新的 writer / planning / query projection

## Shared References（按需）

- `../references/loopback-actualization-spec.md`
  - 用途：核对 `Cards`、`story_map.actualization`、projection 三类写回分工。
- `templates/loopback.json`
  - 用途：当前 loopback artifact 的唯一模板。

## Shadow Governance Artifact Chain

当 `5-Loopback` 跑在 tracked workflow 里时，必须保留与当前 `<run_id>` task artifact 目录的回指关系：

- `validation_report_ref`
- `artifact_manifest_ref`
- `mission_brief_ref`

约束：

- task dir 中的工件负责证明“为什么允许 writeback”。
- `Loopback/第N集.loopback.json` 负责记录“具体写回了什么”。
- 两者必须互相回指，但不能互相替代。
## Hard Gate

- 只有 `4-Validation = PASS`，才允许：
  - Cards 增量回写
  - `story_map.actualization` 更新
  - writer / planning / query projection refresh
- 若不是 `PASS`：
  - 禁止写入 `Cards.current_state/history`
  - 禁止写入 `story_map.actualization`
  - 禁止刷新 projection
  - 仅允许回到 `3-Drafting` / `review/` / `resume/` 等修复或恢复路径

## Responsibility Split

### 写入 `Cards`

只处理“对象状态已经变化，且后续必须继续当真”的 validated change。

固定写入层：

- `core`
  - 默认不动
- `current_state`
  - 更新为本集结束后默认有效状态
- `history`
  - append-only 追加本集已验证 episode-level 变化记录

### 写入 `story_map.actualization`

只处理“规划节点实际推进到哪了”，不改 planning rationale。

强约束：

- 只新增或更新 `actualization / validated_* / actual_*`
- 不静默覆盖原 `planned_*`
- `planned_*` 与 `actualized_*` 必须可并存对照

### 不写入 `Cards` 的内容

以下内容保留在 `story_map.actualization` 或 episode artifacts，不回写 `Cards`：

- 本集 suspense / rhythm 的执行打法
- 哪一场是高潮
- 哪一页是 reveal 落点
- 本集 prose 的局部文面处理
- 起稿时的临时裁决
- 只对单集成立、不会持续影响后续 truth 的局部波动

## Card Writeback Whitelist

必须优先支持的可演化对象：

- `character cards`
  - 身份暴露
  - 伤势 / 立场 / 目标变化
  - `knowledge_state`
  - 已验证持续后果
- `relationship cards`
  - `trust / hostility / dependency / alliance`
  - 承诺债、背叛、保护、共犯等关系状态
- `prop cards`
  - 持有者
  - 损坏 / 耗尽 / 失落 / 激活 / 封印
  - 线索物品是否已识别或失效
- `scene cards`
  - 封锁、损毁、污染、归属变化、常驻压力变化
- `timeline cards`
  - 已验证时间锚
  - 倒计时推进
  - 退出状态 marker
- `knowledge cards`
  - 谁掌握了什么
  - secrecy 是否被打破
  - 某条认知是否从误解变成正式真知

按需才允许回写：

- `world cards`
- `culture cards`
- `tech cards`
- `costume cards`
- `landscape cards`

前提固定为：本集确实形成了跨集持续、后续必须继续当真的正式变化。

## Workflow

### Step 1: `1-outcome-extract / 结果提纯`

从以下工件提纯统一 `loopback_delta`：

- `manuscript`
- `validation packet`
- `draft packet`

输出至少包含：

- `card_deltas`
- `map_deltas`
- `projection_refresh`
- `evidence_refs`

要求：

- 只能提纯已被 `PASS` 验证的结果
- 不能把草稿阶段猜测、未通过的争议判断混入 delta

### Step 2: `2-card-writeback / 卡回写`

只回写白名单 cards 的 `current_state/history`。

硬规则：

- 不得重新生成“动态卡”
- 不得把所有 cards 全量重写一遍
- 不得默认改 `core`

每条 `history` 记录至少包含：

- `episode_ref`
- `loopback_ref`
- `validation_ref`
- `changed_fields`
- `change_summary`
- `impact_scope`
- `evidence_refs`
- `timestamp`

### Step 3: `3-map-actualization / MAP 实绩回写`

只更新 `story_map.actualization`，不改 planning rationale。

至少更新：

- `episode_nodes[].execution_status`
- `episode_nodes[].validated_at`
- `episode_nodes[].manuscript_ref`
- `episode_nodes[].validation_ref`
- `episode_nodes[].actual_outcome_summary`
- `episode_nodes[].carry_forward_refs`
- `clue_points[].actual_status`
- `clue_points[].validated_resolution_episode`
- `foreshadow_points[].actual_status`
- `foreshadow_points[].validated_payoff_episode`
- `promise_threads[].actual_status`
- `suspense_threads[].actual_release_state`
- `tasklines[].actual_progress`
- `threads[].actual_release_state`

### Step 4: `4-context-refresh / 上下文刷新`

必须显式刷新 task-facing projection，不留给下一集运行时自行猜测。

至少刷新：

- `setting_route_packet.writer_context_projection.memory_projection`
- `story_map` 的 `episode_map_view`
- 下一集默认 `carryover_context`
- runtime marker / dirty flag

## Satellite Routing Contract

当当前诉求不是 `PASS` episode actualization，而是运维型回环动作时：

1. 查询诉求 -> 路由到 `query/`
2. 中断恢复诉求 -> 路由到 `resume/`
3. 若暴露出更高层的路径、schema、合同冲突，先修源层，再继续路由

禁止把卫星技能输出冒充为 actualization 主产物。

## Output Contract

`5-Loopback` 自身至少产出：

- `loopback_ref`
- `episode_ref`
- `validation_ref`
- `validation_status`
- `card_deltas`
- `map_deltas`
- `projection_refresh`
- `evidence_refs`

若执行 actualization 主流程，还必须能追到：

- 正式 loopback artifact 路径
- 已写入的 card refs
- 已更新的 story_map 节点 refs
- 已刷新的 projection refs 或 runtime markers

## Output Structure

输出模式固定为 JSON-first。

生成前必须动态读取 `templates/loopback.json`，最终输出只能是 1 个 JSON 对象。

```json
{
  "schema_version": "story2026/loopback/v1",
  "meta": {},
  "inputs": {},
  "content": {},
  "gate_summary": {},
  "execution_notes": {}
}
```

## Root-Cause 执行合同

- 若出现“该回写的没回写”“把对象状态写成 planning ledger”“把 planning progress 写进 card 本体”等问题，必须按 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` 上溯。
- 本 skill 的 `Rule Source` 默认优先检查：
  - 当前 `5-Loopback/SKILL.md`
  - `1-Cards/SKILL.md`
  - `2-Planning/SKILL.md`
  - `4-Validation/SKILL.md`
  - `query/`、`resume/` 的对应合同
- `Meta Rule Source` 默认上溯到仓库 `AGENTS.md` 与相关 meta skill。
- 修复顺序必须是：
  1. 先修 gate、字段边界、回写协议
  2. 再修本次 artifact
  3. 最后才考虑局部补救单张 card 或单个 map node

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
|---|---|---|---|---|---|
| FIELD-LOOP-GATE-01 | Step 0 | 确认只有 `PASS` episode 才进入 actualization | `validation_status`、gate 判定 | FAIL-LOOP-GATE-01 | 回到 gate 层，阻断非 PASS 写入 |
| FIELD-LOOP-DELTA-02 | Step 1 | 统一提纯 validated delta | `card_deltas`、`map_deltas`、`evidence_refs` | FAIL-LOOP-DELTA-02 | 重做结果提纯，剔除未验证推断 |
| FIELD-LOOP-CARD-03 | Step 2 | 保守回写 card 状态层 | card refs、history append 记录 | FAIL-LOOP-CARD-03 | 回到白名单与状态层边界，禁止改 `core` |
| FIELD-LOOP-MAP-04 | Step 3 | 更新 `story_map.actualization` | updated map refs、`actual_*` 字段 | FAIL-LOOP-MAP-04 | 回到 MAP 实绩层，禁止覆盖 `planned_*` |
| FIELD-LOOP-CTX-05 | Step 4 | 刷新下一轮 projection | `projection_refresh`、runtime marker | FAIL-LOOP-CTX-05 | 重新生成 carryover / projection 刷新包 |

## Completion Gate

- 已确认 `validation_status=PASS`，而非绕过 gate 直接写入。
- 已生成 `Loopback/第N集.loopback.json`。
- 已明确区分 `Cards` 对象状态回写 与 `story_map.actualization` 规划进度回写。
- Cards 仅修改白名单对象的 `current_state/history`，没有重写 `core` 或重建动态卡。
- `story_map` 仅补入 `actualization / validated_* / actual_*`，没有覆盖 planning rationale。
- 下一轮 writer / planning / query projection 已显式刷新。
