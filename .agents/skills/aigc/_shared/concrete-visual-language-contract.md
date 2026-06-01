# Concrete Visual Language Contract

## Purpose

本共享合同定义 `2-编导` 的画面化语言门。它不是保真剧本层的简单继承检查，而是要求编导稿中的导演判断和表演工艺在自身思考、证据、初始化 team 综合摘要消费、执行报告和最终落盘中，都使用具像、可拍、可听、可演的影视语言，避免把已经画面化的上游成果重新抽象化、概念化或解释化。

## Core Rule

`2-编导` 的 director layer 和 performance layer 可以拥有各自任务重心，但所有新增判断和内嵌表达都必须同时满足：

| dimension | required behavior | fail signal |
| --- | --- | --- |
| `concrete` | 把导演判断或表演判断落到身体、空间、道具、声音、光线、动作、停顿、表情、群像或可执行任务 | 只写"更有戏""高级感""压迫感""关系变化" |
| `anti_abstract` | 不用抽象名词替代可拍材料 | 写"命运感""规则压力""情绪张力"但没有可见/可听/可演锚点 |
| `anti_concept` | 不把主题、类型、关系、导演意图或表演概念直接当作正文成果 | 写"这是权力反转""她完成自我防御" |
| `anti_explanation` | 不直接说明因果、心理、主题和观众应理解的结论 | 写"因为他害怕所以退缩""观众会理解这是背叛" |
| `performable_or_shootable` | 编导稿回答画面/声音/空间如何显影，以及演员身体、声线、节奏和反应如何执行 | 离开文字解释后无法拍、无法演、无法听 |
| `field_embedded` | 结果必须内嵌到既有正式字段或执行证据，不新造第二体系 | 新增"导演意图说明""表演概念总结""主题阐释" |
| `faithful` | 不借具像化新增事实、对白、因果、线索、规则、人物动机或无关前史 | 用"更电影化/更有表演"扩写剧情 |

最小判断句固定为：摄影机能看见什么，演员能做什么，声音能听见什么，空间/道具如何承托；如果答案只是观众应该理解什么，则尚未完成画面化。

## Stage Consumption

| stage | must do |
| --- | --- |
| `2-编导 / director layer` | `director_substance_plan`、`peak_visual_plan`、`episode_visual_spine`、`visual_aesthetic_plan`、`atmosphere_mood_evidence`、`episode_final_image_plan` 和 `init_team_synthesis_context` 都必须带可见/可听/可执行锚点；不得只输出戏剧问题、视觉主轴、氛围意境或导演意图的抽象概念。 |
| `2-编导 / performance layer` | `psychological_reaction_evidence`、`actor_performance_control_evidence`、`dialogue_performance_evidence`、`scene_dramatic_map`、`performance_task_map`、`blocking_power_map`、`init_team_synthesis_context` 和终稿字段都必须落到演员可演的身体、声线、呼吸、停顿、空间、道具或对手反应；不得只输出情绪标签、心理结论或表演概念。 |

## Evidence Shape

执行报告或节点证据中必须能保留等价结构：

```yaml
concrete_visual_language_evidence:
  - stage: "2-编导"
    node_id: ""
    source_anchor: ""
    abstract_or_conceptual_risk: ""
    concrete_projection: ""
    target_fields:
      - ""
    sensory_or_performable_channels:
      visible: []
      audible: []
      performable: []
      spatial_or_prop: []
    risk_check:
      abstract_residue: false
      concept_residue: false
      explanatory_residue: false
      field_summary_block: false
      cinematography_overreach: false
      fact_drift: false
      new_dialogue_or_event: false
```

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `2-编导` 的导演判断、视觉主轴、氛围意境、高潮处理、终结画面、心理反应、五层表演、台词表演、潜台词行为和场面调度是否都落到可见/可听/可执行锚点？ | `GATE-BD-13` | `FAIL-BD-VISUAL-LANGUAGE` | `2-编导/steps/directing-workflow.md#N5-BD-VISUAL-LANGUAGE` / `#N6R-BD-REPAIR` | `concrete_visual_language_evidence` 记录抽象风险、具像投影、目标字段和感官/执行通道 |
| 初始化 team 综合摘要、planning evidence 和执行报告是否同样遵守画面化语言门，没有把抽象概念留在报告里而终稿字段无法消费？ | `GATE-BD-13` | `FAIL-BD-VISUAL-LANGUAGE` | 对应最早责任节点 + review repair | `init_team_synthesis_context.concrete_actionability_check`、`thinking_action_node_ledger.evidence_keys`、`concrete_visual_language_evidence` |
| 具像化是否仍保持上游保真，没有新增对白、事件、因果、线索、规则、人物动机或无关前史？ | `GATE-BD-09` | `FAIL-BD-CONTROLLED-ENRICHMENT` | `N3-BD-DIRECTOR` / `N4-BD-PERFORMANCE` | `risk_check.fact_drift=false`、`new_dialogue_or_event=false`、上游锚点 |
