# Episode Final Image Contract

## Purpose

本细则定义 `3-导演` 的每集终结画面：它是导演层面的迷你彩蛋尾钩，用最后一个可见/可听/可感受的落点吸引观众继续追更下一集。

终结画面必须同时满足三件事：

- 与下一集真实有关联，但不剧透下一集的具体事件结果、反转、对白或新信息。
- 从本集最后的剧情、情绪、视觉母题、道具状态或高点余波中丝滑顺延，不硬塞预告。
- 只落入既有剧本字段，不新增 `终结画面` 正文字段，不提前写摄影、分镜或图像提示词。
- 作为剧本正文时必须保持纯画面/纯声音/纯表演可执行，不写小说式抽象、作者解释、象征说明或文学比喻。

## Episode Final Image Pass

每集进入 LLM 草稿前，必须先按 `types/episode-final-image-type-map.md` 形成 `final_image_type_profile`，再建立 `episode_final_image_plan`，并由 `N9-DIR-DRAFT` 把它内嵌到本集最后一组既有字段中。

| axis | question | output evidence |
| --- | --- | --- |
| `source_anchor` | 本集最后哪些段落、动作、道具、环境、情绪或高点余波支撑尾钩？ | `final_image_source_anchor` |
| `next_episode_relation` | 它与下一集的真实关联是什么？若无法读取下一集，只能做项目/本集局部推断。 | `next_episode_relation` |
| `spoiler_boundary` | 哪些下一集信息不能提前显影？ | `spoiler_boundary` |
| `continuity_bridge` | 它如何从本集当前情境自然滑向下一集压力，而不是硬切预告？ | `continuity_bridge` |
| `hook_surface` | 尾钩的表层吸引力是什么：悬念、危险、关系未竟、信息差、主题定格、状态反差或情绪余韵？ | `hook_surface` |
| `method` | 使用哪一种主手法：环境描写式、道具特写式、情绪酝酿式、高潮结尾式？ | `final_image_method` |
| `field_projection` | 终结画面落入哪些既有字段？ | `final_field_projection` |
| `risk_check` | 是否新增事实、剧透下一集、制造新线索、改变事件结果或摄影越权？ | `final_image_risk_check` |

## Type Matching Contract

`episode_final_image_pass` 必须消费 `final_image_type_profile`，先判定尾钩类型再写计划：

- `final_anchor_surface=environment`：优先环境描写式，用空间、天气、光线、远处声音或环境刷新承接下一集压力。
- `final_anchor_surface=prop`：优先道具特写式，用本集已有物件状态、归属、异常或未完成动作承接未解问题。
- `final_anchor_surface=emotion`：优先情绪酝酿式，用沉默、停顿、距离、手部、群像或声音余波保留追更欲。
- `final_anchor_surface=peak_aftershock`：优先高潮结尾式，消费 `peak_visual_plan.cost_or_aftershock`，只强化高点余波。
- `spoiler_risk_level=high`：不得使用下一集具体信息，必须降级到环境描写式或情绪酝酿式。
- `next_episode_context_status=episode_local_only`：不得声称下一集事实，只能标注 `episode-local inference`。

## Method Types

| method | use when | projection rule |
| --- | --- | --- |
| `environmental_tag` / 环境描写式 | 下一集压力可以由天气、空间、光线、远处声音、门窗、街道、海雾、走廊等环境状态先露出影子 | 落入最后的 `环境描写`、`音效画面` 或 `群像画面`；只改变氛围和方向感，不让观众提前知道下一集具体发生什么。 |
| `prop_closeup_tag` / 道具特写式 | 本集已有道具、纸面、屏幕、伤痕、封口、衣角、钥匙、残页等能承接下一集问题 | 落入最后的 `道具特写` 或紧贴道具的 `对白画面`；只显影状态、归属、异常或未完成动作，不新增新功能、新线索或新规则。 |
| `emotional_brew_tag` / 情绪酝酿式 | 观众应带着关系未尽、选择未明、恐惧未落、柔软余韵或人物沉默继续追 | 落入 `对白画面`、`表情特写`、`角色动作`、`群像画面`、`心理反应` 或沉默/声音余波；不新增解释性台词。 |
| `climax_tail_tag` / 高潮结尾式 | 本集高点刚兑现，尾钩来自代价、余波、局势改变、群体迟滞或新压力逼近 | 消费 `peak_visual_plan.cost_or_aftershock`；强化高点后的状态差，不改写胜负、死亡、反转或因果。 |

## Construction Rules

- 优先从本集末场、`peak_visual_plan.cost_or_aftershock`、`episode_visual_spine.callback_targets`、关键道具状态、环境刷新、沉默反应和未完成动作中寻找尾钩。
- 若下一集正文可读，必须只提取“关联方向”，不得搬运下一集事件、台词、反转、角色登场或结果。
- 若下一集正文不可读，允许写 `next_episode_relation: episode-local inference`，只基于本集未解决压力、项目类型承诺和视觉主轴建立尾钩，不硬造下一集事实。
- 终结画面不是只能一两个镜头；可以是一段 3-6 个 beat 的尾场小段落，通过环境刷新、道具状态、人物停顿、群像位置、声音层次和空间方向共同完成收束。
- 终结画面应准、可拍、余味强；它是最后一组画面/声音/动作落点，不是结尾说明、剧情总结或预告词。
- 避免“像/仿佛/象征/意味着/命运/下一处账目”等小说化或评论式表达；若需要意境，改用具体光线、湿度、物件运动、身体距离、门窗开合、船灯位置、声源方向和停顿节奏。
- 尾钩必须能被下游摄影和分组消费，但 `3-导演` 只写导演/演员/声画可执行材料，不写机位、景别、镜头运动或分镜编号。

## Boundary

允许：

- 使用本集已有环境、道具、声音、群像、表演和高点余波制造追更欲望。
- 让尾钩与下一集主题、压力、关系、空间或未解信息方向有关联。
- 通过留白、异常状态、声音余波、道具未归位、人物未出口反应制造小悬念。

禁止：

- 剧透下一集具体事件、反转、死亡、胜负、告白、规则答案、新角色身份或关键对白。
- 为了尾钩新增本集没有的道具、线索、规则、伤势、来信、系统提示、灾害、追兵或人物动机。
- 把终结画面写成“下一集预告”“敬请期待”“他不知道的是...”或作者式解释。
- 在逐集正文中新增 `终结画面：` 字段；证据写入执行报告，正文只使用既有字段。

## Review Checklist

- 本集是否有明确的 `episode_final_image_plan`？
- 尾钩是否与下一集真实有关联，或在下一集不可读时明确为本集局部推断？
- 是否没有剧透下一集具体事件、结果、台词或新信息？
- 是否从本集内容丝滑顺延，而不是硬塞预告？
- 是否使用了环境描写式、道具特写式、情绪酝酿式或高潮结尾式之一？
- 是否落入既有字段，并保持保真、对白冻结、无摄影越权？
