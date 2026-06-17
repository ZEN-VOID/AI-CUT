# Prop Design Review Contract

本文件定义 `道具/2-设计` 的质量门禁、reviewer provider 接入和本地 checklist 口径。

## Default Provider

- 默认 worker：`Worker-Prop`
- 初始化上下文消费按 `../../../_shared/team-advisor-consultation-contract.md` 执行：只读消费项目 `MEMORY.md` 中的 `project_memory_init_context`、团队配置与协作偏好、资料吸收摘要和阶段上下文读取指南，再进入单道具设计汇流；不得在本阶段解析监制 roster、请教顾问、调用 team 身份或补造顾问问答。
- 默认 reviewer：独立 prop-design reviewer provider；若无专名，则使用可用的 `code-reviewer` / design reviewer provider 执行结构与语义门禁。
- 默认 review 必须同时读取 `references/design-output-contract.md`、`references/design-slot-review-contract.md` 与 `references/workflow-supervision-contract.md`；`PROP-BUNDLE-01` 必须被解析为非空 slot bundle 记录。
- 若当前运行环境不使用外部 reviewer，直接使用本地 review checklist。

## Review Scope

| dimension | checks |
| --- | --- |
| source | 是否回指 `1-清单/道具清单.md` 的单个清单项 |
| context | 是否读取并消费 `2-美学` 输出、项目记忆和相关上下文 |
| authorship | 研究、物语、解构和 prompt 是否为 LLM-first，而非脚本拼接 |
| research_chain | 研究是否转译为形制、材料、工艺、年代、使用/保存状态、功能逻辑、风险/不确定性和 prompt evidence token |
| design_detail_culture | 道具是否有可见设计价值；是否具备独特轮廓、材质记忆点、工艺/结构细节、条件性文化/身份/功能符号、使用/保存状态和功能结构；关键道具是否有 signature detail，而不是简单和平凡；是否避免无证据旧化、随机贴文化符号或强加装饰 |
| corpus_usage | 触发道具审美、文化/身份符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语时，是否加载 `knowledge-base/prop-design-corpus.md`，并完成符合时代语境的原创转译 |
| structure | 必填章节是否齐全，`## 4. 解构` 下方是否先写 `主体ID号：<主体ID>`，`Photography` 与 `Prop Design` 是否分离 |
| output_naming | 文件名是否为 `<主体ID>-<安全文件名>.md`，且文件名前缀与解构主体 ID、提示词设计主体 ID、英文 prompt 前缀一致 |
| prompt | 英文 prompt 是否以主体 ID 号开头，包含 `画面基调.Global Style Prompt + 道具风格.Prop Style Prompt`，且 1300 characters 内；prompt 前缀是否与解构主体 ID、提示词设计主体 ID 完全一致；整合对象是否为 `## 4. 解构` 全部有效信息而不是前后缀拼接 |
| design_output_contract | 是否逐条检查 `references/design-output-contract.md` 的结构硬规则、prompt 整合硬规则、字符数、自然语言负向约束和 `--no` 禁用 |
| slot_bundle_review | 是否按 `references/design-slot-review-contract.md` 解析 `PROP-BUNDLE-01`，并对 `required_slots` 逐项给出证据位置或缺槽 finding |
| prompt_evidence | 核心 prompt token 是否能回指研究、物语或解构字段，并包含 `deconstruction_coverage` 说明解构槽位如何进入、合并或被剔除 |
| fixed_visual | 是否为纯色背景单道具完整全貌展示、45 度视角、完整展示道具全貌、完整轮廓和主要结构、仅展示道具、无局部特写/裁切特写/半截道具、无人物、无背景元素、无场景环境 |
| project_memory_init_context | 是否按项目 `MEMORY.md` 形成 `project_memory_init_context`；采纳内容是否绑定当前思维·执行节点；是否禁止 team 身份调用、旧 stage profile 和伪顾问问答 |
| workflow_supervision | 是否按 `references/workflow-supervision-contract.md` 记录外部 provider 或本地 checklist 路径、本地 reviewer checklist 和汇流裁决 |
| type | `type_profile` 是否合理，冷门考据和多状态是否按类型处理 |
| scope | 是否只写入 `3-主体/道具/2-设计`，未触碰 registry、父级或其他技能 |

