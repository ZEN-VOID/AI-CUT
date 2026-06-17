# Scene Design Contract

本文件展开 `$aigc-scene-design` 的业务细则。它不拥有入口路由权；入口、输出路径和完成门禁以同目录 `SKILL.md` 为准。

## Source Contract

| source | required use | must not do |
| --- | --- | --- |
| `3-主体/场景/1-清单/场景清单.md` | 作为场景主体、首次登场和原文关键词的唯一上游清单真源 | 新增未在清单出现的主体 |
| `2-美学/类型风格.md` | 提取类型元素、媒介属性和下游 handoff 边界 | 替代细目场景风格协议或单场景设计判断 |
| `2-美学/画面基调/全局风格协议.md` | 提取 `Global Style Prompt`、`Visual Gene Profile`、`Negative Traits` 等画面基调最终内容 | 被单场景擅自改写，或被项目记忆/旧初始化风格载体替代 |
| 当前集优先/项目级回退的 `2-美学/场景风格/场景风格协议.md` | 提取 `Scene Style Prompt`、空间/建筑/材质/地域时间风格等场景风格最终内容；能推断 `第N集` 时先读 `2-美学/第N集/场景风格/场景风格协议.md` | 被单场景擅自改写，被项目记忆/旧初始化风格载体替代，或未记录 fallback |
| `MEMORY.md` / `CONTEXT/` | 读取项目长期偏好、初始化用户要求、资料吸收摘要、禁区和共享事实 | 写入跨项目经验、技能规则或冒充最终风格提示词真源 |
| 用户补充资料 | 承接本轮特殊约束 | 覆盖更高优先级禁区，除非用户明确纠偏 |

## LLM-First Authorship

- 研究考据、物语、Scene Design、Cinematography 和英文提示词必须由 LLM 直接创作。
- `research_brief`、`source_posture`、`uncertainty_register`、`visual_translation` 与 `prompt_evidence_chain` 也属于核心研究/设计判断，必须由 LLM 直接完成。
- 脚本可以检查 Markdown 标题、字段缺失、输出路径、文件名非法字符和英文提示词长度。
- 脚本不得用模板拼接、规则扩写、关键词替换或模型外启发式生成核心正文、研究结论、来源姿态、视觉翻译或提示词证据链。
- 若使用网络搜索，只能作为 LLM 研究证据的来源之一；搜索结果不得被脚本无审美判断地直接灌入正文。

## Fixed Visual Constraint

- 场景设计稿默认是纯空镜空间设计，服务场景资产与空间氛围锁定。
- 不得出现人物、人体局部、剪影、倒影、人群、背影或任何可识别人类存在。
- `Cinematography` 可以描述动线和镜头可达点，但画面最终必须为空镜，不安排人物入画。
- 英文 prompt 必须包含 `empty shot, no people, no human figures` 或等价约束。

## Content Requirements

### 名称 / 首次登场 / 原文描述复述

- `名称` 使用上游清单 canonical 场景名。
- `首次登场` 保留上游清单值。
- `原文描述复述` 将上游 `原文描述（关键词式）` 转为短段，保留证据口径，不新增剧情事件。

### 研究考据 / Research Brief

研究层必须先产出可传递的 `research_brief`，再进入物语、解构和提示词。它不是百科段落，也不是给 prompt 堆名词，而是把来源、判断、不确定性和可见画面翻译成同一个证据链。

`research_brief` 至少包含：

| artifact | requirement |
| --- | --- |
| `research_questions` | 2-5 个会影响空间形制、材质、光线、仪式、时代或地域可信度的问题 |
| `source_posture` | 标注每个关键判断来自 `project_source`、`user_source`、`common_knowledge`、`scene_inference`、`web_source` 或 `unresolved` |
| `evidence_matrix` | 每条来源事实/推断必须说明设计影响，不写与画面无关的资料 |
| `uncertainty_register` | 对年代、地域、建筑制式、文化符号、材质、自然地理等不确定处标注风险和处理方式 |
| `visual_translation` | 将研究判断翻译为可见的空间结构、材料、色彩、光源、陈设、构图或空镜限制 |

