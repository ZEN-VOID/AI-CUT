# Review Contract

本文件定义 `角色/2-设计` 的质量门禁、初始化综合消费、本地 review 汇流审查和验收输出。

## Default Reviewer Path

- 默认使用初始化综合消费 + 本地 reviewers。
- 初始化综合消费按 `../../../_shared/team-advisor-consultation-contract.md` 执行：只读消费项目 `team.yaml.init_synthesis.stage_seed_summary."6-设计"`、`init_handoff.design_seed` 或 `north_star.yaml.创作阶段不变量.设计`，形成 `init_team_synthesis_context` 后再进入设计稿汇流；不得在本阶段解析监制 roster、请教顾问、调用 team 身份或补造顾问问答。
- 默认 review 必须同时读取 `references/design-output-contract.md`、`references/design-slot-review-contract.md` 与 `references/workflow-supervision-contract.md`；`ROLE-BUNDLE-01` 必须被解析为非空 slot bundle 记录。
- 推荐 reviewer：`character-research-reviewer`、`visual-costume-reviewer`、`cinematography-reviewer`、`prompt-length-reviewer`。
- 若当前环境无外部 reviewer provider，主 agent 直接采用本地顺序 checklist；不得把本地 checklist 说成外部并行执行，也不得用本地 checklist 冒充 team 顾问问答。

## Review Dimensions

| dimension | checks |
| --- | --- |
| upstream_anchor | 角色名称、首次登场、原文描述复述是否来自 `角色清单.md` |
| project_context | 是否读取并体现 `north_star.yaml` 和 `team.yaml.init_synthesis` 的相关设计上下文 |
| research_layer | 研究是否转化为身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性和 prompt evidence chain |
| llm_first | 研究、物语、解构和提示词是否由 LLM 直接完成，脚本未替代主创 |
| required_sections | 是否包含研究考据、物语、解构、提示词设计 |
| decomposition | `## 4. 解构` 下方是否先写 `主体ID号：<主体ID>`；五个解构字段是否齐全且内容不互相串位 |
| output_naming | 文件名是否为 `<主体ID>-<角色名>.md`，且文件名前缀与解构主体 ID、提示词设计主体 ID、英文 prompt 前缀一致 |
| costume | 服装是否含廓形、材质、色彩、配件、使用痕迹或功能逻辑 |
| cinematography | 是否固定为纯色背景全身定妆照，而非剧情场景或环境肖像 |
| prompt | 英文、以主体 ID 号开头、融合全局风格和服装风格、不超过 1300 characters，且该前缀与解构主体 ID、提示词设计主体 ID 完全一致；整合对象是 `## 4. 解构` 全部有效信息，不是前后缀拼接；关键短语可回指 prompt evidence chain 与 `deconstruction_coverage` |
| design_output_contract | 是否逐条检查 `references/design-output-contract.md` 的结构硬规则、prompt 整合硬规则、字符数、自然语言负向约束和 `--no` 禁用 |
| slot_bundle_review | 是否按 `references/design-slot-review-contract.md` 解析 `ROLE-BUNDLE-01`，并对 `required_slots` 逐项给出证据位置或缺槽 finding |
| fixed_visual | 是否包含 full-body costume fitting photo、solid color background、no scene environment |
| init_team_synthesis | 是否按 `team.yaml.init_synthesis.stage_seed_summary."6-设计"`、`init_handoff.design_seed` 或 `north_star.yaml.创作阶段不变量.设计` 形成 `init_team_synthesis_context`；采纳内容是否绑定当前思维·执行节点；是否禁止 team 身份调用、旧 stage profile 和伪顾问问答 |
| 本地 review | 本地 reviewer / checklist 记录是否完整；是否按 `references/workflow-supervision-contract.md` 留下 supervision 记录 |
| scope | 是否未修改父级、registry、上游清单或其他 worker 范围 |

## Review Gates

