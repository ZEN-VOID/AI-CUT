# {{角色名称}}

source_character_list: `projects/aigc/<项目名>/3-主体/角色/1-清单/角色清单.md`
source_north_star: `projects/aigc/<项目名>/0-初始化/north_star.yaml`
source_team_synthesis: `projects/aigc/<项目名>/team.yaml.init_synthesis`

## 固定画面约束

- Format: full-body costume fitting photo
- Background: solid color background
- Scene Placement: no scene environment, no architecture, no street, no interior set, no props-heavy background
- Prompt Must Include: `full-body costume fitting photo, solid color background, no scene environment`
- Aesthetic Appeal: 强化镜头辨识度、容貌/身体/妆发/服装的审美完成度；审美路线必须匹配清单证据、年龄、性别/性别表达、身份、物种/族群、项目调性和角色权重。美丽、英俊、清癯、粗粝、威严、危险、怪诞、质朴或平凡但可识别都可成立；主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 必须写出 `charisma_floor=high` 的可见镜头魅力证据，不得只写“可识别”；不得把所有女性默认写美、所有男性默认写帅。真实人物灵感默认 none/generic_only，只有用户或项目允许且有必要时才原创转译。

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据

{{结合角色清单、north_star.yaml、team.yaml.init_synthesis 和必要考据，形成可执行研究证据链。研究不得停留在资料摘抄；每个镜头都必须转化为外观、服装、姿态、摄影或 prompt 决策。}}

### Identity Evidence

- Evidence: {{清单身份、关系、故事压力、项目主题中的身份线索}}
- Design Decision: {{身份如何转化为面部气质、身体状态、站姿、服装系统或视觉钩子}}
- Prompt Phrase: {{可进入英文 prompt 的身份/主体短语}}

### Occupation / Class Evidence

- Evidence: {{职业、劳动方式、权力位置、阶层、资源边界、教育或消费痕迹}}
- Design Decision: {{职业和阶层如何转化为手部痕迹、面料品质、服装状态/维护状态、配饰克制度、身体自信或拘谨；磨损只在有依据时写入}}
- Prompt Phrase: {{可进入英文 prompt 的职业/阶层/材质短语}}

### Region & Era Evidence

- Evidence: {{地域、年代、气候、制度、审美环境；若为推演必须标注}}
- Design Decision: {{地域年代如何转化为廓形、发型、色彩、鞋履、妆容和禁用元素}}
- Prompt Phrase: {{可进入英文 prompt 的地域年代短语；低证据时保持克制}}

### Costume Craft Evidence

- Evidence: {{剪裁、织物、工艺、闭合方式、层次、服装状态/维护状态/穿着状态或可参考来源；磨损、污渍、补丁、破洞只在有依据时写入}}
- Design Decision: {{服饰工艺如何支撑角色身份、动作和全身定妆照辨识度}}
- Prompt Phrase: {{可进入英文 prompt 的服装工艺短语}}

### Body & Posture Evidence

- Evidence: {{身体比例、重心、职业肌肉记忆、伤病或情绪防御；避免无证据医学化}}
- Design Decision: {{身体姿态如何转化为全身站姿、手部位置、头颈角度、肩背状态}}
- Prompt Phrase: {{可进入英文 prompt 的姿态短语}}

### Aesthetic Appeal Evidence

- Evidence: {{清单、主配角权重、性别气质、项目审美、角色正反派功能或用户偏好中的审美线索}}
- Source-Fit Aesthetic Target: {{按清单证据、年龄、性别/性别表达、身份、物种/族群、项目调性和角色权重选择美丽、英俊、清癯、粗粝、威严、危险、阴郁、病态、怪诞、质朴或平凡但可识别等路线；主角/大反派强化镜头完成度、气质、压迫性、危险魅力或服装系统，不强行美/帅/性化}}
- Charisma Floor: {{lead_high / major_antagonist_high / standard_distinctive / readable；主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 必须为 high，并说明脸部、眼神、妆发、身形、姿态、服装 signature 或镜头气质中的可见证据；普通配角/功能角色可为 standard_distinctive 或 readable}}
- Celebrity Face Inspiration: {{默认 none 或 generic_only；只有用户/项目明确允许且有必要时，才写 1 到 2 个明星/演员/模特的抽象脸型、骨相、眼神、妆发或镜头魅力灵感；必须原创转译，不得精确复刻现实人物}}
- Design Decision: {{审美目标与魅力下限如何转化为脸型、骨相、五官、眼神、妆发、身形比例、站姿、服装廓形、材质、配色和整体镜头吸引力}}
- Prompt Phrase: {{可进入英文 prompt 的审美短语，避免写成真实人物同款肖像}}

