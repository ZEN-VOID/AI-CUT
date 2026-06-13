# Character Design Contract

本文件展开 `角色/2-设计` 的业务细则。入口、路由和最终输出路径仍以同目录 `SKILL.md` 为准。

## Upstream Consumption

- Canonical input: `projects/aigc/<项目名>/11-主体/角色/1-清单/角色清单.md`。
- Required columns: `名称`、`首次登场`、`原文描述（关键词式）`。
- 本技能只能为清单中存在的角色主体生成设计稿。
- 若清单存在同名冲突、疑似漏项或角色归并错误，输出执行报告提出上游修复建议，不直接修改清单。

## Project Context Consumption

`3-美学/画面基调/全局风格协议.md` + 当前集优先/项目级回退的 `3-美学/角色风格/角色风格协议.md`:

- 抽取 `Global Style Prompt`、`Character Style Prompt`、角色造型原则、服装/妆发/身体语言和负向审美边界；角色设计风格词必须由 `画面基调.Global Style Prompt + 角色风格.Character Style Prompt` 组成。
- 若字段命名不统一，由 LLM 根据语义识别，但必须在执行报告中说明使用了哪些字段。
- 不得虚构不存在的画面基调或角色风格；缺失时写明具体缺失文件和字段，不得从 `north_star.yaml` 补造最终风格提示词。

`north_star.yaml`:

- 抽取项目北极星、主题、时代/地域、创作阶段不变量、禁区和视觉约束。
- 只作为项目语义与安全边界来源，不作为角色最终风格提示词真源。

`team.yaml.init_synthesis`:

- 只消费初始化阶段已统合的、与导演、美术、服装、摄影、角色设计、表演、动漫/漫画视觉相关的设计种子、约束、启发和风险。
- 初始化综合是创作前上下文，不是文风模仿许可；输出应吸收其设计判断，而不是堆人名。
- 多个初始化建议冲突时，以用户请求、项目 north star 和角色功能为裁决依据。

## LLM-First Creative Authorship

- 研究考据、物语、解构、服装设计、摄影描述和提示词必须由 LLM 直接完成。
- 脚本不得生成创作正文，不得把字段模板扩写成设计稿，不得根据关键词拼接英文 prompt。
- 脚本允许执行：读取上游清单、列检查、路径创建、文件存在检查、prompt 字符数统计、空字段报告、manifest 汇总。

## Research Layer Contract

研究层不是资料堆叠，而是把上游清单、项目上下文、必要考据和 LLM 创作判断转换为后续设计可执行的证据链。每个角色必须形成 `research_profile`，并让结论回流到 `物语`、`解构`、`Cinematography` 和英文 prompt。

### Required Research Lenses

| lens | required question | design conversion |
| --- | --- | --- |
| `identity` | 这个人以什么身份被世界看见，自己又如何抵抗或认领这个身份？ | 写入 `Identity & Story Pressure`、面部气质、姿态和 prompt 主体短语 |
| `occupation` | 角色的劳动、权力、技能或日常职能是什么？ | 转化为手部痕迹、站姿、服装功能、工具痕迹；不得把道具作为背景主元素 |
| `class` | 角色的阶层、资源、教育、权力距离和消费痕迹如何显现？ | 转化为面料品质、磨损方式、配饰克制度、身体自信或拘谨 |
| `region_era` | 地域、年代、气候、制度和审美环境带来什么可见限制？ | 转化为廓形、色彩、发型、鞋履、化妆和禁用元素 |
| `costume_craft` | 服饰的剪裁、织物、工艺、闭合方式、层次和使用痕迹是什么？ | 写入 `Detailed Costume Design`，并压缩进英文 prompt 的服装短语 |
| `body_posture` | 身体比例、重心、肌肉记忆、职业姿态和情绪防御如何呈现？ | 写入 `Detailed Character Design / Body`、`Cinematography` 和 prompt 姿态 |
| `aesthetic_appeal` | 这个角色如何从清单关键词提升为好看、有辨识度、有镜头魅力的主体？女性是否美丽动人，男性是否英俊不凡，主角是否进一步强化颜值、气质和服装完成度？明星脸灵感是否只作原创转译？ | 写入 `Visual Drivers`、`Detailed Character Design / Face`、`Detailed Costume Design` 和 prompt 审美短语 |
| `corpus_usage` | 当前角色是否命中高质量语料库触发：审美强化、妆容化、角色类型词库、服装时代语境或 prompt 审美短语？ | 写入 `Corpus Usage Trace`，说明选用 lens、原创转译、服装时代语境和剔除语料 |
| `taboo_constraints` | 有哪些文化误读、项目禁区、年龄/性化、安全或版权风险？ | 写入 guardrails；prompt 必须避开禁区并保持定妆照约束 |
| `uncertainty` | 哪些信息来自清单，哪些来自推演，哪些需要考据或用户确认？ | 在 `Uncertainty Notes` 标注置信度，不把低证据推演写成事实 |
| `prompt_evidence_chain` | prompt 中每个关键主体、服装、姿态、光线、风格短语来自哪里？ | 生成 `Prompt Evidence Chain`，确保英文 prompt 可回指研究与项目风格 |

