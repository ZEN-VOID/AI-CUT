# 角色设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/7-设计/角色/2-设计/templates/character_masterprompt.structured.v2.md`

角色设计正文由 LLM 在 `2-设计` leaf 中完成；组根模板只登记结构真源，脚本仅做机械投影和校验。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该 ID 必须与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Identity & Story Pressure、Visual Drivers、Detailed Character Design、Detailed Costume Design 与 Cinematography 信息；只追加主体 ID、全局风格、服装风格、定妆照词或负向词，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。英文 prompt 必须控制在 1300 characters 内，使用自然语言负向约束，不得使用 Midjourney `--no` 参数。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 输出结构是否以 `.agents/skills/aigc/7-设计/角色/2-设计/templates/character_masterprompt.structured.v2.md` 为 canonical structured template，而不是由组根模板或脚本生成角色设计正文？ | `GATE-CHAR-DESIGN-14` | `FAIL-CHAR-DESIGN-TEMPLATE-REGISTRY` | `N7-MERGE-DRAFT` | 模板路径、渲染来源、脚本机械边界说明 |
| `## 4. 解构` 标题下方是否先写 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID 字段、英文 prompt 前缀完全一致？ | `GATE-CHAR-DESIGN-11` | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | 四处主体 ID 对照表、文件名前缀检查 |
| 英文 prompt 是否整合 `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design` 与 `Cinematography` 全部有效信息，而不是只追加主体 ID、全局风格、服装风格、定妆照词或负向词？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 与解构槽位对照、`deconstruction_coverage` |
| 被压缩、合并或剔除的解构槽位是否在 `prompt_evidence_chain.deconstruction_coverage` 中说明？ | `GATE-CHAR-DESIGN-08` | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage` 缺口记录 |
| 英文 prompt 是否不超过 1300 characters，使用自然语言负向约束，且没有 Midjourney `--no` 参数？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 字符数、负向约束文本、`--no` 检查 |
