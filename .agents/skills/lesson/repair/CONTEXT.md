# CONTEXT.md

本文件是 `lesson-repair` 的经验层知识库，不是第二份执行合同。它用于沉淀课程课件项目 source-first 修复中的 owner 判定、三端漂移、LLM-first 作者性、状态残留和回接路线经验。

## Purpose & Loading Contract

- 每次调用 `$lesson-repair` 时，必须同时加载同目录 `CONTEXT.md`。
- 本文件只保存经验性 Type Map、Repair Playbook 与 Reusable Heuristics，不改写 `SKILL.md` 的入口、模式、gate 或输出合同。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / skill-2.0 meta 规则 > lesson 根 `SKILL.md` > `lesson-repair/SKILL.md` > owning stage `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 30000
hard_limit_chars: 60000
status: ok
last_checked_at: 2026-06-05
recommended_action: keep-repair-heuristics-only
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只改 PPT 或 HTML 文案，下一轮 DOC 又出现旧术语 | delivery drift layer | 回到第 8 父包和共享内容模型，再同步叶子 | repair 先做 `delivery_consistency_matrix` | doc/ppt/html 三端术语和顺序同源 |
| 学习目标不可测却先改课时正文 | source owner shortcut | 回到第 3 阶段学习目标与评价蓝图 | owner 判定必须先看最早可修源层 | `canonical_owner` 指向第 3 阶段或说明例外 |
| 课时正文像模板套句 | scripted authorship layer | 标记 LLM-first 失败，回到 owning stage 逐条重写 | 禁止脚本批量生成、正则套句和映射投影正文 | `authorship_note` 可追溯到 source rules |
| 活动题目与目标不对齐 | assessment alignment layer | 回到第 6 阶段，并检查第 3 阶段目标与 rubric | 活动/题库必须有目标和知识点锚点 | alignment matrix 无孤立题目 |
| 视觉方案只做美化不服务学习 | visual overreach layer | 回到第 7 阶段，追溯 3-6 阶段上游 | 视觉/交互 brief 必须说明学习用途和下游落点 | visual evidence 包含 upstream anchors |
| `content-model/` 与阶段目录形成两套主稿 | content model truth split layer | 找 owning stage，`content-model/` 只保留索引、handoff 或授权共享片段 | 第 8 阶段不得首次主创课程质量 | 阶段 canonical files 是可追溯真源 |
| 删除交付物后 manifest 仍引用旧路径 | state residual layer | 同步项目内 manifest、进度索引、handoff 和消费者引用 | 删除/失效操作必须执行状态残留检查 | `sync_evidence` 列出残留为 0 或遗留项 |
| 用户长期品牌语气只写进本次报告 | project memory drift | 若用户明确长期要求，更新项目 `MEMORY.md` | intake 区分一次性修复和长期偏好 | MEMORY 与 repair packet 口径一致 |

## Repair Playbook

1. 先锁定 `projects/lesson/<项目名>/`、target locality、修复意图和写回权限。
2. 定位目标产物所属 stage、delivery parent 或 doc/ppt/html leaf，加载该 owning skill 的 `SKILL.md + CONTEXT.md`。
3. 建立 source review：列出 canonical owner candidate、canonical files、stage gate refs、禁止越权边界和 LLM-first gate。
4. 建立 impact map：upstream、current、neighbors、downstream、`content-model/`、delivery parent、doc/ppt/html leaves、manifest/state 和 future guardrails。
5. 先修最早 canonical owner，再同步 handoff、`content-model/`、第 8 父包和叶子消费者；不得用下游润色掩盖源层错误。
6. 对执行型内容修复，当前技能只形成 repair brief 或在授权范围内做最小局部写回；正文、题目、讲稿、slide/web 文案和设计正文必须由 LLM 基于 owning stage 合同判断。
7. 三端漂移先检查 shared content model 和第 8 父包，再决定 doc/ppt/html 叶子是否需要重验或同步 manifest。
8. 删除、失效或移动项目内产物时，同轮检查项目内状态、进度、manifest、handoff 和消费者引用残留。
9. 修复后必须执行 audit gate：source review、impact map、owner、permission、LLM-first、delivery consistency、changed files、old refs 和 residual risks。

## Reusable Heuristics

- lesson repair 的核心产物不是 patch，而是 `source_review + impact_map + canonical_owner + writeback_order`。
- 越靠后的产物越像症状：PPT/HTML 漂移通常源自第 8 父包、`content-model/`、第 5 阶段正文或第 3 阶段目标不稳。
- “课件更好看”不是合法 repair intent；应翻译成学习体验、信息层级、互动反馈、可访问性、目标对齐或交付端一致性。
- `content-model/` 适合承载跨端索引和 handoff，不适合替代阶段 canonical files。
- 题库和活动问题优先检查第 3 阶段目标与第 6 阶段 alignment，不要直接改答案解析。
- 视觉和交互问题优先检查第 7 阶段是否追溯 3-6 阶段上游，而不是直接在 PPT 或 HTML 叶子美化。
- 若用户要求“以后都按这个品牌语气/受众/禁区”，写项目 `MEMORY.md`；若只是本次返工，不污染长期记忆。
- repair 的脚本价值在定位和校验，不在主创；任何批量润色、批量出题、批量生成 slide 文案或 web 文案都要回到 LLM-first gate。

## Case Log

> 仅记录里程碑案例，避免过程流水账。

### Case-001

- milestone_type: satellite_runtime_spine_initialization
- outcome: 建立 `lesson-repair` core layout，固定 source-first 修复、owning stage 边界、三端漂移回接和 LLM-first 作者性门禁。
- design_decision: 本卫星只拥有诊断、影响图、owner 判定、repair brief、写回顺序和审计汇流权，不拥有 1-8 阶段主稿 ownership。
- evidence_paths: `.agents/skills/lesson/repair/SKILL.md`, `.agents/skills/lesson/repair/CONTEXT.md`
