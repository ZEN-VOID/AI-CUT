# 角色设计输出合同

## Markdown Template Registry

Canonical structured template: `.agents/skills/aigc/3-主体/角色/2-设计/templates/character_masterprompt.structured.v2.md`

角色设计正文由 LLM 在 `2-设计` leaf 中完成；组根模板只登记结构真源，脚本仅做格式检查、字符计数和校验，不得批量生成、批量插入、正则套句或映射投影创作正文。

结构硬规则：`## 4. 解构` 标题下方必须先写 `主体ID号：<asset_id>`；默认稿 `asset_id=base_subject_id`，变体稿 `asset_id=variant_id`。该 ID 必须与文件名前缀、`## 5. 提示词设计` 的主体 ID 字段和英文 prompt 前缀完全一致。变体稿还必须记录 `Base Subject ID`、`Variant ID`、`Variant Label`、`Variant Type`、`Identity Invariants` 和 `Variant State Delta`。

变体身份硬规则：多服装、战斗态、战损态、受伤态、少年期、老年期、伪装或时间跳跃，是同一 `base_subject_id` 的资产变体，不是新 base character。变体必须保留脸部骨相、眼神、身形比例、核心气质、signature、身份压力或核心色彩等 `identity_invariants`；只在 `variant_state_delta` 中改变服装套系、战斗状态、损伤/伤势、年龄比例、妆发、姿态、配色或维护状态。

Prompt 整合硬规则：最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Identity & Story Pressure、Variant State、Visual Drivers、Detailed Character Design、Detailed Costume Design 与 Cinematography 信息；其中必须覆盖身份不变量、变体状态 delta、审美吸引力、`Lead Beauty / Handsomeness Floor`、`Lead Presence / Temperament Floor`、`Charisma Floor`、脸部/骨相策略、身高档位、身形比例、发型轮廓、整体气质/姿态能量、服装吸引力策略、服装配色系统、面部可读性光线和固定画面约束。只追加主体 ID、画面基调、角色风格、定妆照词或负向词，不构成完整整合。被压缩、合并或剔除的解构槽位必须在 `prompt_evidence_chain.deconstruction_coverage` 中说明。英文 prompt 必须控制在 1300 characters 内，使用自然语言负向约束，不得使用 Midjourney `--no` 参数。

来源匹配审美硬规则：角色设计不得只做清单关键词还原。审美路线必须匹配清单证据、年龄、性别/性别表达、身份、物种/族群、项目调性和角色权重；美丽、英俊、清癯、粗粝、威严、危险、阴郁、病态、怪诞、质朴或平凡但可识别都可以成立。主角、核心情感线角色和长期复用角色必须具备 `lead_beauty_handsomeness_floor=required` 的帅哥/美女/主角级好看证据，不能只有气场或可识别度；同一批角色还必须具备 `lead_presence_temperament_floor=required` 的整体气质、主角感、精神状态、姿态能量和镜头存在感证据，不能只有漂亮脸、好身材或服装好看；主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 必须具备 `charisma_floor=high` 的可见镜头魅力证据，不能只写“可识别”；普通正派、普通反派、配角和功能角色必须有个性化魅力或清晰可识别度。主角帅/美和气质下限必须来源匹配、年龄安全、身份匹配，不等于成人化、性化、模板脸、空泛“有气质”或真实人物复刻。真实人物灵感默认不用或泛化处理，只有用户/项目允许且有必要时才可作为原创转译参考，不得精确复刻、换脸、同款肖像或让角色可识别为现实本人。

语料库触发硬规则：命中审美强化、妆容化、角色类型词库、服装时代语境或 prompt 审美短语时，必须加载 `knowledge-base/character-design-corpus.md` 并留下 `corpus_usage_trace`。语料只能原创转译，不能逐字套用成模板脸或模板服装；服装风格化必须回到项目时代、地域、阶层和职业母体。

身体造型与配色硬规则：角色设计必须明确 `height_scale`、`body_build`、`hair_design` 和 `costume_color_palette`。身高可以用档位或安全范围，不强制具体数字；身形必须写骨架、肩颈背、腰线、四肢比例、重心等可见结构；发型必须写长度、体量、轮廓、发际/鬓角和时代/职业适配；服装配色必须写主色、辅色、点缀色、明度/饱和度/冷暖/反差和文化/身份含义。只写“高挑、修长、黑发、深色衣服、华丽配色”不得通过。

