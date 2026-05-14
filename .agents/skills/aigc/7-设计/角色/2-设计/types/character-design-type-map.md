# Character Design Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `角色/2-设计` 的类型变量和分型策略。它不替代 `steps/` 的执行流程。

## Type Variables

| variable | values | use |
| --- | --- | --- |
| `character_scope` | `lead` / `supporting` / `episodic` / `group` | 决定研究、物语和细节密度 |
| `evidence_quality` | `strong` / `partial` / `thin` | 决定是否需要风险提示或上游修复建议 |
| `research_need` | `none` / `light` / `web_allowed` | 决定是否允许网络搜索 |
| `research_depth` | `anchor_only` / `profile` / `craft_deep` / `cross_checked` | 决定研究层从清单锚点到工艺考据的深度 |
| `uncertainty_level` | `low` / `medium` / `high` | 决定是否必须写待确认项、风险提示或上游修复建议 |
| `costume_complexity` | `plain` / `period` / `ritual` / `uniform` / `fantasy` / `hybrid` | 决定服装字段重点 |
| `cultural_specificity` | `generic` / `regional` / `historical` / `ethnic_or_religious` / `institutional` | 决定地域年代、礼制、职业制服和禁区审查强度 |
| `body_posture_risk` | `low` / `medium` / `high` | 决定姿态是否需要避免性化、伤病误写、刻板化或场景动作 |
| `cinematic_role` | `heroic` / `intimate` / `threat` / `comic` / `background_anchor` / `mystery` | 决定摄影字段语言 |

## Strategy Matrix

| type_profile | route | design emphasis | review risk |
| --- | --- | --- | --- |
| `lead + strong` | 完整研究、物语、视觉服装、摄影 | 角色矛盾、长期视觉识别、跨场景一致性 | 避免过度百科化 |
| `supporting + strong/partial` | 中等篇幅设计 | 与主线关系、单一强视觉钩子、服装功能 | 避免主角化 |
| `episodic + partial/thin` | 短稿但字段齐全 | 首次登场辨识度、动作功能、镜头记忆点 | 避免凭空补复杂背景 |
| `group` | 群像主体设计 | 群体轮廓、统一服装系统、个体差异规则 | 避免假装每个个体都有姓名 |
| `period/ritual/uniform` costume | 允许轻量或网络考据 | 廓形、材质、礼制、磨损和职业功能 | 避免历史/文化误写 |
| `thin evidence` | 先降深度 | 明确哪些来自清单，哪些是设计推演 | 必须标记低证据风险 |
| `regional/historical/institutional` specificity | 研究层升级为 `craft_deep` 或 `cross_checked` | 地域年代、制度身份、职业服制、禁区和不确定性 | 避免把现代泛化审美套进特定文化 |
| `high uncertainty + high specificity` | 降低断言强度，必要时请求确认 | 写清清单事实、推演和待确认项 | 不得把低证据考据写成事实 |

## Routing Map

```mermaid
flowchart TD
    A["清单角色行"] --> B{"character_scope"}
    B -->|"lead"| C["完整研究与长期识别"]
    B -->|"supporting"| D["中等篇幅与关系钩子"]
    B -->|"episodic"| E["短稿但字段齐全"]
    B -->|"group"| F["群体系统与变体规则"]
    C --> G{"evidence_quality"}
    D --> G
    E --> G
    F --> G
    G -->|"strong / partial"| H["进入 LLM-first 设计"]
    G -->|"thin"| I["降深度并标记低证据风险"]
    H --> R{"research_depth / specificity"}
    I --> R
    R --> J{"costume_complexity"}
    J -->|"period / ritual / uniform / hybrid"| K["允许轻量或网络考据"]
    J -->|"plain / fantasy"| L["使用项目上下文与设计判断"]
    K --> M["type_profile"]
    L --> M
    M --> N["steps/character-design-workflow.md"]
```

## Web Search Routing

| condition | allowed_action | required_record |
| --- | --- | --- |
| 冷门服饰、职业或地域 | 搜索 1 到 3 个可信来源 | 来源名称、链接或摘要、使用边界 |
| 真实历史人物或事件影射 | 搜索并交叉核对 | 不把单一来源写成事实 |
| 普通现代日常角色 | 默认不搜索 | 直接用项目上下文设计 |

## Research Depth Rules

| profile signal | research_depth | required output |
| --- | --- | --- |
| 配角、普通现代、证据强、服装简单 | `profile` | 完成八个研究镜头，但每镜头可短写；必须有 prompt evidence chain |
| 主角、阶层压力强、职业身份强 | `profile` 或 `craft_deep` | 职业、阶层、身体姿态和服装工艺必须转化为可见设计 |
| 年代、地域、制服、礼仪、宗教、民族或真实制度相关 | `craft_deep` 或 `cross_checked` | 地域年代、工艺、禁区和不确定性必须详写；必要时允许搜索 |
| 清单证据薄但用户要求输出 | `anchor_only` | 只做低断言推演，明确待确认项；不得虚构复杂背景 |

## Prompt Evidence Chain Rules

- 英文 prompt 中的身份、服装、姿态、光线、风格与固定画面短语，都应能回指到 `research_profile` 或项目上下文。
- 不允许出现研究层没有支持的特定文化符号、真实制服、宗教标识、医学特征或阶层标签。
- `full-body costume fitting photo`、`solid color background`、`no scene environment` 是固定证据，来自本技能合同，不需要外部来源。

## Depth Rules

- 所有类型都必须保留模板必填字段。
- 低证据角色可以短，但不能缺字段。
- 主角与高复杂服装角色必须在 `Detailed Costume Design` 中写到材质、层次、配件和使用痕迹。
- 群像角色的提示词应强调群体系统和可重复变体，不虚构具体姓名。
- 任何类型都必须输出研究层八个镜头；差异只在深度，不在字段是否存在。
