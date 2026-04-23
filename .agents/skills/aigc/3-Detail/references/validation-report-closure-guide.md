# 3-Detail Validation Report Closure Guide

本文件细化 `projects/aigc/<项目名>/3-Detail/validation-report.md` 中 `Thinking-Action Closure` 的书写规则。
若与主 `SKILL.md` 冲突，以主合同为准。

## Purpose

- 让 `思考过程 / 关键证据 / 风险/例外 / 下一入口` 不只“有这四段”，而是写得可复核、可返工、可 handoff。
- 让知行合一 closure 与学院派知识证据共存于同一份阶段报告，不另起 sidecar。
- 让 query / resume / review 读取阶段报告时，能直接恢复本轮决策与返工入口。

## Required Placement

`validation-report.md` 推荐至少具备以下章节：

1. `## Layered Trace`
2. `## 已执行校验`
3. `## Academy Knowledge Evidence`
4. `## Thinking-Action Closure` 或兼容 `## Closure Triad`

硬规则：

1. closure 段必须晚于校验与知识证据，不能在前面先下结论。
2. closure 段只进入 `validation-report.md`，不另起第二真源文件。
3. closure 文字必须回链到本轮真实 JSON、真实 validator 结果与真实返工入口。

## Closure Writing Order

### 1. `思考过程`

回答四件事：

- 当前为什么锁定这个 `episode/group scope`
- 为什么本轮判定需要或不需要学院派知识包
- 为什么从 `N2/P1` 先行，而不是先修后续字段
- 为什么最终选择 `pass / rework / stop`

最小健康模式：

- 先写本轮 scope
- 再写知识域判断
- 再写主要节点路径
- 最后写 verdict 依据

### 2. `关键证据`

至少回链以下证据中的命中项：

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `python3 .agents/skills/aigc/3-Detail/scripts/validate_stage_output.py ...` 的结果
- 本轮实际写入的 `group_id / shot_id / field_scope`
- `knowledge_mode / selected_bundles / applied_passes / translation_targets`
- 若是增量 patch，本轮保留未命中 scope 的说明

硬规则：

1. 关键证据不能只写“已通过校验”“已参考知识库”。
2. 必须能看出到底改了哪几个 group、哪几个字段、用了哪几个 bundle。
3. 若本轮未使用学院派知识，也必须把 `unused_with_reason` 作为关键证据的一部分写明。

### 3. `风险/例外`

至少覆盖以下风险类型中的命中项：

- 当前仅完成局部 `group_scope / shot_scope / field_scope`
- 未命中 scope 沿用既有确认内容，未重跑
- 上游 `2-Global` seed 有潜在漂移，但本轮未重写
- 某些字段仍需回 `N2/N3/N4/N5/N6` 指定节点返工
- 本轮未读取某知识域，因此相关判断仍偏经验写法

硬规则：

1. 风险不能写成泛泛“仍有优化空间”。
2. 必须指明哪个 scope 仍有风险，以及风险属于结构、字段、知识转译还是 handoff。
3. 若本轮是 `stop`，这里必须清楚写出 blocker。

### 4. `下一入口`

只允许给一个默认下一入口：

- `rework -> N2`
- `rework -> N3`
- `rework -> N4`
- `rework -> N5`
- `rework -> N6`
- `re-audit -> N7/N8`
- `handoff -> 4-Design`
- `blocked -> back to 2-Global`

硬规则：

1. 不允许同时给多个平级候选入口。
2. 若是返工，必须写明具体节点，而不是只写“回头优化”。
3. 若是完成态 handoff，默认下一入口是 `4-Design`，除非用户当前目标另有指定。

## Closure Templates

### Pass Template

```md
## Thinking-Action Closure

### 思考过程
- 本轮锁定 `<episode/group scope>`，先经 `N1` 明确 `<knowledge_mode>`，随后按 `N2 -> ... -> N7` 完成细化；由于 `分镜构图` 已先锁镜数、正文切分点与主体锚定，后续字段未再反改骨架。

### 关键证据
- canonical 输出：`projects/aigc/<项目名>/3-Detail/第N集.json`
- validator：`PASS`
- knowledge evidence：`<selected_bundles / applied_passes / translation_targets>`

### 风险/例外
- 本轮 `<是否局部 patch>`；未命中 scope `<保留/无>`

### 下一入口
- `handoff -> 4-Design`
```

### Rework Template

```md
## Thinking-Action Closure

### 思考过程
- 本轮在 `<node>` 发现 `<symptom>`，判断其根因属于 `<layer>`，因此不进入下游 handoff。

### 关键证据
- fail code：`<FAIL-DETAIL-XX>`
- validator / rubric 证据：`<evidence>`

### 风险/例外
- 当前 `<group/shot/field>` 若继续下游消费，会导致 `<risk>`

### 下一入口
- `rework -> <N2|N3|N4|N5|N6|N7/N8>`
```

## Anti-Patterns

- 只有“已完成”或“已通过”，没有四段细节。
- `思考过程` 变成大段情绪化自述，读不出 scope 和节点路径。
- `关键证据` 只有文件名，没有 validator、group、field 或知识包证据。
- `风险/例外` 只写“后续可继续优化”。
- `下一入口` 同时列 `4-Design / review / resume` 多个候选。

## Minimal Healthy Pattern

一份健康的 `3-Detail` closure，至少要让读者一眼回答：

1. 本轮到底改了什么 scope。
2. 为什么这样改。
3. 有什么真实证据证明它成立。
4. 还有什么没解决。
5. 下一步唯一应该去哪。
