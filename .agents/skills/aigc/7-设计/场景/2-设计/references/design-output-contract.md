# 场景设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/7-设计/场景/2-设计/templates/scene_masterprompt.structured.v2.md`

场景设计正文由 LLM 在 `2-设计` leaf 中完成；叶子模板只登记结构真源，脚本仅做机械投影和校验。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该 ID 必须与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息；只追加主体 ID、风格、时间地域、pure empty shot / no people 等前缀或后缀，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。
