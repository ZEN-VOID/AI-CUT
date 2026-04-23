---
name: story-loopback
description: Use when a PASS-validated volume has been explicitly handed off to `5-Loopback` for validated actualization into Cards, story_map actualization, and runtime projections, or when loopback-shaped requests must be rerouted to `query/` or `resume/` without rewriting truth.
governance_tier: full
---

# 5-Loopback

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `5-Loopback` 的父单元已经从单章 actualization 升级为卷级 validated actualization。
- 若 `CONTEXT.md`、`templates/loopback.json`、`../scripts/loopback_manager.py`、`../scripts/workflow_manager.py` 与本合同冲突，先修这些源层载体，再修单次 artifact。

## Overview

`5-Loopback` 现在负责把已经通过卷级终验的整卷变化，稳定写回未来还会继续被消费的 truth 层。

它的正式主干固定为：

1. 只消费 `4-Validation` 的卷级聚合 JSON。
2. 同时检查：
   - `validation_status == PASS`
   - `routing_decision == handoff_to_review_and_loopback`
   - `handoff_targets` 同时包含 `review/` 与 `5-Loopback`
3. 提纯整卷统一 `loopback_delta`。
4. 串行写回：
   - `Cards.current_state/history`
   - `2-Planning/整体规划.actualization.json`
   - `2-Planning/第N卷/卷规划.actualization.json`
   - `2-Planning/第N卷/第N章.actualization.json`
   - 当前卷命中的 `2-Planning/卷分片/*.json.content.holomap_slice.actualization`
   - `2-Planning/全息地图.json.content.holomap.actualization` 的卷级 summary/index
5. 刷新 `STATE.json` 中下一轮要消费的 projection 与 runtime markers。
6. 生成唯一正式产物 `5-Loopback/第V卷.loopback.json`。

一句话裁决：

- `PASS` 不是唯一 gate。
- 只有 `PASS + handoff granted` 才能进入卷级 actualization。

## Parent Positioning

### 父层拥有

- `PASS-only + handoff-granted` intake gate
- 整卷 `loopback_delta` 提纯与边界裁决
- 三层规划 sidecar actualization 写回
- `Cards` 与 `story_map_slice.actualization + story_map_root.actualization summary` 的 truth split
- projection refresh 与 runtime marker 刷新
- `5-Loopback/第V卷.loopback.json` 唯一正式 artifact
- `query/`、`resume/` 的卫星路由裁决

### 父层不拥有

- 重写 `validation_status`
- 重写 `routing_decision / handoff_targets`
- 代替 `review/` 产出正式审查报告
- 代替 `3-Drafting` 修改正文
- 覆盖 `Cards.core`
- 覆盖 planning 中的 `planned_*` 理由层

## Shared Canonical Sources

- `.agents/skills/story/SKILL.md + CONTEXT.md`
- 当前 `SKILL.md + CONTEXT.md`
- `../4-Validation/SKILL.md`
- `../review/SKILL.md`
- `../query/SKILL.md`
- `../resume/SKILL.md`
- `../4-Validation/_shared/checker-output-schema.md`
- `../_shared/entity-management-spec.md`
- `./_shared/loopback-actualization-spec.md`
- `templates/loopback.json`
- `../scripts/loopback_manager.py`
- `../scripts/workflow_manager.py`

## Canonical Runtime

- `projects/story/<项目名>/5-Loopback/第V卷.loopback.json`

## Total Input Contract

### 必需输入

- `project_root`
- `volume / volume_ref`
- `chapter_refs`
- `validation_ref`
- 当前轮 `4-Validation/第V卷.validation.json`
- `book_plan_ref`，默认 `2-Planning/整体规划.md`
- `volume_plan_ref`，默认 `2-Planning/第N卷/卷规划.md`
- `chapter_plan_refs`，默认命中 `2-Planning/第N卷/第N章.md`
- `story_map_ref`，默认 `2-Planning/全息地图.json`
- `story_map_slice_ref`
- `STATE.json`

### validation aggregate JSON 必需字段

- `validation_status`
- `routing_decision`
- `handoff_targets`
- `validation_ref`
- `issues`
- `severity_counts`
- `overall_score`
- `volume_ref`
- `chapter_refs`

### 硬规则

1. 仅 `validation_status == PASS` 还不够；必须同时满足：
   - `routing_decision == handoff_to_review_and_loopback`
   - `handoff_targets` 明确包含 `review/`
   - `handoff_targets` 明确包含 `5-Loopback`
2. 若当前是 `handoff_to_review_only` 的历史复核 PASS，禁止 actualization 写回。
3. `loopback_delta` 只能包含 validated 结果，不得混入 drafting 猜测、review 主观建议或 source-fix 草案。
4. `Cards` 回写只允许落到 `current_state/history`，默认不改 `core`。
5. 三层规划正文 `整体规划.md / 第N卷/卷规划.md / 第N卷/第N章.md` 仍保持 planning-only，不直接混入 validated actualization；loopback 只允许写它们各自的 `.actualization.json` companion sidecar。
6. `story_map` 回写只允许把卷级 validated actualization 明细落到命中的 `story_map_slice_ref.actualization`，并把卷级 summary/index 回刷到 root `actualization`；不得覆盖 `planned_*`。
7. 若当前诉求其实是查询、恢复或源层修复，必须改走 `query/`、`resume/` 或 upstream source fix，而不是强行 actualize。

## Dispatch Order Contract

### 固定 tracked steps

1. `N1-VALIDATION-AND-DELTA`
2. `N2-TRUTH-WRITEBACK`
3. `N3-PROJECTION-REFRESH`
4. `N4-PASS-ONLY-CLOSURE`

### 并发规则

- 正式写回：禁止并发
- 允许并发的仅有：
  - `card_delta / map_delta / projection_refresh` 的 staged patch 预计算
  - 风险分析或 commit 计划生成

## Output Contract

### Canonical final output

- `projects/story/<项目名>/5-Loopback/第V卷.loopback.json`

### 至少包含

- `volume_ref`
- `chapter_refs`
- `validation_ref`
- `loopback_delta`
- `writeback_summary`
- `gate_summary`
- `execution_notes`

## Satellite Routing Contract

当当前请求不是 “PASS + handoff-granted volume actualization” 时，固定路由如下：

- 查询态：
  - `query/`
- 恢复态：
  - `resume/`
- 上游 source 修复：
  - `0-Init / 1-Cards / 2-Planning / 3-Drafting / 4-Validation`

禁止把 `query/` 或 `resume/` 的输出伪装成 `5-Loopback/第V卷.loopback.json`。

## Completion Contract

- 当前卷 aggregate gate 已确认合法
- Cards / MAP / STATE 的 validated delta 已按顺序写回
- 已生成 `5-Loopback/第V卷.loopback.json`
- artifact 能回指 validation 与 governance evidence
