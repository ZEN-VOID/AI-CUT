# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/lesson/benchmark` 的经验层知识库，不是第二份执行合同。
- 调用 `$lesson-benchmark` 时，它必须与同目录 `SKILL.md` 一起加载，用于识别 benchmark 证据不足、版权边界、维度漂移、owner route 越权和报告真源混淆。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md` > 外部 benchmark 材料。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
recommended_action: keep-benchmark-heuristics-focused
```

## Type Map

| type_id | symptom | likely root layer | immediate fix | verification |
| --- | --- | --- | --- | --- |
| `LESSON-BM-TM-01` | benchmark 报告只写“竞品更好”但没有证据 | evidence layer | 回到 `N3-BENCHMARK-EVIDENCE`，补 locator、用户摘录、截图或标准条目 | 每条结论有 benchmark evidence |
| `LESSON-BM-TM-02` | 直接把竞品课件正文、题库或讲义复制进报告 | copyright boundary layer | 删除复制内容，改成短证据摘要、维度描述和差距判断 | 输出无长段复制正文 |
| `LESSON-BM-TM-03` | 对标维度无法落到 lesson 1-8 阶段 | dimension mapping layer | 回到 `N4-DIMENSION-MAP`，按定位、资料、目标、架构、正文、测评、视觉、交付归一 | 每个建议有 stage owner 或不适用说明 |
| `LESSON-BM-TM-04` | benchmark 直接改写课程正文、题库、PPT 或 HTML | satellite boundary layer | 输出 owner route，改写动作交给对应阶段或 repair | 业务真源未被 benchmark 写入 |
| `LESSON-BM-TM-05` | 把行业标准当成必须全量采用 | tradeoff layer | 补项目目标、受众、场景、时长、预算和平台约束，形成 adopt/adapt/reject | 每条建议有取舍理由 |
| `LESSON-BM-TM-06` | 竞品、标准和项目现状混在一起导致 owner 冲突 | scope lock layer | 先锁单一项目根、单一主目标和 benchmark object 清单 | final packet scope 清楚 |
| `LESSON-BM-TM-07` | 只给评分不说明下一入口 | owner route layer | 为每条高优先级差距指定 owning stage、下游影响和阻断项 | next_entry 唯一或 blocker 明确 |
| `LESSON-BM-TM-08` | 用脚本或表格模板批量生成 gap matrix | authorship layer | 废弃机械结论，LLM 逐项基于项目证据与 benchmark 证据裁决 | review result 记录 authorship note |

## Repair Playbook

1. 先锁定 benchmark 类型：竞品课程、标准 rubric、项目阶段、gap-only、improvement route 或 audit-only。
2. 证据不足时，不急着写建议；先补 source locator、用户摘录、截图、目录、标准条款编号或说明不可验证假设。
3. 外部资料涉及版权时，只保留必要短摘录和 paraphrase，重点输出维度、差距、取舍和 owner route。
4. 维度过散时，回到 lesson 1-8 阶段表：定位、资料、目标评价、策略架构、课时正文、活动测评、视觉交互、多端交付。
5. 建议看起来“合理”但没有 owner 时，必须降级为待路由建议，不得让 benchmark 自己写阶段主稿。
6. 对平台课或竞品课件，只评价结构、节奏、评估方式、交互方式、案例策略和交付质量；避免复刻表达、题目和页面文案。
7. 标准对齐类 benchmark 要区分 must-have、should-have 和 nice-to-have，防止过度合规破坏项目目标。
8. 若用户只要评分，仍要输出评分依据、证据、缺口和下一入口，不能给无证分数。
9. 若用户要求落盘报告，报告只是 side carrier；阶段 canonical files 由 owning stage 或 repair 写入。
10. 发现同类失败模式，先写入本 `CONTEXT.md`，稳定后再提炼到 `SKILL.md`。

## Reusable Heuristics

- lesson benchmark 的价值不是“模仿最强竞品”，而是把外部强项翻译成当前项目可执行的 stage route。
- 高质量 benchmark packet 至少回答四件事：证据在哪里、差距是什么、为什么值得改、应该由哪个 stage 改。
- 竞品课程优点通常要降维成教学设计变量，例如目标清晰度、认知负荷、案例贴合、练习密度、反馈机制和交付可读性。
- 标准和考试大纲更适合校准目标、评价证据和覆盖范围，不应直接替代课程架构和课时讲稿。
- 企业培训范例更适合校准场景、角色、任务流和绩效指标，但需要与当前受众、业务环境和时长约束做取舍。
- 对 DOC/PPT/HTML 的 benchmark 应优先查共享内容模型和第 8 阶段投影关系，避免三端各自形成新主稿。
- 只要建议需要写进课程正文、题库、视觉系统或交付物，就必须回到 owning stage；benchmark 只能给路线和证据。
- 当 benchmark 对象证据弱于项目内证据时，应把建议标成 low confidence 或 hold，而不是为了完整性强行采用。

## Case Log

> 仅记录可复用里程碑案例，避免过程流水账。

### Case-001

- milestone_type: satellite_initialization
- outcome: 建立 lesson benchmark core runtime-spine 卫星技能包。
- design_decision: 只做基准证据、差距矩阵、取舍建议和 owning stage 改进路线，不创建 optional modules，不作为独立 review stage。
- evidence_paths: `.agents/skills/lesson/benchmark/SKILL.md`, `.agents/skills/lesson/benchmark/CONTEXT.md`
