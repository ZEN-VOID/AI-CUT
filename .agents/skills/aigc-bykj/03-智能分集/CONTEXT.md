# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/03-智能分集` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-28

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `03` 直接读取小说源或 `projects/aigc/<项目名>/源/` | BYKJ 上游真源层 | 回到 `output/[项目名]/02-剧本处理/`，锁定 `manifest.json`、`剧本处理稿.json` 或 `episodes/` | `SKILL.md` 固定 `02` 输出为默认输入 | 执行报告的 input_root 指向 `02-剧本处理` |
| 输出写回旧 `projects/aigc/<项目名>/1-分集/` | BYKJ 路由层 | 移回 `output/[项目名]/03-智能分集/` | 父级与阶段合同都固定 BYKJ output 路径 | manifest 中 output_root 正确 |
| `02` 已有 episodes 却被按字数重切 | 上游集标保护层 | 恢复上游集号和边界，只做索引、coverage 和 handoff | `PASS-03-04` 阻断忽略 P1 上游集标 | 输出集号能回指 `02/episodes/第N集.json` |
| 把 `第N章` 当成 `第N集` | 集标判定层 | 把章节降级为 P2 候选，重新按场景完整性和断点裁决 | `SKILL.md` 固定章节不是 P1 集标 | 报告有 `excluded_marker_map` |
| 在场景、对白或动作链中间断集 | 剧本场景完整性层 | 回到 `N3C-BOUNDARY-SOLVE`，选择场景闭合点或冲突遗产点 | `FAIL-03-SCENE-INTEGRITY` 阻断硬切 | 每集边界落在场景/动作闭合处 |
| 分集过程中改写 `02` 剧本正文 | 剧本保真层 | 恢复上游字段、对白、场景顺序，只允许新增 frontmatter、简表和 handoff | `FAIL-03-FIDELITY` 阻断改写 | 抽样回指 `02` 正文一致 |
| 分集总表可读但下游无法消费 | 交接层 | 补每集主要角色、场景、道具、情绪/视觉钩子和风险 | `FAIL-03-HANDOFF` 固定 handoff evidence | `04/05/06` 能按集号读取 |

## Repair Playbook

1. 先确认输入是否是 `02-剧本处理` 输出；不是则先路由或阻断。
2. 若 `02/episodes/` 已存在，优先沿用上游集号，不做二次重切。
3. 若只有 `剧本处理稿.json`，先扫描 P1 集标，再把章节、场景、冲突遗产和尾钩作为候选边界。
4. 划分边界时先保场景和对白完整，再考虑 2500-3000 字目标窗。
5. 写回前核对 `coverage_map`：无遗漏、无重复、每段上游正文只归属一集。
6. 报告只记录裁决证据、思考过程和返工入口，不写长篇过程流水。

## Reusable Heuristics

- `03-智能分集` 的关键变化是输入对象变了：它切的是 `02` 的处理后剧本，不是小说原文。
- 上游已经分好 episodes 时，智能分集的价值在校验、总表、handoff 和 manifest，而不是强行再聪明一次。
- 无显式集标时，剧本场景完整性比精确字数更重要；硬切场景会直接破坏下游分镜和资产提取。
- 章节标题来自原小说结构，通常只能帮助定位来源范围，不能直接决定 AIGC 集号。
- 每集文件既要保留正文，又要给下游阶段足够索引；正文保真和 handoff 增强必须分层，不能把新说明混入剧本正文。
- BYKJ 阶段输出目录优先于原 AIGC runtime；本阶段只产出 `output/[项目名]/03-智能分集/`。