### Evidence Rules

- 每个研究镜头至少输出一个 `design implication`；没有设计转化的资料不得进入最终稿。
- `Prompt Evidence Chain` 必须按 `evidence -> design decision -> prompt phrase` 写清，覆盖身份、服装、姿态、摄影、`画面基调 + 角色风格` 和固定画面约束。
- 若证据薄弱，使用 `likely`、`inferred`、`open question` 等标记；中文稿中必须写明“推演”或“待确认”，不得伪装成清单事实。
- 研究层可以参考外部资料，但 canonical 判断仍由 LLM 综合项目上下文完成；外部资料不能覆盖 `north_star.yaml`、用户禁区或清单锚点。
- 服饰工艺必须服务角色身份与身体动作，不得只写品牌、潮流词或抽象审美。
- 身体姿态必须服务纯色背景全身定妆照：允许写站姿、重心、手部位置和头颈角度，不得引入剧情场景或环境动作。
- 审美吸引力必须转成具体可见设计：脸型、骨相、五官、眼神、妆发、身形比例、服装廓形、材质、配色、层次和镜头气质。不得只写“好看”“帅”“高级”。
- 女性角色默认朝美丽、动人、有辨识度设计；男性角色默认朝英俊、不凡、有辨识度设计；主角必须比一般角色更突出颜值、气质和服装完成度。
- 反派、配角和功能角色也必须有个性化魅力，可以锋利、危险、阴郁、病态或怪诞，但不能平庸、模板脸或只靠职业标签区分。
- 明星、演员或模特只能作为脸型、骨相、眼神、妆发或镜头魅力的灵感来源；输出必须原创转译，不得写成精确复刻、换脸、同款肖像或现实本人可识别形象。
- `knowledge-base/character-design-corpus.md` 是审美强化、妆容化和服装时代语境的授权知识库；命中触发条件时必须加载，并用 `Corpus Usage Trace` 说明转译过程。
- 使用语料库时，先定角色类型和项目时代母体，再选择脸部、妆容、服装词。不得先套“剑眉星目 / 楚楚动人 / 哥特 / 高定”等词，再反推角色。

## Web Search Allowance

网络搜索只在以下条件下允许：

- 用户明确要求考据，或角色涉及冷门历史、地域、民族服饰、职业制服、宗教/礼仪、器物、医学、军事、法律、真实地点等容易误写的信息。
- 搜索用于支持 `研究考据`，不能替代 LLM 对角色设计的综合判断。
- 搜索结果必须保留来源名称、访问日期或链接摘要；若来源不确定，写为“参考线索”而非事实。
- 搜索不得泄露项目未公开内容，不得把外部版权文本长段复制进设计稿。

## Required Content Blocks

每份设计稿必须包含以下块：

1. `名称 / 首次登场 / 原文描述复述`
2. `研究考据`
3. `物语`
4. `解构`
5. `提示词设计`

`解构` 固定子字段：

- 标题 `## 4. 解构` 下方必须先写 `主体ID号：<主体ID>`；该值必须与 `提示词设计` 的主体 ID 字段和英文 prompt 前缀一致。
- `Identity & Story Pressure`
- `Visual Drivers`
- `Detailed Character Design`
- `Detailed Costume Design`
- `Cinematography`

`Visual Drivers` 必须额外覆盖：

- `Beauty / Handsomeness Target`
- `Face / Bone Aesthetic`
- `Costume Appeal Strategy`
- 可选 `Celebrity Face Inspiration`，且只能写原创转译参考，不得精确复刻现实人物。
- `Corpus Usage Trace`，用于记录 `knowledge-base/character-design-corpus.md` 的触发原因、选用 lens、原创转译和服装时代语境。

