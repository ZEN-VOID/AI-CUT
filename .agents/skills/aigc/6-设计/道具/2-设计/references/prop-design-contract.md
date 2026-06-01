# Prop Design Contract

本文件定义 `道具/2-设计` 的业务细则。根 `SKILL.md` 拥有入口、路由和输出合同；本文件只展开单道具细目设计规则。

## Upstream Contract

必须消费：

- `projects/aigc/<项目名>/6-设计/道具/1-清单/道具清单.md`
- `projects/aigc/<项目名>/0-初始化/north_star.yaml`
- `projects/aigc/<项目名>/team.yaml`

可按需消费：

- `projects/aigc/<项目名>/MEMORY.md`
- `projects/aigc/<项目名>/CONTEXT/`
- 上游首次登场对应的分组稿或分镜稿，仅用于回查原文证据，不用于新增清单外道具。

## LLM-First Creative Authorship

- 研究考据、物语、解构、物品风格和英文 prompt 必须由 LLM 直接创作与裁决。
- 脚本不得通过模板拼接、启发式补句、字段扩写或规则生成来冒充道具设计正文。
- 脚本可以读取清单、枚举项目路径、检查 Markdown 标题、统计 prompt 字符数、生成空目录或报告缺字段。

## Required Design Sections

每个单道具 Markdown 文件必须包含以下章节：

| section | required content |
| --- | --- |
| `名称 / 首次登场 / 原文描述复述` | 清单项名称、首次登场、对上游原文描述的短复述；不得改写成新事实 |
| `研究考据` | 与道具形制、材质、工艺、年代、文化来源或功能逻辑有关的考据；必须附研究证据链，冷门信息可网络搜索 |
| `物语` | 道具在故事中的压力、象征、拥有者痕迹、使用历史或情绪功能 |
| `解构` | `## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`，再至少包含 `Photography` 和 `Prop Design` 两个字段 |
| `提示词设计` | 引用全局风格提示词、补充物品风格，列出 prompt evidence chain，并给出英文 prompt，整合 `## 4. 解构` 全部有效信息，使用自然语言负向约束，不使用 `--no`，1300 characters 内 |

## Fixed Visual Constraint

- 道具设计稿默认是纯色背景上的单道具完整全貌展示，用于锁定物件整体形制、完整轮廓、主要结构、材质和识别点；不得默认做局部特写。
- 默认摄影为 full-view prop shot、45-degree view、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、solid color background。
- 必须完整展示道具全貌、完整轮廓和主要结构，仅展示道具本体；不得写成局部特写、裁切特写、半截道具画面，也不得让道具置身于剧情场景、桌面环境、室内陈设、街景、人物手持情境、多物件场景或任何背景元素中。
- 若道具的使用方式需要说明，只能在 `物语` 或 `Prop Design` 中解释，不得让最终画面出现手、角色或场景。

## Design Source Map

```mermaid
flowchart TD
    A["道具清单项"] --> B["来源复述与单主体边界"]
    C["north_star.yaml"] --> D["全局风格 / 主题 / 禁区"]
    E["team.yaml"] --> F["设计相关大师监制上下文"]
    G["MEMORY.md / CONTEXT/"] --> H["项目长期偏好与共享事实"]
    B --> I["LLM-first 道具设计判断"]
    D --> I
    F --> I
    H --> I
    I --> J["研究考据"]
    I --> K["物语"]
    I --> L["Photography"]
    I --> M["Prop Design"]
    J --> N["英文生成 prompt"]
    K --> N
    L --> N
    M --> N
    N --> O["单道具细目 Markdown"]
```

```mermaid
flowchart LR
    A["脚本可做: 读取 / 枚举 / 检查 / 统计"] --> B["机械辅助证据"]
    C["脚本禁止: 研究 / 物语 / 解构 / prompt 主创"] --> D["必须回到 LLM"]
    B --> E["LLM 裁决与创作"]
    D --> E
    E --> F["review gate"]
```

## Research Rules

