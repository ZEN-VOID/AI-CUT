# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/8-多端交付生成/html` 的经验层知识库，不是第二份 HTML 交付合同。
- 调用 `.agents/skills/lesson/8-多端交付生成/html/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > 父包 `SKILL.md` > 本叶子 `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-html-delivery-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| HTML 叶子重新决定三端交付范围 | parent packet 缺失 | 回到父包生成 html leaf packet | HTML 叶子只消费父包 packet | `packet_inventory` 指向父包 manifest |
| 页面正文像模板套句 | LLM-first 违规 | 废弃机械产物，回到 `N4-LLM-WEB-ADAPTATION` | 脚本只做站点组装和校验 | authorship note 可追踪 |
| web 结构只有文件名 | architecture 缺口 | 回到 `N3-WEB-ARCHITECTURE` 补导航、页面和状态 | web 架构先于站点 manifest | plan 包含 routes 和 pages |
| HTML 组装覆盖了未授权页面 | update scope 漂移 | 只改受影响 pages/components 并更新 manifest diff | 正式写回前记录 overwrite note | changed pages 和 manifest 一致 |
| HTML 与 DOC/PPT 术语不一致 | cross-channel consistency 缺口 | 回到父包 delivery map 或本叶子 gate | 术语和目标以父包 map 为真源 | consistency section 无冲突 |
| 真实 HTML artifact 未调用 `claude-design`、未落盘或缺少设计质量证据 | executor handoff / writeback / quality gate 缺失 | 回到 `N6-WRITEBACK`，加载 `.agents/skills/claude-design/SKILL.md + CONTEXT.md` 后再生成/改造/验证，并补 artifact paths、writeback status、selected modules、visual system、browser verification 和 quality verdict | manifest 固定 `HTML-08-design-executor`，真实 artifact 执行器为 `.agents/skills/claude-design`，且只描述目标路径或泛化模板感设计不得 pass | `claude_design_handoff`、artifact_paths、writeback_status、selected_modules、visual_system、verification 和 quality_verdict 可见 |

## Repair Playbook

1. 先确认任务确实是 HTML、web course、静态站点、移动端阅读或 LMS 嵌入交付。
2. 缺父包 packet 时回到 `$lesson-delivery`，不要在 HTML 叶子补父包 manifest。
3. 设备、发布方式和交互要求不清时先定 web variant。
4. 所有 HTML/site 组装都必须从 LLM-approved page plan 和 manifest 出发。
5. 只要需要真实 `.html`、`index.html`、静态站点或现有 HTML 改造，就加载并调用 `.agents/skills/claude-design/SKILL.md + CONTEXT.md`；本叶子传递课程真源边界、页面计划、视觉约束、manifest、required upstream design modules、verification target 和目标路径，并回收 artifact paths、writeback status、selected modules、visual system、browser verification 与 quality verdict。
6. 修订既有 HTML 时只改受影响 pages/components，并同步 `html-site-manifest.json`。

## Reusable Heuristics

- HTML 的优势是导航、响应式阅读和轻交互，不应复制 DOC 长文或 PPT 短句。
- 页面计划要明确学习路径、状态、活动反馈和测评入口。
- 路由、资源复制、静态站点生成和校验属于机械组装，不属于网页正文主创。
- `claude-design` 负责高保真 HTML 视觉执行、交互 polish、能力模块选择、浏览器验证和 quality verdict；lesson HTML 叶子负责课程真源、页面计划、manifest 和路径边界。
- 最终 HTML artifact 未写入 `index.html` / 静态站点文件、或未返回 `writeback_status` 时，不得把设计说明或目标路径当作已交付成品。
- 如果 HTML artifact 看起来只是通用卡片/模板页面，即使 `artifact_paths` 和浏览器验证存在，也要回到 `N6/N7` 要求补强 visual system、信息层级、响应式行为和 quality verdict。
- 缺交互或可访问性要求时应保守列缺口，不臆造最终实现。
- 如果 HTML 与父包 map 冲突，优先修 HTML 叶子，不改父包事实。

## Case Log

### Case-001

- milestone_type: html_leaf_creation
- outcome: 建立 HTML/web 课程交付叶子的 Skill 2.0 runtime spine。
- design_decision: HTML 叶子拥有 web architecture、page plan、site manifest 和可选 HTML/site 组装目标。
- replication_checklist: 父包 packet -> web architecture -> LLM web 适配 -> site manifest -> consistency gate。
- evidence_paths: `.agents/skills/lesson/8-多端交付生成/html/SKILL.md`