## Review Gates

| gate_id | dimension | fail_code | blocking_when | rework_target | report_evidence |
| --- | --- | --- | --- | --- | --- |
| `GATE-PROP-DESIGN-01` | source | `FAIL-PROP-DESIGN-01` | 缺少 `1-清单/道具清单.md` 来源，或目标道具无法回指单个清单项的名称、首次登场、原文描述 | `N2-UPSTREAM` / `N3-SCOPE` | `upstream_manifest`、清单行号、缺失字段或降级说明 |
| `GATE-PROP-DESIGN-02` | source / scope | `FAIL-PROP-DESIGN-02` | 设计稿混入多个道具主体、新增清单外主体，或把上游冲突静默裁决为新 canonical 真源 | `N3-SCOPE` | `prop_worklist`、单主体边界说明、上游修复建议 |
| `GATE-PROP-DESIGN-02A` | scope | `FAIL-PROP-DESIGN-02A` | 增量补缺时覆盖既有设计稿、为未调度主体补占位，或未记录 alias merge / design gap 状态 | `N3-SCOPE` / `N8-WRITE` | `design_manifest_delta`、跳过/覆盖许可、alias merge 记录 |
| `GATE-PROP-DESIGN-03` | structure | `FAIL-PROP-DESIGN-03` | 必填章节缺失，`## 4. 解构` 下方未先写 `主体ID号：<主体ID>`，或 `Photography` / `Prop Design` 未拆分 | `N6-DESIGN` | 模板块覆盖检查、解构标题证据、缺块 finding |
| `GATE-PROP-DESIGN-04` | context | `FAIL-PROP-DESIGN-04` | 未读取或未实际消费 `2-美学/类型风格.md`、`2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/道具风格/道具风格协议.md`、项目 `MEMORY.md`、主题禁区或设计相关初始化上下文 | `N2-UPSTREAM` / `N5-RESEARCH-CHAIN` | `project_design_context`、project memory source、已消费字段、episode override / fallback 与缺口说明 |
| `GATE-PROP-DESIGN-05` | authorship | `FAIL-SCRIPT-AUTHORSHIP` | 研究考据、物语、解构、道具风格或英文 prompt 由脚本、模板拼接或启发式补句生成 | `N6-DESIGN` | 脚本职责清单、LLM 主创声明、正文生成来源说明 |
| `GATE-PROP-DESIGN-06` | prompt / output_naming | `FAIL-PROP-DESIGN-05` | 英文 prompt 未以同一主体 ID 开头、未引用 `画面基调.Global Style Prompt + 道具风格.Prop Style Prompt`、超过 1300 characters、使用 `--no`，或未整合 `## 4. 解构` 全部有效信息 | `N6-DESIGN` | prompt 字符数、三处主体 ID 对照、解构槽位覆盖、自然语言负向约束检查 |
| `GATE-PROP-DESIGN-07` | scope / output_naming | `FAIL-PROP-DESIGN-06` | 输出路径不在 `3-主体/道具/2-设计/`，文件名缺主体 ID 前缀，或触碰父级、`1-清单`、`3-生成`、registry 或其他技能目录 | `N8-WRITE` | 输出路径、文件名前缀、改动文件清单、越界项排除说明 |
| `GATE-PROP-DESIGN-08` | fixed_visual | `FAIL-PROP-DESIGN-07` | `Photography` 或 prompt 未固定纯色背景 45 度单道具完整全貌展示、完整展示道具全貌、完整轮廓和主要结构、仅展示道具，或写成局部特写、裁切特写、半截道具，或出现人物、手、桌面、房间、街景、背景元素 | `N6-DESIGN` | fixed visual phrase 检查、禁用元素清单、prompt 约束位置 |
| `GATE-PROP-DESIGN-09` | research_chain | `FAIL-PROP-DESIGN-08` | 研究停留在百科、气氛词或未验证断言，未转译为形制、材料、工艺、年代、使用/保存状态、功能逻辑、风险/不确定性 | `N5-RESEARCH-CHAIN` | research evidence chain、`visual translation`、`risk_uncertainty`、状态证据 |
| `GATE-PROP-DESIGN-10` | prompt_evidence | `FAIL-PROP-DESIGN-09` | prompt 核心 token 无法回指研究、物语或解构字段，或缺少 `deconstruction_coverage` 说明槽位整合/合并/剔除 | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `prompt_evidence_chain`、`deconstruction_coverage`、缺槽 finding |
| `GATE-PROP-DESIGN-11` | project_memory_init_context | `FAIL-PROP-DESIGN-10` | 项目记忆初始化上下文存在但未形成 `project_memory_init_context`，或采纳内容没有绑定当前 `node_id / pass_id / gate_id` 并转成节点级判断、取舍、patch 或风险提示，或误触发 team 身份 / 旧 stage profile / 伪顾问问答 | `N5-RESEARCH-CHAIN` / `N7-REVIEW` | `project_memory_init_context`、`init_synthesis_node_coverage`、缺失原因 |
| `GATE-PROP-DESIGN-12` | design_output_contract | `FAIL-PROP-DESIGN-TEMPLATE-REGISTRY` | 未使用 canonical structured template 登记的结构真源，或组根模板/脚本替代 leaf LLM 正文创作 | `N6-DESIGN` | 模板路径、渲染来源、脚本机械边界说明 |
| `GATE-PROP-DESIGN-13` | design_detail_culture | `FAIL-PROP-DESIGN-DETAIL-CULTURE` | 道具只是普通功能物、缺少审美设计、条件性文化/身份/功能符号或克制设计理由、工艺/结构细节、signature detail、材质记忆点、使用/保存状态或时代语境，导致画面平凡无辨识度；或无证据添加文化贴花、装饰纹样、划痕、污渍、包浆、锈蚀、破损、折旧感 | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `design_detail_culture_evidence`、`Design Appeal Target`、`Signature Detail`、`Cultural Element Strategy or Minimal Function-Led Rationale`、`Condition State Policy`、prompt token |
| `GATE-PROP-DESIGN-14` | corpus_usage | `FAIL-PROP-DESIGN-CORPUS-MISSING` | 已进入单道具设计、批量设计、增量补缺或修复，且涉及审美、文化/身份符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语，但未加载 `knowledge-base/prop-design-corpus.md` 或未说明原创转译、适用性判断与时代语境约束 | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `prop_corpus_usage_trace`、语料种子、原创转译说明、period/culture guardrail、符号/装饰适用性、旧化 token 依据 |
| `GATE-PROP-DESIGN-SLOT-01` | slot_bundle_review | `FAIL-PROP-DESIGN-SLOT-01` | 未解析非空 `PROP-BUNDLE-01`，或 required slots 缺少证据位置且未形成 blocking finding | `N7-REVIEW` | `slot_bundle_review`、required slot evidence map、缺槽 finding |
| `GATE-PROP-DESIGN-WORKFLOW-01` | workflow_supervision | `FAIL-PROP-DESIGN-WORKFLOW` | `workflow_supervision` 缺 subject、blocking layer、init synthesis source、本地 reviewer/checklist、slot findings 或 merge decision | `N7-REVIEW` | `workflow_supervision` packet、local checklist、unlaunched reviewers |
| `GATE-PROP-DESIGN-WORKFLOW-02` | workflow_supervision | `FAIL-PROP-DESIGN-MERGE-DECISION` | reviewer / checklist / slot bundle findings 未由主 agent 汇流裁决，或留下互相竞争的并列稿 | `N7-REVIEW` / `N6-DESIGN` | `merge_decision`、采纳/拒绝 patch 记录、最终单稿声明 |
| `GATE-PROP-DESIGN-RESEARCH-SAFETY` | research_chain | `FAIL-PROP-DESIGN-RESEARCH-SAFETY` | 冷门网络信息、危险物、医疗器械、武器或违法用途研究被写成确定事实、操作步骤或可执行伤害/制造说明 | `N5-RESEARCH-CHAIN` | 搜索必要性、来源姿态、不确定性/安全转译记录 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为单道具细目设计交付 |
| `pass_with_followups` | 可交付，但有非阻断后续项 |
| `needs_rework` | 有阻断问题，必须返工后再交付 |
| `blocked` | 缺失关键输入、权限或上层策略阻断 |

