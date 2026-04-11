# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `光影设计` 的经验层知识库，不是执行日志。
- 调用 `光影设计/SKILL.md` 时，应自动预加载本文件。
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
| 光影只有抽象氛围词，没有光源实体 | 表达层 | 回补光源实体与入射方向 | 在 SKILL 固定“实体 + 方向”门禁 | 能说出光从哪来 |
| 只有亮部，没有阴影和反差 | 影调层 | 补明暗结构与遮挡关系 | 在字段主表固定阴影关系 | 画面不再平铺照亮 |
| 光很美，但没有戏剧作用 | 叙事层 | 回补揭示/压迫/亲密/反转等作用 | 在工作流中强制回答“为何此刻这样照” | 光影能服务剧情 |
| 光影越界写成综合色彩 | 边界层 | 移除综合色彩判断，回退给 `色彩设计` | 在 leaf 合同里明确只拥有光源与影调 | 光影段不再替代色彩段 |
| 光影直接改写静态镜头字段 | 结构层 | 回滚对 `[分镜N]` 的越界改动 | 固定只写 `[摄影美学].光影` | 分镜骨架保持不动 |

## Repair Playbook

1. 先问这束光来自哪里。
2. 再问它照到谁，谁被留在影子里。
3. 再问它为什么要在这一刻这样出现。
4. 最后确认有没有把颜色或参数问题越权写进来。

## Reusable Heuristics

- 好的光影句子至少能同时回答“来源、方向、对象、作用”中的三个问题。
- 只写亮，不写影，画面就没有戏剧切面。
- 光影是叙事杠杆，不是形容词喷雾。
- 若一句话已经在谈综合色板，那通常说明该回到 `色彩设计` 了。

## Case Log

### Case-20260409-AIGC-SCRIPT-LIGHTING-DESIGN-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `光影设计` 建立了适配当前 `3-明细` 终稿模式的 leaf 合同与经验层。
- root_cause_or_design_decision: 用户要求 `5-摄影美学` 包含光影能力；直接技术缺口是当前仓没有任何“把导演光影判断落回脚本终稿”的稳定 leaf。
- final_fix_or_heuristic: 吸收旧仓 `6-光影美学` 的高价值判断维度，但把输出载体改写为共享终稿中的 `[摄影美学].光影` 段。
- prevention_or_replication_checklist:
  - [x] 已固定共享终稿落点
  - [x] 已建立光源/方向/阴影/作用门禁
  - [x] 已限制只写 `[摄影美学].光影`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/光影设计/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/光影设计/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/6-光影美学/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `5-摄影美学` 应覆盖光影能力，并服务当前仓的“共享终稿逐层发酵”模式。
