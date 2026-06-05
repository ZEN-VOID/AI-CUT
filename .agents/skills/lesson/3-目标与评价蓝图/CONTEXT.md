# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/3-目标与评价蓝图` 的经验层知识库，不是第二份目标与评价蓝图合同。
- 调用 `.agents/skills/lesson/3-目标与评价蓝图/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-objective-assessment-blueprint-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 学习目标只是章节主题或知识点名称 | objective measurability gap | 回到行为、条件、标准和知识/能力锚点重写 | `N4` 必须检查可观察、可测量、可评价 | 每条目标都有行为动词和成功标准 |
| 目标脱离受众、场景或业务目标 | upstream anchor drift | 回到第 1 阶段定位和第 2 阶段 handoff 抽锚点 | `N2` 必须形成 upstream anchor | 目标可追溯到定位和知识模型 |
| 评价证据变成完整题库 | stage boundary drift | 删除题目、答案和解析，只保留证据类型、采证方式和可接受表现 | `6-活动练习与测评开发` 拥有题库和练习 | 第 3 阶段输出不含完整题目 |
| rubric 等级描述空泛 | rubric threshold gap | 补表现维度、等级差异、通过阈值和常见扣分点 | `N6` 必须绑定评价证据 | rubric 能指导后续测评开发 |
| alignment 只有目标和活动，没有测评证据 | alignment completeness gap | 为每条目标补活动类型、测评证据、rubric 维度和 owner | `N7` 必须做目标-活动-测评-rubric 四联对齐 | alignment matrix 行完整 |
| 为了补齐目标而虚构知识证据 | evidence hallucination | 标记上游缺口或待确认，不强行定稿 | 上游不足时回到 `2-资料吸收与知识建模` | 缺证据目标有 N/A 理由 |
| 下游 handoff 不说明 owner | handoff ambiguity | 补 `4/5/6/8` 各自消费字段和限制 | `N10` 必须输出 owner map | downstream-handoff 可直接路由 |

## Repair Playbook

1. 先确认 `course-positioning.md` 和第 2 阶段知识模型是否足够；没有上游锚点不要凭空写目标。
2. 对每条学习目标按“行为动词、条件/场景、成功标准、知识/能力锚点、评价证据”检查。
3. 如果用户要求题库、答案解析或具体练习，把需求路由到第 6 阶段；本阶段只保留评价证据蓝图。
4. rubric 不要只写“优秀/良好/一般”；每个等级要能区分可观察表现。
5. alignment matrix 至少要连接目标、知识锚点、活动类型、测评证据、rubric 维度和后续 owning stage。
6. 如果目标数量超过 12 条，优先分组或提升层级；不要生成难以维护的超长目标清单。
7. 如果评价场景缺失，用保守假设并列为待确认，不把考试型评价强行套到实操型课程。

## Reusable Heuristics

- 好的学习目标不是“学生理解某概念”，而是“在某场景下完成某动作，并达到可观察标准”。
- 评价证据要先服务目标，再服务活动；活动有趣但不能采证时，不应成为核心测评依据。
- rubric 的价值是降低后续活动和题库开发的主观漂移，而不是提前写完整评分手册。
- 第 3 阶段的 alignment 只写活动类型和测评意图，完整活动流程和题目细节交给第 6 阶段。
- 企业内训类课程通常需要行为证据或工作产出证据；纯知识测验只能覆盖较低层目标。
- 对初学者课程，目标层级宜少而清晰；过多高阶目标会让后续正文和测评无法承载。
- 下游 handoff 要明确哪些目标适合课程架构、哪些适合练习测评、哪些只适合课件提示。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: objective_assessment_stage_contract_creation
- outcome: 建立 lesson 第 3 阶段的 backward-design runtime spine。
- design_decision: 以上游定位和知识模型为锚点，先定可测目标，再配评价证据和 rubric，最后生成目标-活动-测评 alignment。
- replication_checklist: 锁上游 -> 定范围 -> 写目标 -> 配证据 -> 做 rubric -> 对齐 -> 多 MD 写回 -> review。
- evidence_paths: `.agents/skills/lesson/3-目标与评价蓝图/SKILL.md`
