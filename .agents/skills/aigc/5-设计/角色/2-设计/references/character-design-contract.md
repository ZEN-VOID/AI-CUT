# Character Design Contract

本文件展开 `角色/2-设计` 的业务细则。入口、路由和最终输出路径仍以同目录 `SKILL.md` 为准。

## Upstream Consumption

- Canonical input: `projects/aigc/<项目名>/5-设计/角色/1-清单/角色清单.md`。
- Required columns: `名称`、`首次登场`、`原文描述（关键词式）`。
- 本技能只能为清单中存在的角色主体生成设计稿。
- 若清单存在同名冲突、疑似漏项或角色归并错误，输出执行报告提出上游修复建议，不直接修改清单。

## Project Context Consumption

`north_star.yaml`:

- 抽取全局风格提示词、主题、时代/地域、影像气质、禁区和视觉约束。
- 若字段命名不统一，由 LLM 根据语义识别，但必须在执行报告中说明使用了哪些字段。
- 不得虚构不存在的全局风格提示词；缺失时写明“未提供明确全局风格提示词”，并从 north star 的主题描述中提炼临时工作口径。

`team.yaml`:

- 只消费与导演、美术、服装、摄影、角色设计、表演、动漫/漫画视觉相关的成员或大师上下文。
- 大师上下文是监制视角，不是文风模仿许可；输出应吸收其设计判断，而不是堆人名。
- 多个大师建议冲突时，以用户请求、项目 north star 和角色功能为裁决依据。

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
| `taboo_constraints` | 有哪些文化误读、项目禁区、年龄/性化、安全或版权风险？ | 写入 guardrails；prompt 必须避开禁区并保持定妆照约束 |
| `uncertainty` | 哪些信息来自清单，哪些来自推演，哪些需要考据或用户确认？ | 在 `Uncertainty Notes` 标注置信度，不把低证据推演写成事实 |
| `prompt_evidence_chain` | prompt 中每个关键主体、服装、姿态、光线、风格短语来自哪里？ | 生成 `Prompt Evidence Chain`，确保英文 prompt 可回指研究与项目风格 |

### Evidence Rules

- 每个研究镜头至少输出一个 `design implication`；没有设计转化的资料不得进入最终稿。
- `Prompt Evidence Chain` 必须按 `evidence -> design decision -> prompt phrase` 写清，覆盖身份、服装、姿态、摄影、全局风格和固定画面约束。
- 若证据薄弱，使用 `likely`、`inferred`、`open question` 等标记；中文稿中必须写明“推演”或“待确认”，不得伪装成清单事实。
- 研究层可以参考外部资料，但 canonical 判断仍由 LLM 综合项目上下文完成；外部资料不能覆盖 `north_star.yaml`、用户禁区或清单锚点。
- 服饰工艺必须服务角色身份与身体动作，不得只写品牌、潮流词或抽象审美。
- 身体姿态必须服务纯色背景全身定妆照：允许写站姿、重心、手部位置和头颈角度，不得引入剧情场景或环境动作。

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

`提示词设计`:

- 使用英文。
- 开头必须包含主体 ID 号，格式为 `<主体ID>: ...`；主体 ID 来自上游清单、source row 或角色安全名派生的 ASCII ID。
- 英文 prompt 开头的主体 ID 必须与 `## 4. 解构` 下方 `主体ID号：<主体ID>` 完全一致。
- 引用或融合全局风格提示词。
- 明确包含服装风格。
- 最终英文整合提示词的整合对象是 `## 4. 解构` 的全部有效信息，包括 `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography` 中的身份压力、视觉钩子、面部/发型/身体、服装廓形与材质、姿态、构图、光线和固定画面约束；不得只把主体 ID、全局风格、服装风格、定妆照词或负向词作为前缀/后缀拼接后宣布完成。
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
