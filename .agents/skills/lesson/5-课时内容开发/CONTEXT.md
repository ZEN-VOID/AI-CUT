# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/5-课时内容开发` 的经验层知识库，不是第二份课时内容开发合同。
- 调用 `.agents/skills/lesson/5-课时内容开发/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-lesson-content-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 课时正文脱离知识证据、学习目标或课程架构 | upstream anchor drift | 回到 `N2-UPSTREAM-ANCHOR`，重建 2/3/4 上游锚点 | 正式写回前必须有课时到目标、概念和证据的映射 | `objective_alignment_map` 可追溯 |
| 讲师稿看似完整但全是套话 | authorship gap | 废弃机械化正文，回到 `N4-LESSON-AUTHORING` 由 LLM 逐课时重写 | LLM-first gate 阻断脚本批量生成、正则套句和映射投影 | `authorship_note` 说明创作依据 |
| 只写讲师稿，缺学习者材料或案例/概念解释 | material split gap | 回到 `N5-MATERIAL-SPLIT`，按 `LC-01` 到 `LC-08` 补齐 | 输出 schema 固定讲师、学员、案例、概念和媒体占位 | `coverage_matrix` 无缺口或有 N/A 理由 |
| 案例解释使用弱证据或越过项目禁区 | case evidence boundary failure | 补 source id、限制和替代案例；必要时回到第 2 阶段 | 项目 `MEMORY.md` 的案例禁区优先，弱证据不写成强事实 | `case-and-concept-notes.md` 有证据状态 |
| 媒体占位变成视觉系统或成品素材 | stage boundary drift | 删除视觉规范和成品素材，把需求路由给第 7 阶段 | 本阶段只写媒体意图、内容点和占位说明 | `media-placeholders.md` 不含视觉系统 |
| 课时内容阶段顺手生成完整题库 | assessment overreach | 移除题库、答案解析和 rubric，路由到第 6 阶段 | 第 5 阶段只可写活动/练习提示边界，不生成完整活动题库 | 输出不含 question bank |
| Markdown 内容包被直接投影成 DOC/PPT/HTML | delivery overreach | 回到 Output Contract，保留 Markdown 内容包并路由第 8 阶段 | 第 8 阶段拥有 DOC/PPT/HTML 生成 | 无 `.docx`、`.pptx`、`.html` 成品 |

## Repair Playbook

1. 先确认当前请求是否属于第 5 阶段：课时讲授内容、讲师稿、学习者材料、案例解释、概念展开或媒体占位。
2. 正式写回前检查第 2 阶段知识证据、第 3 阶段目标蓝图、第 4 阶段课程架构；缺失时不要硬写全课时正文。
3. 每个课时先做目标、概念、案例和时长映射，再写正文；不要从标题直接扩写。
4. 讲师稿要能服务讲授现场，学习者材料要能服务课后复习；两者不要简单复制同一段文字。
5. 案例必须带来源、适用受众、限制和风险；内部案例、客户案例和敏感行业案例优先检查项目记忆。
6. 媒体占位只写“需要表达什么”和“素材/图表/演示意图”，不写视觉风格系统。
7. 如果用户要求题库、练习、测验或答案解析，把需求交给第 6 阶段；第 5 阶段只保留可转活动的内容点。
8. 如果用户要求 PPT/DOC/HTML，先完成 Markdown 内容包，再由第 8 阶段投影，不在第 5 阶段生成成品。

## Reusable Heuristics

- 课时内容的质量取决于三重对齐：知识证据说得准，学习目标说得清，课程架构说得顺。
- 讲师稿不是逐字朗读稿越长越好；它要标出讲授意图、强调点、转场、易错提醒和现场判断点。
- 学习者材料应比讲师稿更结构化，偏向术语、步骤、清单、复盘和延伸阅读。
- 案例解释要回答“为什么现在讲这个案例、学员应该看见什么、哪些结论不能从案例推出”。
- 关键概念展开通常需要定义、通俗讲法、例子、反例和常见误解；只有定义不足以支撑教学。
- 媒体占位是给第 7 阶段的内容需求，不是视觉方案；写清表达意图比指定风格更重要。
- 局部修复要保护未命中的课时，最终报告应列出 scope 和未触碰范围。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: content_development_stage_contract_creation
- outcome: 建立 lesson 第 5 阶段的 LLM-first 课时内容开发 runtime spine。
- design_decision: 以 2/3/4 上游锚点控制每课时正文，输出讲授内容、讲师稿、学习者材料、案例与概念讲解、媒体占位和下游 handoff；不生成完整活动题库、视觉系统或三端成品。
- replication_checklist: 锁上游 -> 逐课时设计 -> LLM 创作 -> 材料拆分 -> 写回 -> review -> handoff。
- evidence_paths: `.agents/skills/lesson/5-课时内容开发/SKILL.md`