| gate_id | dimension | fail_code | blocking_when | rework_target | report_evidence |
| --- | --- | --- | --- | --- | --- |
| `GATE-CHAR-DESIGN-01` | upstream_anchor | `FAIL-NO-LIST` | 找不到 `角色清单.md`，或待设计主体无法回指 `名称 / 首次登场 / 原文描述（关键词式）` | `N3-CHARACTER-LIST` | `character_intake_table`、清单行号或缺失说明 |
| `GATE-CHAR-DESIGN-02` | scope | `FAIL-CHAR-DESIGN-UPSTREAM-SCOPE` | 设计阶段新增清单外主体、直接修改上游清单，或把同名冲突/漏项静默裁决为 canonical 设计稿 | `N1-INTAKE` / `N3-CHARACTER-LIST` | `execution_scope`、上游修复建议、未改动上游声明 |
| `GATE-CHAR-DESIGN-03` | project_context | `FAIL-NO-STYLE` | 未读取 `north_star.yaml`，虚构全局风格，或未记录字段命名漂移与临时工作口径 | `N2-PROJECT-CONTEXT` | `project_design_context`、已消费字段清单、缺失字段说明 |
| `GATE-CHAR-DESIGN-04` | project_context | `FAIL-CHAR-DESIGN-ADVISOR-CONTEXT` | `team.yaml.init_synthesis` 相关设计种子未选择性消费，或把初始化综合写成人名堆砌/文风模仿 | `N2-PROJECT-CONTEXT` / `N6-INIT-SYNTHESIS-REVIEW` | 设计相关 init synthesis source、冲突裁决依据、被剔除无关内容说明 |
| `GATE-CHAR-DESIGN-05` | llm_first | `FAIL-SCRIPT-AUTHORSHIP` | 脚本生成研究、物语、解构、服装、摄影或英文 prompt 正文 | `N7-MERGE-DRAFT` | 脚本职责清单、LLM 汇流声明、正文生成来源说明 |
| `GATE-CHAR-DESIGN-06` | research_layer | `FAIL-RESEARCH-FLAT` | 研究层缺少任一必需 lens，或资料未转化为外观、服装、姿态、摄影和 prompt 决策 | `N5-RESEARCH-PROFILE` | `research_profile`、`design implication`、八镜头覆盖表 |
| `GATE-CHAR-DESIGN-07` | research_layer | `FAIL-UNCERTAINTY-HIDDEN` | 低证据推演、外部搜索线索或待确认信息被写成清单事实 | `N5-RESEARCH-PROFILE` | `Uncertainty Notes`、来源/置信度标注、待确认项 |
| `GATE-CHAR-DESIGN-08` | prompt | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | prompt 关键主体、服装、姿态、光线、风格或固定画面短语无法回指 `evidence -> design decision -> prompt phrase` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage` |
| `GATE-CHAR-DESIGN-09` | research_layer | `FAIL-CHAR-DESIGN-WEB-EVIDENCE` | 未经许可或无必要地使用网络搜索，长段复制外部资料，或让外部资料覆盖清单、north star、用户禁区 | `N5-RESEARCH-PROFILE` | 搜索许可/必要性说明、来源摘要、使用边界 |
| `GATE-CHAR-DESIGN-10` | required_sections | `FAIL-CHAR-DESIGN-SECTIONS` | 设计稿缺少清单锚点、研究考据、物语、解构或提示词设计任一必填块 | `N7-MERGE-DRAFT` | 模板块覆盖检查、缺块 finding |
| `GATE-CHAR-DESIGN-11` | decomposition | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` | `## 4. 解构` 下缺 `主体ID号`，或文件名、解构 ID、提示词主体 ID、英文 prompt 前缀不一致 | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | 四处主体 ID 对照表 |
| `GATE-CHAR-DESIGN-12` | prompt | `FAIL-PROMPT-SHALLOW-INTEGRATION` | 英文 prompt 未整合 `## 4. 解构` 全部有效信息，超过 1300 characters，包含中文解释/多版本堆叠或使用 `--no` | `N7-MERGE-DRAFT` | prompt 字符数、`deconstruction_coverage`、自然语言负向约束检查 |
| `GATE-CHAR-DESIGN-13` | fixed_visual | `FAIL-CHAR-DESIGN-FIXED-VISUAL` | 摄影字段或 prompt 把角色放进剧情场景、建筑、街景、室内陈设、自然环境、复杂背景、半身头像或环境肖像 | `N7-MERGE-DRAFT` | fixed visual phrase 检查、禁用环境元素清单 |
| `GATE-CHAR-DESIGN-14` | design_output_contract | `FAIL-CHAR-DESIGN-TEMPLATE-REGISTRY` | 未使用 canonical structured template，或脚本/组根模板替代 leaf LLM 正文创作 | `N7-MERGE-DRAFT` | 模板路径、渲染来源、脚本机械边界说明 |
| `GATE-CHAR-DESIGN-15` | slot_bundle_review | `FAIL-SLOT-BUNDLE-MISSING` | 未解析 `ROLE-BUNDLE-01`，`slot_bundles` 为空，或 required slots 没有证据位置/缺槽 finding | `N8-REVIEW-GATE` | `slot_bundle_review`、required slot evidence map、blocking findings |
| `GATE-CHAR-DESIGN-16` | 本地 review | `FAIL-CHAR-DESIGN-SUPERVISION-PACKET` | `workflow_supervision` 缺 subject、blocking layer、init synthesis source、本地 reviewer/checklist 或 merge decision | `N6-INIT-SYNTHESIS-REVIEW` | `workflow_supervision_record` 完整字段 |
| `GATE-CHAR-DESIGN-17` | init_team_synthesis | `FAIL-INIT-SYNTHESIS-SKIPPED` | 初始化综合存在但被静默跳过，或 `init_team_synthesis_context` / `init_synthesis_node_coverage` 未绑定当前 `node_id / pass_id / gate_id`，或误触发 team 身份 / 旧 stage profile / 伪顾问问答 | `N6-INIT-SYNTHESIS-REVIEW` | `init_synthesis_node_coverage`、缺失原因、本地 checklist 结果 |
| `GATE-CHAR-DESIGN-18` | 本地 review | `FAIL-CHAR-DESIGN-MERGE-DECISION` | reviewer / checklist / slot bundle findings 未被主 agent 汇流裁决，或保留互相竞争的并列稿 | `N8-REVIEW-GATE` / `N7-MERGE-DRAFT` | `merge_decision`、采纳/拒绝 patch 记录、最终单稿声明 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为角色细目设计稿交付 |
| `pass_with_followups` | 可交付，但存在非阻断改进项 |
| `needs_rework` | 字段、风格、prompt 或锚点存在阻断问题 |
| `blocked` | 缺少上游清单、项目初始化上下文或被上层策略阻断 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: upstream_anchor | project_context | research_layer | llm_first | required_sections | decomposition | output_naming | costume | cinematography | prompt | design_output_contract | slot_bundle_review | fixed_visual | init_team_synthesis | local_review | scope
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Research Layer Gate

