# {{道具名称}}

source_prop_list: `projects/aigc/<项目名>/3-主体/道具/1-清单/道具清单.md`
source_type_style: `projects/aigc/<项目名>/2-美学/类型风格.md`
source_visual_tone: `projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md`
source_prop_style: `projects/aigc/<项目名>/2-美学/第N集/道具风格/道具风格协议.md` 或 `projects/aigc/<项目名>/2-美学/道具风格/道具风格协议.md`
source_project_memory: `projects/aigc/<项目名>/MEMORY.md`

## 固定画面约束

- Type: full-view single prop shot
- Camera Angle: 45-degree view
- Framing: full prop in view, entire prop fully visible, uncropped full silhouette, prop only
- Background: solid color background only, no background elements
- Scene Placement: no scene environment, no tabletop scene, no room set, no street, no hands holding the prop, no people
- Prompt Must Include: `full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background, no people, no background elements, no scene environment`
- Design Appeal: 道具必须有可见设计价值，不得只是简单功能还原或平凡物件；文化/身份/机构/功能符号和装饰纹样只在有证据、有语境或有功能必要时写入。极简、洁净、无菌、高科技或工业道具可通过比例、材质精度、结构逻辑、维护状态和表面处理形成设计感。

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据

{{结合道具清单、2-美学输出、项目 MEMORY / CONTEXT 和必要考据，思考当前道具符合叙事的文化属性和具象特征；若涉及冷门信息点且本地资料不足，可启用网络搜索并记录来源或不确定性。研究必须转译为可见设计，不写不能改变形制、材料、工艺、年代、使用状态/保存状态、功能逻辑或 prompt token 的百科段落。}}

### 研究证据链

| source cue | confidence | visual translation | design lock / allow variation | prompt evidence token |
| --- | --- | --- | --- | --- |
| {{清单 / 2-美学 / MEMORY / CONTEXT / source_fact / inference / inspired_by / unknown}} | {{confirmed / probable / inferred / uncertain；说明风险或缺口}} | {{形制 / 材料 / 工艺 / 年代 / 使用状态/保存状态 / 功能逻辑 / 风险不确定性}} | {{必须锁定的识别点；允许变化的细节}} | {{英文 prompt 中可追溯的短 token}} |

### 研究转译清单

- 形制：{{轮廓、比例、开口、接口、可动件、携带/存放逻辑；不得要求手或人物入镜}}
- 材料：{{主材、副材、表面处理、反光/吸光、重量感}}
- 工艺：{{铸造、锻打、漆面、雕刻、缝制、拼接、修补等可见工艺痕迹}}
- 设计细节：{{独特轮廓、材质记忆点、工艺/结构细节、条件性装饰、signature detail、生成时必须锁定的识别点}}
- 文化 / 身份 / 功能符号：{{若有依据，写纹样、铭文、徽记、封缄、器型、地域/时代/阶层/职业/机构/功能符号，并说明文化语境与禁区；若无依据，写 none / minimal / function-led detail，不得随机贴花}}
- 年代：{{时代、地域、技术阶段或世界观层级如何影响造型；不确定则写 inspired by}}
- 使用状态 / 保存状态：{{根据上游证据、年代、持有者、环境和功能判断，可为全新、未启封、洁净/无菌、高维护抛光、展陈级完好、仪式封存、轻度使用、重度磨损、修补、氧化、污染或损伤；磨损、划痕、污渍、包浆、锈蚀、破损只在有依据时写入，不得强行做旧}}
- 功能逻辑：{{道具如何被识别、开启、储存、误用或象征性使用；只写可见逻辑，不写操作教程}}
- 风险/不确定性：{{事实缺口、冷门考据、文化误读、危险用途、生成歧义和保守表达方案}}

## 3. 物语

{{结合以上内容展开散文式、诗意化的道具描述，说明物件的功能、主人痕迹、时间沉积、象征压力和视觉记忆点。}}

## 4. 解构

主体ID号：{{道具主体 ID；必须与 5. 提示词设计中的主体 ID 号和英文 prompt 开头完全一致}}

## Photography