### Corpus Usage Trace

- Corpus Loaded: `knowledge-base/character-design-corpus.md`
- Trigger Reason: {{审美强化 / 妆容化 / 角色类型语料 / 服装时代语境 / prompt 审美短语；可多选}}
- Selected Corpus Lenses: {{男主/女主/反派/书生/武将/少年/成熟角色/平民等角色类型；妆容模式；服装时代语境}}
- Originalized Transfer: {{说明语料如何被转译到当前角色，不逐字套用，不形成模板脸或模板服装}}
- Costume Period Guardrail: {{说明服装风格化所依据的时代、地域、阶层、职业母体；时代不明时写 project-era-consistent costume silhouette}}
- Rejected Corpus Items: {{因时代、项目禁区、身份不符或过度现代化而剔除的语料；没有则写 none}}

### Taboo / Safety Constraints

- Project Taboos: {{来自 north_star.yaml / MEMORY.md / 用户要求的禁区}}
- Cultural / Identity Risks: {{文化误读、刻板化、年龄/性化、安全或版权风险}}
- Visual Guardrails: full-body costume fitting photo, solid color background, no scene environment; {{本角色额外禁止项}}

### Uncertainty Notes

- Confirmed From List: {{明确来自角色清单的事实}}
- Inferred By LLM: {{由 LLM 基于项目上下文推演的设计判断}}
- Needs Confirmation: {{需用户或上游补充确认的信息；没有则写 none}}
- Confidence: {{high / medium / low，并说明原因}}

### Prompt Evidence Chain