## Review Flow Map

```mermaid
flowchart TD
    A["design draft"] --> B["source / context / authorship 检查"]
    B --> C["structure / prompt / fixed_visual 检查"]
    C --> A1["检查 project memory init context packet"]
    A1 --> A2["检查输出合同、PROP-BUNDLE-01 与 supervision 记录"]
    A2 --> D{"外部 reviewer provider 可用?"}
    D -->|"yes"| E["独立 reviewer verdict"]
    D -->|"local checklist"| F["本地 checklist 结果"]
    E --> G{"verdict"}
    F --> G
    G -->|"pass / pass_with_followups"| H["允许写入 canonical 文件"]
    G -->|"needs_rework"| I["回到 N5-RESEARCH-CHAIN / N6-DESIGN 修复"]
    G -->|"blocked"| J["停止并报告缺口"]
```

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: source | context | authorship | research_chain | design_detail_culture | corpus_usage | structure | output_naming | prompt | design_output_contract | slot_bundle_review | prompt_evidence | fixed_visual | init_team_synthesis | workflow_supervision | type | scope
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Checklist

- [ ] 文件名为 `<主体ID>-<安全文件名>.md`，对应单个道具主体，未混入总稿。
- [ ] `名称 / 首次登场 / 原文描述复述` 与上游清单一致。
- [ ] 研究考据服务可见设计；冷门信息有来源说明或不确定性注记。
- [ ] 研究证据链覆盖形制、材料、工艺、年代、使用/保存状态、功能逻辑、风险/不确定性中的必要项。
- [ ] 道具有可见设计价值，包含独特轮廓、材质记忆点、工艺/结构细节、条件性文化/身份/功能符号或克制设计理由、使用/保存状态和功能结构，不是简单功能还原或平凡物件。
- [ ] 磨损、污渍、包浆、锈蚀、破损、折旧感等旧化 token 均有上游证据、功能逻辑、年代逻辑或项目风格依据；新物、洁净物、封存物、展陈物、高维护物或高科技物没有被强行做旧。
- [ ] 文化元素、身份符号、纹样、铭文、徽记、器型、封缄、材质和装饰只在有证据、有语境或有功能必要时出现，并符合项目时代、地域、阶层、职业、宗教/族群禁区与功能逻辑，没有错置现代奢侈品、街头潮牌、战术风、赛博朋克、哥特奇幻等元素。
- [ ] 触发审美、文化/身份符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语时，已加载 `knowledge-base/prop-design-corpus.md`，并在 `Prop Corpus Usage Trace` 中说明原创转译和适用性判断。
- [ ] 研究结论区分确定事实、推断、灵感转译和未知项，没有把不确定信息写成确定史实。
- [ ] 物语没有扩写成新剧情真源。
- [ ] `Photography` 描述拍摄可见语言，`Prop Design` 描述物件造型语言。
- [ ] `## 4. 解构` 下方存在 `主体ID号：<主体ID>`，且与 `## 5. 提示词设计` 的主体 ID 号、英文 prompt 开头完全一致。
- [ ] 文件名前缀与 `## 4. 解构` 主体 ID、`## 5. 提示词设计` 主体 ID、英文 prompt 前缀完全一致。
- [ ] `Photography` 固定为完整全貌展示、45 度视角、完整展示道具全貌、完整轮廓和主要结构、仅展示道具、纯色背景、无局部特写/裁切特写/半截道具、无人物、无背景元素、无场景环境。
- [ ] 英文 prompt 不超过 1300 characters。
- [ ] 英文 prompt 以主体 ID 号开头，格式为 `<主体ID>: ...`。
- [ ] prompt 引用 `画面基调.Global Style Prompt + 道具风格.Prop Style Prompt`。
- [ ] prompt evidence chain 覆盖核心 token：主体名、形制、材料、工艺/年代、使用/保存状态、功能逻辑、`deconstruction_coverage` 和固定画面约束。
- [ ] 英文 prompt 整合 `## 4. 解构` 的全部有效 Photography + Prop Design 信息，而不是只拼接主体 ID、风格、物品、固定画面或负向词。
- [ ] 英文 prompt 使用自然语言负向约束，未使用 Midjourney `--no` 参数。
- [ ] prompt 明确包含 full-view prop shot、45-degree view、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、solid color background、no people、no background elements、no scene environment。
- [ ] 已逐条消费 `references/design-output-contract.md`。
- [ ] 已解析 `PROP-BUNDLE-01`，且 required slots 均有证据位置或 blocking finding。
- [ ] 已按 `references/workflow-supervision-contract.md` 记录 provider/local checklist/merge。
- [ ] 项目记忆初始化上下文存在时，`project_memory_init_context` 已从 `MEMORY.md` 中提炼出节点级可执行指导、局部 patch 或风险提示；缺失时已记录 `not_applicable` / `blocked`。
- [ ] 输出路径在 `projects/aigc/<项目名>/3-主体/道具/2-设计/`。

