# {{道具名称}}

source_prop_list: `projects/aigc/<项目名>/7-设计/道具/1-清单/道具清单.md`
source_north_star: `projects/aigc/<项目名>/0-初始化/north_star.yaml`
source_team: `projects/aigc/<项目名>/team.yaml`

## 固定画面约束

- Type: close-up single prop shot
- Camera Angle: 45-degree view
- Framing: full prop in view, entire prop fully visible, prop only
- Background: solid color background only, no background elements
- Scene Placement: no scene environment, no tabletop scene, no room set, no street, no hands holding the prop, no people
- Prompt Must Include: `close-up prop shot, 45-degree view, full prop in view, prop only, solid color background, no people, no background elements, no scene environment`

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据

{{结合 north_star.yaml 中的世界观，思考当前道具符合叙事的文化属性和具象特征；若涉及冷门信息点且本地资料不足，可启用网络搜索并记录来源或不确定性。研究必须转译为可见设计，不写不能改变形制、材料、工艺、年代、使用痕迹、功能逻辑或 prompt token 的百科段落。}}

### 研究证据链

| source cue | confidence | visual translation | design lock / allow variation | prompt evidence token |
| --- | --- | --- | --- | --- |
| {{清单 / north_star / team / MEMORY / CONTEXT / source_fact / inference / inspired_by / unknown}} | {{confirmed / probable / inferred / uncertain；说明风险或缺口}} | {{形制 / 材料 / 工艺 / 年代 / 使用痕迹 / 功能逻辑 / 风险不确定性}} | {{必须锁定的识别点；允许变化的细节}} | {{英文 prompt 中可追溯的短 token}} |

### 研究转译清单

- 形制：{{轮廓、比例、开口、接口、可动件、携带/存放逻辑；不得要求手或人物入镜}}
- 材料：{{主材、副材、表面处理、反光/吸光、重量感}}
- 工艺：{{铸造、锻打、漆面、雕刻、缝制、拼接、修补等可见工艺痕迹}}
- 年代：{{时代、地域、技术阶段或世界观层级如何影响造型；不确定则写 inspired by}}
- 使用痕迹：{{磨损、划痕、污渍、氧化、包浆、折痕、修补、损伤}}
- 功能逻辑：{{道具如何被识别、开启、储存、误用或象征性使用；只写可见逻辑，不写操作教程}}
- 风险/不确定性：{{事实缺口、冷门考据、文化误读、危险用途、生成歧义和保守表达方案}}

## 3. 物语

{{结合以上内容展开散文式、诗意化的道具描述，说明物件的功能、主人痕迹、时间沉积、象征压力和视觉记忆点。}}

## 4. 解构

主体ID号：{{道具主体 ID；必须与 5. 提示词设计中的主体 ID 号和英文 prompt 开头完全一致}}

## Photography

Type: close-up single prop shot
Shot Size: close-up
Camera Angle: 45-degree view
Framing: full prop in view, entire prop fully visible, prop only
Background: solid color background only, no background elements
Scene Placement: no scene environment, no hands holding the prop, no people

## Prop Design

Style Backbone: {{style_backbone}}
Prop Type: {{prop_type_en}}
Design Inspiration: {{design_inspiration_en}}
Period Attribute: {{period_attribute_en}}
Functionality: {{functionality_en}}
Evidence Logic: {{how_research_translates_into_shape_material_craft_period_wear_function_en}}

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

## 5. 提示词设计

- 全局风格提示词引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“全局风格提示词”}}
- 物品风格引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“物品风格”}}
- 主体 ID 号：{{道具主体 ID；若上游清单已有 ID 则原样沿用，否则使用清单行/安全文件名派生的 ASCII ID}}
- 固定画面约束：close-up prop shot, 45-degree view, full prop in view, prop only, solid color background, no people, no background elements, no scene environment

### Prompt Evidence Chain

| prompt token | evidence source | reason |
| --- | --- | --- |
| {{主体 ID 号 prefix}} | {{道具清单主体 ID / source_row / 安全文件名}} | {{英文 prompt 必须以该主体 ID 号开头}} |
| {{single prop subject token}} | {{名称 / 原文描述 / Prop Design}} | {{锁定单道具主体}} |
| {{form / material / craft / period / wear / function token}} | {{研究证据链对应行}} | {{说明该 token 如何来自研究转译}} |
| deconstruction_coverage | {{## 4. 解构 / Photography / Prop Design}} | {{说明 Photography 与 Prop Design 的全部有效镜头、形制、材质、工艺、年代、磨损、功能和尺度槽位如何被整合进英文 prompt；若压缩、合并或剔除，写明理由}} |
| `close-up prop shot, 45-degree view, full prop in view, prop only, solid color background, no people, no background elements, no scene environment` | 固定画面约束 | 锁定完整展示道具全貌、仅展示道具、纯色背景单道具 45 度近景，不置身场景，不出现人物或背景元素 |

```text
{{英文整合提示词必须以主体 ID 号开头，格式为 "<主体ID>: ..."; 整合对象是 4. 解构的全部有效信息，而不是只拼接主体 ID、全局风格、物品风格、固定画面词和负向词；必须把 Photography 与 Prop Design 中的镜头距离、45 度角度、完整展示、形制、线条、体积、材料、纹理、装饰、年代、磨损、功能逻辑和固定画面约束蒸馏组织为自然流畅、可生成画面的英文整合提示词，1300 characters 以内；必须包含 close-up prop shot / 45-degree view / full prop in view / prop only / solid color background / no people / no background elements / no scene environment，并以自然语言写入 avoid people, hands, character, model, body parts, tabletop scene, room set, street, landscape, props cluster, background elements, cropped prop, partial prop 等负向约束，不得使用 --no。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{道具清单中的名称}}"
prompt_character_count: 0
research_chain_status: pending
prompt_evidence_chain_status: pending
reviewer: ""
subagent_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个道具主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究证据链、物语、完整 Photography + Prop Design 解构、提示词设计。 |
| Output format | Markdown 单道具设计稿；`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`，再写固定解构字段 `Photography` 与 `Prop Design`；英文 prompt 放入 fenced text block。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/7-设计/道具/2-设计/PROP-###-<安全文件名>.md`；若上游已有主体 ID，则用该 ID 替代 `PROP-###`。 |
| Naming convention | 默认使用 `<主体ID>-<安全文件名>.md`；主体 ID 默认从 `PROP-001` 起按清单顺序补零；同名或多状态道具在安全文件名后追加首次登场 ID 或状态。 |
| Completion gate | 道具来自上游清单；已消费 `north_star.yaml` 与 `team.yaml`；正文由 LLM 创作；研究已转译为形制/材料/工艺/年代/使用痕迹/功能逻辑/风险不确定性；prompt evidence chain 可追溯；`## 4. 解构` 下的主体 ID、`## 5. 提示词设计` 的主体 ID 和英文 prompt 开头三者一致；英文 prompt 以主体 ID 号开头，融合全局风格和物品风格，整合 `## 4. 解构` 全部有效信息，使用自然语言负向约束且不含 `--no`，不超过 1300 characters；画面固定为纯色背景近景特写、45 度视角，完整展示道具全貌，仅展示道具，不置身具体场景，不出现人物或背景元素。 |
