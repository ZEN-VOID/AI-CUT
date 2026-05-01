# Review Contract

本文件定义 `角色/2-设计` 的质量门禁、subagent 汇流审查和验收输出。

## Default Reviewer Path

- 默认启用真实 subagents / reviewers。
- 默认顾问路径按 `../../../_shared/team-advisor-consultation-contract.md` 执行：先从项目 `team.yaml` 解析监制 roster，请教角色/服装/美术/摄影/导演相关顾问，形成 `advisor_consultation_packet` 后再进入设计稿汇流。
- 推荐 reviewer：`character-research-reviewer`、`visual-costume-reviewer`、`cinematography-reviewer`、`prompt-length-reviewer`。
- 若当前环境无真实 subagent 工具，主 agent 必须报告工具层阻断，并采用本地顺序 checklist 作为降级 review；不得把降级说成真实并行执行。

## Review Dimensions

| dimension | checks |
| --- | --- |
| upstream_anchor | 角色名称、首次登场、原文描述复述是否来自 `角色清单.md` |
| project_context | 是否读取并体现 `north_star.yaml` 和 `team.yaml` 的相关设计上下文 |
| research_layer | 研究是否转化为身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性和 prompt evidence chain |
| llm_first | 研究、物语、解构和提示词是否由 LLM 直接完成，脚本未替代主创 |
| required_sections | 是否包含研究考据、物语、解构、提示词设计 |
| decomposition | `## 4. 解构` 下方是否先写 `主体ID号：<主体ID>`；五个解构字段是否齐全且内容不互相串位 |
| output_naming | 文件名是否为 `<主体ID>-<角色名>.md`，且文件名前缀与解构主体 ID、提示词设计主体 ID、英文 prompt 前缀一致 |
| costume | 服装是否含廓形、材质、色彩、配件、使用痕迹或功能逻辑 |
| cinematography | 是否固定为纯色背景全身定妆照，而非剧情场景或环境肖像 |
| prompt | 英文、以主体 ID 号开头、融合全局风格和服装风格、不超过 1300 characters，且该前缀与解构主体 ID、提示词设计主体 ID 完全一致；整合对象是 `## 4. 解构` 全部有效信息，不是前后缀拼接；关键短语可回指 prompt evidence chain 与 `deconstruction_coverage` |
| fixed_visual | 是否包含 full-body costume fitting photo、solid color background、no scene environment |
| advisor_consultation | 是否按 `team.yaml` 请教项目监制顾问，问题是否具体，指导是否落入身份、服装、姿态、摄影或 prompt |
| subagents | 默认 dispatch 是否真实启动；阻断时降级记录是否完整 |
| scope | 是否未修改父级、registry、上游清单或其他 worker 范围 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为角色细目设计稿交付 |
| `pass_with_followups` | 可交付，但存在非阻断改进项 |
| `needs_rework` | 字段、风格、prompt 或锚点存在阻断问题 |
| `blocked` | 缺少上游清单、项目初始化上下文或被上层策略阻断 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: upstream_anchor | project_context | research_layer | llm_first | sections | decomposition | output_naming | costume | cinematography | prompt | fixed_visual | advisor_consultation | subagents | scope
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Research Layer Gate

研究层需逐项通过以下审查：

| gate_id | blocking_when_missing | reviewer_question |
| --- | --- | --- |
| `RESEARCH-IDENTITY` | high | 身份和故事压力是否来自清单/项目上下文，并转化为外观或姿态？ |
| `RESEARCH-OCCUPATION-CLASS` | high | 职业、阶层和资源痕迹是否转化为身体、面料、磨损、配饰或行动功能？ |
| `RESEARCH-REGION-ERA` | medium/high | 地域年代是否明确，特定文化/制度信息是否避免误写？ |
| `RESEARCH-COSTUME-CRAFT` | high | 服装是否写到剪裁、面料、层次、闭合方式、工艺或使用痕迹？ |
| `RESEARCH-BODY-POSTURE` | high | 身体姿态是否可用于纯色背景全身定妆照，而非剧情场景动作？ |
| `RESEARCH-TABOO` | critical | 项目禁区、安全风险、文化误读和固定画面禁区是否已写入 guardrails？ |
| `RESEARCH-UNCERTAINTY` | high | 低证据推演是否标明置信度和待确认项？ |
| `RESEARCH-PROMPT-CHAIN` | high | prompt 中的关键短语是否能回指 `evidence -> design decision -> prompt phrase`？ |

## Review Flow Map

```mermaid
flowchart TD
    A["待审查角色设计稿"] --> B["检查上游清单锚点"]
    B --> C["检查 north_star.yaml / team.yaml 消费"]
    C --> R["检查研究层八镜头与 prompt evidence chain"]
    R --> D["检查 LLM-first 与脚本边界"]
    D --> E["检查文件名前缀、解构主体 ID 与五个解构字段"]
    E --> F["检查服装细节与摄影字段"]
    F --> G["检查英文 prompt 长度和固定画面约束"]
    G --> H["检查 advisor consultation 与 subagent dispatch 或降级记录"]
    H --> I{"阻断 finding?"}
    I -->|"yes"| J["needs_rework / blocked"]
    I -->|"no"| K{"存在非阻断改进?"}
    K -->|"yes"| L["pass_with_followups"]
    K -->|"no"| M["pass"]
```

## Gate Rule

不得宣布完成：

- 任一设计稿缺少模板必填块。
- 英文提示词超过 1300 characters。
- 英文提示词没有以主体 ID 号开头。
- 英文提示词只拼接主体 ID、风格、服装或负向词等前缀后缀，未整合 `## 4. 解构` 的全部有效身份、外观、服装、姿态和摄影信息。
- 英文提示词使用 Midjourney `--no` 参数，而不是自然语言负向约束。
- `## 4. 解构` 下方缺少 `主体ID号：<主体ID>`，或该 ID 与 `## 5. 提示词设计` 主体 ID / 英文 prompt 前缀不一致。
- 输出文件名缺少主体 ID 前缀，或文件名前缀与 `## 4. 解构` 主体 ID、`## 5. 提示词设计` 主体 ID、英文 prompt 前缀不一致。
- 摄影字段或英文提示词把角色放进具体场景、建筑空间、街景、室内陈设或复杂环境。
- 缺少全身定妆照、纯色背景或 no scene environment 约束。
- 研究层缺少身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性或 prompt evidence chain 任一关键镜头。
- 研究内容无法说明如何转化为角色外观、服装、姿态、摄影或 prompt。
- prompt 关键短语无法回指研究证据、项目风格、`deconstruction_coverage` 或固定画面合同。
- 默认 subagents 路径启用时，缺少 `advisor_consultation_packet`，或顾问问题没有落到身份、服装、姿态、摄影、prompt evidence。
- 未消费 `north_star.yaml` 和 `team.yaml` 却声称项目风格对齐。
- 脚本生成了创作正文。
- 默认 subagent 路径被跳过且无降级说明。
- 任务改动越过 `.agents/skills/aigc/5-设计/角色/2-设计/**` 或项目输出路径。