研究层需逐项通过以下审查：

| gate_id | blocking_when_missing | reviewer_question |
| --- | --- | --- |
| `RESEARCH-IDENTITY` | high | 身份和故事压力是否来自清单/项目上下文，并转化为外观或姿态？ |
| `RESEARCH-OCCUPATION-CLASS` | high | 职业、阶层和资源痕迹是否转化为身体、面料、磨损、配饰或行动功能？ |
| `RESEARCH-REGION-ERA` | medium/high | 地域年代是否明确，特定文化/制度信息是否避免误写？ |
| `RESEARCH-COSTUME-CRAFT` | high | 服装是否写到剪裁、面料、层次、闭合方式、工艺或使用痕迹？ |
| `RESEARCH-BODY-POSTURE` | high | 身体姿态是否可用于纯色背景全身定妆照，而非剧情场景动作？ |
| `RESEARCH-TABOO` | critical | 项目禁区、安全风险、文化误读和固定画面禁区是否已写入 guardrails？ |
| `RESEARCH-UNCERTAINTY` | high | 低证据推演是否标明置信度和待确认项？ |
| `RESEARCH-PROMPT-CHAIN` | high | prompt 中的关键短语是否能回指 `evidence -> design decision -> prompt phrase`？ |

## Review Flow Map

```mermaid
flowchart TD
    A["待审查角色设计稿"] --> B["检查上游清单锚点"]
    B --> C["检查 north_star.yaml / team.yaml 消费"]
    C --> R["检查研究层八镜头与 prompt evidence chain"]
    R --> D["检查 LLM-first 与脚本边界"]
    D --> E["检查文件名前缀、解构主体 ID 与五个解构字段"]
    E --> F["检查服装细节与摄影字段"]
    F --> G["检查英文 prompt 长度和固定画面约束"]
    G --> H["检查 init team synthesis 与本地 review 记录"]
    H --> H1["检查输出合同、ROLE-BUNDLE-01 与 supervision 记录"]
    H1 --> I{"阻断 finding?"}
    I -->|"yes"| J["needs_rework / blocked"]
    I -->|"no"| K{"存在非阻断改进?"}
    K -->|"yes"| L["pass_with_followups"]
    K -->|"no"| M["pass"]
```

## Gate Rule

不得宣布完成：

- 任一设计稿缺少模板必填块。
- 英文提示词超过 1300 characters。
- 英文提示词没有以主体 ID 号开头。
- 英文提示词只拼接主体 ID、风格、服装或负向词等前缀后缀，未整合 `## 4. 解构` 的全部有效身份、外观、服装、姿态和摄影信息。
- 英文提示词使用 Midjourney `--no` 参数，而不是自然语言负向约束。
- `## 4. 解构` 下方缺少 `主体ID号：<主体ID>`，或该 ID 与 `## 5. 提示词设计` 主体 ID / 英文 prompt 前缀不一致。
- 输出文件名缺少主体 ID 前缀，或文件名前缀与 `## 4. 解构` 主体 ID、`## 5. 提示词设计` 主体 ID、英文 prompt 前缀不一致。
- 摄影字段或英文提示词把角色放进具体场景、建筑空间、街景、室内陈设或复杂环境。
- 缺少全身定妆照、纯色背景或 no scene environment 约束。
- 研究层缺少身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性或 prompt evidence chain 任一关键镜头。
- 研究内容无法说明如何转化为角色外观、服装、姿态、摄影或 prompt。
- prompt 关键短语无法回指研究证据、项目风格、`deconstruction_coverage` 或固定画面合同。
- 未逐条消费 `references/design-output-contract.md`，或输出结构/prompt 整合硬规则只停留在旁路文档。
- 未解析 `ROLE-BUNDLE-01`，或 required slot 缺少证据位置且未形成 blocking finding。
- `references/workflow-supervision-contract.md` 要求的 provider/local checklist/merge 记录为空。
- 初始化综合存在时，缺少 `init_team_synthesis_context`，或采纳内容没有绑定当前 `node_id / pass_id / gate_id`，或误触发 team 身份、旧 stage profile、伪顾问问答。
- 未消费 `north_star.yaml` 和 `team.yaml.init_synthesis` 却声称项目风格对齐。
- 脚本生成了创作正文。
- 初始化综合存在却被跳过。
- 任务改动越过 `.agents/skills/aigc/6-设计/角色/2-设计/**` 或项目输出路径。