Type: full-view single prop shot
Shot Size: full object view
Camera Angle: 45-degree view
Framing: full prop in view, entire prop fully visible, uncropped full silhouette, prop only
Background: solid color background only, no background elements
Scene Placement: no scene environment, no hands holding the prop, no people

## Prop Design

Style Backbone: {{style_backbone}}
Design Appeal Target: {{prop_must_be_visually_designed_not_plain_en}}
Signature Detail: {{unique_silhouette_material_memory_craft_detail_or_iconic_mark_en}}
Cultural Element Strategy: {{period_region_class_profession_symbol_or_motif_with_context_guardrail_en}}
Craft / Ornament Detail: {{visible_craft_ornament_pattern_inscription_seal_binding_inlay_or_repair_detail_en}}
Period Context Guardrail: {{era_region_technology_class_and_forbidden_mismatch_en}}
Condition State Policy: {{condition_or_preservation_state_en; include pristine/new/sealed/clean/polished/maintained/display-grade/used/worn/repaired/oxidized only when supported; do not force distress, dirt, patina, rust, or damage}}
Prop Type: {{prop_type_en}}
Design Inspiration: {{design_inspiration_en}}
Period Attribute: {{period_attribute_en}}
Functionality: {{functionality_en}}
Evidence Logic: {{how_research_translates_into_shape_material_craft_period_condition_function_en}}

Shape Sense: {{shape_en}}
Line Sense: {{line_sense_en}}
Dimensional Layering: {{volume_en}}
Size: {{size_en}}

Material Detail: {{material_en}}
Texture Detail: {{texture_en}}
Decoration Detail: {{decoration_en}}
Pattern Detail: {{pattern_en}}

Art Elements: {{art_element_en}}
Cultural Elements: {{culture_en}}
Ergonomics: {{ergonomics_en}}

## Prop Corpus Usage Trace

- Corpus Loaded: `knowledge-base/prop-design-corpus.md`
- Trigger Reason: {{single_prop / batch_from_inventory / incremental_fill / repair 中涉及道具审美、文化/身份符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语时必须触发}}
- Corpus Seeds Used: {{从语料库中选用的类型语汇、文化/身份符号、设计轴或短语转化，不得整段照搬}}
- Original Transfer: {{如何转译为当前项目时代、地域、阶层、职业、人物关系和道具功能；不得脱离时代语境}}
- Period / Culture Guardrail: {{避免现代奢侈品、街头潮牌、战术风、赛博朋克、哥特奇幻等错置元素；说明保守处理}}
- Evidence In Prompt: {{英文 prompt 中对应的设计细节、条件性文化/身份符号、工艺/结构细节、使用/保存状态或功能结构 token；文化贴花与旧化 token 都必须说明依据}}

## 5. 提示词设计

- 画面基调引用：{{引用 projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md 中的 Global Style Prompt}}
- 道具风格引用：{{优先引用 projects/aigc/<项目名>/2-美学/第N集/道具风格/道具风格协议.md 中的 Prop Style Prompt；缺失时回退 projects/aigc/<项目名>/2-美学/道具风格/道具风格协议.md，并记录 fallback}}
- 主体 ID 号：{{道具主体 ID；若上游清单已有 ID 则原样沿用，否则使用清单行/安全文件名派生的 ASCII ID}}
- 固定画面约束：full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background, no people, no background elements, no scene environment

### Prompt Evidence Chain