研究应按场景类型选择重点：

- 现实建筑：地域、年代、结构、材料、使用功能、社会阶层痕迹。
- 城市街区：街道尺度、招牌、交通、时代标识、公共/私密边界。
- 室内空间：平面布局、家具、物件密度、光源、生活痕迹。
- 自然地貌：地形、植被、水体、气候、季节、可拍摄路径。
- 仪式/宗教/民俗空间：符号、禁忌、材料、动线和观看关系。
- 超现实/异化空间：现实锚点、变形规则、物理边界、视觉逻辑。

冷门信息允许网络搜索的条件：

- 本地项目资料不足，且信息会影响建筑、地域、材质、服饰/陈设或仪式空间。
- 用户未禁止联网。
- 输出中必须区分“来源事实”“合理推断”和“创作性设计选择”。

来源姿态规则：

- `project_source`：来自 `场景清单.md`、`2-美学` 输出、项目 `MEMORY.md` 或项目 `CONTEXT/`，可作为强约束。
- `user_source`：来自用户本轮明确补充，优先级高但仍受根禁区和纯空镜约束限制。
- `common_knowledge`：通用历史、建筑、自然或摄影常识；只能支撑低风险判断，不得伪装成精确出处。
- `scene_inference`：LLM 基于场景名、关键词、母题和类型画像作出的设计推断，必须标注为推断。
- `web_source`：联网或外部资料来源，只摘取会影响设计的事实，不复制长文。
- `unresolved`：无法确认的信息，必须进入 `uncertainty_register`，在视觉上采用保守、可替换或非特指方案。

不确定性处理规则：

- 不确定性不等于缺陷；缺陷是把不确定信息写成确定事实。
- 高风险文化符号、宗教/民俗元素、具体年代制式、地域建筑细部，若没有可靠来源，应降级为“受其启发的非特指设计”。
- prompt 中不得出现未被证据链支撑的具体朝代、族群、宗教、地点或建筑大师名。
- 无法确认但仍要表现氛围时，用材质、比例、光线、磨损、空间边界等可见设计语言承接，不用事实断言承接。

视觉翻译规则：

- 每条关键研究判断必须至少落到一个可见维度：空间结构、材料、表面老化、色彩、光源、尺度、边界、陈设密度、标识系统、地形/水体/植被、构图或镜头限制。
- 视觉翻译必须服务纯空镜；不得通过人物、人体痕迹、影子、倒影、人群尺度参照来证明研究结论。
- 若研究判断不能影响可见空间或 prompt token，应移出正文或降为备注。

### 物语

`物语` 回答空间在故事中的叙事功能：

- 它压迫、保护、诱惑、隔离、揭示或误导角色感知的方式，但不让角色出现在画面中。
- 它如何承接项目母题、角色关系和“人不在场”的空间痕迹。
- 它的历史痕迹或社会气味如何服务情绪。
- 它不应写成新的剧情段落，不应替代剧本。

### 解构

`Scene Design` 字段至少覆盖：

- 空间结构与边界
- 建筑/空间风格
- 材质与表面
- 色彩与光源逻辑
- 陈设/道具密度
- 空间动线与镜头可达点
- 可制作资产提示

`Cinematography` 字段至少覆盖：

- 构图策略
- 镜头距离与焦段倾向
- 机位高度与运动方式
- 光线方向、对比度与色温
- 景深、遮挡、前中后景关系
- 情绪节奏与拍摄禁忌

### 提示词设计

