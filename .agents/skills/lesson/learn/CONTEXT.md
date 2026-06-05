# CONTEXT.md

本文件是 `lesson-learn` 的经验层知识库，不是第二份执行合同。它用于沉淀课程课件学习吸收中的来源摄取、版权可信度裁决、owner 映射、gap 诊断、最窄写回和审计经验。

## Purpose & Loading Contract

- 每次调用 `$lesson-learn` 时，必须同时加载同目录 `CONTEXT.md`。
- 本文件只保存经验性 Type Map、Repair Playbook 与 Reusable Heuristics，不改写 `SKILL.md` 的入口、模式、节点、gate 或输出合同。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > `lesson-learn/SKILL.md` > owning skill `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 30000
hard_limit_chars: 60000
status: ok
recommended_action: keep-source-first-learning-heuristics
last_checked_at: 2026-06-05
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只看课件摘要就要求改 lesson 根规则 | evidence layer | 先补 source digest、版权边界和适用场景 | 学习任务先过 `N2-SOURCE` 再做 owner 映射 | final packet 含 locator、anchor 或缺口说明 |
| 外部课程结构被直接写成阶段真源 | satellite boundary layer | 回到 `N5-MAP`，只给 gap 和落点建议 | learn 卫星不直接覆盖阶段 canonical files | changed_files 不包含阶段主稿 |
| 竞品课件文案被复制进技能包 | copyright layer | 降级为教学设计原则、结构启发或风险提示 | `N4-VERIFY` 固定检查版权和引用边界 | audit_result 无版权复制阻断 |
| 项目个案经验被写成跨项目规则 | memory boundary layer | 区分项目 `MEMORY.md`、项目 `CONTEXT/`、技能 `CONTEXT.md` | `N9-DEPOSIT` 先判定经验作用域 | deposition_note 说明最窄落点 |
| 只生成学习报告但没有 gap_matrix 或 owner | execution closure layer | 回到 `N5-MAP` 补 owner、landing_set 和 sync_scope | 报告不能替代学习包和改进计划 | final_packet 含 gap_matrix 和 improvement_plan |
| 执行写回后没有审计 | validation layer | 运行 `N8-AUDIT`，检查 changed_files、版权、边界和残余风险 | execute_improvement 必须以 audit_result 收束 | audit_result 为 pass 或 pass_with_followups |
| 脚本转写或引用扫描结果被当成教学设计判断 | LLM-first layer | 废弃机械结论，回到 LLM 判断节点 | 脚本只做读取、转写、引用扫描、diff、校验 | final_packet 说明 LLM adoption decisions |

## Repair Playbook

1. 先锁定学习对象、目标范围、写回权限和是否绑定 `projects/lesson/<项目名>/`。
2. 任何外部课件、课程、书籍或视频都先做 source digest；记录访问状态、版权、可信度、适用对象和证据缺口。
3. 学到的方法先抽象成原则和适用条件，不复制原课程表达、课件文案或完整结构。
4. 建立 target_skill_map：lesson 根、0-8 阶段、8 的 doc/ppt/html 叶子、卫星、项目 `MEMORY.md`、项目 `CONTEXT/` 或本技能经验层。
5. 改进落点选择最窄有效 owner；跨阶段同步只同步消费者和控制面，不复制第二真源。
6. 单项目偏好、品牌口径和禁区不写进跨项目技能规则；只有跨项目可复用失败模式才写技能 `CONTEXT.md`。
7. 执行型写回完成后必须审计 changed_files、owner、版权降级、卫星边界、LLM-first 和残余风险。
8. 如果 source digest、target_skill_map 和写回权限已齐备，不要停在报告；按最窄 owner 执行写回或明确 blocker。

## Reusable Heuristics

- `lesson-learn` 的核心产物不是摘要，而是 `source_digest + gap_matrix + owner landing + audit_result`。
- 优秀课件通常只能提供结构、节奏、活动形态和表达策略的启发，不能直接成为项目或技能真源。
- 课程标准和官方指南可提升可信度，但仍要检查适用地区、版本、受众、课程层级和版权边界。
- 参考课程越完整，越要慢一步：先判断它的受众、目标、时长、评估方式是否与当前 lesson 项目匹配。
- 多端交付问题不要让 learn 卫星直接修 PPT 或 HTML；应映射到 `7-视觉媒体与交互设计` 或 `8-多端交付生成` 的 owning leaf。
- 报告只是追溯凭证；执行型学习吸收的终点是最窄写回通过审计。
- 外部材料中的具体表达要抽象成教学设计原则、rubric 启发、活动机制或风险清单，不能直接复制为模板正文。
- `content-model/` 是三端投影的共享上游，不是 learn 卫星写入新主稿的入口。