| Evidence | Design Decision | Prompt Phrase |
| --- | --- | --- |
| {{角色主体 ID / source row / 安全文件名}} | {{英文 prompt 必须以该主体 ID 号开头}} | {{主体ID}}: |
| {{身份/清单证据}} | {{主体设计决策}} | {{英文主体短语}} |
| {{职业/阶层证据}} | {{身体或服装决策}} | {{英文职业/阶层短语}} |
| {{地域年代证据}} | {{廓形/色彩/发型决策}} | {{英文地域年代短语}} |
| {{服饰工艺证据}} | {{面料/剪裁/层次决策}} | {{英文服装短语}} |
| {{身体姿态证据}} | {{全身定妆站姿决策}} | {{英文姿态短语}} |
| {{审美吸引力证据}} | {{来源匹配的审美路线、Charisma Floor、容貌、骨相、妆发、身形和服装吸引力决策；主角/大反派的 high 魅力证据必须可见；真实人物灵感如有则说明许可与原创转译}} | {{英文审美短语；不得指向精确复刻现实人物}} |
| {{语料库触发证据}} | {{角色类型、妆容、服装时代语境语料如何原创转译；剔除哪些不合时代/身份的词}} | {{最终采用的英文审美/服装短语}} |
| {{项目风格证据}} | {{光线/质感/影像调性决策}} | {{英文风格短语}} |
| deconstruction_coverage | {{## 4. 解构 / Identity & Story Pressure / Visual Drivers / Detailed Character Design / Detailed Costume Design / Cinematography}} | {{说明解构的全部有效身份、外观、服装、姿态、摄影槽位如何被整合进英文 prompt；若压缩、合并或剔除，写明理由}} |
| Skill fixed visual contract | 固定为纯色背景全身定妆照 | full-body costume fitting photo, solid color background, no scene environment |

## 3. 物语

{{结合以上内容展开散文式、诗意化的角色描述，说明身份、欲望、压力、关系、身体和服装如何共同显像。}}

## 4. 解构

主体ID号：{{角色主体 ID；必须与 5. 提示词设计中的主体 ID 号和英文 prompt 开头完全一致}}

## Identity & Story Pressure

Identity Hook: {{identity_hook}}
Narrative Tension: {{narrative_tension}}
Power / Relationship Axis: {{power_axis}}
Differentiation Axes: {{differentiation_axes}}

## Visual Drivers

Style Backbone: {{style_backbone}}
Character Style: {{character_style}}
Source-Fit Aesthetic Target: {{source_fit_aesthetic_target}}
Charisma Floor: {{charisma_floor}}
Celebrity Face Inspiration: {{celebrity_face_inspiration_none_generic_or_allowed_originalized}}
Face / Bone Aesthetic: {{face_bone_aesthetic}}
Costume Appeal Strategy: {{costume_appeal_strategy}}
Reference: {{body_reference}}
Face Signature: {{face_signature}}
Hair Signature: {{hair_signature}}
Silhouette & Build: {{body_signature}}
Costume System: {{costume_signature}}
Accessories & Continuity: {{continuity_signature}}
Design Guardrails: {{design_guardrails}}
Research Transfer: {{概括研究层如何转化为身份、职业、阶层、地域年代、服饰工艺、身体姿态、审美吸引力、禁区、不确定性和 prompt evidence chain}}
Corpus Transfer: {{概括 character-design-corpus.md 如何参与妆容化、角色类型审美和服装时代语境转译}}

## Detailed Character Design

Reference: {{body_reference}}
Age: {{body_age}}
Species / Ethnicity: {{body_species}}
Gender: {{body_gender}}
Occupation: {{body_occupation}}

### Face

- Aesthetic Function: {{说明脸型、骨相、五官和妆发如何服务来源匹配的审美目标，如美丽、英俊、清癯、粗粝、威严、危险、阴郁、病态、怪诞、质朴或平凡但可识别，而不是机械还原关键词}}
- Makeup: {{face_makeup}}
- Face Shape: {{face_shape_cn}}
- Bone Structure: {{face_bone_cn}}
- Eyes: {{face_eyes_cn}}
- Eyelashes: {{face_eyelash_cn}}
- Brows: {{face_brow_cn}}
- Nose: {{face_nose_cn}}
- Mouth: {{face_mouth_cn}}

### Hair

- Style: {{hair_style_cn}}
- Length: {{hair_length_cn}}
- Color: {{hair_color_cn}}
- Texture: {{hair_texture_cn}}
- Hairline: {{hairline_cn}}
- Temple Hair: {{temple_hair_cn}}

### Body

- Overall Style: {{body_style_cn}}
- Height: {{body_height_cn}}
- Weight: {{body_weight_cn}}
- Build: {{body_type_cn}}
- Posture: {{body_posture_cn}}
- Proportion: {{body_ratio_cn}}
- Upper Body:
  - Arms: {{upper_arm_cn}}
  - Fingers: {{finger_cn}}
- Lower Body:
  - Legs: {{leg_cn}}
  - Feet: {{foot_cn}}

### Personality

- Constellation: {{personality_constellation}}
- Blood Type: {{personality_blood_type}}
- Spirit: {{personality_spirit}}
- Emotional Profile: {{personality_emotion}}
- Interests: {{personality_interest}}
- Inner State: {{personality_inner}}
- Identity Core: {{personality_id}}

## Detailed Costume Design

- Costume Appeal: {{说明服装廓形、材质、配色、层次和露肤/包裹边界如何让角色好看、有型、有辨识度，并符合项目禁区}}
- Era: {{costume_era_cn}}
- Designer / Brand Reference: {{costume_brand_cn}}
- Styling Direction: {{costume_style_cn}}
- Cultural Elements: {{costume_culture_cn}}
- Type: {{costume_type_cn}}
- Material / Attribute: {{costume_attribute_cn}}
- Craft Logic: {{costume_craft_logic_cn}}
- Costume Condition / Maintenance Logic: {{costume_condition_maintenance_logic_cn; 先判断全新、礼服级整洁、高维护、制服化、洁净/无菌、日常穿着、轻度使用、修补、战损、污损或老化；磨损/做旧只在有依据时出现}}

### Wearing Details

- Head: {{costume_head_cn}}
- Upper Body: {{costume_upper_cn}}
- Lower Body: {{costume_lower_cn}}
- Footwear: {{costume_foot_cn}}

## Cinematography

Format: full-body costume fitting photo
Shot Size: full body
Background: solid color background
Scene Placement: no scene environment
Composition: {{composition}}
Camera Setup: {{camera_setup}}
Midjourney V8 Parameters: {{midjourney_params}}

## 5. 提示词设计

- 画面基调引用：{{引用 projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md 中的 Global Style Prompt}}
- 角色风格引用：{{优先引用 projects/aigc/<项目名>/2-美学/第N集/角色风格/角色风格协议.md 中的 Character Style Prompt；缺失时回退 projects/aigc/<项目名>/2-美学/角色风格/角色风格协议.md，并记录 fallback}}
- 主体 ID 号：{{角色主体 ID；若上游清单已有 ID 则原样沿用，否则使用清单行/角色安全名派生的 ASCII ID}}
- 固定画面约束：full-body costume fitting photo, solid color background, no scene environment

```text
{{英文整合提示词必须以主体 ID 号开头，格式为 "<主体ID>: ..."; 整合对象是 4. 解构的全部有效信息，而不是只拼接主体 ID、画面基调、角色风格、定妆照词和负向词；必须把 Identity & Story Pressure、Visual Drivers、Detailed Character Design、Detailed Costume Design、Cinematography 中的身份压力、面部/发型/身体、服装廓形与材质、姿态、构图、光线和固定画面约束蒸馏组织为自然流畅、可生成画面的英文整合提示词，1300 characters 以内；必须包含 full-body costume fitting photo / solid color background / no scene environment，并以自然语言写入 avoid scene environment, architecture, street, interior set, props cluster, extra characters, crowds, cropped body, sexualized framing 等负向约束，不得使用 --no。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{角色清单中的名称}}"
prompt_character_count: 0
reviewer: ""
review_status: ""
notes: ""
research_layer:
  identity: pending
  occupation_class: pending
  region_era: pending
  costume_craft: pending
  body_posture: pending
  aesthetic_appeal: pending
  charisma_floor: pending
  corpus_usage_trace: pending
  taboo_constraints: pending
  uncertainty_notes: pending
  prompt_evidence_chain: pending
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个角色主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究考据、物语、完整角色解构字段、提示词设计；研究考据必须包含固定研究镜头、审美吸引力证据和 prompt evidence chain。 |
| Output format | Markdown 单角色设计稿；`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`，再写固定解构字段 `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography`。 |
| Output path | Canonical 路径为 `projects/aigc/<项目名>/3-主体/角色/2-设计/C###-<角色名>.md`；若上游已有主体 ID，则用该 ID 替代 `C###`。 |
| Naming convention | 默认使用 `<主体ID>-<角色名>.md`；主体 ID 默认从 `C001` 起按清单顺序补零；冲突或多状态时在角色名后追加状态或首次登场 ID。 |
| Completion gate | 角色来自上游清单；已消费 `2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/角色风格/角色风格协议.md`、`north_star.yaml` 与 `team.yaml.init_synthesis`；研究层已转化为设计证据链并标明不确定性；容貌、妆发、骨相、身形和服装具备来源匹配的审美吸引力，审美路线与清单证据、年龄、性别/性别表达、身份、物种/族群、项目调性和角色权重一致；主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 已写出 `charisma_floor=high` 的可见证据，真实人物灵感如有则已获允许并原创转译；服装状态先于磨损判断，磨损/污渍/补丁/做旧只在有依据时出现；正文由 LLM 创作；`## 4. 解构` 下的主体 ID、`## 5. 提示词设计` 的主体 ID 和英文 prompt 开头三者一致；英文 prompt 以主体 ID 号开头，融合 `画面基调.Global Style Prompt + 角色风格.Character Style Prompt`，整合 `## 4. 解构` 全部有效信息，使用自然语言负向约束且不含 `--no`，不超过 1300 characters；画面固定为纯色背景全身定妆照，不置身具体场景。 |
