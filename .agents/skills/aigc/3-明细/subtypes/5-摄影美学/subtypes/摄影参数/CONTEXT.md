# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `摄影参数` 的经验层知识库，不是执行日志。
- 调用 `摄影参数/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父级 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有“电影感参数”空话，没有具体数值 | 执行层 | 回补快门、ISO、白平衡、滤镜、曝光 | 在 SKILL 固定五项参数门禁 | 参数可直接执行 |
| 快门与动作质感不匹配 | 运动捕捉层 | 根据动作强度重判快门 | 在工作流里先判断动作感再定快门 | 爆发镜不再拖泥带水 |
| ISO/白平衡与光色条件打架 | 感光层 | 回读 `光影` 与 `色彩` 段后重写 | 参数层强制以后读光色为前提 | 参数与光色自洽 |
| 偷偷改了焦距/光圈等静态字段 | 边界层 | 回滚越界改动并上溯报告 | 在 leaf 合同固定“本层不拥有静态光学字段” | 参数层不再侵占上游 |
| 只填数值，没有质感意图 | 质感层 | 补齐滤镜与曝光倾向 | 在字段主表固定 texture 字段 | 参数能解释画面质感 |

## Repair Playbook

1. 先问这镜是要更锐、更稳、更脏还是更柔。
2. 再根据动作和光比定快门、ISO。
3. 再根据综合色板定白平衡。
4. 最后决定滤镜和曝光倾向，并检查是否越界改了静态光学字段。

## Reusable Heuristics

- 参数层最怕“像参数，其实只是口号”。
- 快门通常最先暴露问题，因为它最直接决定动作质感是否成立。
- 白平衡不是单独美学偏好，它必须服从当前光源与综合色板。
- 如果为了修参数去改焦距或光圈，通常说明边界已经坏了。

## Case Log

### Case-20260409-AIGC-SCRIPT-CAMERA-PARAMETERS-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `摄影参数` 建立了适配当前 `3-明细` 终稿模式的 leaf 合同与经验层。
- root_cause_or_design_decision: 用户要求 `5-摄影美学` 覆盖摄影参数；直接技术缺口是当前仓缺少“在不改静态镜头骨架的前提下补捕捉参数”的稳定 leaf。
- final_fix_or_heuristic: 将本层限定为 `快门 / ISO / 白平衡 / 滤镜 / 曝光` 五项捕捉参数，并把 `焦距 / 光圈 / 景深 / 对焦点` 明确留在 `1-分镜表现`。
- prevention_or_replication_checklist:
  - [x] 已固定共享终稿落点
  - [x] 已建立五项参数门禁
  - [x] 已限制不改静态光学字段
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/摄影参数/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/摄影参数/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/5-分镜构图/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `5-摄影美学` 应覆盖摄影参数，同时保持当前仓“共享终稿逐层发酵”的写集模式。