- 研究必须服务可见设计，不写与造型和拍摄无关的百科段落。
- 每条研究结论必须落到至少一个可见或可生成字段：形制、材料、工艺、年代、使用痕迹、功能逻辑、风险/不确定性、prompt evidence token。
- 研究证据链应区分 `source_fact`、`inference`、`inspired_by` 与 `unknown`：确定事实可直接锁定，推断和灵感只能作为设计方向，不得伪装成上游事实。
- 研究输出优先使用短表格或短条目，避免长段抄写；每条最好能回答“它改变了哪个形状、材料、工艺、磨损、年代或 prompt token”。
- 冷门信息允许网络搜索的条件：用户明确要求考据、项目题材依赖真实历史/工艺/地域信息、或 LLM 对事实置信度不足。
- 使用网络搜索时应优先可靠来源，并在输出中用简短来源说明或“不确定性注记”标识，不长篇摘录。
- 若无法验证冷门信息，设计可使用“受某类工艺启发”的措辞，避免伪造具体史实。
- 与现实危险物、医疗器械、武器或违法用途相关的研究只能转译为外观和叙事安全描述，不得提供可执行制造、使用或伤害步骤。

## Research Evidence Chain Contract

研究层必须形成如下最小链路：

```text
source cue -> confidence -> visual translation -> design lock -> prompt evidence token
```

| chain slot | required decision |
| --- | --- |
| `source cue` | 来自清单、north_star、team、项目记忆、项目 CONTEXT、本地知识或网络来源的哪一类证据 |
| `confidence` | `confirmed` / `probable` / `inferred` / `uncertain`，并说明不确定性 |
| `visual translation` | 转成形制、材料、工艺、年代、使用痕迹、功能逻辑或安全边界 |
| `design lock` | 哪些特征必须固定，哪些允许生成时微变 |
| `prompt evidence token` | 最终英文 prompt 中应出现的紧凑 token 或短语 |

推荐研究覆盖面：

| research axis | output expectation |
| --- | --- |
| `form_factor` | 轮廓、比例、开口、接口、可动件、握持/携带方式；不得加入手或场景入镜 |
| `material_system` | 主材、副材、表面处理、反光/吸光、透明度、重量感 |
| `craft_process` | 手作、铸造、锻打、漆面、缝制、雕刻、磨蚀、拼接等可见工艺痕迹 |
| `period_logic` | 年代、地域、技术水平或世界观阶段如何改变形制与装饰 |
| `wear_trace` | 划痕、磨损、污渍、修补、包浆、断裂、氧化等叙事痕迹 |
| `function_logic` | 道具如何被使用、储存、开启、识别或误用；只写可见逻辑，不写操作教程 |
| `risk_uncertainty` | 事实缺口、文化误读、危险用途、生成歧义和需要保守表达的位置 |

## Prompt Evidence Chain Rules

- 英文 prompt 的关键名词、材质、年代、磨损、工艺、形制和禁止项，应能回指 `研究考据`、`物语` 或 `解构` 的字段。
- `prompt evidence chain` 不要求每个英文词都溯源，但必须覆盖会影响生成结果的核心 token。
- 若某 token 只是全局风格提示词的一部分，应标注 `global_style`；若来自物品风格，应标注 `item_style`。
- 不得为了塞入证据链而增加场景、人物、手持、桌面、房间或街景 token。

## North Star And Team Consumption

`north_star.yaml` 应转译为：

- 全局风格提示词或视觉母题。
- 主题、时代、材质、色彩、镜头、禁区。
- 该道具在项目整体美术系统中的位置。

`team.yaml` 应转译为：

- 与设计、摄影、美术、服装、动作、导演或审美有关的大师监制视角。
- 至少一条可见的设计决策，例如材质克制、形制陌生化、手作痕迹、可拍摄反光、握持方式或留白。
- 不把大师名字当装饰性标签；必须说明它如何改变道具方案。

## Deconstruction Rules

`Photography` 字段应回答：

- 镜头距离、角度、焦段感、景深、光线、反光、阴影、运动或静置状态。
- 道具在画面中如何被识别，如何用全貌构图、边缘光或轮廓隔离让整体结构可读。
- 默认固定为完整全貌展示、45 度视角、完整展示道具全貌与完整轮廓、仅展示道具、纯色背景；不得写成局部特写、裁切特写或半截道具画面，不得把人物、手、桌面、房间、街景、环境对照或背景元素写入默认画面，只能在文字中说明用途。

`Prop Design` 字段应回答：

- 外形轮廓、材质、工艺、颜色、尺度、重量感、使用痕迹、损伤、可动部件、接口、包装或携带方式。
- 哪些元素是生成时必须锁定的识别点，哪些可以随机变化。

## Prompt Rules

