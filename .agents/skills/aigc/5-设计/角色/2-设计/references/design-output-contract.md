# 角色设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/5-设计/角色/2-设计/templates/character_masterprompt.structured.v2.md`

角色设计正文由 LLM 在 `2-设计` leaf 中完成；组根模板只登记结构真源，脚本仅做机械投影和校验。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该 ID 必须与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Identity & Story Pressure、Visual Drivers、Detailed Character Design、Detailed Costume Design 与 Cinematography 信息；只追加主体 ID、全局风格、服装风格、定妆照词或负向词，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。英文 prompt 必须控制在 1300 characters 内，使用自然语言负向约束，不得使用 Midjourney `--no` 参数。