面部可读性光线硬规则：角色设计是可复用主体资产，不是剧情暗场肖像。`Cinematography` 和英文 prompt 必须确保脸部骨相、眉眼、鼻梁、嘴部、肤色层次和表情意图清晰可读；允许受控侧光、轮廓光、低调反差或局部眼尾压暗来强化气质，但不得用重阴影、遮眼阴影、半脸阴影、低调剪影、`shadowed face`、`deep facial shadow`、`low-key silhouette`、`dark face` 等作为主效果。阴郁、危险或压迫感应通过可读眉眼、骨相、姿态、服装材质和受控边缘光表达，并在 prompt 中写入 `soft frontal fill light`、`clear readable facial features` 或等价短语。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 输出结构是否以 `.agents/skills/aigc/3-主体/角色/2-设计/templates/character_masterprompt.structured.v2.md` 为 canonical structured template，而不是由组根模板或脚本生成角色设计正文？ | `GATE-CHAR-DESIGN-14` | `FAIL-CHAR-DESIGN-TEMPLATE-REGISTRY` | `N7-MERGE-DRAFT` | 模板路径、渲染来源、脚本机械边界说明 |
| `## 4. 解构` 标题下方是否先写 `主体ID号：<asset_id>`，并与文件名前缀、`## 5. 提示词设计` 主体 ID 字段、英文 prompt 前缀完全一致？ | `GATE-CHAR-DESIGN-11` | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | 四处 asset ID 对照表、文件名前缀检查 |
| 变体稿是否记录 `base_subject_id / variant_id / identity_invariants / variant_state_delta`，并保留同一角色身份，不把状态写成新人物？ | `GATE-CHAR-DESIGN-23` | `FAIL-CHAR-DESIGN-VARIANT-INVARIANT` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | variant integrity evidence、base/variant ID map、identity invariants、state delta |
| 英文 prompt 是否整合 `Identity & Story Pressure`、`Variant State`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design` 与 `Cinematography` 全部有效信息，覆盖身份不变量、变体状态 delta、审美吸引力、`Lead Beauty / Handsomeness Floor`、`Lead Presence / Temperament Floor`、`Charisma Floor`、脸部/骨相策略、整体气质/姿态能量、服装吸引力和面部可读性光线，而不是只追加主体 ID、画面基调、角色风格、定妆照词或负向词？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 与解构槽位对照、`deconstruction_coverage` |
| 被压缩、合并或剔除的解构槽位是否在 `prompt_evidence_chain.deconstruction_coverage` 中说明？ | `GATE-CHAR-DESIGN-08` | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage` 缺口记录 |
| 英文 prompt 是否不超过 1300 characters，使用自然语言负向约束，且没有 Midjourney `--no` 参数？ | `GATE-CHAR-DESIGN-12` | `FAIL-PROMPT-SHALLOW-INTEGRATION` | `N7-MERGE-DRAFT` | prompt 字符数、负向约束文本、`--no` 检查 |
| 角色容貌、妆发、骨相、身形和服装是否具备来源匹配的审美吸引力；主角、核心情感线角色和长期复用角色是否具备 `lead_beauty_handsomeness_floor=required` 的帅哥/美女/主角级好看证据，并具备 `lead_presence_temperament_floor=required` 的整体气质、主角感、精神状态和镜头存在感证据；主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 是否具备 `charisma_floor=high` 的可见镜头魅力证据；真实人物灵感是否获允许并原创转译而非现实人物复刻？ | `GATE-CHAR-DESIGN-19` | `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | `N7-MERGE-DRAFT` | `aesthetic_appeal_evidence`、来源匹配审美目标、`Lead Beauty / Handsomeness Floor`、`Lead Presence / Temperament Floor`、`Charisma Floor`、脸部骨相策略、服装吸引力策略、真实人物灵感原创转译说明 |
| 命中审美强化、妆容化、角色类型词库、服装时代语境或 prompt 审美短语时，是否加载 `knowledge-base/character-design-corpus.md` 并留下原创转译证据？ | `GATE-CHAR-DESIGN-20` | `FAIL-CHAR-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `corpus_usage_trace`、选用 lens、服装时代语境、剔除语料说明 |
| 身高档位/安全范围、身形结构、发型轮廓和服装配色系统是否进入解构、证据链和英文 prompt，而不是泛词占位？ | `GATE-CHAR-DESIGN-21` | `FAIL-CHAR-DESIGN-PHYSICAL-STYLING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `height_scale`、`body_build`、`hair_design`、`costume_color_palette`、`deconstruction_coverage` |
| 摄影字段和英文 prompt 是否保持脸部骨相、眉眼、鼻梁、嘴部、肤色层次和表情意图清楚可读，而不是用重阴影、遮眼阴影、半脸阴影或低调剪影吞掉面部特征？ | `GATE-CHAR-DESIGN-22` | `FAIL-CHAR-DESIGN-FACE-READABILITY` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `face_readability_lighting`、`Cinematography / Face Readability Lighting`、prompt 光线短语、`deconstruction_coverage` |
