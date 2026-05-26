# Book And Long-Context Learning Contract

本文件定义 `$aigc-learn` 面对书籍、超长 PDF、长篇文档、课程讲义合集、长网页合集和其他超长上下文材料时的学习细则。它扩展 `source-ingestion-contract.md`，只拥有长上下文分层读取、证据锚点、覆盖度控制和可迁移知识抽取规则，不直接决定技能写回 owner。

## Scope

适用对象：

- 书籍、电子书、PDF、docx、扫描 OCR 文档、长篇研究报告、课程讲义合集、长网页合集、用户提供的超长文本。
- 用户要求“学习这本书”“吸收这套资料”“把长书的方法补进 AIGC 技能树”“从超长上下文中提炼工作流”的任务。

不适用对象：

- 短摘录或单篇短文：优先使用 `types/text-source/text-source.md`，必要时只建立局部锚点。
- 需要事实更新的在线资料：同时加载 `types/web-source/web-source.md`，并按 `conflict-verification-contract.md` 核查。

## Long-Context Principle

书籍和超长文档不得一次性“读完即总结”。必须采用分层学习：

1. `catalog_digest`：目录、章节结构、作者意图、核心主题、版本/出版信息、版权边界。
2. `relevance_map`：把章节或段落簇映射到本轮学习目标和潜在 AIGC owning skill。
3. `sampling_plan`：选择必读章节、抽样章节、可跳过章节，并说明理由。
4. `deep_reading_notes`：对高相关章节建立页码、章节、标题或段落锚点。
5. `cross_chapter_synthesis`：合并跨章节重复模式、矛盾、递进关系和适用边界。
6. `skill_transfer_units`：转化为流程节点、门禁、类型策略、审查维度、失败模式或经验层 heuristic。

## Evidence Anchors

长上下文学习必须保留可回指锚点：

| source form | anchor requirement |
| --- | --- |
| 有页码书籍 / PDF | 页码、章节、标题、段落范围或图表编号 |
| 无页码电子书 | 章节、标题、小节、位置编号或用户提供片段编号 |
| OCR / 扫描文档 | 页图编号、OCR 片段编号、置信度和不可读区域 |
| 长网页合集 | URL、标题、抓取时间、页面段落或 heading 锚点 |
| 用户粘贴长文本 | 用户消息编号、段落序号、标题或自建 chunk id |

不得把受版权保护材料的长段原文写入技能包；只允许短锚点、概括、方法抽象和必要的极短引用。

## Chunking Strategy

| stage | action | gate |
| --- | --- | --- |
| `structure_pass` | 读取目录、前言/导言、章节标题、结语、索引或摘要 | 能说明材料整体结构 |
| `target_pass` | 根据学习目标选择相关章节簇 | 能说明为何读这些、不读那些 |
| `evidence_pass` | 对相关章节建立可回指 evidence_units | 每条关键结论至少有一个锚点 |
| `synthesis_pass` | 跨章节合并方法、限制、冲突和递进关系 | 不是章节摘要堆叠 |
| `transfer_pass` | 映射到 target_skill_map、gap_matrix、landing_set | 可落到最窄 owner 或明确 blocker |

## Coverage Rules

- 全书学习必须先交付 `catalog_digest` 和 `relevance_map`，不得只凭随机章节生成全局结论。
- 当上下文过长无法一次处理，必须分批推进，并维护 `coverage_ledger`：已读范围、未读范围、跳过理由、待复核点。
- 高相关章节要深读；低相关章节可摘要或跳过，但跳过理由必须与学习目标相关。
- 对理论书、方法书和案例书，优先抽取可迁移判断框架；对作品类书籍，优先抽象叙事、结构、风格和审美原则，不复制具体表达。
- 若书中方法与 AIGC 现有合同冲突，不能以“书里这么说”为由直接覆盖，必须走冲突核查和 owner 裁决。

## Output Additions

书籍 / 超长上下文学习对象的学习证据必须补充：

| field | requirement |
| --- | --- |
| `catalog_digest` | 结构、版本、作者/来源、主题和许可边界 |
| `relevance_map` | 章节或 chunk 到学习目标 / owning skill 的映射 |
| `sampling_plan` | 深读、略读、跳过范围及理由 |
| `coverage_ledger` | 已覆盖、未覆盖、不可读和待复核范围 |
| `evidence_units` | 页码、章节、标题、段落或 chunk 锚点 |
| `cross_chapter_synthesis` | 跨章节归纳，不是逐章摘要堆叠 |

> **注意**：以上是执行型改进的学习证据，不是报告。完成任务的标准是：`audit_result: pass` + `changed_files` 已验证。

## Review Gate

不得通过书籍 / 超长上下文学习审计，若出现以下情况：

- 没有 `catalog_digest` 就声称掌握全书。
- 没有 `coverage_ledger` 就从局部阅读推出全局结论。
- 关键学习结论缺少页码、章节、标题或 chunk 锚点。
- 把章节摘要当作技能改进，未形成 `target_skill_map`、`gap_matrix` 和 `landing_set`。
- 复制受版权保护长段正文或把书中单一观点无核查地提升为强制规则。