- 必须记录 `画面基调引用`，来自 `2-美学/画面基调/全局风格协议.md` 的 `Global Style Prompt` 或用户明确覆盖说明。
- 必须记录 `场景风格引用`，来自当前集优先/项目级回退的 `2-美学/场景风格/场景风格协议.md` 的 `Scene Style Prompt`、`2-美学/类型风格.md`、`type_profile`、场景设计判断、项目 `MEMORY.md` 或用户明确补充。
- 必须记录 `时间与地域引用`，来自 `research_brief`、`type_profile`、上游清单、项目资料或用户明确补充；若具体年代或地域无法确认，必须写成有来源姿态的保守英文锚点，例如 `non-specific 16th-century East Asian maritime setting`，不得省略，也不得编造具体年份、国家、城市、族群、宗教或建筑流派。
- 必须记录 `prompt_evidence_chain`，将英文 prompt 的关键 token 组回指到 `research_brief`、`visual_translation`、`Scene Design` 或 `Cinematography`。
- `## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`；该值必须与 `提示词设计` 的主体 ID 字段和英文 prompt 前缀一致。
- `English prompt` 必须为英文，面向图像生成，开头必须包含主体 ID 号，格式为 `<主体ID>: ...`，长度不超过 2000 characters。
- 英文提示词应描述可见空间、材质、光线、构图和摄影语言；避免中文、解释性段落和不可见抽象口号。
- 最终英文整合提示词的整合对象是 `## 4. 解构` 的全部有效信息，包括 `Scene Design` 与 `Cinematography` 的空间结构、尺度、边界、材质、表面、色彩、陈设、动线、镜头距离、构图、光线、焦段、景深、运动和氛围节奏；不得只把主体 ID、画面基调、场景风格、时间地域或 pure empty shot 作为前缀/后缀拼接后宣布完成。
- 若某个解构槽位因不可见、重复、互相冲突或不适合图像提示词而未进入英文 prompt，必须在 `prompt_evidence_chain` 中标注取舍理由；未标注的遗漏视为整合不完整。
- 最终英文整合提示词必须显式包含时间和地域 token；时间可为具体年份、世纪、时代或保守时代锚点，地域可为具体地名、文化地理区域、海域/岛屿/城市区域或保守地域锚点，但二者都必须能通过 `prompt_evidence_chain` 回指来源姿态。低证据时必须使用 `non-specific`、`project-era-consistent`、`inferred coastal / mountain / urban region` 等保守表达。
- 最终英文整合提示词还必须包含按 `scene_type` 选择的空间风格 token：建筑、室内和城市街区可使用建筑/室内/街区风格；自然地貌使用地理、生态、季节或材质系统；超现实空间使用变形规则或尺度逻辑；交通/过渡空间使用路径、节点和材料逻辑。不得给自然、超现实、交通或抽象空间强行套建筑流派。
- 英文提示词必须明确为 pure empty shot，并排除 people、human figures、body parts、silhouettes 和 reflections of people。

`prompt_evidence_chain` 至少覆盖：

| chain node | must explain |
| --- | --- |
| `subject_id_prefix` | 主体 ID 号来自上游清单、文件名前缀或 structured input，如何同时写入 `## 4. 解构` 下方并作为 English prompt 开头 |
| `style_anchor` | `画面基调.Global Style Prompt + 场景风格.Scene Style Prompt` 如何进入 prompt |
| `period_region_tokens` | 时间与地域 token 来自哪条来源、推断或不确定性处理，如何在英文 prompt 中显式出现 |
| `space_style_token` | 建筑/室内/街区/自然地理/材质系统/超现实规则/交通空间 token 如何按 `scene_type` 选择，且没有强行建筑化 |
| `spatial_tokens` | 空间结构、尺度、边界和动线 token 来自哪条研究或设计判断 |
| `material_tokens` | 材质、表面、装饰、陈设 token 的来源姿态和不确定性处理 |
| `light_camera_tokens` | 光线、镜头、构图 token 如何承接 Cinematography |
| `deconstruction_coverage` | `## 4. 解构` 的 Scene Design 与 Cinematography 全部有效槽位如何进入英文 prompt；被压缩、合并或剔除的槽位必须说明原因 |
| `empty_shot_tokens` | `empty shot, no people, no human figures` 等纯空镜约束必须原样或等价出现 |

