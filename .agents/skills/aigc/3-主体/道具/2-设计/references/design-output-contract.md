# 道具设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/3-主体/道具/2-设计/templates/prop_masterprompt.structured.v2.md`

道具设计正文由 LLM 在 `2-设计` leaf 中完成；组根模板只登记结构真源，脚本仅做格式检查、字符计数和校验，不得批量生成、批量插入、正则套句或映射投影创作正文。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该 ID 必须与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Photography 与 Prop Design 信息；只追加主体 ID、画面基调、道具风格、固定画面词或负向词，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。英文 prompt 必须控制在 1300 characters 内，使用自然语言负向约束，不得使用 Midjourney `--no` 参数。

设计吸引力硬规则：道具必须有可见设计价值和可生成细节；每个道具至少要形成独特轮廓、材质记忆点、工艺/结构细节、条件性文化/身份/功能符号、使用/保存状态和功能结构中的有效组合，关键道具必须有 `signature detail`。道具不得只是简单和平凡的功能还原。文化元素、身份符号、机构标识、纹样、铭文、徽记和装饰只在有证据、有语境或有功能必要时写入；普通功能、极简、洁净/无菌、高科技或工业道具可以用比例、材质精度、结构逻辑、维护状态和表面处理形成设计价值。使用/保存状态必须按证据选择，`wear_trace` 只是条件子类；不得为了“设计感”强行为所有道具添加划痕、污渍、包浆、锈蚀、破损或折旧感。

语料库硬规则：单道具设计、批量设计、增量补缺或修复中，只要涉及审美、文化/身份/功能符号适用性、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语，就必须加载 `knowledge-base/prop-design-corpus.md`，并在 `Prop Corpus Usage Trace` 中记录语料种子、原创转译、时代/文化 guardrail、条件适用性或克制设计理由与 prompt 证据；不得照搬语料、加入脱离项目时代语境的装饰或默认旧化。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 输出结构是否以 `.agents/skills/aigc/3-主体/道具/2-设计/templates/prop_masterprompt.structured.v2.md` 为 canonical structured template，而不是由组根模板或脚本生成道具设计正文？ | `GATE-PROP-DESIGN-12` | `FAIL-PROP-DESIGN-TEMPLATE-REGISTRY` | `N6-DESIGN` | 模板路径、渲染来源、脚本机械边界说明 |
| `## 4. 解构` 标题下方是否先写 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID 字段、英文 prompt 前缀完全一致？ | `GATE-PROP-DESIGN-03` / `GATE-PROP-DESIGN-06` | `FAIL-PROP-DESIGN-03` / `FAIL-PROP-DESIGN-05` | `N6-DESIGN` | 解构标题、提示词主体 ID、英文 prompt 前缀三处对照 |
| 英文 prompt 是否整合 `## 4. 解构` 中全部有效 `Photography` 与 `Prop Design` 信息，而不是只追加主体 ID、画面基调、道具风格、固定画面词或负向词？ | `GATE-PROP-DESIGN-06` | `FAIL-PROP-DESIGN-05` | `N6-DESIGN` | prompt 与 Photography / Prop Design 槽位对照、解构槽位覆盖记录 |
| `Prop Design` 是否包含设计吸引力、signature detail、文化/身份/功能符号策略或克制设计理由、工艺/结构细节、使用/保存状态和时代语境 guardrail，且道具不是普通平凡的功能物，也没有无证据旧化或无证据贴花？ | `GATE-PROP-DESIGN-13` | `FAIL-PROP-DESIGN-DETAIL-CULTURE` | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `Design Appeal Target`、`Signature Detail`、`Cultural / Identity / Functional Symbol Strategy or Minimal Function-Led Rationale`、`Craft / Structure Detail`、`Condition State Policy`、prompt token |
| 触发审美、文化/身份/功能符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语时，是否加载 `knowledge-base/prop-design-corpus.md` 并写出 `Prop Corpus Usage Trace`？ | `GATE-PROP-DESIGN-14` | `FAIL-PROP-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `Prop Corpus Usage Trace`、语料种子、原创转译说明、period/culture guardrail、条件适用性或克制设计理由、旧化 token 依据 |
| 被压缩、合并或剔除的解构槽位是否写入 `prompt_evidence_chain.deconstruction_coverage`，并说明进入、合并或剔除理由？ | `GATE-PROP-DESIGN-10` | `FAIL-PROP-DESIGN-09` | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `prompt_evidence_chain`、`deconstruction_coverage`、缺槽 finding |
| 英文 prompt 是否控制在 1300 characters 内，使用自然语言负向约束，且没有 Midjourney `--no` 参数？ | `GATE-PROP-DESIGN-06` | `FAIL-PROP-DESIGN-05` | `N6-DESIGN` | prompt 字符数、自然语言负向约束文本、`--no` 检查 |
