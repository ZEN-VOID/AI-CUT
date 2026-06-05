# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/6-活动练习与测评开发` 的经验层知识库，不是第二份活动测评合同。
- 调用 `.agents/skills/lesson/6-活动练习与测评开发/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-assessment-design-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 题库看起来很多但无法映射学习目标 | alignment drift | 回到 `N3-ALIGNMENT`，补目标-内容-测评矩阵 | 每题必须有 `objective_ref`、`knowledge_ref` 或明确 N/A | question-bank metadata 可追踪目标 |
| 活动设计变成重写课程架构 | stage boundary drift | 删除重排模块或课时的内容，回到第 4 阶段 owning skill | 本阶段只消费架构，不改课程路径 | 活动说明不改变模块/课时顺序 |
| 答案解析变成讲稿正文 | lesson content drift | 压回答案、思路、错因和知识点回扣 | 讲解正文归第 5 阶段，解析只服务作答反馈 | answer-explanations 不含完整授课讲稿 |
| rubric 只有形容词，没有可评分行为证据 | scoring ambiguity | 补行为证据、等级描述、分值和扣分项 | 主观任务必须绑定 rubric | scoring-rubrics 可支持讲师一致评分 |
| 形成性测评缺失，只剩期末考试 | assessment balance failure | 补课前诊断、课中练习或课后反思 | 形成性和总结性均需覆盖或给 N/A 理由 | assessment-package 有两类测评说明 |
| 脚本或模板批量套出题目 | creative authorship violation | 废弃机械题目，回到 LLM-first 节点逐题判断 | scripts/templates 只能做机械辅助，不写创作正文 | review 有 anti-scripted authorship note |
| 输出直接进入 PPT/DOC/HTML 文案 | delivery overreach | 转路由到第 8 阶段，本阶段只提供下游 handoff | `downstream-handoff.md` 只写消费说明 | 第 6 阶段无三端成品 |

## Repair Playbook

1. 先确认 3/4/5 上游产物是否存在；不要在缺目标、缺架构、缺课时内容时凭空出题。
2. 先建目标-内容-测评对齐矩阵，再写活动、题目和 rubric。
3. 每个活动至少说明目标、步骤、时长、材料、提交物和反馈方式。
4. 每题至少保留目标映射、知识点、难度、答案或评分点、解析引用和使用场景。
5. 主观题和项目任务优先补 rubric；客观题优先补答案、干扰项解析和错因反馈。
6. 如果用户只要局部题库或活动，也要列出未覆盖对象的 N/A 理由，避免被误认为完整测评包。
7. 如果用户明确要求长期题型偏好、评分禁区或反馈语气，写入项目 `MEMORY.md`；一次性题目和解析只写第 6 阶段输出。
8. 发现机械批量生成痕迹时，不做局部润色，必须回到 LLM-first 创作节点重做。

## Reusable Heuristics

- 好题库不是题量多，而是每题都能说明测什么、为什么这样问、学生答错说明什么。
- 活动设计要服务行为证据；如果活动没有可观察产出，就很难形成评分和反馈。
- rubric 的核心是可观察行为和等级差异，不是“优秀/良好/一般”的同义词列表。
- 形成性测评更适合诊断误区和推动学习，不能只靠总结性考试证明课程有效。
- 答案解析要回扣知识点和常见错因，避免只给标准答案。
- 评价包要让讲师知道什么时候用、怎么收、怎么评、怎么反馈，而不只是给学生题目。
- 对 AI、销售、管理、合规等应用课，情境题和综合任务通常比孤立记忆题更能证明迁移。
- 本阶段输出应为后续 DOC/PPT/HTML 提供唯一测评真源；三端交付只投影，不应各自新写题库。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: assessment_development_stage_contract_creation
- outcome: 建立 lesson 第 6 阶段活动练习与测评开发 runtime-spine core layout。
- design_decision: 阶段 6 以 3/4/5 上游为输入，输出活动练习、题库、评分规程、答案解析、rubric、形成性/总结性测评包和下游 handoff；不启用 optional modules。
- replication_checklist: 锁上游 -> 对齐目标 -> 设计活动 -> 开发题库 -> 制定评分与解析 -> 组包 -> 写回 -> review。
- evidence_paths: `.agents/skills/lesson/6-活动练习与测评开发/SKILL.md`
