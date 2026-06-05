# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/2-资料吸收与知识建模` 的经验层知识库，不是第二份资料吸收合同。
- 调用 `.agents/skills/lesson/2-资料吸收与知识建模/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-research-and-knowledge-modeling-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 资料吸收变成泛百科资料堆砌 | positioning anchor drift | 回到 `course-positioning.md` 抽取受众、场景、目标和边界 | `N1` 必须先形成定位锚点和研究问题 | 输出研究范围可追溯到课程定位 |
| 只列链接不做证据审计 | evidence audit gap | 为每个 source 补访问状态、可信度、采用方式和限制 | `source_inventory` 不等于结论，必须进入 `N4` | 关键结论有 source id |
| 论坛观点被写成官方事实 | source hierarchy confusion | 回到来源分层，区分 official、practice、community、待核验 | Review gate 检查 source_class | 事实摘要不混淆来源层级 |
| 术语表只有名词没有教学口径 | pedagogy adaptation gap | 补推荐讲法、常见混淆和受众适配说明 | 术语表必须服务后续课程正文 | terminology 可直接供 `5` 使用 |
| 案例库变成完整课时正文 | stage boundary drift | 删除教学脚本和活动展开，只保留案例要点、证据和适用场景 | `5/6` 阶段拥有正文和活动设计 | 案例库不含完整讲稿或题目 |
| 用户补充资料全部写入 MEMORY | memory boundary drift | 只把长期偏好、禁区、资料优先级写入 `MEMORY.md` | 一次性事实和资料放第 2 阶段输出 | `MEMORY.md` 不承载阶段研究正文 |
| 知识依赖缺失导致后续目标/架构返工 | dependency modeling gap | 补前置、并列、后继和难度阶梯 | `KM-07` 为必需槽位 | downstream handoff 有依赖说明 |

## Repair Playbook

1. 先确认是否存在 `1-课程定位/course-positioning.md` 或等价定位 brief；没有定位不要开始泛化调研。
2. 对用户资料先建立 source inventory，再进入事实摘要；不要边读边直接定稿知识模型。
3. deep research 至少尝试覆盖官方/权威、实践/案例、社区/误区三类视角；缺某类时写 N/A 理由。
4. 易变事实、政策、产品能力、价格、版本、人物、公司、法规和软件行为必须联网核验，不使用过期记忆直接定论。
5. 关键事实优先用官方、标准、论文、原始资料；论坛和社区主要用来发现痛点、误区、常见问题。
6. 知识模型要服务目标受众和使用场景；不适合受众水平的高级概念可放入边界或后续扩展。
7. 如果用户说“以后都按这个资料优先级/禁区/品牌口径”，同步更新项目 `MEMORY.md`；如果只是给一次性文档，写入阶段输出。

## Reusable Heuristics

- 资料吸收阶段的价值不是找到最多资料，而是把资料转成“下游可以安全使用的知识真源”。
- 官方资料适合定义和规则，社区资料适合误区和痛点，案例资料适合教学情境；三者不能互相冒充。
- “可引用证据”不等于“可以长段复制来源文本”；课程中应使用短引用、事实转述和 source id。
- 概念层级至少要回答：这个领域有哪些大块、每块有哪些核心概念、哪些概念先学才不迷路。
- 术语表要写推荐讲法，否则后续课时正文容易在同一概念上换词漂移。
- 常见误区是教学设计的重要输入；它通常比完整百科条目更能决定活动、练习和案例安排。
- 依赖关系要保守：后续阶段宁可看到“待核验/先不讲”，也不要让课程建立在弱证据上。
- 本阶段输出多份 MD 比一个巨型文档更适合下游读取，但 canonical 文件名必须稳定。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: knowledge_modeling_stage_contract_creation
- outcome: 建立 lesson 第 2 阶段的 research-first runtime spine。
- design_decision: 以 `course-positioning.md` 锁定调研边界，先做 source inventory 和 evidence audit，再合成知识模型与下游 handoff。
- replication_checklist: 锁定位 -> 研究计划 -> 来源吸收 -> 证据审计 -> 知识模型 -> 多 MD 写回 -> review。
- evidence_paths: `.agents/skills/lesson/2-资料吸收与知识建模/SKILL.md`

