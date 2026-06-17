# Scene Pressure Texture Contract

本文件把旧影视“氛围强化”的可取部分迁移为小说初稿的“场景压力与感官承托”规则。它只服务 `3-初稿/SKILL.md#N5-CREATIVE-DRAFT`，不得成为独立氛围层、五感清单或装饰性环境段落。

## Core Principle

场景不是为了“有氛围”，而是承托人物行动、信息延迟、关系压力、空间阻隔和章末牵引。感官颗粒必须推动当前戏，不能变成天气、气味、光线或声音的孤立描写。

## Texture Checks

| check | requirement |
| --- | --- |
| `scene_pressure_anchor` | 场景细节必须服务冲突、危险、遮蔽、误会、关系压迫或行动限制。 |
| `object_or_space_trigger` | 现场发现优先来自物件、门槛、桌面、衣物、血迹、脚步、纸张、灯、墙面、距离或遮挡。 |
| `sound_or_silence` | 声音和沉默应承担信息延迟、威胁接近、尴尬、谎言或决断。 |
| `sensory_selectivity` | 每段只选最有效的 1-2 类感官，不追求五感覆盖。 |
| `environment_reaction` | 环境变化应由人物动作、道具、天气事实、空间结构或既有设定触发。 |
| `reader_pull` | 场景颗粒要推动读者追问“接下来会怎样”，而不是停在审美展示。 |

## Prohibitions

- 不为氛围新增 source 没有的雨、雪、烟、火、风、光源、气味或人群。
- 不把“压抑、宿命、诗意、高级、电影感”当成正文效果词。
- 不用天气和光影抢走人物动作链。
- 不把场景描写写成独立装饰段落，打断冲突推进。
- 不机械追求视觉、听觉、触觉、嗅觉和时间感全覆盖。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 场景颗粒是否服务冲突、信息、关系、空间限制或章末牵引？ | `scene_pressure_texture` | `FAIL-DRAFT-PRESENCE-TEXTURE` | `N5-CREATIVE-DRAFT` | `scene_pressure_texture_profile` |
| 感官和环境描写是否少而准，没有为了氛围新增事实或打断人物动作链？ | `prose_reader_pull` | `FAIL-DRAFT-PROSE-PULL` | `N5-CREATIVE-DRAFT` | offending excerpt |
