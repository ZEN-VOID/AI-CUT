# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/4-教学策略与课程架构` 的经验层知识库，不是第二份课程架构合同。
- 调用 `.agents/skills/lesson/4-教学策略与课程架构/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-architecture-and-load-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 课程架构变成完整讲稿或讲义正文 | stage boundary drift | 删除正文展开，保留模块、课时目的、策略和输入输出 | `5-课时内容开发` 拥有完整正文 | 第 4 阶段输出不含逐字稿 |
| 课程结构按资料章节机械拆分 | strategy-first gap | 回到目标、评价证据和学习者约束，重做策略矩阵 | 先选教学策略，再设计模块蓝图 | 每个模块有目标承接和策略理由 |
| 缺第 3 阶段目标蓝图却强行定稿 | upstream dependency gap | 标记草案风险或回到 `3-目标与评价蓝图` | 正式定稿必须有目标/评价锚点 | `upstream_anchor_matrix` 有目标证据 |
| 课时序列过密导致不可教 | cognitive load overload | 拆分高负荷点，增加练习、缓冲和复盘 | `N7` 必须审查峰值负荷和活动密度 | 高负荷点有支架或缓冲 |
| 教学策略只写口号 | pedagogy rationale gap | 为每个策略补对应目标、受众约束和取舍理由 | 策略矩阵绑定模块和目标 | strategy matrix 可追溯 |
| 下游 handoff 缺失导致第 5 阶段反推 | handoff gap | 补 `downstream-handoff.md`，列出模块、课时、策略和限制 | 第 4 阶段完成门绑定 handoff | `5/6/7/8` 均有输入说明 |
| 脚本或模板投影课程结构正文 | creative authorship violation | 废弃机械产物，回到 LLM 逐条判断节点 | `SKILL.md` 和 review gate 阻断脚本主创 | anti-scripted gate 通过 |

## Repair Playbook

1. 先确认定位文档、知识模型和目标蓝图是否存在；缺目标蓝图时不要直接定稿完整架构。
2. 先用学习目标、评价证据和知识依赖决定教学策略，再切模块，不按资料目录机械拆分。
3. 课时序列只写结构性信息：主题、目标承接、活动类型、时长、输入、输出和依赖；不要写正文或题目。
4. 每个高负荷学习点至少配置一种支架：示范、分步练习、前置复习、缓冲、复盘或拆课。
5. 若总时长不足，优先缩小范围或降级目标，不通过压缩讲授密度解决。
6. 若用户要求“以后都保持高互动/少理论/偏案例”等长期口味，写入项目 `MEMORY.md`；一次性结构方案仍留在第 4 阶段输出。
7. 若用户顺手要求生成讲稿、题库或 PPT，交给 `5/6/8`，第 4 阶段只提供结构 handoff。

## Reusable Heuristics

- 第 4 阶段的核心价值是“让后续阶段不再争论结构”，不是提前把每节课写完。
- 好的课程架构同时满足三条线：学习目标线、知识依赖线和学习者体验线。
- 模块数不是越多越细；模块应该代表学习者可感知的能力台阶或任务场景。
- 课时序列要留下练习和复盘空间；只排讲授内容通常会在第 5 阶段失控。
- 认知负荷审查要关注连续新概念、连续抽象解释、过多切换任务和缺少反馈的练习。
- 策略选择要匹配受众：新人需要示范和支架，熟手需要案例、决策练习和迁移任务。
- 下游 handoff 要告诉第 5 阶段“每节课为什么存在”，告诉第 6 阶段“哪些位置需要练习或测评”，告诉第 7/8 阶段“哪里需要视觉或交互承托”。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: course_architecture_stage_contract_creation
- outcome: 建立 lesson 第 4 阶段的 teaching-strategy-first runtime spine。
- design_decision: 以 `1/2/3` 上游锚点锁定结构，再依次完成策略矩阵、模块蓝图、课时序列、认知负荷审查和下游 handoff。
- replication_checklist: 锁上游 -> 定范围 -> 选策略 -> 切模块 -> 排课时 -> 审负荷 -> 写回 -> handoff。
- evidence_paths: `.agents/skills/lesson/4-教学策略与课程架构/SKILL.md`
