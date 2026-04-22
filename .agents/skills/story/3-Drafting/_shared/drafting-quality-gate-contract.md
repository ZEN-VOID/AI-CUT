# Drafting Quality Gate Contract

本文件定义 `3-Drafting` 在“卷级批次已完成、准备移交 `4-Validation` 之前”的质量闸门合同。

## Purpose

它不负责裁决：

- planning 是否齐
- step / hook / ledger 是否完整
- 正文是否达到章节级长度

这些仍分别由：

- `3-Drafting/SKILL.md`
- `drafting-instant-validation-contract.md`
- `scripts/drafting_manuscript_guard.py`

负责。

它专门负责拦截另一类问题：

- 正文已经“写完”
- hook 与日志也都齐
- 但整卷仍明显呈现程序化推进、关系零裂口、空间语法趋同、反派没有面孔、卷末只有升级预告

一句话：

- `drafting-quality-gate` 不拦“没写够”。
- `drafting-quality-gate` 拦“写够了但还写平了”。

## Canonical Runtime Slot

卷级质量闸门快照固定写入：

- `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml -> quality_gate_snapshot`

旧轮若只存在 `post_review_summary`，可作为兼容输入读取，但不得再作为新轮标准写位。

## Quality Gate Snapshot Minimum Shape

```yaml
quality_gate_snapshot:
  checkpoint_stage: pre_validation
  review_mode: master-check-team|quality-self-audit|custom-council
  reviewed_at: 2026-04-22T13:10:00-07:00
  reviewer_source: team-explicit|team-inferred|fallback-no-team|self-audit
  reviewers:
    - 金庸
    - 徐克
  verdict: ready_for_validation|rework_required_before_validation
  guard_axes:
    anti_formula_progression: pass|block
    relationship_friction: pass|block
    spatial_separation: pass|block
    antagonist_face: pass|block
    volume_closure: pass|block
  representative_chapter_refs:
    - 3-Drafting/第5集.md
    - 3-Drafting/第8集.md
    - 3-Drafting/第10集.md
  primary_issues: []
  priority_rework_targets: []
  cross_volume_upgrade_axes: []
  next_action: 4-Validation|3-Drafting-rework
```

## Required Guard Axes

以下五轴是卷级预终验前的默认硬轴：

1. `anti_formula_progression`
   - 拦“章节长期重复同一推进骨架”
   - 重点看是否反复落入“发现线索 -> 破一层网 -> 去下一处”

2. `relationship_friction`
   - 拦“核心关系只有分工，没有代价交换”
   - 重点看主角关系是否真的发生方法冲突、信任损耗或责任转移

3. `spatial_separation`
   - 拦“夜市、税关、王府、海路等场域只换名词、不换语法”
   - 重点看物象、光线、动作几何、声音压力是否分相

4. `antagonist_face`
   - 拦“反派只有系统功能，没有私人面孔”
   - 重点看敌方是否具有可追读的私债、嗜好、羞耻、执念或稳定行为印记

5. `volume_closure`
   - 拦“卷末只做升级预告，不做本卷命运结算”
   - 重点看本卷是否已经真实改写主角处境、关系或阵地

## Verdict Rule

### `ready_for_validation`

必须同时满足：

1. `guard_axes` 五轴全部为 `pass`
2. `next_action == 4-Validation`
3. 若 `reviewer_source != self-audit`，则 `reviewers` 不能为空
4. `representative_chapter_refs` 不能为空

### `rework_required_before_validation`

任一条件成立即可：

1. 任一 `guard_axis == block`
2. 会审明确判定本卷仍需返工
3. `next_action == 3-Drafting-rework`
4. 卷级会审指出代表章节仍是“工整但平庸”

若 verdict 为返工：

- `priority_rework_targets` 应尽量给出 1-3 个优先返工章节
- `primary_issues` 不得留空

## Dispatch Guidance

默认推荐来源：

- `master-check-team`
- `team.yaml` 驱动的 review council
- 若 team 不可用，则允许 `quality-self-audit`

但无论来源如何，最终都必须把结论压成同一份 `quality_gate_snapshot`，而不是只停在聊天纪要里。

## Runtime Rule

1. `candidate_volume_draft` 只代表“卷级 drafting 工序与章节完整度已经收束”。
2. `可移交 4-Validation` 还必须额外通过 `scripts/drafting_volume_quality_guard.py`。
3. 若 quality gate 判定 `rework_required_before_validation`：
   - runtime / resume 必须回到 `3-Drafting`
   - 不得继续把下一稳定入口写成 `4-Validation`

## Compatibility Rule

为兼容旧轮工件：

- 若只存在 `post_review_summary` 且其 verdict 明确为 `rework_required_before_validation`，可直接视为 `block`
- 若只存在 `post_review_summary` 但缺少 `guard_axes`，则不得视为 `ready_for_validation`
- 新轮写回一律改写到 `quality_gate_snapshot`