`提示词设计`:

- 使用英文。
- 开头必须包含主体 ID 号，格式为 `<主体ID>: ...`；主体 ID 来自上游清单、source row 或角色安全名派生的 ASCII ID。
- 英文 prompt 开头的主体 ID 必须与 `## 4. 解构` 下方 `主体ID号：<主体ID>` 完全一致。
- 引用并融合 `画面基调.Global Style Prompt`。
- 引用并融合 `角色风格.Character Style Prompt`，服装风格化只作为角色风格在服装系统中的可见落点。
- 最终英文整合提示词的整合对象是 `## 4. 解构` 的全部有效信息，包括 `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography` 中的身份压力、视觉钩子、面部/发型/身体、审美吸引力、服装廓形与材质、姿态、构图、光线和固定画面约束；不得只把主体 ID、画面基调、角色风格、定妆照词或负向词作为前缀/后缀拼接后宣布完成。
- 明确包含 `full-body costume fitting photo`、`solid color background` 和 `no scene environment`。
- 控制在 1300 characters 内。
- 使用自然语言负向约束，例如 `avoid scene environment, architecture, street, interior set, props cluster, extra characters, crowds, cropped body, sexualized framing`；不得使用 Midjourney `--no` 参数。
- 不包含 markdown 表格、中文解释或多版本堆叠。

`研究考据` 固定子字段：

- `Identity Evidence`
- `Occupation / Class Evidence`
- `Region & Era Evidence`
- `Costume Craft Evidence`
- `Body & Posture Evidence`
- `Aesthetic Appeal Evidence`
- `Corpus Usage Trace`
- `Taboo / Safety Constraints`
- `Uncertainty Notes`
- `Prompt Evidence Chain`

## Fixed Visual Constraint

- 角色设计稿默认是纯色背景全身定妆照，用于锁定角色身体、服装、比例和可重复识别点。
- 不得让角色置身于剧情场景、建筑空间、街景、室内陈设、自然环境或复杂背景。
- `Cinematography` 必须写作棚拍式角色设计参考：full body、solid color background、neutral design lighting。
- 如果项目上下文需要表达角色所属场景，只能在研究/物语中说明，不得让最终画面进入该场景。

## Non-Goals

