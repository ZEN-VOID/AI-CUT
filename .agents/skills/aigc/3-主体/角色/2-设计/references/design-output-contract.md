# 角色设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/3-主体/角色/2-设计/templates/character_masterprompt.structured.v2.md`

角色设计正文由 LLM 在 `2-设计` leaf 中完成；组根模板只登记结构真源，脚本仅做格式检查、字符计数和校验，不得批量生成、批量插入、正则套句或映射投影创作正文。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该 ID 必须与 `## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Identity & Story Pressure、Visual Drivers、Detailed Character Design、Detailed Costume Design 与 Cinematography 信息；其中必须覆盖审美吸引力、`Charisma Floor`、脸部/骨相策略、服装吸引力策略和固定画面约束。只追加主体 ID、画面基调、角色风格、定妆照词或负向词，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。英文 prompt 必须控制在 1300 characters 内，使用自然语言负向约束，不得使用 Midjourney `--no` 参数。

来源匹配审美硬规则：角色设计不得只做清单关键词还原。审美路线必须匹配清单证据、年龄、性别/性别表达、身份、物种/族群、项目调性和角色权重；美丽、英俊、清癯、粗粝、威严、危险、阴郁、病态、怪诞、质朴或平凡但可识别都可以成立。主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 必须具备 `charisma_floor=high` 的可见镜头魅力证据，不能只写“可识别”；普通正派、普通反派、配角和功能角色必须有个性化魅力或清晰可识别度。该魅力下限不等于默认美化、帅化、成人化或性化。真实人物灵感默认不用或泛化处理，只有用户/项目允许且有必要时才可作为原创转译参考，不得精确复刻、换脸、同款肖像或让角色可识别为现实本人。

语料库触发硬规则：命中审美强化、妆容化、角色类型词库、服装时代语境或 prompt 审美短语时，必须加载 `knowledge-base/character-design-corpus.md` 并留下 `corpus_usage_trace`。语料只能原创转译，不能逐字套用成模板脸或模板服装；服装风格化必须回到项目时代、地域、阶层和职业母体。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 输出结构是否以 `.agents/skills/aigc/3-主体/角色/2-设计/templates/character_masterprompt.structured.v2.md` 为 canonical structured template，而不是由组根模板或脚本生成角色设计正文？ | `GATE-CHAR-DESIGN-14` | `FAIL-CHAR-DESIGN-TEMPLATE-REGISTRY` | `N7-MERGE-DRAFT` | 模板路径、渲染来源、脚本机械边界说明 |
| `## 4. 解构` 标题下方是否先写 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID 字段、英文 prompt 前缀完全一致？ | `GATE-CHAR-DESIGN-11` | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | 四处主体 ID 对照表、文件名前缀检查 |
| 英文 prompt 是否整合 `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design` 与 `Cinematography` 全部有效信息，覆盖审美吸引力、`Charisma Floor`、脸部/骨相策略和服装吸引力，而不是只追加主体 ID、画面基调、角色风格、定妆照词或负向词？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 与解构槽位对照、`deconstruction_coverage` |
| 被压缩、合并或剔除的解构槽位是否在 `prompt_evidence_chain.deconstruction_coverage` 中说明？ | `GATE-CHAR-DESIGN-08` | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage` 缺口记录 |
| 英文 prompt 是否不超过 1300 characters，使用自然语言负向约束，且没有 Midjourney `--no` 参数？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 字符数、负向约束文本、`--no` 检查 |
| 角色容貌、妆发、骨相、身形和服装是否具备来源匹配的审美吸引力；主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 是否具备 `charisma_floor=high` 的可见镜头魅力证据；真实人物灵感是否获允许并原创转译而非现实人物复刻？ | `GATE-CHAR-DESIGN-19` | `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | `N7-MERGE-DRAFT` | `aesthetic_appeal_evidence`、来源匹配审美目标、`Charisma Floor`、脸部骨相策略、服装吸引力策略、真实人物灵感原创转译说明 |
| 命中审美强化、妆容化、角色类型词库、服装时代语境或 prompt 审美短语时，是否加载 `knowledge-base/character-design-corpus.md` 并留下原创转译证据？ | `GATE-CHAR-DESIGN-20` | `FAIL-CHAR-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `corpus_usage_trace`、选用 lens、服装时代语境、剔除语料说明 |
