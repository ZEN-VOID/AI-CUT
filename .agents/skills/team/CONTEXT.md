# Context: team

本文件是 `.agents/skills/team/` 根技能的经验层。它只沉淀跨部门、跨人物、跨子技能的路由与治理经验；单人物视角的局部经验应写入对应人物目录的 `CONTEXT.md`。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~6000
current_lines: ~90
current_cases: 0
status: ok
recommended_action: keep-target-scoped-knowledge-updates
last_checked_at: 2026-04-15T09:45:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| TM-TEAM-01 | 用户点名人物，却被路由到同部门其他人物 | 路由裁决层 | 回到用户显式点名的人物子技能 | 在根 `SKILL.md` 中保持“用户点名优先”规则；子技能描述只做触发补充 | 最终加载路径与用户点名一致 |
| TM-TEAM-02 | 未点名人物时按表层风格词误触 | 需求分析层 | 先按任务对象判定部门，再选人物 | 将 `target_object -> department_route` 作为默认路由顺序 | 路由说明能解释为什么选该部门 |
| TM-TEAM-03 | 多视角会诊输出变成并列摘抄，没有结论 | 汇流合同层 | 根层重写 synthesis，裁决共识、冲突和取舍 | council mode 限定 2-4 个必要视角，并固定 parent synthesis gate | 最终只有一个可执行建议 |
| TM-TEAM-04 | 子技能事实越界，像本人新近发言或私人记忆 | 事实边界层 | 删除伪造内容，补“公开资料蒸馏”边界；必要时检索核验 | 根层保持 `fact_risk` 字段，子技能继续写明事实型问题先核验 | 无未核验引用、近况或私人动机 |
| TM-TEAM-05 | 根层经验写进人物 `CONTEXT.md`，导致局部文档膨胀 | 经验落点层 | 将跨技能经验移回 `team/CONTEXT.md` | 采用“最窄有效作用域”规则：跨人物写根层，单人物写本地 | 经验适用范围与落点一致 |
| TM-TEAM-06 | 子技能本地规则被根合同覆盖，人物视角失真 | 真源边界层 | 还原子技能的本地身份、语气、工作流 | 根合同只治理 taxonomy、route、load、synthesis、repair，不复制人物模型 | 根文档不含具体人物心智模型 |
| TM-TEAM-07 | 批量维护时多个兄弟技能重复改同一规则 | canonical source 层 | 判断共享规则是否应上收到根 `SKILL.md` 或根 `CONTEXT.md` | 若同一规范影响 2+ 子技能，先建立根级真源再让子技能继承/特化 | 兄弟技能不再静默分叉 |
| TM-TEAM-08 | 调用子技能时跳过本地 `CONTEXT.md` | 加载顺序层 | 重新加载根 `CONTEXT.md` 和命中子技能 `CONTEXT.md` | Root 与子技能均保留 Context Loading Contract | 输出能说明加载过的根/子上下文 |

## Repair Playbook

1. 先判断问题是 `路由错误`、`事实越界`、`角色口吻失真`、`汇流失败`、`加载缺口`，还是 `经验落点错误`。
2. 路由错误优先检查用户点名、任务对象、部门 taxonomy 和子技能 description，不急着改人物正文。
3. 事实越界先删除或标注未核验内容；若用户问题依赖新近事实、具体引用、奖项、项目近况或历史争议，必须检索或核对来源。
4. 会诊结果分裂时，减少参与子技能数量，再由根层 synthesis gate 裁决，而不是继续追加更多视角。
5. 若同类失败出现在多个部门或人物技能，先补根 `CONTEXT.md` Type Map；稳定后再晋升根 `SKILL.md`。
6. 若只有单人物本地输出问题，优先修该人物 `CONTEXT.md` 或 `SKILL.md`，不要把局部经验上收成根规则。

## Reusable Heuristics

- team 根技能的价值在于“选对视角并汇流”，不是把每个大师的内容重新写一遍。
- 用户点名人物时，路由不应自作聪明；只有当用户目标和点名明显冲突时，才说明假设并建议替代视角。
- 未点名人物时，先看任务对象再看风格词：结构问题通常先进编剧组，场面先进导演组，表演进演员组，影像进摄影组，空间/服装/美术进设计组，打戏进武术组。
- council mode 的质量来自必要性和裁决，不来自参与人数；超过 4 个视角通常会稀释结论。
- 子技能的“我”是一种公开资料蒸馏出的工作视角，不是历史人物或现实创作者本人；事实型问题要把这个边界放在创作判断前面。
- 经验沉淀按最窄有效作用域落盘：跨人物写根 `CONTEXT.md`，单人物写本地 `CONTEXT.md`，稳定规则再晋升 `SKILL.md`。
- 共享规范影响 2+ 兄弟技能时，优先建立或恢复根级 canonical source，而不是批量复制同一句规则。
- 根层输出的 `思考过程` 应解释路由、关键判断和汇流理由，不应展开子技能完整草稿。

## Promotion Backlog

| candidate_id | pattern | current_scope | promotion_condition | target |
| --- | --- | --- | --- | --- |
| PB-TEAM-01 | 多视角会诊默认限制为 2-4 个必要视角 | root heuristic | 在两次以上独立任务中证明能减少空泛并提高裁决质量 | 根 `SKILL.md` council hard gate |
| PB-TEAM-02 | 事实型问题先核验再进入角色视角 | root heuristic + child local rules | 若继续出现跨人物事实越界，提升为更强的根层 mandatory gate | 根 `SKILL.md` fact-risk gate |
| PB-TEAM-03 | 任务对象优先于表层风格词 | root routing heuristic | 若多次解决误触发，可写入更细的 route matrix | 根 `SKILL.md` Department Taxonomy 或独立 route spec |