- 不生成最终图片。
- 不创建场景、道具、分镜或视频提示词。
- 不修改 registry、父级 skill、上游清单或其他 worker 负责的技能包。
- 不把单角色设计稿变成项目百科。
- 不输出环境肖像、剧情剧照、场景内角色照或半身头像作为默认主图口径。
- 不把研究层写成百科条目、真实资料摘抄或来源汇编；研究必须转化为角色设计决策。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 待设计角色是否能回指 `角色清单.md` 的 `名称 / 首次登场 / 原文描述（关键词式）`，且未凭设计阶段兴趣新增主体？ | `GATE-CHAR-DESIGN-01` | `FAIL-NO-LIST` | `N3-CHARACTER-LIST` | `character_intake_table`、清单行号、缺失字段说明 |
| 同名冲突、疑似漏项或归并错误是否只形成上游修复建议，而没有在本 leaf 直接改清单或静默裁决 canonical 主体？ | `GATE-CHAR-DESIGN-02` | `FAIL-CHAR-DESIGN-UPSTREAM-SCOPE` | `N1-INTAKE` / `N3-CHARACTER-LIST` | `execution_scope`、上游修复建议、未改动上游声明 |
| `3-美学/画面基调/全局风格协议.md` 的 `Global Style Prompt`、当前集优先/项目级回退的 `3-美学/角色风格/角色风格协议.md` 的 `Character Style Prompt`、`north_star.yaml` 的主题/时代/地域/禁区和视觉约束是否被读取；字段漂移、fallback 或缺失是否明确报告，而非虚构风格？ | `GATE-CHAR-DESIGN-03` | `FAIL-NO-STYLE` | `N2-PROJECT-CONTEXT` | `project_design_context`、已消费字段清单、缺失字段说明 |
| `team.yaml.init_synthesis` 是否只消费设计相关初始化综合，并把冲突建议按用户请求、north star 与角色功能裁决，而不是堆人名、模仿文风或补造顾问问答？ | `GATE-CHAR-DESIGN-04` | `FAIL-CHAR-DESIGN-ADVISOR-CONTEXT` | `N2-PROJECT-CONTEXT` / `N6-INIT-SYNTHESIS-REVIEW` | init synthesis source、冲突裁决依据、剔除无关内容说明 |
| 研究考据、物语、解构、服装设计、摄影描述和 prompt 是否由 LLM 主创，脚本只做读取、列检查、路径、统计、空字段和 manifest 汇总？ | `GATE-CHAR-DESIGN-05` | `FAIL-SCRIPT-AUTHORSHIP` | `N7-MERGE-DRAFT` | 脚本职责清单、LLM 汇流声明、正文生成来源说明 |
| `identity / occupation / class / region_era / costume_craft / body_posture / aesthetic_appeal / taboo_constraints / uncertainty / prompt_evidence_chain` 是否都产生设计转化，而非资料堆叠？ | `GATE-CHAR-DESIGN-06` | `FAIL-RESEARCH-FLAT` | `N5-RESEARCH-PROFILE` | `research_profile`、研究镜头与审美证据覆盖表、每个 lens 的 `design implication` |
| 低证据推演、外部资料线索和待确认项是否标明“推演/待确认/置信度”，没有伪装成清单事实？ | `GATE-CHAR-DESIGN-07` | `FAIL-UNCERTAINTY-HIDDEN` | `N5-RESEARCH-PROFILE` | `Uncertainty Notes`、来源/置信度标注、待确认项 |
| prompt 中关键主体、服装、姿态、光线、风格和固定画面短语是否能回指 `evidence -> design decision -> prompt phrase`？ | `GATE-CHAR-DESIGN-08` | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage` |
| 网络搜索是否仅在用户许可或冷门考据必要时使用，并留下来源摘要/使用边界，没有泄露项目内容或复制外部版权长文？ | `GATE-CHAR-DESIGN-09` | `FAIL-CHAR-DESIGN-WEB-EVIDENCE` | `N5-RESEARCH-PROFILE` | 搜索许可/必要性说明、来源摘要、使用边界 |
| 设计稿是否包含清单锚点、研究考据、物语、解构、提示词设计五个必填块？ | `GATE-CHAR-DESIGN-10` | `FAIL-CHAR-DESIGN-SECTIONS` | `N7-MERGE-DRAFT` | 模板块覆盖检查、缺块 finding |
| `## 4. 解构` 下方是否先写 `主体ID号：<主体ID>`，且与 `## 5. 提示词设计` 主体 ID 和英文 prompt 前缀一致？ | `GATE-CHAR-DESIGN-11` | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | 解构 ID、提示词 ID、prompt 前缀、文件名前缀对照 |
| 英文 prompt 是否融合 `画面基调.Global Style Prompt + 角色风格.Character Style Prompt` 和 `## 4. 解构` 全部有效信息，控制 1300 characters 内，使用自然语言负向约束且不含 `--no`？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 字符数、`deconstruction_coverage`、自然语言负向约束检查 |
| 摄影字段和 prompt 是否固定为纯色背景全身定妆照，没有进入剧情场景、建筑、街景、室内陈设、自然环境、复杂背景或半身头像？ | `GATE-CHAR-DESIGN-13` | `FAIL-CHAR-DESIGN-FIXED-VISUAL` | `N7-MERGE-DRAFT` | fixed visual phrase 检查、禁用环境元素清单 |
| 容貌、妆发、骨相、身形和服装是否具备审美吸引力；女性角色是否美丽动人、男性角色是否英俊不凡、主角是否更突出；正反派是否都有个性化魅力；明星脸灵感是否原创转译？ | `GATE-CHAR-DESIGN-19` | `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | `N7-MERGE-DRAFT` | `aesthetic_appeal_evidence`、审美目标、脸部骨相策略、服装吸引力策略、明星脸原创转译说明 |
| 命中审美强化、妆容化、角色类型词库、服装时代语境或 prompt 审美短语时，是否加载 `knowledge-base/character-design-corpus.md`，并留下原创转译与时代语境校验证据？ | `GATE-CHAR-DESIGN-20` | `FAIL-CHAR-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `corpus_usage_trace`、选用 lens、服装时代语境、剔除语料说明 |
| 本文件的 Non-Goals 是否被执行：不生成图片，不创建场景/道具/分镜/视频提示词，不修改父级、registry、上游清单或其他 worker 范围？ | `GATE-CHAR-DESIGN-02` | `FAIL-CHAR-DESIGN-UPSTREAM-SCOPE` | `N1-INTAKE` | `execution_scope`、改动文件清单、越界项排除说明 |
