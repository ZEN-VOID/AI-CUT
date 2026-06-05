# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/7-视觉媒体与交互设计` 的经验层知识库，不是第二份视觉媒体与交互设计合同。
- 调用 `.agents/skills/lesson/7-视觉媒体与交互设计/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-visual-media-interaction-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 第 7 阶段变成泛美化或视觉主题选择 | upstream anchor drift | 回到 3-6 阶段目标、架构、正文和活动测评，重新建立设计范围 | `N2-UPSTREAM` 必须形成 upstream matrix | 每个关键视觉决策可追溯到教学意图 |
| 视觉系统只写色彩和字体 | visual system coverage gap | 补信息层级、版式节奏、图标、图片风格、动效、品牌禁区和多端边界 | Pass Table 要求至少 8 个视觉槽位 | `visual-system.md` 能指导第 8 阶段 |
| 媒体 brief 伪造素材来源或版权状态 | asset provenance failure | 把素材标记为待确认、需采购、需拍摄、需生成或用户提供，不写成已授权 | 媒体条目必须有来源状态和替代方案 | `media-asset-brief.md` 不含伪造授权 |
| 图解规划与课程内容脱节 | diagram anchor gap | 为每个图解补内容锚点、学习目标和落点 | 图解规划要消费第 5 阶段正文和第 3 阶段目标 | 图解条目有用途和下游落点 |
| 交互模型只有功能名没有状态 | interaction state gap | 补入口、动作、反馈、状态、失败路径、讲师操作和平台边界 | `interaction-model.md` 必须有状态模型 | 第 8 阶段能实现或降级 |
| 无障碍只写口号 | accessibility operational gap | 补对比度、字号、键盘/焦点、替代文本、字幕、认知负荷和移动端要求 | 无障碍要求必须可检查 | `accessibility-requirements.md` 有检查项 |
| 输出开始生成 PPT/HTML/DOC 成品 | delivery stage boundary drift | 删除成品生成内容，保留视觉交付约束并路由到第 8 阶段 | Output Contract 固定第 7 阶段只写 MD 设计规划 | 无 `.pptx/.html/.docx` 成品写回 |
| 视觉设计改写课时正文或题库 | owning stage overreach | 回到第 5 或第 6 阶段，视觉阶段只引用而不改写 | Core Task Contract 明确非目标 | 输出不含讲稿、题库或答案解析 |

## Repair Playbook

1. 先确认任务是否属于第 7 阶段；如果用户要最终 PPT/HTML/DOC，路由第 8 阶段。
2. 正式写回前检查 3-6 阶段四类输入；缺目标、结构、正文或活动测评时，不要凭想象定稿。
3. 视觉系统先服务学习体验，再谈色彩和风格；避免只做装饰。
4. 媒体资产 brief 必须区分已提供、需制作、需采购、可生成、待授权和不可用素材。
5. 图解规划优先覆盖复杂概念、流程、对比、数据证据、案例拆解和学习路径，不为每页强行配图。
6. 交互模型要写清动作、反馈、状态和失败路径；否则第 8 阶段只能做静态页面。
7. 无障碍要求要可执行；如果法规或组织标准不明，采用保守要求并列待确认项。
8. 若用户明确说“以后都按这个品牌/视觉禁区/无障碍标准”，同步更新项目 `MEMORY.md`；一次性素材和设计结论写第 7 阶段输出。

## Reusable Heuristics

- 第 7 阶段的价值不是“好看”，而是让课程变得可观看、可演示、可操作，同时让第 8 阶段少猜。
- 一个好的视觉系统要同时回答：学员先看哪里、内容如何分层、复杂概念如何图解、交互在哪里发生、错误如何反馈。
- PPT 和 HTML 的视觉约束不同：PPT 更重讲师节奏和大屏可读，HTML 更重导航、状态、响应式和键盘可达。
- 媒体 brief 不等于素材生成；它应说明素材目的、使用位置、来源限制、替代方案和优先级。
- 交互越多不一定越好；每个交互都应服务学习目标、练习反馈或认知分块。
- 无障碍要求越早进入第 7 阶段，第 8 阶段越少返工。
- 如果第 7 阶段发现正文、活动或测评无法视觉化，通常是第 5 或第 6 阶段表达结构不清，应回到 owning stage。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: visual_media_interaction_stage_contract_creation
- outcome: 建立 lesson 第 7 阶段的 runtime-spine 技能包。
- design_decision: 以 3-6 阶段输入为设计锚点，输出七份 canonical MD 供第 8 阶段投影，不生成最终 PPT/HTML/DOC。
- replication_checklist: 锁上游 -> 定设计范围 -> 视觉系统 -> 媒体/图解 -> 交互/无障碍 -> 交付约束 -> 写回 -> review -> handoff。
- evidence_paths: `.agents/skills/lesson/7-视觉媒体与交互设计/SKILL.md`
