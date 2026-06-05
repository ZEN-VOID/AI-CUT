# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/8-多端交付生成/doc` 的经验层知识库，不是第二份 DOC 交付合同。
- 调用 `.agents/skills/lesson/8-多端交付生成/doc/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > 父包 `SKILL.md` > 本叶子 `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-doc-delivery-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| DOC 叶子重新决定三端交付范围 | parent packet 缺失 | 回到父包生成 doc leaf packet | DOC 叶子只消费父包 packet | `packet_inventory` 指向父包 manifest |
| 讲义正文像模板套句 | LLM-first 违规 | 废弃机械产物，回到 `N4-LLM-DOC-ADAPTATION` | 脚本只做 Word 组装和导出 | authorship note 可追踪 |
| Word 文档结构只有文件名 | architecture 缺口 | 回到 `N3-DOC-ARCHITECTURE` 补章节、读者和变体 | 文档结构先于组装 manifest | plan 包含目录和章节策略 |
| `.docx` 组装覆盖了未授权章节 | update scope 漂移 | 只改受影响章节并更新 manifest diff | 正式写回前记录 overwrite note | output paths 和 changed sections 一致 |
| DOC 与 PPT/HTML 术语不一致 | cross-channel consistency 缺口 | 回到父包 delivery map 或本叶子 gate | 术语和目标以父包 map 为真源 | consistency section 无冲突 |

## Repair Playbook

1. 先确认任务确实是 DOC/Word、讲义、手册或文档交付。
2. 缺父包 packet 时回到 `$lesson-delivery`，不要在 DOC 叶子补父包 manifest。
3. 文档读者不清时先定学员手册、讲师手册还是参考手册。
4. 所有 `.docx` 组装都必须从 LLM-approved 文档内容和 manifest 出发。
5. 修订既有文档时只改受影响章节，并同步 `doc-assembly-manifest.json`。

## Reusable Heuristics

- DOC 的优势是完整性、可检索性和课后复习，不应复制 PPT 的短句节奏。
- 学员手册优先清晰和练习步骤；讲师手册优先授课提示、时间控制和答疑提醒。
- Word 样式、页眉页脚、目录和导出设置属于机械组装，不属于课程正文主创。
- 文档引用和资料来源要保留边界，不能把弱证据写成权威结论。
- 如果 DOC 与父包 map 冲突，优先修 DOC 叶子，不改父包事实。

## Case Log

### Case-001

- milestone_type: doc_leaf_creation
- outcome: 建立 DOC/Word 交付叶子的 Skill 2.0 runtime spine。
- design_decision: DOC 叶子拥有文档结构、doc delivery plan、assembly manifest 和可选 DOCX 组装目标。
- replication_checklist: 父包 packet -> 文档结构 -> LLM 适配 -> assembly manifest -> consistency gate。
- evidence_paths: `.agents/skills/lesson/8-多端交付生成/doc/SKILL.md`