## 初始化综合消费 / Reviewer Path

在当前上层策略允许外部 provider 调度，且用户显式要求或仓库治理合同视为已授权时，默认拆成四个 reviewer 视角：

| reviewer | responsibility |
| --- | --- |
| `research-reviewer` | `research_brief`、来源姿态、不确定性、视觉翻译、地域/年代/建筑合理性 |
| `scene-design-reviewer` | 空间结构、材质、陈设和可制作性 |
| `cinematography-reviewer` | 镜头、光线、构图和摄影一致性 |
| `prompt-reviewer` | 英文提示词主体 ID 开头、画面基调、场景风格、时间与地域显式锚点、`prompt_evidence_chain` 和 2000 character gate |

若外部 reviewer provider 不可用或用户显式要求不用初始化综合消费，执行者直接使用本地等价 checklist；不得用本地 checklist 冒充 team 顾问问答。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否把 `3-主体/场景/1-清单/场景清单.md`、`2-美学/类型风格.md`、`2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/场景风格/场景风格协议.md`、项目 `MEMORY.md` / `CONTEXT/` 和用户补充资料分别按 Source Contract 的用途锁定，而不是让任一来源替代单场景设计判断？ | `GATE-SCENE-DESIGN-01` | `FAIL-SCENE-DESIGN-01` | `N2-SOURCES` | 报告记录 `input_manifest`、各来源路径、使用方式和任何缺失/降级/fallback 说明。 |
| 场景主体、首次登场和原文关键词是否只来自上游场景清单，且没有从剧情想象、研究资料或用户临时描述中新增清单外主体？ | `GATE-SCENE-DESIGN-02` | `FAIL-SCENE-DESIGN-02` | `N3-SELECT` | 留下目标主体、清单行号、`S###` 编号和未新增主体的判定证据。 |
| 研究考据、物语、Scene Design、Cinematography、英文 prompt、`source_posture`、`visual_translation` 与 `prompt_evidence_chain` 是否由 LLM 直接完成，脚本只做字段、路径、字符数等机械检查？ | `GATE-SCENE-DESIGN-07` | `FAIL-SCENE-DESIGN-07` | `N6-DESIGN` | 报告说明核心正文生成路径、脚本实际职责和是否存在模板拼接/规则扩写痕迹。 |
| 场景设计稿和英文 prompt 是否明确为纯空镜，并排除人物、人体局部、剪影、倒影、人群、背影或任何可识别人类存在？ | `GATE-SCENE-DESIGN-09` | `FAIL-SCENE-DESIGN-09` | `N6-DESIGN` | 留下摄影字段与 English prompt 中 `empty shot / no people / no human figures` 等约束位置，以及禁用项检查结果。 |
| `research_brief` 是否包含 2-5 个会影响空间形制、材质、光线、仪式、时代或地域可信度的问题，而不是百科式资料堆叠？ | `GATE-SCENE-DESIGN-03` | `FAIL-SCENE-DESIGN-03` | `N5-RESEARCH` | 报告列出 `research_questions`、对应设计影响和未服务画面的资料剔除情况。 |
| `source_posture` 是否逐项区分 `project_source`、`user_source`、`common_knowledge`、`scene_inference`、`web_source` 或 `unresolved`，并防止推断、常识或冷门信息伪装成确定事实？ | `GATE-SCENE-DESIGN-03` | `FAIL-SCENE-DESIGN-03` | `N5-RESEARCH` | 留下来源姿态表、高风险事实清单、推断/未解项和保守处理方式。 |
| `evidence_matrix` 与 `uncertainty_register` 是否把每条来源事实或推断转成设计影响，并对年代、地域、建筑制式、文化符号、材质或自然地理风险给出处理方式？ | `GATE-SCENE-DESIGN-03` | `FAIL-SCENE-DESIGN-03` | `N5-RESEARCH` | 报告记录 evidence matrix、uncertainty register、风险等级和视觉降级方案。 |
| `visual_translation` 是否把关键研究判断落到空间结构、材料、表面老化、色彩、光源、尺度、边界、陈设密度、地形/水体/植被、构图或镜头限制，而不是停留在抽象研究结论？ | `GATE-SCENE-DESIGN-03` | `FAIL-SCENE-DESIGN-03` | `N5-RESEARCH` | 留下研究判断到可见维度的映射表，以及不能转化为画面的剔除项。 |
| `物语` 是否解释空间如何压迫、保护、诱惑、隔离、揭示或误导感知，并承接项目母题与人不在场的空间痕迹，而不是新增剧情段落或替代剧本？ | `GATE-SCENE-DESIGN-04` | `FAIL-SCENE-DESIGN-04` | `N6-DESIGN` | 报告摘录 `物语` 的空间功能句、新增剧情风险和人物入画风险。 |
| `Scene Design` 是否覆盖空间结构与边界、按场景类型选择的建筑/空间/自然/材质风格、材质表面、色彩光源、陈设/道具密度、动线与镜头可达点、可制作资产提示？ | `GATE-SCENE-DESIGN-05` | `FAIL-SCENE-DESIGN-05` | `N6-DESIGN` | 留下 Scene Design 槽位覆盖表、`space_style_token` 来源、缺槽 finding 和修复后的段落位置。 |
| `Cinematography` 是否覆盖构图策略、镜头距离与焦段、机位高度与运动、光线方向/对比度/色温、景深遮挡和情绪节奏，且不把人物入画作为摄影依据？ | `GATE-SCENE-DESIGN-05` | `FAIL-SCENE-DESIGN-05` | `N6-DESIGN` | 留下 Cinematography 槽位覆盖表、空镜约束交叉检查和缺槽 finding。 |
| `提示词设计` 是否记录 `画面基调.Global Style Prompt`、`场景风格.Scene Style Prompt`、时间与地域引用，且时间/地域无法确认时采用有来源姿态的保守英文锚点而不是省略或编造；空间风格 token 是否按场景类型选择而非强行建筑化？ | `GATE-SCENE-DESIGN-06` | `FAIL-SCENE-DESIGN-06` | `N6-DESIGN` | 报告列出 visual tone anchor、scene style、period token、region token、space_style_token 与来源姿态。 |
| `## 4. 解构` 下的 `主体ID号`、`## 5. 提示词设计` 主体 ID 和 English prompt 前缀是否三处一致，且 prompt 为英文、以 `<主体ID>: ...` 开头并不超过 2000 characters？ | `GATE-SCENE-DESIGN-05` | `FAIL-SCENE-DESIGN-05` | `N6-DESIGN` | 留下三处 ID 比对、prompt 开头、语言检查和字符数。 |
| English prompt 是否真正整合 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息，并在 `prompt_evidence_chain` 中解释关键 token、被压缩/合并/剔除槽位和 pure empty shot 约束？ | `GATE-SCENE-DESIGN-10` | `FAIL-SCENE-DESIGN-10` | `N6-DESIGN` | 提供 prompt token evidence、`deconstruction_coverage`、未覆盖槽位和 empty-shot token 证据。 |
| 默认 reviewer 路径启用时，是否按四个 reviewer 视角检查 research、scene design、cinematography 与 prompt；provider 不可用或用户禁用时是否切换为本地等价 checklist？ | `GATE-SCENE-DESIGN-12` | `FAIL-SCENE-DESIGN-WORKFLOW` | `N7-REVIEW` | 报告记录 reviewer 路径、外部 provider 状态、本地 checklist、未启动 reviewer 和汇流裁决。 |