- prompt 必须为英文，最多 1300 characters。
- prompt 必须以主体 ID 号开头，格式为 `<主体ID>: ...`；主体 ID 来自上游清单、source row 或安全文件名派生的 ASCII ID。
- prompt 开头的主体 ID 必须与 `## 4. 解构` 下方 `主体ID号：<主体ID>` 和 `提示词设计` 中记录的主体 ID 完全一致。
- prompt 必须同时包含全局风格提示词引用和物品风格。
- 最终英文整合提示词的整合对象是 `## 4. 解构` 的全部有效信息，包括 `Photography` 与 `Prop Design` 中的全貌构图、45 度角度、完整轮廓、形制、线条、体积、材料、纹理、装饰、年代、磨损、功能逻辑、尺度和固定画面约束；不得只把主体 ID、全局风格、物品风格、固定画面词或负向词作为前缀/后缀拼接后宣布完成。
- prompt 应聚焦单个道具，避免把角色、场景或完整剧情塞入主体。
- prompt 必须包含 `full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background, no people, no background elements, no scene environment` 或等价约束。
- prompt 必须使用自然语言负向约束，例如 `avoid people, hands, character, model, body parts, tabletop scene, room set, street, landscape, props cluster, background elements, cropped prop, partial prop`，但不得压过主体设计；不得使用 Midjourney `--no` 参数。
- 若全局风格提示词缺失，必须写明 `Global style prompt: missing upstream source`，并只输出物品风格 prompt 草案。

## Non-Goals

