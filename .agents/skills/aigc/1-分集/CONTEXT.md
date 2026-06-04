# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-分集` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

- soft_limit_chars: 16000
- hard_limit_chars: 32000
- status: ok
- last_checked_at: 2026-06-04

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 默认源路径仍指向旧 `Original/` | 输入合同层 | 改为默认读取 `projects/aigc/<项目名>/源/`，旧路径只在用户指定或兼容任务中读取 | 在 `SKILL.md` 和 `references/input-output-contract.md` 固定 `源/` 口径 | 执行报告的 primary source 是 `源/` 或用户显式路径 |
| 原资料已有集数划分却被重切 | 边界裁决层 | 回到显式集标，按原资料边界落盘 | 在 workflow 中先检测 `第N集` / `Episode N` / `第N话` 等显式标记 | 每个输出文件能回指原集标 |
| 把 story 的 `第N章` 当成 AIGC 原生 `第N集`，机械一章一集 | 集标判定层 | 将 `第N章`、chapter、卷/章/节降级为 P2 候选边界，重新按 2500-3000 字目标窗和戏剧断点裁决 | 在 `SKILL.md`、`input-output-contract.md`、workflow、type map、review gate 与审计脚本同步排除章/集误映射 | 只有 `第N集` / `Episode N` / `EP N` / 明确连载语义的 `第N话` 能触发 P1；章节源进入 P2/P3 |
| 没有集数划分时切分过短或过长 | 默认策略层 | 回到 2500-3000 字目标窗，并用自然段/章节小节修正 | 把偏离理由写进执行报告 | 大多数集数字数落在目标窗或有明确边界理由 |
| 分集阶段改写了小说正文 | 真源保真层 | 恢复原文，只保留最小标题/frontmatter | 固定“只切分不改写”门禁 | 抽样 diff 可证明正文未被润色、扩写或剧本化 |
| 多文件源顺序错乱 | 输入排序层 | 按文件名数字、章节标题、正文内序号建立稳定顺序 | 执行报告记录排序依据 | 输入清单顺序可复查 |
| 旧流程模块与 `SKILL.md` 同时维护流程节点 | 节点真源漂移层 | 删除旧流程节点展开，把节点、Mermaid、gate 和返工入口收回 `SKILL.md` | 模块只能在 `Module Loading Matrix` 中被授权展开，不得另立节点网络 | 全仓扫描无残留执行引用 |
| 缺少可复现评估 prompt | 评估资产层 | 新增 `test-prompts.json` 覆盖 source_scan、explicit split、chaptered split、repair/review | 优化或达尔文评分时先跑 dry-run prompt 清单 | 至少 3 条 prompt 且无 TODO |

## Repair Playbook

1. 先锁定用户是否指定了小说原文路径；指定路径优先。
2. 若未指定路径，绑定项目并读取 `projects/aigc/<项目名>/源/`。
3. 扫描显式集标；只要原资料已有可靠集数划分，就不启用 2500-3000 字重切。
4. 若只发现 `第N章`、chapter、卷/章/节或 story 章节文件名，判定为“没有原生集标”，先按章节/小节/自然段建候选边界，再用 2500-3000 字目标窗微调。
5. 写回前核对编号连续、覆盖完整、正文未改写。
6. 执行报告只记录裁决证据和返工入口，不写长篇思维流水。
7. 如果发现模块、模板或审查合同指向旧流程模块，优先改回 `SKILL.md#T*` 主节点，而不是恢复平行节点文件。

## Reusable Heuristics

- “自带集数划分”优先于所有字数策略；字数策略只在原资料没有集标时启用。
- Story 章节编号不是 AIGC 集数编号；不要因为输入有 `第1章` 到 `第20章` 就直接生成 `第1集` 到 `第20集`。
- 2500-3000 字是目标窗，不是机械截断点；自然段闭合、章节小高潮、悬念点比精确字数更重要。
- 项目 `源/` 是小说正文默认真源；项目 `CONTEXT/` 适合补设定、偏好和禁区，但不能替代正文。
- 分集文件最好保持朴素：标题、可选来源 frontmatter、原文正文即可；复杂改编说明应写入执行报告。
- runtime-spine 优化时，`SKILL.md` 必须能独立跑完最小路径；`references/` 和 `review/` 只能提供细则与 gate 展开。