## Gate Rule

不得在以下情况宣布完成：

- 缺少上游清单来源。
- 缺少必填章节任一项。
- `## 4. 解构` 下方缺少 `主体ID号：<主体ID>`，或该 ID 与 `## 5. 提示词设计` 主体 ID / 英文 prompt 前缀不一致。
- 输出文件名缺少主体 ID 前缀，或文件名前缀与 `## 4. 解构` 主体 ID、`## 5. 提示词设计` 主体 ID、英文 prompt 前缀不一致。
- 研究没有转译为形制、材料、工艺、年代、使用/保存状态、功能逻辑或不确定性处理。
- 道具只是简单和平凡的功能物，缺少审美吸引力、设计细节、条件性文化/身份/功能符号或克制设计理由、signature detail 或时代语境。
- 触发道具审美、文化/身份符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语时，未加载 `knowledge-base/prop-design-corpus.md`，或只是照搬语料而未完成原创转译和适用性判断。
- 无上游证据、功能逻辑、年代逻辑或项目风格依据，却把道具写成划痕、污渍、包浆、锈蚀、破损、折旧或“有旧损感”。
- prompt 核心 token 与研究/物语/解构字段脱节，或缺少 `deconstruction_coverage`。
- prompt 非英文、未以主体 ID 号开头、超长、使用 `--no` 参数、没有 `画面基调.Global Style Prompt + 道具风格.Prop Style Prompt`，或只拼接前后缀而未整合 `## 4. 解构` 全部有效信息。
- 未逐条消费 `references/design-output-contract.md`，或输出结构/prompt 整合硬规则只停留在旁路文档。
- 未解析 `PROP-BUNDLE-01`，或 required slot 缺少证据位置且未形成 blocking finding。
- `references/workflow-supervision-contract.md` 要求的 provider/local checklist/merge 记录为空。
- 摄影字段或 prompt 把道具置入具体场景、桌面环境、室内陈设、街景、人物手持情境或背景元素。
- 缺少 full-view prop shot、45-degree view、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、solid color background、no people、no background elements 或 no scene environment 约束，或把画面写成局部特写、裁切特写、半截道具。
- 项目记忆初始化上下文存在时，缺少 `project_memory_init_context`，或采纳内容没有绑定当前 `node_id / pass_id / gate_id`，或误触发 team 身份、旧 stage profile、伪顾问问答。
- 脚本替代 LLM 生成核心创作正文。
- 输出越过本技能授权范围。
