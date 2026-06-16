# Source And Merge Contract

## Upstream Source

- 唯一 canonical 上游是 `projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `subjects.characters`。
- 候选角色只从 registry 条目的 `id`、`canonical_name`、`aliases`、`first_appearance`、`source_anchors` 和 `style_refs` 进入清单候选池。
- `1-分集` 故事源和 `2-美学/角色风格` 协议只作为 source anchor 与风格证据回查，用于解释 registry 中的别名、代称、身份称呼或含糊项。
- 已有 `8-分组` 稿只允许作为后置命名对齐证据；不得直接从 `8-分组`、`7-摄影`、剧情梗概、场景清单、道具清单或外部设定创建角色清单条目。

## Evidence Rules

| evidence_type | allowed_use | forbidden_use |
| --- | --- | --- |
| registry `subjects.characters` | 创建候选角色、记录 canonical name / alias、定位首次登场 | 自动扩写角色设定 |
| source anchors / 故事源 | 解释候选角色身份、代称回指、合并证据 | 绕过 registry 新增候选 |
| 项目 `MEMORY.md` | 应用已确认命名偏好、禁区、长期别名规则 | 推翻上游明确事实 |
| 项目 `CONTEXT/` | 复核已有角色映射和人工设定 | 替代本轮 registry 证据 |

## Merge Rules

1. 同名或明确别名默认归并为一个 canonical 角色。
2. 姓名、身份称呼、亲属称呼、职务称呼、代称之间的归并必须有 source anchor 或项目上下文证据。
3. 群体角色只有在下游需要作为设计主体时才纳入；普通背景人群记录到执行报告风险区。
4. 低置信度归并不得强行落入清单；应在执行报告中列出待确认项。
5. `名称` 单元承载别名，例如 `林晓（别名：班长、她）`；清单主体不新增 `别名` 列。

## Description Rules

- `原文描述（关键词式）` 使用分号或顿号分隔关键词。
- 关键词来源优先级：registry 原词 > source anchor 中用于辨认身份的短语 > 项目已确认别名规则。
- 禁止加入外貌设计、服装设计、性格分析、后续剧情推断或提示词。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个最终角色主体是否都来自 `projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `subjects.characters` 条目，而不是 `8-分组`、`7-摄影`、剧情梗概、场景/道具清单或外部设定？ | `GATE-CHAR-LIST-01` | `FAIL-CHAR-LIST-01` | `N2-REGISTRY-SCAN` | `candidate_evidence_table` 列出 registry `id`、`canonical_name`、`source_anchors`；执行报告列明删除或驳回的非 canonical 来源主体。 |
| source anchor / 故事源是否只用于解释 registry 中的别名、代称、身份称呼或含糊项，没有绕过 registry 新增候选角色？ | `GATE-CHAR-LIST-02` | `FAIL-CHAR-LIST-02` | `N3-EVIDENCE-LOOKUP` | `identity_evidence` 标明正文摘记对应的 registry 候选；报告说明补证用途和被拒绝的正文新增项。 |
| 项目 `MEMORY.md` 与项目 `CONTEXT/` 是否只应用已确认命名偏好、长期别名规则或既有映射，没有推翻本轮 registry 明确事实？ | `GATE-CHAR-LIST-02` | `FAIL-CHAR-LIST-02` | `N3-EVIDENCE-LOOKUP` | 执行报告记录项目记忆/上下文命中项、适用角色和未采纳原因；冲突项进入待确认风险。 |
| 同名或明确别名是否默认归并为同一 canonical 角色，并在 `名称` 单元保留必要别名？ | `GATE-CHAR-LIST-04` | `FAIL-CHAR-LIST-03` | `N4-MERGE` | `canonical_role_map` 记录 `observed_names -> canonical_name`、别名来源组和最终 `名称` 写法。 |
| 姓名、身份称呼、亲属称呼、职务称呼、代称之间的归并是否都有 source anchor 或项目上下文证据，而不是因称谓相似、职业相同或代词性别相同就硬合并？ | `GATE-CHAR-LIST-03` | `FAIL-CHAR-LIST-03` | `types/character-identity-type-map.md` / `N4-MERGE` | `identity_type_profile` 标注 `ID-NAME`、`ID-ALIAS`、`ID-ROLE-TITLE`、`ID-RELATION`、`ID-PRONOUN` 等类型；报告列出归并依据和被拆分的误并候选。 |
| 群体角色是否只有在下游需要作为设计主体时才纳入；普通背景人群是否进入执行报告风险区或不纳入说明？ | `GATE-CHAR-LIST-05` | `FAIL-CHAR-LIST-09` | `N7-REVIEW` | `group_character` 风险项列出 registry 原值、涉及 source anchor、纳入/不纳入理由和待确认问题。 |
| 低置信度归并是否没有强行落入清单，而是在执行报告中列出待确认项？ | `GATE-CHAR-LIST-05` | `FAIL-CHAR-LIST-09` | `N7-REVIEW` | `review_result` 或 `执行报告.md` 包含低置信候选、证据不足点、建议人工确认口径和暂不强归并处理。 |
| `名称` 单元是否承载别名信息，没有新增独立 `别名` 列或把同一角色拆成多个主体行？ | `GATE-CHAR-LIST-07` | `FAIL-CHAR-LIST-05` | `N6-RENDER` | 渲染后的 `角色清单.md` 表头检查、重复主体检查和别名收束记录。 |
| `原文描述（关键词式）` 是否按 registry 原词、source anchor 身份短语、项目已确认别名规则的优先级取证，并保持关键词式表达？ | `GATE-CHAR-LIST-07` | `FAIL-CHAR-LIST-08` | `N6-RENDER` | `description_keyword_evidence` 标明每个关键词来源；执行报告列出被压缩或删除的扩写内容。 |
| `原文描述（关键词式）` 是否没有加入外貌设计、服装设计、性格分析、后续剧情推断或提示词？ | `GATE-CHAR-LIST-07` | `FAIL-CHAR-LIST-08` | `N6-RENDER` | `角色清单.md` 抽样行、扩写删除记录和触发 `FAIL-CHAR-LIST-08` 的原句证据。 |
| 别名、代称、称谓和低置信风险的最终裁决是否由 LLM 完成，脚本只做读取、抽取、列检查、重复提示或机械校验？ | `GATE-CHAR-LIST-08` | `FAIL-CHAR-LIST-06` | `N4-MERGE` | 执行报告记录 LLM 裁决摘要与脚本辅助范围；若使用脚本，列明脚本没有生成 canonical 名称、归并判断或描述关键词。 |
