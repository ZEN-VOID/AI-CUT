# 场景设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/7-设计/场景/2-设计/templates/scene_masterprompt.structured.v2.md`

场景设计正文由 LLM 在 `2-设计` leaf 中完成；叶子模板只登记结构真源，脚本仅做机械投影和校验。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该 ID 必须与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息；只追加主体 ID、风格、时间地域、pure empty shot / no people 等前缀或后缀，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否使用 `.agents/skills/aigc/7-设计/场景/2-设计/templates/scene_masterprompt.structured.v2.md` 作为结构真源，而不是另起字段顺序、临时模板或脚本生成正文？ | `GATE-SCENE-DESIGN-05` | `FAIL-SCENE-DESIGN-05` | `N6-DESIGN` | 记录采用的 canonical template、输出 section 顺序、任何字段偏离及其修复位置。 |
| `## 4. 解构` 标题下方是否第一时间写入 `主体ID号：<主体ID>`，且该 ID 与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致？ | `GATE-SCENE-DESIGN-05` | `FAIL-SCENE-DESIGN-05` | `N6-DESIGN` | 留下解构主体 ID、提示词主体 ID、英文 prompt 开头三处比对证据。 |
| `## 4. 解构` 是否保留 `Scene Design` 与 `Cinematography` 两组有效信息，并把空间结构、尺度、材质、色彩、陈设、动线、镜头距离、构图、光线、焦段、景深和氛围节奏作为 prompt 整合候选？ | `GATE-SCENE-DESIGN-06` | `FAIL-SCENE-DESIGN-06` | `N6-DESIGN` | 报告列出解构槽位覆盖清单、被合并槽位和被剔除槽位。 |
| 最终英文整合 prompt 是否真正吸收 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息，而不是只追加主体 ID、全局风格、时间地域、pure empty shot / no people 等前缀或后缀？ | `GATE-SCENE-DESIGN-06` | `FAIL-SCENE-DESIGN-06` | `N6-DESIGN` | 提供 prompt 字符数、prompt token 到解构槽位的覆盖摘要，以及未覆盖项的 blocking finding。 |
| 被压缩、合并或剔除的解构槽位是否写入 `prompt_evidence_chain.deconstruction_coverage`，并说明它们为何进入、合并或被舍弃？ | `GATE-SCENE-DESIGN-10` | `FAIL-SCENE-DESIGN-10` | `N6-DESIGN` | 留下 `deconstruction_coverage` 条目、关键 token 证据链和缺证据 token 清单。 |
| 场景设计正文、研究判断、解构和英文 prompt 是否由 LLM 直接完成，脚本只做模板登记、机械投影、字符计数或校验？ | `GATE-SCENE-DESIGN-07` | `FAIL-SCENE-DESIGN-07` | `N6-DESIGN` | 报告注明脚本只承担机械辅助；若发现脚本主创正文，记录直接原因与回收范围。 |
