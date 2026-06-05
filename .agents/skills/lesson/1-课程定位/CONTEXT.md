# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/1-课程定位` 的经验层知识库，不是第二份课程定位合同。
- 调用 `.agents/skills/lesson/1-课程定位/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-positioning-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 定位阶段开始写完整课程大纲或课时正文 | stage boundary drift | 删除或移出越界正文，回到领域/受众/场景/目标/边界/交付约束 | 后续 `4` 和 `5` 阶段拥有大纲和正文 | 定位文档只有定位与 handoff |
| 用户只给模糊想法却直接定稿 | slot evidence gap | 进入对话模式，优先澄清核心槽位 | 快速模式必须检查槽位覆盖率 | `POS-01` 到 `POS-06` 有结论或待确认 |
| 对标课程被当成可复刻模板 | benchmark boundary failure | 只提炼定位启发、差异化和风险 | 输出中写明不可复刻边界 | section 9 不含照搬结构或文案 |
| 图片/链接/视频不可访问仍被当成事实 | evidence hallucination | 标记不可访问或待补证据，只使用可见内容和用户描述 | 证据清单必须有状态字段 | section 10 可追踪资料状态 |
| 受众画像混淆购买者、学习者和使用者 | audience role ambiguity | 在问卷中拆分决策者、学员、使用场景和评价者 | 目标受众章节固定说明角色差异 | section 3 有角色说明 |
| 课程定位与学习目标阶段互相吞并 | stage ordering ambiguity | 本阶段只写目标方向和成功指标，不写完整目标矩阵 | `3-目标与评价蓝图` 承接可评价目标 | section 5 不含完整目标表 |
| 快速模式只生成定位 MD，忘记检查上游项目根或输出下一入口 | workflow automation gap | 回到 `N0A` 和 `N7`，补项目根状态、资料状态和推荐下一阶段入口 | 快速模式 completion gate 绑定 upstream state 和 handoff | 最终回复含 automation report |

## Repair Playbook

1. 先判断当前输入是快速模式、对话模式还是资料优先。
2. 如果核心槽位不足，不要急着写定位文档；先输出最多 8 个高优先级问题。
3. 如果用户提供多模态资料，先建立证据清单；不可访问资料不得猜测。
4. 如果用户要求“像某某课程一样”，先提炼可借鉴的定位维度，再写差异化和不可复刻边界。
5. 如果正式写回，确认路径只能是 `projects/lesson/<项目名>/1-课程定位/course-positioning.md`。
6. 如果用户明确说“以后都按这个语气/品牌/禁区”，同步写入项目根 `MEMORY.md`，不要只放在定位文档里。
7. 快速模式不是单文件生成器；必须同时交代上游项目根/资料状态和下游可继续执行的入口，除非用户明确只要草案。

## Reusable Heuristics

- 课程定位最重要的不是把字段填满，而是让后续阶段不用猜：为什么做、给谁用、在哪里用、做到什么程度、哪些不做。
- 快速模式不是跳过澄清；它只是把缺口显式写入 `待确认项`，并在缺口影响核心判断时退回对话模式。
- 对话模式问题要短而有决策价值；能改变课程结构、目标或交付方式的问题优先。
- 受众画像至少拆成角色、基础、痛点、动机和约束；“所有人都能学”通常是定位失败信号。
- 使用场景会强烈影响课程语气和交付物：企业内训、公开课、自学课、考试课、销售赋能课的定位不同。
- 课程边界必须同时写包含和排除；只写“课程包括什么”不足以阻止后续膨胀。
- 对标课程的价值是帮助定位差异，不是帮后续阶段复制结构和话术。
- 定位文档中的目标只到“方向和成功指标”，完整可测学习目标归 `3-目标与评价蓝图`。
- 快速模式的自动化只允许非破坏性上游检查、初始化/恢复路由、证据状态整理和下游 handoff；真正的后续阶段主稿仍由对应阶段拥有。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: positioning_stage_contract_creation
- outcome: 建立 lesson 课程定位阶段的双模式 runtime spine。
- design_decision: 快速模式和对话模式共用同一 MD 输出 schema；资料、图片、链接和视频先转为证据状态，再进入槽位判断。
- replication_checklist: 先判项目和模式，再查槽位，再取证或提问，最后合成 MD 和 handoff。
- evidence_paths: `.agents/skills/lesson/1-课程定位/SKILL.md`
