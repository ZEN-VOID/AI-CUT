# Prop Design Type Map

本文件承载 `道具/2-设计` 的类型变量和分型策略。执行时先形成 `type_profile`，再进入 `steps/prop-design-workflow.md`。

## Type Variables

| variable | values | use |
| --- | --- | --- |
| `narrative_weight` | `key_prop` / `support_prop` / `background_lock` | 决定物语和识别点密度 |
| `function_mode` | `ritual` / `tool` / `weapon` / `document` / `container` / `costume_adjacent` / `device` / `misc` | 决定研究和 Prop Design 重点 |
| `research_need` | `low` / `medium` / `high` | 决定是否允许网络搜索冷门信息 |
| `state_model` | `single_state` / `multi_state` / `damaged_or_transformed` | 决定命名和版本处理 |
| `style_pressure` | `realist` / `symbolic` / `surreal` / `period_specific` / `sci_fi_or_fantasy` | 决定全局风格与物品风格融合方式 |

## Routing Matrix

| type signal | route | required emphasis | review focus |
| --- | --- | --- | --- |
| 关键剧情道具、规则物、反复出现 | `key_prop` | 物语、识别点、生成锁定 | 是否可跨镜头稳定复现 |
| 普通功能道具 | `support_prop` | 材质、使用痕迹、功能逻辑 | 是否过度扩写剧情 |
| 背景但需要生成锁定 | `background_lock` | 轮廓和场景识别关系 | 是否仍为单道具主体 |
| 历史、宗教、工艺、地域冷门物件 | `research_high` | 考据来源、形制、工艺 | 是否伪造史实或无来源断言 |
| 武器、危险装置、医疗器械 | `safety_sensitive` | 视觉描述而非现实操作指导 | 是否包含可执行伤害步骤 |
| 多状态或损坏变形 | `multi_state` | 状态差异、同一主体识别点 | 文件命名是否清楚 |

## Routing Topology

```mermaid
flowchart TD
    A["单道具清单项"] --> B{"narrative_weight"}
    B -->|"key_prop"| C["强化物语 / 识别点 / 生成锁定"]
    B -->|"support_prop"| D["克制功能 / 材质 / 使用痕迹"]
    B -->|"background_lock"| E["轮廓 / 尺度 / 场景识别关系"]
    A --> F{"research_need"}
    F -->|"high"| G["允许可靠来源搜索并标注不确定性"]
    F -->|"low / medium"| H["本地上下文优先"]
    A --> I{"state_model"}
    I -->|"multi_state / damaged_or_transformed"| J["保留 base identity + 状态差异"]
    I -->|"single_state"| K["输出单一设计文件"]
    C --> L["type_profile"]
    D --> L
    E --> L
    G --> L
    H --> L
    J --> L
    K --> L
    L --> M["steps/prop-design-workflow.md:N5-DESIGN"]
```

## Prompt Strategy By Type

| route | prompt strategy |
| --- | --- |
| `key_prop` | 强化 unique silhouette、material memory、story wear、signature detail |
| `support_prop` | 保持紧凑，聚焦功能、材质、年代和手部互动 |
| `background_lock` | 降低戏剧性，明确尺度、位置关系和可识别轮廓 |
| `research_high` | 用 verified / inspired by 语言区分确定事实和灵感转译 |
| `safety_sensitive` | 避免操作教程、结构拆解到可复现伤害层级，只保留美术可见特征 |
| `multi_state` | prompt 中写清 base identity 与当前状态，不丢主体识别点 |

## Default Fallback

类型不确定时采用：

```yaml
narrative_weight: support_prop
function_mode: misc
research_need: medium
state_model: single_state
style_pressure: realist
```

并在输出中保守处理，不新增复杂机制或多状态版本。
