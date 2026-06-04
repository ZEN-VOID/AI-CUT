# Character Design Workflow

本文件定义 `角色/2-设计` 的思行一体化流程。执行时先判断、再行动、再留证据。

## Topology

混合拓扑：项目上下文串行锁定，初始化综合只作为冻结上下文消费，角色主体由主 agent 汇流并进入本地 review。

```mermaid
flowchart TD
    A["N1-INTAKE<br/>scope + boundaries"] --> B["N2-PROJECT-CONTEXT<br/>style + team context"]
    B --> C["N3-CHARACTER-LIST<br/>source character anchors"]
    C --> D["N4-TYPE-PROFILE<br/>type profile"]
    D --> R["N5-RESEARCH-PROFILE<br/>research profile"]
    R --> E{"N6-INIT-SYNTHESIS-REVIEW<br/>frozen synthesis + local review"}
    E --> F["Research Evidence Patch"]
    E --> G["Story Patch"]
    E --> H["Visual Costume Patch"]
    E --> I["Cinematography Patch"]
    F --> J["N7-MERGE-DRAFT<br/>canonical draft"]
    G --> J
    H --> J
    I --> J
    J --> K["N8-REVIEW-GATE<br/>review gate"]
    K --> L{"Pass?"}
    L -->|"yes"| M["N9-WRITE-OUTPUT<br/>write output"]
    L -->|"no"| J
```

## Thinking-Action Nodes

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、角色范围和不动范围 | 用户请求、项目路径 | 解析项目名、角色名、批量范围和只读边界 | `execution_scope` | `N2-PROJECT-CONTEXT` | 项目路径明确 |
| `N2-PROJECT-CONTEXT` | 加载项目风格和初始化综合上下文 | `MEMORY.md`、`CONTEXT/`、`3-美学/画面基调/全局风格协议.md`、`3-美学/角色风格/角色风格协议.md`、`north_star.yaml`、`team.yaml.init_synthesis` | 抽取 `画面基调.Global Style Prompt + 角色风格.Character Style Prompt`、设计相关初始化约束、启发、风险和禁区；`north_star.yaml` 只提供项目北极星/不变量/禁区 | `project_design_context` | `N3-CHARACTER-LIST` | 缺失项已记录 |
| `N3-CHARACTER-LIST` | 锁定清单角色锚点 | `角色清单.md` | 读取待设计角色的名称、首次登场、原文描述关键词 | `character_intake_table` | `N4-TYPE-PROFILE` | 每个角色来自清单 |
| `N4-TYPE-PROFILE` | 判定角色类型和设计深度 | 清单行、项目上下文 | 应用 `types/character-design-type-map.md`，决定研究深度、考据许可、不确定性口径、`aesthetic_priority` 和 `celebrity_inspiration_policy` | `type_profile` | `N5-RESEARCH-PROFILE` | 类型、深度、审美优先级和风险明确 |
| `N5-RESEARCH-PROFILE` | 把研究转化为设计证据链 | `character_intake_table`、`project_design_context`、`type_profile`、必要外部来源、`knowledge-base/character-design-corpus.md` | LLM 生成身份、职业、阶层、地域年代、服饰工艺、身体姿态、审美吸引力、禁区、不确定性和 prompt evidence chain；命中审美强化、妆容化或服装时代语境时加载语料库并形成 `corpus_usage_trace`；搜索只作辅助证据 | `research_profile`、`corpus_usage_trace` | `N6-INIT-SYNTHESIS-REVIEW` | 每个研究镜头和审美吸引力都有设计转化；语料已原创转译且不脱离时代语境 |
| `N6-INIT-SYNTHESIS-REVIEW` | 消费初始化综合并准备本地 review | `team.yaml.init_synthesis.stage_seed_summary."11-主体"`、`init_handoff.design_seed`、`north_star.yaml.创作阶段不变量.设计`、`type_profile`、`research_profile`、`references/workflow-supervision-contract.md` | 只读提取与当前角色设计有关的设计约束、启发和风险，压缩为 `init_team_synthesis_context`；本地 review 仅记录研究证据、物语、视觉服装、摄影 patch 和风险，不从 team 派生成员人格或问答 | `workflow_supervision_record`、`init_synthesis_node_coverage`、`init_team_synthesis_context` | `N7-MERGE-DRAFT` | 不静默跳过可用初始化综合；supervision 记录非空；无 team 身份调用、旧 stage profile 或伪顾问问答 |
| `N7-MERGE-DRAFT` | 生成单一 canonical 设计稿 | 各 patch、模板、`references/design-output-contract.md`、`corpus_usage_trace` | LLM 汇流并写完整设计稿，不保留互相竞争的并列稿；`## 4. 解构` 下方必须写 `主体ID号：<主体ID>`，英文 prompt 必须以同一主体 ID 号开头，整合 `## 4. 解构` 全部有效信息，覆盖审美吸引力、脸部/骨相策略、妆容化和服装吸引力，使用自然语言负向约束且不含 `--no`，prompt 短语必须可回指 evidence chain 与 `deconstruction_coverage` | `character_design_draft` | `N8-REVIEW-GATE` | 字段齐全，审美吸引力、语料库原创转译和输出合同硬规则已逐条满足 |
| `N8-REVIEW-GATE` | 审查字段、风格、研究证据链、审美吸引力、语料库触发、prompt 和 LLM-first | draft、review 合同、`references/design-slot-review-contract.md`、`references/workflow-supervision-contract.md` | 检查清单锚点、项目风格、研究镜头、审美吸引力、语料库触发与服装时代语境、解构主体 ID、解构字段、prompt 长度、脚本边界；解析 `ROLE-BUNDLE-01` 并记录缺槽或通过结论 | `review_result`、`slot_bundle_review` | `N9-WRITE-OUTPUT` 或 `N7-MERGE-DRAFT` | 无阻断 finding，slot bundle 无缺槽 |
| `N9-WRITE-OUTPUT` | 落盘 canonical markdown | 通过审查的设计稿 | 写入 `11-主体/角色/2-设计/<主体ID>-<角色名>.md`，必要时写报告 | output files | done | 文件路径和主体 ID 前缀正确 |