- 不重新生成 `道具清单.md`。
- 不创建图像、视频或生成任务。
- 不修改角色、场景、父级路由、registry 或其他 worker 的文件。
- 不把多个道具合成一个并列总稿。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 设计稿是否消费 `道具清单.md`、`north_star.yaml`、`team.yaml`，并把项目 `MEMORY.md / CONTEXT/` 与首次登场分组稿只作为补充证据而非新增清单外道具？ | `GATE-PROP-DESIGN-01` / `GATE-PROP-DESIGN-04` | `FAIL-PROP-DESIGN-01` / `FAIL-PROP-DESIGN-04` | `N2-UPSTREAM` / `N3-SCOPE` | `upstream_manifest`、项目上下文清单、补充证据使用边界 |
| 每个 Markdown 是否只对应一个道具主体，没有并列多个道具、生成清单外主体或把上游冲突静默裁决为新 canonical 真源？ | `GATE-PROP-DESIGN-02` | `FAIL-PROP-DESIGN-02` | `N3-SCOPE` | `prop_worklist`、单主体边界说明、上游修复建议 |
| 研究考据、物语、解构、物品风格和英文 prompt 是否由 LLM 直接创作与裁决，脚本只做读取、枚举、检查、统计、空目录或缺字段报告？ | `GATE-PROP-DESIGN-05` | `FAIL-SCRIPT-AUTHORSHIP` | `N6-DESIGN` | 脚本职责清单、LLM 主创声明、正文生成来源说明 |
| 设计稿是否包含 `名称 / 首次登场 / 原文描述复述`、`研究考据`、`物语`、`解构`、`提示词设计` 五个必填章节，且复述未改写为新事实？ | `GATE-PROP-DESIGN-03` | `FAIL-PROP-DESIGN-03` | `N6-DESIGN` | 模板块覆盖检查、上游复述对照、缺块 finding |
| 固定画面是否为纯色背景单道具完整全貌展示、45 度视角、完整展示道具全貌、完整轮廓和主要结构、仅展示道具本体，并排除局部特写、裁切特写、半截道具、人物、手持、桌面、室内、街景、多物件和背景元素？ | `GATE-PROP-DESIGN-08` | `FAIL-PROP-DESIGN-07` | `N6-DESIGN` | `Photography` 字段、英文 prompt 固定画面短语、禁用元素清单 |
| 研究是否服务可见设计，并把每条关键结论落到形制、材料、工艺、年代、使用痕迹、功能逻辑、风险/不确定性或 prompt evidence token？ | `GATE-PROP-DESIGN-09` | `FAIL-PROP-DESIGN-08` | `N5-RESEARCH-CHAIN` | research evidence chain、`visual translation`、`design lock`、prompt token |
| 研究证据链是否区分 `source_fact / inference / inspired_by / unknown` 与 `confirmed / probable / inferred / uncertain`，没有把低证据推断写成确定事实？ | `GATE-PROP-DESIGN-09` | `FAIL-PROP-DESIGN-08` | `N5-RESEARCH-CHAIN` | 来源姿态、置信度/不确定性标注、待确认项 |
| 冷门网络信息是否只在必要或用户许可时使用，并用可靠来源、简短来源说明或不确定性注记收束，避免长篇摘录或覆盖清单真源？ | `GATE-PROP-DESIGN-RESEARCH-SAFETY` | `FAIL-PROP-DESIGN-RESEARCH-SAFETY` | `N5-RESEARCH-CHAIN` | 搜索必要性、来源摘要、使用边界、不确定性注记 |
| 危险物、医疗器械、武器或违法用途相关研究是否只转译为外观和叙事安全描述，没有提供制造、使用或伤害步骤？ | `GATE-PROP-DESIGN-RESEARCH-SAFETY` | `FAIL-PROP-DESIGN-RESEARCH-SAFETY` | `N5-RESEARCH-CHAIN` | 安全转译记录、删除的操作性信息、风险注记 |
| `north_star.yaml` 是否转译为全局风格、主题、时代/材质/色彩/镜头禁区和项目美术位置；`team.yaml` 是否转译为至少一条可见设计决策，而不是大师名字装饰？ | `GATE-PROP-DESIGN-04` | `FAIL-PROP-DESIGN-04` | `N2-UPSTREAM` / `N5-RESEARCH-CHAIN` | `project_design_context`、init synthesis source、设计决策证据 |
| `Photography` 是否回答镜头距离、角度、焦段感、景深、光线、识别方式和默认固定画面；`Prop Design` 是否回答外形、材质、工艺、颜色、尺度、重量、使用痕迹和锁定/可变项？ | `GATE-PROP-DESIGN-03` / `GATE-PROP-DESIGN-08` | `FAIL-PROP-DESIGN-03` / `FAIL-PROP-DESIGN-07` | `N6-DESIGN` | `Photography` / `Prop Design` 双字段证据、锁定/可变项 |
| prompt 是否为英文、以 `<主体ID>: ...` 开头，并与 `## 4. 解构` 主体 ID、`提示词设计` 主体 ID 完全一致？ | `GATE-PROP-DESIGN-06` | `FAIL-PROP-DESIGN-05` | `N6-DESIGN` | 三处主体 ID 对照、prompt 开头检查 |
| prompt 是否同时包含全局风格提示词引用和物品风格，并整合 `## 4. 解构` 全部有效 Photography 与 Prop Design 信息，而不是前缀/后缀拼接？ | `GATE-PROP-DESIGN-06` / `GATE-PROP-DESIGN-10` | `FAIL-PROP-DESIGN-05` / `FAIL-PROP-DESIGN-09` | `N6-DESIGN` | prompt 字符数、解构槽位覆盖、`deconstruction_coverage` |
| prompt 是否包含 full-view prop shot、45-degree view、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、solid color background、no people、no background elements、no scene environment 等等价约束？ | `GATE-PROP-DESIGN-08` | `FAIL-PROP-DESIGN-07` | `N6-DESIGN` | fixed visual phrase 检查、prompt 约束位置 |
| prompt 是否使用自然语言负向约束，未使用 Midjourney `--no`，且不超过 1300 characters？ | `GATE-PROP-DESIGN-06` | `FAIL-PROP-DESIGN-05` | `N6-DESIGN` | prompt 字符数、自然语言负向约束文本、`--no` 检查 |
| prompt 关键名词、材质、年代、磨损、工艺、形制和禁止项是否能回指研究、物语、解构、`global_style` 或 `item_style`，且未为证据链新增场景、人物或手持 token？ | `GATE-PROP-DESIGN-10` | `FAIL-PROP-DESIGN-09` | `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `prompt_evidence_chain`、token 来源对照、禁用 token 检查 |
| 本文件的 Non-Goals 是否被执行：不重生成清单、不创建图像/视频/生成任务、不修改角色/场景/父级/registry/其他 worker 文件、不把多个道具合成总稿？ | `GATE-PROP-DESIGN-07` / `GATE-PROP-DESIGN-02` | `FAIL-PROP-DESIGN-06` / `FAIL-PROP-DESIGN-02` | `N8-WRITE` / `N3-SCOPE` | 改动文件清单、输出路径、越界项排除说明 |