| prompt token | evidence source | reason |
| --- | --- | --- |
| {{主体 ID 号 prefix}} | {{道具清单主体 ID / source_row / 安全文件名}} | {{英文 prompt 必须以该主体 ID 号开头}} |
| {{single prop subject token}} | {{名称 / 原文描述 / Prop Design}} | {{锁定单道具主体}} |
| {{form / material / craft / period / condition / function token}} | {{研究证据链对应行}} | {{说明该 token 如何来自研究转译；worn/scratched/dirty/patinated/rusted/damaged 等旧化 token 必须有依据}} |
| {{design detail / cultural motif / function-led detail token}} | {{Prop Design / Prop Corpus Usage Trace}} | {{说明设计细节、文化/身份/功能符号、纹样、铭文、徽记、工艺、结构或装饰如何原创转译且符合时代语境；无依据时说明为何采用克制/极简/功能主导路线}} |
| deconstruction_coverage | {{## 4. 解构 / Photography / Prop Design}} | {{说明 Photography 与 Prop Design 的全部有效镜头、形制、材质、工艺、年代、使用/保存状态、功能和尺度槽位如何被整合进英文 prompt；若压缩、合并或剔除，写明理由}} |
| `full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background, no people, no background elements, no scene environment` | 固定画面约束 | 锁定完整展示道具全貌、完整轮廓和主要结构，仅展示道具、纯色背景单道具 45 度全貌展示，不做局部特写或裁切特写，不置身场景，不出现人物或背景元素 |

```text
{{英文整合提示词必须以主体 ID 号开头，格式为 "<主体ID>: ..."; 整合对象是 4. 解构的全部有效信息，而不是只拼接主体 ID、画面基调、道具风格、固定画面词和负向词；必须把 Photography 与 Prop Design 中的全貌构图、45 度角度、完整轮廓、形制、线条、体积、材料、纹理、条件性装饰/符号、年代、使用/保存状态、功能逻辑和固定画面约束蒸馏组织为自然流畅、可生成画面的英文整合提示词，1300 characters 以内；仅在证据支持时写入 worn、scratched、dirty、patinated、rusted、damaged 等旧化词；必须包含 full-view prop shot / 45-degree view / full prop in view / entire prop fully visible / uncropped full silhouette / prop only / solid color background / no people / no background elements / no scene environment，并以自然语言写入 avoid people, hands, character, model, body parts, tabletop scene, room set, street, landscape, props cluster, background elements, cropped prop, partial prop, detail-only composition 等负向约束，不得使用 --no。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{道具清单中的名称}}"
prompt_character_count: 0
research_chain_status: pending
design_detail_culture_status: pending
prop_corpus_usage_status: pending
prompt_evidence_chain_status: pending
reviewer: ""
review_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个道具主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究证据链、物语、完整 Photography + Prop Design 解构、Prop Corpus Usage Trace、提示词设计。 |
| Output format | Markdown 单道具设计稿；`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`，再写固定解构字段 `Photography` 与 `Prop Design`；英文 prompt 放入 fenced text block。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/3-主体/道具/2-设计/PROP-###-<安全文件名>.md`；若上游已有主体 ID，则用该 ID 替代 `PROP-###`。 |
| Naming convention | 默认使用 `<主体ID>-<安全文件名>.md`；主体 ID 默认从 `PROP-001` 起按清单顺序补零；同名或多状态道具在安全文件名后追加首次登场 ID 或状态。 |
| Completion gate | 道具来自上游清单；已消费 `2-美学/类型风格.md`、`2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/道具风格/道具风格协议.md`、项目 `MEMORY.md` 与 `project_memory_init_context`；正文由 LLM 创作；研究已转译为形制/材料/工艺/设计细节/文化或身份符号适用性/年代/使用状态/保存状态/功能逻辑/风险不确定性；道具有可见设计价值，不得只是简单功能还原或平凡物件；文化符号、纹样、铭文、徽记和装饰只在有证据、有语境或有功能必要时出现，不得默认贴花；磨损、污渍、包浆、锈蚀、破损等旧化词只在有依据时出现，不得默认做旧；触发时已加载 `knowledge-base/prop-design-corpus.md` 并完成原创转译，文化/身份符号符合项目时代、地域、阶层、职业和禁区；prompt evidence chain 可追溯；`## 4. 解构` 下的主体 ID、`## 5. 提示词设计` 的主体 ID 和英文 prompt 开头三者一致；英文 prompt 以主体 ID 号开头，融合 `画面基调.Global Style Prompt + 道具风格.Prop Style Prompt`，整合 `## 4. 解构` 全部有效信息，使用自然语言负向约束且不含 `--no`，不超过 1300 characters；画面固定为纯色背景完整全貌展示、45 度视角，完整展示道具全貌、完整轮廓与主要结构，仅展示道具，不做局部特写、裁切特写或半截道具画面，不置身具体场景，不出现人物或背景元素。 |