## Research Profile Evidence Gate

`N5-RESEARCH-PROFILE` 必须产出以下最小证据表，供后续 `N7-MERGE-DRAFT` 消费：

| evidence_slot | minimum content | must feed |
| --- | --- | --- |
| `identity` | 身份标签、身份冲突、与清单锚点的关系 | `Identity & Story Pressure`、prompt 主体 |
| `occupation_class` | 职业/劳动/权力位置、阶层痕迹、资源边界 | 身体姿态、服装材质、配饰克制 |
| `region_era` | 地域、年代、气候、制度或审美限制 | 发型、廓形、色彩、禁用元素 |
| `costume_craft` | 剪裁、面料、闭合方式、层次、磨损与使用逻辑 | `Detailed Costume Design`、prompt 服装短语 |
| `body_posture` | 身高比例、重心、手部位置、职业肌肉记忆 | `Detailed Character Design / Body`、`Cinematography` |
| `aesthetic_appeal` | 美丽/英俊目标、脸部骨相、妆发、身形、服装吸引力、主角强化、正反派个性魅力、明星脸原创转译边界 | `Visual Drivers`、`Detailed Character Design / Face`、`Detailed Costume Design`、prompt 审美短语 |
| `corpus_usage_trace` | 语料库触发原因、使用的角色类型/妆容/服装时代语境模块、原创转译说明、禁用逐字套用说明 | `Aesthetic Appeal Evidence`、`Visual Drivers`、`Detailed Costume Design`、`Review Gate` |
| `taboo_constraints` | 项目禁区、文化误读、安全风险、固定画面禁区 | guardrails、negative prompt 判断 |
| `uncertainty` | 清单事实、LLM 推演、待确认项和置信度 | `Uncertainty Notes`、执行报告风险 |
| `prompt_evidence_chain` | `subject ID prefix -> evidence -> design decision -> prompt phrase` | `## 4. 解构` 下的主体 ID、英文 prompt 的主体 ID 开头和关键短语 |
| `workflow_supervision_record` | 执行模式、阻断层级、初始化综合来源、本地 reviewer/checklist 路径、`init_synthesis_node_coverage` | `N8-REVIEW-GATE` 的 reviewer 汇流和最终报告 |
| `slot_bundle_review` | `ROLE-BUNDLE-01` 的 required slots 是否存在、来源和缺槽 finding | `review_result` 和返工入口 |

## Failure Routes

| fail_code | symptom | rework_entry |
| --- | --- | --- |
| `FAIL-NO-LIST` | 找不到上游 `角色清单.md` | 回到 `N3-CHARACTER-LIST`，请求或生成上游清单 |
| `FAIL-NO-STYLE` | 未读取 `3-美学/画面基调/全局风格协议.md`、`3-美学/角色风格/角色风格协议.md` 或无法提炼 `Global Style Prompt + Character Style Prompt` | 回到 `N2-PROJECT-CONTEXT` |
| `FAIL-RESEARCH-FLAT` | 研究层只有资料摘录，没有转化为设计决策 | 回到 `N5-RESEARCH-PROFILE` 补 evidence chain |
| `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | 角色设计只还原清单关键词，缺少美丽/英俊/个性魅力、服装审美完成度，或明星脸灵感写成现实人物复刻 | 回到 `N7-MERGE-DRAFT` 补 `Aesthetic Appeal Evidence`、脸部骨相策略、服装吸引力策略和原创转译说明 |
| `FAIL-CHAR-DESIGN-CORPUS-MISSING` | 命中审美强化、妆容化、角色类型语料或服装时代语境时，未加载语料库、未留 `corpus_usage_trace`，或语料逐字套用/服装脱离时代 | 回到 `N5-RESEARCH-PROFILE` 加载 `knowledge-base/character-design-corpus.md`，再到 `N7-MERGE-DRAFT` 原创转译 |
| `FAIL-UNCERTAINTY-HIDDEN` | 低证据推演被写成事实 | 回到 `N5-RESEARCH-PROFILE` 标注来源、置信度和待确认项 |
| `FAIL-INIT-SYNTHESIS-SKIPPED` | 初始化综合存在但被静默跳过，或误触发 team 身份 / 旧 stage profile / 伪顾问问答 | 回到 `N6-INIT-SYNTHESIS-REVIEW` 并补 `init_team_synthesis_context` 或缺失记录 |
| `FAIL-SLOT-BUNDLE-MISSING` | 未解析 `ROLE-BUNDLE-01` 或 slot bundle findings 为空白 | 回到 `N8-REVIEW-GATE`，按 `design-slot-review-contract.md` 补齐槽位验收 |
| `FAIL-PROMPT-LONG` | 英文提示词超过 1300 characters | 回到 `N7-MERGE-DRAFT` 压缩 prompt |
| `FAIL-PROMPT-SHALLOW-INTEGRATION` | 英文提示词只拼接前缀后缀，未整合解构全部有效信息，或使用 `--no` | 回到 `N7-MERGE-DRAFT` 重写 prompt 并补 `deconstruction_coverage` |
| `FAIL-SCRIPT-AUTHORSHIP` | 脚本生成创作正文 | 停用脚本输出，回到 LLM 汇流 |
